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

   1. Proposed BIP for MuSig2 PSBT Fields (Andrew Chow)
   2. Proposed BIP for MuSig2 Descriptors (Andrew Chow)
   3. Re: Refreshed BIP324 (Tim Ruffing)
   4. Re: Proposed BIP for MuSig2 PSBT Fields (Anthony Towns)
   5. Re: Proposed BIP for MuSig2 PSBT Fields (Andrew Chow)
   6. Re: Proposed BIP for MuSig2 PSBT Fields (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Tue, 10 Oct 2023 22:28:37 +0000
From: Andrew Chow <lists@achow101.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Proposed BIP for MuSig2 PSBT Fields
Message-ID: <c3aad7de-ec6d-407a-b33e-b52663523ef7@achow101.com>
Content-Type: text/plain; charset=utf-8

Hi All,

I've written up a BIP draft for MuSig2 PSBT fields. It can be viewed at 
https://github.com/achow101/bips/blob/musig2-psbt/bip-musig2-psbt.mediawiki.

This is based on this gist from Sanket: 
https://gist.github.com/sanket1729/4b525c6049f4d9e034d27368c49f28a6. 
There are a few notable differences:
- The participant pubkeys field is keyed by only the aggregate xonly key
- Participant pubkeys are compressed pubkeys rather than xonly.

Andrew



------------------------------

Message: 2
Date: Tue, 10 Oct 2023 22:30:21 +0000
From: Andrew Chow <lists@achow101.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Proposed BIP for MuSig2 Descriptors
Message-ID: <71971e91-c065-478e-8489-44cc4cdacca4@achow101.com>
Content-Type: text/plain; charset=utf-8

Hi All,

I've written up a BIP draft for MuSig2 descriptors. It can be viewed at 
https://github.com/achow101/bips/blob/musig2-descriptors/bip-musig2-descriptors.mediawiki.

Andrew



------------------------------

Message: 3
Date: Wed, 11 Oct 2023 22:52:52 +0200
From: Tim Ruffing <crypto@timruffing.de>
To: bitcoin-dev@lists.linuxfoundation.org
Cc: Dhruv M <dhruv@bip324.com>
Subject: Re: [bitcoin-dev] Refreshed BIP324
Message-ID:
	<1c32b9c17a7a3ad6646994335c69155b65ac4f8f.camel@timruffing.de>
Content-Type: text/plain; charset="UTF-8"

Hello,

We'd like to announce two recent updates to BIP324 ("Version 2 P2P
Encrypted Transport Protocol"). Some of these changes affect semantics
and some are backwards-incompatible.

While we are not aware of any implementations of BIP324 except the one
in Bitcoin Core (see https://github.com/bitcoin/bitcoin/issues/27634 ),
the purpose of the email is to inform anyone involved in other
implementation efforts. At this point, we don't expect any further
backwards-incompatible changes.

https://github.com/bitcoin/bips/pull/1496 did multiple small changes:
 * Incoming v1 connections are now detected based on first 16 bytes
   they sent (instead of 12), which improves accuracy. If the incoming
   v1 connection appears to come from a wrong network (due to non-
   matching "network magic" bytes), responders may now drop the
   connection immediately.
 * The BIP330 message types have been dropped from the short encodings
   list in the BIP. It feels like it shouldn't be BIP324's goal to
   predict future protocol improvements.

https://github.com/bitcoin/bips/pull/1498 introduced a backwards-
incompatible change:
 * The garbage authentication packet is removed by merging it with the
   version packet. This simplifies the protocol implementation by
   consolidating the states and removing the special case of "ignoring
   the ignore bit." The freedom to choose the contents of the garbage
   authentication packet has also been removed, leading to easier
   testing and implementation.

We also did some editorial improvements. The most recent revision of
the BIP324 can be found at:?

https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki

Best,
Dhruv, Tim, and Pieter

On Sat, 2022-10-08 at 12:59 +0000, Dhruv M wrote:
> Hi all,
> 
> We have refreshed the proposal for BIP324, a new bitcoin P2P protocol
> featuring opportunistic encryption, a mild bandwidth reduction, and
> the
> ability
> to negotiate upgrades before exchanging application messages. We'd
> like
> to invite community members to review the BIP[1] and the related
> Bitcoin
> Core
> code[2].
> 
> The proposal has a rich history[3]. The big changes since the last
> public
> appearance[4] are:
> 
> * Elligator-swift encoding for the pubkeys in the ECDH exchange to
> obtain a pseudorandom bytestream
> * x-only ECDH secret derivation
> * Transport versioning that allows for upgradability
> * Trafic shapability using decoy packets and a shapable handshake
> * Complete rewrite of the BIP text
> 
> We look forward to your review and comments.
> 
> -Dhruv, Tim and Pieter
> 
> 
> [1] BIP Pull Request: https://github.com/bitcoin/bips/pull/1378
> 
> [2] All historical and current PRs:
> https://bip324.com/sections/code-review/
> 
> [3] https://bip324.com/sections/bip-review/
> 
> [4] https://gist.github.com/dhruv/5b1275751bc98f3b64bcafce7876b489
> 
> 
> 


------------------------------

Message: 4
Date: Thu, 12 Oct 2023 09:47:58 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Andrew Chow <lists@achow101.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for MuSig2 PSBT Fields
Message-ID: <ZSc0Luwg3rpNvkfJ@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Tue, Oct 10, 2023 at 10:28:37PM +0000, Andrew Chow via bitcoin-dev wrote:
> I've written up a BIP draft for MuSig2 PSBT fields. It can be viewed at 
> https://github.com/achow101/bips/blob/musig2-psbt/bip-musig2-psbt.mediawiki.

I was hoping to see adaptor signature support in this; but it seems that's
also missing from BIP 327? Though libsecp256k1-zkp has implemented it:

 https://github.com/BlockstreamResearch/secp256k1-zkp/blob/master/include/secp256k1_musig.h
   (adaptor arg to process_nonce; adapt, and extract_adaptor functions)

 https://github.com/BlockstreamResearch/secp256k1-zkp/blob/master/src/modules/musig/musig.md#atomic-swaps

I would have expected the change here to support this to be:

  * an additional field to specify the adaptor, PSBT_IN_MUSIG2_PUB_ADAPTOR
    (optional, 33B compressed pubkey, 32B-hash-or-omitted), that signers
    have to take into account

  * an additional field to specify the adaptor secret,
    PSBT_IN_MUSIG2_PRIV_ADAPTOR (32B), added by a Signer role

  * PartialSigAgg should check if PUB_ADAPTOR is present, and if so,
    incorporate the value from PSBT_IN_MUSIG2_PRIV_ADAPTOR, failing if
    that isn't present

(Note that when using adaptor signatures, signers who don't know the
adaptor secret will want to ensure that the partial signatures provided by
signers who do/might know the secret are valid. But that depends on the
protocol, and isn't something that can be automated at the PSBT level,
I think)

Seems like it would be nice to have that specified asap, so that it can
be supported by all signers?

FWIW, "participant" is typoed a bunch ("particpant") and the tables are
hard to read: you might consider putting the description as a separate
row? eg:

 https://github.com/ajtowns/bips/blob/202310-table/bip-musig2-psbt.mediawiki 

Cheers,
aj



------------------------------

Message: 5
Date: Wed, 11 Oct 2023 23:59:16 +0000
From: Andrew Chow <lists@achow101.com>
To: Anthony Towns <aj@erisian.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for MuSig2 PSBT Fields
Message-ID: <5ebdc1ea-583e-472f-a7ff-6ae8976bf0fb@achow101.com>
Content-Type: text/plain; charset=utf-8

On 10/11/2023 07:47 PM, Anthony Towns wrote:
> On Tue, Oct 10, 2023 at 10:28:37PM +0000, Andrew Chow via bitcoin-dev wrote:
>> I've written up a BIP draft for MuSig2 PSBT fields. It can be viewed at
>> https://github.com/achow101/bips/blob/musig2-psbt/bip-musig2-psbt.mediawiki.
> 
> I was hoping to see adaptor signature support in this; but it seems that's
> also missing from BIP 327?

This is the first time I've heard of that, so it wasn't something that I 
considered adding to the BIP. Really the goal was to just be able to use 
BIP 327.

But that doesn't preclude a future BIP that specifies how to use adaptor 
signatures and to have additional PSBT fields for it. It doesn't look 
like those are mutually exclusive in any way or that the fields that 
I've proposed wouldn't still work.

I don't know enough about the topic to really say much on whether or how 
such fields would work.

> FWIW, "participant" is typoed a bunch ("particpant")and the tables are
> hard to read: you might consider putting the description as a separate
> row? eg:
> 
>   https://github.com/ajtowns/bips/blob/202310-table/bip-musig2-psbt.mediawiki

Yes, I've been making some minor fixes throughout the day, and I'll 
probably take your suggestion for the tables. Mediawiki tables are the 
bane of my existence.

Andrew



------------------------------

Message: 6
Date: Thu, 12 Oct 2023 17:39:32 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Andrew Chow <lists@achow101.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for MuSig2 PSBT Fields
Message-ID: <ZSeitCGbqX9paPro@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Wed, Oct 11, 2023 at 11:59:16PM +0000, Andrew Chow via bitcoin-dev wrote:
> On 10/11/2023 07:47 PM, Anthony Towns wrote:
> > On Tue, Oct 10, 2023 at 10:28:37PM +0000, Andrew Chow via bitcoin-dev wrote:
> >> I've written up a BIP draft for MuSig2 PSBT fields. It can be viewed at
> >> https://github.com/achow101/bips/blob/musig2-psbt/bip-musig2-psbt.mediawiki.
> > 
> > I was hoping to see adaptor signature support in this; but it seems that's
> > also missing from BIP 327?
> This is the first time I've heard of that, so it wasn't something that I 
> considered adding to the BIP. Really the goal was to just be able to use 
> BIP 327.

Yeah, makes sense.

The other related thing is anti-exfil; libwally's protocol for that
(for ecdsa sigs) is described at:

 https://wally.readthedocs.io/en/release_0.8.9/anti_exfil_protocol/
 https://github.com/BlockstreamResearch/secp256k1-zkp/blob/master/include/secp256k1_ecdsa_s2c.h

Though that would probably want to have a PSBT_IN_S2C_DATA_COMMITMENT
item provided before MUSIG2_PUB_NONCE was filled in, then PSBT_IN_S2C_DATA
and PSBT_IN_NONCE_TWEAK can be provided. (Those all need to have specific
relationships in order to be secure though)

> But that doesn't preclude a future BIP that specifies how to use adaptor 
> signatures and to have additional PSBT fields for it. It doesn't look 
> like those are mutually exclusive in any way or that the fields that 
> I've proposed wouldn't still work.

Yeah, it's just that it would be nice if musig capable signers were also
capable of handling s2c/anti-exfil and tweaks/adaptor-sigs immediately,
rather than it being a "wait for the next release" thing...

> I don't know enough about the topic to really say much on whether or how 
> such fields would work.

I think for signers who otherwise don't care about these features, the
only difference is that you add the tweak to the musig nonces before
hashing/signing, which is pretty straightforward. So I think, if it were
specced, it'd be an easy win. Definitely shouldn't be a blocker though.

Here's another idea for formatting the tables fwiw:
https://github.com/ajtowns/bips/blob/d8a90cff616d6e5839748a1b2a50d32947f30850/bip-musig2-psbt.mediawiki

Cheers,
aj



------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 7
*******************************************
