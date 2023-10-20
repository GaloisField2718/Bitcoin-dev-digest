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

   1. Re: Examining ScriptPubkeys in Bitcoin Script (Brandon Black)
   2. Breaking change in calculation of hash_serialized_2 (Fabian)
   3. Re: Breaking change in calculation of	hash_serialized_2
      (Peter Todd)
   4. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Matt Morehouse)


----------------------------------------------------------------------

Message: 1
Date: Fri, 20 Oct 2023 07:19:06 -0700
From: Brandon Black <freedom@reardencode.com>
To: Rusty Russell <rusty@rustcorp.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <ZTKMWr5x_JjaLnIG@console>
Content-Type: text/plain; charset=us-ascii

On 2023-10-20 (Fri) at 14:10:37 +1030, Rusty Russell via bitcoin-dev wrote:
>         I've done an exploration of what would be required (given
> OP_TX/OP_TXHASH or equivalent way of pushing a scriptPubkey on the
> stack) to usefully validate Taproot outputs in Bitcoin Script.  Such
> functionality is required for usable vaults, at least.

So you're proposing this direction as an alternative to the more
constrained OP_UNVAULT that replaces a specific leaf in the taptree in a
specific way? I think the benefits of OP_UNVAULT are pretty big vs. a
generic construction (e.g. ability to unvault multiple inputs sharing
the same scriptPubkey to the same output).

> TL;DR: if we have OP_TXHASH/OP_TX, and add OP_MULTISHA256 (or OP_CAT),
> OP_KEYADDTWEAK and OP_LESS (or OP_CONDSWAP), and soft-fork weaken the
> OP_SUCCESSx rule (or pop-script-from-stack), we can prove a two-leaf
> tapscript tree in about 110 bytes of Script.  This allows useful
> spending constraints based on a template approach.

I agree that this is what is needed. I started pondering this in
response to some discussion about the benefits of OP_CAT or OP_2SHA256
for BitVM.

Personally I'd use OP_TAGGEDCATHASH that pops a tag (empty tag can be
special cased to plain sha256) and a number (n) of elements to hash,
then tagged-hashes the following 'n' elements from the stack.

Best,

--Brandon


------------------------------

Message: 2
Date: Fri, 20 Oct 2023 17:19:19 +0000
From: Fabian <fjahr@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Breaking change in calculation of
	hash_serialized_2
Message-ID:
	<kxXtwQMByYbMavS5P9a2tAUd8wz0yTUifost_txwTiQfNKTBtgdepLmAyV4XN6m4wY74cdZLX4EtsiEJ-jpZsnSxPIrCAN5wK8eK8xx1WGw=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hello list,

on Wednesday I found a potential malleability issue in the UTXO set dump files
generated for and used by assumeutxo [1]. On Thursday morning theStack had
found the cause of the issue [2]: A bug in the serialization of UTXOs for the
calculation of hash_serialized_2. This is the value used by Bitcoin Core to
check if the UTXO set loaded from a dump file matches what is expected. The
value of hash_serialized_2 expected for a particular block is hardcoded into
the chainparams of each chain.

Implications:
We have been working on a fix [3] for the serialization and aim to include it
in v26.0 (aimed to be released in November). The serialization must change
which means that all historical UTXO set hash results will change after you
upgrade your node to v26.0. To further highlight this, we will also increment
the version, i.e., the value returned in gettxoutset will be renamed to
hash_serialized_3.
It should also be noted that there were additional potentially problematic
issues found from fuzz testing by dergoegge which is why we decided to switch
the serialization completely rather than implementing a minimal fix. The
serialization format is now the same as used by MuHash.

How this may concern you:
1. If you are using hash_serialized_2 for any security critical purposes, you
should check if the bugs in the serialization code could cause issues for you.
You may switch to using hash_serialized_3 as soon as possible (or maybe
consider using MuHash).
2. If you are utilizing hash_serialized_2 for anything critical in your project
in general and require time to upgrade and adapt to the change described above,
please let us know. While we usually try to avoid breaking changes in our APIs without deprecation warning, we currently tend to think it is not necessary to
keep the buggy hash_serialized_2 around since we don?t know of any substantial
use cases and using it may even pose security risks. Furthermore, keeping the
old code around comes at some additional review and maintenance burden and may
lead to some delay in the release of v26.0. But we are happy to reconsider if
keeping hash_serialized_2 around holds serious value for downstream projects.

Feel free to reach out to me directly or comment in the PR [3] or here on the
list.

