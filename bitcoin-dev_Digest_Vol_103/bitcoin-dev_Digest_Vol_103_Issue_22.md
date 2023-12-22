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
   2. Re: Swift Activation - CTV (Luke Dashjr)
   3. Re: Lamport scheme (not signature) to economize on L1
      (G. Andrew Stone)


----------------------------------------------------------------------

Message: 1
Date: Thu, 21 Dec 2023 16:07:27 +0000
From: yurisvb@pm.me
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Nagaev Boris
	<bnagaev@gmail.com>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<I11FZ_ZpfwpnQBh5hbBZMHsQt_cKwF9My49X4-MMRIYvaJEoIwta-GEaDNN1EtQxST4gQFAvqfOZElDvIpPrlAVknyN52IMnJKNy5kT8sUE=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

You are right to point out that my proposal was lacking defense against rainbow-table, because there is a simple solution for it:
To take nonces from recent blocks, say, T0-6, ..., T0-13, for salting LSIG, and ECCPUB to salt LAMPPUB. Salts don't need to be secret, only unknown by the builder of rainbow table while they made it, which is the case, since here we have 8*32=256 bits for LSIG, and the entropy of ECCPUB in the second.

With rainbow table out of our way, there is only brute-force analysis to mind. Honestly, Guess I should find a less 'outrageously generous' upper bound for adversary's model, than just assume they have a magic wand to convert SHA256 ASICS into CPU with the same hashrate for memory- and serial-work-hard hashes (therefore giving away hash hardness). That's because with such 'magic wand' many mining pools would, not only be capable of cracking 2^48 hashes far within the protocol's prescribed 48 hours, but also 2^64 within a block time, which would invalidate a lot of what is still in use today.

Please, allow me a few days to think that through.

YSVB

Sent with Proton Mail secure email.

On Wednesday, December 20th, 2023 at 10:33 PM, Nagaev Boris <bnagaev@gmail.com> wrote:


> On Tue, Dec 19, 2023 at 6:22?PM yurisvb@pm.me wrote:
>
> > Thank you for putting yourself through the working of carefully analyzing my proposition, Boris!
> >
> > 1) My demonstration concludes 12 bytes is still a very conservative figure for the hashes. I'm not sure where did you get the 14 bytes figure. This is 2*(14-12) = 4 bytes less.
>
>
> I agree. It should have been 12.
>
> > 2) Thank you for pointing out that ECCPUB is necessary. That's exactly right and I failed to realize that. To lessen the exposure, and the risk of miner of LSIG, it can be left to be broadcast together with LAMPPRI.
> >
> > 3) I avail to advocate for economizing down the fingerprint to just 128 bits for the weakest-link-principle, since 128 bits is a nearly ubiquitous standard, employed even by the majority of seeds. Not an argument against plain Schnorr, because Schnorr keys could use it too, but, compared with current implementations, we have that would be 20-16=4 bytes less.
>
>
> I think that the digest size for hash should be 2x key size for
> symmetric encryption. To find a collision (= break) for a hash
> function with digest size 128 bits one needs to calculate ~ 2^64
> hashes because of the birthday paradox.
>
> > 4) [Again, argument against plain, because it cuts for both sides:] To economize even further, there is also the entropy-derivation cost trade-off of N times costlier derivation for log2(N) less bits. If applied to the Address, we could shave away another byte.
> >
> > 5) T0 is just the block height of burying of LSIG doesn't need to be buried. T2 can perfectly be hard-coded to always be the block equivalent of T0 + 48 hours (a reasonable spam to prevent innocent defaulting on commitment due to network unavailability). T1 is any value such as T0 < T1 < T2, (typically T1 <= T0+6) of user's choosing, to compromise between, on one hand, the convenience of unfreezing UTXO and having TX mining completed ASAP and, on the other, avoiding the risk of blockchain forking causing LAMPPRI to be accidentally leaked in the same block height as LSIG, which allows for signatures to be forged. So this is 16 bytes less.
> >
> > Miners would keep record of unconfirmed BL's, because of the reward of mining either possible outcome of it (successful transaction or execution of commitment). Everything is paid for.
> >
> > So, unless I'm forgetting something else, all other variables kept equal, we have 20 bytes lighter than Schnorr; and up to 25 bytes less the current implementation of Schnorr, if items 3 and 4 are implemented too. Already we have a reduction of between 21% and 26%, while, so far, nobody in the mailing list has disputed how 'outrageously' conservative the 12 bytes figure is.
>
>
> 26% reduction of block space utilization would be great, but the price
> of relying on 12 bytes hashes (only need 2^48 hashes to find a
> collision) is too much for that, IMHO.
>
> Another consideration is about 12 byte hashes. Let's try to figure out
> if they are resistant to rainbow table attack by a large organization.
> Let's assume that the rainbow table has a chain length of 1024^3 (billion).
> What storage size is needed? 2^96 * 12 / 1024^3 = 900 exabytes.
> Both chain length and storage size seems prohibitively high for today,
> but tomorrow the hash function can be optimized, memory can be
> optimized, storage can become cheaper etc. And this attack may be
> affordable for state level attackers.
>
> > Any other objections?
> >
> > YSVB
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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231221/9f954fac/attachment-0001.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231221/9f954fac/attachment-0001.sig>

