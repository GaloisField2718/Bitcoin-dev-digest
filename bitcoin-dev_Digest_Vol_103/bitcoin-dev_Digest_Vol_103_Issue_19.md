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

   1. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Wed, 20 Dec 2023 21:11:28 +0000
From: Peter Todd <pete@petertodd.org>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID: <ZYNYgBovvwodqSuZ@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Wed, Dec 20, 2023 at 03:16:25PM -0500, Greg Sanders wrote:
> Hi Peter,
> 
> Thanks for taking the time to understand the proposal and give thoughtful
> feedback.
> 
> With this kind of "static" approach I think there are fundamental
> limitations because
> the user has to commit "up front" how large the CPFP later will have to be.
> 1kvB
> is an arbitrary value that is two orders of magnitude less than the
> possible package
> size, and allows fairly flexible amounts of inputs(~14 taproot inputs
> IIRC?) to effectuate a CPFP.

Why would you need so many inputs to do a CPFP if they all have to be
confirmed? The purpose of doing a CPFP is to pay fees to get another
transaction mined. Unless you're in some degenerate, unusual, situation where
you've somehow ended up with just some dust left in your wallet, dust that is
barely worth its own fees to spend, one or maybe two UTXOs are going to be
sufficient for a fee payment.

I had incorrectly thought that V3 transctions allowed for a single up-to 1000vB
transaction to pay for multiple parents at once. But if you can't do that, due
to the restriction on unconfirmed inputs, I can't see any reason to have such a
large limit.

> I'd like something much more flexible, but we're barely at whiteboard stage
> for alternatives and
> they probably require more fundamental work. So within these limits, we
> have to pick some number,
> and it'll have tradeoffs.
> 
> When I think of "pinning potential", I consider not only the parent size,
> and not
> only the maximum child size, but also the "honest" child size. If the honest
> user does relatively poor utxo management, or the commitment transaction
> is of very high value(e.g., lots of high value HTLCs), the pin is
> essentially zero.
> If the honest user ever only have one utxo, then the "max pin" is effective
> indeed.

Which is the situation you would expect in the vast majority of cases.

> > Alice would have had to pay a 2.6x higher fee than
> expected.
> 
> I think that's an acceptable worst case starting point, versus the status
> quo which is ~500-1000x+.

No, the status quo is signed anchors, like Lightning already has with anchor
channels. Those anchors could still be zero-valued. But as long as there is a
signature associated with them, pinning isn't a problem as only the intended
party can spend them.

Note BTW that existing Lightning anchor channels inefficiently use two anchor
outputs when just one is sufficient:

    https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-December/004246.html
    [Lightning-dev] The remote anchor of anchor channels is redundant
    Peter Todd, Dec 13th, 2023

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231220/86d81212/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 19
********************************************
