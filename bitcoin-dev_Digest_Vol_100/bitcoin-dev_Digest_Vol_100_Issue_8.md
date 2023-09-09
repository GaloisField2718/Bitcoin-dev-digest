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

   1. Parameters in BIP21 URIs (kiminuo)
   2. Scaling Lightning With Simple Covenants (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Fri, 08 Sep 2023 14:36:16 +0000
From: kiminuo <kiminuo@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Parameters in BIP21 URIs
Message-ID:
	<aqQNYBhbmUz3LRgMxGzzCiToOGl7Ra_gZAhk5xDnZKwkGv16ly2l3BqjQRD7pjaQ_QQ-3bouXBeNjitvPzfbNlP-NnHMkfampmmqiH1UvN8=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

[Formatted version of this post is here: https://gist.github.com/kiminuo/cc2f19a4c5319e439fc7be8cbe5a39f9]

Hi all,

BIP 21 [https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki] defines a URI scheme for making Bitcoin payments and the purpose of the URI scheme is to enable users to easily make payments by simply clicking links on webpages or scanning QR Codes. An example of a BIP21 URI is:

bitcoin:bc1qd4fxq8y8c7qh76gfnvl7amuhag3z27uw0w9f8p?amount=0.004&label=Kiminuo&message=Donation

Now to make it easier, these URIs are typically clickable. Bitcoin wallets register the "bitcoin" URI scheme so that a BIP21 URI is parsed and data are pre-filled in a form to send your bitcoin to a recipient. Notably, wallets do not send your bitcoin once you click a BIP21 URI, there is still a confirmation step that requires user's attention. Very similar experience is with a QR code that encodes a BIP21 URI where one just scans a QR code and data is, again, pre-filled in a wallet's UI for your convenience.

While working on Wasabi's BIP21 implementation I noticed that based on the BIP21 grammar [https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki#abnf-grammar], it is actually allowed to specify URI parameters multiple times. This means that the following URI is actually valid:

bitcoin:bc1qd4fxq8y8c7qh76gfnvl7amuhag3z27uw0w9f8p?amount=0.004&label=Kiminuo&message=Donation&amount=1.004 (note that the 'amount' parameter is specified twice)

Bitcoin Core implements "the last value wins" behavior[^3] so amount=1.004 will be taken into account and not "amount=0.004"[^4]. However, in general, the fact that the same parameter can be specified multiple times can lead to a confusion for users and developers[^1][^2]. In the worst case, it might be exploited by some social engineering attempts by attempting to craft a 'clever' BIP21 URI and exploting behavior of a particular wallet software. For the record, I'm not aware that it actually happens, so this is rather a concern.

The main question of this post is: Is it useful to allow specifying BIP21 parameters multiple times or is it rather harmful?

Regards,
K.

[^1]: https://github.com/JoinMarket-Org/joinmarket-clientserver/pull/1510
[^2]: https://github.com/MetacoSA/NBitcoin/blob/93ef4532b9f2ea52b2c910266eeb6684f3bd25de/NBitcoin/Payment/BitcoinUrlBuilder.cs#L74-L78
[^3]: I added a test to that effect in https://github.com/bitcoin/bitcoin/pull/27928/files, see https://github.com/bitcoin/bitcoin/blob/83719146047947e588aa0c7b5eee02f44884553d/src/qt/test/uritests.cpp#L68-L73.[^4]: You can test your wallet's behavior by scanning the last image here https://github.com/zkSNACKs/WalletWasabi/pull/10578#issue-1687564404 (or directly https://user-images.githubusercontent.com/58662979/265389405-16893ce8-7c19-4262-bb60-5fd711336685.png).
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230908/bfb88e23/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 08 Sep 2023 18:54:46 +0000
From: jlspc <jlspc@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<vUfA21-18moEP9UiwbWvzpwxxn83yJQ0J4YsnzK4iQGieArfWPpIZblsVs1yxEs9NBpqoMBISuufMsckbuWXZE1qkzXkf36oJKfwDVqQ2as=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

TL;DR
=====
* The key challenge in scaling Lightning in a trust-free manner is the creation of Lightning channels for casual users.
  - It appears that signature-based factories are inherently limited to creating at most tens or hundreds of Lightning channels per UTXO.
  - In contrast, simple covenants (including those enabled by CTV [1] or APO [2]) would allow a single UTXO to create Lightning channels for millions of casual users.
* The resulting covenant-based protocols also:
  - support resizing channels off-chain,
  - use the same capital to simultaneously provide in-bound liquidity to casual users and route unrelated payments for other users,
  - charge casual users tunable penalties for attempting to put an old state on-chain, and
  - allow casual users to monitor the blockchain for just a few minutes every few months without employing a watchtower service.
* As a result, adding CTV and/or APO to Bitcoin's consensus rules would go a long way toward making Lightning a widely-used means of payment.

Overview
========

Many proposed changes to the Bitcoin consensus rules, including CheckTemplateVerify (CTV) [1] and AnyPrevOut (APO) [2], would support covenants.
While covenants have been shown to improve Bitcoin in a number of ways, scalability of Lightning is not typically listed as one of them.
This post argues that any change (including CTV and/or APO) that enables even simple covenants greatly improves Lightning's scalability, while meeting the usability requirements of casual users.
A more complete description, including figures, is given in a paper [3].

The Scalability Problem
=======================

If Bitcoin and Lightning are to become widely-used, they will have to be adopted by casual users who want to send and receive bitcoin, but who do not want to go to any effort in order to provide the infrastructure for making payments.
Instead, it's reasonable to expect that the Lightning infrastructure will be provided by dedicated users who are far less numerous than the casual users.
In fact, there are likely to be tens-of-thousands to millions of casual users per dedicated user.
This difference in numbers implies that the key challenge in scaling Bitcoin and Lightning is providing bitcoin and Lightning to casual users.
As a result, the rest of this post will focus on this challenge.

Known Lightning protocols allow casual users to perform Lightning payments without:
 * maintaining high-availability,
 * performing actions at specific times in the future, or
 * having to trust a third-party (such as a watchtower service) [5][6].

In addition, they support tunable penalties for casual users who attempt to put an old channel state on-chain (for example, due to a crash that causes a loss of state).
As a result, these protocols meet casual users' needs and could become widely-used for payments if they were sufficiently scalable.

The Lightning Network lets users send and receive bitcoin off-chain in a trust-free manner [4].
Furthermore, there are Lightning protocols that allow Lightning channels to be resized off-chain [7].
Therefore, making Lightning payments and resizing Lightning channels are highly scalable operations.

However, providing Lightning channels to casual users is not scalable.
In particular, no known protocol that uses the current Bitcoin consensus rules allows a large number (e.g., tens-of-thousands to millions) of Lightning channels, each co-owned by a casual user, to be created from a single on-chain unspent transaction output (UTXO).
As a result, being able to create (and close) casual users' Lightning channels remains the key bottleneck in scaling Lightning.

Casual Users And Signatures
===========================

Unfortunately, there are good reasons to believe this bottleneck is unavoidable given the current Bitcoin consensus rules.
The problem is that in order for a casual user to co-own a Lightning channel, they must co-own an on-chain UTXO [8].
Therefore, if a large number of casual users are to each co-own a Lightning channel, all of which are funded by a single UTXO, that UTXO must require signatures from all of those casual users.

In practice, the problem is much harder than just getting signatures from a large number of casual users, as the signatures themselves depend on the exact set of casual users whose signatures are required.
For example, if a UTXO requires signatures from a set of 1,000 casual users and if 999 of them sign but one does not, the 999 signatures that were obtained can't be used.
Instead, one has to start all over again, say with a new UTXO that requires signatures from the 999 users that signed the previous time.
However, if not all of those 999 sign, the signatures that were obtained in the second try are also unusable.

The requirement for casual users to sign transactions that specify the exact set of casual users whose signatures are required creates a very difficult group coordination problem that's not well-suited to the behavior of casual users [9, Section 2.2].
As a result, while a channel factory could be used to fund channels for perhaps 10 or even 100 casual users, it's very unlikely that any protocol using the current Bitcoin consensus rules can fund tens-of-thousands to millions of channels from a single UTXO.

Simple Covenants And Timeout-Trees
==================================

On the other hand, if the consensus rules are changed to allow even simple covenants, this scaling bottleneck is eliminated.
The key observation is that with covenants, a casual user can co-own an off-chain Lightning channel without having to sign all (or any) of the transactions on which it depends.
Instead, a UTXO can have a covenant that guarantees the creation of the casual user's channel.
The simplest way to have a single UTXO create channels for a large number of casual users is to put a covenant on the UTXO that forces the creation of a tree of transactions, the leaves of which are the casual users' channels.

While such a covenant tree can create channels for millions of casual users without requiring signatures or solving a difficult group coordination problem, it's not sufficient for scaling.
The problem is that each channel created by a covenant tree has a fixed set of owners, and changing the ownership of a channel created by a covenant tree requires putting the channel on-chain.
Therefore, assuming that all casual users will eventually want to pair with different dedicated users (and vice-versa), the covenant tree doesn't actually provide any long-term scaling benefit.

Fortunately, real long-term scaling can be achieved by adding a deadline after which all non-leaf outputs in the covenant tree can be spent without having to meet the conditions of the covenant.
The resulting covenant tree is called a "timeout-tree" [9, Section 5.3].

Let A_1 ... A_n denote a large number of casual users, let B be a dedicated user, and let E denote some fixed time in the future.
User B creates a timeout-tree with expiry E where:
 * leaf i has an output that funds a Lightning channel owned by A_i and B, and
 * after time E, each non-leaf output in the covenant tree can also be spent by user B without having to meet the conditions of the covenant.

Thus, any time before E, casual user A_i can put the Lightning channel (A_i, B) on-chain by putting all of its ancestors in the timeout-tree on-chain.
Once (A_i, B) is on-chain, the expiry E has no effect so A_i and B can continue to use the Lightning channel to send and receive payments from and to A_i.

On the other hand, sometime shortly before E, casual user A_i can use the Lightning Network to send all of their balance in the channel (A_i, B) to themselves in some other Lightning channel that is the leaf of some other timeout-tree.
More precisely, casual user A_i should rollover their balance by sending it from a given timeout-tree between time E - to_self_delay_i and time E, where E is the timeout-tree's expiry and to_self_delay_i is A_i's Lightning channel safety parameter.
Note that to_self_delay_i can be in the range of 1 to 3 months if a watchtower-free channel protocol is used [5][6], so performing the drain within this time window does not put an unreasonable availability requirement on A_i.

If all casual users drain their balances from the timeout-tree before E, then after E dedicated user B can create a new timeout-tree, with leaves that create Lightning channels for a new set of casual users, by putting a single transaction on-chain that spends the UTXO which created the expired timeout-tree.
In this case, all n of the old Lightning channels are closed and n new channels are created with a single on-chain transaction.

Of course, it's possible that some casual users will put their Lightning channel in the old timeout-tree on-chain, while others will drain their balance from the timeout-tree before E.
In this case, user B can create a new timeout-tree that's funded by the non-leaf outputs of the old timeout-tree that have been put on-chain.
While this results in a larger on-chain footprint than the case in which all casual users drain their balances from the old timeout-tree, it can still provide substantial scaling as long as the number of leaves put on-chain is small (in particular, well below n/(log n)).
By creating incentives that reward users who drain their balances from the timeout-tree rather than putting their channels on-chain, almost all leaves will stay off-chain and good scalability will be achieved.

Passive Rollovers For Casual Users
==================================

The timeout-trees defined above don't place unreasonable availability requirements on casual users and they allow a very large number of casual users to obtain a Lightning channel with a single on-chain transaction.
However, there are two problems with forcing casual users to drain their balances from an old timeout-tree to a new timeout-tree before the old timeout-tree's expiry:
  1) if a casual user fails to perform the required drain before the old timeout-tree's expiry (due to unexpected unavailability), they lose all of their funds in the timeout-tree, and
  2) if the dedicated user B is unavailable when a casual user attempts to drain their funds prior to the timeout-tree's expiry, the casual user will put their timeout-tree leaf on-chain (thus increasing the on-chain footprint and limiting scalability).
