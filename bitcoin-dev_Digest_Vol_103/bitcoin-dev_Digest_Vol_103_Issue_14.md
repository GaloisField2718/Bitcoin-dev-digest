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
      (Sergio Demian Lerner)
   2. Re: Lamport scheme (not signature) to economize on L1
      (Nagaev Boris)
   3.  Lamport scheme (not signature) to economize on L1 (yurisvb@pm.me)


----------------------------------------------------------------------

Message: 1
Date: Mon, 18 Dec 2023 09:29:48 -0300
From: Sergio Demian Lerner <sergio.d.lerner@gmail.com>
To: yurisvb@pm.me,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<CAKzdR-qaN7sO62F38tm1ppEow=Oh-3A6kwsfRyts8U+LPXvTnQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Yuri,
While not exactly the same, the idea of using Lamport chains was analyzed
circa 2012 in the context of cryptocurrencies.
I proposed a new signature scheme called MAVE [1], and then a
cryptocurrency scheme called MAVEPAY [2] to reduce the size of signatures
to a minimum of 3 hash verifications per signature, assuming a blockchain
or time-stamping service.

Later there was a similar proposal by A. Miller called FawkesCoin [3]
(using "Guy Fawkes Protocol" [4] or fawkes signatures, for short).

regards

[1] https://bitslog.files.wordpress.com/2012/04/mave1.pdf
[2] https://bitslog.files.wordpress.com/2012/04/mavepay1.pdf
[3] https://link.springer.com/chapter/10.1007/978-3-319-12400-1_36
[4] R. J. Anderson, F. Bergadano, B. Crispo, J.-H. Lee, C. Manifavas, and
R. M. Needham. A new family of authentication protocols. Operating Systems
Review, 32(4):9?20, 1998.


On Mon, Dec 18, 2023 at 6:19?AM Yuri S VB via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Dear colleagues,
>
> After having mentioned it in a Twitter Space
> <https://twitter.com/i/spaces/1vOxwjWWOqdJB> a few moments ago, I felt
> the need to share the idea with you even just as a draft. Utilizing Lamport
> Scheme <https://en.wikipedia.org/wiki/S/KEY> (not signature
> <https://en.wikipedia.org/wiki/Lamport_signature>) for better
> byte-efficiency in L1:
>
>
>    1. Have signing keys consist of the current ECC key AND a Lamport
>    chain;
>    2. For signing of a transaction, broadcast a tuple consisting of
>       1. the plain transaction,
>       2. hash of the previous Lamport chain concatenated to the
>       transaction
>       3. commitment signed by ECC freezing its UTXO and promising that in
>       a few blocks time the pre image of hash will be published.
>    3. a and b (but not c) are buried in coinbase session of a block B1 by
>    miner M1;
>    4. If upon maturity, such pre-image is not broadcasted, signed
>    commitment is buried in the next block and executed. As a consequence,
>    frozen UTXO pays B1 for a and b being buried at M1's coinbase *and* miner
>    M2 for burying it [the commitment] in a block B2 subsequent to maturity;
>    5. If pre-image is broadcasted before maturity, it is buried in
>    another block B2', pays for itself, pays M1 for burying a adn b at B1 and
>    pays whatever else was determined in the plain transaction of item 2.a.
>
>
> The whole point is that, in the typical use case in which pre-image of
> hash is, in fact, successfully broadcasted before maturity, commitment, the
> only ECC signature in this protocol is discarded, and only two Lamport
> hashes end up being buried at L1.
>
> To push economy even further, we could implement a memory-hard hash like
> Argon2 to do the same entropy-processing trade-off already utilized for
> passwords, so we could have hashes of, say 12 bytes, making it 24 in total,
> down from 136 from ECC.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/77a79fbe/attachment-0001.html>

------------------------------

Message: 2
Date: Mon, 18 Dec 2023 13:45:15 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: yurisvb@pm.me,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<CAFC_Vt5xqhuXjNVeSGE2Pn=0N0MuB6pOnREzGhSQSpk+hTUUSg@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hey Yuri,

On Mon, Dec 18, 2023 at 6:19?AM Yuri S VB via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> down from 136 from ECC.

Schnorr signature has size 64 bytes (serialized format consists of x
coordinate of R and of s, 32 bytes each).

> The whole point is that, in the typical use case in which pre-image of hash is, in fact, successfully broadcasted before maturity, commitment, the only ECC signature in this protocol is discarded, and only two Lamport hashes end up being buried at L1.

Two SHA256 hashes are 64 bytes in total, the same as one schnorr signature.

> To push economy even further, we could implement a memory-hard hash like Argon2 to do the same entropy-processing trade-off already utilized for passwords, so we could have hashes of, say 12 bytes, making it 24 in total

12 bytes security for spending bitcoins is not enough, is it?

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 3
Date: Mon, 18 Dec 2023 22:43:48 +0000
From: yurisvb@pm.me
To: Nagaev Boris <bnagaev@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev]  Lamport scheme (not signature) to economize on
	L1
Message-ID:
	<1aHuuO-k0Qo7Bt2-Hu5qPFHXi4RgRASpf9hWshaypHtdN-N9jkubcvmf-aUcFEA6-7L9FNXoilIyydCs41eK4v67GVflEd9WIuEF9t5rE8w=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

