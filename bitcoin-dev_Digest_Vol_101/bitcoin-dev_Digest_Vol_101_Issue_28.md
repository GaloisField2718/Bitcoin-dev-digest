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

   1. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Peter Todd)
   2. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Peter Todd)
   3. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Peter Todd)
   4. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Jochen Hoenicke)


----------------------------------------------------------------------

Message: 1
Date: Fri, 20 Oct 2023 10:31:03 +0000
From: Peter Todd <pete@petertodd.org>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <ZTJW59wQ/4WLZt2h@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Oct 17, 2023 at 10:34:04AM +0000, ZmnSCPxj via bitcoin-dev wrote:
> Good morning Antoine et al.,
> 
> Let me try to rephrase the core of the attack.
> 
> There exists these nodes on the LN (letters `A`, `B`, and `C` are nodes, `==` are channels):
> 
>     A ===== B ===== C
> 
> `A` routes `A->B->C`.
> 
> The timelocks, for example, could be:
> 
>    A->B timeelock = 144
>    B->C timelock = 100
> 
> The above satisfies the LN BOLT requirements, as long as `B` has a `cltv_expiry_delta` of 44 or lower.
> 
> After `B` forwards the HTLC `B->C`, C suddenly goes offline, and all the signed transactions --- commitment transaction and HTLC-timeout transactions --- are "stuck" at the feerate at the time.
>
> At block height 100, `B` notices the `B->C` HTLC timelock is expired without `C` having claimed it, so `B` forces the `B====C` channel onchain.
> However, onchain feerates have risen and the commitment transaction and HTLC-timeout transaction do not confirm.

The problem here is we're failing to use RBF.

As I have suggested before, the correct way to do pre-signed transactions is to
pre-sign enough *different* transactions to cover all reasonable needs for
bumping fees. Even if you just increase the fee by 2x each time, pre-signing 10
different replacement transactions covers a fee range of 1024x. And you
obviously can improve on this by increasing the multiplier towards the end of
the range.

Increasing per-tx (temporary) storage and bandwidth costs by ~10x or even ~100x
is not a big deal in the context of a highly scalable protocol like Lightning.

There is zero reason why the B->C transactions should be getting stuck. This is
a major failing of the Lightning protocol that should be fixed. And of course,
this fix should be applied to other aspects of the lightning protocol, such as
channel opens, etc.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/9b2cee76/attachment-0001.sig>

------------------------------

Message: 2
Date: Fri, 20 Oct 2023 10:47:38 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID: <ZTJays5mDFvDqkkB@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Oct 17, 2023 at 02:11:20AM +0100, Antoine Riard wrote:
> > I think if you want people to understand this exploit, you need to
> explain in more detail how we have a situation where two different parties
> can spend the same HTLC txout, without the first party having the right to
> spend it via their knowledge of the HTLC-preimage.
> 
> If I'm correctly understanding your question, you're asking why we have a
> situation where the spend of a HTLC output can be in competition between 2
> channel counterparties.

No, you are not correctly understanding it.

It's obvious that an HTLC output can be in competition between 2 different
parties. Obviously, the HTLC-preimage doesn't expire. The problem is you
haven't explained why the party with the HTLC pre-image should not *remain* the
party with the *right* to spend that output, even after the timeout branch
becomes another possible way to spend it.

> LN commitment transactions have offered HTLC outputs where a counterparty
> Alice is pledging to her other counterparty Caroll the HTLC amount in
> exchange of a preimage (and Caroll signature).
> 
> After the expiration of the HTLC timelock, if the HTLC has not been claimed
> on-chain by Caroll, Alice can claim it back with her signature (and the
> pre-exchanged Caroll signature).
> 
> The exploit works actually in Caroll leveraging her HTLC-preimage
> transaction as a replace-by-fee of Alice's HTLC-timeout _after_ the
> expiration of the timelock, the HTLC-preimage transaction staying consensus
> valid.

That's precisely my point re: you not properly explaining the problem. If
Caroll has the HTLC-preimage, she has the right to spend it. You need to
explain why her right to spend that HTLC-preimage output should expire.

If anything, the way you've explained it sounds like Bob has stolen the output
from Caroll by virtue of the fact that Caroll wasn't able to spend the
HTLC-preimage output in time.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/f4e147f2/attachment-0001.sig>

------------------------------

