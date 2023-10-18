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
   2. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Tue, 17 Oct 2023 19:34:52 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID:
	<CALZpt+Gu9JJUeJfdUm_eT66DEH=UY+z1vkD_jUNZZyTPaet_QA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Zeeman,

> At block height 100, `B` notices the `B->C` HTLC timelock is expired
without `C` having claimed it, so `B` forces the `B====C` channel onchain.
> However, onchain feerates have risen and the commitment transaction and
HTLC-timeout transaction do not confirm.

This is not that the HTLC-timeout does not confirm. It is replaced in
cycles by C's HTLC-preimage which is still valid after `B->C` HTLC timelock
has expired. And this HTLC-preimage is subsequently replaced itself.

See the test here:
https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf

> At block height 144, `B` is still not able to claim the `A->B` HTLC, so
`A` drops the `A====B` channel onchain.
> As the fees are up-to-date, this confirms immediately and `A` is able to
recover the HTLC funds.
> However, the feerates of the `B====C` pre-signed transactions remain at
the old, uncompetitive feerates.

This is correct that A tries to recover the HTLC funds on the `A===B`
channel.

However, there is no need to consider the fee rates nor mempool congestion
as the exploit lays on the replacement mechanism itself (in simple
scenario).

> At this point, `C` broadcasts an HTLC-success transaction with high
feerates that CPFPs the commitment tx.
> However, it replaces the HTLC-timeout transaction, which is at the old,
low feerate.
> `C` is thus able to get the value of the HTLC, but `B` is now no longer
able to use the knowledge of the preimage, as its own incoming HTLC was
already confirmed as claimed by `A`.

This is correct that `C` broadcasts an HTLC-success transaction at block
height 144.

However `C` broadcasts this high feerate transaction at _every block_
between blocks 100 and 144 to replace B's HTLC-timeout transaction.

> Let me also explain to non-Lightning experts why HTLC-timeout is
presigned in this case and why `B` cannot feebump it.

Note `B` can feebump the HTLC-timeout for anchor output channels thanks to
sighash_single | anyonecanpay on C's signature.

Le mar. 17 oct. 2023 ? 11:34, ZmnSCPxj <ZmnSCPxj@protonmail.com> a ?crit :

