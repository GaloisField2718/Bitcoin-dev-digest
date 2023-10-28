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
   2. Re: Ordinals BIP PR (alicexbt)
   3. Re: Examining ScriptPubkeys in Bitcoin Script (Rusty Russell)


----------------------------------------------------------------------

Message: 1
Date: Sat, 28 Oct 2023 04:32:13 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Ethan Heilman <eth3rs@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTwCLcjmuU4vkxTL@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Sat, Oct 21, 2023 at 01:08:03AM -0400, Ethan Heilman via bitcoin-dev wrote:
> We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
> https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki

If you're interested in making this available via inquisition, here's
a set of 3 patches that should allow it to be messed with on regtest:

  https://github.com/ajtowns/bitcoin/commits/202310-inq25-cat

Tests need updating and adding, however.

You might wish to compare with similar commits from the APO/CTV PRs at

  https://github.com/bitcoin-inquisition/bitcoin/pull/33
  https://github.com/bitcoin-inquisition/bitcoin/pull/34

It may be worth adding support for CSFS as well, if experimenting with
that is desirable, rather than having them as separate script-verify
flags and deployments.

> [1]: R. Pike and B. Kernighan, "Program design in the UNIX
> environment", 1983,
> https://harmful.cat-v.org/cat-v/unix_prog_design.pdf

"harmful cat", you say?

Cheers,
aj


------------------------------

Message: 2
Date: Fri, 27 Oct 2023 17:05:46 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<JrzK-LiMl1adxad-gJWpFNCIXg924YG9cqsginHU2zCgTeCEhvhExnL_E1_PdW8kZGnW-_-CEuS-tNWY0dHUi-lfBucjpLQknqtZUuA7MrA=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Peter,

> At that point, why are we bothering with numbers at all? If BIP #'s aren't
memorable, what is their purpose? Why not just let people publish ideas on
their own web pages and figure out what we're going to call those ideas on a
case-by-case basis.

I agree people can maintain BIPs in their own repositories. I will list all the 
BIPs that are not maintained in https://github.com/bitcoin/bips repository on 
https://bips.wiki

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Friday, October 27th, 2023 at 3:41 AM, Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> On Tue, Oct 24, 2023 at 03:56:55PM -0700, Olaoluwa Osuntokun via bitcoin-dev wrote:
> 
> > TL;DR: let's just use an automated system to assign BIP numbers, so we can
> > spend time on more impactful things.
> 
> 
> Yes, an easy way to do that is to use a mathematical function, like SHA256(<bip contents>)
> 
> or Pubkey(<bip author controlled secret key>).
> 
> 
> Of course, that's also silly, as we might as well use URLs at that point...
> 
> > IIUC, one the primary roles of the dedicated BIP maintainers is just to hand
> > out BIP numbers for documents. Supposedly with this privilege, the BIP
> > maintainer is able to tastefully assign related BIPs to consecutive numbers,
> > and also reserve certain BIP number ranges for broad categories, like 3xx
> > for p2p changes (just an example).
> > 
> > To my knowledge, the methodology for such BIP number selection isn't
> > published anywhere, and is mostly arbitrary. As motioned in this thread,
> > some perceive this manual process as a gatekeeping mechanism, and often
> > ascribe favoritism as the reason why PR X got a number immediately, but PR Y
> > has waited N months w/o an answer.
> > 
> > Every few years we go through an episode where someone is rightfully upset
> > that they haven't been assigned a BIP number after following the requisite
> > process. Most recently, another BIP maintainer was appointed, with the hope
> > that the second maintainer would help to alleviate some of the subjective
> > load of the position. Fast forward to this email thread, and it doesn't
> > seem like adding more BIP maintainers will actually help with the issue of
> > BIP number assignment.
> > 
> > Instead, what if we just removed the subjective human element from the
> > process, and switched to using PR numbers to assign BIPs? Now instead of
> > attempting to track down a BIP maintainer at the end of a potentially
> > involved review+iteration period, PRs are assigned BIP numbers as soon as
> > they're opened and we have one less thing to bikeshed and gatekeep.
> > 
> > One down side of this is that assuming the policy is adopted, we'll sorta
> > sky rocket the BIP number space. At the time of writing of this email, the
> > next PR number looks to be 1508. That doesn't seem like a big deal to me,
> > but we could offset that by some value, starting at the highest currently
> > manually assigned BIP number. BIP numbers would no longer always be
> > contiguous, but that's sort of already the case.
> > 
> > There's also the matter of related BIPs, like the segwit series (BIPs 141,
> > 142, 143, 144, and 145). For these, we can use a suffix scheme to indicate
> > the BIP lineage. So if BIP 141 was the first PR, then BIP 142 was opened
> > later, the OP can declare the BIP 142 is BIP 141.2 or BIP 141-2. I don't
> > think it would be too difficult to find a workable scheme.
> 
> 
> At that point, why are we bothering with numbers at all? If BIP #'s aren't
> memorable, what is their purpose? Why not just let people publish ideas on
> their own web pages and figure out what we're going to call those ideas on a
> case-by-case basis.
> 
> All this gets back to my original point: a functioning BIP system is
> inherently centralized and involves human gatekeepers who inevitably have to
> apply standards to approve BIPs. You can't avoid this as long as you want a BIP
> system.
> 
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 3
Date: Sat, 28 Oct 2023 15:19:30 +1030
From: Rusty Russell <rusty@rustcorp.com.au>
To: Anthony Towns <aj@erisian.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <87r0lfz6zp.fsf@rustcorp.com.au>
Content-Type: text/plain

