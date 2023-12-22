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

   1. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Gloria Zhao)
   2. Re: HTLC output aggregation as a mitigation for tx recycling,
      jamming, and on-chain efficiency (covenants) (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Wed, 20 Dec 2023 19:13:22 +0000
From: Gloria Zhao <gloriajzhao@gmail.com>
To: Peter Todd <pete@petertodd.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID:
	<CAFXO6=KS05So_5FizLJxCLEPwBxNPV9Wrgi=9sjzmrZ+PLpLOQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Peter,

Thanks for spending time thinking about RBF pinning and v3.

> Enter Mallory. His goal is to grief Alice by forcing her to spend more
money
than she intended...
> ...Thus the total fee of Mallory's package would have
> been 6.6 * 1/2.5 = 2.6x more than Alice's total fee, and to get her
transaction
> mined prior to her deadline, Alice would have had to pay a 2.6x higher
fee than
> expected.

I think this is a good understanding of the goal of Rule #3, but I'm not
sure how you're getting these numbers without specifying the size and fees
of the commitment transaction. We should also quantify the severity of the
"damage" of this pin in a meaningful way; the issue of "Alice may need to
pay to replace descendant(s) she isn't aware of" is just a property of
allowing unconfirmed descendants.

Let's use some concrete numbers with your example. As you describe, we need
80-162sat/vB to get into the next block, and Alice can fund a CPFP with a
152vB CPFP. Let's say the commitment transaction has size N, and pays 0
fees.

The lower number of 80sat/vB describes what Mallory needs to shoot below in
order to "pay nothing" for the attack (i.e. otherwise it's a CPFP and gets
the tx confirmed). Mallory can maximize the cost of replacement according
to Rule #3 by keeping a low feerate while maximizing the size of the tx.

The higher number of 162sat/vB describes the reasonable upper bound of what
Alice should pay to get the transactions confirmed. As in: If Alice pays
exactly 162sat/vB * (N + 152vB) satoshis to get her tx confirmed, nothing
went wrong. She hopes to not pay more than that, but she'll keep
broadcasting higher bumps until it confirms.

The "damage" of the pin can quantified by the extra fees Alice has to pay.

For a v3 transaction, Mallory can attach 1000vB at 80sat/vB. This can
increase the cost of replacement to 80,000sat.
For a non-v3 transaction, Mallory can attach (101KvB - N) before maxing out
the descendant limit.
Rule #4 is pretty negligible here, but since you've already specified
Alice's child as 152vB, she'll need to pay Rule #3 + 152sats for a
replacement.

Let's say N is 1000vB. AFAIK commitment transactions aren't usually smaller
than this:
- Alice is happy to pay 162sat/vB * (1000 + 152vB) = 186,624sat
- In a v3 world, Mallory can make the cost to replace 80sat/vB * (1000vB) +
152 = 80,152sat
    - Mallory doesn't succeed, Alice's CPFP easily pays for the replacement
- In a non-v3 world, Mallory can make the cost to replace 80sat/vB *
(100,000vB) + 152 = 8,000,152sat
    - Mallory does succeed, Alice would need to pay ~7 million sats extra

Let's say N is 10,000vB:
- Alice is happy to pay 162sat/vB * (10,000 + 152vB) = 1,644,624
- In a v3 world, Mallory can make the cost to replace 80sat/vB * (1000vB) +
152 = 80,152sat
    - Mallory doesn't succeed, Alice's CPFP easily pays for the replacement
- In a non-v3 world, Mallory can make the cost to replace 80sat/vB *
(91,000vB) + 152 = 7,280,152sat
    - Mallory does succeed Alice would need to pay ~5 million sats extra

Let's say N is 50,000vB:
- Alice is happy to pay 162sat/vB * (50,000 + 152vB) = 8,124,624
- In a v3 world, Mallory can make the cost to replace 80sat/vB * (1000vB) +
152 = 80,152sat
    - Mallory doesn't succeed, Alice's CPFP easily pays for the replacement
- In a non-v3 world, Mallory can make the cost to replace 80sat/vB *
(51,000vB) + 152 = 4,080,152sat
    - Mallory doesn't succeed, Alice's CPFP easily pays for the replacement
    - The key idea here is that there isn't much room for descendants and
the cost to CPFP is very high

These numbers change if you tweak more variables - the fees paid by the
commitment tx, the feerate range, etc. But the point here is to reduce the
potential "damage" by 100x by restricting the allowed child size.

> If V3 children are restricted to, say, 200vB, the attack is much less
effective
as the ratio of Alice vs Mallory size is so small.

This is exactly the idea; note that we've come from 100KvB to 1000vB.

> Mallory can improve the efficiency of his griefing attack by attacking
multiple
> targets at once. Assuming Mallory uses 1 taproot input and 1 taproot
output for
> his own funds, he can spend 21 ephemeral anchors in a single 1000vB
> transaction.

Note that v3 does not allow more than 1 unconfirmed parent per tx.

Let me know if I've made an arithmetic error, but hopefully the general
idea is clear.

Best,
Gloria

On Wed, Dec 20, 2023 at 5:16?PM Peter Todd via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> V3 transactions(1) is a set of transaction relay policies intended to aim
> L2/contracting protocols, namely Lightning. The main aim of V3
> transactions is
> to solve Rule 3 transaction pinning(2), allowing the use of ephemeral
> anchors(3) that do not contain a signature check; anchor outputs that _do_
> contain a signature check are not vulnerable to pinning attacks, as only
> the
> intended party is able to spend them while unconfirmed.
>
> The main way that V3 transactions aims to mitigate transaction pinning is
> with
> the following rule:
>
>     A V3 transaction that has an unconfirmed V3 ancestor cannot be larger
> than
>     1000 virtual bytes.
>
> Unfortunately, this rule - and thus V3 transactions - is insufficient to
> substantially mitigate transaction pinning attacks.
>
>
> # The Scenario
>
> To understand why, let's consider the following scenario: Alice has a
> Lightning
> channel with Bob, who has become unresponsive. Alice is using a Lightning
> protocol where using V3 commitment transactions with a single OP_TRUE
> ephemeral
> anchor of zero value.  The commitment transaction must be broadcast in a
> package, containing both the commitment transaction, and a transaction
> spending
> the anchor output; regardless of the fee of the commitment transaction,
> this is
> a hard requirement, as the zero-valued output is considered non-standard
> by V3
> rules unless spent in the same package.
>
> To pay for the transaction fee of the commitment transaction, Alice spends
> the
> ephemeral output in a 2 input, 1 output, taproot transaction of 152vB in
> size,
> with sufficient feerate Ra to get the transaction mined in what Alice
> considers to be a reasonable amount of time.
>
>
> # The Attack
>
> Enter Mallory. His goal is to grief Alice by forcing her to spend more
> money
> than she intended, at minimum cost. He also maintains well connected nodes,
> giving him the opportunity to both learn about new transactions, and
> quickly
> broadcast transactions to a large number of nodes at once.
>
> When Mallory learns about Alice's commitment+anchor spend package, he
> signs a
> replacement anchor spend transaction, 1000vB in size, with a lower feerate
> Rm
> such that the total fee of Alice's anchor spend is <= Mallory's anchor
> spend
> (in fact, the total fee can be even less due to BIP-125 RBF Rule #4, but
> for
> sake of a simple argument we'll ignore this). Next, Mallory broadcast's
> that
> package widely, using his well-connected nodes.
>
> Due to Rule #3, Alice's higher feerate transaction package does not replace
> Mallory's lower fee rate, higher absolute fee, transaction package. Alice's
> options are now:
>
> 1. Wait for Mallory's low feerate transaction to be mined (mempool
> expiration
>    does not help here, as Mallory can rebroadcast it indefinitely).
> 2. Hope her transaction got to a miner, and wait for it to get mined.
> 3. Replace it with an even higher fee transaction, spending at least as
> much
>    money as Mallory allocated.
>
> In option #1 and #3, Mallory paid no transaction fees to do the attack.
>
> Unfortunately for Alice, feerates are often quite stable. For example, as I
> write this, the feerate required to get into the next block is 162sat/vB,
> while
> the *lowest* feerate transaction to get mined in the past 24 hours is
> approximately 80sat/vB, a difference of just 2x.
>
> Suppose that in this circumstance Alice needs to get her commitment
> transaction
> mined within 24 hours. If Mallory used a feerate of 1/2.5th that of Alice,
> Mallory's transaction would not have gotten mined in the 24 hour period,
> with a
> reasonable safety margin. Thus the total fee of Mallory's package would
> have
> been 6.6 * 1/2.5 = 2.6x more than Alice's total fee, and to get her
> transaction
> mined prior to her deadline, Alice would have had to pay a 2.6x higher fee
> than
> expected.
>
>
> ## Multi-Party Attack
>
> Mallory can improve the efficiency of his griefing attack by attacking
> multiple
> targets at once. Assuming Mallory uses 1 taproot input and 1 taproot
> output for
> his own funds, he can spend 21 ephemeral anchors in a single 1000vB
> transaction.
>
> Provided that the RBF Rule #4 feerate delta is negligible relative to
> current
> feerates, Mallory can build up the attack against multiple targets by
> broadcasting replacements with slightly higher feerates as needed to add
> and
> remove Alice's.
>
> The cost of the attack to Mallory is estimating fees incorrectly, and
> using a
> sufficiently high feerate that his transaction does in fact get mined. In
> that
> circumstance, if he's attacking multiple targets, it is likely that all his
> transactions would get mined at once. Thus having only a single attack
> transaction reduces that worst case cost. Since Mallory can adding and
> remove
> Alice's, he can still force multiple Alice's to spend funds bumping their
> transactions.
>
>
> # Solutions
>
> ## Replace-by-Feerate
>
> Obviously, this attack does not work if Rule #3 is removed for small
> transactions, allowing Alice's transaction to replace Mallory via
> replace-by-feerate. In the common situation where mempools are deep, this
> is
> arguably miner incentive compatible as other transactions at essentially
> the
> same feerate will simply replace the "space" taken up by the griefing
> transaction.
>
>
> ## Restrict V3 Children Even Further
>
> If V3 children are restricted to, say, 200vB, the attack is much less
> effective
> as the ratio of Alice vs Mallory size is so small. Of course, this has the
> disadvantage of making it more difficult in some cases to find sufficient
> UTXO's to pay for fees, and increasing the number of UTXO's needed to fee
> bump
> large numbers of transactions.
>
>
> # References
>
> 1)
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-September/020937.html
> ,
>    "[bitcoin-dev] New transaction policies (nVersion=3) for contracting
> protocols",
>    Gloria Zhao, Sep 23 2022
>
> 2)
> https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki#implementation-details
> ,
>    "The replacement transaction pays an absolute fee of at least the sum
> paid by the original transactions."
>
> 3)
> https://github.com/instagibbs/bips/blob/ephemeral_anchor/bip-ephemeralanchors.mediawiki
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231220/9bcfdea2/attachment.html>

