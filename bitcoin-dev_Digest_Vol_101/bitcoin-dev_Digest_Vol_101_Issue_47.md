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

   1. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Peter Todd)
   2. Re: Examining ScriptPubkeys in Bitcoin Script (Anthony Towns)
   3. Re: Ordinals BIP PR (Alexander F. Moser)


----------------------------------------------------------------------

Message: 1
Date: Fri, 27 Oct 2023 00:43:30 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID: <ZTsHsn5s/wswxlIo@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Sat, Oct 21, 2023 at 09:05:35PM +0100, Antoine Riard via bitcoin-dev wrote:
> In the meanwhile, lightning experts have already deployed mitigations which
> are hardening the lightning ecosystem significantly in face of simple or
> medium attacks. More advanced attacks can only be mounted if you have
> sufficient p2p and mempool knowledge as was pointed out by other bitcoin
> experts like Matt or Peter (which take years to acquire for average bitcoin
> developers) and the months of preparation to attempt them.

To be clear, I am not making any claims about how easy this attack is to pull
off. Indeed, there are probably even cases where it happens by accident. Eg
imagine a node with a HTLC-preimage that happens to be offline and then online
at the right time to broadcast a HTLC-preimage redemption transaction with a
higher fee than the timeout transaction. If the other node happens to go
offline at the right time, after broadcasting the timeout transaction, it may
not notice the HTLC-preimage in the mempool, and thus fail to redeem it.

OP_Expire would help avoid this situation, by making it impossible to redeem
the HTLC-preimage after the timeout.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231027/a49f8a34/attachment-0001.sig>

------------------------------

Message: 2
Date: Fri, 27 Oct 2023 17:00:36 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Rusty Russell <rusty@rustcorp.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <ZTtgFPG4tTeZMnYn@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Fri, Oct 20, 2023 at 02:10:37PM +1030, Rusty Russell via bitcoin-dev wrote:
>         I've done an exploration of what would be required (given
> OP_TX/OP_TXHASH or equivalent way of pushing a scriptPubkey on the
> stack) to usefully validate Taproot outputs in Bitcoin Script.  Such
> functionality is required for usable vaults, at least.
> 
>         https://rusty.ozlabs.org/2023/10/20/examining-scriptpubkey-in-script.html
> 
> (If anyone wants to collaborate to produce a prototype, and debug my
> surely-wrong script examples, please ping me!)
> 
> TL;DR: if we have OP_TXHASH/OP_TX, and add OP_MULTISHA256 (or OP_CAT),
> OP_KEYADDTWEAK and OP_LESS (or OP_CONDSWAP), and soft-fork weaken the
> OP_SUCCESSx rule (or pop-script-from-stack), we can prove a two-leaf
> tapscript tree in about 110 bytes of Script.  This allows useful
> spending constraints based on a template approach.

I think there's two reasons to think about this approach:

 (a) we want to do vault operations specifically, and this approach is
     a good balance between being:
       - easy to specify and implement correctly, and
       - easy to use correctly.

 (b) we want to make bitcoin more programmable, so that we can do
     contracting experiments directly in wallet software, without needing
     to justify new soft forks for each experiment, and this approach
     provides a good balance amongst:
       - opening up a wide range of interesting experiments,
       - making it easy to understand the scope/consequences of opening up
         those experiments,
       - being easy to specify and implement correctly, and
       - being easy to use correctly.

Hopefully that's a fair summary? Obviously what balance is "good"
is always a matter of opinion -- if you consider it hard to do soft
forks, then it's perhaps better to err heavily towards being easy to
specify/implement, rather than easy to use, for example.

For (a) I'm pretty skeptical about this approach for vault operations
-- it's not terribly easy to specify/implement (needing 5 opcodes, one
of which has a dozen or so flags controlling how it behaves, then also
needs to change the way OP_SUCCESS works), and it seems super complicated
to use.

By comparison, while the bip 345 OP_VAULT proposal also proposes 3 new
opcodes (OP_CTV, OP_VAULT, OP_VAULT_RECOVER) [0], those opcodes can be
implemented fairly directly (without requiring different semantics for
OP_SUCCESS, eg) and can be used much more easily [1].

[0] Or perhaps 4, if OP_REVAULT were to be separated out from OP_VAULT, cf
    https://github.com/bitcoin/bips/pull/1421#discussion_r1357788739

[1] https://github.com/jamesob/opvault-demo/blob/57f3bb6b8717acc7ce1eae9d9d8a2661f6fa54e5/main.py#L125-L133