Anthony Towns <aj@erisian.com.au> writes:
> On Fri, Oct 20, 2023 at 02:10:37PM +1030, Rusty Russell via bitcoin-dev wrote:
>>         I've done an exploration of what would be required (given
>> OP_TX/OP_TXHASH or equivalent way of pushing a scriptPubkey on the
>> stack) to usefully validate Taproot outputs in Bitcoin Script.  Such
>> functionality is required for usable vaults, at least.
>> 
>>         https://rusty.ozlabs.org/2023/10/20/examining-scriptpubkey-in-script.html
>> 
>> (If anyone wants to collaborate to produce a prototype, and debug my
>> surely-wrong script examples, please ping me!)
>> 
>> TL;DR: if we have OP_TXHASH/OP_TX, and add OP_MULTISHA256 (or OP_CAT),
>> OP_KEYADDTWEAK and OP_LESS (or OP_CONDSWAP), and soft-fork weaken the
>> OP_SUCCESSx rule (or pop-script-from-stack), we can prove a two-leaf
>> tapscript tree in about 110 bytes of Script.  This allows useful
>> spending constraints based on a template approach.
>
> I think there's two reasons to think about this approach:
>
>  (a) we want to do vault operations specifically, and this approach is
>      a good balance between being:
>        - easy to specify and implement correctly, and
>        - easy to use correctly.
>
>  (b) we want to make bitcoin more programmable, so that we can do
>      contracting experiments directly in wallet software, without needing
>      to justify new soft forks for each experiment, and this approach
>      provides a good balance amongst:
>        - opening up a wide range of interesting experiments,
>        - making it easy to understand the scope/consequences of opening up
>          those experiments,
>        - being easy to specify and implement correctly, and
>        - being easy to use correctly.
>
> Hopefully that's a fair summary? Obviously what balance is "good"
> is always a matter of opinion -- if you consider it hard to do soft
> forks, then it's perhaps better to err heavily towards being easy to
> specify/implement, rather than easy to use, for example.
>
> For (a) I'm pretty skeptical about this approach for vault operations
> -- it's not terribly easy to specify/implement (needing 5 opcodes, one
> of which has a dozen or so flags controlling how it behaves, then also
> needs to change the way OP_SUCCESS works), and it seems super complicated
> to use.

But AFAICT there are multiple perfectly reasonable variants of vaults,
too.  One would be:

1. master key can do anything
2. OR normal key can send back to vault addr without delay
3. OR normal key can do anything else after a delay.

Another would be:
1. normal key can send to P2WPKH(master)
2. OR normal key can send to P2WPKH(normal key) after a delay.

> By comparison, while the bip 345 OP_VAULT proposal also proposes 3 new
> opcodes (OP_CTV, OP_VAULT, OP_VAULT_RECOVER) [0], those opcodes can be
> implemented fairly directly (without requiring different semantics for
> OP_SUCCESS, eg) and can be used much more easily [1].

I'm interested in vaults because they're a concrete example I can get my
head around.  Not because I think they'll be widely used!  So I feel
that anyone who has the ability to protect two distinct keys, and make
two transactions per transfer is not a great candidate for optimization
or convenience.

> I'm not sure, but I think the "deferred check" setup might also
> provide additional functionality beyond what you get from cross-input
> introspection; that is, with it, you can allow multiple inputs to safely
> contribute funds to common outputs, without someone being able to combine
> multiple inputs into a tx where the output amount is less than the sum
> of all the contributions. Without that feature, you can mimic it, but
> only so long as all the input scripts follow known templates that you
> can exactly match.

Agreed, I don't think you would implement anything but 1:1 unvaulting in
bitcoin script, except as a party trick.

> So to me, for the vault use case, the
> TXHASH/MULTISHA256/KEYADDTWEAK/LESS/CAT/OP_SUCCESS approach just doesn't
> really seem very appealing at all in practical terms: lots of complexity,
> hard to use, and doesn't really seem like it works very well even after
> you put in tonnes of effort to get it to work at all?

Well, I found the vault BIP really hard to understand.  I think it wants
to be a new address format, not script opcodes.

I don't think spelling it out in script is actually that much more
complex to use, either.  "Use these templates".  And modulo
consolidation, I think it works as well.

> I think in the context of (b), ie enabling experimentation more generally,
> it's much more interesting. eg, CAT alone would allow for various
> interesting constraints on signatures ("you must sign this tx with the
> given R value -- so attempting to double spend, eg via a feebump, will
> reveal the corresponding private key"), and adding CSFS would allow you
> to include authenticated data in a script, eg market data sourced from
> a trusted oracle.

Oh, oracles like this are the first CSFS use case I've heard of that
doesn't seem like abusing signatures to do hashing; nice!

(Seems like there should be a way to do this without CSFS, but I can't
see it...)

> But even then, it still seems fairly crippled -- script is a very
> limited programming language, and it just isn't really very helpful
> if you want to do things that are novel. It doesn't allow you to (eg)
> loop over the inputs and select just the ones you're interested in, you
> need the opcode to do the looping for you, and that has to be hardcoded
> as a matter of consensus (eg, Steven Roose's TXHASH [2] proposal allows
> you to select the first-n inputs/outputs, but not the last-n).

Indeed, but I still think there's much room for improvement before a
replacement.  It's hard to compare the hobbled script we have today with
an alternative, since most interesting cases are impossible.

Cheers,
Rusty.


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 48
********************************************
