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
      mempool are belong to us" (ziggie1984)


----------------------------------------------------------------------

Message: 1
Date: Tue, 17 Oct 2023 07:21:35 +0000
From: ziggie1984 <ziggie1984@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 /	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your	mempool are belong to us"
Message-ID:
	<eW4O0HQJ2cbrzZhXSlgeDRWuhgRHXcAxIQCHJiqPh1zUxr270xPvl_tb7C4DUauZy56HaCq6BqGN9p4k-bkqQmLb4EHzPgIxZIZGVPlqyF0=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

> ## Deployed LN mitigations
>
> Aggressive rebroadcasting: As the replacement cycling attacker benefits from the HTLC-timeout being usually broadcast by lightning nodes only once every block, or less the replacement cycling malicious transactions paid only equal the sum of the absolute fees paid by the HTLC, adjusted with the replacement penalty. Rebroadcasting randomly and multiple times before the next block increases the absolute fee cost for the attacker.
>
> Implemented and deployed by Eclair, Core-Lightning, LND and LDK .
>
> Local-mempool preimage monitoring: As the replacement cycling attacker in a simple setup broadcast the HTLC-preimage to all the network mempools, the honest lightning node is able to catch on the flight the unconfirmed HTLC-preimage, before its subsequent mempool replacement. The preimage can be extracted from the second-stage HTLC-preimage and used to fetch the off-chain inbound HTLC with a cooperative message or go on-chain with it to claim the accepted HTLC output.

Hi Antoine,

thanks for this detailed explanation. This class of pinning attacks sound not too unlikely especially if the attacker targets channels with high capacity and very loose channel policies (allowing the full htlc amount to be the channel capacity). Could you add more details about the attack you observed on mainnet ? How did you monitor the chain, are the some tools available I can run in parallel to my lightning software to record this kind of suspicious behaviour (which did you use)?
What's also worth mentioning here is that you do not really have to control 2 neighbouring nodes to target your victim. If you can cycle the attack on the tail side and delay the confirmation of the htlc-timeout covenant the peer at the front (incoming link) of the victim will force-close the channel and claim his timeout-path in the same way (canceling back the initial htlc amount to the attackers initial node).

Apart from that I think one can even introduce some kind of feebumping race between the victim and the attacker on the tail side of the attack making the attack even more costly. I think currently when lightning nodes see the preimage in the mempool (during the time where they already can spend the same output with the timeout-covenant) we are honest and just extract the preimage and don't try to race this tx output. So we maybe should start feebumping this output if we end up in this scenario? If we see the preimage and can also claim this output via the htlc-timeout path, we should aggressively fee-bump (racing this output) our htlc-output in addition to grabbing the preimage and claiming it on the incoming. This is only feasible with anchor channels where we can add fees to the htlc-covenant. This would make the attack more costly for a peer when he knows that we use fees up to 50% of the htlc value. When you cycle this 144 times you will be at a heavy loss trying to steal this ht
 lc.

I would add another mitigation to the list for node runners to restrict the amount and number of HTLCs for big channels to unknown peers. It quickly comes with a loss when the HTLCs the attacker tries to steal are small.

Kind regards,

ziggie

------- Original Message -------
On Monday, October 16th, 2023 at 18:57, Antoine Riard <antoine.riard@gmail.com> wrote:

