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

   1. Re: Proposed BIP for OP_CAT (Anthony Towns)
   2. Re: Proposed BIP for OP_CAT (Andrew Poelstra)
   3. Re: Ordinals BIP PR (Andrew Poelstra)
   4. Re: Ordinals BIP PR (Peter Todd)
   5. Re: [Lightning-dev] OP_Expire and Coinbase-Like Behavior:
      Making HTLCs Safer by Letting Transactions Expire Safely (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Mon, 23 Oct 2023 22:26:26 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Rusty Russell <rusty@rustcorp.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTZmcis5IkIGazYq@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Mon, Oct 23, 2023 at 12:43:10PM +1030, Rusty Russell via bitcoin-dev wrote:
> 2. Was there a concrete rationale for maintaining 520 bytes?

Without a limit of 520 bytes, then you can construct a script:

    <p> CHECKSIGVERIFY
    {DUP CAT}x10
      (we know have a string that is the second witness repeated 1024 times
       on the stack; if it was 9 bytes, call it 9216B total)

    {DUP} x 990
      (we now have 1000 strings each of length 9216B bytes, for ~9.2MB total)

    SHA256SUM {CAT SHA256SUM}x999
      (we now have a single 32B field on the stack)
    <h> EQUAL
      (and can do a hardcoded check to make sure there weren't any
       shortcuts taken)

That raises the max memory to verify a single script from ~520kB (1000
stack elements by 520 bytes each) to ~10MB (1000 stack elements by
10kB each).

> 10k is the current script limit, can we get closer to that? :)

The 10k limit applies to scriptPubKey, scriptSig and segwit v0 scripts.
There's plenty of examples of larger tapscripts, eg:

    https://mempool.space/tx/0301e0480b374b32851a9462db29dc19fe830a7f7d7a88b81612b9d42099c0ae

    (3,938,182 bytes of script, non-standard due to being an oversized tx)

   https://mempool.space/tx/2d4ad78073f1187c689c693bde62094abe6992193795f838e8be0db898800434

    (360,543 bytes of script, standard, I believe)

Cheers,
aj


------------------------------

Message: 2
Date: Mon, 23 Oct 2023 13:41:51 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Rusty Russell <rusty@rustcorp.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTZ4H2y6+5pxRcs/@camus>
Content-Type: text/plain; charset="us-ascii"

On Mon, Oct 23, 2023 at 12:43:10PM +1030, Rusty Russell via bitcoin-dev wrote:
> Ethan Heilman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> writes:
> > Hi everyone,
> >
> > We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
> > https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki
> 
> This is really nice to see!
> 
> AFAICT you don't define the order of concatenation, except in the
> implementation[1].  I think if A is top of stack, we get BA, not AB?
> 
> 520 feels quite small for script templates (mainly because OP_CAT itself
> makes Script more interesting!).  For example, using OP_TXHASH and
> OP_CAT to enforce that two input amounts are equal to one output amount
> takes about 250 bytes of Script[2] :(
> 
> So I have to ask:
> 
> 1. Do other uses feel like 520 is too limiting?

In my view, 520 feels limiting provided that we lack rolling sha2
opcodes. If we had those, then arguably 65 bytes is enough. Without
them, I'm not sure that any value is "enough". For CHECKSIGFROMSTACK
emulation purposes ideally we'd want the ability to construct a full
transaction on the stack, which in principle would necessitate a 4M
limit.

> 2. Was there a concrete rationale for maintaining 520 bytes?  10k is the current
>    script limit, can we get closer to that? :)

But as others have said, 520 bytes is the existing stack element limit
and minimizing changes seems like a good strategy to get consensus. (On
the other hand, it's been a few days without any opposition so maybe we
should be more agressive :)).

> 3. Should we restrict elsewhere instead?  After all, OP_CAT doesn't
>    change total stack size, which is arguably the real limit?
> 

Interesting thought. Right now the stack size is limited to 1000
elements of 520 bytes each, which theoretically means a limit of 520k.
Bitcoin Core doesn't explicitly count the "total stack size" in the
sense that you're suggesting; it just enforces these two limits
separately.

I think trying to add a "total stack size limit" (which would have to
live alongside the two existing limits; we can't replace them without
a whole new Tapscript version) would add a fair bit of accounting
complextiy and wind up touching almost every other opcode...probably
not worth the added consensus logic.

> Of course, we can increase this limit in future tapscript versions, too,
> so it's not completely set in stone.
> 

-- 
Andrew Poelstra
Director of Research, Blockstream
Email: apoelstra at wpsoftware.net
Web:   https://www.wpsoftware.net/andrew

The sun is always shining in space
    -Justin Lewis-Webster

-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 488 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/b9aafd3c/attachment-0001.sig>

------------------------------

