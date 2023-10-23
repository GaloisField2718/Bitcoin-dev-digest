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

   1. Re: Examining ScriptPubkeys in Bitcoin Script (Rusty Russell)
   2. Re: Proposed BIP for OP_CAT (Rusty Russell)
   3. Ordinals BIP PR (Casey Rodarmor)
   4. Re: Proposed BIP for OP_CAT (vjudeu@gazeta.pl)
   5. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (David A. Harding)


----------------------------------------------------------------------

Message: 1
Date: Sun, 22 Oct 2023 14:46:33 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: Brandon Black <freedom@reardencode.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <87edhnwau6.fsf@rustcorp.com.au>
Content-Type: text/plain

Brandon Black <freedom@reardencode.com> writes:
> On 2023-10-20 (Fri) at 14:10:37 +1030, Rusty Russell via bitcoin-dev wrote:
>>         I've done an exploration of what would be required (given
>> OP_TX/OP_TXHASH or equivalent way of pushing a scriptPubkey on the
>> stack) to usefully validate Taproot outputs in Bitcoin Script.  Such
>> functionality is required for usable vaults, at least.
>
> So you're proposing this direction as an alternative to the more
> constrained OP_UNVAULT that replaces a specific leaf in the taptree in a
> specific way? I think the benefits of OP_UNVAULT are pretty big vs. a
> generic construction (e.g. ability to unvault multiple inputs sharing
> the same scriptPubkey to the same output).

I would have to write the scripts exactly (and I'm already uncomfortable
that I haven't actually tested the ones I wrote so far!) to properly
evaluate.

In general, script makes it hard to do N-input evaluation (having no
iteration).  It would be useful to attempt this though, as it might
enlighted us as to OP_TXHASH input selection: for example, we might want
to have an "all *but* one input" mode for this kind of usage.

Dealing with satsoshi amounts is possible, but really messy (that's my next
post).

>> TL;DR: if we have OP_TXHASH/OP_TX, and add OP_MULTISHA256 (or OP_CAT),
>> OP_KEYADDTWEAK and OP_LESS (or OP_CONDSWAP), and soft-fork weaken the
>> OP_SUCCESSx rule (or pop-script-from-stack), we can prove a two-leaf
>> tapscript tree in about 110 bytes of Script.  This allows useful
>> spending constraints based on a template approach.
>
> I agree that this is what is needed. I started pondering this in
> response to some discussion about the benefits of OP_CAT or OP_2SHA256
> for BitVM.

Given these examples, I think it's clear that OP_MULTISHA256 is almost
as powerful as OP_CAT, without the stack limit problems.  And OP_2SHA256
is not sufficient in general for CScriptNum generation, for example.

> Personally I'd use OP_TAGGEDCATHASH that pops a tag (empty tag can be
> special cased to plain sha256) and a number (n) of elements to hash,
> then tagged-hashes the following 'n' elements from the stack.

That's definitely a premature optimization to save two opcodes.

Cheers,
Rusty.


------------------------------

Message: 2
Date: Mon, 23 Oct 2023 12:43:10 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: Ethan Heilman <eth3rs@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Bitcoin Dev
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <871qdmulvt.fsf@rustcorp.com.au>
Content-Type: text/plain

Ethan Heilman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> writes:
> Hi everyone,
>
> We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
> https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki

This is really nice to see!

AFAICT you don't define the order of concatenation, except in the
implementation[1].  I think if A is top of stack, we get BA, not AB?

520 feels quite small for script templates (mainly because OP_CAT itself
makes Script more interesting!).  For example, using OP_TXHASH and
OP_CAT to enforce that two input amounts are equal to one output amount
takes about 250 bytes of Script[2] :(

So I have to ask:

1. Do other uses feel like 520 is too limiting?
2. Was there a concrete rationale for maintaining 520 bytes?  10k is the current
   script limit, can we get closer to that? :)
3. Should we restrict elsewhere instead?  After all, OP_CAT doesn't
   change total stack size, which is arguably the real limit?

Of course, we can increase this limit in future tapscript versions, too,
so it's not completely set in stone.

Thanks!
Rusty.
[1] Maybe others are Bitcoin Core fluent, but I found it weird that
    it's not simply `valtype vch1 = popstack(stack);`,
    and `vch3.reserve(vch1.size() + vch2.size());` was just a weird detail.
[2] https://rusty.ozlabs.org/2023/10/22/amounts-in-script.html


------------------------------

Message: 3
Date: Fri, 20 Oct 2023 22:38:01 -0700
From: Casey Rodarmor <casey@rodarmor.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CANLPe+OQBsPiTrLEfz=SMxU8TkM_1XNfJQeq8gt2V6vDu=+Zxw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Dear List,

The Ordinals BIP PR has been sitting open for nine months now[0]. I've
commented a few times asking the BIP editors to let me know what is needed
for the BIP to either be merged or rejected. I've also reached out to the
BIP editors via DM and email, but haven't received a response.

