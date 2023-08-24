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

   1. Conceptual package relay using taproot annex (Joost Jager)


----------------------------------------------------------------------

Message: 1
Date: Mon, 5 Jun 2023 09:57:46 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Conceptual package relay using taproot annex
Message-ID:
	<CAJBJmV9_nvCveynxs8UXmXyx=OTCYqSEKk73cn-TLNHWgo1q-g@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi,

Before starting, I would like to state that I do not necessarily support
the implementation of the idea I'm about to present, but I think it's worth
mentioning as it might inspire different use cases or provoke some debate.
I believe that out-of-band relay is a more preferable and efficient way to
get transaction packages to miners while p2p package relay is under
development.

Let's consider the situation where we have a parent transaction A that pays
0 sat/b (for example a lightning commitment transaction), and a fee bumping
child transaction B. These transactions currently cannot reach miners.

We can, however, conceive a workaround. Let's introduce a third transaction
C, crafted to contain the raw transactions A and B in a taproot annex. A
commit/reveal style inscription could also be used instead, but I think it
would be more complicated and less efficient.

To ensure propagation, transaction C would pay sufficient fees. Also it
would use at least one of the same fee contributing inputs as transaction
B, but obviously not any inputs from A.

Miners, upon receiving transaction C, could detect the embedded
transactions A and B in the annex and immediately submit them to their
mempool as a transaction package. This transaction package (A+B) would then
replace transaction C and could be included in a block for mining.

It's of course important to ensure that the combined package of A+B is more
attractive to miners than the C transaction. The extra weight of the
embedded transactions in C helps with this. Also it is worth noting that
the fees for C will never be paid because it has been replaced. Thus there
are no extra costs for using this package relay scheme, unless perhaps the
weight of A+B is very low and B needs to pay a higher fee rate than
necessary to ensure replacement of C.

If not all miners adopt this incentive-compatible replacement, there's a
chance transaction C ends up being mined. This is likely less probable if
the fee rate for C is kept to a minimum. If transaction C is indeed mined,
the operation can be retried with a modified B and C, though the fees paid
for the initial transaction C would be forfeited.

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230605/0468684e/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 8
******************************************
