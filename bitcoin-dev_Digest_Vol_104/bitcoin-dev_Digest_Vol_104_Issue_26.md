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

   1. Re: BIP process friction (Michael Folkson)
   2. Re: Compressed Bitcoin Transactions (Tom Briar)
   3. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Greg Tonoski)
   4. Re: MuSig2 derivation, descriptor, and PSBT field BIPs
      (Michael Folkson)


----------------------------------------------------------------------

Message: 1
Date: Fri, 19 Jan 2024 19:27:30 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID:
	<WBjioXYlG8LU31KNQAn_r2g7kDGuH4OPUzOhpUqvCM1W43sz70L2KcvHjmFzeBihDTRkXvDGUswJCAZlWitw5ChJYOj3CxW9f-cMmCX33cg=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Thanks for this Peter, really helpful. 

> It is a much more fundamental
standard than Ordinals or Taproot Assets, in the sense that transaction
replacement is expected to be used by essentially all wallets as all wallets
have to deal with fee-rate fluctuations; I do not think that Ordinals or
Taproot assets are appropriate BIP material due to their niche use-case.

Yes I'd personally lean towards this view too. Certainly when you go into alternative asset territory (e.g. Counterparty, Liquid (Network) assets, Taproot assets) it is moving away from what you can do with the Bitcoin asset/currency and into building a new ecosystem with a different asset/currency. I would agree that that should probably be out of scope for *Bitcoin* Improvement Proposals without having any particular opinion on the utility of any of those ecosystems.

> just the other day I ran into someone
that didn't know RBF Rule #6 existed, which Core added on top of BIP-125, and
had made a mistake in their safety analysis of a protocol due to that.

I suspected this might be the case but to actually have a data point to back that up (beyond I personally find it unnecessarily confusing and hard to follow) is helpful, thanks.

> Finally, I think the lesson to be learned here is that mempool policy is better
served by *living* documentation that gets updated to reflect the real world.
There's no easy way for someone to get up to speed on what mempool policy is
actually implemented, and more importantly, *why* it is implemented and what
trade-offs were made to get there. It's quite possible that this "living
documentation" requirement rules out the BIP process.

I get the "living", evolving point. Policy proposals are definitely different to say consensus proposals where assuming they are ever activated you'd expect them to stay static for the rest of Bitcoin's existence barring minor cleanups, clarifications etc. However, one possible addition in a new BIP 3 process would be the introduction of versioning for a particular BIP e.g. BIP 789 version 2 which would be more conducive to these evolving proposals such as policy proposals. You could then update a BIP without needing a new BIP number for every material update.

I'll wait to hear what Luke thinks on this. Beyond the friction concern I think improving the BIP process for consensus and policy proposals would be the biggest potential win for a BIP 3 update.

Thanks also to Kalle too for his 18 month stint as a BIP editor :)

--
Michael Folkson
Email: michaelfolkson at protonmail.com
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F


Learn about Bitcoin: https://www.youtube.com/@portofbitcoin


On Thursday, 18 January 2024 at 18:00, Peter Todd <pete@petertodd.org> wrote:


> On Wed, Jan 17, 2024 at 05:29:48PM +0000, Michael Folkson via bitcoin-dev wrote:
> 
> > Hey Luke
> > 
> > I'd be happy to pick up working on BIP 3 again ([0], [1]) in light of this issue and others that are repeatedly cropping up (e.g. confusion on the recommended flow for working on proposed consensus changes, when to open a pull request to bitcoin-inquisition, when to open a pull request to Core, when to include/exclude activation params etc).
> > 
> > I don't think there is much I personally disagree with you on with regards to BIPs but one issue where I do think there is disagreement is on whether proposed default policy changes can/should be BIPed.
> > 
> > I previously drafted this on proposed default policy changes [2]:
> > 
> > "To address problems such as pinning attacks on Lightning and multiparty protocols (e.g. vaults) there are and will continue to be draft proposals on changing the default policy rules in Bitcoin Core and/or alternative implementations. As these proposals are for default policy rules and not consensus rules there is absolutely no obligation for Bitcoin Core and/or alternative implementations to change their default policy rules nor users to run any particular policy rules (default or otherwise). The authors of these draft proposals are clearly recommending what they think the default policy rules should be and what policy rules users should run but it is merely a recommendation. There are a lot of moving parts, subtleties and complexities involved in designing default policy rules so any recommendation(s) to significantly upgrade default policy rules would benefit from being subject to a spec process. This would also aid the review of any policy related pull requests in Bitcoin Co
 re and/or alternative implementations. An interesting recent case study washttps://github.com/bitcoin/bitcoin/pull/22665and Bitcoin Core not implementing the exact wording of BIP 125 RBF. In this case (for various reasons) as a response Bitcoin Core just removed references to BIP 125 and started documenting the replacement to BIP 125 rules in the Bitcoin Core repo instead. However, it is my view that recommendations for default policy rules should be recommendations to all implementations, reviewed by Lightning and multiparty protocol developers (not just Bitcoin Core) and hence they would benefit from being standardized and being subject to a specification process. I will reiterate once again though that policy rules are not consensus rules. Consensus rules are much closer to an obligation as divergences from consensus rules risk the user being forked off the blockchain and could ultimately end up in network splits. This does not apply to policy rules."
