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

   1. Re: Ark: An Alternative Privacy-preserving Second	Layer
      Solution (G. Andrew Stone)
   2. Re: Ark: An Alternative Privacy-preserving Second	Layer
      Solution (ZmnSCPxj)
   3. Re: Ark: An Alternative Privacy-preserving Second	Layer
      Solution (ZmnSCPxj)
   4. Re: Ark: An Alternative Privacy-preserving Second Layer
      Solution (Burak Keceli)
   5. Re: Ark: An Alternative Privacy-preserving Second Layer
      Solution (Burak Keceli)


----------------------------------------------------------------------

Message: 1
Date: Tue, 23 May 2023 18:06:02 -0400
From: "G. Andrew Stone" <g.andrew.stone@gmail.com>
To: Burak Keceli <burak@buraks.blog>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second	Layer Solution
Message-ID:
	<CAHUwRvvo-HE=dY00jErFMgAqq_jCS_hCna=eaAQPYLkGSEHYtA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Do you have any write up that presents a fully detailed architecture,
including mechanisms like bitcoin scripts, transactions and L2 protocols,
and then derives claims from that base?

On Tue, May 23, 2023, 5:59 AM Burak Keceli via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> > As the access to Lightning is also by the (same?) ASP, it seems to me
> that the ASP will simply fail to forward the payment on the broader
> Lightning network after it has replaced the in-mempool transaction,
> preventing recipients from actually being able to rely on any received
> funds existing until the next pool transaction is confirmed.
>
> Yes, that's correct. Lightning payments are routed through ASPs. ASP may
> not cooperate in forwarding HTLC(s) AFTER double-spending their pool
> transaction. However, it's a footgun if ASP forwards HTLC(s) BEFORE
> double-spending their pool transaction.
>
> What makes Ark magical is, in the collaborative case, users' ability to
> pay lightning invoices with their zero-conf vTXOs, without waiting for
> on-chain confirmations.
>
> This is the opposite of swap-ins, where users SHOULD wait for on-chain
> confirmations before revealing their preimage of the HODL invoice;
> otherwise, the swap service provider can steal users' sats by
> double-spending their zero-conf HTLC.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230523/0870c6d9/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 24 May 2023 00:40:42 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Burak Keceli <burak@buraks.blog>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second	Layer Solution
Message-ID:
	<RqMGBWFiZaAWDLpHiElcCqoOINqnqO_QfmBEYHfV0zkCJhQkhkwxaboCnRF6_2xU8tcVFcnpKzzXRhu126dKvAlsUUg_tx9KUTFZFb4mM5s=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Burak,

> > As the access to Lightning is also by the (same?) ASP, it seems to me that the ASP will simply fail to forward the payment on the broader Lightning network after it has replaced the in-mempool transaction, preventing recipients from actually being able to rely on any received funds existing until the next pool transaction is confirmed.
> 
> 
> Yes, that's correct. Lightning payments are routed through ASPs. ASP may not cooperate in forwarding HTLC(s) AFTER double-spending their pool transaction. However, it's a footgun if ASP forwards HTLC(s) BEFORE double-spending their pool transaction.

This is why competent coders test their code for footguns before deploying in production.

> What makes Ark magical is, in the collaborative case, users' ability to pay lightning invoices with their zero-conf vTXOs, without waiting for on-chain confirmations.

You can also do the same in Lightning, with the same risk profile: the LSP opens a 0-conf channel to you, you receive over Lightning, send out over Lightning again, without waiting for onchain confirmations.
Again the LSP can also steal the funds by double-spending the 0-conf channel open, like in the Ark case.

The difference here is that once confirmed, the LSP can no longer attack you.
As I understand Ark, there is always an unconfirmed transaction that can be double-spent by the ASP, so that the ASP can attack at any time.

> This is the opposite of swap-ins, where users SHOULD wait for on-chain confirmations before revealing their preimage of the HODL invoice; otherwise, the swap service provider can steal users' sats by double-spending their zero-conf HTLC.

If by "swap-in" you mean "onchain-to-offchain swap" then it is the user who can double-spend their onchain 0-conf HTLC, not the swap service provider.
As the context is receiving money and then sending it out, I think that is what you mean, but I think you also misunderstand the concept.

Regards,
ZmnSPCxj


------------------------------

