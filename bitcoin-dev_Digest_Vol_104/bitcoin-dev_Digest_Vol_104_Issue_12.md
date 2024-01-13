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

   1. Re: Introducing a version field to BIP39 mnemonic	phrases
      (Pavol Rusnak)
   2. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Greg Tonoski)


----------------------------------------------------------------------

Message: 1
Date: Sat, 13 Jan 2024 09:12:10 -0500
From: Pavol Rusnak <stick@satoshilabs.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,  Leslie
	<0300dbdd1b@protonmail.com>
Subject: Re: [bitcoin-dev] Introducing a version field to BIP39
	mnemonic	phrases
Message-ID:
	<CAF90AvksvDTUNGZNNfo7tB6iHMpkTDh1TWQ-noJamyY7OAPF0Q@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Leslie, hi list!

BIP39 author here. Not having version was a design decision, not accidental
omission.

When designing BIP39 we were striving for maximum interoperability. There
are thousands of BIP39 applications and all of them have 100% interoperable
way how to share entropy using a single seed.

If there was a version field involved in BIP39 allowing different key
stretching methods, all these implementations would choose to implement
only different subsets which would lead to interoperability disaster.

To give some examples of what I mean:
- there is no way hardware wallets would be able to keystretch using Argon2
or other methods that require lot of memory and/or CPU bandwidth
- having version paves the way to proprietary key stretching algorithms

BIP39 is the universal base layer for sharing entropy. Everything else is
delegated to upper layers.

Adding version that encodes derivation paths is making the scheme less
future proof, not more future proof.

Imagine you created the seed in 2014 that includes version that prescribes
using BIP44 as a derivation path. Now everytime there is a new standard
(Segwit, Compat Segwit, Taproot, etc.). You need to generate (and backup!)
the new seed.

What if you want to use the seed for Nostr? Lightning? Cashu? Ark? User
would be forced to backup multiple seeds for every single application,
leading to sloppy backups.

With BIP39 you can just use the single seed for everything.


?

Best Regards / S pozdravom,

Pavol "Stick" Rusnak
Co-Founder, SatoshiLabs


