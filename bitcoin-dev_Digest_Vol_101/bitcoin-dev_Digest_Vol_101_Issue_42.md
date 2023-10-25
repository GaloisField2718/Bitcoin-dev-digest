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

   1. Re: Proposed BIP for OP_CAT (Andrew Poelstra)
   2. Re: Proposed BIP for OP_CAT (Steven Roose)
   3. Re: Ordinals BIP PR (Olaoluwa Osuntokun)


----------------------------------------------------------------------

Message: 1
Date: Tue, 24 Oct 2023 13:05:56 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Rusty Russell <rusty@rustcorp.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTfBNGipc2O+ojvr@camus>
Content-Type: text/plain; charset="us-ascii"

On Tue, Oct 24, 2023 at 02:15:49PM +1030, Rusty Russell wrote:
> Andrew Poelstra <apoelstra@wpsoftware.net> writes:
> > I had a similar thought. But my feeling is that replacing the stack
> > interpreter data structure is still too invasive to justify the benefit.
> >
> > Also, one of my favorite things about this BIP is the tiny diff.
> 
> To be fair, this diff is even smaller than the OP_CAT diff :)
>

Oh, look at that :). For some reason I had it in my head that looping
like this would mess up the asymptotics and meaningfully harm
performance. But no, it just involves adding (at most) 1000 numbers.
Which is unlikely to even be measurable.

> Though I had to strongly resist refactoring, that interpreter code
> needs a good shake!  Using a class for the stack is worth doing anyway
> (macros, really??).
>

Hah, agreed, but it still makes my hands sweat to think about refactoring
that file.

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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231024/f806cd7b/attachment-0001.sig>

------------------------------

Message: 2
Date: Tue, 24 Oct 2023 20:47:23 +0100
From: Steven Roose <steven@roose.io>
To: vjudeu via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <c76d5c5f-091a-8c41-f1e7-74774c9607c5@roose.io>
Content-Type: text/plain; charset="utf-8"; Format="flowed"

I agree that there is no reason not to use OP_SUCCESS126, i.e. the 
original OP_CAT opcode 0x7e. In many codebases, for example in Core, 
there might be two OP_CAT constants than which might be confusing.

