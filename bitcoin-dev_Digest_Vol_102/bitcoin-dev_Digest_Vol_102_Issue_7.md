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

   1. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Sat, 4 Nov 2023 07:26:24 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZUXyICh45JP6OnDu@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Nov 03, 2023 at 05:25:24AM +0000, Antoine Riard wrote:
> > To be clear, are you talking about anchor channels or non-anchor channels?
> > Because in anchor channels, all outputs other than the anchor outputs
> provided
> > for fee bumping can't be spent until the commitment transaction is mined,
> which
> > means RBF/CPFP isn't relevant.
> 
> I think the distinction is irrelevant here as pre-anchor channel if I have
> one spendable HTLC output spend and I gain knowledge of my counterparty
> commitment transaction from networks mempools, the spend is malleable and
> can be used as a CPFP. If you assume anchor channels, you have 2 anchor
> outputs as long both parties have balance outputs or pending HTLCs.
> 
> Though pre-anchor, legacy channels the counterparty commitment transaction
> will have to be attached with a fee under min mempool fee for the
> replacement cycling to happen, and let network congestion happen.

I think you are misunderstanding a key point to my OP_Expire proposal: because
the ability to spend the preimage branch of the HTLC goes away when the refund
branch becomes available, replacing cycling or any similar technique becomes
entirely irrelevant.

The situation where Carol prevents Bob from learning about the preimage in time
simply can't happen: either Carol collects the HTLC with knowledge of the
preimage, by spending it in a transaction mined prior to the expiration time
and ensuring that Bob learns the preimage from the blockchain itself. Or the
HTLC expires and Bob can use the refund branch at his leisure.

> I think the more interesting case is a future world with package relay
> deployed at the p2p level and anchor output on the lightning-side. Here the
> most advanced replacement as illustrated in the test can happen (where
> commitment has an anchor output - see L125).

Again, with OP_Expire, whether or not package relay or anything similar exists
is irrelevant. Replacement cycling is totally useless because there is a
defined time window in which the HTLC can be spent with the preimage, after
which only the refund branch can be used.

Indeed, with OP_Expire Lightning nodes will no longer need to monitor mempools
for preimages at all. If the preimage is used, it is guaranteed to end up in
the chain, and the Lightning node is guaranteed to see it provided they have
access to up-to-date blockchain data.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231104/58ccff27/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 7
*******************************************