Message: 3
Date: Wed, 24 May 2023 00:45:49 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: Burak Keceli <burak@buraks.blog>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second	Layer Solution
Message-ID:
	<ApngTTvW46O8UkGVrWosWYbTPx5gBVUXL46ihSRkA1jVXNqxLtKXpA-unovlJHXFfAYxIPInJwg849K2MeDUymPqn8Mp_CeUMnK3UYiGmcQ=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Here is an old write-up that should be read by everyone trying to design a NON-custodial L2: https://zmnscpxj.github.io/offchain/safety.html




Sent with Proton Mail secure email.

------- Original Message -------
On Wednesday, May 24th, 2023 at 12:40 AM, ZmnSCPxj via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Good morning Burak,
> 
> > > As the access to Lightning is also by the (same?) ASP, it seems to me that the ASP will simply fail to forward the payment on the broader Lightning network after it has replaced the in-mempool transaction, preventing recipients from actually being able to rely on any received funds existing until the next pool transaction is confirmed.
> > 
> > Yes, that's correct. Lightning payments are routed through ASPs. ASP may not cooperate in forwarding HTLC(s) AFTER double-spending their pool transaction. However, it's a footgun if ASP forwards HTLC(s) BEFORE double-spending their pool transaction.
> 
> 
> This is why competent coders test their code for footguns before deploying in production.
> 
> > What makes Ark magical is, in the collaborative case, users' ability to pay lightning invoices with their zero-conf vTXOs, without waiting for on-chain confirmations.
> 
> 
> You can also do the same in Lightning, with the same risk profile: the LSP opens a 0-conf channel to you, you receive over Lightning, send out over Lightning again, without waiting for onchain confirmations.
> Again the LSP can also steal the funds by double-spending the 0-conf channel open, like in the Ark case.
> 
> The difference here is that once confirmed, the LSP can no longer attack you.
> As I understand Ark, there is always an unconfirmed transaction that can be double-spent by the ASP, so that the ASP can attack at any time.
> 
> > This is the opposite of swap-ins, where users SHOULD wait for on-chain confirmations before revealing their preimage of the HODL invoice; otherwise, the swap service provider can steal users' sats by double-spending their zero-conf HTLC.
> 
> 
> If by "swap-in" you mean "onchain-to-offchain swap" then it is the user who can double-spend their onchain 0-conf HTLC, not the swap service provider.
> As the context is receiving money and then sending it out, I think that is what you mean, but I think you also misunderstand the concept.
> 
> Regards,
> ZmnSPCxj
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 4
Date: Wed, 24 May 2023 09:28:08 +0300 (TRT)
From: Burak Keceli <burak@buraks.blog>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second Layer Solution
Message-ID:
	<1333267652.1427392.1684909688735@eu1.myprofessionalmail.com>
Content-Type: text/plain; charset=UTF-8

> You can also do the same in Lightning, with the same risk profile: the LSP opens a 0-conf channel to you, you receive over Lightning, send out over Lightning again, without waiting for onchain confirmations.

This is not correct. If an LSP opens a zero-conf channel to me, I cannot receive over lightning immediately because I have to wait for that channel to confirm before revealing my preimage for the payment. If I don?t, LSP takes the sender?s money yet double-spends my channel.

This is not the case with Ark. Ark ensures "absolute atomicity" by using ATLCs instead of HTLCs. Users can receive payments and forward them further without waiting for on-chain confirmations. A double-spend attempt breaks the entire atomicity. An ASP cannot redeem senders? vTXO(s) if they double-spend recipients' vTXO(s).


------------------------------

Message: 5
Date: Wed, 24 May 2023 10:53:50 +0300 (TRT)
From: Burak Keceli <burak@buraks.blog>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second Layer Solution
Message-ID:
	<29099205.1444460.1684914830367@eu1.myprofessionalmail.com>
Content-Type: text/plain; charset=UTF-8

> 0-conf transactions are unsafe since it is possible to double-spend the inputs they consume, invalidating the 0-conf transaction.

A future extension of Ark can potentially utilize a hypothetical data manipulation opcode (OP_XOR or OP_CAT) to constrain the ASP's nonce in their signatures to disincentivize double-spending. If a double-spend occurs in a pool transaction, users can forge ASP's signature to claim their previously redeemed vTXOs. This is effectively an inbound liquidity-like tradeoff without compromising on the protocol design.

For the time being, you have to wait for on-chain confirmations to consider a payment 'final'. However, this doesn't prevent you from paying lightning invoices with your zero-conf coins. Ark has immediate availability with delayed finality.

Best,
Burak


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 57
*******************************************
