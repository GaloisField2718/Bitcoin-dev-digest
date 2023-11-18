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

   1. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Fri, 17 Nov 2023 22:36:35 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Olaoluwa Osuntokun <laolu32@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID:
	<CALZpt+F411Qv=8znxXzv6O3r21ZdD9h24RJL2Oq6O-mdBTaYww@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> IIRC correctly, in your scenario, you're dealing with Carol -> Bob ->
Alice.
> Mallory can only replace an HTLC-timeout transaction if she's directly
> connected with the peer she's targeting via a direct channel. She cannot
> unilaterally replace any transaction in the mempool solely with knowledge
of
> the preimage. All HTLC transactions are two party contracts, with the
public
> keys of both participants hard coded into the contract. A third party
cannot
> unilaterally sweep an HTLC given only a preimage.

> I think it's worth taking a minute to step back here so we can establish
> some fundamental context. Once the timelock of an HTLC expires, and the
> receiver has direct knowledge of the preimage, a bidding war begins.  If
the
> receiver is able to confirm their success transaction in time, then they
> gain the funds, and the sender is able to pipeline the preimage backwards
in
> the route, making all parties whole. If the sender is the one that wins
out,
> then it's as if nothing happened, sans the fees paid at the last mile, all
> other hops are able to safely cancel their HTLC back on the chain.

> As mentioned elsewhere in the thread, most implementations today will
watch
> the mempool for preimages, so they can resolve the incoming HTLC as
quickly
> as possible off chain. The attack described critically relies on the
ability
> of an attacker to pull off very precise transaction replacement globally
> across "the mempool". If any of the honest parties see the preimage, in
the
> mempool, then the attack ends as they can settle back off chain, and if
> their timeout is able to confirm first, then the defender has actually
> gained funds.

Correct mostly so far, a part of the globally across "the mempool".

> In addition, such an attack needs to be executed perfectly, for hours if
not
> days. Within the LN, all nodes set a security parameter, the CLTV delta,
> that dictates how much time they have before the outgoing and incoming
HTLCs
> expire. Increasing this value makes the attack more difficult, as they
must
> maintain the superposition of: fees low enough to not get mined, but high
> enough to replace the defender's transaction, but not _too_ high, as then
> it'll be mined and everything is over. With each iteration, the attacker
is
> also forced to increase the amount of fees they pay, increasing the likely
> hood that the transaction will be mined. If mined, the attack is moot.

The attacker just has to overbid the parent of the HTLC-preimage with a
higher fee replacement parent. This replacement parent can be confirmed at
any time, even if the attacker realizes a higher economic gain if this
replacement transaction is delayed as much as possible. Or the absolute fee
consumed to batch attack multiple targets. So I think your assumption on
the attack difficulty is not correct.

> As mentioned in the OP, one thing the attacker can do is try and locate
the
> defender's node to launch the replacement attack directly in their
mempool.
> However, by replacing directly in the mempool of the defender, the
defender
> will learn of the preimage! They can use that to just settle everything
> back, thereby completing the payment, and stopping the attack short. Even
> ignoring direct access to the defender's mempool, the attacker needs to
> somehow iteratively execute the replacement across a real network, with
all
> the network jitter, propagation delay, and geographic heterogeneity that
> entails. If they're off by milliseconds, then either a confirmation
occurs,
> or the preimage is revealed in the mempool. A canned local regtest env is
> one thing, the distributed system that is the Internet is another.

The attacker can blind the defender mempool by locating the associated
full-node with its lightning node, then broadcast a conflicting parent of
the HTLC-preimage, partitioning the mempool from the rest of the network.
The HTLC-preimage will never enter the defender's mempool, as some spent
inputs are missing.

All the considerations on network jitter, propagation delay and geographic
heterogeneity are irrelevant as network mempools are in practice a
distributed system of logically equivalent state machines to favor
propagation of high-fees paying transactions, on top of raw TCP/IP
connections. Propagation works quite deterministically on average if you
have ever used a bitcoin wallet to pay with zero-conf and see the
transaction showing up as unconfirmed on the payment processor. Policy
divergences across implementations and versions does not matter here.

The p2p stack of Bitcoin Core has some propagation delay in the order of
seconds for outbound / inbound connections transaction-relay connections. I
think they're at the advantage of the attacker, as they can be bypassed to
quickly evict the honest HTLC-timeout bypassing them with mass connections.

The p2p transaction-relay is a public network of nodes running common open
software, where their inbound slots can be occupied at low-cost and their
network address might be publicly announced. All at the advantage of the
attacker.

> Returning back to the bidding war: for anchor channels, the second level
> HTLCs allow the defender to attach arbitrary inputs for fee bumping
> purposes. Using this, they can iteratively increase their fee (via RBF) as
> the expiry deadline approaches. With each step, they further increase the
> cost for the attacker. On top of that, this attack cannot be launched
> indiscriminately across the network. Instead, it requires a per-node set
up by
> the attacker, as they need to consume UTXOs to create a chain of
> transactions they'll use to launch the replacement attack. These also need
> to be maintained in a similar state of non-confirming superposition.

As said elsewhere, I'll maintain this is a practical and critical attack on
lightning, I don't doubt you have the level of expertise in this attack by
yourself and re-think if it's a fragile one or bring new insights to the
conversation.

There are no requirements of an "extremely precise timing and execution",
the most adversarial event that an attacker might hit is a block being
mined in the order of few seconds between a HTLC-timeout hit the block
template and a block is mined. On average, you have a 10 min block interval
so probabilities are in favor of the attacker.