This second problem matters, as a casual user should only have to devote a short period (e.g., 10 minutes) every few months to performing the drain, so even a short period of unavailability by the dedicated user could force the casual user to go on-chain.

Instead, it would be preferable if the dedicated user could facilitate the rollover of the casual user's funds from a timeout-tree that's about to expire to another one without requiring input from the casual user.
This can be achieved by using a variation of the FFO-WF Lightning channel protocol [6].
The FFO-WF protocol uses control transactions to determine the current state of the Lightning channel and the resolution of any outstanding HTLCs, and these control transactions determine how the channel's value transactions disperse the channel's funds.

As a result, just prior to E - to_self_delay_i, B can create a new timeout-tree that funds a new Lightning channel with casual user A_i where the new channel is controlled by A_i's *same* control transactions (thus allowing A_i to obtain their funds from either the old or new Lightning channel, but not from both).
Therefore, once the old timeout-tree expires, A_i can still access their funds in the new timeout-tree's Lightning channel without having to perform any actions.
Of course, sometime between E - to_self_delay_i and E, A_i should verify that B has created such a new timeout-tree.

In addition, HTLCs can be handled so that rolling over the casual user's funds from one timeout-tree to another does not require any actions from the casual user.
The details are given in the paper [3].

Off-Chain bitcoin
=================