> > 
> > Are you open to adjusting your stance on proposed policy changes being BIPed? I do think it really stunts work on proposed default policy changes and people's ability to follow work on these proposals when the specifications for them are littered all over the place. I've certainly struggled to follow the latest state of V3 policy proposals without clear reference points for the latest state of these proposals e.g. [3]. In addition some proposed consensus change BIPs are starting to want to include sections on policy (e.g. BIP345, OP_VAULT [4]) where it would be much better if they could just refer to a separate policy BIP rather than including proposals for both policy and consensus in the same BIP.
> 
> 
> BIP-125 is I think an interesting case study. It is a much more fundamental
> standard than Ordinals or Taproot Assets, in the sense that transaction
> replacement is expected to be used by essentially all wallets as all wallets
> have to deal with fee-rate fluctuations; I do not think that Ordinals or
> Taproot assets are appropriate BIP material due to their niche use-case.
> 
> The V3 proposal, and ephemeral anchors, would be expected to be used by a wide
> range of contracting protocols, most notably lightning. This isn't quite as
> broad usage as BIP-124 RBF. But it is close. And yes, Core making changes to
> what is essentially BIP125 has an impact: just the other day I ran into someone
> that didn't know RBF Rule #6 existed, which Core added on top of BIP-125, and
> had made a mistake in their safety analysis of a protocol due to that.
> 
> Meanwhile, engineering documentation on V3 is extremely lacking, with basics
> like worked through use-case examples not being available. We don't even have
> solid agreement let alone documentation on how Lightning channels are meant to
> use V3 transactions and what the trade-offs are. And that has lead to mistaken
> claims, such as overstating(1) the benefit V3 transactions in their current
> form have for transaction pinning.
> 
> I don't think V3 necessarily needs a formal BIP. But it would benefit from a
> proper engineering process where use-cases are actually worked out and analyzed
> properly.
> 
> Finally, I think the lesson to be learned here is that mempool policy is better
> served by living documentation that gets updated to reflect the real world.
> There's no easy way for someone to get up to speed on what mempool policy is
> actually implemented, and more importantly, why it is implemented and what
> trade-offs were made to get there. It's quite possible that this "living
> documentation" requirement rules out the BIP process.
> 
> 1) https://petertodd.org/2023/v3-txs-pinning-vulnerability
> 
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org


------------------------------

Message: 2
Date: Fri, 19 Jan 2024 21:09:35 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: Jonas Schnelli <dev@jonasschnelli.ch>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<xmXvUSue_zG2b5fAInP4nlZ6YSCuPDhDBX_s9WwS7prB7KeIEw_gEj6f9_2ysP2oUBdXcXxNE9SCmt0WOrx-EOEHl1s7G9_Xc8WzLXZVWw0=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Jonas,

As it turns out, most of our size savings come from eliminating unneeded hashes and public keys, which get recovered on decompression. gzip actually expands transactions due to the way it attempts to compress pseudorandom data, my numbers show a legacy transaction of 222 bytes being expanded to 267 bytes.

gzip can possibly shrink the 4-byte integers which have only a couple typical values, and can eliminate some of the "boilerplate" in the tx format, but that's pretty much it at the expense of expanding the signatures, public keys, and hashes.

And your absolutely right this would have to be done at the application layer in a V2-P2P encrypted traffic system.

Thanks-
Tom.


------------------------------

