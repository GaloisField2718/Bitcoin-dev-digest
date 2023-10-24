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

   1. Re: Proposed BIP for OP_CAT (Rusty Russell)
   2. Re: Proposed BIP for OP_CAT (Andrew Poelstra)
   3. Re: Ordinals BIP PR (alicexbt)
   4. Re: Proposed BIP for OP_CAT (Rusty Russell)
   5. Re: Ordinals BIP PR (Ryan Breen)


----------------------------------------------------------------------

Message: 1
Date: Tue, 24 Oct 2023 11:18:24 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: Andrew Poelstra <apoelstra@wpsoftware.net>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <871qdku9pj.fsf@rustcorp.com.au>
Content-Type: text/plain

Andrew Poelstra <apoelstra@wpsoftware.net> writes:
> On Mon, Oct 23, 2023 at 12:43:10PM +1030, Rusty Russell via bitcoin-dev wrote:
>> Ethan Heilman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> writes:
>> > Hi everyone,
>> >
>> > We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
>> > https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki
>> 
>> 520 feels quite small for script templates (mainly because OP_CAT itself
>> makes Script more interesting!).  For example, using OP_TXHASH and
>> OP_CAT to enforce that two input amounts are equal to one output amount
>> takes about 250 bytes of Script[2] :(
>> 
>> So I have to ask:
>> 
>> 1. Do other uses feel like 520 is too limiting?
>
> In my view, 520 feels limiting provided that we lack rolling sha2
> opcodes. If we had those, then arguably 65 bytes is enough. Without
> them, I'm not sure that any value is "enough". For CHECKSIGFROMSTACK
> emulation purposes ideally we'd want the ability to construct a full
> transaction on the stack, which in principle would necessitate a 4M
> limit.

I haven't yet found a desire for rolling sha2: an `OP_MULTISHA256` has
been sufficient for my templating investigations w/ OP_TXHASH.  In fact,
I prefer it to OP_CAT, but OP_CAT does allow your Schnorr sig trick :)

>> 2. Was there a concrete rationale for maintaining 520 bytes?  10k is the current
>>    script limit, can we get closer to that? :)
>
> But as others have said, 520 bytes is the existing stack element limit
> and minimizing changes seems like a good strategy to get consensus. (On
> the other hand, it's been a few days without any opposition so maybe we
> should be more agressive :)).

It's probably worth *thinking* about, yes.

>> 3. Should we restrict elsewhere instead?  After all, OP_CAT doesn't
>>    change total stack size, which is arguably the real limit?
>> 
>
> Interesting thought. Right now the stack size is limited to 1000
> elements of 520 bytes each, which theoretically means a limit of 520k.
> Bitcoin Core doesn't explicitly count the "total stack size" in the
> sense that you're suggesting; it just enforces these two limits
> separately.

BTW, I'm just learning of the 1000 element limit; I couldn't see it on
scanning BIP-141.

> I think trying to add a "total stack size limit" (which would have to
> live alongside the two existing limits; we can't replace them without
> a whole new Tapscript version) would add a fair bit of accounting
> complextiy and wind up touching almost every other opcode...probably
> not worth the added consensus logic.

Simplest thing I can come up with:

- instead of counting simple stack depth, count each stack entry as
  (1 + <size>/520) entries?  You can still only push 520 bytes, so you
  can only make these with OP_CAT.

Looking in interpreter.cpp, `stack` and `altstack` now need to be
objects to count entries differently (not vectors), but it seems like
it'd be simple enough, and the logic could be enabled unconditionally
since it Cannot Be Violated prior to OP_CAT.

Cheers,
Rusty.


------------------------------

Message: 2
Date: Tue, 24 Oct 2023 01:17:28 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Rusty Russell <rusty@rustcorp.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTcbKM+XTCaJ2kIP@camus>
Content-Type: text/plain; charset="us-ascii"

