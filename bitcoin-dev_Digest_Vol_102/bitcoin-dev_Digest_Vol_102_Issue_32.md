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

   1. Re: Ordinals BIP PR (Kostas Karasavvas)
   2. Re: Ordinals BIP PR (vjudeu@gazeta.pl)
   3. Re: Ordinals BIP PR (Kostas Karasavvas)


----------------------------------------------------------------------

Message: 1
Date: Tue, 21 Nov 2023 14:13:55 +0200
From: Kostas Karasavvas <kkarasavvas@gmail.com>
To: vjudeu@gazeta.pl,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CABE6yHtoj_bp18h-pouk_Ja27o6h7PTR-XsgvQgvLutpG5702w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Please see inline.

On Tue, Nov 21, 2023 at 3:21?AM vjudeu via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> > I've commented a few times asking the BIP editors to let me know what is
> needed for the BIP to either be merged or rejected.
>
> I would accept it, if each Ordinal would require including OP_RETURN at
> the beginning of the TapScript, to prevent them from being pushed on-chain.
> In that case, they could still be moved by a single Schnorr signature.
>

I am not sure I understand this. The data are published when spending the
taproot (in the witness). Since it is spent it does not bloat the mempool.
Regardless of OP_RETURN the data will be on chain. What am I missing?


> Or, even better, creating a new Ordinal should not require sending them to
> Taproot at all, but just the R-value of a signature, from any address type,
> should be sufficient to make a commitment.
>
> Which means, if some user has some legacy address, then it should be
> possible to sign a regular transaction, and then, R-value of that signature
> could contain some Ordinal.
>
>
Actually, wrt to ordinals design I agree with comments like this suggesting
a different design. Why? I understand that the BIP process is fundamentally
to discuss a proposal. Something is suggested people tweak on it, improve
it and when they agree they might assign it a number. To Casey (and to
other contributors), you designed ordinals without consulting this list,
you finalized the design, created an implementation and it is running for
months and now you are submitting it for a BIP; i.e. asking for legitimacy
after the fact? Shouldn't people agree/disagree with the design?

Why do you want ordinals as a BIP (apologies if you explained this before
and I missed it)?
1) If you don't care about legitimacy then ordinals is live, you are good
to go.
2) If you are asking legitimacy then you should accept potential design
modifications like the one mentioned above.
3) If you want the BIP for standardisation it makes no sense. People can
design similar protocols anyway. It's permissionless.
4) For another reason?


> Also, Ordinals should support scanning the chain in a similar way as
> Silent Payments could do. Which means, users should not be forced to upload
> data, if they were already uploaded in a different form. For example, there
> was a user, trying to upload the whitepaper, even though it was already
> done, and it was wrapped in a multisig in some old transaction. Which
> means, Ordinals should allow scanning the chain, and discovering old data,
> without reinventing the wheel, and forcing users to post that data again
> on-chain.
>
> Another thing to address is the content of each Ordinal: some people tried
> to create something like NFT. In that case, the uniqueness should be
> enforced. And by scanning the chain for similar data, it should note that
> "hey, the whitepaper was already pushed by someone, in a multisig, long
> time ago", so the Ordinals protocol should prevent users from uploading the
> same data again, and again. Because in some use cases, like NFTs, it could
> be misleading.
>

I don't agree with this. This seems to be a business logic change and not a
technical one. People can and will create other similar protocols that
force (or not) uniqueness regardless of what ordinals do.

Besides, in any chain, NFTs can only enforce uniqueness per contract. A
different contract can have exactly the same NFTs. Uniqueness is kind-of
acquired because of the legitimacy of the person who issued the collection.

Re this BIP proposal:
I would not have an issue to accept this proposal if it was submitted for
discussion beforehand. If there was no need for people in this list to
discuss it before I don't see why a BIP is needed now.

Regards,
Kostas




> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>


