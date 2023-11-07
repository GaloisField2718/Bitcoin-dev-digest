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

   1. Re: [Lightning-dev] OP_Expire and Coinbase-Like	Behavior:
      Making HTLCs Safer by Letting Transactions Expire Safely (ZmnSCPxj)
   2. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Antoine Riard)
   3. Re: ossification and misaligned incentive concerns
      (vjudeu@gazeta.pl)
   4. Re: Proposed BIP for MuSig2 Descriptors (Salvatore Ingala)


----------------------------------------------------------------------

Message: 1
Date: Tue, 07 Nov 2023 11:11:59 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>, security@ariard.me
Subject: Re: [bitcoin-dev] [Lightning-dev] OP_Expire and Coinbase-Like
	Behavior: Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<iBopsZOx5TRDjjfxSLo9GLa00c7Jk0uMSae6_EPsPjnd10Aa87-lxVIZnL37GwEM3ppemBAxCwkv7r4w5AfDjLkKo0OhIpdB0jK0_OTRqf4=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Antoine,


> Once the HTLC is committed on the Bob-Caroll link, Caroll releases the preimage off-chain to Bob with an `update_fulfill_htlc` message, though Bob does _not_ send back his signature for the updated channel state.
> 
> Some blocks before 100, Caroll goes on-chain to claim the inbound HTLC output with the preimage. Her commitment transaction propagation in network mempools is systematically "replaced cycled out" by Bob.

I think this is impossible?

In this scenario, there is an HTLC offered by Bob to Carol.

Prior to block 100, only Carol can actually create an HTLC-success transaction.
Bob cannot propagate an HTLC-timeout transaction because the HTLC timelock says "wait till block 100".

Neither can Bob replace-recycle out the commitment transaction itself, because the commitment transaction is a single-input transaction, whose sole input requires a signature from Bob and a signature from Carol --- obviously Carol will not cooperate on an attack on herself.

So as long as Carol is able to get the HTLC-success transaction confirmed before block 100, Bob cannot attack.
Of course, once block 100 is reached, `OP_EXPIRE` will then mean that Carol cannot claim the fund anymore.

Regards,
ZmnSCPxj


------------------------------

Message: 2
Date: Mon, 6 Nov 2023 18:45:21 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CALZpt+GXGBbo0JjOyMr3B-3dVY2Q_DuzF6Sn3xE5W24x77PRYg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> I think you are misunderstanding a key point to my OP_Expire proposal:
because
> the ability to spend the preimage branch of the HTLC goes away when the
refund
> branch becomes available, replacing cycling or any similar technique
becomes
> entirely irrelevant.

> The situation where Carol prevents Bob from learning about the preimage
in time
> simply can't happen: either Carol collects the HTLC with knowledge of the
> preimage, by spending it in a transaction mined prior to the expiration
time
> and ensuring that Bob learns the preimage from the blockchain itself. Or
the
> HTLC expires and Bob can use the refund branch at his leisure.

I think I understand the semantic of the OP_Expire proposal overall
correctly, however I'm not sure it prevents replacing cycling or any
similar adversarial technique, as the forwarding node might be the attacker
in some scenario.

Consider the following: you have Alice, Bob, Caroll sharing lightning
channels.

Alice forwards a HTLC of 1 BTC to Caroll by the intermediary of Bob.

On the Bob-Caroll link, the HTLC expires at block 100.

According to OP_Expire semantics, Caroll shouldn't be able to claim the
htlc-preimage spends on the Bob-Caroll link, after block 100.

However, this situation offers the ability to Bob the routing node to steal
HTLC payment between Alice and Caroll.

Once the HTLC is committed on the Bob-Caroll link, Caroll releases the
preimage off-chain to Bob with an `update_fulfill_htlc` message, though Bob
does _not_ send back his signature for the updated channel state.

Some blocks before 100, Caroll goes on-chain to claim the inbound HTLC
output with the preimage. Her commitment transaction propagation in network
mempools is systematically "replaced cycled out" by Bob.

At block 100, Caroll cannot claim the payment sent to her by Alice.

Bob claims the htlc-refund path on the Bob-Caroll link and claims the
htlc-preimage path on the Alice-Bob link, as such making a gain of 1 BTC.

If Caroll is a lightning mobile client, it is easy for Bob to claim
publicly that the lack of success in signature exchange to update channels
state is a liveliness mistake of her own.

Assuming this advanced scenario is correct, I'm not sure the OP_Expire
proposal is substantially fixing all the adversarial replacement cycling
situations.

Best,
Antoine

Le sam. 4 nov. 2023 ? 07:26, Peter Todd <pete@petertodd.org> a ?crit :