> Good morning Antoine et al.,
>
> Let me try to rephrase the core of the attack.
>
> There exists these nodes on the LN (letters `A`, `B`, and `C` are nodes,
> `==` are channels):
>
>     A ===== B ===== C
>
> `A` routes `A->B->C`.
>
> The timelocks, for example, could be:
>
>    A->B timeelock = 144
>    B->C timelock = 100
>
> The above satisfies the LN BOLT requirements, as long as `B` has a
> `cltv_expiry_delta` of 44 or lower.
>
> After `B` forwards the HTLC `B->C`, C suddenly goes offline, and all the
> signed transactions --- commitment transaction and HTLC-timeout
> transactions --- are "stuck" at the feerate at the time.
>
> At block height 100, `B` notices the `B->C` HTLC timelock is expired
> without `C` having claimed it, so `B` forces the `B====C` channel onchain.
> However, onchain feerates have risen and the commitment transaction and
> HTLC-timeout transaction do not confirm.
>
> In the mean time, `A` is still online with `B` and updates the onchain
> fees of the `A====B` channel pre-signed transactions (commitment tx and
> HTLC-timeout tx) to the latest.
>
> At block height 144, `B` is still not able to claim the `A->B` HTLC, so
> `A` drops the `A====B` channel onchain.
> As the fees are up-to-date, this confirms immediately and `A` is able to
> recover the HTLC funds.
> However, the feerates of the `B====C` pre-signed transactions remain at
> the old, uncompetitive feerates.
>
> At this point, `C` broadcasts an HTLC-success transaction with high
> feerates that CPFPs the commitment tx.
> However, it replaces the HTLC-timeout transaction, which is at the old,
> low feerate.
> `C` is thus able to get the value of the HTLC, but `B` is now no longer
> able to use the knowledge of the preimage, as its own incoming HTLC was
> already confirmed as claimed by `A`.
>
> Is the above restatement accurate?
>
> ----
>
> Let me also explain to non-Lightning experts why HTLC-timeout is presigned
> in this case and why `B` cannot feebump it.
>
> In the Poon-Dryja mechanism, the HTLCs are "infected" by the Poon-Dryja
> penalty case, and are not plain HTLCs.
>
> A plain HTLC offerred by `B` to `C` would look like this:
>
>     (B && OP_CLTV) || (C && OP_HASH160)
>
> However, on the commitment transaction held by `B`, it would be infected
> by the penalty case in this way:
>
>     (B && C && OP_CLTV) || (C && OP_HASH160) || (C && revocation)
>
> There are two changes:
>
> * The addition of a revocation branch `C && revocation`.
> * The branch claimable by `B` in the "plain" HTLC (`B && OP_CLTV`) also
> includes `C`.
>
> These are necessary in case `B` tries to cheat and this HTLC is on an old,
> revoked transaction.
> If the revoked transaction is *really* old, the `OP_CLTV` would already
> impose a timelock far in the past.
> This means that a plain `B && OP_CLTV` branch can be claimed by `B` if it
> retained this very old revoked transaction.
>
> To prevent that, `C` is added to the `B && OP_CLTV` branch.
> We also introduce an HTLC-timeout transaction, which spends the `B && C &&
> OP_CLTV` branch, and outputs to:
>
>     (B && OP_CSV) || (C && revocation)
>
> Thus, even if `B` held onto a very old revoked commitment transaction and
> attempts to spend the timelock branch (because the `OP_CLTV` is for an old
> blockheight), it still has to contend with a new output with a *relative*
> timelock.
>
> Unfortunately, this means that the HTLC-timeout transaction is pre-signed,
> and has a specific feerate.
> In order to change the feerate, both `B` and `C` have to agree to re-sign
> the HTLC-timeout transaction at the higher feerate.
>
> However, the HTLC-success transaction in this case spends the plain `(C &&
> OP_HASH160)` branch, which only involves `C`.
> This allows `C` to feebump the HTLC-success transaction arbitrarily even
> if `B` does not cooperate.
>
> While anchor outputs can be added to the HTLC-timeout transaction as well,
> `C` has a greater advantage here due to being able to RBF the HTLC-timeout
> out of the way (1 transaction), while `B` has to get both HTLC-timeout and
> a CPFP-RBF of the anchor output of the HTLC-timeout transaction (2
> transactions).
> `C` thus requires a smaller fee to achieve a particular feerate due to
> having to push a smaller number of bytes compared to `B`.
>
> Regards,
> ZmnSCPxj
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231017/e68491ea/attachment.html>

------------------------------

Message: 2
Date: Tue, 17 Oct 2023 19:47:59 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: ziggie1984 <ziggie1984@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID:
	<CALZpt+GBJYJiQJBrLBCOnCUMSD3bLuO_R-XL6_CddSoj3au=UQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> We have conducted one so far, multiple scenarios to look at.

_*none*_ so far. typo of mine - apologize english is not my native language.

We discussed conducting experiments pre-disclosure in an e-mail of the 11th
August 2023.

"If someone is down to setup a "black box" Lightning infra on mainet, I'm
game on to exercise the vulnerabilities and mitigations during the coming
months and revisit the disclosure date dependent on the learnings."

However as the number of Lightning worldwide experts who have level of
knowledge and understandings to take part to experiments is I think
restrained to people listed on the disclosure mails _and_ we had other
pendings non-disclosed security issues at the time like the ones revealed
"fake channel DoS vector" the 23th August 2023, we didn't conduct them.

Le mar. 17 oct. 2023 ? 18:47, Antoine Riard <antoine.riard@gmail.com> a
?crit :