------------------------------

Message: 2
Date: Thu, 21 Dec 2023 20:05:12 -0500
From: Luke Dashjr <luke@dashjr.org>
To: alicexbt <alicexbt@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID: <2e113332-2cfd-73ec-0368-136728ceb31a@dashjr.org>
Content-Type: text/plain; charset=UTF-8; format=flowed

This IS INDEED an attack on Bitcoin. It does not activate CTV - it would 
(if users are fooled into using it) give MINERS the OPTION to activate 
CTV. Nobody should run this, and if it gets any traction, it would 
behoove the community to develop and run a "URSF" making blocks 
signalling for it invalid.

Luke


On 12/19/23 20:44, alicexbt via bitcoin-dev wrote:
> Hello World,
>
> Note: This is not an attack on bitcoin. This is an email with some text and links. Users can decide what works best for themselves. There is also scope for discussion about changing method or params.
>
> I want to keep it short and no energy left. I have explored different options for activation and this feels the safest at this point in 2023. I have not done any magic or innovation but updated activation params. If you agree with them, please run this client else build your own. Anyone who calls this attack and do not build alternative option is an attack in itself.
>
> It activates CTV which is simple covenant proposal and achieves what we expect it to. It is upgradeable.  I like simple things, at least to start with.
>
> Activation parameters:
>
> ```
>          consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].nStartTime = 1704067200;
>          consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].nTimeout = 1727740800;
>          consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].min_activation_height = 874874;
> ```
>
> I need payment pools and it does it for me. Apart from that it enables vaults, congestion control etc. We have more PoCs for CTV than we had for taproot and I understand it better.
>
> If you agree with me, please build and run this client before 01 Jan 2024 else we can discuss ordinals for next 5 years and activate something in 2028.
>
> Cheers
>
> /dev/fd0
> floppy disk guy
>
> Sent with Proton Mail secure email.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>


------------------------------

Message: 3
Date: Thu, 21 Dec 2023 23:52:08 -0500
From: "G. Andrew Stone" <g.andrew.stone@gmail.com>
To: yurisvb@pm.me,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<CAHUwRvuyhQDN5RF0ysMAJgWS2V7vv-3yHzKcLspk_HzQY=tt2Q@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Does this affect the security model WRT chain reorganizations?  In the
classic doublespend attack, an attacker can only redirect UTXOs that they
spent.  With this proposal, if I understand it correctly, an attacker could
redirect all funds that have "matured" (revealed the previous preimage in
the hash chain) to themselves.  The # blocks to maturity in your proposal
becomes the classic "embargo period" and every coin spent by anyone between
the fork point and the maturity depth is available to the attacker to
doublespend?