I beg to disagree: key owner broadcasts first bundle (let's call it this way) so that it is on any miner's best interest to include said bundle on their's attempted coinbase because they know if they don't any other competing miner will in the next block.

Once more I think it's worth mentioning the principle of weakest link: if cracking this Lamport chain within the stipulated few blocks time is harder than the double-spending attack, by definition, it's (much!) more than hard enough.

Consider a 12 bytes = 96 bits Lamport hash link (Less than half a Schnorr signature). Assume a cracking power of one order of magnitude higher than the current global hash rate of say 10^21 H/s. Already our assumption is outrageously pessimistic for more that two reasons: 1) The whole premise of Bitcoin being secure is presumptive unfeasibility of that attack (weakest-link argument); 2) Memory-hard hashes, by definition, are ASIC-resistant in the first place (so, being less efficient than ASICS, the CPUs necessary to match that hashing power would be far *more* costly than today's total global mining hardware). In other words, we are giving away the hardness of the hash.

Let's assume a generous window of 1M seconds, so 10^27 hashes. Multiplying that by log2(10), we have shy of 2^89 hashes (actually it's 2^ 'shy of 89', but again: erring on the side of safety). That divided by our 2^96 possible pre-images gives a probability of approximately 2^-6 < 0.02. This doesn't sound very impressive, but an important thing to have in mind is that this attack would destroy utility only of its specific victim (owner of target UTXO), unlikely the 50%+epsilon attack, in which the adversary may block whomever they want from ever having a transaction mined. Again, we are giving away over 11 days for good measure to safeguard against loss of connection.

More importantly, the economic viability of that attack: if your UTXO has less than ~50 times the cost of that operation, which we could lower bound for, say, half of blocks rewards (again, generously assuming 100% ROI for mining). Let's be generous once again disregard mining fees, which would give us (block reward)*(seconds)/((1+ROI)*(second per block)*(prob. success)) = 6.25*10^6 / (2*600*0.02)BTC ~ 260416 BTC.

So mine is an argument of economic viability: clearly adversary's economy of scale is positive, and it doesn't make sense to consider an adversary with more scale than that necessary for double spending. Even at that unrealistically large scale, however, and even assuming your adversary would gain 1000 times more utility than what they make their victim loose, it would still be unworthy to conduct such attack to an UTXO of less than 1K BTC.

In retrospect, I'm beginning to think that 12 bytes is rather an overkill.

YSVB

Sent with Proton Mail secure email.

On Monday, December 18th, 2023 at 6:48 PM, Nagaev Boris <bnagaev@gmail.com> wrote:


> On Mon, Dec 18, 2023 at 2:22?PM yurisvb@pm.me wrote:
> 

> > Most Wallets implement BIP39 with 12 words, which corresponds to 128 bits of entropy + 4 of checksum (so really only 128 bits).
> > 

> > 2 times that would get even to one Schnorr signature, as you say.
> > Going lower than 128 per hash is, IMO admissible under the same premise of memory-hard hashes like Argon2, Scrypt, CryptoNight, Catena, Balloon Hashing, or Krypton8 (the latter of my authoring, a fully homomorphically encryptable memory-hard hash). You make hashing N times more time-costly under some conservative assumption and allow for the alleviation of log2(N) bits from your key. It's widely adopted in passwords (Argon2, for instance, being the 2015 Password Hash Competition) since human memorization of password is a critical weak link in security and UX. BIP39 itself resorts to PBKDF2 with 2048 iterations with the same goal, even though it's not memory-hard. But there is more:
> > 

> > By design, my proposed Lamport chain needs only to resist brute-force for a few blocks time, so key strength can be cheapened even further. Keep in mind that before its first transaction, the public-key of an address is not published, so the window of opportunity for brute-forcing a key with lower strength really only opens upon the broadcasting of the transaction, and closes within a few blocks time.
> 

> 

> IIRC, miner M1 is the only party who verifies the ECC signature in the
> proposed protocol. If M1 is malicious, he can crack the short hash of
> an address in advance (spending as much time as needed). He should do
> it twice to know the next two hashes. Then mines the first transaction
> (in which he steals coins from the address) with the first hash and
> then publish the second hash a few blocks later to finalize the theft.
> 

> > YSVB
> > 

> > Sent with Proton Mail secure email.
> > 

> > On Monday, December 18th, 2023 at 5:45 PM, Nagaev Boris bnagaev@gmail.com wrote:
> > 

> > > Hey Yuri,
> > 

> > > On Mon, Dec 18, 2023 at 6:19?AM Yuri S VB via bitcoin-dev
> > > bitcoin-dev@lists.linuxfoundation.org wrote:
> > 

> > > > down from 136 from ECC.
> > 

> > > Schnorr signature has size 64 bytes (serialized format consists of x
> > > coordinate of R and of s, 32 bytes each).
> > 

> > > > The whole point is that, in the typical use case in which pre-image of hash is, in fact, successfully broadcasted before maturity, commitment, the only ECC signature in this protocol is discarded, and only two Lamport hashes end up being buried at L1.
> > 

> > > Two SHA256 hashes are 64 bytes in total, the same as one schnorr signature.
> > 

> > > > To push economy even further, we could implement a memory-hard hash like Argon2 to do the same entropy-processing trade-off already utilized for passwords, so we could have hashes of, say 12 bytes, making it 24 in total
> > 

> > > 12 bytes security for spending bitcoins is not enough, is it?
> > 

> > > --
> > > Best regards,
> > > Boris Nagaev
> 

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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/9ce9ebd8/attachment.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/9ce9ebd8/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 14
********************************************
