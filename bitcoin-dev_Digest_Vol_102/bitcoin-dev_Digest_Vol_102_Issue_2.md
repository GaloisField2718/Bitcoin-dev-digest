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

   1. Re: Examining ScriptPubkeys in Bitcoin Script (Rusty Russell)
   2. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Peter Todd)
   3. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Tue, 31 Oct 2023 12:54:27 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: James O'Beirne <james.obeirne@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <87v8anr0kk.fsf@rustcorp.com.au>
Content-Type: text/plain; charset=utf-8

"James O'Beirne" <james.obeirne@gmail.com> writes:
> On Sat, Oct 28, 2023 at 12:51?AM Rusty Russell via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> But AFAICT there are multiple perfectly reasonable variants of vaults,
>> too.  One would be:
>>
>> 1. master key can do anything
>> 2. OR normal key can send back to vault addr without delay
>> 3. OR normal key can do anything else after a delay.
>>
>> Another would be:
>> 1. normal key can send to P2WPKH(master)
>> 2. OR normal key can send to P2WPKH(normal key) after a delay.
>>
>
> I'm confused by what you mean here. I'm pretty sure that BIP-345 VAULT
> handles the cases that you're outlining, though I don't understand your
> terminology -- "master" vs. "normal", and why we are caring about P2WPKH
> vs. anything else. Using the OP_VAULT* codes can be done in an arbitrary
> arrangement of tapleaves, facilitating any number of vaultish spending
> conditions, alongside other non-VAULT leaves.

I was thinking from a user POV: the "master" key is the one they keep
super safe in case of emergencies, the "normal" is the delayed spend
key.

OP_VAULT certainly can encapsulate this, but I have yet to do the kind
of thorough review that I'd need to evaluate the various design
decisions.

> Well, I found the vault BIP really hard to understand.  I think it wants
>> to be a new address format, not script opcodes.
>>
>
> Again confused here. This is like saying "CHECKLOCKTIMEVERIFY wants to be a
> new address format, not a script opcode."

I mean in an ideal world, Bitcoin Script would be powerful enough to
implement vaults, and once a popular use pattern emerged we'd introduce
a new address type, defined to expand to that template.  Like P2WPK or
P2PKH.

Sadly, we're not in that world!  BIP 345 introduces a number of separate
mechanisms, such as limited script delegation, iteration and amount
arithmetic which are not expressible in Script (ok, amount arithmetic
kind of is, but ick!).

To form a real opinion, I need to consider all these elements, and
whether they should exist inside OP_VAULT, or as separate things.
That's a slow process, sorry :(

> That said, I'm sure some VAULT patterns could be abstracted into the
> miniscript/descriptor layer to good effect.

That would be very interesting, but hard.  Volunteers? :)

Cheers,
Rusty.


------------------------------

Message: 2
Date: Thu, 2 Nov 2023 06:26:38 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZUNBHsw2BldPLvPc@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Thu, Nov 02, 2023 at 05:24:36AM +0000, Antoine Riard wrote:
> Hi Peter,
> 
> > So, why can't we make the HTLC-preimage path expire? Traditionally, we've
> tried
> > to ensure that transactions - once valid - remain valid forever. We do
> this
> > because we don't want transactions to become impossible to mine in the
> event of
> > a large reorganization.
> 
> I don't know if reverse time-lock where a lightning spending path becomes
> invalid after a block height or epoch point solves the more advanced
> replacement cycling attacks, where a malicious commitment transaction
> itself replaces out a honest commitment transaction, and the
> child-pay-for-parent of this malicious transaction is itself replaced out
> by the attacker, leading to the automatic trimming of the malicious
> commitment transaction.

To be clear, are you talking about anchor channels or non-anchor channels?
Because in anchor channels, all outputs other than the anchor outputs provided
for fee bumping can't be spent until the commitment transaction is mined, which
means RBF/CPFP isn't relevant.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231102/8a456ef3/attachment-0001.sig>

