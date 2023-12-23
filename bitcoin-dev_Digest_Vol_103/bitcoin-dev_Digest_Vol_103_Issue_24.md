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

   1. Re: Swift Activation - CTV (alicexbt)
   2. Re: Lamport scheme (not signature) to economize on L1
      (yurisvb@pm.me)
   3. Re: Scaling Lightning Safely With Feerate-Dependent	Timelocks
      (Eric Voskuil)


----------------------------------------------------------------------

Message: 1
Date: Fri, 22 Dec 2023 01:56:09 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Luke Dashjr <luke@dashjr.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<Tp6LkEd_YZUe-0sI-EXRmGTaq4Om2RSKIOUsXS0GIsYW5z_MFnicWPz2hB1KZYJ1mihv0KrJT8DmnuDr1RCcIpFM9jCOy82BvRJySkO7Im8=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Luke,

This is not the first time I am writing this but you keep ignoring it and threaten with URSF. Please build BIP 8 client with LOT=TRUE if you think its the best way to activate and share it so that users can run it.

I had created this branch specifically for it but needed help which I didn't get: https://github.com/xbtactivation/bitcoin/tree/bip8-ctv

Discussing trade-offs involved in different activation methods and providing options to users is not an attack.

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

On Friday, December 22nd, 2023 at 1:05 AM, Luke Dashjr <luke@dashjr.org> wrote:


> This IS INDEED an attack on Bitcoin. It does not activate CTV - it would
> (if users are fooled into using it) give MINERS the OPTION to activate
> CTV. Nobody should run this, and if it gets any traction, it would
> behoove the community to develop and run a "URSF" making blocks
> signalling for it invalid.
> 
> Luke
> 
> 
> On 12/19/23 20:44, alicexbt via bitcoin-dev wrote:
> 
> > Hello World,
> > 
> > Note: This is not an attack on bitcoin. This is an email with some text and links. Users can decide what works best for themselves. There is also scope for discussion about changing method or params.
> > 
> > I want to keep it short and no energy left. I have explored different options for activation and this feels the safest at this point in 2023. I have not done any magic or innovation but updated activation params. If you agree with them, please run this client else build your own. Anyone who calls this attack and do not build alternative option is an attack in itself.
> > 
> > It activates CTV which is simple covenant proposal and achieves what we expect it to. It is upgradeable. I like simple things, at least to start with.
> > 
> > Activation parameters:
> > 
> > `consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].nStartTime = 1704067200; consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].nTimeout = 1727740800; consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].min_activation_height = 874874;`
> > 
> > I need payment pools and it does it for me. Apart from that it enables vaults, congestion control etc. We have more PoCs for CTV than we had for taproot and I understand it better.
> > 
> > If you agree with me, please build and run this client before 01 Jan 2024 else we can discuss ordinals for next 5 years and activate something in 2028.
> > 
> > Cheers
> > 
> > /dev/fd0
> > floppy disk guy
> > 
> > Sent with Proton Mail secure email.
> > 
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Fri, 22 Dec 2023 15:32:38 +0000
From: yurisvb@pm.me
To: "G. Andrew Stone" <g.andrew.stone@gmail.com>, Nagaev Boris
	<bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<jGJvlLv4UL13U6aklzwkyRE4XRQtQSK-JZzpevPzyWQhQ4rU84I5fPDSdbtW7ehFzxkLtaOEenMMQAbHslH766qj9DGfb7QlwwXqjGsNRvU=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

There are three possible cryptanalysis to LAMPPRI in my scheme:

1.  From ADDR alone before T0-1 (to be precise, publishing of (TX, SIG));
2.  From ADDR and (TX, SIG) after T0-1 (to be precise, publishing of (TX, SIG));
3.  Outmine the rest of mining community starting from a disadvantage of not less than (T1-T0-1) after T1 (to be precise, at time of publishing of LAMPRI);

