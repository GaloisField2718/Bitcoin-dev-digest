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

   1. Re: Ark: An Alternative Privacy-preserving Second Layer
      Solution (jk_14@op.pl)
   2. Bitcoin Core 25.0 released (Michael Ford)
   3. Re: Merkleize All The Things (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Fri, 26 May 2023 07:33:42 +0000
From: jk_14@op.pl
To: "David A. Harding" <dave@dtrt.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Burak Keceli
	<burak@buraks.blog>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second Layer Solution
Message-ID: <993e075b-f989-ec2d-ad89-ccd0fe0b34e8@op.pl>
Content-Type: text/plain; charset="us-ascii"

An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230526/dc200fd3/attachment.html>

------------------------------

Message: 2
Date: Fri, 26 May 2023 11:39:17 +0100
From: Michael Ford <fanquake@gmail.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin Core 25.0 released
Message-ID:
	<CAFyhPjUcqrVawv7ToSikOXyMVYGhQKTBu-ZZHxnZL9ELRK6qDw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Bitcoin Core version v25.0 is now available from:

    https://bitcoincore.org/bin/bitcoin-core-25.0/

Or through BitTorrent:

    magnet:?xt=urn:btih:092358777175c4306602f9b1b523738df4b4610b&dn=bitcoin-core-25.0&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.bitcoin.sprovoost.nl%3A6969&ws=http%3A%2F%2Fbitcoincore.org%2Fbin%2F

This release includes new features, various bug fixes and performance
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

Notable changes
===============

P2P and network changes
-----------------------

- Transactions of non-witness size 65 bytes and above are now allowed by mempool
  and relay policy. This is to better reflect the actual afforded protections
  against CVE-2017-12842 and open up additional use-cases of smaller
transaction sizes. (#26265)

New RPCs
--------

- The scanblocks RPC returns the relevant blockhashes from a set of
descriptors by
  scanning all blockfilters in the given range. It can be used in
combination with
  the getblockheader and rescanblockchain RPCs to achieve fast wallet
rescans. Note
  that this functionality can only be used if a compact block filter index
  (-blockfilterindex=1) has been constructed by the node. (#23549)

Updated RPCs
------------

- All JSON-RPC methods accept a new [named
  parameter](https://github.com/bitcoin/bitcoin/blob/master/doc/JSON-RPC-interface.md#parameter-passing)
called `args` that can
  contain positional parameter values. This is a convenience to allow some
  parameter values to be passed by name without having to name every value. The
  python test framework and `bitcoin-cli` tool both take advantage of this, so
  for example:

```sh
bitcoin-cli -named createwallet wallet_name=mywallet load_on_startup=1
```

Can now be shortened to:

```sh
bitcoin-cli -named createwallet mywallet load_on_startup=1
```

- The `verifychain` RPC will now return `false` if the checks didn't fail,
  but couldn't be completed at the desired depth and level. This could be due
  to missing data while pruning, due to an insufficient dbcache or due to
  the node being shutdown before the call could finish. (#25574)

- `sendrawtransaction` has a new, optional argument, `maxburnamount`
with a default value of `0`.
  Any transaction containing an unspendable output with a value
greater than `maxburnamount` will
  not be submitted. At present, the outputs deemed unspendable are
those with scripts that begin
  with an `OP_RETURN` code (known as 'datacarriers'), scripts that
exceed the maximum script size,
  and scripts that contain invalid opcodes.

- The `testmempoolaccept` RPC now returns 2 additional results within
the "fees" result:
  "effective-feerate" is the feerate including fees and sizes of
transactions validated together if
  package validation was used, and also includes any modified fees
from prioritisetransaction. The
  "effective-includes" result lists the wtxids of transactions whose
modified fees and sizes were used
  in the effective-feerate (#26646).

- `decodescript` may now infer a Miniscript descriptor under P2WSH
context if it is not lacking
  information. (#27037)

- `finalizepsbt` is now able to finalize a transaction with inputs
spending Miniscript-compatible
  P2WSH scripts. (#24149)

Changes to wallet related RPCs can be found in the Wallet section below.

Build System
------------

- The `--enable-upnp-default` and `--enable-natpmp-default` options
  have been removed. If you want to use port mapping, you can
  configure it using a .conf file, or by passing the relevant
  options at runtime. (#26896)

Updated settings
----------------

- If the `-checkblocks` or `-checklevel` options are explicitly provided by the
user, but the verification checks cannot be completed due to an insufficient
dbcache, Bitcoin Core will now return an error at startup. (#25574)

- Ports specified in `-port` and `-rpcport` options are now validated
at startup.
  Values that previously worked and were considered valid can now
result in errors. (#22087)

- Setting `-blocksonly` will now reduce the maximum mempool memory
  to 5MB (users may still use `-maxmempool` to override). Previously,
  the default 300MB would be used, leading to unexpected memory usage
  for users running with `-blocksonly` expecting it to eliminate
  mempool memory usage.

  As unused mempool memory is shared with dbcache, this also reduces
  the dbcache size for users running with `-blocksonly`, potentially
  impacting performance.
- Setting `-maxconnections=0` will now disable `-dnsseed`
  and `-listen` (users may still set them to override).

Changes to GUI or wallet related settings can be found in the GUI or
Wallet section below.

New settings
------------

- The `shutdownnotify` option is used to specify a command to execute
synchronously
before Bitcoin Core has begun its shutdown sequence. (#23395)


Wallet
------

- The `minconf` option, which allows a user to specify the minimum number
of confirmations a UTXO being spent has, and the `maxconf` option,
which allows specifying the maximum number of confirmations, have been
added to the following RPCs in #25375:
  - `fundrawtransaction`
  - `send`
  - `walletcreatefundedpsbt`
  - `sendall`

- Added a new `next_index` field in the response in `listdescriptors` to
  have the same format as `importdescriptors` (#26194)

- RPC `listunspent` now has a new argument `include_immature_coinbase`
  to include coinbase UTXOs that don't meet the minimum spendability
  depth requirement (which before were silently skipped). (#25730)

- Rescans for descriptor wallets are now significantly faster if compact
  block filters (BIP158) are available. Since those are not constructed
  by default, the configuration option "-blockfilterindex=1" has to be
  provided to take advantage of the optimization. This improves the
  performance of the RPC calls `rescanblockchain`, `importdescriptors`
  and `restorewallet`. (#25957)

- RPC `unloadwallet` now fails if a rescan is in progress. (#26618)

- Wallet passphrases may now contain null characters.
  Prior to this change, only characters up to the first
  null character were recognized and accepted. (#27068)

- Address Purposes strings are now restricted to the currently known
values of "send",
  "receive", and "refund". Wallets that have unrecognized purpose
strings will have
  loading warnings, and the `listlabels` RPC will raise an error if an
unrecognized purpose
  is requested. (#27217)

- In the `createwallet`, `loadwallet`, `unloadwallet`, and
`restorewallet` RPCs, the
  "warning" string field is deprecated in favor of a "warnings" field that
  returns a JSON array of strings to better handle multiple warning messages and
  for consistency with other wallet RPCs. The "warning" field will be fully
  removed from these RPCs in v26. It can be temporarily re-enabled during the
  deprecation period by launching bitcoind with the configuration option
  `-deprecatedrpc=walletwarningfield`. (#27279)

- Descriptor wallets can now spend coins sent to P2WSH Miniscript
descriptors. (#24149)

GUI changes
-----------

- The "Mask values" is a persistent option now. (gui#701)
- The "Mask values" option affects the "Transaction" view now, in
addition to the
  "Overview" one. (gui#708)

REST
----

- A new `/rest/deploymentinfo` endpoint has been added for fetching various
  state info regarding deployments of consensus changes. (#25412)

Binary verification
----

- The binary verification script has been updated. In previous releases it
  would verify that the binaries had been signed with a single "release key".
  In this release and moving forward it will verify that the binaries are
  signed by a _threshold of trusted keys_. For more details and
  examples, see:
  https://github.com/bitcoin/bitcoin/blob/master/contrib/verify-binaries/README.md
  (#27358)

Low-level changes
=================

RPC
---

- The JSON-RPC server now rejects requests where a parameter is
specified multiple
  times with the same name, instead of silently overwriting earlier
parameter values
  with later ones. (#26628)
- RPC `listsinceblock` now accepts an optional `label` argument
  to fetch incoming transactions having the specified label. (#25934)
- Previously `setban`, `addpeeraddress`, `walletcreatefundedpsbt`, methods
  allowed non-boolean and non-null values to be passed as boolean parameters.
  Any string, number, array, or object value that was passed would be treated
  as false. After this change, passing any value except `true`, `false`, or
  `null` now triggers a JSON value is not of expected type error. (#26213)

Credits
=======

Thanks to everyone who directly contributed to this release:

- 0xb10c
- 721217.xyz
- @RandyMcMillan
- amadeuszpawlik
- Amiti Uttarwar
- Andrew Chow
- Andrew Toth
- Anthony Towns
- Antoine Poinsot
- Aur?le Oul?s
- Ben Woosley
- Bitcoin Hodler
- brunoerg
- Bushstar
- Carl Dong
- Chris Geihsler
- Cory Fields
- David Gumberg
- dergoegge
- Dhruv Mehta
- Dimitris Tsapakidis
- dougEfish
- Douglas Chimento
- ekzyis
- Elichai Turkel
- Ethan Heilman
- Fabian Jahr
- FractalEncrypt
- furszy
- Gleb Naumenko
- glozow
- Greg Sanders
- Hennadii Stepanov
- hernanmarino
- ishaanam
- ismaelsadeeq
- James O'Beirne
- jdjkelly@gmail.com
- Jeff Ruane
- Jeffrey Czyz
- Jeremy Rubin
- Jesse Barton
- Jo?o Barbosa
- JoaoAJMatos
- John Moffett
- Jon Atack
- Jonas Schnelli
- jonatack
- Joshua Kelly
- josibake
- Juan Pablo Civile
- kdmukai
- klementtan
- Kolby ML
- kouloumos
- Kristaps Kaupe
- laanwj
- Larry Ruane
- Leonardo Araujo
- Leonardo Lazzaro
- Luke Dashjr
- MacroFake
- MarcoFalke
- Martin Leitner-Ankerl
- Martin Zumsande
- Matt Whitlock
- Matthew Zipkin
- Michael Ford
- Miles Liu
- mruddy
- Murray Nesbitt
- muxator
- omahs
- pablomartin4btc
- Pasta
- Pieter Wuille
- Pttn
- Randall Naar
- Riahiamirreza
- roconnor-blockstream
- Russell O'Connor
- Ryan Ofsky
- S3RK
- Sebastian Falbesoner
- Seibart Nedor
- sinetek
- Sjors Provoost
- Skuli Dulfari
- SomberNight
- Stacie Waleyko
- stickies-v
- stratospher
- Suhas Daftuar
- Suriyaa Sundararuban
- TheCharlatan
- Vasil Dimov
- Vasil Stoyanov
- virtu
- w0xlt
- willcl-ark
- yancy
- Yusuf Sahin HAMZA

As well as to everyone that helped with translations on
[Transifex](https://www.transifex.com/bitcoin/bitcoin/).


------------------------------

Message: 3
Date: Fri, 26 May 2023 13:45:17 +0200
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Salvatore Ingala <salvatore.ingala@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Merkleize All The Things
Message-ID:
	<CAD3i26DMGj=KRfi=gqHPdCZ_WyUAvWV50g7TcH4n2e3xSCx8Lg@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi, Salvatore.

As a further exploration of this idea, I implemented a
proof-of-concept of OP_CICV and OP_COCV in btcd[1] that together with
OP_CAT enables a set of interesting use cases.

One such use case is, as mentioned earlier, CoinPools[2]. The opcodes
let you easily check the "dynamically committed data" of an input you
are spending, and enforce a new commitment on the output. The idea is
to have the set of participants in the pool, and their balances, be
the UTXOs committed data, and  use this to validate the legitimacy of
a transaction, determining whether it permits a peer to exit with a
portion of the pooled funds.

Doing what you suggested above, having the input and output commit to
a merkle tree of participants and balances, we are able to quite
elegantly verify the coin pool exit clause. Here is a working example
of how that could look like: [3]. Obviously this lacks a lot before it
is a working CoinPool implementation, but it demonstrates how
OP_C[I/O]V introduces "memory" to Bitcoin script.

Having done this exercise, I have a few suggestions on how one could
further extend the proposal:

1. In the current proposal for OP_CHECKOUTPUTCONTRACTVERIFY, the
opcodes check whether the output key Q is key X tweaked with data D
and taproot T: Q == tweak(tweak(X,D), T).

OP_CHECKINPUTCONTRACTVERIFY on the other hand, works on the input
internal key, and does not care about the taptree on the input: P ==
tweak(X,D), where Q = tweak(P, T). In most cases this is probably good
enough, since you are already executing the current script and that
way know the spender has provided the correct taproot.

However, in the coin pool script mentioned above, I found that I
wanted to re-use the same taproot for the output (recursively). I
believe this would be a quite common use case. To solve this I
committed the taproot as part of the data itself: D' = hash(T+D),
which was then verified by OP_CICV. If you are aware of more efficient
alternatives, I am eager to hear them.

A simpler way IMO, would be to make OP_CICV and OP_COCV symmetrical:
Have OP_CICV take an optional taproot and do the same check as is done
for the output: Q == tweak(tweak(X,D), T).

2.To make fully functioning CoinPools, one would need functionality
similar to OP_MERKLESUB[4]: remove some data from the merkle tree, and
remove a key from the aggregated internal key.This suggestion may
surpass the intended scope of this proposal, and would likely
necessitate the availability of multiple EC operations to accommodate
various key schemes. If we had opcodes for adding and removing keys
from the internal key this would be even more powerful.

I look forward to hearing your thoughts on these suggestions and
further exploring the possibilities of the proposal!

Cheers,
Johan

[1] https://github.com/halseth/btcd/pull/1/commits/90a4065bdcd8029fe3325514a250490cba66fddd
[2] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017964.html
[3] https://github.com/halseth/tapsim/tree/matt-demo/examples/matt/coinpool
[4] https://github.com/ariard/bips/blob/coinpool-bips/bip-merklesub.mediawiki


On Fri, May 5, 2023 at 11:18?PM Salvatore Ingala
<salvatore.ingala@gmail.com> wrote:
>
> On Thu, 4 May 2023 at 10:34, Johan Tor?s Halseth <johanth@gmail.com> wrote:
> >
> > It sounds like we can generalize the description of the construct to:
> > Access to (the hash of) embedded data of inputs and outputs, and the
> > enforcement of output keys and (static) taptrees. In other words, as
> > long as you can dynamically compute the output embedded data in
> > Script, you can enforce more or less anything (since you can make the
> > output script enforce presenting a witness "satisfying" the embedded
> > data).
> >
> > Does that sound about right?
>
> Yes. Fraud proofs allow us to extend beyond what Script can do (with the
> necessary tradeoffs), but there is plenty that can be done without them.
>
>
> > For instance, I believe you could simulate coin pools pretty easily:
> > Commit to the set of pubkeys and amounts owned by the participants in
> > the pool, and an output taptree where each participant has their own
> > spending path. Now, to exit the pool unilaterally, the participant
> > must present a proof that their pubkey+amount is committed to in the
> > input and an output where it is no longer committed.
>
> I don't think one would want to have a tapleaf for each participant:
> that would make you pay log n hashes just to reveal the tapleaf, and
> then you still need to pay log n hashes to access the embedded data.
>
> Instead, the "unilateral withdrawal Script" can be the same for all the
> participants. The witness would be the Merkle proof, plus perhaps some
> additional information to identify the leaf in the tree (depending on
> how the Merkle tree is implemented). In a complete Merkle tree for
> N = 2^n participants, the witness could contain the n hashes that allow
> to prove the value of the leaf, plus n bits to identify the path to the
> leaf (0/1 for 'left/right" child), since Script doesn't have enough
> opcodes to extract the bits from the leaf index.
>
> The data in the leaf can contain a commitment to all the information
> relevant for that participant (e.g.: their balance and pubkey, in a
> CoinPool construction).
>
> Then, the same witness can easily be reused to compute the new Merkle
> root after the data in the leaf is modified (for example, setting the
> amount to 0 for one participant).
>
>
> > A question that arises is how one would efficiently (in Script) prove
> > the inclusion/exclusion of the data in the commitment. One could
> > naively hash all the data twice during script execution (once for the
> > input, once for the output), but that is costly. It would be natural
> > to show merkle tree inclusion/exclusion in script, but perhaps there
> > are more efficient ways to prove it?
>
> A Merkle tree as described above commits to an entire vector that you
> can index positionally. That's quite versatile, and easier to handle
> than more complex constructions like accumulators with exclusion proofs.
>
> A Merkle proof for 2^7 = 128 participants requires about 8 hashes, so
> around 250 bytes in total of witness size; 2^10 = 1024 should bring that
> to the ballpark of 350 bytes.
>
> Best,
> Salvatore Ingala


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 60
*******************************************
