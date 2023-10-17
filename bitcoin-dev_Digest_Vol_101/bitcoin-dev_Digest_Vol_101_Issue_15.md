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

   1. Batch exchange withdrawal to lightning requires	covenants
      (Bastien TEINTURIER)
   2. Re: Batch exchange withdrawal to lightning requires	covenants
      (ZmnSCPxj)
   3. Re: Batch exchange withdrawal to lightning requires	covenants
      (Greg Sanders)
   4. Re: Batch exchange withdrawal to lightning requires	covenants
      (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Tue, 17 Oct 2023 15:03:05 +0200
From: Bastien TEINTURIER <bastien@acinq.fr>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Batch exchange withdrawal to lightning requires
	covenants
Message-ID:
	<CACdvm3MuKmzQ1EFMJDc0ahhrG6xpD6Rr9Vh=ZTpVHa12ZALB0w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Good morning list,

I've been trying to design a protocol to let users withdraw funds from
exchanges directly into their lightning wallet in an efficient way
(with the smallest on-chain footprint possible).

I've come to the conclusion that this is only possible with some form of
covenants (e.g. `SIGHASH_ANYPREVOUT` would work fine in this case). The
goal of this post is to explain why, and add this usecase to the list of
useful things we could do if we had covenants (insert "wen APO?" meme).

The naive way of enabling lightning withdrawals is to make the user
provide a lightning invoice that the exchange pays over lightning. The
issue is that in most cases, this simply shifts the burden of making an
on-chain transaction to the user's wallet provider: if the user doesn't
have enough inbound liquidity (which is likely), a splice transaction
will be necessary. If N users withdraw funds from an exchange, we most
likely will end up with N separate splice transactions.

Hence the idea of batching those into a single transaction. Since we
don't want to introduce any intermediate transaction, we must be able
to create one transaction that splices multiple channels at once. The
issue is that for each of these channels, we need a signature from the
corresponding wallet user, because we're spending the current funding
output, which is a 2-of-2 multisig between the wallet user and the
wallet provider. So we run into the usual availability problem: we need
signatures from N users who may not be online at the same time, and if
one of those users never comes online or doesn't complete the protocol,
we must discard the whole batch.

There is a workaround though: each wallet user can provide a signature
using `SIGHASH_SINGLE | SIGHASH_ANYONECANPAY` that spends their current
funding output to create a new funding output with the expected amount.
This lets users sign *before* knowing the final transaction, which the
exchange can create by batching pairs of inputs/outputs. But this has
a fatal issue: at that point the wallet user has no way of spending the
new funding output (since it is also a 2-of-2 between the wallet user
and the wallet provider). The wallet provider can now blackmail the user
and force them to pay to get their funds back.

Lightning normally fixes this by exchanging signatures for a commitment
transaction that sends the funds back to their owners *before* signing
the parent funding/splice transaction. But here that is impossible,
because we don't know yet the `txid` of the batch transaction (that's
the whole point, we want to be able to sign before creating the batch)
so we don't know the new `prevout` we should spend from. I couldn't find
a clever way to work around that, and I don't think there is one (but
I would be happy to be wrong).

With `SIGHASH_ANYPREVOUT`, this is immediately fixed: we can exchange
anyprevout signatures for the commitment transaction, and they will be
valid to spend from the batch transaction. We are safe from signature
reuse, because funding keys are rotated at each splice so we will never
create another output that uses the same 2-of-2 script.

I haven't looked at other forms of covenants, but most of them likely
address this problem as well.

Cheers,
Bastien
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231017/8902099c/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 17 Oct 2023 17:04:06 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Bastien TEINTURIER <bastien@acinq.fr>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Batch exchange withdrawal to lightning
	requires	covenants
Message-ID:
	<Ckp3N2cHGyyFyTp8IkjqYwnXsef1KxzhFs9vHQvFCpdWKUCrCfpxLBAgIXsKEtTNQqvfdyywt7weJd2pVz8UKn6egfRy46-xd17pnltcQyU=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Bastien,

I have not gotten around to posting it yet, but I have a write-up in my computer with the title:

> Batched Splicing Considered Risky

The core of the risk is that if:

* I have no funds right now in a channel (e.g. the LSP allowed me to have 0 reserve, or this is a newly-singlefunded channel from the LSP to me).
* I have an old state (e.g. for a newly-singlefunded channel, it could have been `update_fee`d, so that the initial transaction is old state).