------------------------------

Message: 3
Date: Thu, 2 Nov 2023 04:46:29 +0000
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
	<CALZpt+EOQEttscM4ncKiUG810DQkzgjFwp6noLh68tSsnHPATw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi list,

As I received a lot of feedback on the full disclosure of the 16th week of
October and the following posts, some accurate, I'm taking time to address
a few of them.

I think one of the most recurring feedback is the fact that the replacement
cycling issue laid out in the initial full disclosure post could have been
better explained or presented. Here you have a typical disclosure dilemma
encountered by any security researcher, on one hand you wish to explain
them as best you can to enlighten the public audience, on the other hand if
you come up with a full exploitation rootkit, its manual and a paper with a
lot of graphic informing on all the way to exploit, you might expose the
public audience funds.

As a reminder, at the time of the full disclosure the 16th, some lightning
implementations were still adding up mitigations in their codebase and
corresponding release has only been tagged last week. Moreover, I think
when you're doing a full disclosure as a security researcher, it is wiser
to be conservative in the flow of information disclosed, as you might have
missed some observations or insights worsening the severity and
practicality of exploitation.

In my reasonable and modest experience, the amount and clarity of
information you're revealing in matters of security disclosure is an art
rhythmed by contingencies, not a science.

Additionally, there is one "unusual" security risk only affecting Bitcoin
second-layers, namely triggering winds of panic among lightning node
operators. This group of users started to manually force-close channels and
holistically congestion network mempools, opening the door to opportunistic
"flood & loot" exploitation, a risk known by lightning experts for years.

E.g bare option anchor commitment transactions are 900 WU (bolt3), max
block size is 4_000_000 WU, if you have half of the 80k of _public_
channels, you might have a hour and half of full blocks, which might offer
the opportunity of stealing payments from payee, based on historical
timelocks.

This last risk is based on experience from previous security coordination
work and I did inform the core security list of this concern in date of the
5 october: " if we see an abnormal rate of network mempools congestion from
LN node operators manually force-closing their channels with low-trusted
peers, this phenomena has already happened during past Lightning security
issues disclosures" as it could have provoked disruptions ecosystem-wide
beyond lightning.

There have been some voices speaking up on the sudden announcement from my
side to step down from lightning development. While there has been complete
distorsion of my statement by non-specialized journalists and I've been the
first one to complain, howev er it was very deliberate on my side to ring
the bell on the very poor state of lightning security and marked the score
than this new replacement cycling issue is a far more concerning than other
major security risks of lightning known so far. As a friendly reminder, we
start to pile up a very serious stack of security risks: pinnings, channel
jamming, replacement cycling, time dilation (all those ones could kill
lightning if exploited at scale - period) and more minor ones such as dust
HTLC exposure, fee or liquidity griefing and other denial-of-service.

Hard things about hard things, every new major security risk discovered
somehow constrains lightning developers to go back on the whiteboard and
check that any mitigation in development for each risk is not broken or the
security properties with. Most of the time, we might think in isolation to
ease the mitigation of research and development work. Astute adversaries
might not give us those flowers. At the end, technical reality advises that
lightning security issues are better solved at the base-layer, and this is
where expert time is cruelly missing to make lightning more robust on the
very long-term.

On a more ethical plan, there is no wish on my side to stay accountable on
the coordinated handling of security issues in the lightning ecosystem,
when I have the inner conviction than replacement cycling issues are
practical and critical, that they cannot be solved correctly on the
lightning-side, that any serious mitigation on the base-layer might take
numerous years and their integration back in the lightning-side might take
another couple of years. Once again, I warned the whole community of the
nest of issues at the mempool-level for lightning very consistently during
the past years.

With humility, if those replacement cycling attacks start to be played out
at scale by sophisticated attackers during the coming future, I'm not
competent to improvise an effective mitigation. And even less competent to
coordinate dissemination of such eventual patch of mitigations across an
ecosystem of nodes, without losing inter-compatibility between
implementations, wallets and releases versions (and here the lack of
standardized mechanism like dynamic upgrade bolt pr #1090 is a missing
safety feature).