Cheers,
Fabian

[1] https://github.com/bitcoin/bitcoin/issues/28675
[2] https://github.com/bitcoin/bitcoin/issues/28675#issuecomment-1770389468[3] https://github.com/bitcoin/bitcoin/pull/28685
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/b18b6d1b/attachment-0001.html>

------------------------------

Message: 3
Date: Fri, 20 Oct 2023 17:34:28 +0000
From: Peter Todd <pete@petertodd.org>
To: Fabian <fjahr@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Breaking change in calculation of
	hash_serialized_2
Message-ID: <ZTK6JINSo6WyvJL0@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 05:19:19PM +0000, Fabian via bitcoin-dev wrote:
> Hello list,
> 
> on Wednesday I found a potential malleability issue in the UTXO set dump files
> generated for and used by assumeutxo [1]. On Thursday morning theStack had
> found the cause of the issue [2]: A bug in the serialization of UTXOs for the
> calculation of hash_serialized_2. This is the value used by Bitcoin Core to
> check if the UTXO set loaded from a dump file matches what is expected. The
> value of hash_serialized_2 expected for a particular block is hardcoded into
> the chainparams of each chain.

<snip>

> [1] https://github.com/bitcoin/bitcoin/issues/28675
> [2] https://github.com/bitcoin/bitcoin/issues/28675#issuecomment-1770389468[3] https://github.com/bitcoin/bitcoin/pull/28685

James made the following comment on the above issue:

> Wow, good find @fjahr et al. I wonder if there's any value in committing to a
> sha256sum of the snapshot file itself in the source code as a
> belt-and-suspenders remediation for issues like this.

Why *isn't* the sha256 hash of the snapshot file itself the canonical hash?
That would obviously eliminate any malleability issues. gettxoutsetinfo already
has to walk the entire UTXO set to calculate the hash. Making it simply
generate the actual contents of the dump file and calculate the hash of it is
the obvious way to implement this.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/95b1a84e/attachment-0001.sig>

------------------------------

Message: 4
Date: Fri, 20 Oct 2023 18:35:26 +0000
From: Matt Morehouse <mattmorehouse@gmail.com>
To: Peter Todd <pete@petertodd.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID:
	<CAGyamEVGe+z96Rc52V0j=a+He3frzhHEk_NPunXA-g1MwXXdGw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

I think if we apply this presigned fee multiplier idea to HTLC spends,
we can prevent replacement cycles from happening.

We could modify HTLC scripts so that *both* parties can only spend the
HTLC via presigned second-stage transactions, and we can always sign
those with SIGHASH_ALL.  This will prevent the attacker from adding
inputs to their presigned transaction, so (AFAICT) a replacement
cycling attack becomes impossible.

The tradeoff is more bookkeeping and less fee granularity when
claiming HTLCs on chain.

On Fri, Oct 20, 2023 at 11:04?AM Peter Todd via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> On Fri, Oct 20, 2023 at 10:31:03AM +0000, Peter Todd via bitcoin-dev wrote:
> > As I have suggested before, the correct way to do pre-signed transactions is to
> > pre-sign enough *different* transactions to cover all reasonable needs for
> > bumping fees. Even if you just increase the fee by 2x each time, pre-signing 10
> > different replacement transactions covers a fee range of 1024x. And you
> > obviously can improve on this by increasing the multiplier towards the end of
> > the range.
>
> To be clear, when I say "increasing the multiplier", I mean, starting with a
> smaller multiplier at the beginning of the range, and ending with a bigger one.
>
> Eg feebumping with fee increases pre-signed for something like:
>
>     1.1
>     1.2
>     1.4
>     1.8
>     2.6
>     4.2
>     7.4
>
> etc.
>
> That would use most of the range for smaller bumps, as a %, with larger % bumps
> reserved for the end where our strategy is changing to something more
> "scorched-earth"
>
> And of course, applying this idea properly to commitment transactions will mean
> that the replacements may have HTLCs removed, when their value drops below the
> fees necessary to get those outputs mined.
>
> Note too that we can sign simultaneous variants of transactions that deduct the
> fees from different party's outputs. Eg Alice can give Bob the ability to
> broadcast higher and higher fee txs, taking the fees from Bob's output(s), and
> Bob can give Alice the same ability, taking the fees from Alice's output(s). I
> haven't thought through how this would work with musig. But you can certainly
> do that with plain old OP_CheckMultisig.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 29
********************************************
