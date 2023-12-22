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

   1. Swift Activation - CTV (alicexbt)
   2. Re: Lamport scheme (not signature) to economize on L1
      (Nagaev Boris)
   3. libsecp256k1 v0.4.1 released (Jonas Nick)
   4. Re: Altruistic Rebroadcasting - A Partial Replacement Cycling
      Mitigation (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Wed, 20 Dec 2023 01:44:58 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<39ecOLU7GJPGc0zWZmGuaj-a4ANySfoRjwxoUoxP480kfRRc_fsPl9MvZDC-0vSfrO3jYraHVUyxWpcg7AFHRJkEJUERYdHZlzimOwql1j0=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hello World,

Note: This is not an attack on bitcoin. This is an email with some text and links. Users can decide what works best for themselves. There is also scope for discussion about changing method or params.

I want to keep it short and no energy left. I have explored different options for activation and this feels the safest at this point in 2023. I have not done any magic or innovation but updated activation params. If you agree with them, please run this client else build your own. Anyone who calls this attack and do not build alternative option is an attack in itself.

It activates CTV which is simple covenant proposal and achieves what we expect it to. It is upgradeable.  I like simple things, at least to start with.

Activation parameters: 

```
        consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].nStartTime = 1704067200;
        consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].nTimeout = 1727740800;
        consensus.vDeployments[Consensus::DEPLOYMENT_COVTOOLS].min_activation_height = 874874; 
```

I need payment pools and it does it for me. Apart from that it enables vaults, congestion control etc. We have more PoCs for CTV than we had for taproot and I understand it better.

If you agree with me, please build and run this client before 01 Jan 2024 else we can discuss ordinals for next 5 years and activate something in 2028.

Cheers

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.


------------------------------

Message: 2
Date: Wed, 20 Dec 2023 18:33:56 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: yurisvb@pm.me
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<CAFC_Vt6vqZkeenfrsqSj4T3+4+L2KMam0o0FeWJ4VzBEWE=HfA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Tue, Dec 19, 2023 at 6:22?PM <yurisvb@pm.me> wrote:
>
> Thank you for putting yourself through the working of carefully analyzing my proposition, Boris!
>
> 1) My demonstration concludes 12 bytes is still a very conservative figure for the hashes. I'm not sure where did you get the 14 bytes figure. This is 2*(14-12) = 4 bytes less.

I agree. It should have been 12.

> 2) Thank you for pointing out that ECCPUB is necessary. That's exactly right and I failed to realize that. To lessen the exposure, and the risk of miner of LSIG, it can be left to be broadcast together with LAMPPRI.
>
> 3) I avail to advocate for economizing down the fingerprint to just 128 bits for the weakest-link-principle, since 128 bits is a nearly ubiquitous standard, employed even by the majority of seeds. Not an argument against plain Schnorr, because Schnorr keys could use it too, but, compared with current implementations, we have that would be 20-16=4 bytes less.

I think that the digest size for hash should be 2x key size for
symmetric encryption. To find a collision (= break) for a hash
function with digest size 128 bits one needs to calculate ~ 2^64
hashes because of the birthday paradox.

> 4) [Again, argument against plain, because it cuts for both sides:] To economize even further, there is also the entropy-derivation cost trade-off of N times costlier derivation for log2(N) less bits. If applied to the Address, we could shave away another byte.
>
> 5) T0 is just the block height of burying of LSIG doesn't need to be buried. T2 can perfectly be hard-coded to always be the block equivalent of T0 + 48 hours (a reasonable spam to prevent innocent defaulting on commitment due to network unavailability). T1 is any value such as T0 < T1 < T2, (typically T1 <= T0+6) of user's choosing, to compromise between, on one hand, the convenience of unfreezing UTXO and having TX mining completed ASAP and, on the other, avoiding the risk of blockchain forking causing LAMPPRI to be accidentally leaked in the same block height as LSIG, which allows for signatures to be forged. So this is 16 bytes less.
>
> Miners would keep record of unconfirmed BL's, because of the reward of mining either possible outcome of it (successful transaction or execution of commitment). Everything is paid for.
>
> So, unless I'm forgetting something else, all other variables kept equal, we have 20 bytes lighter than Schnorr; and up to 25 bytes less the current implementation of Schnorr, if items 3 and 4 are implemented too. Already we have a reduction of between 21% and 26%, while, so far, nobody in the mailing list has disputed how 'outrageously' conservative the 12 bytes figure is.

26% reduction of block space utilization would be great, but the price
of relying on 12 bytes hashes (only need 2^48 hashes to find a
collision) is too much for that, IMHO.

