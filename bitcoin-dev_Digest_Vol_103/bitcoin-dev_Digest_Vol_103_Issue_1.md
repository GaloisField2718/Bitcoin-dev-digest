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

   1. Re: A proposal for a "PSBT for descriptors" format (Brandon Black)


----------------------------------------------------------------------

Message: 1
Date: Thu, 30 Nov 2023 15:12:05 -0800
From: Brandon Black <freedom@reardencode.com>
To: SeedHammer Team <team@seedhammer.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] A proposal for a "PSBT for descriptors"
	format
Message-ID: <ZWkWxdFPhwqLtyfh@console>
Content-Type: text/plain; charset=us-ascii

Hi Seedhammer,

I think the goal of such a format should be that it is already a valid
PSBT, or can be trivially converted into one. Ideally, a coordinating
device can load the standardized descriptor file, add inputs (PSBTv2) or
unsigned TX (PSBTv1), and send it to compatible signing devices without
further modification.

Seems like the additions to BIP174 would be a PSBT_GLOBAL_DESCRIPTOR
with key of <birthblock>|<name> and value of the descriptor encoded as
proposed, and then PSBT_GLOBAL_KEY_NAME with key of <fingerprint>
and value of <name>.

Best,

--Brandon

On 2023-11-23 (Thu) at 22:25:43 +0000, SeedHammer Team via bitcoin-dev wrote:
> Hi,
> 
> At SeedHammer we're interested in standard, compact output descriptors to make
> self-contained metal engraved backups feasible. To that end, we're proposing a
> descriptor format based on the PSBT binary encoding. The format has not reached
> widespread consensus, never mind adoption, so at this point we're soliciting
> comments before formally proposing it as a BIP.
> 
> See [proposal], [implementation] and [playground] for details and examples.
> 
> The format is a binary and compact serialization specification for the
> [wallet-policies] BIP. Features:
> 
> - Based on the binary [BIP174] PSBT format, including re-using the compact
>   PSBT_GLOBAL_XPUB encoding for extended keys.
> - The descriptor itself is encoded in the same textual format as described
>   in BIPs 380-386 (+389).
> - Key references (always) use the wallet-policies format @<key-index>.
> - Miniscript is trivially supported, except inline keys are not allowed, and
>   pk(NAME) expressions are replaced with indexed (@<idx>) key references.
> - Metadata such as labels and birthdate blocks are encoded as PSBT
>   map entries.
> 
> Known issues:
> 
> - CBOR vs PSBT. Blockchain Commons believes[0] that a CBOR based format is better
>   because it is a widely used binary encoding standard, whereas we believe the
>   complexity of CBOR doesn't justify its cost compared to the PSBT encoding
>   already widely supported by wallet software.
> - The proposal specifies a separate header and magic; should the format instead be
>   an extension to the PSBT format?
> 
> Thanks,
> E
> 
> [proposal] https://github.com/BlockchainCommons/Research/issues/135
> [implementation] https://github.com/seedhammer/bip-serialized-descriptors
> [playground] https://go.dev/play/p/nouZlbbcEWt
> [wallet-policies] https://github.com/bitcoin/bips/blob/bb98f8017a883262e03127ab718514abf4a5e5f9/bip-wallet-policies.mediawiki
> [BIP174] https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
> 
> [0] https://github.com/BlockchainCommons/Research/issues/135#issuecomment-1789644032
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 1
*******************************************