The Lightning Network lets casual users send and receive bitcoin entirely off-chain
However, the casual user has to wait (for a period of time specified by their Lightning partner's to_self_delay parameter) before they can access their Lightning funds on-chain.
This is problematic, as accessing one's Lightning funds on-chain requires paying fees to put transactions on-chain, and those fees cannot be paid using one's Lightning funds (due to the delay mentioned above).
Thus, while Lightning can be used for most of a user's funds, the user must also be able to access some bitcoin (enough to pay transaction fees) without any delays.

Fortunately, timeout-trees can be used to provide casual users with immediately-accessible off-chain bitcoin in addition to bitcoin in Lightning channels.
Furthermore, it's possible to use a control output owned by a casual user to rollover the casual user's immediately-accessible bitcoin from one timeout-tree to the next along with their Lightning funds [3].
In fact, this rollover can also be done without requiring any actions from the casual user and it can be used to rebalance the fraction of the user's funds that are immediately-accessible versus within Lightning [3].

Control UTXOs
=============

The FFO-WF protocol (as adapted for timeout-trees) requires that each casual user own an independent UTXO that is spent by that user's control transactions.
Creating an on-chain UTXO for every casual user could require a significant on-chain footprint, thus limiting scalability.
Instead, each casual user can be given an off-chain UTXO that is created by a leaf of a tree of off-chain transactions defined by covenants [3].

Improving Capital Efficiency
============================

In order to rollover funds from one timeout-tree to another, the dedicated user creating those timeout-trees must fund both the old and new timeout-trees simultaneously, even though they only create one timeout-tree's worth of Lightning channel capacity.
Fortunately, this overhead can be made very small by funding multiple timeout-trees in a staggered fashion, where only one has to be rolled-over at a time [3].

Also, because casual users may send and receive payments infrequently, the dedicated user's capital devoted to timeout-trees may generate few routing fees.
As a result, casual users may have to pay significant fees for the creation of their Lightning channels (and/or for payments to or from those channels).

However, the fees that casual users have to pay could be reduced if the capital in their channels could also be used for routing payments between other users.
This can be accomplished by having the timeout-trees create hierarchical channels, each of which is owned by a single casual user and a pair of dedicated users [7].
By using an idea created by Towns [10][11][3], a single unit of capital in each hierarchical channel can be used to route two independent payments of one unit each.

Scalability
===========

The above protocols can perform the following actions completely off-chain:
  * Lightning sends and receives, and
  * resizing of Lightning channels.

Assuming:
  * 1 million hierarchical Lightning channels per timeout-tree,
  * a 1,000-block (about a week) to_self_delay parameter for dedicated users, and
  * a 10,000-block (about 69 days) to_self_delay parameter for casual users, and
  * 121,000 blocks (about 2.3 years) from the creation of each timeout-tree to its expiry,

a single 1-input/2-output transaction per block provides:
  * 11 Lightning channels per casual user to each of 10 billion casual users [3].

Furthermore, given the above assumptions, a single 1-input/2-output transaction per block allows each casual user to:
  * close an existing Lightning channel,
  * open a new Lightning channel with a new partner, and
  * rebalance funds between Lightning and immediately-accessible off-chain bitcoin
once every 10,000 blocks (about 69 days) [3].

Of course, the above calculations don't mean that 10 billion casual Lightning users would create only 1 on-chain transaction per block.
In reality, their on-chain footprint would be dominated by users who don't follow the protocol due to errors, unavailability, or malicious intent.
The rate of such protocol violations is hard to predict, but it's likely that casual users' unavailability would be the most significant problem.

Usability
=========

The above protocols have the following properties for casual users:
  * watchtower-freedom (that is, they accommodate months-long unavailability without requiring a watchtower service to secure the user's funds) ([5] Section 3.1),
  * one-shot receives (that is, receiving a payment does not require performing actions at multiple blockheights) ([5] Section 3.4),
  * asynchronous receives (that is, it's possible to receive a payment when the sender is offline) ([5] Section 3.6), and
  * tunable penalties for attempting to put an old state on-chain ([12]).

Limitations
===========

Finally, the above results depend on the following assumptions:
  1) the cost of resolving an HTLC on-chain is less than the value of the HTLC,
  2) transaction packages are relayed reliably from users to miners, and
  3) there is a known upper bound on the delay from when a package is submitted to when it is included in the blockchain.

