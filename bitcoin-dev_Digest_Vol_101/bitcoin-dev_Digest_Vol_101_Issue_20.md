Send bitcoin-dev mailing list submissions to
	bitcoin-dev@lists.linuxfoundation.org

To subscribe or unsubscribe via the World Wide Web, visit
	https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
or, via email, send a message with subject or body 'help' to
	bitcoin-dev-request@lists.linuxfoundation.org

You can reach the person managing the list at
	bitcoin-dev-owner@lists.linuxfoundation.org

When replying, please edit your Subject line so it is more specific
than "Re: Contents of bitcoin-dev digest..."


Today's Topics:

   1. Re: [Lightning-dev] Batch exchange withdrawal to	lightning
      requires covenants (Bastien TEINTURIER)
   2. Re: [Lightning-dev] Batch exchange withdrawal to	lightning
      requires covenants (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Wed, 18 Oct 2023 16:35:40 +0200
From: Bastien TEINTURIER <bastien@acinq.fr>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Batch exchange withdrawal
	to	lightning requires covenants
Message-ID:
	<CACdvm3OJsg2Br91aDL8=eACTW1WkdQcUSCvpWyniuEZf+qSAuA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hey Z-man, Antoine,

Thank you for your feedback, responses inline.

z-man:

> Then if I participate in a batched splice, I can disrupt the batched
> splice by broadcasting the old state and somehow convincing miners to
> confirm it before the batched splice.

Correct, I didn't mention it in my post but batched splices cannot use
0-conf, the transaction must be confirmed to remove the risk of double
spends using commit txs associated with the previous funding tx.

But interestingly, with the protocol I drafted, the LSP can finalize and
broadcast the batched splice transaction while users are offline. With a
bit of luck, when the users reconnect, that transaction will already be
confirmed so it will "feel 0-conf".

Also, we need a mechanism like the one you describe when we detect that
a splice transaction has been double-spent. But this isn't specific to
batched transactions, 2-party splice transactions can also be double
spent by either participant. So we need that mechanism anyway? The spec
doesn't have a way of aborting a splice after exchanging signatures, but
you can always do it as an RBF operation (which actually just does a
completely different splice). This is what Greg mentioned in his answer.

> part of the splice proposal is that while a channel is being spliced,
> it should not be spliced again, which your proposal seems to violate.

The spec doesn't require that, I'm not sure what made you think that.
While a channel is being spliced, it can definitely be spliced again as
an RBF attempt (this is actually a very important feature), which double
spends the other unconfirmed splice attempts.

ariard:

> It is uncertain to me if secure fee-bumping, even with future
> mechanisms like package relay and nversion=3, is robust enough for
> multi-party transactions and covenant-enable constructions under usual
> risk models.

I'm not entirely sure why you're bringing this up in this context...
I agree that we most likely cannot use RBF on those batched transactions
we will need to rely on CPFP and potentially package relay. But why is
it different from non-multi-party transactions here?

> See test here:
>
https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf

I'd argue that this is quite different from the standard replacement
cycling attack, because in this protocol wallet users can only
unilaterally double-spend with a commit tx, on which they cannot set
the feerate. The only participant that can "easily" double-spend is
the exchange, and they wouldn't have an incentive to here, users are
only withdrawing funds, there's no opportunity of stealing funds?

Thanks,
Bastien

Le mar. 17 oct. 2023 ? 21:10, Antoine Riard <antoine.riard@gmail.com> a
?crit :

> Hi Bastien,
>
> > The naive way of enabling lightning withdrawals is to make the user
> > provide a lightning invoice that the exchange pays over lightning. The
> > issue is that in most cases, this simply shifts the burden of making an
> > on-chain transaction to the user's wallet provider: if the user doesn't
> > have enough inbound liquidity (which is likely), a splice transaction
> > will be necessary. If N users withdraw funds from an exchange, we most
> > likely will end up with N separate splice transactions.
>
> It is uncertain to me if secure fee-bumping, even with future mechanisms
> like package relay and nversion=3, is robust enough for multi-party
> transactions and covenant-enable constructions under usual risk models.
>
> See test here:
>
> https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf
>
> Appreciated expert eyes of folks understanding both lightning and core
> mempool on this.
> There was a lot of back and forth on nversion=3 design rules, though the
> test is normally built on glozow top commit of the 3 Oct 2023.
>
> Best,
> Antoine
>
> Le mar. 17 oct. 2023 ? 14:03, Bastien TEINTURIER <bastien@acinq.fr> a
> ?crit :
>
>> Good morning list,
>>
>> I've been trying to design a protocol to let users withdraw funds from
>> exchanges directly into their lightning wallet in an efficient way
>> (with the smallest on-chain footprint possible).
>>
>> I've come to the conclusion that this is only possible with some form of
>> covenants (e.g. `SIGHASH_ANYPREVOUT` would work fine in this case). The
>> goal of this post is to explain why, and add this usecase to the list of
>> useful things we could do if we had covenants (insert "wen APO?" meme).
>>
>> The naive way of enabling lightning withdrawals is to make the user
>> provide a lightning invoice that the exchange pays over lightning. The
>> issue is that in most cases, this simply shifts the burden of making an
>> on-chain transaction to the user's wallet provider: if the user doesn't
>> have enough inbound liquidity (which is likely), a splice transaction
>> will be necessary. If N users withdraw funds from an exchange, we most
>> likely will end up with N separate splice transactions.
>>
>> Hence the idea of batching those into a single transaction. Since we
>> don't want to introduce any intermediate transaction, we must be able
>> to create one transaction that splices multiple channels at once. The
>> issue is that for each of these channels, we need a signature from the
>> corresponding wallet user, because we're spending the current funding
>> output, which is a 2-of-2 multisig between the wallet user and the
>> wallet provider. So we run into the usual availability problem: we need
>> signatures from N users who may not be online at the same time, and if
>> one of those users never comes online or doesn't complete the protocol,
>> we must discard the whole batch.
>>
>> There is a workaround though: each wallet user can provide a signature
>> using `SIGHASH_SINGLE | SIGHASH_ANYONECANPAY` that spends their current
>> funding output to create a new funding output with the expected amount.
>> This lets users sign *before* knowing the final transaction, which the
>> exchange can create by batching pairs of inputs/outputs. But this has
>> a fatal issue: at that point the wallet user has no way of spending the
>> new funding output (since it is also a 2-of-2 between the wallet user
>> and the wallet provider). The wallet provider can now blackmail the user
>> and force them to pay to get their funds back.
>>
>> Lightning normally fixes this by exchanging signatures for a commitment
>> transaction that sends the funds back to their owners *before* signing
>> the parent funding/splice transaction. But here that is impossible,
>> because we don't know yet the `txid` of the batch transaction (that's
>> the whole point, we want to be able to sign before creating the batch)
>> so we don't know the new `prevout` we should spend from. I couldn't find
>> a clever way to work around that, and I don't think there is one (but
>> I would be happy to be wrong).
>>
>> With `SIGHASH_ANYPREVOUT`, this is immediately fixed: we can exchange
>> anyprevout signatures for the commitment transaction, and they will be
>> valid to spend from the batch transaction. We are safe from signature
>> reuse, because funding keys are rotated at each splice so we will never
>> create another output that uses the same 2-of-2 script.
>>
>> I haven't looked at other forms of covenants, but most of them likely
>> address this problem as well.
>>
>> Cheers,
>> Bastien
>> _______________________________________________
>> Lightning-dev mailing list
>> Lightning-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/lightning-dev
>>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231018/a8b93b35/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 18 Oct 2023 19:03:48 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Bastien TEINTURIER <bastien@acinq.fr>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Batch exchange withdrawal
	to	lightning requires covenants
