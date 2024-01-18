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

   1. Re: Compressed Bitcoin Transactions (Jonas Schnelli)
   2. Re: BIP process friction (Michael Folkson)


----------------------------------------------------------------------

Message: 1
Date: Thu, 18 Jan 2024 10:24:02 +0100
From: Jonas Schnelli <dev@jonasschnelli.ch>
To: Tom Briar <tombriar11@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID: <A1A794D6-E465-4F45-BF67-EB24B2CB9773@jonasschnelli.ch>
Content-Type: text/plain;	charset=utf-8

One point to add here is that, while V1 non-encrypted p2p traffic could be compressed on a different OSI layer in theory, v2 encrypted traffic ? due to its pseudorandom nature ? will likely have no size savings and thus need to be compressed on the application layer with a proposal like this.

Would be nice to see size comparison of this compression proposal vs LZO/gzip compression of legacy transaction encoding.

A possible advantage of this proposal is that it could save more space with less CPU impact, which might be important for block propagation.

Previous discussion about compressing blocks before sending them:
https://github.com/bitcoin/bitcoin/pull/6973

/jonas

> Am 16.01.2024 um 18:08 schrieb Tom Briar via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>:
> 
> Hi,
> 
> In addition to the use cases listed in the schema, such as steganography, satellite, and radio broadcast, an application can be made for Peer-to-peer communication between Bitcoin nodes. Except when compressing the Txid/Vout, which is optional, Transactions can gain up to 30% size savings while still being completely reversible. Furthermore, in a BIP-324 world, these savings are nontrivial.
> 
> BIP-324: https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki
> Compressed Transaction Schema: compressed_transactions.md
> 
> Thanks-
> Tom.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev



------------------------------

Message: 2
Date: Wed, 17 Jan 2024 17:29:48 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Luke Dashjr <luke@dashjr.org>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID:
	<6ZZYFympMLvwZ3otE_ebPh3wAuPFYb1BKL_3O_NrlQYKfsAJNlobGrZQjK23BxNeIdJ_8x_SAhgF_po1qO68MI_XONG7aPsnEL45y8SNndQ=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hey Luke

I'd be happy to pick up working on BIP 3 again ([0], [1]) in light of this issue and others that are repeatedly cropping up (e.g. confusion on the recommended flow for working on proposed consensus changes, when to open a pull request to bitcoin-inquisition, when to open a pull request to Core, when to include/exclude activation params etc).

I don't think there is much I personally disagree with you on with regards to BIPs but one issue where I do think there is disagreement is on whether proposed default policy changes can/should be BIPed.

I previously drafted this on proposed default policy changes [2]:

"To address problems such as pinning attacks on Lightning and multiparty protocols (e.g. vaults) there are and will continue to be draft proposals on changing the default policy rules in Bitcoin Core and/or alternative implementations. As these proposals are for default policy rules and **not** consensus rules there is absolutely no obligation for Bitcoin Core and/or alternative implementations to change their default policy rules nor users to run any particular policy rules (default or otherwise). The authors of these draft proposals are clearly recommending what they think the default policy rules should be and what policy rules users should run but it is merely a recommendation. There are a lot of moving parts, subtleties and complexities involved in designing default policy rules so any recommendation(s) to significantly upgrade default policy rules would benefit from being subject to a spec process. This would also aid the review of any policy related pull requests in Bitcoin Co
 re and/or alternative implementations. An interesting recent case study washttps://github.com/bitcoin/bitcoin/pull/22665and Bitcoin Core not implementing the exact wording of BIP 125 RBF. In this case (for various reasons) as a response Bitcoin Core just removed references to BIP 125 and started documenting the replacement to BIP 125 rules in the Bitcoin Core repo instead. However, it is my view that recommendations for default policy rules should be recommendations to all implementations, reviewed by Lightning and multiparty protocol developers (not just Bitcoin Core) and hence they would benefit from being standardized and being subject to a specification process. I will reiterate once again though that policy rules are **not** consensus rules. Consensus rules are much closer to an obligation as divergences from consensus rules risk the user being forked off the blockchain and could ultimately end up in network splits. This does not apply to policy rules."

Are you open to adjusting your stance on proposed policy changes being BIPed? I do think it really stunts work on proposed default policy changes and people's ability to follow work on these proposals when the specifications for them are littered all over the place. I've certainly struggled to follow the latest state of V3 policy proposals without clear reference points for the latest state of these proposals e.g. [3]. In addition some proposed consensus change BIPs are starting to want to include sections on policy (e.g. BIP345, OP_VAULT [4]) where it would be much better if they could just refer to a separate policy BIP rather than including proposals for both policy and consensus in the same BIP.

