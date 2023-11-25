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

   1. A proposal for a "PSBT for descriptors" format (SeedHammer Team)


----------------------------------------------------------------------

Message: 1
Date: Thu, 23 Nov 2023 22:25:43 +0000
From: SeedHammer Team <team@seedhammer.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] A proposal for a "PSBT for descriptors" format
Message-ID:
	<_pNFQS1xsa8HZF-9x3hk8EBZRfYAbzCAha1rKaFbwpfqMqjK51rGQspALrdYvB0R0r90iReLLsktJOfFowJG-wkX3E1NvPwtEQyMT95uo_4=@seedhammer.com>
	
Content-Type: text/plain; charset=utf-8

Hi,

At SeedHammer we're interested in standard, compact output descriptors to make
self-contained metal engraved backups feasible. To that end, we're proposing a
descriptor format based on the PSBT binary encoding. The format has not reached
widespread consensus, never mind adoption, so at this point we're soliciting
comments before formally proposing it as a BIP.

See [proposal], [implementation] and [playground] for details and examples.

The format is a binary and compact serialization specification for the
[wallet-policies] BIP. Features:

- Based on the binary [BIP174] PSBT format, including re-using the compact
  PSBT_GLOBAL_XPUB encoding for extended keys.
- The descriptor itself is encoded in the same textual format as described
  in BIPs 380-386 (+389).
- Key references (always) use the wallet-policies format @<key-index>.
- Miniscript is trivially supported, except inline keys are not allowed, and
  pk(NAME) expressions are replaced with indexed (@<idx>) key references.
- Metadata such as labels and birthdate blocks are encoded as PSBT
  map entries.

Known issues:

- CBOR vs PSBT. Blockchain Commons believes[0] that a CBOR based format is better
  because it is a widely used binary encoding standard, whereas we believe the
  complexity of CBOR doesn't justify its cost compared to the PSBT encoding
  already widely supported by wallet software.
- The proposal specifies a separate header and magic; should the format instead be
  an extension to the PSBT format?

Thanks,
E

[proposal] https://github.com/BlockchainCommons/Research/issues/135
[implementation] https://github.com/seedhammer/bip-serialized-descriptors
[playground] https://go.dev/play/p/nouZlbbcEWt
[wallet-policies] https://github.com/bitcoin/bips/blob/bb98f8017a883262e03127ab718514abf4a5e5f9/bip-wallet-policies.mediawiki
[BIP174] https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki

[0] https://github.com/BlockchainCommons/Research/issues/135#issuecomment-1789644032


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 33
********************************************