It is correct that miners can broadcast any of the preimage replacement
transactions, however this is not at all a deployed mechanism today by the
mining ecosystem. DoS-robustness of such a scheme is very unclear.

One more mitigation that can be done by lightning nodes today is
duplicating the mempool-monitoring mitigation to their watchtower backends,
assuming those ones are already running on top of a full-node. For each new
watchtower deployed, this is one more entity to mempool-partition by the
attacker and all of them must be well-partitioned along the attack. This
can still be neutralized by sophisticated attackers, though it's notably
raising the bar to mount a successful replacement attack.

Recommending to LN softwares to adapt this last mitigation, especially if
your implementation is used by high-value routing nodes or LSPs.

Best,
Antoine

Le sam. 21 oct. 2023 ? 01:19, Olaoluwa Osuntokun <laolu32@gmail.com> a
?crit :

> > Let's say you have Alice, Bob and Caroll all "honest" routing hops
> > targeted by an attacker. They all have 3 independent 10 000 sats HTLC
> > in-flight on their outbound channels.
>
> > It is replaced by Mallory at T+2 with a HTLC-preimage X of 200 000 sats
> (+
> > rbf penalty 1 sat / vb rule 4). Alice's HTLC-timeout is out of network
> > mempools.
>
> > Bob broadcasts her HTLC-timeout of 200 000 sats at T+3. It is replaced by
> > Mallory at T+4 with her HLTC-preimage Y of 200 000 sats (+ rbf penalty 1
> > sat / vb rule 4 * 2). Bob's HTLC-timeout is out of network mempools.
>
> IIRC correctly, in your scenario, you're dealing with Carol -> Bob ->
> Alice.
> Mallory can only replace an HTLC-timeout transaction if she's directly
> connected with the peer she's targeting via a direct channel. She cannot
> unilaterally replace any transaction in the mempool solely with knowledge
> of
> the preimage. All HTLC transactions are two party contracts, with the
> public
> keys of both participants hard coded into the contract. A third party
> cannot
> unilaterally sweep an HTLC given only a preimage.
>
> I think it's worth taking a minute to step back here so we can establish
> some fundamental context. Once the timelock of an HTLC expires, and the
> receiver has direct knowledge of the preimage, a bidding war begins.  If
> the
> receiver is able to confirm their success transaction in time, then they
> gain the funds, and the sender is able to pipeline the preimage backwards
> in
> the route, making all parties whole. If the sender is the one that wins
> out,
> then it's as if nothing happened, sans the fees paid at the last mile, all
> other hops are able to safely cancel their HTLC back on the chain.
>
> As mentioned elsewhere in the thread, most implementations today will watch
> the mempool for preimages, so they can resolve the incoming HTLC as quickly
> as possible off chain. The attack described critically relies on the
> ability
> of an attacker to pull off very precise transaction replacement globally
> across "the mempool". If any of the honest parties see the preimage, in the
> mempool, then the attack ends as they can settle back off chain, and if
> their timeout is able to confirm first, then the defender has actually
> gained funds.
>
> In addition, such an attack needs to be executed perfectly, for hours if
> not
> days. Within the LN, all nodes set a security parameter, the CLTV delta,
> that dictates how much time they have before the outgoing and incoming
> HTLCs
> expire. Increasing this value makes the attack more difficult, as they must
> maintain the superposition of: fees low enough to not get mined, but high
> enough to replace the defender's transaction, but not _too_ high, as then
> it'll be mined and everything is over. With each iteration, the attacker is
> also forced to increase the amount of fees they pay, increasing the likely
> hood that the transaction will be mined. If mined, the attack is moot.
>
> As mentioned in the OP, one thing the attacker can do is try and locate the
> defender's node to launch the replacement attack directly in their mempool.
> However, by replacing directly in the mempool of the defender, the defender
> will learn of the preimage! They can use that to just settle everything
> back, thereby completing the payment, and stopping the attack short. Even
> ignoring direct access to the defender's mempool, the attacker needs to
> somehow iteratively execute the replacement across a real network, with all
> the network jitter, propagation delay, and geographic heterogeneity that
> entails. If they're off by milliseconds, then either a confirmation occurs,
> or the preimage is revealed in the mempool. A canned local regtest env is
> one thing, the distributed system that is the Internet is another.
>
> Returning back to the bidding war: for anchor channels, the second level
> HTLCs allow the defender to attach arbitrary inputs for fee bumping
> purposes. Using this, they can iteratively increase their fee (via RBF) as
> the expiry deadline approaches. With each step, they further increase the
> cost for the attacker. On top of that, this attack cannot be launched
> indiscriminately across the network. Instead, it requires per-node set up
> by
> the attacker, as they need to consume UTXOs to create a chain of
> transactions they'll use to launch the replacement attack. These also need
> to be maintained in a similar state of non-confirming superposition.
>
> That's all to say that imo, this is a rather fragile attack, which
> requires:
> per-node setup, extremely precise timing and execution, non-confirming
> superposition of all transactions, and instant propagation across the
> entire
> network of the replacement transaction (somehow also being obscured from
> the
> PoV of the defender). The attack can be launched directly with a miner, or
> "into" their mempool, but that weakens the attack as if the miner
> broadcasts
> any of the preimage replacement transactions, then the defender can once
> again use that to extract the preimage and settle the incoming HTLC.
>
> -- Laolu
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231117/f50939b4/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 30
********************************************
