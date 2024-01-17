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

   1. BitBlend Proposal for 2106 (BitBlend2106)
   2. Re: Compressed Bitcoin Transactions (Tom Briar)
   3. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Nagaev Boris)
   4. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Nagaev Boris)


----------------------------------------------------------------------

Message: 1
Date: Tue, 16 Jan 2024 13:50:43 +0000
From: BitBlend2106 <BitcoinBitBlend@proton.me>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] BitBlend Proposal for 2106
Message-ID:
	<iB0Ngnnxq7em4m_gudf5OZ7Mh29braXehNVygAZWjRTSs5DbKzaGFCxkynPPruaO-NFRLZYFdLLikeKHvh8fdGlScf2-ECxadr6RmSkQ-68=@proton.me>
	
Content-Type: text/plain; charset="utf-8"

Dear Bitcoin Development Community,

I am reaching out to share a solution I have developed to address the anticipated 2106 overflow issue. After a significant development period, I believe the solution is ready for a community review.

Below, you will find an abstract summarizing the key aspects of this proposal, which is titled "BitBlend:A Non-Disruptive Solution to the Bitcoin 2106 Timestamp Overflow.? The abstract aims to provide a concise overview of the solution's approach and objectives. For a more detailed understanding, I have also included a link to the full white paper hosted on GitHub.

Abstract:

The Bitcoin network faces a significant technical challenge as it approaches the year 2106, when the 32-bit field for block timestamps will reach its maximum value. This paper introduces "BitBlend," a solution designed to address this impending overflow without necessitating a coordinated hard fork or consensus change. Similar to the idea by Pieter Wuille [2], BitBlend proposes a novel reinterpretation of the existing 32-bit time field, extending its functionality by representing only the last 32 bits of the full timestamp. The solution incorporates an innovative overflow detection and correction method, named the BitBlend procedure, which seamlessly integrates into the current system. Key to BitBlend is maintaining the original 32-bit format for external communication while employing a 64-bit internal representation for block times. This dual approach ensures backward compatibility and network continuity, allowing nodes to gradually adopt the update without synchronization. Addition
 ally, BitBlend addresses the implications for time locks, advocating for the natural expiration of absolute time locks post-2106 and the continued use of block height and relative time locks. ??This solution prioritizes minimal alterations to Bitcoin's core components, striving to preserve its foundational principles while ensuring its longevity and functionality. The paper seeks feedback from the Bitcoin development community on the feasibility and potential integration of the BitBlend solution into the Bitcoin protocol.

Link to Full White Paper:
https://bitblend2106.github.io/bitcoin/BitBlend2106.pdf

I would greatly appreciate any thoughtful reviews, comments, or suggestions you may have regarding the BitBlend solution. My user name is BitcoinBitBlend on proton mail.
Thank you for your time and consideration. I look forward to your valuable input.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240116/245366af/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 16 Jan 2024 17:08:54 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<jdBdzLD0bcOPikKGQd1VpWU6dIc3_X6I_Q1UFuEiYfiY_Z6xF86nlDqnU00PGsQS3XdBFwjlmYWN-7_aXbjVjkXmGEVf0cGKPHjzhYkVweY=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi,

In addition to the use cases listed in the schema, such as steganography, satellite, and radio broadcast, an application can be made for Peer-to-peer communication between Bitcoin nodes. Except when compressing the Txid/Vout, which is optional, Transactions can gain up to 30% size savings while still being completely reversible. Furthermore, in a BIP-324 world, these savings are nontrivial.

BIP-324: https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki
Compressed Transaction Schema: compressed_transactions.md

Thanks-
Tom.


------------------------------