------------------------------

Message: 2
Date: Thu, 21 Dec 2023 14:34:36 +0100
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] HTLC output aggregation as a mitigation for
	tx recycling, jamming, and on-chain efficiency (covenants)
Message-ID:
	<CAD3i26BT-idOLOSZ9o2f1EnbQSt2GYAC=2mVp0GGSZ5uUakLBg@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

> Bob can craft a HTLC-preimage spend of the single offered output spending one of 0.1 BTC HTLC payout (and revealing its preimage) while burning all the value as fee. This replaces out Alice's honest HTLC-timeout out of network mempools, are they're concurrent spend. Bob can repeat this trick as long as there is HTLC "payout" remaining in the offered set, until he's being able to do a HTLC off-chain double-spend of the 1 BTC HTLC "payout".

What do you mean by "do a HTLC off-chain double-spend of the 1 BTC
HTLC"? Agreed on every detail up to this point.

Note that every time Bob replaces Alice's timeout tx, he reveals a
preimage that Alice can use to settle her incoming HTLC, so for those
Alice loses nothing, Bob loses the HTLC value to fees.

I believe for Bob to be able to profit from this, he would need to
delay all of Alice's transactions until the timelock on Alice's
incoming HTLC expires (CLTV delta blocks). Is this what you mean by
"off-chain double spend"?

