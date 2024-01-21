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

   1. Full-RBF Peering Bitcoin Core v26.0 Released (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Sat, 20 Jan 2024 21:33:39 +0000
From: Peter Todd <pete@petertodd.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Full-RBF Peering Bitcoin Core v26.0 Released
Message-ID: <Zaw8M5Dj46pdwMQm@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

Available from: https://github.com/petertodd/bitcoin/tree/full-rbf-v26.0

eg:

    git clone -b full-rbf-v26.0 https://github.com/petertodd/bitcoin.git

What is this? It's Bitcoin Core v26.0, with Antoine Riard's full-rbf peering
code, and some additional minor updates to it. This does two things for
full-rbf nodes:

1) Advertises a FULL_RBF service bit when mempoolfullrbf=1 is set.
2) Connects to four additional FULL_RBF peers.

Doing this ensures that a core group of nodes are reliably propagating full-rbf
replacements. We don't need everyone to run this. But it'd be helpful if more
people did.

As for why you should run full-rbf, see my blog post:

https://petertodd.org/2023/why-you-should-run-mempoolfullrbf

I'm already running v26.0 on a few nodes with v2transport=1 enabled. You should
too!

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240120/dad4bb55/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 24
********************************************