On Tue, Oct 24, 2023 at 11:18:24AM +1030, Rusty Russell wrote:
> Andrew Poelstra <apoelstra@wpsoftware.net> writes:
> >> 3. Should we restrict elsewhere instead?  After all, OP_CAT doesn't
> >>    change total stack size, which is arguably the real limit?
> >> 
> >
> > Interesting thought. Right now the stack size is limited to 1000
> > elements of 520 bytes each, which theoretically means a limit of 520k.
> > Bitcoin Core doesn't explicitly count the "total stack size" in the
> > sense that you're suggesting; it just enforces these two limits
> > separately.
> 
> BTW, I'm just learning of the 1000 element limit; I couldn't see it on
> scanning BIP-141.
>

This limit is very old and predates segwit. It might predate P2SH.

> > I think trying to add a "total stack size limit" (which would have to
> > live alongside the two existing limits; we can't replace them without
> > a whole new Tapscript version) would add a fair bit of accounting
> > complextiy and wind up touching almost every other opcode...probably
> > not worth the added consensus logic.
> 
> Simplest thing I can come up with:
> 
> - instead of counting simple stack depth, count each stack entry as
>   (1 + <size>/520) entries?  You can still only push 520 bytes, so you
>   can only make these with OP_CAT.
> 
> Looking in interpreter.cpp, `stack` and `altstack` now need to be
> objects to count entries differently (not vectors), but it seems like
> it'd be simple enough, and the logic could be enabled unconditionally
> since it Cannot Be Violated prior to OP_CAT.
>

I had a similar thought. But my feeling is that replacing the stack
interpreter data structure is still too invasive to justify the benefit.

Also, one of my favorite things about this BIP is the tiny diff.

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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231024/09a3f3be/attachment-0001.sig>

------------------------------

Message: 3
Date: Tue, 24 Oct 2023 01:28:17 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Luke Dashjr <luke@dashjr.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<BYM-J2z1pEyXcmR305xM-uh4wNaRs6olvZa_dEhqZlr6_wO4s9dUANyTYg3ihdRJyJuTRHVr2nQpPIjMQeSJXH6deKxteFgBnMGhOdbS1gE=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Luke,

> Maybe we need a 3rd BIP editor. Both Kalle and myself haven't had time
> to keep up. There are several PRs far more important than Ordinals
> nonsense that need to be triaged and probably merged.

I don't think adding another editor solves the problem discussed in this thread. 
Last time we had similar situation and Kalle was added as editor instead of making BIP
process decentralized. It was discussed in this [thread][0].

BIP editors can have personal opinions and bias but if it affects PRs getting merged,
then repo has no use except for a few developers.

> The issue with Ordinals is that it is actually unclear if it's eligible
> to be a BIP at all, since it is an attack on Bitcoin rather than a
> proposed improvement. 

What makes it an attack on bitcoin? Some users want to use their money in a different way.
How is it different from taproot assets and other standards to achieve similar goals?

Some users and developers believe drivechain is an attack on bitcoin, BIP 47 is considered bad,
use of OP_RETURN in colored coins is controversial, increasing blocksize is not an improvement etc.
Still these BIPs exist in the same repository.

> proposed improvement. There is a debate on the PR whether the
> "technically unsound, ..., or not in keeping with the Bitcoin
> philosophy." or "must represent a net improvement." clauses (BIP 2) are
> relevant. Those issues need to be resolved somehow before it could be
> merged.

Can we remove terms like "philosophy", "net improvement" etc. from BIP 2? Because they could mean different
things for different people.

[0]: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-April/018859.html


