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

   1. Re: Proposed BIP for OP_CAT (Peter Todd)
   2. Re: Ordinals BIP PR (Peter Todd)
   3. Re: Ordinals BIP PR (Peter Todd)
   4. Full-RBF Peering Bitcoin Core v25.1 Released (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Thu, 26 Oct 2023 21:55:48 +0000
From: Peter Todd <pete@petertodd.org>
To: Ethan Heilman <eth3rs@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTrgZPwv1BlXqyWV@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Sat, Oct 21, 2023 at 01:08:03AM -0400, Ethan Heilman via bitcoin-dev wrote:
> OP_CAT fails if there are less than two values on the stack or if a
> concatenated value would have a combined size of greater than the
> maximum script element size of 520 Bytes.

Note that if OP_CAT immediately _succeeds_ if the combined size is >= 520
bytes, reverting to the behavior of OP_SUCCESSx, the maximum size can be
increased in a subsequent soft fork.

Of course, this would often require extra opcodes to validate the size of
non-const arguments. But you'd only need another five or six bytes in many
cases:

    SIZE <n> LESSTHAN VERIFY
    <fixed data>
    CAT

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231026/e18fe30c/attachment-0001.sig>

------------------------------

Message: 2
Date: Thu, 26 Oct 2023 22:05:30 +0000
From: Peter Todd <pete@petertodd.org>
To: Tim Ruffing <crypto@timruffing.de>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <ZTriqvhah23jBSFW@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Mon, Oct 23, 2023 at 06:32:47PM +0200, Tim Ruffing wrote:
> On Mon, 2023-10-23 at 15:35 +0000, Peter Todd via bitcoin-dev wrote:
> > Thus
> > we should limit BIP assignment to the minimum possible: _extremely_
> > widespread
> > standards used by the _entire_ Bitcoin community, for the core
> > mission of
> > Bitcoin.
> 
> BIPs are Bitcoin Improvement *Proposals*. What you suggest would imply

BIPs being proposals is itself part of the problem. Note how RFCs have a Draft
RFC system to avoid giving numbers for absolutely every idea.

> that someone needs to evaluate them even before they become proposals.
> And this raises plenty of notoriously hard to answers questions:
>  * Who is in charge?
>  * How to predict if a proposal will be a widespread standard?
>  * What is the core mission of Bitcoin?
>  * How to measure if something is for the core mission?
>  * Who and what is the _entire_ Bitcoin community?

...and we still face those problems with the current BIPs system. In particular
the "Who is in charge?" problem. BIPs are always going to be a centralized
system.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231026/6cafdb22/attachment-0001.sig>

------------------------------

Message: 3
Date: Thu, 26 Oct 2023 22:11:50 +0000
From: Peter Todd <pete@petertodd.org>
To: Olaoluwa Osuntokun <laolu32@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <ZTrkJrqzBB0e9dXB@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Oct 24, 2023 at 03:56:55PM -0700, Olaoluwa Osuntokun via bitcoin-dev wrote:
> TL;DR: let's just use an automated system to assign BIP numbers, so we can
> spend time on more impactful things.

Yes, an easy way to do that is to use a mathematical function, like SHA256(<bip contents>)
or Pubkey(<bip author controlled secret key>).

Of course, that's also silly, as we might as well use URLs at that point...

> IIUC, one the primary roles of the dedicated BIP maintainers is just to hand
> out BIP numbers for documents. Supposedly with this privilege, the BIP
> maintainer is able to tastefully assign related BIPs to consecutive numbers,
> and also reserve certain BIP number ranges for broad categories, like 3xx
> for p2p changes (just an example).
>
> To my knowledge, the methodology for such BIP number selection isn't
> published anywhere, and is mostly arbitrary. As motioned in this thread,
> some perceive this manual process as a gatekeeping mechanism, and often
> ascribe favoritism as the reason why PR X got a number immediately, but PR Y
> has waited N months w/o an answer.
> 
> Every few years we go through an episode where someone is rightfully upset
> that they haven't been assigned a BIP number after following the requisite
> process.  Most recently, another BIP maintainer was appointed, with the hope
> that the second maintainer would help to alleviate some of the subjective
> load of the position.  Fast forward to this email thread, and it doesn't
> seem like adding more BIP maintainers will actually help with the issue of
> BIP number assignment.
> 
> Instead, what if we just removed the subjective human element from the
> process, and switched to using PR numbers to assign BIPs? Now instead of
> attempting to track down a BIP maintainer at the end of a potentially
> involved review+iteration period, PRs are assigned BIP numbers as soon as
> they're opened and we have one less thing to bikeshed and gatekeep.
> 
> One down side of this is that assuming the policy is adopted, we'll sorta
> sky rocket the BIP number space. At the time of writing of this email, the
> next PR number looks to be 1508. That doesn't seem like a big deal to me,
> but we could offset that by some value, starting at the highest currently
> manually assigned BIP number. BIP numbers would no longer always be
> contiguous, but that's sort of already the case.
> 
> There's also the matter of related BIPs, like the segwit series (BIPs 141,
> 142, 143, 144, and 145). For these, we can use a suffix scheme to indicate
> the BIP lineage. So if BIP 141 was the first PR, then BIP 142 was opened
> later, the OP can declare the BIP 142 is BIP 141.2 or BIP 141-2. I don't
> think it would be too difficult to find a workable scheme.

At that point, why are we bothering with numbers at all? If BIP #'s aren't
memorable, what is their purpose? Why not just let people publish ideas on
their own web pages and figure out what we're going to call those ideas on a
case-by-case basis.

All this gets back to my original point: a functioning BIP system is
*inherently* centralized and involves human gatekeepers who inevitably have to
apply standards to approve BIPs. You can't avoid this as long as you want a BIP
system.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231026/6719f1ad/attachment-0001.sig>

------------------------------

Message: 4
Date: Thu, 26 Oct 2023 22:20:21 +0000
From: Peter Todd <pete@petertodd.org>
To: Michael Ford <fanquake@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Full-RBF Peering Bitcoin Core v25.1 Released
Message-ID: <ZTrmJUDWaKCw5zCm@petertodd.org>
Content-Type: text/plain; charset="utf-8"

Available from: https://github.com/petertodd/bitcoin/tree/full-rbf-v25.1

eg:

    git clone -b full-rbf-v25.1 https://github.com/petertodd/bitcoin.git

What is this? It's Bitcoin Core v25.1, with Antoine Riard's full-rbf peering
code, and some additional minor updates to it. This does two things for
full-rbf nodes:

1) Advertises a FULL_RBF service bit when mempoolfullrbf=1 is set.
2) Connects to four additional FULL_RBF peers.

Doing this ensures that a core group of nodes are reliably propagating full-rbf
replacements. We don't need everyone to run this. But it'd be helpful if more
people did.

As for why you should run full-rbf, see my blog post:

https://petertodd.org/2023/why-you-should-run-mempoolfullrbf

At the moment, ?31% of hash power, ?4 pools, are mining full-RBF:

https://petertodd.org/2023/fullrbf-testing


We even have hats! :D

https://twitter.com/peterktodd/status/1659996011086110720/photo/1

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231026/f47bbecb/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 46
********************************************