...which bring us back to my argument with Boris: There is something else we missed in our considerations, which you said yourself: *ironically, LAMPPUB is never published*.

We can have LAMPPUB be 1Mb or even 1Gb long aiming at having rate of collision in HL(.) be negligible (note this is perfectly adherent to the proposition of memory-hard-hash, and would have the additional benefit of allowing processing-storage trade-off). In this case, we really have:

For 1: a pre-image problem for a function 

f1: {k| k is a valid ECCPRI} X {l | l is a valid LAMPPRI} -> {a | a is in the format of a ADDR}
having as domain the Cartesian product of set of possible ECCPRIs with set of possible LAMPPRIs and counter domain, the set of possible ADDRs.

For 2: a pre-image problem for a function 

f2_(TX,ECCPUB): {l | l is 'a valid LAMPPRI'} -> {a | a is 'in the format of ADDRs'} X {LSIG}
(notice the nuance: {LSIG} means the singleton containing of only the specific LSIG that was actually public, not 'in the format of LSIGs').

Notice that, whatever advantage of 2 over 1 has to be compensated by the perspective of having the protocol be successfully terminated before the attack being carried out.

For 3: Equivalente of a double-spending attack with, in the worst case, not less than (T1-T0-1) blocks in advantage for the rest of the community.

When I have the time, I'll do the math on what is the entropy on each case, assuming ideal hashes, but taking for granted the approximation given by Boris, we would have half of size of ADDR as strength, not half of LAMPPRI, so mission accomplished!

Another ramification of that is we can conceive a multi-use version of this scheme, in which LAMPPRI is the ADDR resulting of a previous (ECCPUB, LAMPPUB) pair. The increased size of LAMPPRI would be compensated by one entire ADDR less in the blockchain. Namely, we'd have an extra marginal reduction of 12 bytes per use (possibly more, depending on how much more bytes we can economize given that added strength).

YSVB.

On Friday, December 22nd, 2023 at 5:52 AM, G. Andrew Stone <g.andrew.stone@gmail.com> wrote:


> Does this affect the security model WRT chain reorganizations? In the classic doublespend attack, an attacker can only redirect UTXOs that they spent. With this proposal, if I understand it correctly, an attacker could redirect all funds that have "matured" (revealed the previous preimage in the hash chain) to themselves. The # blocks to maturity in your proposal becomes the classic "embargo period" and every coin spent by anyone between the fork point and the maturity depth is available to the attacker to doublespend?
> 

> On Thu, Dec 21, 2023, 8:05?PM Yuri S VB via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 

> > You are right to point out that my proposal was lacking defense against rainbow-table, because there is a simple solution for it:
> > To take nonces from recent blocks, say, T0-6, ..., T0-13, for salting LSIG, and ECCPUB to salt LAMPPUB. Salts don't need to be secret, only unknown by the builder of rainbow table while they made it, which is the case, since here we have 8*32=256 bits for LSIG, and the entropy of ECCPUB in the second.
> > 

> > With rainbow table out of our way, there is only brute-force analysis to mind. Honestly, Guess I should find a less 'outrageously generous' upper bound for adversary's model, than just assume they have a magic wand to convert SHA256 ASICS into CPU with the same hashrate for memory- and serial-work-hard hashes (therefore giving away hash hardness). That's because with such 'magic wand' many mining pools would, not only be capable of cracking 2^48 hashes far within the protocol's prescribed 48 hours, but also 2^64 within a block time, which would invalidate a lot of what is still in use today.
> > 

> > Please, allow me a few days to think that through.
> > 

> > YSVB
> > 

> > Sent with Proton Mail secure email.
> > 

> > On Wednesday, December 20th, 2023 at 10:33 PM, Nagaev Boris <bnagaev@gmail.com> wrote:
> > 

> > 