> Hi Ziggie,
>
> > thanks for this detailed explanation. This class of pinning attacks
> sound not too unlikely especially if the attacker targets channels with
> high capacity and very loose channel policies (allowing the full htlc
> > amount to be the channel capacity). Could you add more details about the
> attack you observed on mainnet ? How did you monitor the chain, are the
> some tools available I can run in parallel to my
> > lightning software to record this kind of suspicious behaviour (which
> did you use)?
>
> Just to give a clarification no _such_ attack has been observed on
> mainnet, since I and other LN maintainers have been aware of this issue. If
> there is a confusion on the disclosure mail thanks to point to it, I'll
> correct it.
>
> We discussed privately to experiment a demo attack in restrained dev
> circles, like we have done in the past for some LN sec issues. We have
> conducted one so far, multiple scenarios to look at.
>
> I confirm the risk of exposure if an attacker targets channels with high
> capacity and loose channel policies. Note there is no way to configure the
> cap for the total value of outbound HTLC in-flight, which is the flow
> affected.
>
> If you would like to observe the existence of such an attack happening,
> look at your mempool logs and the amount of HTLC output being
> systematically conflicted out with the following sequence (HTLC-timeout -
> HTLC-preimage - HTLC-timeout - ...).
>
> As an observation note, this is not akin to a pinning attack, as there is
> no "honest" or "malicious" transaction pinned in network mempools. And it
> can happen without network mempools congestion.
>
> > What's also worth mentioning here is that you do not really have to
> control 2 neighbouring nodes to target your victim. If you can cycle the
> attack on the tail side and delay the confirmation of the htlc- timeout
> covenant the peer at the front (incoming link) of the victim will
> force-close the channel and claim his timeout-path in the same way
> (canceling back the initial htlc amount to the attackers initial node).
>
> I think this is a behavior worthy of testing.
>
> > Apart from that I think one can even introduce some kind of feebumping
> race between the victim and the attacker on the tail side of the attack
> making the attack even more costly. I think
> > currently when lightning nodes see the preimage in the mempool (during
> the time where they already can spend the same output with the
> timeout-covenant) we are honest and just extract
> > the preimage and don't try to race this tx output.
>
> Local-mempool preimage monitoring has been implemented by Eclair for years
> as a mitigation against old school pinning attacks on second-stage HTLC
> transactions.
>
> This mechanism has been implemented by LND in the last months, following
> the report of replacement cycling attacks. As of today this is not
> implemented by Core-Lightning or LDK.
>
> > So we maybe should start feebumping this output if we end up in this
> scenario? If we see the preimage and can also claim this output via the
> htlc-timeout path, we should aggressively fee-bump (racing this output) our
> htlc-output in addition to grabbing the preimage and claiming it on the
> incoming. This is only feasible with anchor channels where we can add fees
> to the htlc-covenant. This would make the attack more costly for a peer
> when he knows that we use fees up to 50% of the htlc value. When you cycle
> this 144 times you will be at a heavy loss trying to steal this htlc.
>
> This is the "defensive fee mitigation" proposed in the paper. Coming with
> some unknown.
>
> > I would add another mitigation to the list for node runners to restrict
> the amount and number of HTLCs  for big channels to unknown peers. It
> quickly comes with a loss when the HTLCs the attacker tries to steal are
> small.
>
> See the point above on the lack of way at the spec-level to negotiate cap
> on the total value of outbound HTLC in-flight.
>
> Le mar. 17 oct. 2023 ? 08:21, ziggie1984 <ziggie1984@protonmail.com> a
> ?crit :
>
>> ## Deployed LN mitigations
>>
>> Aggressive rebroadcasting: As the replacement cycling attacker benefits
>> from the HTLC-timeout being usually broadcast by lightning nodes only once
>> every block, or less the replacement cycling malicious transactions paid
>> only equal the sum of the absolute fees paid by the HTLC, adjusted with the
>> replacement penalty. Rebroadcasting randomly and multiple times before the
>> next block increases the absolute fee cost for the attacker.
>>
>> Implemented and deployed by Eclair, Core-Lightning, LND and LDK .
>>
>> Local-mempool preimage monitoring: As the replacement cycling attacker in
>> a simple setup broadcast the HTLC-preimage to all the network mempools, the
>> honest lightning node is able to catch on the flight the unconfirmed
>> HTLC-preimage, before its subsequent mempool replacement. The preimage can
>> be extracted from the second-stage HTLC-preimage and used to fetch the
>> off-chain inbound HTLC with a cooperative message or go on-chain with it to
>> claim the accepted HTLC output.
>>
>>
>> Hi Antoine,
>>
>> thanks for this detailed explanation. This class of pinning attacks sound
>> not too unlikely especially if the attacker targets channels with high
>> capacity and very loose channel policies (allowing the full htlc amount to
>> be the channel capacity). Could you add more details about the attack you
>> observed on mainnet ? How did you monitor the chain, are the some tools
>> available I can run in parallel to my lightning software to record this
>> kind of suspicious behaviour (which did you use)?
>> What's also worth mentioning here is that you do not really have to
>> control 2 neighbouring nodes to target your victim. If you can cycle the
>> attack on the tail side and delay the confirmation of the htlc-timeout
>> covenant the peer at the front (incoming link) of the victim will
>> force-close the channel and claim his timeout-path in the same way
>> (canceling back the initial htlc amount to the attackers initial node).
>>
>> Apart from that I think one can even introduce some kind of feebumping
>> race between the victim and the attacker on the tail side of the attack
>> making the attack even more costly. I think currently when lightning nodes
>> see the preimage in the mempool (during the time where they already can
>> spend the same output with the timeout-covenant) we are honest and just
>> extract the preimage and don't try to race this tx output. So we maybe
>> should start feebumping this output if we end up in this scenario? If we
>> see the preimage and can also claim this output via the htlc-timeout path,
>> we should aggressively fee-bump (racing this output) our htlc-output in
>> addition to grabbing the preimage and claiming it on the incoming. This is
>> only feasible with anchor channels where we can add fees to the
>> htlc-covenant. This would make the attack more costly for a peer when he
>> knows that we use fees up to 50% of the htlc value. When you cycle this 144
>> times you will be at a heavy loss trying to steal this htlc.
>>
>> I would add another mitigation to the list for node runners to restrict
>> the amount and number of HTLCs  for big channels to unknown peers. It
>> quickly comes with a loss when the HTLCs the attacker tries to steal are
>> small.
>>
>>
>> Kind regards,
>>
>> ziggie
>>
>>
>> ------- Original Message -------
>> On Monday, October 16th, 2023 at 18:57, Antoine Riard <
>> antoine.riard@gmail.com> wrote:
>>
>> (cross-posting mempool issues identified are exposing lightning chan to
>> loss of funds risks, other multi-party bitcoin apps might be affected)
>>
>> Hi,
>>
>> End of last year (December 2022), amid technical discussions on eltoo
>> payment channels and incentives compatibility of the mempool anti-DoS
>> rules, a new transaction-relay jamming attack affecting lightning channels
>> was discovered.
>>
>> After careful analysis, it turns out this attack is practical and
>> immediately exposed lightning routing hops carrying HTLC traffic to loss of
>> funds security risks, both legacy and anchor output channels. A potential
>> exploitation plausibly happening even without network mempools congestion.
>>
>> Mitigations have been designed, implemented and deployed by all major
>> lightning implementations during the last months.
>>
>> Please find attached the release numbers, where the mitigations should be
>> present:
>> - LDK: v0.0.118 - CVE-2023 -40231
>> - Eclair: v0.9.0 - CVE-2023-40232
>> - LND: v.0.17.0-beta - CVE-2023-40233
>> - Core-Lightning: v.23.08.01 - CVE-2023-40234
>>
>> While neither replacement cycling attacks have been observed or reported
>> in the wild since the last ~10 months or experimented in real-world
>> conditions on bitcoin mainet, functional test is available exercising the
>> affected lightning channel against bitcoin core mempool (26.0 release
>> cycle).
>>
>> It is understood that a simple replacement cycling attack does not demand
>> privileged capabilities from an attacker (e.g no low-hashrate power) and
>> only access to basic bitcoin and lightning software. Yet I still think
>> executing such an attack successfully requests a fair amount of bitcoin
>> technical know-how and decent preparation.
>>
>> From my understanding of those issues, it is yet to be determined if the
>> mitigations deployed are robust enough in face of advanced replacement
>> cycling attackers, especially ones able to combine different classes of
>> transaction-relay jamming such as pinnings or vetted with more privileged
>> capabilities.
>>
>> Please find a list of potential affected bitcoin applications in this
>> full disclosure report using bitcoin script timelocks or multi-party
>> transactions, albeit no immediate security risk exposure as severe as the
>> ones affecting lightning has been identified. Only cursory review of
>> non-lightning applications has been conducted so far.
>>
>> There is a paper published summarizing replacement cycling attacks on the
>> lightning network:
>>
>> https://github.com/ariard/mempool-research/blob/2023-10-replacement-paper/replacement-cycling.pdf
>>
>> ## Problem
>>
>> A lightning node allows HTLCs forwarding (in bolt3's parlance accepted
>> HTLC on incoming link and offered HTLC on outgoing link) should settle the
>> outgoing state with either a success or timeout before the incoming state
>> timelock becomes final and an asymmetric defavorable settlement might
>> happen (cf "Flood & Loot: A Systematic Attack on The Lightning Network"
>> section 2.3 for a classical exposition of this lightning security property).
>>
>> Failure to satisfy this settlement requirement exposes a forwarding hop
>> to a loss of fund risk where the offered HTLC is spent by the outgoing link
>> counterparty's HTLC-preimage and the accepted HTLC is spent by the incoming
>> link counterparty's HTLC-timeout.
>>
>> The specification mandates the incoming HTLC expiration timelock to be
>> spaced out by an interval of `cltv_expiry_delta` from the outgoing HTLC
>> expiration timelock, this exact interval value being an implementation and
>> node policy setting. As a minimal value, the specification recommends 34
>> blocks of interval. If the timelock expiration I of the inbound HTLC is
>> equal to 100 from chain tip, the timelock expiration O of the outbound HTLC
>> must be equal to 66 blocks from chain tip, giving a reasonable buffer of
>> reaction to the lightning forwarding node.
>>
>> In the lack of cooperative off-chain settlement of the HTLC on the
>> outgoing link negotiated with the counterparty (either
>> `update_fulfill_htlc` or `update_fail_htlc`) when O is reached, the
>> lightning node should broadcast its commitment transaction. Once the
>> commitment is confirmed (if anchor and the 1 CSV encumbrance is present),
>> the lightning node broadcasts and confirms its HTLC-timeout before I height
>> is reached.
>>
>> Here enter a replacement cycling attack. A malicious channel counterparty
>> can broadcast its HTLC-preimage transaction with a higher absolute fee and
>> higher feerate than the honest HTLC-timeout of the victim lightning node
>> and triggers a replacement. Both for legacy and anchor output channels, a
>> HTLC-preimage on a counterparty commitment transaction is malleable, i.e
>> additional inputs or outputs can be added. The HTLC-preimage spends an
>> unconfirmed and unrelated to the channel parent transaction M and conflicts
>> its child.
>>
>> As the HTLC-preimage spends an unconfirmed input that was already
>> included in the unconfirmed and unrelated child transaction (rule 2), pays
>> an absolute higher fee of at least the sum paid by the HTLC-timeout and
>> child transaction (rule 3) and the HTLC-preimage feerate is greater than
>> all directly conflicting transactions (rule 6), the replacement is
>> accepted. The honest HTLC-timeout is evicted out of the mempool.
>>
>> In an ulterior move, the malicious counterparty can replace the parent
>> transaction itself with another candidate N satisfying the replacement
>> rules, triggering the eviction of the malicious HTLC-preimage from the
>> mempool as it was a child of the parent T.
>>
>> There is no spending candidate of the offered HTLC output for the current
>> block laying in network mempools.
>>
>> This replacement cycling tricks can be repeated for each rebroadcast
>> attempt of the HTLC-timeout by the honest lightning node until expiration
>> of the inbound HTLC timelock I. Once this height is reached a HTLC-timeout
>> is broadcast by the counterparty's on the incoming link in collusion with
>> the one on the outgoing link broadcasting its own HTLC-preimage.
>>
>> The honest Lightning node has been "double-spent" in its HTLC forwarding.
>>
>> As a notable factor impacting the success of the attack, a lightning
>> node's honest HTLC-timeout might be included in the block template of the
>> miner winning the block race and therefore realizes a spent of the offered
>> output. In practice, a replacement cycling attack might over-connect to
>> miners' mempools and public reachable nodes to succeed in a fast eviction
>> of the HTLC-timeout by its HTLC-preimage. As this latter transaction can
>> come with a better ancestor-score, it should be picked up on the flight by
>> economically competitive miners.
>>
>> A functional test exercising a simple replacement cycling of a HTLC
>> transaction on bitcoin core mempool is available:
>> https://github.com/ariard/bitcoin/commits/2023-test-mempool
>>
>> ## Deployed LN mitigations
>>
>> Aggressive rebroadcasting: As the replacement cycling attacker benefits
>> from the HTLC-timeout being usually broadcast by lightning nodes only once
>> every block, or less the replacement cycling malicious transactions paid
>> only equal the sum of the absolute fees paid by the HTLC, adjusted with the
>> replacement penalty. Rebroadcasting randomly and multiple times before the
>> next block increases the absolute fee cost for the attacker.
>>
>> Implemented and deployed by Eclair, Core-Lightning, LND and LDK .
>>
>> Local-mempool preimage monitoring: As the replacement cycling attacker in
>> a simple setup broadcast the HTLC-preimage to all the network mempools, the
>> honest lightning node is able to catch on the flight the unconfirmed
>> HTLC-preimage, before its subsequent mempool replacement. The preimage can
>> be extracted from the second-stage HTLC-preimage and used to fetch the
>> off-chain inbound HTLC with a cooperative message or go on-chain with it to
>> claim the accepted HTLC output.
>>
>> Implemented and deployed by Eclair and LND.
>>
>> CLTV Expiry Delta: With every jammed block comes an absolute fee cost
>> paid by the attacker, a risk of the HTLC-preimage being detected or
>> discovered by the honest lightning node, or the HTLC-timeout to slip in a
>> winning block template. Bumping the default CLTV delta hardens the odds of
>> success of a simple replacement cycling attack.
>>
>> Default setting: Eclair 144, Core-Lightning 34, LND 80 and LDK 72.
>>
>> ## Affected Bitcoin Protocols and Applications
>>
>> From my understanding the following list of Bitcoin protocols and
>> applications could be affected by new denial-of-service vectors under some
>> level of network mempools congestion. Neither tests or advanced review of
>> specifications (when available) has been conducted for each of them:
>> - on-chain DLCs
>> - coinjoins
>> - payjoins
>> - wallets with time-sensitive paths
>> - peerswap and submarine swaps
>> - batch payouts
>> - transaction "accelerators"
>>
>> Inviting their developers, maintainers and operators to investigate how
>> replacement cycling attacks might disrupt their in-mempool chain of
>> transactions, or fee-bumping flows at the shortest delay. Simple flows and
>> non-multi-party transactions should not be affected to the best of my
>> understanding.
>>
>> ## Open Problems: Package Malleability
>>
>> Pinning attacks have been known for years as a practical vector to
>> compromise lightning channels funds safety, under different scenarios (cf.
>> current bip331's motivation section). Mitigations at the mempool level have
>> been designed, discussed and are under implementation by the community
>> (ancestor package relay + nverrsion=3 policy). Ideally, they should
>> constraint a pinning attacker to always attach a high feerate package
>> (commitment + CPFP) to replace the honest package, or allow a honest
>> lightning node to overbid a malicious pinning package and get its
>> time-sensitive transaction optimistically included in the chain.
>>
>> Replacement cycling attack seem to offer a new way to neutralize the
>> design goals of package relay and its companion nversion=3 policy, where an
>> attacker package RBF a honest package out of the mempool to subsequently
>> double-spend its own high-fee child with a transaction unrelated to the
>> channel. As the remaining commitment transaction is pre-signed with a
>> minimal relay fee, it can be evicted out of the mempool.
>>
>> A functional test exercising a simple replacement cycling of a lightning
>> channel commitment transaction on top of the nversion=3 code branch is
>> available:
>> https://github.com/ariard/bitcoin/commits/2023-10-test-mempool-2
>>
>> ## Discovery
>>
>> In 2018, the issue of static fees for pre-signed lightning transactions
>> is made more widely known, the carve-out exemption in mempool rules to
>> mitigate in-mempool package limits pinning and the anchor output pattern
>> are proposed.
>>
>> In 2019, bitcoin core 0.19 is released with carve-out support. Continued
>> discussion of the anchor output pattern as a dynamic fee-bumping method.
>>
>> In 2020, draft of anchor output submitted to the bolts. Initial finding
>> of economic pinning against lightning commitment and second-stage HTLC
>> transactions. Subsequent discussions of a preimage-overlay network or
>> package-relay as mitigations. Public call made to inquiry more on potential
>> other transaction-relay jamming attacks affecting lightning.
>>
>> In 2021, initial work in bitcoin core 22.0 of package acceptance.
>> Continued discussion of the pinning attacks and shortcomings of current
>> mempool rules during community-wide online workshops. Later the year, in
>> light of all issues for bitcoin second-layers, a proposal is made about
>> killing the mempool.
>>
>> In 2022, bip proposed for package relay and new proposed v3 policy design
>> proposed for a review and implementation. Mempoolfullrbf is supported in
>> bitcoin core 24.0 and conceptual questions about alignment of mempool rules
>> w.r.t miners incentives are investigated.
>>
>> Along this year 2022, eltoo lightning channels design are discussed,
>> implemented and reviewed. In this context and after discussions on mempool
>> anti-DoS rules, I discovered this new replacement cycling attack was
>> affecting deployed lightning channels and immediately reported the finding
>> to some bitcoin core developers and lightning maintainers.
>>
>> ## Timeline
>>
>> - 2022-12-16: Report of the finding to Suhas Daftuar, Anthony Towns, Greg
>> Sanders and Gloria Zhao
>> - 2022-12-16: Report to LN maintainers: Rusty Russell, Bastien
>> Teinturier, Matt Corallo and Olaoluwa Osuntunkun
>> - 2022-12-23: Sharing to Eugene Siegel (LND)
>> - 2022-12-24: Sharing to James O'Beirne and Antoine Poinsot
>> (non-lightning potential affected projects)
>> - 2022-01-14: Sharing to Gleb Naumenko (miners incentives and
>> cross-layers issuers) and initial proposal of an early public disclosure
>> - 2022-01-19: Collection of analysis if other second-layers and
>> multi-party applications affected. LN mitigations development starts.
>> - 2023-05-04: Sharing to Wilmer Paulino (LDK)
>> - 2023-06-20: LN mitigations implemented and progressively released. Week
>> of the 16 october proposed for full disclosure.
>> - 2023-08-10: CVEs assigned by MITRE
>> - 2023-10-05: Pre-disclosure of LN CVEs numbers and replacement cycling
>> attack existence to security@bitcoincore.org.
>> - 2023-10-16: Full disclosure of CVE-2023-40231 / CVE-2023-40232 /
>> CVE-2023-40233 / CVE-2023-40234 and replacement cycling attacks
>>
>> ## Conclusion
>>
>> Despite the line of mitigations adopted and deployed by current major
>> lightning implementations, I believe replacement cycling attacks are still
>> practical for advanced attackers. Beyond this new attack might come as a
>> way to partially or completely defeat some of the pinning mitigations which
>> have been working for years as a community.
>>
>> As of today, it is uncertain to me if lightning is not affected by a more
>> severe long-term package malleability critical security issue under current
>> consensus rules, and if any other time-sensitive multi-party protocol,
>> designed or deployed isn't de facto affected too (loss of funds or denial
>> of service).
>>
>> Assuming analysis on package malleability is correct, it is unclear to me
>> if it can be corrected by changes in replacement / eviction rules or
>> mempool chain of transactions processing strategy. Inviting my technical
>> peers and the bitcoin community to look more on this issue, including to
>> dissent. I'll be the first one pleased if I'm fundamentally wrong on those
>> issues, or if any element has not been weighted with the adequate technical
>> accuracy it deserves.
>>
>> Do not trust, verify. All mistakes and opinions are my own.
>>
>> Antoine
>>
>> "meet with Triumph and Disaster. And treat those two impostors just the
>> same" - K.
>>
>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231017/36ea4307/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 17
********************************************