Message: 3
Date: Fri, 20 Oct 2023 11:03:43 +0000
From: Peter Todd <pete@petertodd.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <ZTJej/ipIl5hZIUn@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 10:31:03AM +0000, Peter Todd via bitcoin-dev wrote:
> As I have suggested before, the correct way to do pre-signed transactions is to
> pre-sign enough *different* transactions to cover all reasonable needs for
> bumping fees. Even if you just increase the fee by 2x each time, pre-signing 10
> different replacement transactions covers a fee range of 1024x. And you
> obviously can improve on this by increasing the multiplier towards the end of
> the range.

To be clear, when I say "increasing the multiplier", I mean, starting with a
smaller multiplier at the beginning of the range, and ending with a bigger one.

Eg feebumping with fee increases pre-signed for something like:

    1.1
    1.2
    1.4
    1.8
    2.6
    4.2
    7.4

etc.

That would use most of the range for smaller bumps, as a %, with larger % bumps
reserved for the end where our strategy is changing to something more
"scorched-earth"

And of course, applying this idea properly to commitment transactions will mean
that the replacements may have HTLCs removed, when their value drops below the
fees necessary to get those outputs mined.

Note too that we can sign simultaneous variants of transactions that deduct the
fees from different party's outputs. Eg Alice can give Bob the ability to
broadcast higher and higher fee txs, taking the fees from Bob's output(s), and
Bob can give Alice the same ability, taking the fees from Alice's output(s). I
haven't thought through how this would work with musig. But you can certainly
do that with plain old OP_CheckMultisig.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/4e6d1615/attachment-0001.sig>

------------------------------

Message: 4
Date: Fri, 20 Oct 2023 13:18:46 +0200
From: Jochen Hoenicke <hoenicke@gmail.com>
To: Peter Todd <pete@petertodd.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID:
	<CANYHNmLb3_JRSu1Di4LNtVs7Z=jsPQ0T+-0LznE9Ma++Xiqbew@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

I found the original explanation a bit confusing.  As I understand it,
the attack starts by double-spending the timeout HTLC transaction of
the victim with a pre-image revealing HTLC transaction.  This itself
is not an attack: the victim can then use the pre-image to receive its
incoming HTLC safely, because its timeout hasn't expired yet.  The
trick is now that the attacker double-spends their own transaction
before it hits the chain (the third transaction only double-spends
some attacker controlled input used also by the pre-image HTLC
transaction).  In ideal condition, the pre-image transaction is never
seen by the victim and the victim still doesn't know the pre-image.
The attacker may only attack the mempool of the mining nodes. The
victim may not even know that their transaction was replaced and are
only confused why it didn't get mined.

On Fri, 20 Oct 2023 at 12:47, Peter Todd via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> On Tue, Oct 17, 2023 at 02:11:20AM +0100, Antoine Riard wrote:
> > > I think if you want people to understand this exploit, you need to
> > explain in more detail how we have a situation where two different parties
> > can spend the same HTLC txout, without the first party having the right to
> > spend it via their knowledge of the HTLC-preimage.
> >
> > If I'm correctly understanding your question, you're asking why we have a
> > situation where the spend of a HTLC output can be in competition between 2
> > channel counterparties.
>
> No, you are not correctly understanding it.
>
> It's obvious that an HTLC output can be in competition between 2 different
> parties. Obviously, the HTLC-preimage doesn't expire. The problem is you
> haven't explained why the party with the HTLC pre-image should not *remain* the
> party with the *right* to spend that output, even after the timeout branch
> becomes another possible way to spend it.
>
> > LN commitment transactions have offered HTLC outputs where a counterparty
> > Alice is pledging to her other counterparty Caroll the HTLC amount in
> > exchange of a preimage (and Caroll signature).
> >
> > After the expiration of the HTLC timelock, if the HTLC has not been claimed
> > on-chain by Caroll, Alice can claim it back with her signature (and the
> > pre-exchanged Caroll signature).
> >
> > The exploit works actually in Caroll leveraging her HTLC-preimage
> > transaction as a replace-by-fee of Alice's HTLC-timeout _after_ the
> > expiration of the timelock, the HTLC-preimage transaction staying consensus
> > valid.
>
> That's precisely my point re: you not properly explaining the problem. If
> Caroll has the HTLC-preimage, she has the right to spend it. You need to
> explain why her right to spend that HTLC-preimage output should expire.
>
> If anything, the way you've explained it sounds like Bob has stolen the output
> from Caroll by virtue of the fact that Caroll wasn't able to spend the
> HTLC-preimage output in time.
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

End of bitcoin-dev Digest, Vol 101, Issue 28
********************************************