Another consideration is about 12 byte hashes. Let's try to figure out
if they are resistant to rainbow table attack by a large organization.
Let's assume that the rainbow table has a chain length of 1024^3 (billion).
What storage size is needed? 2^96 * 12 / 1024^3 = 900 exabytes.
Both chain length and storage size seems prohibitively high for today,
but tomorrow the hash function can be optimized, memory can be
optimized, storage can become cheaper etc. And this attack may be
affordable for state level attackers.

> Any other objections?
>
> YSVB
>


-- 
Best regards,
Boris Nagaev


------------------------------

Message: 3
Date: Thu, 21 Dec 2023 17:31:49 +0000
From: Jonas Nick <jonasd.nick@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] libsecp256k1 v0.4.1 released
Message-ID: <9dacd6ec-d7c2-459a-8f6b-fb0c57e60584@gmail.com>
Content-Type: text/plain; charset=UTF-8; format=flowed

Hello,

Today we'd like to announce the release of version 0.4.1 of libsecp256k1:

     https://github.com/bitcoin-core/secp256k1/releases/tag/v0.4.1

This release slightly increases the speed of the ECDH operation and significantly enhances the performance of many library functions when using the default configuration on x86_64.

For a list of changes, see the CHANGELOG.md:

     https://github.com/bitcoin-core/secp256k1/blob/master/CHANGELOG.md


------------------------------

Message: 4
Date: Thu, 21 Dec 2023 21:59:04 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Altruistic Rebroadcasting - A Partial
	Replacement Cycling Mitigation
Message-ID:
	<CALZpt+Hy+ayawj38Bh3TLZqA3C=G-wGvy_nz9=_5S8-ZZiot7w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Peter,

> Obviously a local replacement cache is a possibility. The whole point of
my
> email is to show that a local replacement cache isn't necessarily needed,
as
> any alturistic party can implement that cache for all nodes.

Sure, note as soon as you start to introduce an altruistic party
rebroadcasting for everyone in the network, we're talking about a different
security model for time-sensitive second-layers. And unfortunately, one can
expect the same dynamics we're seeing with BIP157 filter servers, a handful
of altruistic nodes for a large swarm of clients.

> 1) That is trivially avoided by only broadcasting txs that meet the local
> mempool min fee, plus some buffer. There's no point to broadcasting txs
that
> aren't going to get mined any time soon.
>
> 2) BIP-133 feefilter avoids this as well, as Bitcoin Core uses the
feefilter
> P2P message to tell peers not to send transactions below a threshold fee
rate.
>
> https://github.com/bitcoin/bips/blob/master/bip-0133.mediawiki

I know we can introduce BIP-133 style of filtering here only the top % of
the block template is altruistically rebroadcast. I still think this is an
open question how a second-layer node would discover the "global" mempool
min fee, and note an adversary might inflate the top % of block template to
prevent rebroadcast of malicious HTLC-preimage.

> Did you actually read my email? I worked out the budget required in a
> reasonable worst case scenario:

Yes. I think my uncertainty lies in the fact that an adversary can
rebroadcast _multiple_ times the same UTXO amount under different txids,
occupying all your altruistic bandwidth. Your economic estimation makes an
assumption per-block (i.e 3.125 BTC / 10 minutes). Where it might be
pernicious is that an adversary should be able to reuse those 3.125 BTC of
value for each inter-block time.

Of course, you can introduce an additional rate-limitation per-UTXO, though
I think this is very unsure how this rate-limit would not introduce a new
pinning vector for "honest" counterparty transaction.

> Here, we're talking about an attacker that has financial resources high
enough
> to possibly do 51% attacks. And even in that scenario, storing the entire
> replacement database in RAM costs under $1000

> The reality is such an attack would probably be limited by P2P bandwidth,
not
> financial resources, as 2MB/s of tx traffic would likely leave mempools
in an
> somewhat inconsistent state across the network due to bandwidth
limitations.
> And that is *regardless* of whether or not anyone implements alturistic tx
> broadcasting.

Sure, I think we considered bandwidth limitations in the design of the
package relay. Though see my point above, the real difficulty in your
proposed design sounds to me in the ability to reuse the same UTXO
liquidity for an unbounded number of concurrent replacement transactions
exhausting all the altruistic bandwidth.

One can just use a 0.1 BTC UTXO and just fan-out 3.125 BTC of concurrent
replacement transactions from then. So I don't think the assumed adversary
financial resources are accurate.

I think the best long-term way to fix replacement cycling is still more in
the direction of things like:
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-December/022191.html

