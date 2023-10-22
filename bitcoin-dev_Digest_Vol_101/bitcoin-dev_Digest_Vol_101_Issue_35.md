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

   1. On solving pinning, replacement cycling and mempool issues
      for bitcoin second-layers (Antoine Riard)
   2. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Nadav Ivgi)


----------------------------------------------------------------------

Message: 1
Date: Sun, 22 Oct 2023 03:27:37 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Cc: security@ariard.me
Subject: [bitcoin-dev] On solving pinning, replacement cycling and
	mempool issues for bitcoin second-layers
Message-ID:
	<CALZpt+HwmacQ9VFu+SfmKms363ZU1xYZe+9o8TsoemTVQLprLg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi,

I think if Gleb Naumenko and myself allocate our research time on this
issue, we should (hopefully) be able to come with a strong sustainable fix
to the lightning network, both systematically solving pinnings and
replacement cycling attacks (and maybe other mempools issues or things
related like massive force-closure beyond available blockspace can absorb
before pre-signed transactions timelocks expiration as mentioned in the
original paper).

I have not yet probed Gleb's mind on this, though we both studied those
cross-layer issues together as early as 2019 / 2020, and I think we have
built an intuitive understanding of the problem-space, with both practical
experience of bitcoin core and rust-lightning codebases and landmark
research in this area [0] [1]. If Gleb isn't too busy with Erlay in core,
I'm sure he'll be enthusiastic to contribute research time at his own pace
(and I might probe a bit of Elichai Turkel time to verify the maths of all
sustainable lightning fixes we might propose and the risks models). All
soft commitments and assuming the interest of the bitcoin community.

One good advantage of long-term sustainable fixes, it should
(optimistically yet to be demonstrated) lower the fee-bumping reserve value
and number of UTXOs lightning users (and maybe bandwidth) have to lock
continuously to use this worldwide 24 / 7 payment system.

Reopened the issue on coordinated security issues handling in the LN
ecosystem:
https://github.com/lightning/bolts/pull/772

While I'll stay focused on solving the above problems at the base-layer
where they're best solved, at least I'll stay around for a few months
making transitions with the younger generation of LN devs.

For transparency, I don't have any strong solution design yet at all,
neither code, conceptual draft or paper ready, and game-theory and nodes
network processing resources changes will have to be weighted very
carefully, all under the bitcoin open and responsible process we currently
have. Overall, this will take reasonable time (e.g package relay design
discussions have been started in 2018 and we're only now at the hard
implementation and review phase) to carry on forward.

Looking forward to hearing thoughts of the Bitcoin and Lightning
development protocols community.

[0]
https://lists.linuxfoundation.org/pipermail/lightning-dev/2020-February/002569.html
[1] https://arxiv.org/pdf/2006.01418.pdf

"They who face calamity without wincing, and who offer the most energetic
resistance, these, be they States or individuals, are the truest heroes". -
Thucydides.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231022/210ee728/attachment.html>

------------------------------

Message: 2
Date: Sun, 22 Oct 2023 07:49:19 +0300
From: Nadav Ivgi <nadav@shesek.info>
To: Antoine Riard <antoine.riard@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID:
	<CAGXD5f2S4-Om7pkaUR+H6OiiyZ2F_AEWsohu8uJMvR7_+wwQkw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Could this be addressed with an OP_CSV_ALLINPUTS, a covenant opcode that
requires *all* inputs to have a matching nSequence, and using `1
OP_CSV_ALLINPUTS` in the HTLC preimage branch?

This would prevent using unconfirmed outputs in the HTLC-preimage-spending
transaction entirely, which IIUC should protect it against the replacement
cycling attack.

(If desirable, this could alternatively be OP_CSV_OTHERINPUTS to allow the
HTLC output itself to be spent immediately via the preimage branch, and
only require that the other inputs added for fees are confirmed.)


