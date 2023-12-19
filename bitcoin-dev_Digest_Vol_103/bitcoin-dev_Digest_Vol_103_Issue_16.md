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

   1. Lamport scheme (not signature) to economize on L1 (yurisvb@pm.me)
   2. Kerckhoffian protocol for coercion-resistance in	non-shared
      custody (yurisvb@pm.me)
   3. Re: Lamport scheme (not signature) to economize on L1
      (Nagaev Boris)


----------------------------------------------------------------------

Message: 1
Date: Tue, 19 Dec 2023 14:07:23 +0000
From: yurisvb@pm.me
To: Nagaev Boris <bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Lamport scheme (not signature) to economize on
	L1
Message-ID:
	<ue8nChOuMtyW_JM-WxikLpWUSn9I99UHI5ukFVfLOEmQtCo4noetzyVKercbrwjr_EqNotDsR1QZ0oijMu11TO2jpEjlJF71OjLlNoZ-00Y=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Thank you for the question, Boris. That was an easy one:

Short answer is Lamport hashes are protected by long hash of key fingerprint an ECC (Schnorr or otherwise conventional) public-key, which is not published until first transaction. For clarity:

HL(.) = serial-work- and memory-*hard* hash with *short* digest (ex.: Argon2 with ~ 12 bytes output. "L" for "Lamport");
HC(.) = nonspecific representation of conventional, serial-work- and memory-*easy* hashes with *long* (brute-force-resistant) digest length. "C" for "Conventional";
KDF(.) = conventional key deriving function
ECCPUB = public key correspondent to ECCPRI
ECCPRI = KDF(seed, tag) //conventional BTC signing key (could be Schnorr instead)
LAMPPUB = HL(LAMPPRIi)
LAMPPRI = HL(seed, tag) //Though it is (more) feasible to crack a seed S that works as pre-image to LAMPRI, such seed can only be deemed valid if the public key correspondent to KDF(s) = ECCPUB, so ultimately, cracking seed is still as hard as cracking a conventional seed.
ADDR = H(ECCPUB, LAMPPUB) //Conventional BTC key fingerprinting with conventionally used hashes and their respective brute-force-resistant digest lengths
TX = plaintext transaction
LSIG = HL(TX, LAMPPRI)
COMMITMENT = Smart contract stating "This UTXO is frozen until one of the following happens: A) publishing of a L such that HL(TX,L) = LSIG before T2 in which case TX is deemed valid and executed, or B) T2 blocks from now, when miner of LSIG has gets F1+FF1, and the miner of COMMITMENT gets FC, both from UTXO"
BL = "Bundle of Lamport scheme" = (TX, LSIG)
BC = "Bundle of Commitment and Conventional Signing" = (COMMITMENT, ECCPRI(COMMITMENT), ECCPUB, LAMPPUB)	//LAMPPUB is added here to allow easy verification that ECCPUB corresponds to ADDR
BT = "Total Bundle" = (BL, BC)
F1 = fee offered to mine BL
FF1 = fine offered to miner of BL to compensate for delay
FC = fee offered to mine BC in case of default
T0 = Block height of broadcasting of BT
T1 = Block height owner should aim at broadcasting LAMPPRI  block ~ T0+1 to T0+6 blocks. This is to protect owner from dissensus (revealing LAMPPRI in a block and have it utilized to forge transaction in a competing block of same height).
T2 = Block height of expiration of commitment ~ T0+24 hours to T0+ a few days to protect user from execution of commitment being triggered by innocent unavailability.

>From ADDR alone, Miners, cannot forge a valid LSIG, nor try to ascertain LAMPPUB or LAMPPRI, because of pre-image-resistance of H(.) and brute-force resistance of ECCPUB before being published. The saving happens because, safe from T2 passing without LAMPRI being broadcasted, only BL and LAMPPR, and not BC, end up in Blockchain.

The proposed scheme, therefore allows for only 1 instance of Lamport schemed-based economic transaction, which has to be the first transaction of ADDR (because of publishing of ECCPUB). After this first transaction, ADDR is stil valid, just no longer able to issue transactions.

The proposed scheme, therefore, favors the good practice of non-address reuse.

YSVB

Sent with Proton Mail secure email.

On Tuesday, December 19th, 2023 at 1:45 AM, Nagaev Boris <bnagaev@gmail.com> wrote:


> On Mon, Dec 18, 2023 at 7:44?PM yurisvb@pm.me wrote:
> 

