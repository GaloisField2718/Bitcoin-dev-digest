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

   1. Bitcoin Core 26.0 release candidate 2 available (Michael Ford)
   2. ossification and misaligned incentive concerns (Erik Aronesty)
   3. Re: The Pinning & Replacement Problem Set (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Fri, 3 Nov 2023 17:21:24 +0000
From: Michael Ford <fanquake@gmail.com>
To: bitcoin-core-dev@lists.linuxfoundation.org,
	bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin Core 26.0 release candidate 2 available
Message-ID:
	<CAFyhPjXOP3+zhTOsT8iCkxh2ejoDddO9GX49F64zMYOSTX5fcA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Binaries for Bitcoin Core version v26.0rc2 are available from:

    https://bitcoincore.org/bin/bitcoin-core-26.0/test.rc2/

Source code can be found in git under the signed tag

    https://github.com/bitcoin/bitcoin/tree/v26.0rc2

This is a release candidate for a new major version release.

Preliminary release notes for the release can be found here:

    https://github.com/bitcoin-core/bitcoin-devwiki/wiki/26.0-Release-Notes-Draft

Release candidates are test versions for releases.
When no critical problems are found, this release candidate will be
tagged as v26.0.
26.0rc1 was abandoned after packaing issues with the codesigned
macOS binaries.


------------------------------

Message: 2
Date: Fri, 3 Nov 2023 14:24:00 -0400
From: Erik Aronesty <erik@q32.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] ossification and misaligned incentive concerns
Message-ID:
	<CAJowKgJXxS3L=pQR=jhSXBgdDR9k5mwPyKhKkuFESw5_qOgdrQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

currently, there are providers of anonymity services, scaling services,
custody, and other services layered on top of bitcoin using trust-based and
federated models.

as bitcoin becomes more popular, these service providers have increasingly
had a louder "voice" in development and maintenance of the protocol

holders generally want these features

but service providers have an incentive to maintain a "moat" around their
services

in summary, making privacy, scaling and vaulting "hard" for regular users,
keeping it off-chain and federated...  is now incentivised among a vocal,
but highly technical, minority

is anyone else worried about this?
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231103/5c29bb85/attachment.html>

------------------------------

Message: 3
Date: Fri, 3 Nov 2023 19:57:35 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: John Carvalho <john@synonym.to>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] The Pinning & Replacement Problem Set
Message-ID:
	<CALZpt+HQ0KMufd7Hmkpq+opOT7H9rZJccqzy=v6s3bao5zQAzQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi John,

I think lightning and other second time-sensitive layers being hit by
safety issues whenever the blocks are full is common knowledge as the issue
is being described in the paper under the "forced expiration spam" issues
arising spontaneously within an environment with high block space demand. I
believe you have known variants of those issues with the "flood & loot"
style scenarios.

What is coming as a new problem with the novel replacement issues lay in
the fact that your counterparty channel might always defer the confirmation
of your honest on-chain spend, in a way which is compatible with miners
incentives.

While this has been commonized by the wide deployment of bip-125-style RBF
over network mempools, this ability has been always available to any party
reaching out directly to miners out-of-band with consensus-valid
transactions. In a world where miners are pseudonymous (as we're mostly
seeing today, not considering pools) miners motivated by maximizing their
satoshi-denominated income is a reasonable assumption in my opinion.

As an ecosystem beyond core to fix sustainably pinning and replacement
problems, and I agree with you here, we are stuck with a "between Scylla
and Charybdis" serious safety issue, I'm seeing the following options.
Matching yours, rephrasing in my own words to ensure correct understanding.

1. We can revert to a static world with no replacement-by-fee mechanism as
a widely deployed network policy.

I think in a world where miners are in competition you can always reach out
to them with out-of-band higher fees packages than available in their local
mempool.

2. We can design, implement and deploy policies to better capture
transaction-issuer intent on the way future spend candidates are allowed
(or not) to replace the current in-mempool transaction.

Sadly, I think with lightning and other second time-sensitive layers, there
is no "single" transaction-issuer intent, though you might have as many
intents that you have counterparties within your off-chain states, all with
competing interests.

3. We can remove all policy and let the network of nodes and the economic
ecosystem evolve on its own.

I think a lot of mempool policy in place is actually anti-DoS measures
which are protecting at least the lowest-performance full-nodes, and those
measures are the source of issues for pinning. "Pure" RBF sounds to me only
to make adversarial replacement issues worse (at least nversion=3-style
policy introduces some assumptions on max package size if widely deployed).

4. We can do nothing and let a fragmented mempool environment, where every
large lightning and bitcoin business have out-of-band relationships with
miners and pools to support their packages, with some service-level safety
agreements.

I think this option was weighted as a way to solve pinning issues at the
commitment and second-state level years ago by the lightning community,
though it was brushed aside as bringing rampant centralization of the
lightning network, where small lightning nodes might not have privileged
access to miners [0].

5. We can design and implement some magical consensus-change or alter the
processing requirements (bandwidth, CPU perf, I/O disk) of full-nodes on
the peer-to-peer network to align incentives between miners and lightning
and time-sensitive second-layers.

I think this option represents more or less what are the trade-offs of what
is discussed by the "reverse locktime" new bitcoin script opcode idea or
replacement cache at the mempool-level in core [1].

Best,
Antoine

[0] https://github.com/lightning/bolts/issues/783
[1] https://github.com/bitcoin/bitcoin/issues/28699

Le jeu. 2 nov. 2023 ? 11:38, John Carvalho via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

> Good morning,
>
> All layers and technologies "on" Bitcoin will fail in situations where
> miners misbehave or the blocks & mempool remain consistently, overly full.
> Consider this as a "law" of Bitcoin/blockchains.
>
> In hindsight (for you, not me) it was very unwise to start messing with
> mempool policies, like with RBF, mempoolfullrbf. First-seen policy brought
> a fragile harmony and utility to Bitcoin, which we were lucky to have for
> as long as we could.
>
> The engineers intentionally broke this. Mempoofullrbf washes away the
> ability for users to express their intent on whether to pin or replace a
> transaction, and now Lightning has BOTH pinning and replacement problems.
> You could argue this was inevitable. The point here is that layers have
> mempool and miner problems.
>
> Core has a few choices here, as I see it:
>
> 1. They can try to revert mempoolfullrbf and re-establish first-seen
> policy. Hard to say whether this would work, or whether it would be
> enough...
>
> 2. They can create additional policies that are enforced by default that
> allow people to flag how they want their txn handled, as in, a "pin this"
> vs "replace this" aspect to every txn. This is probably the best option, as
> it allows miners to know what people want and give it to them. This is
> utility, thus incentive-compatible.
>
> 3. Remove all policy and let the market evolve to deal with the chaos.
> Which is similar to the next option: do nothing.
>
> 4. Do nothing and allow a fractured mempool environment to evolve where
> large businesses form private contracts with miners and pools to support
> their own unsupported policies, so they can provide better experiences to
> customers and users.
>
> 5. Invent some miracle magical crypto cure that I am not capable of
> imagining at this time.
>
> I disclaim some ignorance to details of how other mempool research might
> affect these options and problems, but I am skeptical the dynamics
> discussed here can be removed entirely.
>
> --John Carvalho
> CEO, Synonym.to <http://synonym.to/>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231103/2222c152/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 6
*******************************************