/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Monday, October 23rd, 2023 at 11:59 PM, Luke Dashjr via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Everything standardized between Bitcoin software is eligible to be and
> should be a BIP. I completely disagree with the claim that it's used for
> too many things.
> 
> SLIPs exist for altcoin stuff. They shouldn't be used for things related
> to Bitcoin.
> 
> BOLTs also shouldn't have ever been a separate process and should really
> just get merged into BIPs. But at this point, that will probably take
> quite a bit of effort, and obviously cooperation and active involvement
> from the Lightning development community.
> 
> Maybe we need a 3rd BIP editor. Both Kalle and myself haven't had time
> to keep up. There are several PRs far more important than Ordinals
> nonsense that need to be triaged and probably merged.
> 
> The issue with Ordinals is that it is actually unclear if it's eligible
> to be a BIP at all, since it is an attack on Bitcoin rather than a
> proposed improvement. There is a debate on the PR whether the
> "technically unsound, ..., or not in keeping with the Bitcoin
> philosophy." or "must represent a net improvement." clauses (BIP 2) are
> relevant. Those issues need to be resolved somehow before it could be
> merged. I have already commented to this effect and given my own
> opinions on the PR, and simply pretending the issues don't exist won't
> make them go away. (Nor is it worth the time of honest people to help
> Casey resolve this just so he can further try to harm/destroy Bitcoin.)
> 
> Luke
> 
> 
> On 10/23/23 13:43, Andrew Poelstra via bitcoin-dev wrote:
> 
> > On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via bitcoin-dev wrote:
> > 
> > > I have not requested a BIP for OpenTimestamps, even though it is of much
> > > wider relevance to Bitcoin users than Ordinals by virtue of the fact that much
> > > of the commonly used software, including Bitcoin Core, is timestamped with OTS.
> > > I have not, because there is no need to document every single little protocol
> > > that happens to use Bitcoin with a BIP.
> > > 
> > > Frankly we've been using BIPs for too many things. There is no avoiding the act
> > > that BIP assignment and acceptance is a mark of approval for a protocol. Thus
> > > we should limit BIP assignment to the minimum possible: extremely widespread
> > > standards used by the entire Bitcoin community, for the core mission of
> > > Bitcoin.
> > 
> > This would eliminate most wallet-related protocols e.g. BIP69 (sorted
> > keys), ypubs, zpubs, etc. I don't particularly like any of those but if
> > they can't be BIPs then they'd need to find another spec repository
> > where they wouldn't be lost and where updates could be tracked.
> > 
> > The SLIP repo could serve this purpose, and I think e.g. SLIP39 is not a BIP
> > in part because of perceived friction and exclusivity of the BIPs repo.
> > But I'm not thrilled with this situation.
> > 
> > In fact, I would prefer that OpenTimestamps were a BIP :).
> > 
> > > It's notable that Lightning is not standardized via the BIP process. I think
> > > that's a good thing. While it's arguably of wide enough use to warrent BIPs,
> > > Lightning doesn't need the approval of Core maintainers, and using their
> > > separate BOLT process makes that clear.
> > 
> > Well, LN is a bit special because it's so big that it can have its own
> > spec repo which is actively maintained and used.
> > 
> > While it's technically true that BIPs need "approval of Core maintainers"
> > to be merged, the text of BIP2 suggests that this approval should be a
> > functionary role and be pretty-much automatic. And not require the BIP
> > be relevant or interesting or desireable to Core developers.
> > 
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 4
Date: Tue, 24 Oct 2023 14:15:49 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: Andrew Poelstra <apoelstra@wpsoftware.net>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <87r0lksmxe.fsf@rustcorp.com.au>
Content-Type: text/plain

Andrew Poelstra <apoelstra@wpsoftware.net> writes:
> I had a similar thought. But my feeling is that replacing the stack
> interpreter data structure is still too invasive to justify the benefit.
>
> Also, one of my favorite things about this BIP is the tiny diff.

To be fair, this diff is even smaller than the OP_CAT diff :)

Though I had to strongly resist refactoring, that interpreter code
needs a good shake!  Using a class for the stack is worth doing anyway
(macros, really??).

diff --git a/src/script/interpreter.cpp b/src/script/interpreter.cpp
index dcaf28c2472..2ee2034115f 100644
--- a/src/script/interpreter.cpp
+++ b/src/script/interpreter.cpp
@@ -403,6 +403,19 @@ static bool EvalChecksig(const valtype& sig, const valtype& pubkey, CScript::con
     assert(false);
 }
 
