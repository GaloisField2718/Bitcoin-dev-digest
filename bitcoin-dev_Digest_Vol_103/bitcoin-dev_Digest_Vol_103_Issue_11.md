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

   1. Re: Scaling Lightning Safely With Feerate-Dependent	Timelocks
      (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Sun, 17 Dec 2023 23:01:22 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: jlspc <jlspc@protonmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: "lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent	Timelocks
Message-ID:
	<CALZpt+Gpv3SjPJyamy_CChKybTdhNgaGdb213E4cSnfYOoc3tA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi John,

While the idea of using sliding reaction window for blockchain congestion
detection has been present in the "smart contract" space at large [0] and
this has been discussed informally among Lightning devs and covenant
designers few times [1] [2], this is the first and best formalization of
sliding-time-locks in function of block fee rates for Bitcoin I'm aware
off, to the best of my knowledge.

Here my understanding of the feerate-dependent timelock proposal.

A transaction cannot be included in a block:
- height-based or epoch-based absolute or relative timelocks are not
satisfied according to current consensus rules (bip68 and bip 113 and
implementation details)
- less than `block_count` has a block median-feerate above the
median-feerate of the `window_size` period

A median feerate is computed for each block.
(This is unclear to me if this is the feerate for half of the block's
weight or the median feerate with all weight units included in the
block as the sample)

>From then, you have 3 parameters included in the nSequence field.
- feerate_value_bound
- window_size
- block_count

Those parameters can be selected by the transaction builder (and
committed with a signature or hash chain-based covenant).
As such, off-chain construction counterparties can select the
feerate_value_bound at which their time-sensitive transaction
confirmation will be delayed.

E.g let's say you have a LN-penalty Alice-Bob channel. Second-stage
HTLC transactions are pre-signed with feerate_value_bound at 100 sat /
vbytes.
The window_size selected is 100 blocks and the block_count is 70 (this
guarantees tampering-robustness of the feerate_value_bound in face of
miners coalitions).

There is 1 BTC offered HTLC pending with expiration time T, from Alice to Bob.

If at time T, the per-block median feerate of at least 70 blocks over
the latest 100 block is above 100 sat / vbytes, any Alice's
HTLC-timeout or Bob's HTLC-preimage cannot be included in the chain.

>From my understanding, Feerate-Dependent Timelocks effectively
constitute the lineaments of a solution to the "Forced Expiration
Spam" as described in the LN paper.

I think you have few design caveats to be aware off:
- for current LN-penalty, the revokeable scripts should be modified to
ensure the CSV opcode inspect the enforcement of FDT's parameters, as
those revokeable scripts are committed by all parties
- there should be a delay period at the advantage of one party
otherwise you still a feerate-race if the revocation bip68 timelock
has expired during the FDT delay

As such, I believe the FDT parameters should be enriched with another
parameter : `claim_grace_period`, a new type of relative timelock of
which the endpoint should be the `feerate_value_bound` itself.

I think it works in terms of consensus chain state, validation
resources and reorg-safety are all the parameters that are
self-contained in the spent FDT-encumbered transaction itself.
If the per-block feerate fluctuates, the validity of the ulterior
FDT-locked transactions changes too, though this is already the case
with timelock-encumbered transactions.

(One corollary for Lightning, it sounds like all the channels carrying
on a HTLC along a payment path should have the same FDT-parameters to
avoid off-chain HTLC double-spend, a risk not clearly articulated in
the LN paper).

Given the one more additional parameter `claim_grace_period`, I think
it would be wiser design to move all the FDT parameters in the bip341
annex.
There is more free bits room there and additionally you can have
different FDT parameters for each of your HTLC outputs in a single LN
transaction, if combined with future covenant mechanisms like HTLC
aggregation [3].
(The current annex design draft has been designed among others to
enable such "block-feerate-lock-point" [4] [5])

I cannot assert that the FDT proposal makes the timeout-tree protocol
more efficient than state-of-the-art channel factories and payment
pool constructions.
Still from my understanding, all those constructions are sharing
frailties in face of blockchain congestion and they would need
something like FDT.

I'm truly rejoicing at the idea that we have now the start of a
proposal solving one of the most imperative issues of Lightning and
other time-sensitive use-cases.
(Note, I've not reviewed the analysis and game-theory in the face of
miners collusion / coalition, as I think the introduction of a
`claim_grace_period` is modifying the fundamentals).

Best,
Antoine

[0] https://fc22.ifca.ai/preproceedings/119.pdf
[1] https://github.com/ariard/bitcoin-contracting-primitives-wg/blob/main/meetings/meetings-18-04.md
[2] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-November/022180.html
[3] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-October/022093.html
[4] https://github.com/bitcoin-inquisition/bitcoin/pull/9

[5] https://github.com/bitcoin/bips/pull/1381


Le ven. 15 d?c. 2023 ? 09:20, jlspc via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

> TL;DR
> =====
> * All known Lightning channel and factory protocols are susceptible to forced expiration spam attacks, in which an attacker floods the blockchain with transactions in order to prevent honest users from putting their transactions onchain before timelocks expire.
> * Feerate-Dependent Timelocks (FDTs) are timelocks that automatically extend when blockchain feerates spike.
>   - In the normal case, there's no spike in feerates and thus no tradeoff between capital efficiency and safety.
>   - If a dishonest user attempts a forced expiration spam attack, feerates increase and FDTs are extended, thus penalizing the attacker by keeping their capital timelocked for longer.
>   - FDTs are tunable and can be made to be highly resistant to attacks from dishonest miners.
> * Of separate interest, an exact analysis of the risk of double spend attacks is presented that corrects an error in the original Bitcoin whitepaper.
>
> Overview
> ========
>
> Because the Lightning protocol relies on timelocks to establish the correct channel state, Lightning users could lose their funds if they're unable to put their transactions onchain quickly enough.
> The original Lightning paper [1] states that "[f]orced expiration of many transactions may be the greatest systemic risk when using the Lightning Network" and it uses the term "forced expiration spam" for an attack in which a malicious party "creates many channels and forces them all to expire at once", thus allowing timelocked transactions to become valid.
> That paper also says that the creation of a credible threat against "spamming the blockchain to encourage transactions to timeout" is "imperative" [1].
>
> Channel factories that create multiple Lightning channels with a single onchain transaction [2][3][4][5] increase this risk in two ways.
> First, factories allow more channels to be created, thus increasing the potential for many channels to require onchain transactions at the same time.
> Second, channel factories themselves use timelocks, and thus are vulnerable to a "forced expiration spam" attack.
>
> In fact, the timelocks in Lightning channels and factories are risky even without an attack from a malicious party.
> Blockchain congestion is highly variable and new applications (such as ordinals) can cause a sudden spike in congestion at any time.
> As a result, timelocks that were set when congestion was low can be too short when congestion spikes.
> Even worse, a spike in congestion could be self-reinforcing if it causes malicious parties to attack opportunistically and honest parties to put their channels onchain due to the heightened risk.
>
> One way to reduce the risk of a forced expiration spam attack is to use longer timelocks that give honest users more time to put their transactions onchain.
> However, long timelocks limit the ability to dynamically reassign the channel's (or factory's) funds, thus creating a tradeoff between capital efficiency and safety [6].
> While long timelocks could maintain safety for small numbers of channels, supporting billions (or tens of billions) of channels while maintaining safety is probably impossible [7].
>
> Another way to reduce risk is to impose a penalty on an attacker.
> Some channel protocols, such as the original Lightning protocol [1], a version of the two-party eltoo protocol [8], the fully-factory-optimized protocol [9], and the tunable-penalty channel protocol [10] include such penalties.
> In addition, the tunable-penalty and single-commitment factory protocols [4] support penalties.
> However, as was noted in the original Lightning paper [1], penalties don't eliminate the risk of a forced expiration spam attack.
> Furthermore, existing penalty-based factory protocols [4] have limited scalability, as they depend on getting large numbers of casual users to coordinate and co-sign transactions [11][5].
>
> In contrast, the timeout-tree protocol [5] scales via simple covenants (enabled by support for CheckTemplateVerify, AnyPrevOut, or a similar change to the Bitcoin consensus rules).
> As a result, a single timeout-tree can support millions of channels and one small transaction per block can fund timeout-trees with tens of billions of offchain channels [5].
> However, timeout-trees don't support penalties, and like all other known factory protocols [2][3][4], timeout-trees rely on timelocks.
>
> Therefore, if the need to protect against forced expiration spam was already "imperative" for the original Lightning channel protocol [1], the use of scalable channel factories will make such protection indispensable.
>
> This post proposes a change to Bitcoin's consensus rules that allows the length of a timelock to depend on the feerate being charged for putting transactions onchain.
> Such Feerate-Dependent Timelocks (FDTs) can be used to make the above channel and factory protocols resistant to sudden spikes in blockchain congestion.
> In the normal case, when there's no spike in congestion, FDTs don't extend the lengths of timelocks and thus don't create a tradeoff between capital efficiency and safety.
> On the other hand, when congestion spikes, FDTs extend the lengths of timelocks and thus penalize the owner of the timelocked capital by reducing its efficiency.
> Therefore, FDTs can be viewed as creating a penalty for spamming the blockchain, thus reducing the likelihood of such an attack even if the channel (or factory) protocol being used doesn't have an explicit penalty mechanism.
>
> FDTs have other uses, including reducing the risk of having to pay unexpectedly high fees during a congestion spike, improving the accuracy of fee-penalties [5] and reducing the risk of one-shot receives [12].
>
> Of separate interest, the analysis of FDTs given here leads to an exact analysis of the risk of double spend attacks that corrects an error in the original Bitcoin whitepaper [13].
>
> A more complete description and analysis of FDTs is given in a paper [14].
>
> Feerate-Dependent Timelock (FDT) Proposal
> =========================================
>
> A Feerate-Dependent Timelock (FDT) is created by encoding a feerate upper bound in a transaction's nSequence field.
> A transaction with an FDT cannot be put onchain until:
>   1) its absolute timelock encoded in its nLocktime field (and its relative timelock encoded in the same nSequence field, if present) has been satisfied, and
>   2) the prevailing feerate has fallen below the FDT's feerate upper bound.
> As a result, FDTs are automatically extended when the feerate for putting transactions onchain spikes (such as would occur during a forced expiration spam attack).
>
> In order to determine the prevailing feerate, the median feerate of each block is calculated as the feerate (in satoshis/vbyte) that is paid for at least half of the block's vbytes.
>
> If all miners were honest, a single block with a low median feerate would be enough to guarantee that congestion is low.
> However, even a small fraction of dishonest miners would be able to occasionally mine a block with an artificially low feerate.
> As a result, it isn't safe to wait for one block (or some other fixed number of blocks) with a low feerate in order to guarantee that honest users have had an opportunity to put their transactions onchain.
>
> Instead, an FDT requires that some maximum number of blocks within an aligned window of consecutive blocks have a high median feerate.
> The FDT proposal uses 14 currently masked-off bits in the nSequence field to express the FDT's three parameters:
>   * feerate_value,
>   * window_size, and
>   * block_count.
> An aligned window of window_size blocks satisfies the FDT's parameters if it has fewer than block_count blocks with median feerate above feerate_value.
> A transaction with an FDT can only be put onchain after an aligned window that satisfies the FDT's parameters and starts no earlier than when the transaction's absolute timelock (and corresponding relative timelock, if present) is satisfied.
>
> In addition, the CheckSequenceVerify (CSV) operator is extended to enforce the desired feerate_value, window_size and block_count.
> The details are given in the paper [14].
>
> Safe Lightning Channels And Factories
> =====================================
>
> In order to protect a channel or factory protocol against forced expiration spam attacks, the protocol's timelocks are made to be feerate-dependent.
> This is done by selecting a feerate_value (such as 4 times the current feerate) that would be caused by a forced expiration spam attack, along with the desired window_size and block_count parameters.
>
> It's also possible to create multiple conflicting transactions with different FDTs (with later timelocks allowing higher feerates) in order to avoid timelocks that will never expire if feerates remain high permanently.
>
> Other Uses
> ==========
>
> FDTs have uses in addition to protecting channel and factory protocols from forced expiration spam attacks.
>
> For example, FDTs can protect users that are racing against timelocks from having to pay an unexpectedly high feerate due to temporary feerate fluctuations [14].
> In addition, FDTs can be used to improve the accuracy of fee-penalties that are assessed when a casual user puts their timeout-tree leaf onchain [14](Section 4.10 of [5]).
> Finally, FDTs can be used to allow a casual user to submit a transaction to the blockchain without having to then monitor the blockchain for a sudden spike in feerates, thus reducing the risk of one-shot receives [14][12].
>
> Analysis
> ========
>
> FDT Implementation Cost
> -----------------------
> In order to verify an FDT, nodes have to determine whether or not there is an aligned window with a sufficient number of low-feerate blocks after the FDT's absolute timelock (and corresponding relative timelock, if present) is satisfied.
> Therefore, if a node knows the starting block of the most recent aligned window that satisfies the FDT's feerate_value, window_size, and block_count parameters, the node can compare that starting block with the FDT's timelocks to verify the FDT.
> Because the FDT parameters can be expressed using 14 bits, nodes only have to keep track of the starting block for 2^14 = 16k different low-feerate windows.
> The starting block for each such window can be stored in 4 bytes, so 16k * 4B = 64kB of memory allows a node to verify an FDT in constant time.
> (In practice, slightly more memory could be used in order to accommodate a reordering of the most recent 1k blocks.)
> Therefore, DRAM that costs less than one cent, plus a small constant number of computations, suffice to verify an FDT.
>
> FDT Dishonest Miner Attacks
> ---------------------------
> The window_size and block_count parameters can be selected to balance between:
>   1) latency,
>   2) the feerate paid by honest users, and
>   3) security against dishonest miners.
> At one extreme, if dishonest miners are of no concern, window_size and block_count can be set to 1, so the FDT can be satisfied when the first block with a sufficiently low feerate is mined.
> At the other extreme, if dishonest miners are of great concern, window_size can be set to 16k and block_count can be set to 1024, in which case dishonest miners with 45% of the hashpower would have less than a 10^-33 chance of dishonestly mining enough blocks in a given window to satisfy the FDT prior to the honest users being able to get their transactions onchain [14].
>
> Double Spend Attacks
> --------------------
> While it's unrelated to FDTs, the analysis of FDTs' resistance to dishonest miner attacks can also be used to analyze the risk of double spend attacks.
>
> The original Bitcoin whitepaper [13] includes an analysis of the probability of a double spend attack in which a dishonest party colludes with dishonest miners in order to undo a bitcoin transaction and steal the goods purchased with that transaction.
> That analysis correctly shows that the probability of success of a double spend attack falls exponentially with z, the depth of the transaction that's being double spent.
> However, there are two problems with that analysis:
>   1) it is approximate, and
>   2) it ignores the possibility of the dishonest miners using pre-mining.
>
> The first problem was addressed by Grunspan and Perez-Marco [15].
> However, it doesn't appear that the second problem has been addressed previously.
>
> Exact formulas for the risk of double spend attacks, including pre-mining, are given in the paper [14] and programs that implement those formulas are available on GitHub [16].
>
> The effect of including pre-mining only becomes apparent when a large fraction of the miners are dishonest.
> For example, Nakamoto estimates the required value of z to guarantee at most a 0.1% chance of a successful double spend, and Grunspan and Perez-Marco give exact values assuming no pre-mining.
> Those results, plus exact results with pre-mining, are as follows:
>
> % dishonest  Estimated z w/o      Exact z w/o       Exact z w/
>      miners  pre-mining [13]  pre-mining [15]  pre-mining [14]
> ===========  ===============  ===============  ===============
>          10                5                6                6
>          15                8                9                9
>          20               11               13               13
>          25               15               20               20
>          30               24               32               33
>          35               41               58               62
>          40               89              133              144
>          45              340              539              589
>
> It's important to note that the above results with pre-mining assume that the time of the double spend attack is not selected by the attacker.
> If the attacker can select when to perform the attack, they are guaranteed to succeed given any value of z, but the expected time required to perform the attack grows exponentially with z [14].
>
> Conclusions
> ===========
>
> Securing Lightning channels and channel factories against forced expiration spam attacks is imperative.
>
> Feerate-Dependent Timelocks (FDTs) provide this security without forcing the timelocks to be extended in the typical case, thus avoiding a capital efficiency vs. safety tradeoff.
> Furthermore, a dishonest user who tries to use a forced expiration spam attack to steal funds is penalized by having their funds timelocked for a longer period, thus discouraging such attacks.
> Finally, FDTs can be made to be highly resistant to attacks by dishonest miners.
>
> FDTs have other uses, including the reduction of feerate risk and the calculation of fee-penalties.
>
> While implementing FDTs requires some additional DRAM and computation, the costs are extremely small.
> Given these advantages and their low costs, it's hoped that the Bitcoin consensus rules will be changed to support FDTs.
>
> Regards,
> John
>
> [1] Poon and Dryja, The Bitcoin Lightning Network, https://lightning.network/lightning-network-paper.pdf
> [2] Burchert, Decker and Wattenhofer, "Scalable Funding of Bitcoin Micropayment Channel Networks", http://dx.doi.org/10.1098/rsos.180089
> [3] Decker, Russell and Osuntokun. "eltoo: A Simple Layer2 Protocol for Bitcoin", https://blockstream.com/eltoo.pdf
> [4] Law, "Efficient Factories For Lightning Channels", https://github.com/JohnLaw2/ln-efficient-factories
> [5] Law, "Scaling Lightning With Simple Covenants", https://github.com/JohnLaw2/ln-scaling-covenants
> [6] Towns, "Re: Scaling Lightning With Simple Covenants", https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-September/021943.html
> [7] Law, "Re: Scaling Lightning With Simple Covenants", https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-November/022175.html
> [8] Towns, "Two-party eltoo w/ punishment", https://lists.linuxfoundation.org/pipermail/lightning-dev/2022-December/003788.html
> [9] Law, "Factory-Optimized Channel Protocols For Lightning", https://github.com/JohnLaw2/ln-factory-optimized
> [10] Law, "Lightning Channels With Tunable Penalties", https://github.com/JohnLaw2/ln-tunable-penalties
> [11] Riard, "Solving CoinPool high-interactivity issue with cut-through update of Taproot leaves", https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-September/021969.html
> [12] Law, "Watchtower-Free Lightning Channels For Casual Users", https://github.com/JohnLaw2/ln-watchtower-free
> [13] Nakamoto. "Bitcoin: A Peer-to-Peer Electronic Cash System", http://bitcoin.org/bitcoin.pdf
> [14] Law, "Scaling Lightning Safely With Feerate-Dependent Timelocks", https://github.com/JohnLaw2/ln-fdts
> [15] Grunspan and Perez-Marco, "Double Spend Races", CoRR, vol. abs/1702.02867, http://arxiv.org/abs/1702.02867v3
> [16] Law, https://github.com/JohnLaw2/ln-fdts
>
>
>
>
> Sent with Proton Mail <https://proton.me/> secure email.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231217/e80ed929/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 11
********************************************