> On Fri, Nov 03, 2023 at 05:25:24AM +0000, Antoine Riard wrote:
> > > To be clear, are you talking about anchor channels or non-anchor
> channels?
> > > Because in anchor channels, all outputs other than the anchor outputs
> > provided
> > > for fee bumping can't be spent until the commitment transaction is
> mined,
> > which
> > > means RBF/CPFP isn't relevant.
> >
> > I think the distinction is irrelevant here as pre-anchor channel if I
> have
> > one spendable HTLC output spend and I gain knowledge of my counterparty
> > commitment transaction from networks mempools, the spend is malleable and
> > can be used as a CPFP. If you assume anchor channels, you have 2 anchor
> > outputs as long both parties have balance outputs or pending HTLCs.
> >
> > Though pre-anchor, legacy channels the counterparty commitment
> transaction
> > will have to be attached with a fee under min mempool fee for the
> > replacement cycling to happen, and let network congestion happen.
>
> I think you are misunderstanding a key point to my OP_Expire proposal:
> because
> the ability to spend the preimage branch of the HTLC goes away when the
> refund
> branch becomes available, replacing cycling or any similar technique
> becomes
> entirely irrelevant.
>
> The situation where Carol prevents Bob from learning about the preimage in
> time
> simply can't happen: either Carol collects the HTLC with knowledge of the
> preimage, by spending it in a transaction mined prior to the expiration
> time
> and ensuring that Bob learns the preimage from the blockchain itself. Or
> the
> HTLC expires and Bob can use the refund branch at his leisure.
>
> > I think the more interesting case is a future world with package relay
> > deployed at the p2p level and anchor output on the lightning-side. Here
> the
> > most advanced replacement as illustrated in the test can happen (where
> > commitment has an anchor output - see L125).
>
> Again, with OP_Expire, whether or not package relay or anything similar
> exists
> is irrelevant. Replacement cycling is totally useless because there is a
> defined time window in which the HTLC can be spent with the preimage, after
> which only the refund branch can be used.
>
> Indeed, with OP_Expire Lightning nodes will no longer need to monitor
> mempools
> for preimages at all. If the preimage is used, it is guaranteed to end up
> in
> the chain, and the Lightning node is guaranteed to see it provided they
> have
> access to up-to-date blockchain data.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231106/706321dd/attachment.html>

------------------------------

Message: 3
Date: Tue, 07 Nov 2023 09:58:44 +0100
From: vjudeu@gazeta.pl
To: JK <jk_14@op.pl>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Erik Aronesty <erik@q32.com>,
	Bitcoin Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] ossification and misaligned incentive
	concerns
Message-ID:
	<194638433-36890bea95b2ebab3a168daf3c806e8f@pmq7v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> Imagine a system that tries to maintain a constant level of difficulty and reacts flexibly to changes in difficulty, by modulating the block reward level accordingly (using negative feedback).
?
This is exactly what I did, when experimenting with LN-based mining. CPU power was too low to get a full block reward out of that. But getting single millisatoshis from a channel partner? This is possible, and I started designing my model from that assumption. Also, because channel partner usually don't want to explicitly pay, I created it in a form of "LN transaction fee discount". Which means, a CPU miner just received cheaper LN transactions through the channel partner, instead of getting paid explicitly. Which also caused better network connectivity, because then you have an upper bound for your mining (it won't be cheaper LN transaction than for free). Which means, if you mine so many shares, that you have free LN transactions, then you have to sell them, or open another channel, and then instead of having "one channel with free transactions", you have many.
?
> The free market is more important than finite supply.
?
I would say, the backward compatibility is more important than increased (no matter if still constant or not) supply. Which means, you can "increase" the supply, just by introducing millisatoshis on-chain. Or add any "tail supply", or anything like that, what was discussed in the past. The only thing that matters is: can you make it compatible with the current system? Hard-fork will be instantly rejected, without any discussion. Soft-fork will be stopped at best, exactly in the same way, how other soft-fork proposals were stopped, when achieving consensus was hard, and the topic was controversial. So, what is left? Of course no-forks and second layers. This is the only way, that is wide-open today, and which requires no support from the community. And that's why Ordinals are so strong: because they are a no-fork. Better or worse designed, it doesn't matter, but still a no-fork. Which means, they exist in the wild, no matter if you like them or not.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231107/018581a8/attachment.html>

------------------------------

Message: 4
Date: Tue, 7 Nov 2023 11:34:46 +0000
From: Salvatore Ingala <salvatore.ingala@gmail.com>
To: Andrew Chow <lists@achow101.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for MuSig2 Descriptors
Message-ID:
	<CAMhCMoHLfRDZPeVcuDnDy4mXbsyOQbgbqWPK51VBxCW=a1wD-A@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Andrew,

Thank you for putting this together; these standards will be of great
help for implementations.

The only concern I have is about the utility of supporting KEY
expressions inside musig to contain ranged derivations with `/*`.

Consider a wallet described as follows:

  musig(key1/<0;1>/*, key2/<0;1>/*, ..., keyN/<0;1>/*)

With such a setup, for each input being spent, each signer is required
to derive the child xpub for each key, and then execute the KeyAgg
algorithm [1] (which includes N scalar multiplications).

Instead, a policy like:

  musig(key1, key2, ..., keyN)/<0;1>/*

is more succinct, and KeyAgg is executed only once for all the inputs.
I think the performance impact is substantial for signing devices.

Therefore, unless there are known use cases, I would suggest keeping
the standard minimal and supporting only the second form, avoiding
both the performance overhead and the additional complexity when
writing descriptor parsers.

If, on the contrary, there are legitimate use cases, a discussion
about them (and the above mentioned tradeoffs) might be worth adding
to the BIP proposal.

Best,
Salvatore


[1] - BIP-327 MuSig2: https://github.com/bitcoin/bips/blob/master/bip-0327
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231107/253c6c31/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 11
********************************************
