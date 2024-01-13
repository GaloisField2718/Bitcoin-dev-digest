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

   1. Re: Introducing a version field to BIP39 mnemonic	phrases (Leslie)


----------------------------------------------------------------------

Message: 1
Date: Sat, 13 Jan 2024 15:55:07 +0000
From: Leslie <0300dbdd1b@protonmail.com>
To: Pavol Rusnak <stick@satoshilabs.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Introducing a version field to BIP39
	mnemonic	phrases
Message-ID:
	<qasgf9QSlEKnsWipYSu7ABTqKQbqa7kHwSQl7yM8ihEO9Kivk9pMtnx9tsl6q1frnmCijbmr5w6TDMadip8PFd_6GoLGipbCSwymhlMBwU4=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Dear Pavol,

Thank you for your valuable perspective on the subject.
I fully appreciate the original design intentions of BIP39 and the importance of maintaining interoperability and simplicity.
However, I'd like to share some thoughts in light of the concerns you've raised.

Regarding the potential fragmentation of the ecosystem, there are instances where wallets use non-standard derivation paths, which can be a challenge for users in terms of fund recovery.
Introducing a versioned mnemonic phrase, in my view, wouldn't necessarily exacerbate this issue.
Instead, it might offer a more structured way to manage these variations.

In my proposal, I am not pushing for a change of the KDF.
Rather, I consider it as a possible route for future developments or adapting to emerging standards.
I understand and share your concerns about the implications of such changes, particularly in relation to hardware wallets.
I recognize the necessity of proceeding with caution to ensure that any modifications do not compromise the interoperability and practical utility that are central to the success of BIP39.
The goal is to initiate a discussion on evolving while preserving the integrity and core functionality of BIP39.

I advocate for the evolution of mnemonic phrases in line with the standards they aim to support.
This could include facilitating updates of versioned mnemonic phrases, by either changing the KDF or by omitting the 32-bit version field when deriving the seed.
Such flexibility could be essential for adapting to future needs and technological advancements.

Moreover, it's apparent that many users are already managing multiple mnemonics for different applications.
This reflects the varied needs and practices of users.
Developments like aezeed[1] or Electrum V2[2] also demonstrate that the standard BIP39 entropy might not always suffice for specific applications, leading to alternative standards being developed.
This reality underscores the need to consider ways to enhance the existing system to more effectively accommodate these evolving requirements.

In summary, while I hold deep respect for the fundamental principles of BIP39, I firmly believe that exploring the potential of versioned mnemonics can effectively address the dynamic nature of user practices and application demands, all while preserving the core strengths of the BIP39 standard.

