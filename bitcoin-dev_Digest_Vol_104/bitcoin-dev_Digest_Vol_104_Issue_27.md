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

   1. Re: One-Shot Replace-By-Fee-Rate (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Wed, 24 Jan 2024 04:44:14 +0000
From: Peter Todd <pete@petertodd.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <ZbCVnl8HbREQV5su@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Mon, Jan 22, 2024 at 10:52:01PM +0000, Peter Todd via bitcoin-dev wrote:
> An even simpler fix would be to just require that all unconfirmed inputs in a
> replacement come from the *same* replaced transaction. That would make certain
> rare, but economically viable, replacements infeasible. But it would definitely
> fix the issue.

FYI I've implemented this fix, and pure replace-by-fee-rate with a minimum 2x
fee-rate increate, in my Libre Relay fork:

https://github.com/petertodd/bitcoin/tree/libre-relay-v26.0

Similar to my full-RBF peering fork, it uses a new service bit to ensure it's
peering with other Libre Relay nodes to make transaction propagation actually
works.

I wouldn't call this a "public" release at this point. But people are welcome
to review the code and try it out. I have a few mainnet and testnet nodes
running it right now.

I'm *very* interested if anyone else can find any further exploits in the pure
replace-by-fee-rate code. I'm also interested to see if anyone bothers to spend
the money to do the well-known, and expensive, replace-by-fee-rate DoS attacks.

The fun thing about this release, is Libre Relay also removes the restrictions
on OP_Return, which I'm sure will make some people quite angry... So maybe
that'll give someone an incentive to attack it. :D I'm already sufficiently
well connected to get oversized OP_Return's mined. So if you want to do that
too, running a Libre Relay node will work.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240124/9f67da39/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 27
********************************************