On Mon, Oct 16, 2023 at 8:03?PM Antoine Riard via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> (cross-posting mempool issues identified are exposing lightning chan to
> loss of funds risks, other multi-party bitcoin apps might be affected)
>
> Hi,
>
> End of last year (December 2022), amid technical discussions on eltoo
> payment channels and incentives compatibility of the mempool anti-DoS
> rules, a new transaction-relay jamming attack affecting lightning channels
> was discovered.
>
> After careful analysis, it turns out this attack is practical and
> immediately exposed lightning routing hops carrying HTLC traffic to loss of
> funds security risks, both legacy and anchor output channels. A potential
> exploitation plausibly happening even without network mempools congestion.
>
> Mitigations have been designed, implemented and deployed by all major
> lightning implementations during the last months.
>
> Please find attached the release numbers, where the mitigations should be
> present:
> - LDK: v0.0.118 - CVE-2023 -40231
> - Eclair: v0.9.0 - CVE-2023-40232
> - LND: v.0.17.0-beta - CVE-2023-40233
> - Core-Lightning: v.23.08.01 - CVE-2023-40234
>
> While neither replacement cycling attacks have been observed or reported
> in the wild since the last ~10 months or experimented in real-world
> conditions on bitcoin mainet, functional test is available exercising the
> affected lightning channel against bitcoin core mempool (26.0 release
> cycle).
>
> It is understood that a simple replacement cycling attack does not demand
> privileged capabilities from an attacker (e.g no low-hashrate power) and
> only access to basic bitcoin and lightning software. Yet I still think
> executing such an attack successfully requests a fair amount of bitcoin
> technical know-how and decent preparation.
>
> From my understanding of those issues, it is yet to be determined if the
> mitigations deployed are robust enough in face of advanced replacement
> cycling attackers, especially ones able to combine different classes of
> transaction-relay jamming such as pinnings or vetted with more privileged
> capabilities.
>
> Please find a list of potential affected bitcoin applications in this full
> disclosure report using bitcoin script timelocks or multi-party
> transactions, albeit no immediate security risk exposure as severe as the
> ones affecting lightning has been identified. Only cursory review of
> non-lightning applications has been conducted so far.
>
> There is a paper published summarizing replacement cycling attacks on the
> lightning network:
>
> https://github.com/ariard/mempool-research/blob/2023-10-replacement-paper/replacement-cycling.pdf
>
>  ## Problem
>
> A lightning node allows HTLCs forwarding (in bolt3's parlance accepted
> HTLC on incoming link and offered HTLC on outgoing link) should settle the
> outgoing state with either a success or timeout before the incoming state
> timelock becomes final and an asymmetric defavorable settlement might
> happen (cf "Flood & Loot: A Systematic Attack on The Lightning Network"
> section 2.3 for a classical exposition of this lightning security property).
>
> Failure to satisfy this settlement requirement exposes a forwarding hop to
> a loss of fund risk where the offered HTLC is spent by the outgoing link
> counterparty's HTLC-preimage and the accepted HTLC is spent by the incoming
> link counterparty's HTLC-timeout.
>
> The specification mandates the incoming HTLC expiration timelock to be
> spaced out by an interval of `cltv_expiry_delta` from the outgoing HTLC
> expiration timelock, this exact interval value being an implementation and
> node policy setting. As a minimal value, the specification recommends 34
> blocks of interval. If the timelock expiration I of the inbound HTLC is
> equal to 100 from chain tip, the timelock expiration O of the outbound HTLC
> must be equal to 66 blocks from chain tip, giving a reasonable buffer of
> reaction to the lightning forwarding node.
>
> In the lack of cooperative off-chain settlement of the HTLC on the
> outgoing link negotiated with the counterparty (either
> `update_fulfill_htlc` or `update_fail_htlc`) when O is reached, the
> lightning node should broadcast its commitment transaction. Once the
> commitment is confirmed (if anchor and the 1 CSV encumbrance is present),
> the lightning node broadcasts and confirms its HTLC-timeout before I height
> is reached.
>
> Here enter a replacement cycling attack. A malicious channel counterparty
> can broadcast its HTLC-preimage transaction with a higher absolute fee and
> higher feerate than the honest HTLC-timeout of the victim lightning node
> and triggers a replacement. Both for legacy and anchor output channels, a
> HTLC-preimage on a counterparty commitment transaction is malleable, i.e
> additional inputs or outputs can be added. The HTLC-preimage spends an
> unconfirmed and unrelated to the channel parent transaction M and conflicts
> its child.
>
> As the HTLC-preimage spends an unconfirmed input that was already included
> in the unconfirmed and unrelated child transaction (rule 2), pays an
> absolute higher fee of at least the sum paid by the HTLC-timeout and child
> transaction (rule 3) and the HTLC-preimage feerate is greater than all
> directly conflicting transactions (rule 6), the replacement is accepted.
> The honest HTLC-timeout is evicted out of the mempool.
>
> In an ulterior move, the malicious counterparty can replace the parent
> transaction itself with another candidate N satisfying the replacement
> rules, triggering the eviction of the malicious HTLC-preimage from the
> mempool as it was a child of the parent T.
>
> There is no spending candidate of the offered HTLC output for the current
> block laying in network mempools.
>
> This replacement cycling tricks can be repeated for each rebroadcast
> attempt of the HTLC-timeout by the honest lightning node until expiration
> of the inbound HTLC timelock I. Once this height is reached a HTLC-timeout
> is broadcast by the counterparty's on the incoming link in collusion with
> the one on the outgoing link broadcasting its own HTLC-preimage.
>
> The honest Lightning node has been "double-spent" in its HTLC forwarding.
>
> As a notable factor impacting the success of the attack, a lightning
> node's honest HTLC-timeout might be included in the block template of the
> miner winning the block race and therefore realizes a spent of the offered
> output. In practice, a replacement cycling attack might over-connect to
> miners' mempools and public reachable nodes to succeed in a fast eviction
> of the HTLC-timeout by its HTLC-preimage. As this latter transaction can
> come with a better ancestor-score, it should be picked up on the flight by
> economically competitive miners.
>
> A functional test exercising a simple replacement cycling of a HTLC
> transaction on bitcoin core mempool is available:
> https://github.com/ariard/bitcoin/commits/2023-test-mempool
>
> ## Deployed LN mitigations
>
> Aggressive rebroadcasting: As the replacement cycling attacker benefits
> from the HTLC-timeout being usually broadcast by lightning nodes only once
> every block, or less the replacement cycling malicious transactions paid
> only equal the sum of the absolute fees paid by the HTLC, adjusted with the
> replacement penalty. Rebroadcasting randomly and multiple times before the
> next block increases the absolute fee cost for the attacker.
>
> Implemented and deployed by Eclair, Core-Lightning, LND and LDK .
>
> Local-mempool preimage monitoring: As the replacement cycling attacker in
> a simple setup broadcast the HTLC-preimage to all the network mempools, the
> honest lightning node is able to catch on the flight the unconfirmed
> HTLC-preimage, before its subsequent mempool replacement. The preimage can
> be extracted from the second-stage HTLC-preimage and used to fetch the
> off-chain inbound HTLC with a cooperative message or go on-chain with it to
> claim the accepted HTLC output.
>
> Implemented and deployed by Eclair and LND.
>
> CLTV Expiry Delta: With every jammed block comes an absolute fee cost paid
> by the attacker, a risk of the HTLC-preimage being detected or discovered
> by the honest lightning node, or the HTLC-timeout to slip in a winning
> block template. Bumping the default CLTV delta hardens the odds of success
> of a simple replacement cycling attack.
>
> Default setting: Eclair 144, Core-Lightning 34, LND 80 and LDK 72.
>
> ## Affected Bitcoin Protocols and Applications
>
> From my understanding the following list of Bitcoin protocols and
> applications could be affected by new denial-of-service vectors under some
> level of network mempools congestion. Neither tests or advanced review of
> specifications (when available) has been conducted for each of them:
> - on-chain DLCs
> - coinjoins
> - payjoins
> - wallets with time-sensitive paths
> - peerswap and submarine swaps
> - batch payouts
> - transaction "accelerators"
>
> Inviting their developers, maintainers and operators to investigate how
> replacement cycling attacks might disrupt their in-mempool chain of
> transactions, or fee-bumping flows at the shortest delay. Simple flows and
> non-multi-party transactions should not be affected to the best of my
> understanding.
>
> ## Open Problems: Package Malleability
>
> Pinning attacks have been known for years as a practical vector to
> compromise lightning channels funds safety, under different scenarios (cf.
> current bip331's motivation section). Mitigations at the mempool level have
> been designed, discussed and are under implementation by the community
> (ancestor package relay + nverrsion=3 policy). Ideally, they should
> constraint a pinning attacker to always attach a high feerate package
> (commitment + CPFP) to replace the honest package, or allow a honest
> lightning node to overbid a malicious pinning package and get its
> time-sensitive transaction optimistically included in the chain.
>
> Replacement cycling attack seem to offer a new way to neutralize the
> design goals of package relay and its companion nversion=3 policy, where an
> attacker package RBF a honest package out of the mempool to subsequently
> double-spend its own high-fee child with a transaction unrelated to the
> channel. As the remaining commitment transaction is pre-signed with a
> minimal relay fee, it can be evicted out of the mempool.
>
> A functional test exercising a simple replacement cycling of a lightning
> channel commitment transaction on top of the nversion=3 code branch is
> available:
> https://github.com/ariard/bitcoin/commits/2023-10-test-mempool-2
>
> ## Discovery
>
> In 2018, the issue of static fees for pre-signed lightning transactions is
> made more widely known, the carve-out exemption in mempool rules to
> mitigate in-mempool package limits pinning and the anchor output pattern
> are proposed.
>
> In 2019, bitcoin core 0.19 is released with carve-out support. Continued
> discussion of the anchor output pattern as a dynamic fee-bumping method.
>
> In 2020, draft of anchor output submitted to the bolts. Initial finding of
> economic pinning against lightning commitment and second-stage HTLC
> transactions. Subsequent discussions of a preimage-overlay network or
> package-relay as mitigations. Public call made to inquiry more on potential
> other transaction-relay jamming attacks affecting lightning.
>
> In 2021, initial work in bitcoin core 22.0 of package acceptance.
> Continued discussion of the pinning attacks and shortcomings of current
> mempool rules during community-wide online workshops. Later the year, in
> light of all issues for bitcoin second-layers, a proposal is made about
> killing the mempool.
>
> In 2022, bip proposed for package relay and new proposed v3 policy design
> proposed for a review and implementation. Mempoolfullrbf is supported in
> bitcoin core 24.0 and conceptual questions about alignment of mempool rules
> w.r.t miners incentives are investigated.
>
> Along this year 2022, eltoo lightning channels design are discussed,
> implemented and reviewed. In this context and after discussions on mempool
> anti-DoS rules, I discovered this new replacement cycling attack was
> affecting deployed lightning channels and immediately reported the finding
> to some bitcoin core developers and lightning maintainers.
>
> ## Timeline
>
> - 2022-12-16: Report of the finding to Suhas Daftuar, Anthony Towns, Greg
> Sanders and Gloria Zhao
> - 2022-12-16: Report to LN maintainers: Rusty Russell, Bastien Teinturier,
> Matt Corallo and Olaoluwa Osuntunkun
> - 2022-12-23: Sharing to Eugene Siegel (LND)
> - 2022-12-24: Sharing to James O'Beirne and Antoine Poinsot (non-lightning
> potential affected projects)
> - 2022-01-14: Sharing to Gleb Naumenko (miners incentives and cross-layers
> issuers) and initial proposal of an early public disclosure
> - 2022-01-19: Collection of analysis if other second-layers and
> multi-party applications affected. LN mitigations development starts.
> - 2023-05-04: Sharing to Wilmer Paulino (LDK)
> - 2023-06-20: LN mitigations implemented and progressively released. Week
> of the 16 october proposed for full disclosure.
> - 2023-08-10: CVEs assigned by MITRE
> - 2023-10-05: Pre-disclosure of LN CVEs numbers and replacement cycling
> attack existence to security@bitcoincore.org.
> - 2023-10-16: Full disclosure of CVE-2023-40231 / CVE-2023-40232 /
> CVE-2023-40233 / CVE-2023-40234 and replacement cycling attacks
>
> ## Conclusion
>
> Despite the line of mitigations adopted and deployed by current major
> lightning implementations, I believe replacement cycling attacks are still
> practical for advanced attackers. Beyond this new attack might come as a
> way to partially or completely defeat some of the pinning mitigations which
> have been working for years as a community.
>
> As of today, it is uncertain to me if lightning is not affected by a more
> severe long-term package malleability critical security issue under current
> consensus rules, and if any other time-sensitive multi-party protocol,
> designed or deployed isn't de facto affected too (loss of funds or denial
> of service).
>
> Assuming analysis on package malleability is correct, it is unclear to me
> if it can be corrected by changes in replacement / eviction rules or
> mempool chain of transactions processing strategy. Inviting my technical
> peers and the bitcoin community to look more on this issue, including to
> dissent. I'll be the first one pleased if I'm fundamentally wrong on those
> issues, or if any element has not been weighted with the adequate technical
> accuracy it deserves.
>
> Do not trust, verify. All mistakes and opinions are my own.
>
> Antoine
>
> "meet with Triumph and Disaster. And treat those two impostors just the
> same" - K.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231022/036c3cc1/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 35
********************************************