I'm not sure, but I think the "deferred check" setup might also
provide additional functionality beyond what you get from cross-input
introspection; that is, with it, you can allow multiple inputs to safely
contribute funds to common outputs, without someone being able to combine
multiple inputs into a tx where the output amount is less than the sum
of all the contributions. Without that feature, you can mimic it, but
only so long as all the input scripts follow known templates that you
can exactly match.

So to me, for the vault use case, the
TXHASH/MULTISHA256/KEYADDTWEAK/LESS/CAT/OP_SUCCESS approach just doesn't
really seem very appealing at all in practical terms: lots of complexity,
hard to use, and doesn't really seem like it works very well even after
you put in tonnes of effort to get it to work at all?



I think in the context of (b), ie enabling experimentation more generally,
it's much more interesting. eg, CAT alone would allow for various
interesting constraints on signatures ("you must sign this tx with the
given R value -- so attempting to double spend, eg via a feebump, will
reveal the corresponding private key"), and adding CSFS would allow you
to include authenticated data in a script, eg market data sourced from
a trusted oracle.

But even then, it still seems fairly crippled -- script is a very
limited programming language, and it just isn't really very helpful
if you want to do things that are novel. It doesn't allow you to (eg)
loop over the inputs and select just the ones you're interested in, you
need the opcode to do the looping for you, and that has to be hardcoded
as a matter of consensus (eg, Steven Roose's TXHASH [2] proposal allows
you to select the first-n inputs/outputs, but not the last-n).

[2] https://github.com/bitcoin/bips/pull/1500

I've said previously [3] that I think using a lisp variant would
be a promising solution here: you can replace script's "two stacks
of byte-strings" with "(recursive) lists of byte-strings", and go
from a fairly limited language, to a fairly complete one. I've been
experimenting with this on and off since then [4], and so far I haven't
seen anything much to dissuade me from that view. I think you can get
a pretty effective language with perhaps 43 opcodes [5] (compared to
script's ~60 active opcodes), and I don't think you need to do anything
too fancy to implement it.

[3] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-March/020036.html
[4] https://github.com/ajtowns/lisp-play/
[5] https://github.com/ajtowns/lisp-play/blob/5975870423f9dace902ef42208b965f9d8a0f005/btclisp.py#L738

Here's an example. I've included a "CSFS" equivalent opcode, namely
"(bip340_verify pk msg sig)" that validates a signature per BIP340,
and also a "(bip342_txmsg)" opcode that generates a "msg" corresponding
to the BIP 342 "Signature Validation" spec (just calling the bitcoind
core test framework code), which then allows me to verify existing
signatures on existing transactions via lisp code, rather than executing
the actual script.

But what if we wanted to experiment with a new SIGHASH mode? For that,
I've added an OP_TX like opcode, '(tx N)' that allows you to select
various information about the tx by choosing N -- '(tx 1)' gives you the
locktime, '(tx 10)' gives you your input's nSequence, '(tx (10 . 3))'
gives you the nSequence of the 4th input, eg. With that, it's possible
to select whichever bits of the transaction you like, in whatever order
you like, and pass the results through the '(sha256)' opcode, then pass
that into the signature check.

Unlike the OP_TXHASH proposals and the like, it's possible (though perhaps
not *easy*) to exactly mimic existing hash constructs, eg "(bip342_txmsg)"
(for SIGHASH_ALL) can be constructed manually via:

ENV=(a (i 14 '(a 8 8 12 (+ 10 '1) (- 14 '1) (cat 3 (a 12 10))) '3))

  ^-- (basically a for loop, so that "(a 1 1 'X '0 K)" will
       invoke "X" with values [0, K), and cat the results
       together; used with K=(tx '2) to do inputs, and (tx '3) to
       dou outputs)

PROGRAM=(a '(sha256 4 4 '0x00 6 3) (sha256 '\"TapSighash\") (cat '0x00 (tx '0) (tx '1) (sha256 (a 1 1 '(cat (tx (c '11 1)) (tx (c '12 1))) '0 (tx '2) 'nil)) (sha256 (a 1 1 '(tx (c '15 1)) '0 (tx '2) 'nil)) (sha256 (a 1 1 '(a '(cat (strlen 1) 1) (tx (c '16 '0))) '0 (tx '2) 'nil)) (sha256 (a 1 1 '(tx (c '10 1)) '0 (tx '2) 'nil)) (sha256 (a 1 1 '(cat (tx (c '20 1)) (a '(cat (strlen 1) 1) (tx (c '21 1)))) '0 (tx '3) 'nil)) (i (tx '7) '0x03 '0x01) (substr (cat (tx '4) '0x00000000) 'nil '4) (i (tx '7) (sha256 (a '(cat (strlen 1) 1) (tx '7))) 'nil)) (cat (tx '6) '0x00 '0xffffffff))

  ^-- (sha256's the sha256 of TapSighash twice, then the epoch, then
       the sigmsg, then the extension; with the SIGHASH_ALL logic
       being hardcoded)

That's obviously not easy to read, but it's also essentially programming
in assembler, and would be much improved by having a higher-level
macro-enabled lisp variation that allows you to define your own
symbols/variable names, and translate that down to the raw code. (Or
even just having a parser that allows you to add comments, I guess)

What I've implemented is essentially an eager interpretor with some tail
call optimisations to allow memory to be freed up a bit earlier. I think
it would be better to do it as a properly lazy iinterpretor though --
that way you can actually have the same memory efficiency as streaming
sha256 operators provide, even with the additional flexibility provided
by iteration/recursion/function calls.

There are various other tricks that aren't done in my python testbed,
eg encoding/decoding lists as a byte stream rather than a parenthesised
string; working out whether string comparison should be normal or reversed
(so that you can comapre proof-of-work) or both, providing other crypto
ops like ecdsa, doing bignum maths rather than just uint64, keeping track
of allocations when an exception occurs, providing an easy way to tell
how much computation will be required to evaluate an input script and
inflate the tx's weight correspondingly if necessary, etc.

I've also only done fairly toy-level problems: factorial and fibonacci
calculations, reimplementing an existing sighash, etc. I think doing
TLUV or VAULT or graftroot should be feasible (at least given opcodes
to provide secp256k1 tweaks and deferred-checks), but haven't actually
done it.

Anyway, this seems to me to be a much more promising approach for
experimentation than trying to fit everything into script's square hole
[6], and perhaps also more promising than Simplicity for the reasons
discussed at the end of [3]. Once you have the nicer structure that a
lisp-like language provides, compared to script, I think OP_TX, OP_CAT,
OP_CSFS etc all end up working pretty great.

[6] https://twitter.com/TiredActor/status/1609641593836822530

Cheers,
aj


------------------------------

Message: 3
Date: Fri, 27 Oct 2023 11:39:44 +0200
From: "Alexander F. Moser" <am@alexmoser.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <15AD6E27-D6C7-4848-B961-A313BBFFB396@alexmoser.com>
Content-Type: text/plain; charset=utf-8

A mostly self-managed scheme without exploding number spaces and half-decent quality control:

New ideas and proposals-in-development are in a draft/discussion state without any assigned or reserved BIP ordinal and remain as such until the following three conditions are true:

1 - author(s) consider the proposal final and want to promote it to a BIP.
Purpose: quality ensured by reputation 
Risk: Expectations, Experience, Ego

2 - enough non-author interactions with the draft exist. This can be platform agnostic, with ?interactions? meaning comments, non-author contributors, likes, stars, threads,.. and ?enough? meaning flat thresholds, a function of various factors, a combination of the two or nothing specific at all. 
Purpose: quality ensured by many 
Risk: heated discussions on stupid topics and spam inflate interactions 

3 - no other drafts exist that fulfill condition 1 and 2 and seek the ordinal ?lastBIP#+1?. 
Purpose: avoiding coincidental concurrency issues and fights over esoteric numbers. 
Risk: resolutions may need moderation and can be tedious 

Draft promotions are done in batches at e.g. every quadruple-zero ending block number (xx0000) - a bit more often than once a quarter or more often at e.g every 2016 blocks (~2w) at difficulty adjustment. 



Fairly straightforward and simple methodology, but should still provide - in an ideal world - enough framework for proposers to self manage fully. In realistic worlds, we can use BIP maintainers to moderate and protect the process. 

Condition 2 ?Interactions? could be changed to ?Enough non-authors consider proposal final? to ensure more quality by enticing co-responsibility, but it?d need a new approval process, which is more annoying than soft-defining required levels of community engagement and relying on the authors for common sense. 

Best,
A


On 27.10.2023, at 00:12, Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

?On Tue, Oct 24, 2023 at 03:56:55PM -0700, Olaoluwa Osuntokun via bitcoin-dev wrote:
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
_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 47
********************************************