> > > On Tue, Dec 19, 2023 at 6:22?PM yurisvb@pm.me wrote:
> > >
> > > > Thank you for putting yourself through the working of carefully analyzing my proposition, Boris!
> > > >
> > > > 1) My demonstration concludes 12 bytes is still a very conservative figure for the hashes. I'm not sure where did you get the 14 bytes figure. This is 2*(14-12) = 4 bytes less.
> > >
> > >
> > > I agree. It should have been 12.
> > >
> > > > 2) Thank you for pointing out that ECCPUB is necessary. That's exactly right and I failed to realize that. To lessen the exposure, and the risk of miner of LSIG, it can be left to be broadcast together with LAMPPRI.
> > > >
> > > > 3) I avail to advocate for economizing down the fingerprint to just 128 bits for the weakest-link-principle, since 128 bits is a nearly ubiquitous standard, employed even by the majority of seeds. Not an argument against plain Schnorr, because Schnorr keys could use it too, but, compared with current implementations, we have that would be 20-16=4 bytes less.
> > >
> > >
> > > I think that the digest size for hash should be 2x key size for
> > > symmetric encryption. To find a collision (= break) for a hash
> > > function with digest size 128 bits one needs to calculate ~ 2^64
> > > hashes because of the birthday paradox.
> > >
> > > > 4) [Again, argument against plain, because it cuts for both sides:] To economize even further, there is also the entropy-derivation cost trade-off of N times costlier derivation for log2(N) less bits. If applied to the Address, we could shave away another byte.
> > > >
> > > > 5) T0 is just the block height of burying of LSIG doesn't need to be buried. T2 can perfectly be hard-coded to always be the block equivalent of T0 + 48 hours (a reasonable spam to prevent innocent defaulting on commitment due to network unavailability). T1 is any value such as T0 < T1 < T2, (typically T1 <= T0+6) of user's choosing, to compromise between, on one hand, the convenience of unfreezing UTXO and having TX mining completed ASAP and, on the other, avoiding the risk of blockchain forking causing LAMPPRI to be accidentally leaked in the same block height as LSIG, which allows for signatures to be forged. So this is 16 bytes less.
> > > >
> > > > Miners would keep record of unconfirmed BL's, because of the reward of mining either possible outcome of it (successful transaction or execution of commitment). Everything is paid for.
> > > >
> > > > So, unless I'm forgetting something else, all other variables kept equal, we have 20 bytes lighter than Schnorr; and up to 25 bytes less the current implementation of Schnorr, if items 3 and 4 are implemented too. Already we have a reduction of between 21% and 26%, while, so far, nobody in the mailing list has disputed how 'outrageously' conservative the 12 bytes figure is.
> > >
> > >
> > > 26% reduction of block space utilization would be great, but the price
> > > of relying on 12 bytes hashes (only need 2^48 hashes to find a
> > > collision) is too much for that, IMHO.
> > >
> > > Another consideration is about 12 byte hashes. Let's try to figure out
> > > if they are resistant to rainbow table attack by a large organization.
> > > Let's assume that the rainbow table has a chain length of 1024^3 (billion).
> > > What storage size is needed? 2^96 * 12 / 1024^3 = 900 exabytes.
> > > Both chain length and storage size seems prohibitively high for today,
> > > but tomorrow the hash function can be optimized, memory can be
> > > optimized, storage can become cheaper etc. And this attack may be
> > > affordable for state level attackers.
> > >
> > > > Any other objections?
> > > >
> > > > YSVB
> > >
> > >
> > >
> > > --
> > > Best regards,
> > > Boris Nagaev_______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231222/0fe5dd0c/attachment-0001.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231222/0fe5dd0c/attachment-0001.sig>

------------------------------

Message: 3
Date: Fri, 22 Dec 2023 23:09:15 -0500
From: Eric Voskuil <eric@voskuil.org>
To: jlspc <jlspc@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: lightning-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent	Timelocks
Message-ID: <6B73AF52-FB69-45A3-92BC-CC09204DB64D@voskuil.org>
Content-Type: text/plain; charset="us-ascii"

An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231222/eb8d0a53/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 24
********************************************