On 10/22/23 09:58, vjudeu via bitcoin-dev wrote:
> > This opcode would be activated via a soft fork by redefining the 
> opcode OP_SUCCESS80.
> Why OP_SUCCESS80, and not OP_SUCCESS126? When there is some existing 
> opcode, it should be reused. And if OP_RESERVED will ever be 
> re-enabled, I think it should behave in the same way, as in 
> pre-Taproot, so it should "Mark transaction as invalid unless occuring 
> in an unexecuted OP_IF branch". Which means, "<condition> OP_VERIFY" 
> should be equivalent to "<condition> OP_NOTIF OP_RESERVED OP_ENDIF".
>
>
> On 2023-10-21 07:09:13 user Ethan Heilman via bitcoin-dev 
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>     Hi everyone,
>
>     We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
>     https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki
>
>     OP_CAT was available in early versions of Bitcoin. It was disabled as
>     it allowed the construction of a script whose evaluation could create
>     stack elements exponential in the size of the script. This is no
>     longer an issue in the current age as tapscript enforces a maximum
>     stack element size of 520 Bytes.
>
>     Thanks,
>     Ethan
>
>     ==Abstract==
>
>     This BIP defines OP_CAT a new tapscript opcode which allows the
>     concatenation of two values on the stack. This opcode would be
>     activated via a soft fork by redefining the opcode OP_SUCCESS80.
>
>     When evaluated the OP_CAT instruction:
>     # Pops the top two values off the stack,
>     # concatenate the popped values together,
>     # and then pushes the concatenated value on the top of the stack.
>
>     OP_CAT fails if there are less than two values on the stack or if a
>     concatenated value would have a combined size of greater than the
>     maximum script element size of 520 Bytes.
>
>     ==Motivation==
>     Bitcoin tapscript lacks a general purpose way of combining objects on
>     the stack restricting the expressiveness and power of tapscript. For
>     instance this prevents among many other things the ability to
>     construct and evaluate merkle trees and other hashed data structures
>     in tapscript. OP_CAT by adding a general purpose way to concatenate
>     stack values would overcome this limitation and greatly increase the
>     functionality of tapscript.
>
>     OP_CAT aims to expand the toolbox of the tapscript developer with a
>     simple, modular and useful opcode in the spirit of Unix[1]. To
>     demonstrate the usefulness of OP_CAT below we provide a non-exhaustive
>     list of some usecases that OP_CAT would enable:
>
>     * Tree Signatures provide a multisignature script whose size can be
>     logarithmic in the number of public keys and can encode spend
>     conditions beyond n-of-m. For instance a transaction less than 1KB in
>     size could support tree signatures with a thousand public keys. This
>     also enables generalized logical spend conditions. [2]
>     * Post-Quantum Lamport Signatures in Bitcoin transactions. Lamport
>     signatures merely requires the ability to hash and concatenate values
>     on the stack. [3]
>     * Non-equivocation contracts [4] in tapscript provide a mechanism to
>     punish equivocation/double spending in Bitcoin payment channels.
>     OP_CAT enables this by enforcing rules on the spending transaction's
>     nonce. The capability is a useful building block for payment channels
>     and other Bitcoin protocols.
>     * Vaults [5] which are a specialized covenant that allows a user to
>     block a malicious party who has compromised the user's secret key from
>     stealing the funds in that output. As shown in A. Poelstra, "CAT
>     and Schnorr Tricks II", 2021,
>     https://www.wpsoftware.net/andrew/blog/cat-and-schnorr-tricks-ii.html
>     OP_CAT is sufficent to build vaults in Bitcoin.
>     * Replicating CheckSigFromStack  A. Poelstra, "CAT and Schnorr
>     Tricks I", 2021,
>     https://medium.com/blockstream/cat-and-schnorr-tricks-i-faf1b59bd298
>       which would allow the creation of simple covenants and other
>     advanced contracts without having to presign spending transactions,
>     possibly reducing complexity and the amount of data that needs to be
>     stored. Originally shown to work with Schnorr signatures, this result
>     has been extended to ECDSA signatures. [6]
>
>     The opcode OP_CAT was available in early versions of Bitcoin. However
>     OP_CAT was removed because it enabled the construction of a script for
>     which an evaluation could have memory usage exponential in the size of
>     the script.
>     For instance a script which pushed an 1 Byte value on the stack then
>     repeated the opcodes OP_DUP, OP_CAT 40 times would result in a stack
>     value whose size was greater than 1 Terabyte. This is no longer an
>     issue because tapscript enforces a maximum stack element size of 520
>     Bytes.
>
>     ==Specification==
>
>     Implementation
>
>        if (stack.size() < 2)
>          return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>        valtype vch1 = stacktop(-2);
>        valtype vch2 = stacktop(-1);
>
>        if (vch1.size() + vch2.size() > MAX_SCRIPT_ELEMENT_SIZE)
>            return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>
>        valtype vch3;
>        vch3.reserve(vch1.size() + vch2.size());
>        vch3.insert(vch3.end(), vch1.begin(), vch1.end());
>        vch3.insert(vch3.end(), vch2.begin(), vch2.end());
>
>        popstack(stack);
>        popstack(stack);
>        stack.push_back(vch3);
>
>     The value of MAX_SCRIPT_ELEMENT_SIZE is 520 Bytes == Reference Implementation == [Elements](https://github.com/ElementsProject/elements/blob/master/src/script/interpreter.cpp#L1043) ==References== [1]: R. Pike and B. Kernighan, "Program design in the UNIX environment", 1983,https://harmful.cat-v.org/cat-v/unix_prog_design.pdf  [2]: P. Wuille, "Multisig on steroids using tree signatures", 2015,https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html  [3]: J. Rubin, "[bitcoin-dev] OP_CAT Makes Bitcoin Quantum Secure [was CheckSigFromStack for Arithmetic Values]", 2021,https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html  [4]: T. Ruffing, A. Kate, D. Schr?der, "Liar, Liar, Coins on Fire: Penalizing Equivocation by Loss of Bitcoins", 2015,https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.727.6262&rep=rep1&type=pdf  [5]: M. Moser, I. Eyal, and E. G. Sirer, Bitcoin Covenants,http://fc16.ifca.ai/bitcoin/papers/MES16.pdf  [6]: R. Li
 nus, "Covenants with CAT and ECDSA", 2023,https://gist.github.com/RobinLinus/9a69f5552be94d13170ec79bf34d5e85#file-covenants_cat_ecdsa-md  _______________________________________________ bitcoin-dev mailing listbitcoin-dev@lists.linuxfoundation.org  https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231024/65e82fa8/attachment-0001.html>

------------------------------

Message: 3
Date: Tue, 24 Oct 2023 15:56:55 -0700
From: Olaoluwa Osuntokun <laolu32@gmail.com>
To: Luke Dashjr <luke@dashjr.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CAO3Pvs_uUtCfhayU=3LCtpNGtkcDr=H0AM65bhNJcTMuBzWn_w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

TL;DR: let's just use an automated system to assign BIP numbers, so we can
spend time on more impactful things.

IIUC, one the primary roles of the dedicated BIP maintainers is just to hand
out BIP numbers for documents. Supposedly with this privilege, the BIP
maintainer is able to tastefully assign related BIPs to consecutive numbers,
and also reserve certain BIP number ranges for broad categories, like 3xx
for p2p changes (just an example).

To my knowledge, the methodology for such BIP number selection isn't
published anywhere, and is mostly arbitrary. As motioned in this thread,
some perceive this manual process as a gatekeeping mechanism, and often
ascribe favoritism as the reason why PR X got a number immediately, but PR Y
has waited N months w/o an answer.

Every few years we go through an episode where someone is rightfully upset
that they haven't been assigned a BIP number after following the requisite
process.  Most recently, another BIP maintainer was appointed, with the hope
that the second maintainer would help to alleviate some of the subjective
load of the position.  Fast forward to this email thread, and it doesn't
seem like adding more BIP maintainers will actually help with the issue of
BIP number assignment.

Instead, what if we just removed the subjective human element from the
process, and switched to using PR numbers to assign BIPs? Now instead of
attempting to track down a BIP maintainer at the end of a potentially
involved review+iteration period, PRs are assigned BIP numbers as soon as
they're opened and we have one less thing to bikeshed and gatekeep.

One down side of this is that assuming the policy is adopted, we'll sorta
sky rocket the BIP number space. At the time of writing of this email, the
next PR number looks to be 1508. That doesn't seem like a big deal to me,
but we could offset that by some value, starting at the highest currently
manually assigned BIP number. BIP numbers would no longer always be
contiguous, but that's sort of already the case.

There's also the matter of related BIPs, like the segwit series (BIPs 141,
142, 143, 144, and 145). For these, we can use a suffix scheme to indicate
the BIP lineage. So if BIP 141 was the first PR, then BIP 142 was opened
later, the OP can declare the BIP 142 is BIP 141.2 or BIP 141-2. I don't
think it would be too difficult to find a workable scheme.