Then if I participate in a batched splice, I can disrupt the batched splice by broadcasting the old state and somehow convincing miners to confirm it before the batched splice.

Thus, it is important for *any* batched splicing mechanism to have a backout, where if the batched splice transaction can no longer be confirmed due to some participant disrupting it by posting an old commitment transaction, either a subset of the splice is re-created or the channels revert back to pre-splice state (with knowledge that the post-splice state can no longer be confirmed).

I know that current splicing tech is to run both the pre-splice and post-splice state simultaneously until the splicing transaction is confirmed.
However we need to *also* check if the splicing transaction *cannot* be confirmed --- by checking if the other inputs to the splice transaction were already consumed by transactions that have deeply confirmed, and in that case, to drop the post-splice state and revert to the pre-splice state.
I do not know if existing splice implementations actually perform such a check.
Unless all splice implementations do this, then any kind of batched splicing is risky.

Regards,
ZmnSCPxj



------------------------------

Message: 3
Date: Tue, 17 Oct 2023 13:10:42 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: "lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Batch exchange withdrawal to lightning
	requires	covenants
Message-ID:
	<CAB3F3Dtb2s7gCjV6ok3=XjOx174DEuRksij4GOoFD20atwJfig@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> I do not know if existing splice implementations actually perform such a
check.
Unless all splice implementations do this, then any kind of batched
splicing is risky.

As long as the implementation decides to splice again at some point when a
prior
splice isn't confirming, it will self-resolve once any subsequent splice is
confirmed.

Cheers,
Greg

On Tue, Oct 17, 2023 at 1:04?PM ZmnSCPxj via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Good morning Bastien,
>
> I have not gotten around to posting it yet, but I have a write-up in my
> computer with the title:
>
> > Batched Splicing Considered Risky
>
> The core of the risk is that if:
>
> * I have no funds right now in a channel (e.g. the LSP allowed me to have
> 0 reserve, or this is a newly-singlefunded channel from the LSP to me).
> * I have an old state (e.g. for a newly-singlefunded channel, it could
> have been `update_fee`d, so that the initial transaction is old state).
>
> Then if I participate in a batched splice, I can disrupt the batched
> splice by broadcasting the old state and somehow convincing miners to
> confirm it before the batched splice.
>
> Thus, it is important for *any* batched splicing mechanism to have a
> backout, where if the batched splice transaction can no longer be confirmed
> due to some participant disrupting it by posting an old commitment
> transaction, either a subset of the splice is re-created or the channels
> revert back to pre-splice state (with knowledge that the post-splice state
> can no longer be confirmed).
>
> I know that current splicing tech is to run both the pre-splice and
> post-splice state simultaneously until the splicing transaction is
> confirmed.
> However we need to *also* check if the splicing transaction *cannot* be
> confirmed --- by checking if the other inputs to the splice transaction
> were already consumed by transactions that have deeply confirmed, and in
> that case, to drop the post-splice state and revert to the pre-splice state.
> I do not know if existing splice implementations actually perform such a
> check.
> Unless all splice implementations do this, then any kind of batched
> splicing is risky.
>
> Regards,
> ZmnSCPxj
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231017/831a1dfc/attachment-0001.html>

------------------------------

Message: 4
Date: Tue, 17 Oct 2023 17:17:04 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Batch exchange withdrawal to lightning
	requires	covenants
Message-ID:
	<xq5SXj5Qx2uuhwui_Xoc0K0WBxoJj98cYBCoumHLi101ofbMCET_-4athmHvDvDl0H9GKHlsRo73j9iUuSx9OmHbfQNjDDYAx-JzFNLMNtI=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


Good morning Greg,


> > I do not know if existing splice implementations actually perform such a check.
> Unless all splice implementations do this, then any kind of batched splicing is risky.
> As long as the implementation decides to splice again at some point when a prior
> splice isn't confirming, it will self-resolve once any subsequent splice is confirmed.

Do note that there is a risk here that the reason for "not confirming" is because of an unexpected increase in mempool usage.

In particular, if the attack is not being performed, it is possible for the previous splice tx that was not confirming for a while, to be the one that confirms in the end, instead of the subsequent splice.
This is admittedly an edge case, but one that could potentially be specifically attacked and could lead to loss of funds if the implementations naively deleted the signatures for commitment transactions for the previously-not-confirming splice transaction.

Indeed, as I understood it, part of the splice proposal is that while a channel is being spliced, it should not be spliced again, which your proposal seems to violate.

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 15
********************************************