-- 
https://twitter.com/kkarasavvas
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231121/7e399527/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 22 Nov 2023 00:10:55 +0100
From: vjudeu@gazeta.pl
To: Kostas Karasavvas <kkarasavvas@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<196658683-e78610e544d8c89fc4432671990127cb@pmq1v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> Since it is spent it does not bloat the mempool.
?
This is not the case. If you post some 100 kB TapScript, with some Ordinal, then it of course bloats mempools, because then other users could post 100 kB less, when it comes to regular payments. If you have Ordinals in the current form, then they take place of regular payments. Which means, you can include some payment, or some data. You cannot include both, because you can produce 4 MB block per 10 minutes. It is always a choice: confirm this payment, or confirm that data.
?
> Regardless of OP_RETURN the data will be on chain. What am I missing?
?
If you have regular OP_RETURN, the data is pushed on-chain. However, if your OP_RETURN is part of your TapScript, then you cannot provide any valid input to satisfy that kind of TapScript, so it cannot be pushed on-chain. Which means, you have to use another TapScript branch, without OP_RETURN, or simply spend by key. Note that regular OP_RETURNs are placed in transaction outputs, but in that case, TapScript is revealed in transaction input (and to be more specific, in the witness part), which prevents from posting a commitment on-chain, if it contains OP_RETURN at the beginning of the TapScript.
?
> If there was no need for people in this list to discuss it before I don't see why a BIP is needed now.
?
It is needed, but for a different reason. There should be a BIP, but not to promote Ordinals, but to handle them properly, and to provide regular users a way, to compete with the currently posted Ordinals, in this fee-based competition. Which means, regular users should have a way, to turn their Ordinals into proper commitments. They should be hidden behind some R-value, instead of being posted as a TapScript, and fully revealed in the witness. That would make it smaller, cheaper, and will provide more room for more regular payments, while preserving the strong cryptographical proof, that a given data is connected with a given transaction input.
?
Also, it would allow them to be uncensorable, because then users could decide to hide any Ordinal behind their signature, in any address type (it works even on P2PK), and then reveal it later, but not on-chain, to not take a room of other regular payments. In general, transactions should always contain payments, and Ordinals could be attached as a feature, and not the other way around, when the actual payment is just a feature to be discarded, and the posted data is what people care about. Bitcoin is a payment system first, and not a P2P cloud storage, so it should work as "always a payment, and optionally also an Ordinal", and not "just a data push, and unfortunately a payment, because the protocol forced us to include some satoshis".
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231122/a989ef1f/attachment.html>

------------------------------

Message: 3
Date: Wed, 22 Nov 2023 13:27:03 +0200
From: Kostas Karasavvas <kkarasavvas@gmail.com>
To: vjudeu@gazeta.pl
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CABE6yHsstgUBTC+5FU+LiHMTAkLJDCynNthCRosOBjpAAS1-MA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Wed, Nov 22, 2023 at 1:11?AM <vjudeu@gazeta.pl> wrote:

> > Since it is spent it does not bloat the mempool.
>
> This is not the case. If you post some 100 kB TapScript, with some
> Ordinal, then it of course bloats mempools, because then other users could
> post 100 kB less, when it comes to regular payments. If you have Ordinals
> in the current form, then they take place of regular payments. Which means,
> you can include some payment, or some data. You cannot include both,
> because you can produce 4 MB block per 10 minutes. It is always a choice:
> confirm this payment, or confirm that data.
>
>

I meant the UTXO set, not the mempool. But still, even for the mempool,
since tx fees are paid I don't see it as bloat. It is competing with the
other txs and won. The bloat is of course in storage since the blocks are
'fuller' with ordinals... but that is the whole point of ordinals (see
below).


> > Regardless of OP_RETURN the data will be on chain. What am I missing?
>
> If you have regular OP_RETURN, the data is pushed on-chain. However, if
> your OP_RETURN is part of your TapScript, then you cannot provide any valid
> input to satisfy that kind of TapScript, so it cannot be pushed on-chain.
> Which means, you have to use another TapScript branch, without OP_RETURN,
> or simply spend by key. Note that regular OP_RETURNs are placed in
> transaction outputs, but in that case, TapScript is revealed in transaction
> input (and to be more specific, in the witness part), which prevents from
> posting a commitment on-chain, if it contains OP_RETURN at the beginning of
> the TapScript.
>

I see, thanks.


> > If there was no need for people in this list to discuss it before I
> don't see why a BIP is needed now.
>
> It is needed, but for a different reason. There should be a BIP, but not
> to promote Ordinals, but to handle them properly, and to provide regular
> users a way, to compete with the currently posted Ordinals, in this
> fee-based competition. Which means, regular users should have a way, to
> turn their Ordinals into proper commitments. They should be hidden behind
> some R-value, instead of being posted as a TapScript, and fully revealed in
> the witness. That would make it smaller, cheaper, and will provide more
> room for more regular payments, while preserving the strong cryptographical
> proof, that a given data is connected with a given transaction input.
>
> Also, it would allow them to be uncensorable, because then users could
> decide to hide any Ordinal behind their signature, in any address type (it
> works even on P2PK), and then reveal it later, but not on-chain, to not
> take a room of other regular payments. In general, transactions should
> always contain payments, and Ordinals could be attached as a feature, and
> not the other way around, when the actual payment is just a feature to be
> discarded, and the posted data is what people care about. Bitcoin is a
> payment system first, and not a P2P cloud storage, so it should work as
> "always a payment, and optionally also an Ordinal", and not "just a data
> push, and unfortunately a payment, because the protocol forced us to
> include some satoshis".
>

The whole point of ordinals is supposed to have the data on-chain (the
ordinals team can correct me). You are not suggesting merely a technical
design change, you are suggesting a completely different design and
business logic, which I believe would never be accepted by the ordinals
team*, and thus no point for this BIP now. We'll just have to wait for
their reply and see.

* This is fair game for a new competing project. However, the 'on-chain'
part is the main ordinals selling point so a new project would not even be
competing.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231122/c04112d4/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 32
********************************************