Security of critical software systems is somehow akin to medical practice.
If you wish to nurture an adequate clinical treatment, you have to get the
diagnosis of the illness severity first, even if it's a painful truth for
the patient. In my opinion, here the patient is the community of lightning
node operators and lightning users, and if we wish for an adequate
technical treatment to overcome the vulnerability severity, building
consensus on the severity sounds a necessary step.

As of today, I think the criticality of this replacement cycling attack is
still misappreciated by other bitcoin devs, including lightning experts. I
have not seen so far discussion of the issue entitled "package
malleability" and the corresponding test on bitcoin core mempool, adapting
the replacement cycling scenario to a post-package relay world. If I'm
correct here though welcoming more expert eyes with pleasure here, dynamic
fee-bumping of pre-signed lightning states as we have been working from
years can be broken by replacement cycling attacks, extending the types of
lightning nodes at risk from forwarding nodes to just any lightning node
(and in the lack of dynamic fee-bumping pre-signed states might not
propagate to miners template due to the dynamic mempool min fee).

Finally, running a piece of software is a matter of an individual or
business decision. While one can as a technical "domain expert" explain the
risk model with the utmost care and diligence, at the end of the day the
decision belongs to everyone on what to do with their own computing
infrastructure and stack of satoshis. Yet if you're servicing customers or
users with your infrastructure, please be mindful of the safety of their
funds and take time to understand how your technical decisions might affect
them. Their risk tolerance is very likely not yours [0].

All that said, after months of working on those issues under embargo, I
find it pleasant to see the bitcoin technical community and beyond actually
talking about those issues at length with a "don't trust, verify" mindset.
I'll take time to answer the public mails on those subjects during the
coming weeks and months. I'm still enthusiastic to do a real-world
demonstration of a replacement cycling attack on mainnet though I won't
have time until the second semester of 2024 at the very best (I'm still
late on my announcement of 2020 to do a real-world demonstration of pinning
attacks - I'm learning to be very conservative with my public open-source
commitment now). Assuming a timeline of a decade or two, I'm still
optimistic on seeing one day a lightning ecosystem looking like the p2p
cypherpunk version as fleshed out in the original paper.

Cheers,
Antoine

[0] "Chancellor on the brink of second bailout of banks" - I think the 2008
crisis and its massive bailout of big financial players by the small guy
money worldwide is a good meditation. Hopefully, we're not building a new
financial system where the big bitcoin and lightning players are concealing
massive security risks from the average end-user, and in the occurrence of
the risks flagrant realization will deny any form of accountability by
walls of PR statements.

Le sam. 21 oct. 2023 ? 21:05, Antoine Riard <antoine.riard@gmail.com> a
?crit :