With the additional constraint of removing package malleability, where all
the feerate is coming from package self-contained fee-bumping reserves
UTXOs.

Best,
Antoine

Le dim. 17 d?c. 2023 ? 10:57, Peter Todd <pete@petertodd.org> a ?crit :

> On Fri, Dec 15, 2023 at 10:29:22PM +0000, Antoine Riard wrote:
> > Hi Peter,
> >
> > > Altruistic third parties can partially mitigate replacement cycling(1)
> > attacks
> > > by simply rebroadcasting the replaced transactions once the replacement
> > cycle
> > > completes. Since the replaced transaction is in fact fully valid, and
> the
> > > "cost" of broadcasting it has been paid by the replacement
> transactions,
> > it can
> > > be rebroadcast by anyone at all, and will propagate in a similar way to
> > when it
> > > was initially propagated. Actually implementing this simply requires
> code
> > to be
> > > written to keep track of all replaced transactions, and detect
> > opportunities to
> > > rebroadcast transactions that have since become valid again. Since any
> > > interested third party can do this, the memory/disk space requirements
> of
> > > keeping track of these replacements aren't important; normal nodes can
> > continue
> > > to operate exactly as they have before.
> >
> > I think there is an alternative to altruistic and periodic rebroadcasting
> > still solving replacement cycling at the transaction-relay level, namely
> > introducing a local replacement cache.
> >
> > https://github.com/bitcoin/bitcoin/issues/28699
> >
> > One would keep in bounded memory a list of all seen transactions, which
> > have entered our mempool at least once at current mempool min fee.
>
> Obviously a local replacement cache is a possibility. The whole point of my
> email is to show that a local replacement cache isn't necessarily needed,
> as
> any alturistic party can implement that cache for all nodes.
>
> > For the full-nodes which cannot afford extensive storage in face of
> > medium-liquidity capable attackers, could imagine replacement cache nodes
> > entering into periodic altruistic rebroadcast. This would introduce a
> > tiered hierarchy of full-nodes participating in transaction-relay. I
> think
> > such topology would be more frail in face of any sybil attack or scarce
> > inbound slots connections malicious squatting.
> >
> > The altruistic rebroadcasting default rate could be also a source of
> > amplification attacks, where there is a discrepancy between the feerate
> of
> > the rebroadcast traffic and the current dynamic mempool min fee of the
> > majority of network mempools. As such wasting bandwidth for everyone.
>
> 1) That is trivially avoided by only broadcasting txs that meet the local
> mempool min fee, plus some buffer. There's no point to broadcasting txs
> that
> aren't going to get mined any time soon.
>
> 2) BIP-133 feefilter avoids this as well, as Bitcoin Core uses the
> feefilter
> P2P message to tell peers not to send transactions below a threshold fee
> rate.
>
> https://github.com/bitcoin/bips/blob/master/bip-0133.mediawiki
>
> > Assuming some medium-liquidity or high-liquidity attackers might reveal
> any
> > mitigation as insufficient, as an unbounded number of replacement
> > transactions might be issued from a very limited number of UTXOs, all
> > concurrent spends. In the context of multi-party time-sensitive protocol,
> > the highest feerate spend of an "honest" counterparty might fall under
> the
> > lowest concurrent replacement spend of a malicious counterparty,
> occupying
> > all the additional replacement cache storage.
>
> Did you actually read my email? I worked out the budget required in a
> reasonable worst case scenario:
>
> > > Suppose the DoS attacker has a budget equal to 50% of the total block
> > > reward.
> > > That means they can spend 3.125 BTC / 10 minutes, or 520,833sats/s.
> > >
> > >     520,833 sats/s
> > >     -------------- = 2,083,332 bytes / s
> > >     0.25 sats/byte
> > >
> > > Even in this absurd case, storing a one day worth of replacements would
> > > require
> > > just 172GB of storage. 256GB of RAM costs well under $1000 these days,
> > > making
> > > altruistic rebroadcasting a service that could be provided to the
> network
> > > for
> > > just a few thousand dollars worth of hardware even in this absurd case.
>
> Here, we're talking about an attacker that has financial resources high
> enough
> to possibly do 51% attacks. And even in that scenario, storing the entire
> replacement database in RAM costs under $1000
>
> The reality is such an attack would probably be limited by P2P bandwidth,
> not
> financial resources, as 2MB/s of tx traffic would likely leave mempools in
> an
> somewhat inconsistent state across the network due to bandwidth
> limitations.
> And that is *regardless* of whether or not anyone implements alturistic tx
> broadcasting.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231221/f0328bc3/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 20
********************************************