These limitations, and ideas for how they can be addressed, are discussed further in the paper [3].

Conclusions
===========

With the current Bitcoin consensus rules, there are reasons to believe that the scalability of Lightning is inherently limited.
However, simple covenants and timeout-trees can overcome these scalability limitations.
In particular, CheckTemplateVerify (CTV) and/or AnyPrevOut (APO) could be used to dramatically increase the number of casual users who send and receive bitcoin in a trust-free manner.
As a result, it's hoped that CTV, APO or a similar mechanism that enables simple covenants will be added to Bitcoin's consensus rules in order to allow Lightning to become a widely-used means of payment.

Regards,
John

[1] BIP 119 CHECKTEMPLATEVERIFY, https://github.com/bitcoin/bips/blob/master/bip-0119.mediawiki
[2] BIP 118 SIGHASH_ANYPREVOUT, https://anyprevout.xyz/
[3] Law, "Scaling Lightning With Simple Covenants", https://github.com/JohnLaw2/ln-scaling-covenants
[4] "BOLT (Basis Of Lightning Technology) specifications", https://github.com/lightningnetwork/lightning-rfc
[5] Law, "Watchtower-Free Lightning Channels For Casual Users", https://github.com/JohnLaw2/ln-watchtower-free
[6] Law, "Factory-Optimized Channel Protocols For Lightning", available at https://github.com/JohnLaw2/ln-factory-optimized.
[7] Law, "Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://github.com/JohnLaw2/ln-hierarchical-channels
[8] Burchert, Decker and Wattenhofer, "Scalable Funding of Bitcoin Micropayment Channel Networks", http://dx.doi.org/10.1098/rsos.180089
[9] Law, "Scaling Bitcoin With Inherited IDs", https://github.com/JohnLaw2/btc-iids
[10] Towns, "Re: Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-April/003913.html
[11] Law, "Re: Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-April/003917.html
[12] Law, "Lightning Channels With Tunable Penalties", https://github.com/JohnLaw2/ln-tunable-penalties

Sent with [Proton Mail](https://proton.me/) secure email.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230908/90196255/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 8
*******************************************