Anyways, this means that Bob will have to pay ~next block fees each
block in the delta period (assuming Alice is eager to get into the
block since the timelocks are expiring on her incoming HTLCs), and
burn the value of an HTLC for every such transaction.

However, I think it is possible to make this very risky for Bob to
play out, based on a simple fact:
Alice can claim all the expired HTLCs cheaply (1 input 1 output tx, no
merkle paths or preimages needed), and she is game theoretically
willing to burn almost all of it to fees to get it confirmed before
expiry. So for the last 1 BTC HTLC, she could pay ~0.9 BTC to fees,
which Bob couldn't compete with by burning the much smaller HTLCs.
However, Bob could of course grief Alice by making her do this, but
unsure if that's rational.



On Sun, Dec 17, 2023 at 11:56?PM Antoine Riard <antoine.riard@gmail.com> wrote:
>
> Hi Johan,
>
> > Is this a concern though, if we assume there's no revoked state that
> > can be broadcast (Eltoo)? Could you share an example of how this would
> > be played out by an attacker?
>
> Sure, let's assume no revoked state can be broadcast (Eltoo).
>
> My understanding of the new covenant mechanism is the aggregation or collapsing of all HTLC outputs in one or at least 2 outputs (offered / received).
> Any spend of an aggregated HTLC "payout" should satisfy the script locking condition by presenting a preimage and a signature.
> An offerd aggregated HTLC output might collapse a M number of HTLC "payout", where M is still limited by the max standard transaction relay, among other things.
>
> The offered-to counterparty can claim any subset N of the aggregation M by presenting the list of signatures and preimages (How they're feeded to the spent script is a covenant implementation detail). However, there is no guarantee that the offered-to counterparty reveal "all" the preimages she is awarded off. Non-spent HTLC outputs are clawback to a remainder subset of M, M'.
>
> I think this partial reveal of HTLC payout preimages still opens the door to replacement cycling attacks.
>
> Let's say you have 5 offered HTLC "payouts" between Alice and Bob aggregated in a single output, 4 of value 0.1 BTC and 1 of value 1 BTC. All expire at timelock T.
> At T, Alice broadcasts an aggregated HTLC-timeout spend for the 5 HTLC with 0.0.1 BTC on-chain fee.
>
> Bob can craft a HTLC-preimage spend of the single offered output spending one of 0.1 BTC HTLC payout (and revealing its preimage) while burning all the value as fee. This replaces out Alice's honest HTLC-timeout out of network mempools, are they're concurrent spend. Bob can repeat this trick as long as there is HTLC "payout" remaining in the offered set, until he's being able to do a HTLC off-chain double-spend of the 1 BTC HTLC "payout".
>
> This stealing gain of the 1 BTC HTLC "payout" covers what has been burned as miners fees to replace cycle out Alice's sequence of honest HTLC-timeout.
>
> And it should be noted that Bob might benefit from network mempools congestion delaying the confirmation of his malicious low-value high-fee HTLC-preimage transactions.
>
> > I'm not sure what you mean here, could you elaborate?
>
> See https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-December/022191.html and my answer there.
> I think "self-sustained" fees is one only part of the solution, the other part being the sliding delay of the HTLC timelock based on block feerate.
> Otherwise, a replacement cycling attacker can always benefit from network mempools congestion spontaneously pushing out a malicious cycling transaction out of block templates.
>
> > That sounds possible, but how would you deal with the exponential
> > blowup in the number of combinations?
>
> In a taproot-world, "swallow the bullet" in terms of witness size growth in case of non-cooperative closure.
> I think this is where introducing an accumulator at the Script level to efficiently test partial set membership would make sense.
> Note, exponential blowup is an issue for mass non-coordinated withdrawals of a payment pool too.
>
> Best,
> Antoine
>
>
> Le lun. 11 d?c. 2023 ? 09:17, Johan Tor?s Halseth <johanth@gmail.com> a ?crit :
>>
>> Hi, Antoine.
>>
>> > The attack works on legacy channels if the holder (or local) commitment transaction confirms first, the second-stage HTLC claim transaction is fully malleable by the counterparty.
>>
>> Yes, correct. Thanks for pointing that out!
>>
>> > I think one of the weaknesses of this approach is the level of malleability still left to the counterparty, where one might burn in miners fees all the HTLC accumulated value promised to the counterparty, and for which the preimages have been revealed off-chain.
>>
>> Is this a concern though, if we assume there's no revoked state that
>> can be broadcast (Eltoo)? Could you share an example of how this would
>> be played out by an attacker?
>>
>> > I wonder if a more safe approach, eliminating a lot of competing interests style of mempool games, wouldn't be to segregate HTLC claims in two separate outputs, with full replication of the HTLC lockscripts in both outputs, and let a covenant accepts or rejects aggregated claims with satisfying witness and chain state condition for time lock.
>>
>> I'm not sure what you mean here, could you elaborate?
>>
>> > I wonder if in a PTLC world, you can generate an aggregate curve point for all the sub combinations of scalar plausible. Unrevealed curve points in a taproot branch are cheap. It might claim an offered HTLC near-constant size too.
>>
>> That sounds possible, but how would you deal with the exponential
>> blowup in the number of combinations?
>>
>> Cheers,
>> Johan
>>
>>
>> On Tue, Nov 21, 2023 at 3:39?AM Antoine Riard <antoine.riard@gmail.com> wrote:
>> >
>> > Hi Johan,
>> >
>> > Few comments.
>> >
>> > ## Transaction recycling
>> > The transaction recycling attack is made possible by the change made
>> > to HTLC second level transactions for the anchor channel type[8];
>> > making it possible to add fees to the transaction by adding inputs
>> > without violating the signature. For the legacy channel type this
>> > attack was not possible, as all fees were taken from the HTLC outputs
>> > themselves, and had to be agreed upon by channel counterparties during
>> > signing (of course this has its own problems, which is why we wanted
>> > to change it).
>> >
>> > The attack works on legacy channels if the holder (or local) commitment transaction confirms first, the second-stage HTLC claim transaction is fully malleable by the counterparty.
>> >
>> > See https://github.com/lightning/bolts/blob/master/03-transactions.md#offered-htlc-outputs (only remote_htlcpubkey required)
>> >
>> > Note a replacement cycling attack works in a future package-relay world too.
>> >
>> > See test: https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf
>> >
>> > > The idea of HTLC output aggregation is to collapse all HTLC outputs on
>> > > the commitment to a single one. This has many benefits (that I?ll get
>> > > to), one of them being the possibility to let the spender claim the
>> > > portion of the output that they?re right to, deciding how much should
>> > > go to fees. Note that this requires a covenant to be possible.
>> >
>> > Another advantage of HTLC output aggregation is the reduction of fee-bumping reserves requirements on channel counterparties, as second-stage HTLC transactions have common fields (nVersion, nLocktime, ...) *could* be shared.
>> >
>> > > ## A single HTLC output
>> > > Today, every forwarded HTLC results in an output that needs to be
>> > > manifested on the commitment transaction in order to claw back money
>> > > in case of an uncooperative channel counterparty. This puts a limit on
>> > > the number of active HTLCs (in order for the commitment transaction to
>> > > not become too large) which makes it possible to jam the channel with
>> > > small amounts of capital [1]. It also turns out that having this limit
>> > > be large makes it expensive and complicated to sweep the outputs
>> > > efficiently [2].
>> >
>> > > Instead of having new HTLC outputs manifest for each active
>> > > forwarding, with covenants on the base layer one could create a single
>> > > aggregated output on the commitment. The output amount being the sum
>> > > of the active HTLCs (offered and received), alternatively one output
>> > > for received and one for offered. When spending this output, you would
>> > > only be entitled to the fraction of the amount corresponding to the
>> > > HTLCs you know the preimage for (received), or that has timed out
>> > > (offered).
>> >
>> > > ## Impacts to transaction recycling
>> > > Depending on the capabilities of the covenant available (e.g.
>> > > restricting the number of inputs to the transaction) the transaction
>> > > spending the aggregated HTLC output can be made self sustained: the
>> > > spender will be able to claim what is theirs (preimage or timeout) and
>> > > send it to whatever output they want, or to fees. The remainder will
>> > > go back into a covenant restricted output with the leftover HTLCs.
>> > > Note that this most likely requires Eltoo in order to not enable fee
>> > > siphoning[7].
>> >
>> > I think one of the weaknesses of this approach is the level of malleability still left to the counterparty, where one might burn in miners fees all the HTLC accumulated value promised to the counterparty, and for which the preimages have been revealed off-chain.
>> >
>> > I wonder if a more safe approach, eliminating a lot of competing interests style of mempool games, wouldn't be to segregate HTLC claims in two separate outputs, with full replication of the HTLC lockscripts in both outputs, and let a covenant accepts or rejects aggregated claims with satisfying witness and chain state condition for time lock.
>> >
>> > > ## Impacts to slot jamming
>> > > With the aggregated output being a reality, it changes the nature of
>> > > ?slot jamming? [1] significantly. While channel capacity must still be
>> > > reserved for in-flight HTLCs, one no longer needs to allocate a
>> > > commitment output for each up to some hardcoded limit.
>> >
>> > > In today?s protocol this limit is 483, and I believe most
>> > > implementations default to an even lower limit. This leads to channel
>> > > jamming being quite inexpensive, as one can quickly fill a channel
>> > > with small HTLCs, without needing a significant amount of capital to
>> > > do so.
>> >
>> > > The origins of the 483 slot limits is the worst case commitment size
>> > > before getting into unstandard territory [3]. With an aggregated
>> > > output this would no longer be the case, as adding HTLCs would no
>> > > longer affect commitment size. Instead, the full on-chain footprint of
>> > > an HTLC would be deferred until claim time.
>> >
>> > > Does this mean one could lift, or even remove the limit for number of
>> > > active HTLCs? Unfortunately, the obvious approach doesn?t seem to get
>> > > rid of the problem entirely, but mitigates it quite a bit.
>> >
>> > Yes, protocol limit of 483 is a long-term limit on the payment throughput of the LN, though as an upper bound we have the dust limits and mempool fluctuations rendering irrelevant the claim of such aggregated dust outputs. Aggregated claims might give a more dynamic margin of what is a tangible and trust-minimized HTLC payment.
>> >
>> > > ### Slot jamming attack scenario
>> > > Consider the scenario where an attacker sends a large number of
>> > > non-dust* HTLCs across a channel, and the channel parties enforce no
>> > > limit on the number of active HTLCs.
>> >
>> > > The number of payments would not affect the size of the commitment
>> > > transaction at all, only the size of the witness that must be
>> > > presented when claiming or timing out the HTLCs. This means that there
>> > > is still a point at which chain fees get high enough for the HTLC to
>> > > be uneconomical to claim. This is no different than in today?s spec,
>> > > and such HTLCs will just be stranded on-chain until chain fees
>> > > decrease, at which point there is a race between the success and
>> > > timeout spends.
>> >
>> > > There seems to be no way around this; if you want to claim an HTLC
>> > > on-chain, you need to put the preimage on-chain. And when the HTLC
>> > > first reaches you, you have no way of predicting the future chain fee.
>> > > With a large number of uneconomical HTLCs in play, the total BTC
>> > > exposure could still be very large, so you might want to limit this
>> > > somewhat.
>> >
>> > > * Note that as long as the sum of HTLCs exceeds the dust limit, one
>> > > could manifest the output on the transaction.
>> >
>> > Unless we introduce sliding windows during which the claim periods of an HTLC can be claimed and freeze accordingly the HTLC-timeout path.
>> >
>> > See: https://fc22.ifca.ai/preproceedings/119.pdf
>> >
>> > Bad news: you will need off-chain consensus on the feerate threshold at which the sliding windows kick-out among all the routing nodes participating in the HTLC payment path.
>> >
>> > > ## The good news
>> > > With an aggregated HTLC output, the number of HTLCs would no longer
>> > > impact the commitment transaction size while the channel is open and
>> > > operational.
>> >
>> > > The marginal cost of claiming an HTLC with a preimage on-chain would
>> > > be much lower; no new inputs or outputs, only a linear increase in the
>> > > witness size. With a covenant primitive available, the extra footprint
>> > > of the timeout and success transactions would no longer exist.
>> >
>> > > Claiming timed out HTLCs could still be made close to constant size
>> > > (no preimage to present), so no additional on-chain cost with more
>> > > HTLCs.
>> >
>> > I wonder if in a PTLC world, you can generate an aggregate curve point for all the sub combinations of scalar plausible. Unrevealed curve points in a taproot branch are cheap. It might claim an offered HTLC near-constant size too.
>> >
>> > > ## The bad news
>> > > The most obvious problem is that we would need a new covenant
>> > > primitive on L1 (see below). However, I think it could be beneficial
>> > > to start exploring these ideas now in order to guide the L1 effort
>> > > towards something we could utilize to its fullest on L2.
>> >
>> > > As mentioned, even with a functioning covenant, we don?t escape the
>> > > fact that a preimage needs to go on-chain, pricing out HTLCs at
>> > > certain fee rates. This is analogous to the dust exposure problem
>> > > discussed in [6], and makes some sort of limit still required.
>> >
>> > Ideally such covenant mechanisms would generalize to the withdrawal phase of payment pools, where dozens or hundreds of participants wish to confirm their non-competing withdrawal transactions concurrently. While unlocking preimage or scalar can be aggregated in a single witness, there will still be a need to verify that each withdrawal output associated with an unlocking secret is present in the transaction.
>> >
>> > Maybe few other L2s are answering this N-inputs-to-M-outputs pattern with advanced locking scripts conditions to satisfy.
>> >
>> > > ### Open question
>> > > With PTLCs, could one create a compact proof showing that you know the
>> > > preimage for m-of-n of the satoshis in the output? (some sort of
>> > > threshold signature).
>> >
>> > > If we could do this we would be able to remove the slot jamming issue
>> > > entirely; any number of active PTLCs would not change the on-chain
>> > > cost of claiming them.
>> >
>> > See comments above, I think there is a plausible scheme here you just generate all the point combinations possible, and only reveal the one you need at broadcast.
>> >
>> > > ## Covenant primitives
>> > > A recursive covenant is needed to achieve this. Something like OP_CTV
>> > > and OP_APO seems insufficient, since the number of ways the set of
>> > > HTLCs could be claimed would cause combinatorial blowup in the number
>> > > of possible spending transactions.
>> >
>> > > Personally, I?ve found the simple yet powerful properties of
>> > > OP_CHECKCONTRACTVERIFY [4] together with OP_CAT and amount inspection
>> > > particularly interesting for the use case, but I?m certain many of the
>> > > other proposals could achieve the same thing. More direct inspection
>> > > like you get from a proposal like OP_TX[9] would also most likely have
>> > > the building blocks needed.
>> >
>> > As pointed out during the CTV drama and payment pool public discussion years ago, what would be very useful to tie-break among all covenant constructions would be an efficiency simulation framework. Even if the same semantic can be achieved independently by multiple covenants, they certainly do not have the same performance trade-offs (e.g average and worst-case witness size).
>> >
>> > I don't think the blind approach of activating many complex covenants at the same time is conservative enough in Bitcoin, where one might design "malicious" L2 contracts, of which the game-theory is not fully understood.
>> >
>> > See e.g https://blog.bitmex.com/txwithhold-smart-contracts/
>> >
>> > > ### Proof-of-concept
>> > > I?ve implemented a rough demo** of spending an HTLC output that pays
>> > > to a script with OP_CHECKCONTRACTVERIFY to achieve this [5]. The idea
>> > > is to commit to all active HTLCs in a merkle tree, and have the
>> > > spender provide merkle proofs for the HTLCs to claim, claiming the sum
>> > > into a new output. The remainder goes back into a new output with the
>> > > claimed HTLCs removed from the merkle tree.
>> >
>> > > An interesting trick one can do when creating the merkle tree, is
>> > > sorting the HTLCs by expiry. This means that one in the timeout case
>> > > claim a subtree of HTLCs using a single merkle proof (and RBF this
>> > > batched timeout claim as more and more HTLCs expire) reducing the
>> > > timeout case to constant size witness (or rather logarithmic in the
>> > > total number of HTLCs).
>> >
>> > > **Consider it an experiment, as it is missing a lot before it could be
>> > > usable in any real commitment setting.
>> >
>> > I think this is an interesting question if more advanced cryptosystems based on assumptions other than the DL problem could constitute a factor of scalability of LN payment throughput by orders of magnitude, by decoupling number of off-chain payments from the growth of the on-chain witness size need to claim them, without lowering in security as with trimmed HTLC due to dust limits.
>> >
>> > Best,
>> > Antoine
>> >
>> > Le jeu. 26 oct. 2023 ? 20:28, Johan Tor?s Halseth via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> a ?crit :
>> >>
>> >> Hi all,
>> >>
>> >> After the transaction recycling has spurred some discussion the last
>> >> week or so, I figured it could be worth sharing some research I?ve
>> >> done into HTLC output aggregation, as it could be relevant for how to
>> >> avoid this problem in a future channel type.
>> >>
>> >> TLDR; With the right covenant we can create HTLC outputs that are much
>> >> more chain efficient, not prone to tx recycling and harder to jam.
>> >>
>> >> ## Transaction recycling
>> >> The transaction recycling attack is made possible by the change made
>> >> to HTLC second level transactions for the anchor channel type[8];
>> >> making it possible to add fees to the transaction by adding inputs
>> >> without violating the signature. For the legacy channel type this
>> >> attack was not possible, as all fees were taken from the HTLC outputs
>> >> themselves, and had to be agreed upon by channel counterparties during
>> >> signing (of course this has its own problems, which is why we wanted
>> >> to change it).
>> >>
>> >> The idea of HTLC output aggregation is to collapse all HTLC outputs on
>> >> the commitment to a single one. This has many benefits (that I?ll get
>> >> to), one of them being the possibility to let the spender claim the
>> >> portion of the output that they?re right to, deciding how much should
>> >> go to fees. Note that this requires a covenant to be possible.
>> >>
>> >> ## A single HTLC output
>> >> Today, every forwarded HTLC results in an output that needs to be
>> >> manifested on the commitment transaction in order to claw back money
>> >> in case of an uncooperative channel counterparty. This puts a limit on
>> >> the number of active HTLCs (in order for the commitment transaction to
>> >> not become too large) which makes it possible to jam the channel with
>> >> small amounts of capital [1]. It also turns out that having this limit
>> >> be large makes it expensive and complicated to sweep the outputs
>> >> efficiently [2].
>> >>
>> >> Instead of having new HTLC outputs manifest for each active
>> >> forwarding, with covenants on the base layer one could create a single
>> >> aggregated output on the commitment. The output amount being the sum
>> >> of the active HTLCs (offered and received), alternatively one output
>> >> for received and one for offered. When spending this output, you would
>> >> only be entitled to the fraction of the amount corresponding to the
>> >> HTLCs you know the preimage for (received), or that has timed out
>> >> (offered).
>> >>
>> >> ## Impacts to transaction recycling
>> >> Depending on the capabilities of the covenant available (e.g.
>> >> restricting the number of inputs to the transaction) the transaction
>> >> spending the aggregated HTLC output can be made self sustained: the
>> >> spender will be able to claim what is theirs (preimage or timeout) and
>> >> send it to whatever output they want, or to fees. The remainder will
>> >> go back into a covenant restricted output with the leftover HTLCs.
>> >> Note that this most likely requires Eltoo in order to not enable fee
>> >> siphoning[7].
>> >>
>> >> ## Impacts to slot jamming
>> >> With the aggregated output being a reality, it changes the nature of
>> >> ?slot jamming? [1] significantly. While channel capacity must still be
>> >> reserved for in-flight HTLCs, one no longer needs to allocate a
>> >> commitment output for each up to some hardcoded limit.
>> >>
>> >> In today?s protocol this limit is 483, and I believe most
>> >> implementations default to an even lower limit. This leads to channel
>> >> jamming being quite inexpensive, as one can quickly fill a channel
>> >> with small HTLCs, without needing a significant amount of capital to
>> >> do so.
>> >>
>> >> The origins of the 483 slot limits is the worst case commitment size
>> >> before getting into unstandard territory [3]. With an aggregated
>> >> output this would no longer be the case, as adding HTLCs would no
>> >> longer affect commitment size. Instead, the full on-chain footprint of
>> >> an HTLC would be deferred until claim time.
>> >>
>> >> Does this mean one could lift, or even remove the limit for number of
>> >> active HTLCs? Unfortunately, the obvious approach doesn?t seem to get
>> >> rid of the problem entirely, but mitigates it quite a bit.
>> >>
>> >> ### Slot jamming attack scenario
>> >> Consider the scenario where an attacker sends a large number of
>> >> non-dust* HTLCs across a channel, and the channel parties enforce no
>> >> limit on the number of active HTLCs.
>> >>
>> >> The number of payments would not affect the size of the commitment
>> >> transaction at all, only the size of the witness that must be
>> >> presented when claiming or timing out the HTLCs. This means that there
>> >> is still a point at which chain fees get high enough for the HTLC to
>> >> be uneconomical to claim. This is no different than in today?s spec,
>> >> and such HTLCs will just be stranded on-chain until chain fees
>> >> decrease, at which point there is a race between the success and
>> >> timeout spends.
>> >>
>> >> There seems to be no way around this; if you want to claim an HTLC
>> >> on-chain, you need to put the preimage on-chain. And when the HTLC
>> >> first reaches you, you have no way of predicting the future chain fee.
>> >> With a large number of uneconomical HTLCs in play, the total BTC
>> >> exposure could still be very large, so you might want to limit this
>> >> somewhat.
>> >>
>> >> * Note that as long as the sum of HTLCs exceeds the dust limit, one
>> >> could manifest the output on the transaction.
>> >>
>> >> ## The good news
>> >> With an aggregated HTLC output, the number of HTLCs would no longer
>> >> impact the commitment transaction size while the channel is open and
>> >> operational.
>> >>
>> >> The marginal cost of claiming an HTLC with a preimage on-chain would
>> >> be much lower; no new inputs or outputs, only a linear increase in the
>> >> witness size. With a covenant primitive available, the extra footprint
>> >> of the timeout and success transactions would no longer exist.
>> >>
>> >> Claiming timed out HTLCs could still be made close to constant size
>> >> (no preimage to present), so no additional on-chain cost with more
>> >> HTLCs.
>> >>
>> >> ## The bad news
>> >> The most obvious problem is that we would need a new covenant
>> >> primitive on L1 (see below). However, I think it could be beneficial
>> >> to start exploring these ideas now in order to guide the L1 effort
>> >> towards something we could utilize to its fullest on L2.
>> >>
>> >> As mentioned, even with a functioning covenant, we don?t escape the
>> >> fact that a preimage needs to go on-chain, pricing out HTLCs at
>> >> certain fee rates. This is analogous to the dust exposure problem
>> >> discussed in [6], and makes some sort of limit still required.
>> >>
>> >> ### Open question
>> >> With PTLCs, could one create a compact proof showing that you know the
>> >> preimage for m-of-n of the satoshis in the output? (some sort of
>> >> threshold signature).
>> >>
>> >> If we could do this we would be able to remove the slot jamming issue
>> >> entirely; any number of active PTLCs would not change the on-chain
>> >> cost of claiming them.
>> >>
>> >> ## Covenant primitives
>> >> A recursive covenant is needed to achieve this. Something like OP_CTV
>> >> and OP_APO seems insufficient, since the number of ways the set of
>> >> HTLCs could be claimed would cause combinatorial blowup in the number
>> >> of possible spending transactions.
>> >>
>> >> Personally, I?ve found the simple yet powerful properties of
>> >> OP_CHECKCONTRACTVERIFY [4] together with OP_CAT and amount inspection
>> >> particularly interesting for the use case, but I?m certain many of the
>> >> other proposals could achieve the same thing. More direct inspection
>> >> like you get from a proposal like OP_TX[9] would also most likely have
>> >> the building blocks needed.
>> >>
>> >> ### Proof-of-concept
>> >> I?ve implemented a rough demo** of spending an HTLC output that pays
>> >> to a script with OP_CHECKCONTRACTVERIFY to achieve this [5]. The idea
>> >> is to commit to all active HTLCs in a merkle tree, and have the
>> >> spender provide merkle proofs for the HTLCs to claim, claiming the sum
>> >> into a new output. The remainder goes back into a new output with the
>> >> claimed HTLCs removed from the merkle tree.
>> >>
>> >> An interesting trick one can do when creating the merkle tree, is
>> >> sorting the HTLCs by expiry. This means that one in the timeout case
>> >> claim a subtree of HTLCs using a single merkle proof (and RBF this
>> >> batched timeout claim as more and more HTLCs expire) reducing the
>> >> timeout case to constant size witness (or rather logarithmic in the
>> >> total number of HTLCs).
>> >>
>> >> **Consider it an experiment, as it is missing a lot before it could be
>> >> usable in any real commitment setting.
>> >>
>> >>
>> >> [1] https://bitcoinops.org/en/topics/channel-jamming-attacks/#htlc-jamming-attack
>> >> [2] https://github.com/lightning/bolts/issues/845
>> >> [3] https://github.com/lightning/bolts/blob/aad959a297ff66946effb165518143be15777dd6/02-peer-protocol.md#rationale-7
>> >> [4] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021182.html
>> >> [5] https://github.com/halseth/tapsim/blob/b07f29804cf32dce0168ab5bb40558cbb18f2e76/examples/matt/claimpool/script.txt
>> >> [6] https://lists.linuxfoundation.org/pipermail/lightning-dev/2021-October/003257.html
>> >> [7] https://github.com/lightning/bolts/issues/845#issuecomment-937736734
>> >> [8] https://github.com/lightning/bolts/blob/8a64c6a1cef979b3f0cecb00ba7a48c2d28b3588/03-transactions.md?plain=1#L333
>> >> [9] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020450.html
>> >> _______________________________________________
>> >> bitcoin-dev mailing list
>> >> bitcoin-dev@lists.linuxfoundation.org
>> >> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 21
********************************************