Message-ID:
	<CALZpt+EwwQJo16_5tWVBz6xRZ-O0q7S+JCuJm9hwGMrrgsdRjw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Bastien,

Thanks for the answer.

If I understand correctly the protocol you're describing you're aiming to
enable batched withdrawals where a list of users are being sent funds from
an exchange directly in a list of channel funding outputs ("splice-out").
Those channels funding outputs are 2-of-2, between two lambda users or e.g
a lambda user and a LSP.

If I'm correct, two users can cooperate maliciously against the batch
withdrawal transactions by re-signing a CPFP from 2-of-2 and broadcasting
the batch withdrawal as a higher-feerate package / high fee package and
then evicting out the CPFP.

If the batch withdrawal has been signed with 0-fee thanks to the nversion=3
policy exemption, it will be evicted out of the mempool. A variant of a
replacement cycling attack.

I think this more or less matches the test I'm pointing to you which is on
non-deployed package acceptance code:
https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf

Please correct me if I'm wrong or missing assumptions. Agree with you on
the assumptions that the exchange does not have an incentive to
double-spend its own withdrawal transactions, or if all the batched funding
outputs are shared with a LSP, malicious collusion is less plausible.

Best,
Antoine

Le mer. 18 oct. 2023 ? 15:35, Bastien TEINTURIER <bastien@acinq.fr> a
?crit :