> Hi,
>
> As I've been shown offline Twitter posts misrepresenting my previous mail,
> I think it's good to correct them. The security flaws are not "intentional
> backdoor" or whatever misrepresentation that would question the competence
> and know-how of the Bitcoin and Lightning development community.
>
> The replacement cycling issue discovered has been known by a small circle
> of Bitcoin developers since December 2022. As it appears to some experts
> and it has been commented publicly, changes at the bitcoin base-layer might
> be the most substantial fixes. Those changes take time and here this is
> akin to how the linux kernel, bsds and OS vendors are working [0].
>
> All I can say is that we had recently had internal discussion on how to
> improve coordinated security fixes and patching processes for the coming
> decades. This is an area of concern where I've always been at the forefront
> as early as 2020 / 2021 [1].
>
> In the meanwhile, lightning experts have already deployed mitigations
> which are hardening the lightning ecosystem significantly in face of simple
> or medium attacks. More advanced attacks can only be mounted if you have
> sufficient p2p and mempool knowledge as was pointed out by other bitcoin
> experts like Matt or Peter (which take years to acquire for average bitcoin
> developers) and the months of preparation to attempt them.
>
> If you're a journalist reporting on the information in mainstream crypto
> publications, I'll suggest waiting to do so before expert reporters of
> bitcoin circles who have more in-field knowledge can do so and qualify the
> technical situation with more distance. As I've already been interviewed by
> top financial publication years ago for my work on bitcoin, as a journalist
> you're engaging your own reputation on the information you're reporting.
> Thanks for being responsible here.
>
> This is the nature of the electronic communication and contemporaneous
> media that information is extremely fluid and there is no native anti-DoS
> mechanism to slow down the propagation of sensitive information where
> mitigations are still in deployment. A reason I'm not on social media of
> any kind [2]. In the meanwhile, it's good to go to read senecca and marcus
> aurelius take the situation with stoicism and with a zelt of meditation [3].
>
> All my previous statements are mostly technically correct (even if some
> could have been written with more clarity once again I'm not an english
> native [4]). While I wish to wait the week of the 30th Oct o discuss
> further what is best fix and what are the trade-offs as a community as a
> wide (give time some laggard lightning implementations ship fixes), though
> I'll comment further on the mailing list if the flow of information on
> "social media" is DoSing the ability of the bitcoin community to work on
> the long-term appropriate fixes in a responsible and constructive fashion.
>
> [0] See meltdown class of vulnerability and how operating systems are
> handling hardware-sourced vulnerabilities
> https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability). Most of
> the time they do their best on the software side and they go to see with
> hardware vendors how to do the necessary updates.
>
> [1]
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2021-April/003002.html
>
> [2] And for the wider analysis on contemporaneous culture of information
> propagation and network effect, I can only recommend to read venkatesh
> rao's ribbonfarm essays http://ribbonfarm.com
>
> [3] There are very good reasons why some executives at top modern
> technology companies are doing meditation daily, some even hours. "mind
> illuminated" is a good read.
>
> [4] While my former employer, Chaincode Labs, paid for my english lessons
> back in 2020. Generally it was a good insight from them to train people on
> how to communicate in a crisis.
>
>
> Le ven. 20 oct. 2023 ? 07:56, Antoine Riard <antoine.riard@gmail.com> a
> ?crit :
>
>> Hi,
>>
>> After writing the mail reply on the economics of sequential malicious
>> replacement of honest HTLC-timeout, I did write one more test to verify the
>> behavior on core mempool, and it works as expected.
>>
>>
>> https://github.com/ariard/bitcoin/commit/30f5d5b270e4ff195e8dcb9ef6b7ddcc5f6a1bf2
>>
>> Responsible disclosure process has followed the lines of hardware issues
>> affecting operating system, as documented for the Linux kernel, while
>> adapted to the bitcoin ecosystem:
>>
>> https://docs.kernel.org/6.1/process/embargoed-hardware-issues.html
>>
>> Effective now, I'm halting my involvement with the development of the
>> lightning network and its implementations, including coordinating the
>> handling of security issues at the protocol level (I informed some senior
>> lightning devs in that sense before).
>>
>> Closed the very old issue which was affected to me at this purpose on the
>> bolt repository:
>>
>> https://github.com/lightning/bolts/pull/772
>>
>> I think this new class of replacement cycling attacks puts lightning in a
>> very perilous position, where only a sustainable fix can happen at the
>> base-layer, e.g adding a memory-intensive history of all-seen transactions
>> or some consensus upgrade. Deployed mitigations are worth something in face
>> of simple attacks, though I don't think they're stopping advanced attackers
>> as said in the first full disclosure mail.
>>
>> Those types of changes are the ones necessitating the utmost transparency
>> and buy-in of the community as a whole, as we're altering the full-nodes
>> processing requirements or the security architecture of the decentralized
>> bitcoin ecosystem in its integrality.
>>
>> On the other hand fully explaining why such changes would be warranted
>> for the sake of lightning and for designing them well, we might need to lay
>> out in complete state practical and critical attacks on a ~5 355 public BTC
>> ecosystem.
>>
>> Hard dilemma.
>>
>> There might be a lesson in terms of bitcoin protocol deployment, we might
>> have to get them right at first try. Little second chance to fix them in
>> flight.
>>
>> I'll be silent on those issues on public mailing lists until the week of
>> the 30 oct. Enough material has been published and other experts are
>> available. Then I'll be back focusing more on bitcoin core.
>>
>> Best,
>> Antoine
>>
>> Le lun. 16 oct. 2023 ? 17:57, Antoine Riard <antoine.riard@gmail.com> a
>> ?crit :
>>
>>> (cross-posting mempool issues identified are exposing lightning chan to
>>> loss of funds risks, other multi-party bitcoin apps might be affected)
>>>
>>> Hi,
>>>
>>> End of last year (December 2022), amid technical discussions on eltoo
>>> payment channels and incentives compatibility of the mempool anti-DoS
>>> rules, a new transaction-relay jamming attack affecting lightning channels
>>> was discovered.
>>>
>>> After careful analysis, it turns out this attack is practical and
>>> immediately exposed lightning routing hops carrying HTLC traffic to loss of
>>> funds security risks, both legacy and anchor output channels. A potential
>>> exploitation plausibly happening even without network mempools congestion.
>>>
>>> Mitigations have been designed, implemented and deployed by all major
>>> lightning implementations during the last months.
>>>
>>> Please find attached the release numbers, where the mitigations should
>>> be present:
>>> - LDK: v0.0.118 - CVE-2023 -40231
>>> - Eclair: v0.9.0 - CVE-2023-40232
>>> - LND: v.0.17.0-beta - CVE-2023-40233
>>> - Core-Lightning: v.23.08.01 - CVE-2023-40234
>>>
>>> While neither replacement cycling attacks have been observed or reported
>>> in the wild since the last ~10 months or experimented in real-world
>>> conditions on bitcoin mainet, functional test is available exercising the
>>> affected lightning channel against bitcoin core mempool (26.0 release
>>> cycle).
>>>
>>> It is understood that a simple replacement cycling attack does not
>>> demand privileged capabilities from an attacker (e.g no low-hashrate power)
>>> and only access to basic bitcoin and lightning software. Yet I still think
>>> executing such an attack successfully requests a fair amount of bitcoin
>>> technical know-how and decent preparation.
>>>
>>> From my understanding of those issues, it is yet to be determined if the
>>> mitigations deployed are robust enough in face of advanced replacement
>>> cycling attackers, especially ones able to combine different classes of
>>> transaction-relay jamming such as pinnings or vetted with more privileged
>>> capabilities.
>>>
>>> Please find a list of potential affected bitcoin applications in this
>>> full disclosure report using bitcoin script timelocks or multi-party
>>> transactions, albeit no immediate security risk exposure as severe as the
>>> ones affecting lightning has been identified. Only cursory review of
>>> non-lightning applications has been conducted so far.
>>>
>>> There is a paper published summarizing replacement cycling attacks on
>>> the lightning network:
>>>
>>> https://github.com/ariard/mempool-research/blob/2023-10-replacement-paper/replacement-cycling.pdf
>>>
>>>  ## Problem
>>>
>>> A lightning node allows HTLCs forwarding (in bolt3's parlance accepted
>>> HTLC on incoming link and offered HTLC on outgoing link) should settle the
>>> outgoing state with either a success or timeout before the incoming state
>>> timelock becomes final and an asymmetric defavorable settlement might
>>> happen (cf "Flood & Loot: A Systematic Attack on The Lightning Network"
>>> section 2.3 for a classical exposition of this lightning security property).
>>>
>>> Failure to satisfy this settlement requirement exposes a forwarding hop
>>> to a loss of fund risk where the offered HTLC is spent by the outgoing link
>>> counterparty's HTLC-preimage and the accepted HTLC is spent by the incoming
>>> link counterparty's HTLC-timeout.
>>>
>>> The specification mandates the incoming HTLC expiration timelock to be
>>> spaced out by an interval of `cltv_expiry_delta` from the outgoing HTLC
>>> expiration timelock, this exact interval value being an implementation and
>>> node policy setting. As a minimal value, the specification recommends 34
>>> blocks of interval. If the timelock expiration I of the inbound HTLC is
>>> equal to 100 from chain tip, the timelock expiration O of the outbound HTLC
>>> must be equal to 66 blocks from chain tip, giving a reasonable buffer of
>>> reaction to the lightning forwarding node.
>>>
>>> In the lack of cooperative off-chain settlement of the HTLC on the
>>> outgoing link negotiated with the counterparty (either
>>> `update_fulfill_htlc` or `update_fail_htlc`) when O is reached, the
>>> lightning node should broadcast its commitment transaction. Once the
>>> commitment is confirmed (if anchor and the 1 CSV encumbrance is present),
>>> the lightning node broadcasts and confirms its HTLC-timeout before I height
>>> is reached.
>>>
>>> Here enter a replacement cycling attack. A malicious channel
>>> counterparty can broadcast its HTLC-preimage transaction with a higher
>>> absolute fee and higher feerate than the honest HTLC-timeout of the victim
>>> lightning node and triggers a replacement. Both for legacy and anchor
>>> output channels, a HTLC-preimage on a counterparty commitment transaction
>>> is malleable, i.e additional inputs or outputs can be added. The
>>> HTLC-preimage spends an unconfirmed and unrelated to the channel parent
>>> transaction M and conflicts its child.
>>>
>>> As the HTLC-preimage spends an unconfirmed input that was already
>>> included in the unconfirmed and unrelated child transaction (rule 2), pays
>>> an absolute higher fee of at least the sum paid by the HTLC-timeout and
>>> child transaction (rule 3) and the HTLC-preimage feerate is greater than
>>> all directly conflicting transactions (rule 6), the replacement is
>>> accepted. The honest HTLC-timeout is evicted out of the mempool.
>>>
>>> In an ulterior move, the malicious counterparty can replace the parent
>>> transaction itself with another candidate N satisfying the replacement
>>> rules, triggering the eviction of the malicious HTLC-preimage from the
>>> mempool as it was a child of the parent T.
>>>
>>> There is no spending candidate of the offered HTLC output for the
>>> current block laying in network mempools.
>>>
>>> This replacement cycling tricks can be repeated for each rebroadcast
>>> attempt of the HTLC-timeout by the honest lightning node until expiration
>>> of the inbound HTLC timelock I. Once this height is reached a HTLC-timeout
>>> is broadcast by the counterparty's on the incoming link in collusion with
>>> the one on the outgoing link broadcasting its own HTLC-preimage.
>>>
>>> The honest Lightning node has been "double-spent" in its HTLC forwarding.
>>>
>>> As a notable factor impacting the success of the attack, a lightning
>>> node's honest HTLC-timeout might be included in the block template of the
>>> miner winning the block race and therefore realizes a spent of the offered
>>> output. In practice, a replacement cycling attack might over-connect to
>>> miners' mempools and public reachable nodes to succeed in a fast eviction
>>> of the HTLC-timeout by its HTLC-preimage. As this latter transaction can
>>> come with a better ancestor-score, it should be picked up on the flight by
>>> economically competitive miners.
>>>
>>> A functional test exercising a simple replacement cycling of a HTLC
>>> transaction on bitcoin core mempool is available:
>>> https://github.com/ariard/bitcoin/commits/2023-test-mempool
>>>
>>> ## Deployed LN mitigations
>>>
>>> Aggressive rebroadcasting: As the replacement cycling attacker benefits
>>> from the HTLC-timeout being usually broadcast by lightning nodes only once
>>> every block, or less the replacement cycling malicious transactions paid
>>> only equal the sum of the absolute fees paid by the HTLC, adjusted with the
>>> replacement penalty. Rebroadcasting randomly and multiple times before the
>>> next block increases the absolute fee cost for the attacker.
>>>
>>> Implemented and deployed by Eclair, Core-Lightning, LND and LDK .
>>>
>>> Local-mempool preimage monitoring: As the replacement cycling attacker
>>> in a simple setup broadcast the HTLC-preimage to all the network mempools,
>>> the honest lightning node is able to catch on the flight the unconfirmed
>>> HTLC-preimage, before its subsequent mempool replacement. The preimage can
>>> be extracted from the second-stage HTLC-preimage and used to fetch the
>>> off-chain inbound HTLC with a cooperative message or go on-chain with it to
>>> claim the accepted HTLC output.
>>>
>>> Implemented and deployed by Eclair and LND.
>>>
>>> CLTV Expiry Delta: With every jammed block comes an absolute fee cost
>>> paid by the attacker, a risk of the HTLC-preimage being detected or
>>> discovered by the honest lightning node, or the HTLC-timeout to slip in a
>>> winning block template. Bumping the default CLTV delta hardens the odds of
>>> success of a simple replacement cycling attack.
>>>
>>> Default setting: Eclair 144, Core-Lightning 34, LND 80 and LDK 72.
>>>
>>> ## Affected Bitcoin Protocols and Applications
>>>
>>> From my understanding the following list of Bitcoin protocols and
>>> applications could be affected by new denial-of-service vectors under some
>>> level of network mempools congestion. Neither tests or advanced review of
>>> specifications (when available) has been conducted for each of them:
>>> - on-chain DLCs
>>> - coinjoins
>>> - payjoins
>>> - wallets with time-sensitive paths
>>> - peerswap and submarine swaps
>>> - batch payouts
>>> - transaction "accelerators"
>>>
>>> Inviting their developers, maintainers and operators to investigate how
>>> replacement cycling attacks might disrupt their in-mempool chain of
>>> transactions, or fee-bumping flows at the shortest delay. Simple flows and
>>> non-multi-party transactions should not be affected to the best of my
>>> understanding.
>>>
>>> ## Open Problems: Package Malleability
>>>
>>> Pinning attacks have been known for years as a practical vector to
>>> compromise lightning channels funds safety, under different scenarios (cf.
>>> current bip331's motivation section). Mitigations at the mempool level have
>>> been designed, discussed and are under implementation by the community
>>> (ancestor package relay + nverrsion=3 policy). Ideally, they should
>>> constraint a pinning attacker to always attach a high feerate package
>>> (commitment + CPFP) to replace the honest package, or allow a honest
>>> lightning node to overbid a malicious pinning package and get its
>>> time-sensitive transaction optimistically included in the chain.
>>>
>>> Replacement cycling attack seem to offer a new way to neutralize the
>>> design goals of package relay and its companion nversion=3 policy, where an
>>> attacker package RBF a honest package out of the mempool to subsequently
>>> double-spend its own high-fee child with a transaction unrelated to the
>>> channel. As the remaining commitment transaction is pre-signed with a
>>> minimal relay fee, it can be evicted out of the mempool.
>>>
>>> A functional test exercising a simple replacement cycling of a lightning
>>> channel commitment transaction on top of the nversion=3 code branch is
>>> available:
>>> https://github.com/ariard/bitcoin/commits/2023-10-test-mempool-2
>>>
>>> ## Discovery
>>>
>>> In 2018, the issue of static fees for pre-signed lightning transactions
>>> is made more widely known, the carve-out exemption in mempool rules to
>>> mitigate in-mempool package limits pinning and the anchor output pattern
>>> are proposed.
>>>
>>> In 2019, bitcoin core 0.19 is released with carve-out support. Continued
>>> discussion of the anchor output pattern as a dynamic fee-bumping method.
>>>
>>> In 2020, draft of anchor output submitted to the bolts. Initial finding
>>> of economic pinning against lightning commitment and second-stage HTLC
>>> transactions. Subsequent discussions of a preimage-overlay network or
>>> package-relay as mitigations. Public call made to inquiry more on potential
>>> other transaction-relay jamming attacks affecting lightning.
>>>
>>> In 2021, initial work in bitcoin core 22.0 of package acceptance.
>>> Continued discussion of the pinning attacks and shortcomings of current
>>> mempool rules during community-wide online workshops. Later the year, in
>>> light of all issues for bitcoin second-layers, a proposal is made about
>>> killing the mempool.
>>>
>>> In 2022, bip proposed for package relay and new proposed v3 policy
>>> design proposed for a review and implementation. Mempoolfullrbf is
>>> supported in bitcoin core 24.0 and conceptual questions about alignment of
>>> mempool rules w.r.t miners incentives are investigated.
>>>
>>> Along this year 2022, eltoo lightning channels design are discussed,
>>> implemented and reviewed. In this context and after discussions on mempool
>>> anti-DoS rules, I discovered this new replacement cycling attack was
>>> affecting deployed lightning channels and immediately reported the finding
>>> to some bitcoin core developers and lightning maintainers.
>>>
>>> ## Timeline
>>>
>>> - 2022-12-16: Report of the finding to Suhas Daftuar, Anthony Towns,
>>> Greg Sanders and Gloria Zhao
>>> - 2022-12-16: Report to LN maintainers: Rusty Russell, Bastien
>>> Teinturier, Matt Corallo and Olaoluwa Osuntunkun
>>> - 2022-12-23: Sharing to Eugene Siegel (LND)
>>> - 2022-12-24: Sharing to James O'Beirne and Antoine Poinsot
>>> (non-lightning potential affected projects)
>>> - 2022-01-14: Sharing to Gleb Naumenko (miners incentives and
>>> cross-layers issuers) and initial proposal of an early public disclosure
>>> - 2022-01-19: Collection of analysis if other second-layers and
>>> multi-party applications affected. LN mitigations development starts.
>>> - 2023-05-04: Sharing to Wilmer Paulino (LDK)
>>> - 2023-06-20: LN mitigations implemented and progressively released.
>>> Week of the 16 october proposed for full disclosure.
>>> - 2023-08-10: CVEs assigned by MITRE
>>> - 2023-10-05: Pre-disclosure of LN CVEs numbers and replacement cycling
>>> attack existence to security@bitcoincore.org.
>>> - 2023-10-16: Full disclosure of CVE-2023-40231 / CVE-2023-40232 /
>>> CVE-2023-40233 / CVE-2023-40234 and replacement cycling attacks
>>>
>>> ## Conclusion
>>>
>>> Despite the line of mitigations adopted and deployed by current major
>>> lightning implementations, I believe replacement cycling attacks are still
>>> practical for advanced attackers. Beyond this new attack might come as a
>>> way to partially or completely defeat some of the pinning mitigations which
>>> have been working for years as a community.
>>>
>>> As of today, it is uncertain to me if lightning is not affected by a
>>> more severe long-term package malleability critical security issue under
>>> current consensus rules, and if any other time-sensitive multi-party
>>> protocol, designed or deployed isn't de facto affected too (loss of funds
>>> or denial of service).
>>>
>>> Assuming analysis on package malleability is correct, it is unclear to
>>> me if it can be corrected by changes in replacement / eviction rules or
>>> mempool chain of transactions processing strategy. Inviting my technical
>>> peers and the bitcoin community to look more on this issue, including to
>>> dissent. I'll be the first one pleased if I'm fundamentally wrong on those
>>> issues, or if any element has not been weighted with the adequate technical
>>> accuracy it deserves.
>>>
>>> Do not trust, verify. All mistakes and opinions are my own.
>>>
>>> Antoine
>>>
>>> "meet with Triumph and Disaster. And treat those two impostors just the
>>> same" - K.
>>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231102/c422c01d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 2
*******************************************
