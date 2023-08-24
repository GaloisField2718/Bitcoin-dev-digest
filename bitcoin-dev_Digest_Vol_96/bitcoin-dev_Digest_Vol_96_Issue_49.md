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

   1. Bitcoin Core 24.1 released (Michael Ford)
   2. Bitcoin Core 23.2 released (Michael Ford)


----------------------------------------------------------------------

Message: 1
Date: Fri, 19 May 2023 11:56:14 +0100
From: Michael Ford <fanquake@gmail.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin Core 24.1 released
Message-ID:
	<CAFyhPjVNQztgy-+Jrnhcd9qS=Uky3_m4LnO1NA+2=WCc0PzoRQ@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Bitcoin Core version 24.1 is now available from:

  <https://bitcoincore.org/bin/bitcoin-core-24.1/>

Or through BitTorrent:

  magnet:?xt=urn:btih:ebb58d7495a8aaed2f20ec4ce3e5ae27aff69529&dn=bitcoin-core-24.1&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftrakcer.bitcoin.sprovoost.nl%3A6969

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

### P2P

- #26878 I2P network optimizations
- #26909 net: prevent peers.dat corruptions by only serializing once
- #27608 p2p: Avoid prematurely clearing download state for other peers
- #27610 Improve performance of p2p inv to send queues

### RPC and other APIs

- #26515 rpc: Require NodeStateStats object in getpeerinfo
- #27279 doc: fix/improve warning helps in {create,load,unload,restore}wallet
- #27468 rest: avoid segfault for invalid URI

### Build System

- #26944 depends: fix systemtap download URL
- #27462 depends: fix compiling bdb with clang-16 on aarch64

### Wallet

- #26595 wallet: be able to specify a wallet name and passphrase to
migratewallet
- #26675 wallet: For feebump, ignore abandoned descendant spends
- #26679 wallet: Skip rescanning if wallet is more recent than tip
- #26761 wallet: fully migrate address book entries for
watchonly/solvable wallets
- #27053 wallet: reuse change dest when re-creating TX with avoidpartialspends
- #27080 wallet: Zero out wallet master key upon locking so it doesn't
persist in memory
- #27473 wallet: Properly handle "unknown" Address Type

### GUI changes

- gui#687 Load PSBTs using istreambuf_iterator rather than istream_iterator
- gui#704 Correctly limit overview transaction list

### Miscellaneous

- #26880 ci: replace Intel macOS CI job
- #26924 refactor: Add missing includes to fix gcc-13 compile error

Credits
=======

Thanks to everyone who directly contributed to this release:

- Andrew Chow
- Anthony Towns
- Hennadii Stepanov
- John Moffett
- Jon Atack
- Marco Falke
- Martin Zumsande
- Matthew Zipkin
- Michael Ford
- pablomartin4btc
- Sebastian Falbesoner
- Suhas Daftuar
- Thomas Nguyen
- Vasil Dimov

As well as to everyone that helped with translations on
[Transifex](https://www.transifex.com/bitcoin/bitcoin/).


------------------------------

Message: 2
Date: Fri, 19 May 2023 11:59:51 +0100
From: Michael Ford <fanquake@gmail.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin Core 23.2 released
Message-ID:
	<CAFyhPjWZsyWg3MOMc=9=U=3v4gwXQqQb8ZWOGvhfRXwptyV-rw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Bitcoin Core version 23.2 is now available from:

  <https://bitcoincore.org/bin/bitcoin-core-23.2/>

Or through BitTorrent:

  magnet:?xt=urn:btih:e672796b257f0d3d3043d9022c4df57b2c9f6ede&dn=bitcoin-core-23.2&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftrakcer.bitcoin.sprovoost.nl%3A6969

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

### P2P

- #26909 net: prevent peers.dat corruptions by only serializing once
- #27608 p2p: Avoid prematurely clearing download state for other peers
- #27610 Improve performance of p2p inv to send queues

### Build system

- #25436 build: suppress array-bounds errors in libxkbcommon
- #25763 bdb: disable Werror for format-security
- #26944 depends: fix systemtap download URL
- #27462 depends: fix compiling bdb with clang-16 on aarch64

### Miscellaneous

- #25444 ci: macOS task imrovements
- #26388 ci: Use macos-ventura-xcode:14.1 image for "macOS native" task
- #26924 refactor: Add missing includes to fix gcc-13 compile error

Credits
=======

Thanks to everyone who directly contributed to this release:

- Anthony Towns
- Hennadii Stepanov
- MacroFake
- Martin Zumsande
- Michael Ford
- Suhas Daftuar

As well as to everyone that helped with translations on
[Transifex](https://www.transifex.com/bitcoin/bitcoin/).


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 49
*******************************************