Message: 3
Date: Mon, 23 Oct 2023 13:45:44 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Casey Rodarmor <casey@rodarmor.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <ZTZ5CGtBB9+zFbtY@camus>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 10:38:01PM -0700, Casey Rodarmor via bitcoin-dev wrote:
>
> <snip>
> 
> There has been much misunderstanding of the nature of the BIP process.
> BIPS, in particular informational BIPs, are a form of technical
> documentation, and their acceptance does not indicate that they will be
> included in any implementation, including Bitcoin Core, nor that they they
> have consensus among the community.
> 
> Preexisting BIPs include hard-fork block size increases, hard-fork
> proof-of-work changes, colored coin voting protocols, rejected soft fork
> proposals, encouragement of address reuse, and drivechain.
>
> <snip>
>

I agree and I think it sets a bad precedent to be evaluating BIPs based
on the merits of their implementation (vs their specification) or their
consequences for the network. Actual consensus is much bigger than the
BIPs repo, so this accomplishes little beyond making the BIPs repo itself
hard to interact with.

In the worst case it may cause people to interpret BIP numbers as
indicating that proposals are "blessed" by some particular influential
set of people, which can only cause problems.

-- 
Andrew Poelstra
Director of Research, Blockstream
Email: apoelstra at wpsoftware.net
Web:   https://www.wpsoftware.net/andrew

The sun is always shining in space
    -Justin Lewis-Webster

-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 488 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/4d3e98f7/attachment-0001.sig>

------------------------------

Message: 4
Date: Mon, 23 Oct 2023 15:35:30 +0000
From: Peter Todd <pete@petertodd.org>
To: Casey Rodarmor <casey@rodarmor.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <ZTaSwtvctmIiF74k@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 10:38:01PM -0700, Casey Rodarmor via bitcoin-dev wrote:
> Dear List,
> 
> The Ordinals BIP PR has been sitting open for nine months now[0]. I've
> commented a few times asking the BIP editors to let me know what is needed
> for the BIP to either be merged or rejected. I've also reached out to the
> BIP editors via DM and email, but haven't received a response.
> 
> There has been much misunderstanding of the nature of the BIP process.
> BIPS, in particular informational BIPs, are a form of technical
> documentation, and their acceptance does not indicate that they will be
> included in any implementation, including Bitcoin Core, nor that they they
> have consensus among the community.
> 
> Preexisting BIPs include hard-fork block size increases, hard-fork
> proof-of-work changes, colored coin voting protocols, rejected soft fork
> proposals, encouragement of address reuse, and drivechain.

I have _not_ requested a BIP for OpenTimestamps, even though it is of much
wider relevance to Bitcoin users than Ordinals by virtue of the fact that much
of the commonly used software, including Bitcoin Core, is timestamped with OTS.
I have not, because there is no need to document every single little protocol
that happens to use Bitcoin with a BIP.

Frankly we've been using BIPs for too many things. There is no avoiding the act
that BIP assignment and acceptance is a mark of approval for a protocol. Thus
we should limit BIP assignment to the minimum possible: _extremely_ widespread
standards used by the _entire_ Bitcoin community, for the core mission of
Bitcoin.

It's notable that Lightning is _not_ standardized via the BIP process. I think
that's a good thing. While it's arguably of wide enough use to warrent BIPs,
Lightning doesn't need the approval of Core maintainers, and using their
separate BOLT process makes that clear.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/7d7259be/attachment-0001.sig>

------------------------------

Message: 5
Date: Mon, 23 Oct 2023 15:45:44 +0000
From: Peter Todd <pete@petertodd.org>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] OP_Expire and Coinbase-Like
	Behavior: Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZTaVKB1wdsLL7XiK@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Mon, Oct 23, 2023 at 11:10:56AM +0000, ZmnSCPxj wrote:
> Hi all,
> 
> This was discussed partially on the platform formerly known as twitter, but an alternate design goes like this:
> 
> * Add an `nExpiryTime` field in taproot annex.

I would strongly suggest making it nExpiryHeight, and only offering the option
of expiration at a given height.

Time-based anything is sketchy, as it could give miners incentives to lie about
the current time in the nTime field. If anything, the fact that nLockTime can
in fact be time-based was a design mistake.

>   * This indicates that the transaction MUST NOT exist in a block at or above the height specified.
>   * Mempool should put txes buckets based on `nExpiryTime`, and if the block is reached, drop all the buckets with `nExpiryTime` less than that block height.
> * Add an `OP_CHECKEXPIRYTIMEVERIFY` opcode, mostly similar in behavior to `OP_EXPIRE` proposed by Peter Todd:

Note that if we redefine an OP_SuccessX opcode, we do not need _Verify
behavior.  We can produce a true/false stack element, making either OP_Expire
or OP_CheckExpiryTime better names for the opcode.

>   * Check if `nExpiryTime` exists and has value equal or less than the stack top.
> 
> The primary difference is simply that while Peter proposes an implicit field for the value that `OP_EXPIRE` will put in `CTransaction`, I propose an explicit field for it in the taproot annex.

To be clear, I also proposed an explicit field too. But I had a brainfart and
forgot that we'd added the taproot annex. So I proposed re-using part of
nVersion.

> The hope is that "explicit is better than implicit" and that the design will be better implemented as well by non-Bitcoin-core implementations, as the use of tx buckets is now explicit in treating the `nExpiryTime` field.

Also, having a nExpiryHeight may be useful in cases where a signature covering
the field is sufficient.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/f1541099/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 39
********************************************