+// First 520 bytes is free, after than you consume an extra slot!
+static size_t effective_size(const std::vector<std::vector<unsigned char> >& stack)
+{
+    size_t esize = stack.size();
+
+    for (const auto& v : stack)
+    {
+        if (v.size() > MAX_SCRIPT_ELEMENT_SIZE) 
+            esize += (v.size() - 1) / MAX_SCRIPT_ELEMENT_SIZE;
+    }
+    return esize;
+}
+    
 bool EvalScript(std::vector<std::vector<unsigned char> >& stack, const CScript& script, unsigned int flags, const BaseSignatureChecker& checker, SigVersion sigversion, ScriptExecutionData& execdata, ScriptError* serror)
 {
     static const CScriptNum bnZero(0);
@@ -1239,7 +1252,7 @@ bool EvalScript(std::vector<std::vector<unsigned char> >& stack, const CScript&
             }
 
             // Size limits
-            if (stack.size() + altstack.size() > MAX_STACK_SIZE)
+            if (effective_size(stack) + effective_size(altstack) > MAX_STACK_SIZE)
                 return set_error(serror, SCRIPT_ERR_STACK_SIZE);
         }
     }



------------------------------

Message: 5
Date: Mon, 23 Oct 2023 13:26:06 -0400
From: Ryan Breen <ryan@breen.xyz>
To: L?o Haf <leohaf@orangepill.ovh>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <15A90517-83ED-4285-831A-46B8B3C6749A@breen.xyz>
Content-Type: text/plain; charset="utf-8"

Presumably the people using it feel it is an improvement. However you feel about it, Ordinals and Inscriptions are now a part of the Bitcoin ecosystem.

Whether Ordinals deserve a BIP is yet to be determined, but it doesn?t seem appropriate to try and force him to retract it. That solves nothing. If there is a reason this shouldn?t be a BIP, then that should be laid out as part of the process and formally rejected. Otherwise it should go through the normal process and be accepted.

As it is, leaving it in limbo and just hoping that it goes away is not a solution.

Thanks,

Ryan Breen
@ursuscamp

> On Oct 23, 2023, at 12:49?PM, L?o Haf via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> ?
> ? BIPs such as the increase in block size, drives-chains, colored coins, etc... were proposals for Bitcoin improvements. On the other hand, your BIP brings absolutely no improvement, on the contrary it is a regression, but you already know that.
> 
> I strongly invite you to retract or if the desire continues to push you to negatively affect the chain, to create OIPs or anything similar, as far as possible from the development of Bitcoin and real BIPs that improve Bitcoin.
> 
> L?o Haf. 
> 
>>> Le 23 oct. 2023 ? 10:23, Casey Rodarmor via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> a ?crit :
>>> 
>> ?
>> Dear List,
>> 
>> The Ordinals BIP PR has been sitting open for nine months now[0]. I've commented a few times asking the BIP editors to let me know what is needed for the BIP to either be merged or rejected. I've also reached out to the BIP editors via DM and email, but haven't received a response.
>> 
>> There has been much misunderstanding of the nature of the BIP process. BIPS, in particular informational BIPs, are a form of technical documentation, and their acceptance does not indicate that they will be included in any implementation, including Bitcoin Core, nor that they they have consensus among the community.
>> 
>> Preexisting BIPs include hard-fork block size increases, hard-fork proof-of-work changes, colored coin voting protocols, rejected soft fork proposals, encouragement of address reuse, and drivechain.
>> 
>> I believe ordinals is in-scope for a BIP, and am hoping to get the PR unstuck. I would appreciate feedback from the BIP editors on whether it is in-scope for a BIP, if not, why not, and if so, what changes need to be made for it to be accepted.
>> 
>> Best regards,
>> Casey Rodarmor
>> 
>> [0] https://github.com/bitcoin/bips/pull/1408
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/a218a362/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 41
********************************************