On Thu, Dec 21, 2023, 8:05?PM Yuri S VB via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> You are right to point out that my proposal was lacking defense against
> rainbow-table, because there is a simple solution for it:
> To take nonces from recent blocks, say, T0-6, ..., T0-13, for salting
> LSIG, and ECCPUB to salt LAMPPUB. Salts don't need to be secret, only
> unknown by the builder of rainbow table while they made it, which is the
> case, since here we have 8*32=256 bits for LSIG, and the entropy of ECCPUB
> in the second.
>
> With rainbow table out of our way, there is only brute-force analysis to
> mind. Honestly, Guess I should find a less 'outrageously generous' upper
> bound for adversary's model, than just assume they have a magic wand to
> convert SHA256 ASICS into CPU with the same hashrate for memory- and
> serial-work-hard hashes (therefore giving away hash hardness). That's
> because with such 'magic wand' many mining pools would, not only be capable
> of cracking 2^48 hashes far within the protocol's prescribed 48 hours, but
> also 2^64 within a block time, which would invalidate a lot of what is
> still in use today.
>
> Please, allow me a few days to think that through.
>
> YSVB
>
> Sent with Proton Mail secure email.
>
> On Wednesday, December 20th, 2023 at 10:33 PM, Nagaev Boris <
> bnagaev@gmail.com> wrote:
>
>
> > On Tue, Dec 19, 2023 at 6:22?PM yurisvb@pm.me wrote:
> >
> > > Thank you for putting yourself through the working of carefully
> analyzing my proposition, Boris!
> > >
> > > 1) My demonstration concludes 12 bytes is still a very conservative
> figure for the hashes. I'm not sure where did you get the 14 bytes figure.
> This is 2*(14-12) = 4 bytes less.
> >
> >
> > I agree. It should have been 12.
> >
> > > 2) Thank you for pointing out that ECCPUB is necessary. That's exactly
> right and I failed to realize that. To lessen the exposure, and the risk of
> miner of LSIG, it can be left to be broadcast together with LAMPPRI.
> > >
> > > 3) I avail to advocate for economizing down the fingerprint to just
> 128 bits for the weakest-link-principle, since 128 bits is a nearly
> ubiquitous standard, employed even by the majority of seeds. Not an
> argument against plain Schnorr, because Schnorr keys could use it too, but,
> compared with current implementations, we have that would be 20-16=4 bytes
> less.
> >
> >
> > I think that the digest size for hash should be 2x key size for
> > symmetric encryption. To find a collision (= break) for a hash
> > function with digest size 128 bits one needs to calculate ~ 2^64
> > hashes because of the birthday paradox.
> >
> > > 4) [Again, argument against plain, because it cuts for both sides:] To
> economize even further, there is also the entropy-derivation cost trade-off
> of N times costlier derivation for log2(N) less bits. If applied to the
> Address, we could shave away another byte.
> > >
> > > 5) T0 is just the block height of burying of LSIG doesn't need to be
> buried. T2 can perfectly be hard-coded to always be the block equivalent of
> T0 + 48 hours (a reasonable spam to prevent innocent defaulting on
> commitment due to network unavailability). T1 is any value such as T0 < T1
> < T2, (typically T1 <= T0+6) of user's choosing, to compromise between, on
> one hand, the convenience of unfreezing UTXO and having TX mining completed
> ASAP and, on the other, avoiding the risk of blockchain forking causing
> LAMPPRI to be accidentally leaked in the same block height as LSIG, which
> allows for signatures to be forged. So this is 16 bytes less.
> > >
> > > Miners would keep record of unconfirmed BL's, because of the reward of
> mining either possible outcome of it (successful transaction or execution
> of commitment). Everything is paid for.
> > >
> > > So, unless I'm forgetting something else, all other variables kept
> equal, we have 20 bytes lighter than Schnorr; and up to 25 bytes less the
> current implementation of Schnorr, if items 3 and 4 are implemented too.
> Already we have a reduction of between 21% and 26%, while, so far, nobody
> in the mailing list has disputed how 'outrageously' conservative the 12
> bytes figure is.
> >
> >
> > 26% reduction of block space utilization would be great, but the price
> > of relying on 12 bytes hashes (only need 2^48 hashes to find a
> > collision) is too much for that, IMHO.
> >
> > Another consideration is about 12 byte hashes. Let's try to figure out
> > if they are resistant to rainbow table attack by a large organization.
> > Let's assume that the rainbow table has a chain length of 1024^3
> (billion).
> > What storage size is needed? 2^96 * 12 / 1024^3 = 900 exabytes.
> > Both chain length and storage size seems prohibitively high for today,
> > but tomorrow the hash function can be optimized, memory can be
> > optimized, storage can become cheaper etc. And this attack may be
> > affordable for state level attackers.
> >
> > > Any other objections?
> > >
> > > YSVB
> >
> >
> >
> > --
> > Best regards,
> > Boris Nagaev_______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231221/3c2966a8/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 22
********************************************
