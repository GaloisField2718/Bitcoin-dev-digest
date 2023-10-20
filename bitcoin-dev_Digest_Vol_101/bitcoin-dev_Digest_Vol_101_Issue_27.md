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

   1. Announcing My PhD Thesis: "Evolving Bitcoin Custody"
      (Jacob Swambo)
   2. Examining ScriptPubkeys in Bitcoin Script (Rusty Russell)
   3. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Thu, 19 Oct 2023 20:23:07 +0000
From: Jacob Swambo <jacob.swambo@kcl.ac.uk>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Announcing My PhD Thesis: "Evolving Bitcoin
	Custody"
Message-ID:
	<VI1PR03MB510397F78CFF34747DFDDC5DCCD4A@VI1PR03MB5103.eurprd03.prod.outlook.com>
	
Content-Type: text/plain; charset="iso-8859-1"

Hello Bitcoin Community,

I'm thrilled to share with you my PhD thesis titled "Evolving Bitcoin Custody," a deep-dive into the design and analysis of Bitcoin custody systems, exploring their evolution in the face of a constantly changing technological and threat landscape.

You can access the full thesis on ArXiv here: https://arxiv.org/abs/2310.11911

Your feedback and questions are not only welcomed but immensely appreciated. I'm looking forward to discussion and am excited to see how your inputs will shape the future of custody systems and covenants.


Bitcoin Covenants:


In my research, I've given particular attention to deleted-key covenants, aiming to harness what's feasible with the current state of Bitcoin. As we venture deeper into the realm of covenants, I advocate for a similar depth and rigor, if not more, for other covenant proposals that necessitate soft-forks. By adopting systematic specifications coupled with meticulous analysis, we're better positioned to identify and rectify potential pitfalls, thereby safeguarding users from undue risks.


A pressing concern I've identified pertains to coin-control challenges and the subsequent user experience hurdles they present. My observations suggest that addressing these effectively might necessitate more granular covenants, akin to the INSPECT_X implemented in the Liquid sidechain.

Ajolote Custody System:

The Ajolote custody system proposed is theoretical, serving as a case study illustrating how vault covenants can operate within a complete custody system design. It is not my expectation for it to be built but rather to be utilized as a conceptual framework for further discussions and developments in the field. In my opinion Ajolote as presented turned out to be too complicated for users, but I believe it's a useful case study that adds several insights to the ongoing debate on bitcoin covenants and vaults in particular. I hope in time we can use these ideas in realistic custody systems.

For Custody System Designers:

Custody system designers may find the approach to security analysis delineated in this thesis to be of notable value. The methodology employed not only addresses the multifaceted challenges faced by custody systems but also provides a structured framework for evaluating and enhancing them. I encourage designers to explore and possibly integrate this attack model and methodology into the security analysis of their respective systems, and I am open to discussions and collaborations in this domain.

Thank you for your time and consideration.

Best Regards,

Jacob G?ker Swambo
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231019/31c67868/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 20 Oct 2023 14:10:37 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: "Bitcoin Protocol Discussion"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <87v8b2vu4q.fsf@rustcorp.com.au>
Content-Type: text/plain

Hi all,

        I've done an exploration of what would be required (given
OP_TX/OP_TXHASH or equivalent way of pushing a scriptPubkey on the
stack) to usefully validate Taproot outputs in Bitcoin Script.  Such
functionality is required for usable vaults, at least.

        https://rusty.ozlabs.org/2023/10/20/examining-scriptpubkey-in-script.html

(If anyone wants to collaborate to produce a prototype, and debug my
surely-wrong script examples, please ping me!)

TL;DR: if we have OP_TXHASH/OP_TX, and add OP_MULTISHA256 (or OP_CAT),
OP_KEYADDTWEAK and OP_LESS (or OP_CONDSWAP), and soft-fork weaken the
OP_SUCCESSx rule (or pop-script-from-stack), we can prove a two-leaf
tapscript tree in about 110 bytes of Script.  This allows useful
spending constraints based on a template approach.

Thanks!
Rusty.


------------------------------

Message: 3
Date: Fri, 20 Oct 2023 07:56:34 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Cc: security@ariard.me
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID:
	<CALZpt+G-eLLShrJckLG1UMDQ9tMGzqP1pBsUpEZ+82e9wHZGYw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi,

After writing the mail reply on the economics of sequential malicious
replacement of honest HTLC-timeout, I did write one more test to verify the
behavior on core mempool, and it works as expected.

https://github.com/ariard/bitcoin/commit/30f5d5b270e4ff195e8dcb9ef6b7ddcc5f6a1bf2

Responsible disclosure process has followed the lines of hardware issues
affecting operating system, as documented for the Linux kernel, while
adapted to the bitcoin ecosystem:

https://docs.kernel.org/6.1/process/embargoed-hardware-issues.html

Effective now, I'm halting my involvement with the development of the
lightning network and its implementations, including coordinating the
handling of security issues at the protocol level (I informed some senior
lightning devs in that sense before).

Closed the very old issue which was affected to me at this purpose on the
bolt repository:

https://github.com/lightning/bolts/pull/772

I think this new class of replacement cycling attacks puts lightning in a
very perilous position, where only a sustainable fix can happen at the
base-layer, e.g adding a memory-intensive history of all-seen transactions
or some consensus upgrade. Deployed mitigations are worth something in face
of simple attacks, though I don't think they're stopping advanced attackers
as said in the first full disclosure mail.

Those types of changes are the ones necessitating the utmost transparency
and buy-in of the community as a whole, as we're altering the full-nodes
processing requirements or the security architecture of the decentralized
bitcoin ecosystem in its integrality.

On the other hand fully explaining why such changes would be warranted for
the sake of lightning and for designing them well, we might need to lay out
in complete state practical and critical attacks on a ~5 355 public BTC
ecosystem.

Hard dilemma.

There might be a lesson in terms of bitcoin protocol deployment, we might
have to get them right at first try. Little second chance to fix them in
flight.

I'll be silent on those issues on public mailing lists until the week of
the 30 oct. Enough material has been published and other experts are
available. Then I'll be back focusing more on bitcoin core.

Best,
Antoine

Le lun. 16 oct. 2023 ? 17:57, Antoine Riard <antoine.riard@gmail.com> a
?crit :

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
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/f717238e/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 27
********************************************
