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

   1. Re: Lamport scheme (not signature) to economize on L1
      (yurisvb@pm.me)


----------------------------------------------------------------------

Message: 1
Date: Tue, 19 Dec 2023 21:22:20 +0000
From: yurisvb@pm.me
To: Nagaev Boris <bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<HG9-9VDKRd3-0v0x9QP05_Cjyk9Y3UW-94A1RHsT3xMQYmb7Y6sk9-wTUlqVZzm6ACigM7aM-B6NB-z6jVCCXhQIGEYkEcBKryzP587FlIo=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Thank you for putting yourself through the working of carefully analyzing my proposition, Boris!

1) My demonstration concludes 12 bytes is still a very conservative figure for the hashes. I'm not sure where did you get the 14 bytes figure. This is 2*(14-12) = 4 bytes less.

2) Thank you for pointing out that ECCPUB is necessary. That's exactly right and I failed to realize that. To lessen the exposure, and the risk of miner of LSIG, it can be left to be broadcast together with LAMPPRI.

3) I avail to advocate for economizing down the fingerprint to just 128 bits for the weakest-link-principle, since 128 bits is a nearly ubiquitous standard, employed even by the majority of seeds. Not an argument against plain Schnorr, because Schnorr keys could use it too, but, compared with current implementations, we have that would be 20-16=4 bytes less.

4) [Again, argument against plain, because it cuts for both sides:] To economize even further, there is also the entropy-derivation cost trade-off of N times costlier derivation for log2(N) less bits. If applied to the Address, we could shave away another byte.

5) T0 is just the block height of burying of LSIG doesn't need to be buried. T2 can perfectly be hard-coded to always be the block equivalent of T0 + 48 hours (a reasonable spam to prevent innocent defaulting on commitment due to network unavailability). T1 is any value such as T0 < T1 < T2, (typically T1 <= T0+6) of user's choosing, to compromise between, on one hand, the convenience of unfreezing UTXO and having TX mining completed ASAP and, on the other, avoiding the risk of blockchain forking causing LAMPPRI to be accidentally leaked in the same block height as LSIG, which allows for signatures to be forged. So this is 16 bytes less.

Miners would keep record of unconfirmed BL's, because of the reward of mining either possible outcome of it (successful transaction or execution of commitment). Everything is paid for.

So, unless I'm forgetting something else, all other variables kept equal, we have 20 bytes lighter than Schnorr; and up to 25 bytes less the current implementation of Schnorr, if items 3 and 4 are implemented too. Already we have a reduction of between 21% and 26%, while, so far, nobody in the mailing list has disputed how 'outrageously' conservative the 12 bytes figure is.

Any other objections?

YSVB

Sent with Proton Mail secure email.

On Tuesday, December 19th, 2023 at 6:08 PM, Nagaev Boris <bnagaev@gmail.com> wrote:


> On Tue, Dec 19, 2023 at 11:07?AM yurisvb@pm.me wrote:
> 

> > Thank you for the question, Boris. That was an easy one:
> > 

> > Short answer is Lamport hashes are protected by long hash of key fingerprint an ECC (Schnorr or otherwise conventional) public-key, which is not published until first transaction. For clarity:
> > 

> > HL(.) = serial-work- and memory-hard hash with short digest (ex.: Argon2 with ~ 12 bytes output. "L" for "Lamport");
> > HC(.) = nonspecific representation of conventional, serial-work- and memory-easy hashes with long (brute-force-resistant) digest length. "C" for "Conventional";
> > KDF(.) = conventional key deriving function
> > ECCPUB = public key correspondent to ECCPRI
> > ECCPRI = KDF(seed, tag) //conventional BTC signing key (could be Schnorr instead)
> > LAMPPUB = HL(LAMPPRIi)
> > LAMPPRI = HL(seed, tag) //Though it is (more) feasible to crack a seed S that works as pre-image to LAMPRI, such seed can only be deemed valid if the public key correspondent to KDF(s) = ECCPUB, so ultimately, cracking seed is still as hard as cracking a conventional seed.
> > ADDR = H(ECCPUB, LAMPPUB) //Conventional BTC key fingerprinting with conventionally used hashes and their respective brute-force-resistant digest lengths
> > TX = plaintext transaction
> > LSIG = HL(TX, LAMPPRI)
> > COMMITMENT = Smart contract stating "This UTXO is frozen until one of the following happens: A) publishing of a L such that HL(TX,L) = LSIG before T2 in which case TX is deemed valid and executed, or B) T2 blocks from now, when miner of LSIG has gets F1+FF1, and the miner of COMMITMENT gets FC, both from UTXO"
> > BL = "Bundle of Lamport scheme" = (TX, LSIG)
> > BC = "Bundle of Commitment and Conventional Signing" = (COMMITMENT, ECCPRI(COMMITMENT), ECCPUB, LAMPPUB) //LAMPPUB is added here to allow easy verification that ECCPUB corresponds to ADDR
> > BT = "Total Bundle" = (BL, BC)
> > F1 = fee offered to mine BL
> > FF1 = fine offered to miner of BL to compensate for delay
> > FC = fee offered to mine BC in case of default
> > T0 = Block height of broadcasting of BT
> > T1 = Block height owner should aim at broadcasting LAMPPRI block ~ T0+1 to T0+6 blocks. This is to protect owner from dissensus (revealing LAMPPRI in a block and have it utilized to forge transaction in a competing block of same height).
> > T2 = Block height of expiration of commitment ~ T0+24 hours to T0+ a few days to protect user from execution of commitment being triggered by innocent unavailability.
> > 

> > From ADDR alone, Miners, cannot forge a valid LSIG, nor try to ascertain LAMPPUB or LAMPPRI, because of pre-image-resistance of H(.) and brute-force resistance of ECCPUB before being published. The saving happens because, safe from T2 passing without LAMPRI being broadcasted, only BL and LAMPPR, and not BC, end up in Blockchain.
> > 

> > The proposed scheme, therefore allows for only 1 instance of Lamport schemed-based economic transaction, which has to be the first transaction of ADDR (because of publishing of ECCPUB). After this first transaction, ADDR is stil valid, just no longer able to issue transactions.
> > 

> > The proposed scheme, therefore, favors the good practice of non-address reuse.
> > 

> > YSVB
> 

> 

> Thank you for the great explanation, Yuri!
> 

> Let's make sure we are on the same page.
> 

> I calculated the on-chain footprint of signatures of the proposed
> scheme and compared it with schnorr keys as are used in taproot.
> 

> Lamport scheme, the case no ECC signature is published:
> - output: 20 bytes. ADDR = H(ECCPUB, LAMPPUB)
> - input 1: LSIG (14 bytes)
> - input 2: ECCPUB, LAMPPRI (32+14=46). (ECCPUB is needed to verify
> hashing to ADDR; LAMPPUB is not needed onchain, because it is a hash
> of LAMPPRI.)
> Total onchain footprint: 20+14+46=80 (bytes)
> Is this correct?
> 

> Taproot:
> - output: 32 bytes (schnorr public key)
> - input: 64 bytes (schnorr signature)
> Total: 32+64 = 96 (bytes)
> 

> Some additional space is needed in the lamport scheme case to address
> T0 from T1 and to have T1 in the first place. Tx overhead is around 10
> bytes and say 6 bytes for the reference. It looks, the footprint will
> be the same.
> 

> 

> 

> --
> Best regards,
> Boris Nagaev
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/82cbfb17/attachment-0001.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/82cbfb17/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 17
********************************************
