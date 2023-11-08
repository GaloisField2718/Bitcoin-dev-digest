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

   1. Re: Future of the bitcoin-dev mailing list (Peter Todd)
   2. Re: Future of the bitcoin-dev mailing list (Peter Todd)
   3. Re: Future of the bitcoin-dev mailing list (Peter Todd)
   4. Implementing Blake3 in Bitcoin Script (Robin Linus)


----------------------------------------------------------------------

Message: 1
Date: Tue, 7 Nov 2023 22:59:54 +0000
From: Peter Todd <pete@petertodd.org>
To: Christopher Allen <ChristopherA@lifewithalacrity.com>, Bitcoin
	Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID: <ZUrBalQQJyaKr2a9@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Nov 07, 2023 at 11:41:59AM -0800, Christopher Allen via bitcoin-dev wrote:
> As Bitcoin-Core already uses GitHub, another possibility is to use the new
> GitHub discussions feature. We increasingly have been using this at
> Blockchain Commons as everyone is using already using GitHub. We have also
> created some GitHub actions to backup discussions so that GitHub will not
> be a central point of failure -should be possible to create a static page
> archive using GitHub pages (but have not had budget for that).
> 
> For instance, here is the GitHub discussion area for wallet developers
> working together on Bitcoin wallet interoperability specifications:
> https://github.com/BlockchainCommons/Gordian-Developer-Community

Strong NACK.

bitcoin-dev should be independent of Bitcoin Core.

Also, a very useful thing that a mailing list does that GitHub does not is
cryptographic signatures, both obvious like PGP, and less obvious like DKIM. We
should not be moving even more discussion to mediums where authors aren't
properly signing their messages.

The user experience of GitHub and similar web forums is poor too. It's much
nicer to be able to reply to messages offline, asyncronously, regardless of
whether or not you happen to have a good internet connection at the time.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231107/8004ee17/attachment-0001.sig>

------------------------------

Message: 2
Date: Tue, 7 Nov 2023 23:07:07 +0000
From: Peter Todd <pete@petertodd.org>
To: Ademan <ademan555@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID: <ZUrDGzVHuciQPfLB@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Nov 07, 2023 at 11:03:30AM -0600, Ademan via bitcoin-dev wrote:
> Hi Bryan,
> 
> I don't really want my first (and last?) devlist message to be a fairly
> off-the-cuff post on this topic, but here we go anyway.
> 
> At the risk of sounding like a nostr evangelist (I promise I'm not), I want
> to suggest nostr as a potential replacement to the mailing list. A decent
> chunk of software would need to be written, but none of the alternatives
> seem particularly attractive to me. I particularly dislike the idea of
> locking into a single siloed forum service like the bitcointalk forums. I
> realize I may be in the minority of course.

Strong NACK on nostr. It's a badly designed, centralized, protocol that needs a
significant redesign to be usable. While off topic for this mailing list, some
of its many issues include:

* Reliance on single-key, cryptography that often results in people having
  their keys compromised. This is a serious problem in the context of
  bitcoin-dev, where faked messages published could easily have market-moving
  results.

* Inability to mirror relays: since nostr deliberately ignores the lessons of
  blockchains, there is no way to be sure that you have a complete set of
  messages from a given person, for a given topic, etc.

* Highly centralized design: since mirroring relays isn't reliable, in reality
  nostr operates in a highly centralized fashion, dependent on a tiny number of
  relays that can't be easily replaced if taken down.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231107/1f3fa4a7/attachment-0001.sig>

------------------------------

Message: 3
Date: Tue, 7 Nov 2023 23:08:58 +0000
From: Peter Todd <pete@petertodd.org>
To: Bryan Bishop <kanzure@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID: <ZUrDip1Uf1/rRPIX@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Nov 07, 2023 at 09:37:22AM -0600, Bryan Bishop via bitcoin-dev wrote:
> Anti spam has been an issue for the moderators. It's relentless. Without
> access to the underlying server, it has been difficult to fight spam. There
> is some support for filters in mailman2 but it's not great.

Since this is a technical mailing list it would be fine to require people to
pay a non-refundable anti-spam fee, eg via lightning, to gain the ability to
send messages. While this would require some custom software, it's probably
even possible to implement this if a third party is used for hosting, provided
they have some kind of API.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231107/5bb40523/attachment-0001.sig>

------------------------------

Message: 4
Date: Wed, 8 Nov 2023 00:22:44 +0100
From: Robin Linus <robin@zerosync.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Implementing Blake3 in Bitcoin Script
Message-ID: <91D40E43-526E-42BC-BBBF-AABBD4F158F4@zerosync.org>
Content-Type: text/plain; charset="us-ascii"

Good morning mailing list,

We implemented a hash function in Bitcoin Script to verify Merkle inclusion proofs in the BitVM. This allows the VM to have sheer infinite memory, which doesn't have to get represented in expensive bit commitments.

The following transaction demonstrates on-chain a Blake3 hash lock, which is unlocked by providing the preimage in the unlocking script: https://blockstream.info/tx/d8a091a7f5ffa4993681b3df688968fd274bc76897b8b3953309ffad6055f4b0?expand <https://blockstream.info/tx/d8a091a7f5ffa4993681b3df688968fd274bc76897b8b3953309ffad6055f4b0?expand> If you're curious, here you can find the source code: https://github.com/BitVM/BitVM/blob/main/opcodes/examples/blake3.js 

We chose Blake3 as it seems to be one of the most simple modern hash functions in terms of instruction count. We implemented only a single round performed over a 64 byte message, because that's sufficient for us to verify Merkle paths. Our implementation represents u32 words as 4 separate bytes on the stack, because that seemed to be the optimal tradeoff to implement u32 addition, u32 bitwise XOR, and u32 bitwise rotations, as required for Blake3. 

We used JavaScript as templating language, to assemble complex programs from relatively simple opcodes. You can find the implementation of our u32 opcodes here: https://github.com/BitVM/BitVM/tree/main/opcodes/u32 <https://github.com/BitVM/BitVM/tree/main/opcodes/u32> In particular, for the bitwise XOR we used some cool hacks with a lookup table for a helper function: https://github.com/BitVM/BitVM/blob/main/opcodes/docs/u8_xor.md <https://github.com/BitVM/BitVM/blob/main/opcodes/docs/u8_xor.md>

Furthermore, we added a simple memory management, which allows us to have identifiers for variables, which we can read and write, and keep track of them while they're moved on the stack. For example, this allows us to implement the permutations of the Blake state simply by relabeling the identifiers of variables, instead of actually moving them around on the stack.

In total, the script is about 100kB or 25k vBytes. That's fine for now to build a toy-version of BitVM, but the actual plan is to split up the Blake code, such that verifier and prover can reduce the required onchain data significantly by bisecting the execution in a challenge-response game instead of executing it fully.


Cheers, 
- Robin




Co-Founder and President

ZeroSync
6300 Zug
Switzerland

https://zerosync.org | https://twitter.com/zerosync_

-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231108/7ad84234/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 19
********************************************