> Hey Z-man, Antoine,
>
> Thank you for your feedback, responses inline.
>
> z-man:
>
> > Then if I participate in a batched splice, I can disrupt the batched
> > splice by broadcasting the old state and somehow convincing miners to
> > confirm it before the batched splice.
>
> Correct, I didn't mention it in my post but batched splices cannot use
> 0-conf, the transaction must be confirmed to remove the risk of double
> spends using commit txs associated with the previous funding tx.
>
> But interestingly, with the protocol I drafted, the LSP can finalize and
> broadcast the batched splice transaction while users are offline. With a
> bit of luck, when the users reconnect, that transaction will already be
> confirmed so it will "feel 0-conf".
>
> Also, we need a mechanism like the one you describe when we detect that
> a splice transaction has been double-spent. But this isn't specific to
> batched transactions, 2-party splice transactions can also be double
> spent by either participant. So we need that mechanism anyway? The spec
> doesn't have a way of aborting a splice after exchanging signatures, but
> you can always do it as an RBF operation (which actually just does a
> completely different splice). This is what Greg mentioned in his answer.
>
> > part of the splice proposal is that while a channel is being spliced,
> > it should not be spliced again, which your proposal seems to violate.
>
> The spec doesn't require that, I'm not sure what made you think that.
> While a channel is being spliced, it can definitely be spliced again as
> an RBF attempt (this is actually a very important feature), which double
> spends the other unconfirmed splice attempts.
>
> ariard:
>
> > It is uncertain to me if secure fee-bumping, even with future
> > mechanisms like package relay and nversion=3, is robust enough for
> > multi-party transactions and covenant-enable constructions under usual
> > risk models.
>
> I'm not entirely sure why you're bringing this up in this context...
> I agree that we most likely cannot use RBF on those batched transactions
> we will need to rely on CPFP and potentially package relay. But why is
> it different from non-multi-party transactions here?
>
> > See test here:
> >
> https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf
>
> I'd argue that this is quite different from the standard replacement
> cycling attack, because in this protocol wallet users can only
> unilaterally double-spend with a commit tx, on which they cannot set
> the feerate. The only participant that can "easily" double-spend is
> the exchange, and they wouldn't have an incentive to here, users are
> only withdrawing funds, there's no opportunity of stealing funds?
>
> Thanks,
> Bastien
>
> Le mar. 17 oct. 2023 ? 21:10, Antoine Riard <antoine.riard@gmail.com> a
> ?crit :
>
>> Hi Bastien,
>>
>> > The naive way of enabling lightning withdrawals is to make the user
>> > provide a lightning invoice that the exchange pays over lightning. The
>> > issue is that in most cases, this simply shifts the burden of making an
>> > on-chain transaction to the user's wallet provider: if the user doesn't
>> > have enough inbound liquidity (which is likely), a splice transaction
>> > will be necessary. If N users withdraw funds from an exchange, we most
>> > likely will end up with N separate splice transactions.
>>
>> It is uncertain to me if secure fee-bumping, even with future mechanisms
>> like package relay and nversion=3, is robust enough for multi-party
>> transactions and covenant-enable constructions under usual risk models.
>>
>> See test here:
>>
>> https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf
>>
>> Appreciated expert eyes of folks understanding both lightning and core
>> mempool on this.
>> There was a lot of back and forth on nversion=3 design rules, though the
>> test is normally built on glozow top commit of the 3 Oct 2023.
>>
>> Best,
>> Antoine
>>
>> Le mar. 17 oct. 2023 ? 14:03, Bastien TEINTURIER <bastien@acinq.fr> a
>> ?crit :
>>
>>> Good morning list,
>>>
>>> I've been trying to design a protocol to let users withdraw funds from
>>> exchanges directly into their lightning wallet in an efficient way
>>> (with the smallest on-chain footprint possible).
>>>
>>> I've come to the conclusion that this is only possible with some form of
>>> covenants (e.g. `SIGHASH_ANYPREVOUT` would work fine in this case). The
>>> goal of this post is to explain why, and add this usecase to the list of
>>> useful things we could do if we had covenants (insert "wen APO?" meme).
>>>
>>> The naive way of enabling lightning withdrawals is to make the user
>>> provide a lightning invoice that the exchange pays over lightning. The
>>> issue is that in most cases, this simply shifts the burden of making an
>>> on-chain transaction to the user's wallet provider: if the user doesn't
>>> have enough inbound liquidity (which is likely), a splice transaction
>>> will be necessary. If N users withdraw funds from an exchange, we most
>>> likely will end up with N separate splice transactions.
>>>
>>> Hence the idea of batching those into a single transaction. Since we
>>> don't want to introduce any intermediate transaction, we must be able
>>> to create one transaction that splices multiple channels at once. The
>>> issue is that for each of these channels, we need a signature from the
>>> corresponding wallet user, because we're spending the current funding
>>> output, which is a 2-of-2 multisig between the wallet user and the
>>> wallet provider. So we run into the usual availability problem: we need
>>> signatures from N users who may not be online at the same time, and if
>>> one of those users never comes online or doesn't complete the protocol,
>>> we must discard the whole batch.
>>>
>>> There is a workaround though: each wallet user can provide a signature
>>> using `SIGHASH_SINGLE | SIGHASH_ANYONECANPAY` that spends their current
>>> funding output to create a new funding output with the expected amount.
>>> This lets users sign *before* knowing the final transaction, which the
>>> exchange can create by batching pairs of inputs/outputs. But this has
>>> a fatal issue: at that point the wallet user has no way of spending the
>>> new funding output (since it is also a 2-of-2 between the wallet user
>>> and the wallet provider). The wallet provider can now blackmail the user
>>> and force them to pay to get their funds back.
>>>
>>> Lightning normally fixes this by exchanging signatures for a commitment
>>> transaction that sends the funds back to their owners *before* signing
>>> the parent funding/splice transaction. But here that is impossible,
>>> because we don't know yet the `txid` of the batch transaction (that's
>>> the whole point, we want to be able to sign before creating the batch)
>>> so we don't know the new `prevout` we should spend from. I couldn't find
>>> a clever way to work around that, and I don't think there is one (but
>>> I would be happy to be wrong).
>>>
>>> With `SIGHASH_ANYPREVOUT`, this is immediately fixed: we can exchange
>>> anyprevout signatures for the commitment transaction, and they will be
>>> valid to spend from the batch transaction. We are safe from signature
>>> reuse, because funding keys are rotated at each splice so we will never
>>> create another output that uses the same 2-of-2 script.
>>>
>>> I haven't looked at other forms of covenants, but most of them likely
>>> address this problem as well.
>>>
>>> Cheers,
>>> Bastien
>>> _______________________________________________
>>> Lightning-dev mailing list
>>> Lightning-dev@lists.linuxfoundation.org
>>> https://lists.linuxfoundation.org/mailman/listinfo/lightning-dev
>>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231018/b61abc54/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 20
********************************************