There has been much misunderstanding of the nature of the BIP process.
BIPS, in particular informational BIPs, are a form of technical
documentation, and their acceptance does not indicate that they will be
included in any implementation, including Bitcoin Core, nor that they they
have consensus among the community.

Preexisting BIPs include hard-fork block size increases, hard-fork
proof-of-work changes, colored coin voting protocols, rejected soft fork
proposals, encouragement of address reuse, and drivechain.

I believe ordinals is in-scope for a BIP, and am hoping to get the PR
unstuck. I would appreciate feedback from the BIP editors on whether it is
in-scope for a BIP, if not, why not, and if so, what changes need to be
made for it to be accepted.

Best regards,
Casey Rodarmor

[0] https://github.com/bitcoin/bips/pull/1408
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/1786bc1b/attachment-0001.html>

------------------------------

Message: 4
Date: Mon, 23 Oct 2023 07:13:48 +0200
From: vjudeu@gazeta.pl
To: Rusty Russell <rusty@rustcorp.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Ethan Heilman
	<eth3rs@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Bitcoin Dev
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<194405691-79e11acd8b1dc1e2cdafc878b45b15c8@pmq3v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> I think if A is top of stack, we get BA, not AB?
?
Good question. I always thought "0x01234567 0x89abcdef OP_CAT 0x0123456789abcdef OP_EQUAL" is correct, but it could be reversed as well. If we want to stay backward-compatible, we can dig into the past, and test the old implementation of OP_CAT, before it was disabled. But anyway, any of those two choices will lead to similar consequences. Because you can always turn the former into the latter by using "OP_SWAP OP_CAT", instead of "OP_CAT".
?
> 520 feels quite small for script templates
?
It will be easier to start with that, when it comes to reaching consensus for a new soft-fork. But yes, I am very surprised, because I thought we will never see things like that, and I assumed the path to OP_CAT is just permanently closed. So, I am surprised this BIP reached a positive reaction, but well, that kind of proposal was not battle-tested, so maybe it could succeed.
?
> 10k is the current script limit, can we get closer to that?
?
We will get there anyway. Even if OP_CAT would allow concatenating up to 520-bit Schnorr signature (not to confuse 520-bit with 520-byte), people would chain it, to reach arbitrary size. If you can concatenate secp256k1 public keys with signatures, you can create a chain of OP_CATs, that will handle arbitrary size. The only limitation is then blockchain speed, which is something around 4 MB/10 min, and that is your only limit in this case.
?
And yes, if I can see that some people try to build logical gates like NAND with Bitcoin Script, then I guess all paths will be explored anyway. Which means, even if we will take more conservative approach, and switch from 520-byte proposal into 520-bit proposal, then still, people will do exactly the same things. Now, it is all about the cost of pushing data, because some people noticed, that everything can be executed on Script. I knew we will get there, but I expected it would just happen later than it happened.
?
> Of course, we can increase this limit in future tapscript versions, too, so it's not completely set in stone.
?
Judging by the last misuse of Ordinals, I think it may happen before anyone will propose some official future version. Which means, nothing is really set in stone anymore, because now people know, how to activate new features, without any soft-fork, and some no-forks will probably be done by newbies, without careful designing and testing, as it is done here.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/1f94ed32/attachment-0001.html>

------------------------------

Message: 5
Date: Sun, 22 Oct 2023 22:49:55 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Nadav Ivgi <nadav@shesek.info>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID: <0ae928c4209debc1fd4271fddfffde65@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-10-21 18:49, Nadav Ivgi via bitcoin-dev wrote:
> Could this be addressed with an OP_CSV_ALLINPUTS, a covenant opcode
> that requires _all_ inputs to have a matching nSequence, and using `1
> OP_CSV_ALLINPUTS` in the HTLC preimage branch?
> 
> This would prevent using unconfirmed outputs in the
> HTLC-preimage-spending transaction entirely, which IIUC should protect
> it against the replacement cycling attack.

I don't think that addresses the underlying problem.  In Riard's 
description, a replacement cycle looks like this:

- Bob broadcasts an HTLC-timeout  (input A, input B for fees, output X)
- Mallory replaces the HTLC-timeout with an HTLC-preimage (input A, 
input C for fees, output Y)
- Mallory replaces the transaction that created input C, removing the 
HTLC-preimage from the mempool

However, an alternative approach is:

- (Same) Bob broadcasts an HTLC-timeout (input A, input B for fees, 
output X)
- (Same) Mallory replaces the HTLC-timeout with an HTLC-preimage (input 
A, input C for fees, output Y)
- (Different) Mallory uses input C to replace the HTLC-preimage with a 
transaction that does not include input A, removing the preimage from 
the mempool

The original scenario requires input C to be from an unconfirmed 
transaction, so OP_CSV_ALLINPUTS works.  The alternative scenario works 
even if input C comes from a confirmed transaction, so OP_CSV_ALLINPUTS 
is ineffective.

-Dave


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 37
********************************************