Message: 3
Date: Tue, 16 Jan 2024 20:29:58 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: Greg Tonoski <gregtonoski@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAFC_Vt4aDvWsUh4q+UxFa3ZyRC_eK2ek7HR-G+nOiaC-wSa-WA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Sat, Jan 13, 2024 at 12:03?PM Greg Tonoski <gregtonoski@gmail.com> wrote:
>
> On Wed, Dec 27, 2023 at 8:06?PM Nagaev Boris <bnagaev@gmail.com> wrote:
> >
> > On Wed, Dec 27, 2023 at 2:26?PM Greg Tonoski via bitcoin-dev
> > <bitcoin-dev@lists.linuxfoundation.org> wrote:
> > > As a result, there are incentives structure distorted and critical
> > > inefficiencies/vulnerabilities (e.g. misallocation of block space,
> > > blockspace value destruction, disincentivized simple transaction,
> > > centralization around complex transactions originators).
> > >
> > > Price of blockspace should be the same for any data (1 byte = 1 byte,
> > > irrespectively of location inside or outside of witness), e.g. 205/205
> > > and 767/767 bytes in the examples above.
> >
> > Witness data does not contribute to utxo set. The discount on storing
> > data in witness creates an incentive to store data exactly in the
> > witness and not in the parts contributing to utxo set.
> >
> > $ du -sh blocks/ chainstate/
> > 569G    blocks/
> > 9.3G    chainstate/
> >
> > Witness data is part of the "blocks" directory which is not
> > latency-critical and can be stored on a slow and cheap storage device.
> > Directory "chainstate" contains the data needed to validate new
> > transactions and should fit into a fast storage device otherwise
> > initial block download takes weeks. It is important to maintain the
> > incentives structure, resulting in a small chainstate.
>
> I think that the argument "discount on storing data in witness creates
> an incentive to store data exactly in the witness (...)" is
> fallacious. The "witness discount" does not affect the cost of data
> storage in a Bitcoin node. What the "witness discount" affects is the
> priority of a transaction pending confirmation only. For example, a
> SegWit type of transaction of size of 1MB is prioritized (by miners)
> over a non-SegWit transaction of the same size and fee. "Segwit
> discount" benefits bloated transactions and puts simple transactions
> at disadvantage (demonstrated at
> "https://gregtonoski.github.io/bitcoin/segwit-mispricing/comparison-of-costs.html"
> and "https://gregtonoski.github.io/bitcoin/segwit-mispricing/Comparison_of_4MB_and_1.33MB_blocks_in_Bitcoin.pdf").
>
> The Bitcoin fee is not charged per UTXO set size. It is not charged
> from a node operator. Nodes are up and running independently of
> Bitcoin fees.
>
> Any relation between UTXO set size and discount would be artificial
> and inefficient, wouldn't it?

Node operators are likely to put UTXO set to SSD and blocks to HDD.
SSD is more expensive than HDD. It is aligned with the fact that
people putting data into blockchain are financially motivated to put
it into witness data, i.e. into HDD. If miners charge the same per 1
byte in a transaction output and 1 byte in witness, then people
putting data into blockchain could put it into transaction outputs
(why not, if the price is the same), inflating the UTXO set and making
node operators buy bigger SSD (more costs for node operators). As a
node operator, I prefer the current structure.

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 4
Date: Tue, 16 Jan 2024 20:40:12 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: Greg Tonoski <gregtonoski@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAFC_Vt7EKhipSECtpa87fx5Ff1eFwfjn19P=9GONOcXFFhQYOA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Sun, Jan 14, 2024 at 10:21?AM Greg Tonoski via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> > > Price of blockspace should be the same for any data (1 byte = 1 byte,
> > irrespectively of location inside or outside of witness), e.g. 205/205
> > and 767/767 bytes in the examples above.
> >
> > "Should" ... to what end?
>
> "Should" in order to avoid hazard of centralization. A single bidder
> who takes advantage of "buy 1 get 3 megabytes free" may outcompete a
> number of individuals whose simple transactions recieve
> anti-preferential treatment - "buy 1 get 0.33 megabytes free" in
> aggregate. There is the illustration at:
> "https://gregtonoski.github.io/bitcoin/segwit-mispricing/Comparison_of_4MB_and_1.33MB_blocks_in_Bitcoin.pdf".

It is not sufficient to be a centralized sender to utilize this
advanage. The sender has to store data in the blockchain which itself
is not the best utilization of money, even given the discount. Also
what is the danger of centralization of such senders? The dangerous
centralization is the centralization of real bitcoin sending, which
has already happened - exchanges utilize batch transaction sending,
saving on fees over a regular bitcoin sender, because they avoid
change creation. This has nothing to do with witness discount, though.

> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev



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

End of bitcoin-dev Digest, Vol 104, Issue 17
********************************************
