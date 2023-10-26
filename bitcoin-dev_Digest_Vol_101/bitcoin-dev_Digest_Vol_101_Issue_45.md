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

   1. Bitcoin Core 24.2 released (Michael Ford)
   2. Re: Proposed BIP for OP_CAT (Ryan Grant)
   3. Re: Proposed BIP for OP_CAT (James O'Beirne)
   4. HTLC output aggregation as a mitigation for tx recycling,
      jamming, and on-chain efficiency (covenants) (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Thu, 26 Oct 2023 14:06:00 +0100
From: Michael Ford <fanquake@gmail.com>
To: bitcoin-core-dev@lists.linuxfoundation.org,
	bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin Core 24.2 released
Message-ID:
	<CAFyhPjUVqgc27zAqbjmr+exuqttKqAJ0FZa+=QRicqs5i6_4Aw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Bitcoin Core version v24.2 is now available from:

    https://bitcoincore.org/bin/bitcoin-core-24.2/

Or through BitTorrent:

    magnet:?xt=urn:btih:6bde4d046f4aa794df4f3603688cb22e0a8a4a68&dn=bitcoin-core-24.2&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.bitcoin.sprovoost.nl%3A6969&ws=http%3A%2F%2Fbitcoincore.org%2Fbin%2F

This release includes various bug fixes and performance
improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/bitcoin/bitcoin/issues>

To receive security and update notifications, please subscribe to:

  <https://bitcoincore.org/en/list/announcements/join/>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes in some cases), then run the
installer (on Windows) or just copy over `/Applications/Bitcoin-Qt` (on macOS)
or `bitcoind`/`bitcoin-qt` (on Linux).

Upgrading directly from a version of Bitcoin Core that has reached its EOL is
possible, but it might take some time if the data directory needs to
be migrated. Old
wallet versions of Bitcoin Core are generally supported.

Compatibility
==============

Bitcoin Core is supported and extensively tested on operating systems
using the Linux kernel, macOS 10.15+, and Windows 7 and newer.  Bitcoin
Core should also work on most other Unix-like systems but is not as
frequently tested on them.  It is not recommended to use Bitcoin Core on
unsupported systems.

### Fees

- #27622 Fee estimation: avoid serving stale fee estimate

### RPC and other APIs

- #27727 rpc: Fix invalid bech32 address handling

### Build System

- #28097 depends: xcb-proto 1.15.2
- #28543 build, macos: Fix qt package build with new Xcode 15 linker
- #28571 depends: fix unusable memory_resource in macos qt build

### CI

- #27777 ci: Prune dangling images on RESTART_CI_DOCKER_BEFORE_RUN
- #27834 ci: Nuke Android APK task, Use credits for tsan
- #27844 ci: Use podman stop over podman kill
- #27886 ci: Switch to amd64 container in "ARM" task

### Miscellaneous
- #28452 Do not use std::vector = {} to release memory

Credits
=======

Thanks to everyone who directly contributed to this release:

- Abubakar Sadiq Ismail
- Hennadii Stepanov
- Marco Falke
- Michael Ford
- Pieter Wuille

As well as to everyone that helped with translations on
[Transifex](https://www.transifex.com/bitcoin/bitcoin/).


------------------------------

Message: 2
Date: Thu, 26 Oct 2023 14:30:12 +0000
From: Ryan Grant <bitcoin-dev@rgrant.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<CAMnpzfp3Df3SpE5+B5x2xYnjOWz+Q-BcRWdmotNhVO=-JDyTMw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

I support OP_CAT, along with reasonable resource-consumption limiters.

Implementation as a UASF would help build confidence in that method.

I also support moving forward on other opcodes as soon as they are
known to be safe and maintainable; whether for introspection, tx
unpinning, or vaults.


------------------------------

Message: 3
Date: Thu, 26 Oct 2023 12:04:52 -0400
From: "James O'Beirne" <james.obeirne@gmail.com>
To: Andrew Poelstra <apoelstra@wpsoftware.net>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<CAPfvXfK667yenYeZi_4iUWskdVaJgS37PC3X0dqYNaehPErDcQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

I have to admit - I'm somewhat baffled at the enthusiasm for a "just CAT"
softfork, since I can't see that it would achieve much. It's indicative to
me that there isn't a compelling example to date that (i) actually has
working code and (ii) only relies upon CAT. I'm not averse to CAT, just
confused that there's a lot of enthusiasm for a CAT-only fork.

To do actually-interesting covenants, afacit you'd need "introspection"
opcodes and/or CHECKSIGFROMSTACK - and even then, for almost all
applications I'm familiar with, that kind of CAT-based approach would be
much more circuitous than the alternatives that have been discussed for
years on this list.

> Vaults

I don't think this is actually a use-case that CAT materially helps with.
Andrew's posts, while well written and certainly foundational, do not
sketch a design for vaults that someone would actually use. I don't see how
CAT alone (without many auxiliary introspection opcodes) facilitates vaults
that clear the usability hurdles I describe in this paper:
https://jameso.be/vaults.pdf. For example, batched withdrawals and partial
unvaultings don't seem possible.

Even with introspection opcodes, Burak's (
https://brqgoo.medium.com/emulating-op-vault-with-elements-opcodes-bdc7d8b0fe71)
prototype wasn't able to handle revaulting - an important feature for
usability (https://twitter.com/jamesob/status/1636546085186412544).

> Tree signatures

To what extent does Taproot obviate this use?
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231026/2c0de51e/attachment.html>

------------------------------

Message: 4
Date: Thu, 26 Oct 2023 12:52:03 -0400
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] HTLC output aggregation as a mitigation for tx
	recycling, jamming, and on-chain efficiency (covenants)
Message-ID:
	<CAD3i26Dux33wF=Ki0ouChseW7dehRuz+QC54bmsm7xzm2YACQQ@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi all,

After the transaction recycling has spurred some discussion the last
week or so, I figured it could be worth sharing some research I?ve
done into HTLC output aggregation, as it could be relevant for how to
avoid this problem in a future channel type.

TLDR; With the right covenant we can create HTLC outputs that are much
more chain efficient, not prone to tx recycling and harder to jam.

## Transaction recycling
The transaction recycling attack is made possible by the change made
to HTLC second level transactions for the anchor channel type[8];
making it possible to add fees to the transaction by adding inputs
without violating the signature. For the legacy channel type this
attack was not possible, as all fees were taken from the HTLC outputs
themselves, and had to be agreed upon by channel counterparties during
signing (of course this has its own problems, which is why we wanted
to change it).

The idea of HTLC output aggregation is to collapse all HTLC outputs on
the commitment to a single one. This has many benefits (that I?ll get
to), one of them being the possibility to let the spender claim the
portion of the output that they?re right to, deciding how much should
go to fees. Note that this requires a covenant to be possible.

## A single HTLC output
Today, every forwarded HTLC results in an output that needs to be
manifested on the commitment transaction in order to claw back money
in case of an uncooperative channel counterparty. This puts a limit on
the number of active HTLCs (in order for the commitment transaction to
not become too large) which makes it possible to jam the channel with
small amounts of capital [1]. It also turns out that having this limit
be large makes it expensive and complicated to sweep the outputs
efficiently [2].

Instead of having new HTLC outputs manifest for each active
forwarding, with covenants on the base layer one could create a single
aggregated output on the commitment. The output amount being the sum
of the active HTLCs (offered and received), alternatively one output
for received and one for offered. When spending this output, you would
only be entitled to the fraction of the amount corresponding to the
HTLCs you know the preimage for (received), or that has timed out
(offered).

## Impacts to transaction recycling
Depending on the capabilities of the covenant available (e.g.
restricting the number of inputs to the transaction) the transaction
spending the aggregated HTLC output can be made self sustained: the
spender will be able to claim what is theirs (preimage or timeout) and
send it to whatever output they want, or to fees. The remainder will
go back into a covenant restricted output with the leftover HTLCs.
Note that this most likely requires Eltoo in order to not enable fee
siphoning[7].

## Impacts to slot jamming
With the aggregated output being a reality, it changes the nature of
?slot jamming? [1] significantly. While channel capacity must still be
reserved for in-flight HTLCs, one no longer needs to allocate a
commitment output for each up to some hardcoded limit.

In today?s protocol this limit is 483, and I believe most
implementations default to an even lower limit. This leads to channel
jamming being quite inexpensive, as one can quickly fill a channel
with small HTLCs, without needing a significant amount of capital to
do so.

The origins of the 483 slot limits is the worst case commitment size
before getting into unstandard territory [3]. With an aggregated
output this would no longer be the case, as adding HTLCs would no
longer affect commitment size. Instead, the full on-chain footprint of
an HTLC would be deferred until claim time.

Does this mean one could lift, or even remove the limit for number of
active HTLCs? Unfortunately, the obvious approach doesn?t seem to get
rid of the problem entirely, but mitigates it quite a bit.

### Slot jamming attack scenario
Consider the scenario where an attacker sends a large number of
non-dust* HTLCs across a channel, and the channel parties enforce no
limit on the number of active HTLCs.

The number of payments would not affect the size of the commitment
transaction at all, only the size of the witness that must be
presented when claiming or timing out the HTLCs. This means that there
is still a point at which chain fees get high enough for the HTLC to
be uneconomical to claim. This is no different than in today?s spec,
and such HTLCs will just be stranded on-chain until chain fees
decrease, at which point there is a race between the success and
timeout spends.

There seems to be no way around this; if you want to claim an HTLC
on-chain, you need to put the preimage on-chain. And when the HTLC
first reaches you, you have no way of predicting the future chain fee.
With a large number of uneconomical HTLCs in play, the total BTC
exposure could still be very large, so you might want to limit this
somewhat.

* Note that as long as the sum of HTLCs exceeds the dust limit, one
could manifest the output on the transaction.

## The good news
With an aggregated HTLC output, the number of HTLCs would no longer
impact the commitment transaction size while the channel is open and
operational.

The marginal cost of claiming an HTLC with a preimage on-chain would
be much lower; no new inputs or outputs, only a linear increase in the
witness size. With a covenant primitive available, the extra footprint
of the timeout and success transactions would no longer exist.

Claiming timed out HTLCs could still be made close to constant size
(no preimage to present), so no additional on-chain cost with more
HTLCs.

## The bad news
The most obvious problem is that we would need a new covenant
primitive on L1 (see below). However, I think it could be beneficial
to start exploring these ideas now in order to guide the L1 effort
towards something we could utilize to its fullest on L2.

As mentioned, even with a functioning covenant, we don?t escape the
fact that a preimage needs to go on-chain, pricing out HTLCs at
certain fee rates. This is analogous to the dust exposure problem
discussed in [6], and makes some sort of limit still required.

### Open question
With PTLCs, could one create a compact proof showing that you know the
preimage for m-of-n of the satoshis in the output? (some sort of
threshold signature).

If we could do this we would be able to remove the slot jamming issue
entirely; any number of active PTLCs would not change the on-chain
cost of claiming them.

## Covenant primitives
A recursive covenant is needed to achieve this. Something like OP_CTV
and OP_APO seems insufficient, since the number of ways the set of
HTLCs could be claimed would cause combinatorial blowup in the number
of possible spending transactions.

Personally, I?ve found the simple yet powerful properties of
OP_CHECKCONTRACTVERIFY [4] together with OP_CAT and amount inspection
particularly interesting for the use case, but I?m certain many of the
other proposals could achieve the same thing. More direct inspection
like you get from a proposal like OP_TX[9] would also most likely have
the building blocks needed.

### Proof-of-concept
I?ve implemented a rough demo** of spending an HTLC output that pays
to a script with OP_CHECKCONTRACTVERIFY to achieve this [5]. The idea
is to commit to all active HTLCs in a merkle tree, and have the
spender provide merkle proofs for the HTLCs to claim, claiming the sum
into a new output. The remainder goes back into a new output with the
claimed HTLCs removed from the merkle tree.

An interesting trick one can do when creating the merkle tree, is
sorting the HTLCs by expiry. This means that one in the timeout case
claim a subtree of HTLCs using a single merkle proof (and RBF this
batched timeout claim as more and more HTLCs expire) reducing the
timeout case to constant size witness (or rather logarithmic in the
total number of HTLCs).

**Consider it an experiment, as it is missing a lot before it could be
usable in any real commitment setting.


[1] https://bitcoinops.org/en/topics/channel-jamming-attacks/#htlc-jamming-attack
[2] https://github.com/lightning/bolts/issues/845
[3] https://github.com/lightning/bolts/blob/aad959a297ff66946effb165518143be15777dd6/02-peer-protocol.md#rationale-7
[4] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021182.html
[5] https://github.com/halseth/tapsim/blob/b07f29804cf32dce0168ab5bb40558cbb18f2e76/examples/matt/claimpool/script.txt
[6] https://lists.linuxfoundation.org/pipermail/lightning-dev/2021-October/003257.html
[7] https://github.com/lightning/bolts/issues/845#issuecomment-937736734
[8] https://github.com/lightning/bolts/blob/8a64c6a1cef979b3f0cecb00ba7a48c2d28b3588/03-transactions.md?plain=1#L333
[9] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020450.html


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 45
********************************************