References:
[1] (https://pkg.go.dev/github.com/lightningnetwork/lnd/aezeed#section-readme)
[2] (https://electrum.readthedocs.io/en/latest/seedphrase.html)

Best Regards,
Leslie

On Saturday, January 13th, 2024 at 15:12, Pavol Rusnak <stick@satoshilabs.com> wrote:

> Hi Leslie, hi list!
>
> BIP39 author here. Not having version was a design decision, not accidental omission.
>
> When designing BIP39 we were striving for maximum interoperability. There are thousands of BIP39 applications and all of them have 100% interoperable way how to share entropy using a single seed.
>
> If there was a version field involved in BIP39 allowing different key stretching methods, all these implementations would choose to implement only different subsets which would lead to interoperability disaster.
>
> To give some examples of what I mean:
> - there is no way hardware wallets would be able to keystretch using Argon2 or other methods that require lot of memory and/or CPU bandwidth
> - having version paves the way to proprietary key stretching algorithms
> BIP39 is the universal base layer for sharing entropy. Everything else is delegated to upper layers.
>
> Adding version that encodes derivation paths is making the scheme less future proof, not more future proof.
>
> Imagine you created the seed in 2014 that includes version that prescribes using BIP44 as a derivation path. Now everytime there is a new standard (Segwit, Compat Segwit, Taproot, etc.). You need to generate (and backup!) the new seed.
>
> What if you want to use the seed for Nostr? Lightning? Cashu? Ark? User would be forced to backup multiple seeds for every single application, leading to sloppy backups.
>
> With BIP39 you can just use the single seed for everything.
>
> ?
>
> Best Regards / S pozdravom,
>
> Pavol "Stick" Rusnak
> Co-Founder, SatoshiLabs
>
> On Thu 11. 1. 2024 at 6:17, Leslie via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> <pre>
>> BIP:
>> Layer: Applications
>> Title: Versioned BIP39 Mnemonic Phrases
>> Author: Leslie <0300dbdd1b@protonmail.com>
>> Status: None
>> Type: Standards Track
>> Created: 2024-01-10
>> </pre>
>>
>> ## Abstract
>>
>> This BIP proposes an enhancement to the BIP39 mnemonic phrases by introducing a version field.
>> The version field will be a 32-bit field, prepended to the entropy of the BIP39 mnemonic phrase.
>> The first 24 bits are for general purposes, and the subsequent 8 bits are for defining the version used.
>>
>> ## Motivation
>> The current implementation of BIP39 mnemonic phrases lacks a crucial feature: versioning.
>> This omission has been identified as a significant design flaw, affecting the robustness and future-proofness of the mnemonic phrase generation and usage.
>> Notable community members and projects have expressed concerns over this shortcoming:
>>
>>>The lack of versioning is a serious design flaw in this proposal. On this basis alone I would recommend against use of this proposal.
>>
>> \- [Greg Maxwell 2017-03-14](https://github.com/bitcoin/bips/wiki/Comments:BIP-0039/fd2ddb6d840c6a91c98a29146b9a62d6a65d03bf)
>>
>> Furthermore, the absence of a version number in BIP39 seed phrases poses risks and inefficiencies in wallet software development and backward compatibility:
>>
>>>BIP39 seed phrases do not include a version number. This means that software should always know how to generate keys and addresses. BIP43 suggests that wallet software will try various existing derivation schemes within the BIP32 framework. This is extremely inefficient and rests on the assumption that future wallets will support all previously accepted derivation methods. If, in the future, a wallet developer decides not to implement a particular derivation method because it is deprecated, then the software will not be able to detect that the corresponding seed phrases are not supported, and it will return an empty wallet instead. This threatens users funds.
>>>
>>>For these reasons, Electrum does not generate BIP39 seeds.
>>
>> \- [Electrum Documentation 2017-01-27](https://electrum.readthedocs.io/en/latest/seedphrase.html#motivation)
>>
>> The proposed BIP aims to address these concerns by introducing a version field in the BIP39 mnemonic phrases.
>> The introduction of versioning is expected to enhance the mnemonic's adaptability to future changes, improve the efficiency of wallet software in handling different derivation methods, and secure users funds by reducing the risk of incompatibilities between mnemonic phrases and wallet implementations.
>>
>> ## Generating the Mnemonic
>>
>> In this proposal, we build upon the structure of BIP39 to include a versioned enhancement in the mnemonic generation process. The mnemonic encodes entropy, as in BIP39, but with a flexible approach to the size of the initial entropy (ENT).
>>
>> ### Version Field Inclusion:
>>
>> 1. **Initial Entropy Generation:**
>> The initial entropy of ENT bits is generated, where ENT can be any size as long as it is a multiple of 32 bits.
>>
>> 2. **Version Field Prepending:**
>> A crucial addition to this process is the prepending of a 32-bit version field to the initial entropy. This field is composed of:
>> - The first 24 bits are reserved for general purposes, which can be utilized for various enhancements or specific wallet functionalities.
>> - The remaining 8 bits are designated for specifying the version of the BIP39 standard.
>>
>> 3. **Checksum Calculation:**
>> A checksum is generated following the BIP39 method: taking the first (ENT + VF ) / 32 bits of the SHA256 hash of the combined entropy (initial entropy plus the 32-bit version field). This checksum is then appended to the combined entropy.
>>
>> 4. **Concatenation and Splitting:**
>> The combined entropy, including the initial entropy, version field, and checksum, is split into groups of 11 bits. Each group of bits corresponds to an index in the BIP39 wordlist.
>>
>> 5. **Mnemonic Sentence Formation:**
>> The mnemonic sentence is formed by converting these 11-bit groups into words using the standard BIP39 wordlist.
>>
>> ## Compatibility Considerations
>>
>> - **Backward Compatibility:** Systems designed for BIP39, unaware of the 32-bit extension, will interpret the mnemonic as a 'Legacy' BIP39 phrase.
>> - **Forward Compatibility:** The versioning mechanism prepares systems for future modifications to the BIP39 standard, facilitating seamless integration.
>>
>> ## Dictionary Dependency
>>
>> Wallets will still require access to the predefined BIP39 dictionary to retrieve the version of the mnemonic seed and validate the checksum.
>>
>>> ? It's noteworthy that the BIP39 English wordlist includes specific words that software can use to identify the mnemonic's version number in a user-friendly manner, reducing dependence on the wordlist for version recognition.
>>>
>>> One way to achieve this is by assigning the first 22
>>> bits of the reserved field to match these words.
>>>
>>> 11110010110 11111111101 : version zero
>>> 11110010110 10011010101 : version one
>>> 11110010110 11101011101 : version two
>>> 11110010110 11100001000 : version three
>>> ...
>>> 11110010110 01101111001 : version hundred
>>
>> ## Changing Derivation Methods
>>
>> The introduction of mnemonic versioning provides the flexibility to adopt alternative entropy derivation methods in the future. While BIP39 currently uses PBKDF2 for key stretching, future versions could employ different mechanisms to meet evolving cryptographic standards and requirements.
>>
>>> ? Changing the derivation method in versioned mnemonics could lead to compatibility issues with older software.
>>
>> ## References
>> 1. [Bitcoin Improvement Proposals. BIP39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)2. [bip39-versioned](https://github.com/lukechilds/bip39-versioned)_______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240113/93e512ec/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 13
********************************************