Message: 3
Date: Sun, 21 Jan 2024 18:14:14 +0100
From: Greg Tonoski <gregtonoski@gmail.com>
To: Nagaev Boris <bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAMHHROzkqCVJQc7uszmtATiWWSm=WAEa2QmSxhcevCQowCyb9w@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Wed, Jan 17, 2024 at 12:30?AM Nagaev Boris <bnagaev@gmail.com> wrote:
>
> Node operators are likely to put UTXO set to SSD and blocks to HDD.
> SSD is more expensive than HDD.

Again, the UTXO set size argument is irrelevant. A simple transaction
is at disadvantage even if it doesn't result in a change of UTXO set
size.

> It is aligned with the fact that
> people putting data into blockchain are financially motivated to put
> it into witness data, i.e. into HDD. If miners charge the same per 1
> byte in a transaction output and 1 byte in witness, then people
> putting data into blockchain could put it into transaction outputs
> (why not, if the price is the same), (...)

By the same token, "people putting data into blockchain are
financially" demotivated to put them into non-witness data (e.g.
outputs) - which make vast majority of a simple, genuine transaction.
As a result "blockchain" changes its nature and becomes full of
bloated witness data (e.g. a JPEG in a single transaction in a
"pathological" 4MB block) instead of simple, genuine transactions.

> inflating the UTXO set (...).

UTXO set inflates naturally as there are more and more participants.
Besides, blockspace price discrimination didn't stop it. Again, the
UTXO set size argument is irrelevant to the subject.


------------------------------

Message: 4
Date: Tue, 23 Jan 2024 12:12:35 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Christopher Allen <ChristopherA@lifewithalacrity.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, bitcoindev@groups.io
Subject: Re: [bitcoin-dev] MuSig2 derivation, descriptor, and PSBT
	field BIPs
Message-ID:
	<3PpTlvmcynhdlowdRZmbx8HBFe-hcaS408SL98B_0qe_6NF1tzaTBkG5xBLo656jvWJqgqQ7NM4YoZf9bvbqae6vk1uv3lsOujIseS4gE6U=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Christopher

In the absence of a response from someone who is working on MuSig2/FROST etc I did ask Tim Ruffing about the problems with using x-only pubkeys for MuSig2 etc in an (online) London Bitcoin Devs meetup [0] in 2022.

His response was:

"If you want to do more complex things, for example MuSig or more complex crypto then this bit is always a little pain in the ass. We can always get around this but whenever we do advanced stuff like tweaking keys, a lot of schemes involve tweaking keys, even Taproot itself involves tweaking, MuSig2 has key aggregation and so on. You always have to implicitly remember that bit because it is not explicitly there. You have to implicitly remember it sometimes. This makes specifications annoying. I don?t think it is a problem for security but for engineering it is certainly annoying. In hindsight it is not clear if we would make that decision again. I still think it is good because we save a byte but you can also say the increased engineering complexity is not worth it. At this point I can understand both points of view."

Hope this helps.

Thanks
Michael

[0]: https://btctranscripts.com/london-bitcoin-devs/2022-08-11-tim-ruffing-musig2/#a-retrospective-look-at-bip340

--
Michael Folkson
Email: michaelfolkson at [protonmail.com](http://protonmail.com/)
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F

Learn about Bitcoin: https://www.youtube.com/@portofbitcoin

On Tuesday, 16 January 2024 at 08:18, Christopher Allen via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> On Mon, Jan 15, 2024 at 4:28?PM Ava Chow via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> I've also made a change to the PSBT fields BIP where the aggregate
>> pubkey is included as a plain pubkey rather than as xonly. I think this
>> change is necessary for to make discovering derived keys easier. The
>> derivation paths for derived keys contain the fingerprint of the parent
>> (i.e. the aggregate pubkey) and the fingerprint requires the evenness
>> bit to be serialized. So the aggregate pubkey in the PSBT fields need to
>> contain that evenness information in order for something looking at only
>> the PSBT to be able to determine whether a key is derived from an
>> aggregate pubkey also specified in the PSBT.
>
> The topic of some challenges in using x-only pubkeys with FROST recently came up in a conversation that I didn't completely understand. It sounds like it may be related to this issue with MuSig2.
>
> What are the gotcha's in x-only keys with these multisig protocols? Can you explain a little more? Any other particular things do we need to be careful about with x-only pubkeys? I had mistakenly assumed the technique was just a useful trick, not that it might cause some problems in higher level protocols.
>
> Thanks!
>
> -- Christopher Allen
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240123/88b753fc/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 26
********************************************