Thoughts?

-- Laolu


On Mon, Oct 23, 2023 at 11:35?AM Luke Dashjr via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

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
> > On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via bitcoin-dev
> wrote:
> >> I have _not_ requested a BIP for OpenTimestamps, even though it is of
> much
> >> wider relevance to Bitcoin users than Ordinals by virtue of the fact
> that much
> >> of the commonly used software, including Bitcoin Core, is timestamped
> with OTS.
> >> I have not, because there is no need to document every single little
> protocol
> >> that happens to use Bitcoin with a BIP.
> >>
> >> Frankly we've been using BIPs for too many things. There is no avoiding
> the act
> >> that BIP assignment and acceptance is a mark of approval for a
> protocol. Thus
> >> we should limit BIP assignment to the minimum possible: _extremely_
> widespread
> >> standards used by the _entire_ Bitcoin community, for the core mission
> of
> >> Bitcoin.
> >>
> > This would eliminate most wallet-related protocols e.g. BIP69 (sorted
> > keys), ypubs, zpubs, etc. I don't particularly like any of those but if
> > they can't be BIPs then they'd need to find another spec repository
> > where they wouldn't be lost and where updates could be tracked.
> >
> > The SLIP repo could serve this purpose, and I think e.g. SLIP39 is not a
> BIP
> > in part because of perceived friction and exclusivity of the BIPs repo.
> > But I'm not thrilled with this situation.
> >
> > In fact, I would prefer that OpenTimestamps were a BIP :).
> >
> >> It's notable that Lightning is _not_ standardized via the BIP process.
> I think
> >> that's a good thing. While it's arguably of wide enough use to warrent
> BIPs,
> >> Lightning doesn't need the approval of Core maintainers, and using their
> >> separate BOLT process makes that clear.
> >>
> > Well, LN is a bit special because it's so big that it can have its own
> > spec repo which is actively maintained and used.
> >
> > While it's technically true that BIPs need "approval of Core maintainers"
> > to be merged, the text of BIP2 suggests that this approval should be a
> > functionary role and be pretty-much automatic. And not require the BIP
> > be relevant or interesting or desireable to Core developers.
> >
> >
> >
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231024/5a564471/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 42
********************************************