Thanks for your long and continued work on the BIP process. It is thankless work and we don't see the alternative futures where all sorts of garbage was merged and given BIP numbers because the BIP editors just merged everything without looking at it and not caring about quality standards.

Thanks
Michael

[0]: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019412.html
[1]: https://github.com/bitcoin/bips/wiki/BIP-Process-wishlist
[2]: https://github.com/bitcoin/bips/wiki/BIP-Process-wishlist#default-policy-changes-eg-v3-a-recommendation-but-not-an-obligation-for-bitcoin-implementations
[3]: https://bitcoin.stackexchange.com/questions/117315/what-and-where-are-the-current-status-of-the-bip-125-replacement-the-v3-policy
[4]: https://github.com/bitcoin/bips/pull/1421

--
Michael Folkson
Email: michaelfolkson at [protonmail.com](http://protonmail.com/)
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F

Learn about Bitcoin: https://www.youtube.com/@portofbitcoin

On Wednesday, 17 January 2024 at 16:45, Luke Dashjr via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> Perhaps a BIP 3 is in order, but most of the real issue is simply a matter of volunteer time.
>
> AJ's attempt to conflate that with his own personal disagreements with how BIPs have always worked, is unrelated.
>
> Luke
>
> On 1/17/24 01:55, Christopher Allen via bitcoin-dev wrote:
>
>> On Tue, Jan 16, 2024 at 6:43?PM Anthony Towns via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>>
>>> If people want to use it for bitcoin-related proposals that don't have
>>> anything to do with inquisition, that's fine; I'm intending to apply the
>>> policies I think the BIPs repo should be using, so feel free to open a PR,
>>> even if you already know I think your idea is BS on its merits. If someone
>>> wants to write an automatic-merge-bot for me, that'd also be great.
>>>
>>> If someone wants to reform the BIPs repo itself so it works better,
>>> that'd be even better, but I'm not volunteering for that fight.
>>
>> I've no idea how to reform BIPs, but we have a similar problem with the Blockchain Commons Research (BCR) vs Proposals (BCP), vs. specifications that are emerging in various other standards groups (IETF, W3C, and we have desire to submit some of these as BIPs as well).
>>
>> We do a few things differently, one of which in particular might be useful for the future of BIPs: we reset the numbers every year. So the first new BCR (research proposal) for 2024 would be 2024-01. Also, when there is a major change in an old BCR, we create a new number for it in the new year it is update.
>>
>> We also have a concept called "Status", which is a progression that only moves forward if BCRs are actually implemented with a reference implementation, and advances further when they have multiple implementations (and thus are qualified moved over to BCP repo as it is somewhat stable and no longer "research".). A last form is when a specification has moved to be controlled by another standards group (such as a BIP). If only one organization implements a BCR, it will never advance to BCP.
>>
>> Some form of Status for BIPs inspired by this concept could track if a BIP was ever actually implemented by someone, or more ideally, implemented by multiple people in multiple organizations, ideally in multiple languages.
>>
>> Here is how we currently do status, and the status of our current specifications: https://github.com/BlockchainCommons/Research/blob/master/README.md#status
>>
>> Each BCR has a status which is indicated by a symbol.
>>
>> Symbol	Title	Description
>> ??	Withdrawn	Of historic interest only. Withdrawn either because never came into use or proved sufficiently problematic that we do not recommend its usage in any way.
>> ?	Superseded	Superseded by a newer BCR. We do not suggest implementing as an output format, but you may still wish to implement as an input format to maintain backward compatibility.
>> ?	Research	Contains original research or proposes specifications that have not yet been implemented by us. Offered to the community for consideration.
>> ??	Reference Implementation	At least one reference implementation has been released, usually as a library, and may include demos or other supporting tools. This specification still remains very open to change because it has not yet (to our knowledge) been implemented by additional parties.
>> ????	Multiple Implementations	At least two (known) implementations exist, at least one not by the owner of the reference implementation. Has demonstrable community support. May still change due to the needs of the community, but community feedback will be sought.
>> ??????	Standards Track	Typically at least two implementations, and is considered stable and ready for standardization. Being proposed as a BIP, IETF Internet Draft, or some other standardization draft format. Will typically be moved to the[BCP repo](https://github.com/BlockchainCommons/bcps). Though changes may still be made to the specification, these changes will exclusively be to allow for standardization, and will be conducted with community feedback.
>> ????????	Standardized	A specification has been standardized as a an IETF RFC, BIP, or approved by some other standards body.
>>
>> ?? after another status symbol is read, "...but withdrawn" and ? is read, "...but superseded".
>>
>> -- Christopher Allen
>>
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>>
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240117/479bb74d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 20
********************************************