> (cross-posting mempool issues identified are exposing lightning chan to loss of funds risks, other multi-party bitcoin apps might be affected)
>
> Hi,
>
> End of last year (December 2022), amid technical discussions on eltoo payment channels and incentives compatibility of the mempool anti-DoS rules, a new transaction-relay jamming attack affecting lightning channels was discovered.
>
> After careful analysis, it turns out this attack is practical and immediately exposed lightning routing hops carrying HTLC traffic to loss of funds security risks, both legacy and anchor output channels. A potential exploitation plausibly happening even without network mempools congestion.
>
> Mitigations have been designed, implemented and deployed by all major lightning implementations during the last months.
>
> Please find attached the release numbers, where the mitigations should be present:
> - LDK: v0.0.118 - CVE-2023 -40231
> - Eclair: v0.9.0 - CVE-2023-40232
> - LND: v.0.17.0-beta - CVE-2023-40233
> - Core-Lightning: v.23.08.01 - CVE-2023-40234
>
> While neither replacement cycling attacks have been observed or reported in the wild since the last ~10 months or experimented in real-world conditions on bitcoin mainet, functional test is available exercising the affected lightning channel against bitcoin core mempool (26.0 release cycle).
>
> It is understood that a simple replacement cycling attack does not demand privileged capabilities from an attacker (e.g no low-hashrate power) and only access to basic bitcoin and lightning software. Yet I still think executing such an attack successfully requests a fair amount of bitcoin technical know-how and decent preparation.
>
> From my understanding of those issues, it is yet to be determined if the mitigations deployed are robust enough in face of advanced replacement cycling attackers, especially ones able to combine different classes of transaction-relay jamming such as pinnings or vetted with more privileged capabilities.
>
> Please find a list of potential affected bitcoin applications in this full disclosure report using bitcoin script timelocks or multi-party transactions, albeit no immediate security risk exposure as severe as the ones affecting lightning has been identified. Only cursory review of non-lightning applications has been conducted so far.
>
> There is a paper published summarizing replacement cycling attacks on the lightning network:
> https://github.com/ariard/mempool-research/blob/2023-10-replacement-paper/replacement-cycling.pdf
>
> ## Problem
>
> A lightning node allows HTLCs forwarding (in bolt3's parlance accepted HTLC on incoming link and offered HTLC on outgoing link) should settle the outgoing state with either a success or timeout before the incoming state timelock becomes final and an asymmetric defavorable settlement might happen (cf "Flood & Loot: A Systematic Attack on The Lightning Network" section 2.3 for a classical exposition of this lightning security property).
>
> Failure to satisfy this settlement requirement exposes a forwarding hop to a loss of fund risk where the offered HTLC is spent by the outgoing link counterparty's HTLC-preimage and the accepted HTLC is spent by the incoming link counterparty's HTLC-timeout.
>
> The specification mandates the incoming HTLC expiration timelock to be spaced out by an interval of `cltv_expiry_delta` from the outgoing HTLC expiration timelock, this exact interval value being an implementation and node policy setting. As a minimal value, the specification recommends 34 blocks of interval. If the timelock expiration I of the inbound HTLC is equal to 100 from chain tip, the timelock expiration O of the outbound HTLC must be equal to 66 blocks from chain tip, giving a reasonable buffer of reaction to the lightning forwarding node.
>
> In the lack of cooperative off-chain settlement of the HTLC on the outgoing link negotiated with the counterparty (either `update_fulfill_htlc` or `update_fail_htlc`) when O is reached, the lightning node should broadcast its commitment transaction. Once the commitment is confirmed (if anchor and the 1 CSV encumbrance is present), the lightning node broadcasts and confirms its HTLC-timeout before I height is reached.
>
> Here enter a replacement cycling attack. A malicious channel counterparty can broadcast its HTLC-preimage transaction with a higher absolute fee and higher feerate than the honest HTLC-timeout of the victim lightning node and triggers a replacement. Both for legacy and anchor output channels, a HTLC-preimage on a counterparty commitment transaction is malleable, i.e additional inputs or outputs can be added. The HTLC-preimage spends an unconfirmed and unrelated to the channel parent transaction M and conflicts its child.
>
> As the HTLC-preimage spends an unconfirmed input that was already included in the unconfirmed and unrelated child transaction (rule 2), pays an absolute higher fee of at least the sum paid by the HTLC-timeout and child transaction (rule 3) and the HTLC-preimage feerate is greater than all directly conflicting transactions (rule 6), the replacement is accepted. The honest HTLC-timeout is evicted out of the mempool.
>
> In an ulterior move, the malicious counterparty can replace the parent transaction itself with another candidate N satisfying the replacement rules, triggering the eviction of the malicious HTLC-preimage from the mempool as it was a child of the parent T.
>
> There is no spending candidate of the offered HTLC output for the current block laying in network mempools.
>
> This replacement cycling tricks can be repeated for each rebroadcast attempt of the HTLC-timeout by the honest lightning node until expiration of the inbound HTLC timelock I. Once this height is reached a HTLC-timeout is broadcast by the counterparty's on the incoming link in collusion with the one on the outgoing link broadcasting its own HTLC-preimage.
>
> The honest Lightning node has been "double-spent" in its HTLC forwarding.
>
> As a notable factor impacting the success of the attack, a lightning node's honest HTLC-timeout might be included in the block template of the miner winning the block race and therefore realizes a spent of the offered output. In practice, a replacement cycling attack might over-connect to miners' mempools and public reachable nodes to succeed in a fast eviction of the HTLC-timeout by its HTLC-preimage. As this latter transaction can come with a better ancestor-score, it should be picked up on the flight by economically competitive miners.
>
> A functional test exercising a simple replacement cycling of a HTLC transaction on bitcoin core mempool is available:
> https://github.com/ariard/bitcoin/commits/2023-test-mempool
>
> ## Deployed LN mitigations
>
> Aggressive rebroadcasting: As the replacement cycling attacker benefits from the HTLC-timeout being usually broadcast by lightning nodes only once every block, or less the replacement cycling malicious transactions paid only equal the sum of the absolute fees paid by the HTLC, adjusted with the replacement penalty. Rebroadcasting randomly and multiple times before the next block increases the absolute fee cost for the attacker.
>
> Implemented and deployed by Eclair, Core-Lightning, LND and LDK .
>
> Local-mempool preimage monitoring: As the replacement cycling attacker in a simple setup broadcast the HTLC-preimage to all the network mempools, the honest lightning node is able to catch on the flight the unconfirmed HTLC-preimage, before its subsequent mempool replacement. The preimage can be extracted from the second-stage HTLC-preimage and used to fetch the off-chain inbound HTLC with a cooperative message or go on-chain with it to claim the accepted HTLC output.
>
> Implemented and deployed by Eclair and LND.
>
> CLTV Expiry Delta: With every jammed block comes an absolute fee cost paid by the attacker, a risk of the HTLC-preimage being detected or discovered by the honest lightning node, or the HTLC-timeout to slip in a winning block template. Bumping the default CLTV delta hardens the odds of success of a simple replacement cycling attack.
>
> Default setting: Eclair 144, Core-Lightning 34, LND 80 and LDK 72.
>
> ## Affected Bitcoin Protocols and Applications
>
> From my understanding the following list of Bitcoin protocols and applications could be affected by new denial-of-service vectors under some level of network mempools congestion. Neither tests or advanced review of specifications (when available) has been conducted for each of them:
> - on-chain DLCs
> - coinjoins
> - payjoins
> - wallets with time-sensitive paths
> - peerswap and submarine swaps
> - batch payouts
> - transaction "accelerators"
>
> Inviting their developers, maintainers and operators to investigate how replacement cycling attacks might disrupt their in-mempool chain of transactions, or fee-bumping flows at the shortest delay. Simple flows and non-multi-party transactions should not be affected to the best of my understanding.
>
> ## Open Problems: Package Malleability
>
> Pinning attacks have been known for years as a practical vector to compromise lightning channels funds safety, under different scenarios (cf. current bip331's motivation section). Mitigations at the mempool level have been designed, discussed and are under implementation by the community (ancestor package relay + nverrsion=3 policy). Ideally, they should constraint a pinning attacker to always attach a high feerate package (commitment + CPFP) to replace the honest package, or allow a honest lightning node to overbid a malicious pinning package and get its time-sensitive transaction optimistically included in the chain.
>
> Replacement cycling attack seem to offer a new way to neutralize the design goals of package relay and its companion nversion=3 policy, where an attacker package RBF a honest package out of the mempool to subsequently double-spend its own high-fee child with a transaction unrelated to the channel. As the remaining commitment transaction is pre-signed with a minimal relay fee, it can be evicted out of the mempool.
>
> A functional test exercising a simple replacement cycling of a lightning channel commitment transaction on top of the nversion=3 code branch is available:
> https://github.com/ariard/bitcoin/commits/2023-10-test-mempool-2
>
> ## Discovery
>
> In 2018, the issue of static fees for pre-signed lightning transactions is made more widely known, the carve-out exemption in mempool rules to mitigate in-mempool package limits pinning and the anchor output pattern are proposed.
>
> In 2019, bitcoin core 0.19 is released with carve-out support. Continued discussion of the anchor output pattern as a dynamic fee-bumping method.
>
> In 2020, draft of anchor output submitted to the bolts. Initial finding of economic pinning against lightning commitment and second-stage HTLC transactions. Subsequent discussions of a preimage-overlay network or package-relay as mitigations. Public call made to inquiry more on potential other transaction-relay jamming attacks affecting lightning.
>
> In 2021, initial work in bitcoin core 22.0 of package acceptance. Continued discussion of the pinning attacks and shortcomings of current mempool rules during community-wide online workshops. Later the year, in light of all issues for bitcoin second-layers, a proposal is made about killing the mempool.
>
> In 2022, bip proposed for package relay and new proposed v3 policy design proposed for a review and implementation. Mempoolfullrbf is supported in bitcoin core 24.0 and conceptual questions about alignment of mempool rules w.r.t miners incentives are investigated.
>
> Along this year 2022, eltoo lightning channels design are discussed, implemented and reviewed. In this context and after discussions on mempool anti-DoS rules, I discovered this new replacement cycling attack was affecting deployed lightning channels and immediately reported the finding to some bitcoin core developers and lightning maintainers.
>
> ## Timeline
>
> - 2022-12-16: Report of the finding to Suhas Daftuar, Anthony Towns, Greg Sanders and Gloria Zhao
> - 2022-12-16: Report to LN maintainers: Rusty Russell, Bastien Teinturier, Matt Corallo and Olaoluwa Osuntunkun
> - 2022-12-23: Sharing to Eugene Siegel (LND)
> - 2022-12-24: Sharing to James O'Beirne and Antoine Poinsot (non-lightning potential affected projects)
> - 2022-01-14: Sharing to Gleb Naumenko (miners incentives and cross-layers issuers) and initial proposal of an early public disclosure
> - 2022-01-19: Collection of analysis if other second-layers and multi-party applications affected. LN mitigations development starts.
> - 2023-05-04: Sharing to Wilmer Paulino (LDK)
> - 2023-06-20: LN mitigations implemented and progressively released. Week of the 16 october proposed for full disclosure.
> - 2023-08-10: CVEs assigned by MITRE
> - 2023-10-05: Pre-disclosure of LN CVEs numbers and replacement cycling attack existence to security@bitcoincore.org.
> - 2023-10-16: Full disclosure of CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 and replacement cycling attacks
>
> ## Conclusion
>
> Despite the line of mitigations adopted and deployed by current major lightning implementations, I believe replacement cycling attacks are still practical for advanced attackers. Beyond this new attack might come as a way to partially or completely defeat some of the pinning mitigations which have been working for years as a community.
>
> As of today, it is uncertain to me if lightning is not affected by a more severe long-term package malleability critical security issue under current consensus rules, and if any other time-sensitive multi-party protocol, designed or deployed isn't de facto affected too (loss of funds or denial of service).
>
> Assuming analysis on package malleability is correct, it is unclear to me if it can be corrected by changes in replacement / eviction rules or mempool chain of transactions processing strategy. Inviting my technical peers and the bitcoin community to look more on this issue, including to dissent. I'll be the first one pleased if I'm fundamentally wrong on those issues, or if any element has not been weighted with the adequate technical accuracy it deserves.
>
> Do not trust, verify. All mistakes and opinions are my own.
>
> Antoine
>
> "meet with Triumph and Disaster. And treat those two impostors just the same" - K.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231017/d67c5702/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 14
********************************************