On Thu 11. 1. 2024 at 6:17, Leslie via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> <pre>
>   BIP:
>   Layer: Applications
>   Title: Versioned BIP39 Mnemonic Phrases
>   Author: Leslie <0300dbdd1b@protonmail.com>
>   Status: None
>   Type: Standards Track
>   Created: 2024-01-10
> </pre>
>
> ## Abstract
>
> This BIP proposes an enhancement to the BIP39 mnemonic phrases by
> introducing a version field.
> The version field will be a 32-bit field, prepended to the entropy of the
> BIP39 mnemonic phrase.
> The first 24 bits are for general purposes, and the subsequent 8 bits are
> for defining the version used.
>
> ## Motivation
> The current implementation of BIP39 mnemonic phrases lacks a crucial
> feature: versioning.
> This omission has been identified as a significant design flaw, affecting
> the robustness and future-proofness of the mnemonic phrase generation and
> usage.
> Notable community members and projects have expressed concerns over this
> shortcoming:
>
> >The lack of versioning is a serious design flaw in this proposal. On this
> basis alone I would recommend against use of this proposal.
>
> \- [Greg Maxwell 2017-03-14](
> https://github.com/bitcoin/bips/wiki/Comments:BIP-0039/fd2ddb6d840c6a91c98a29146b9a62d6a65d03bf
> )
>
>
> Furthermore, the absence of a version number in BIP39 seed phrases poses
> risks and inefficiencies in wallet software development and backward
> compatibility:
>
> >BIP39 seed phrases do not include a version number. This means that
> software should always know how to generate keys and addresses. BIP43
> suggests that wallet software will try various existing derivation schemes
> within the BIP32 framework. This is extremely inefficient and rests on the
> assumption that future wallets will support all previously accepted
> derivation methods. If, in the future, a wallet developer decides not to
> implement a particular derivation method because it is deprecated, then the
> software will not be able to detect that the corresponding seed phrases are
> not supported, and it will return an empty wallet instead. This threatens
> users funds.
> >
> >For these reasons, Electrum does not generate BIP39 seeds.
>
> \- [Electrum Documentation 2017-01-27](
> https://electrum.readthedocs.io/en/latest/seedphrase.html#motivation)
>
> The proposed BIP aims to address these concerns by introducing a version
> field in the BIP39 mnemonic phrases.
> The introduction of versioning is expected to enhance the mnemonic's
> adaptability to future changes, improve the efficiency of wallet software
> in handling different derivation methods, and secure users funds by
> reducing the risk of incompatibilities between mnemonic phrases and wallet
> implementations.
>
> ## Generating the Mnemonic
>
> In this proposal, we build upon the structure of BIP39 to include a
> versioned enhancement in the mnemonic generation process. The mnemonic
> encodes entropy, as in BIP39, but with a flexible approach to the size of
> the initial entropy (ENT).
>
> ### Version Field Inclusion:
>
> 1. **Initial Entropy Generation:**
>    The initial entropy of ENT bits is generated, where ENT can be any size
> as long as it is a multiple of 32 bits.
>
> 2. **Version Field Prepending:**
>    A crucial addition to this process is the prepending of a 32-bit
> version field to the initial entropy. This field is composed of:
>    - The first 24 bits are reserved for general purposes, which can be
> utilized for various enhancements or specific wallet functionalities.
>    - The remaining 8 bits are designated for specifying the version of the
> BIP39 standard.
>
> 3. **Checksum Calculation:**
>    A checksum is generated following the BIP39 method: taking the first
> (ENT + VF ) / 32 bits of the SHA256 hash of the combined entropy (initial
> entropy plus the 32-bit version field). This checksum is then appended to
> the combined entropy.
>
> 4. **Concatenation and Splitting:**
>    The combined entropy, including the initial entropy, version field, and
> checksum, is split into groups of 11 bits. Each group of bits corresponds
> to an index in the BIP39 wordlist.
>
> 5. **Mnemonic Sentence Formation:**
>    The mnemonic sentence is formed by converting these 11-bit groups into
> words using the standard BIP39 wordlist.
>
>
> ## Compatibility Considerations
>
> - **Backward Compatibility:** Systems designed for BIP39, unaware of the
> 32-bit extension, will interpret the mnemonic as a 'Legacy' BIP39 phrase.
> - **Forward Compatibility:** The versioning mechanism prepares systems for
> future modifications to the BIP39 standard, facilitating seamless
> integration.
>
> ## Dictionary Dependency
>
> Wallets will still require access to the predefined BIP39 dictionary to
> retrieve the version of the mnemonic seed and validate the checksum.
>
> > ? It's noteworthy that the BIP39 English wordlist includes specific
> words that software can use to identify the mnemonic's version number in a
> user-friendly manner, reducing dependence on the wordlist for version
> recognition.
> >
> > One way to achieve this is by assigning the first 22
> > bits of the reserved field to match these words.
> >
> >     11110010110 11111111101 : version zero
> >     11110010110 10011010101 : version one
> >     11110010110 11101011101 : version two
> >     11110010110 11100001000 : version three
> >     ...
> >     11110010110 01101111001 : version hundred
>
>
> ## Changing Derivation Methods
>
> The introduction of mnemonic versioning provides the flexibility to adopt
> alternative entropy derivation methods in the future. While BIP39 currently
> uses PBKDF2 for key stretching, future versions could employ different
> mechanisms to meet evolving cryptographic standards and requirements.
>
> > ? Changing the derivation method in versioned mnemonics could lead to
> compatibility issues with older software.
>
> ## References
> 1. [Bitcoin Improvement Proposals. BIP39: Mnemonic code for generating
> deterministic keys](
> https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
> 2. [bip39-versioned](https://github.com/lukechilds/bip39-versioned)
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240113/863330fb/attachment-0001.html>

------------------------------

Message: 2
Date: Sat, 13 Jan 2024 16:04:12 +0100
From: Greg Tonoski <gregtonoski@gmail.com>
To: Nagaev Boris <bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAMHHROxBqLrBCT-y4Va5=xe6JUqb=FPyEq2PJ7=JrpqmHOJd8Q@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Wed, Dec 27, 2023 at 8:06?PM Nagaev Boris <bnagaev@gmail.com> wrote:
>
> On Wed, Dec 27, 2023 at 2:26?PM Greg Tonoski via bitcoin-dev
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
> > As a result, there are incentives structure distorted and critical
> > inefficiencies/vulnerabilities (e.g. misallocation of block space,
> > blockspace value destruction, disincentivized simple transaction,
> > centralization around complex transactions originators).
> >
> > Price of blockspace should be the same for any data (1 byte = 1 byte,
> > irrespectively of location inside or outside of witness), e.g. 205/205
> > and 767/767 bytes in the examples above.
>
> Witness data does not contribute to utxo set. The discount on storing
> data in witness creates an incentive to store data exactly in the
> witness and not in the parts contributing to utxo set.
>
> $ du -sh blocks/ chainstate/
> 569G    blocks/
> 9.3G    chainstate/
>
> Witness data is part of the "blocks" directory which is not
> latency-critical and can be stored on a slow and cheap storage device.
> Directory "chainstate" contains the data needed to validate new
> transactions and should fit into a fast storage device otherwise
> initial block download takes weeks. It is important to maintain the
> incentives structure, resulting in a small chainstate.

I think that the argument "discount on storing data in witness creates
an incentive to store data exactly in the witness (...)" is
fallacious. The "witness discount" does not affect the cost of data
storage in a Bitcoin node. What the "witness discount" affects is the
priority of a transaction pending confirmation only. For example, a
SegWit type of transaction of size of 1MB is prioritized (by miners)
over a non-SegWit transaction of the same size and fee. "Segwit
discount" benefits bloated transactions and puts simple transactions
at disadvantage (demonstrated at
"https://gregtonoski.github.io/bitcoin/segwit-mispricing/comparison-of-costs.html"
and "https://gregtonoski.github.io/bitcoin/segwit-mispricing/Comparison_of_4MB_and_1.33MB_blocks_in_Bitcoin.pdf").

The Bitcoin fee is not charged per UTXO set size. It is not charged
from a node operator. Nodes are up and running independently of
Bitcoin fees.

Any relation between UTXO set size and discount would be artificial
and inefficient, wouldn't it?


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 12
********************************************