> > I beg to disagree: key owner broadcasts first bundle (let's call it this way) so that it is on any miner's best interest to include said bundle on their's attempted coinbase because they know if they don't any other competing miner will in the next block.
> 

> 

> What if an attacker broadcasts the first bundle? He spent a lot of
> time cracking the hash which is the part of the address in the
> proposed scheme. Then he cracked the second layer of hashing to have
> both hashes ready. If the utxo has enough sats, the attack is
> economically viable.
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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/ab67fa5f/attachment-0001.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/ab67fa5f/attachment-0001.sig>

------------------------------

Message: 2
Date: Tue, 19 Dec 2023 16:11:56 +0000
From: yurisvb@pm.me
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Kerckhoffian protocol for coercion-resistance
	in	non-shared custody
Message-ID:
	<dOT19vgpqOP1vRhXuxPbUfKMl7GyIH22j20OleZJYhXn_vc3To_oaqj1xM4nNKlw4Q3yr0aUU7U0TYuiwNZvLWxdMZ7w7aN6whxHzMBu8WQ=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Hello, colleagues

Since some of you seem to be enjoying my ideas and having a better time understanding them than most of investors I share them with, here goes a white paper of my proposed Kerckhoffian (non-obscure) protocol for coercion-resistance in self-(not shared-)custody
https://github.com/Yuri-SVB/Great_Wall/blob/main/executive_summary.md
https://linktr.ee/greatwallt3
On top of that, my proposed protocol is interoperable with others like multi-signature schemes, S4 (Shamir Secret Sharing Scheme) and inheritance protocols, and it is monetizable --- hence why the commercial wording. It can be made to work as a distributed service like LN.

I avail to also mention my proposed public-key cryptosystem based on the conjectured hardness of factorizing polynomials in finite fields:
https://github.com/Yuri-SVB/FFM-cryptography/blob/main/ffm_cryptosystem.pdf
https://linktr.ee/srvbcrypto
(still being written)

YSVB
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/dc9f39e9/attachment.html>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/dc9f39e9/attachment.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231219/dc9f39e9/attachment.sig>

------------------------------

Message: 3
Date: Tue, 19 Dec 2023 14:08:40 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: yurisvb@pm.me
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<CAFC_Vt5PcqqcREJ67Jzcg=K+Agd02a9f5uSit8LwkYHshbvF7A@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Tue, Dec 19, 2023 at 11:07?AM <yurisvb@pm.me> wrote:
>
> Thank you for the question, Boris. That was an easy one:
>
> Short answer is Lamport hashes are protected by long hash of key fingerprint an ECC (Schnorr or otherwise conventional) public-key, which is not published until first transaction. For clarity:
>
> HL(.) = serial-work- and memory-*hard* hash with *short* digest (ex.: Argon2 with ~ 12 bytes output. "L" for "Lamport");
> HC(.) = nonspecific representation of conventional, serial-work- and memory-*easy* hashes with *long* (brute-force-resistant) digest length. "C" for "Conventional";
> KDF(.) = conventional key deriving function
> ECCPUB = public key correspondent to ECCPRI
> ECCPRI = KDF(seed, tag) //conventional BTC signing key (could be Schnorr instead)
> LAMPPUB = HL(LAMPPRIi)
> LAMPPRI = HL(seed, tag) //Though it is (more) feasible to crack a seed S that works as pre-image to LAMPRI, such seed can only be deemed valid if the public key correspondent to KDF(s) = ECCPUB, so ultimately, cracking seed is still as hard as cracking a conventional seed.
> ADDR = H(ECCPUB, LAMPPUB) //Conventional BTC key fingerprinting with conventionally used hashes and their respective brute-force-resistant digest lengths
> TX = plaintext transaction
> LSIG = HL(TX, LAMPPRI)
> COMMITMENT = Smart contract stating "This UTXO is frozen until one of the following happens: A) publishing of a L such that HL(TX,L) = LSIG before T2 in which case TX is deemed valid and executed, or B) T2 blocks from now, when miner of LSIG has gets F1+FF1, and the miner of COMMITMENT gets FC, both from UTXO"
> BL = "Bundle of Lamport scheme" = (TX, LSIG)
> BC = "Bundle of Commitment and Conventional Signing" = (COMMITMENT, ECCPRI(COMMITMENT), ECCPUB, LAMPPUB)        //LAMPPUB is added here to allow easy verification that ECCPUB corresponds to ADDR
> BT = "Total Bundle" = (BL, BC)
> F1 = fee offered to mine BL
> FF1 = fine offered to miner of BL to compensate for delay
> FC = fee offered to mine BC in case of default
> T0 = Block height of broadcasting of BT
> T1 = Block height owner should aim at broadcasting LAMPPRI  block ~ T0+1 to T0+6 blocks. This is to protect owner from dissensus (revealing LAMPPRI in a block and have it utilized to forge transaction in a competing block of same height).
> T2 = Block height of expiration of commitment ~ T0+24 hours to T0+ a few days to protect user from execution of commitment being triggered by innocent unavailability.
>
> From ADDR alone, Miners, cannot forge a valid LSIG, nor try to ascertain LAMPPUB or LAMPPRI, because of pre-image-resistance of H(.) and brute-force resistance of ECCPUB before being published. The saving happens because, safe from T2 passing without LAMPRI being broadcasted, only BL and LAMPPR, and not BC, end up in Blockchain.
>
> The proposed scheme, therefore allows for only 1 instance of Lamport schemed-based economic transaction, which has to be the first transaction of ADDR (because of publishing of ECCPUB). After this first transaction, ADDR is stil valid, just no longer able to issue transactions.
>
> The proposed scheme, therefore, favors the good practice of non-address reuse.
>
> YSVB
>

Thank you for the great explanation, Yuri!

Let's make sure we are on the same page.

I calculated the on-chain footprint of signatures of the proposed
scheme and compared it with schnorr keys as are used in taproot.

Lamport scheme, the case no ECC signature is published:
 - output: 20 bytes. ADDR = H(ECCPUB, LAMPPUB)
 - input 1: LSIG (14 bytes)
 - input 2: ECCPUB, LAMPPRI (32+14=46). (ECCPUB is needed to verify
hashing to ADDR; LAMPPUB is not needed onchain, because it is a hash
of LAMPPRI.)
Total onchain footprint: 20+14+46=80 (bytes)
Is this correct?

Taproot:
 - output: 32 bytes (schnorr public key)
 - input: 64 bytes (schnorr signature)
Total: 32+64 = 96 (bytes)

Some additional space is needed in the lamport scheme case to address
T0 from T1 and to have T1 in the first place. Tx overhead is around 10
bytes and say 6 bytes for the reference. It looks, the footprint will
be the same.



-- 
Best regards,
Boris Nagaev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 16
********************************************
