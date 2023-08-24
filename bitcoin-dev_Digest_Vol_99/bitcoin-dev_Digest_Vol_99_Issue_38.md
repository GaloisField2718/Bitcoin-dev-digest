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

   1. Nucleus: Capital-efficient multipeer Lightning	payment
      channels (Atomic Mr Nuclear)


----------------------------------------------------------------------

Message: 1
Date: Sun, 20 Aug 2023 14:25:07 +0000
From: Atomic Mr Nuclear <atomic-mr-nuclear@onionmail.org>
To: bitcoin-dev@lists.linuxfoundation.org,
	lightning-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Nucleus: Capital-efficient multipeer Lightning
	payment channels
Message-ID: <1a7c7373-5511-d5f4-4aa9-8c19c3c0303d@onionmail.org>
Content-Type: text/plain; charset="utf-8"

Dear community,

In the attachment you will find a new proposal for Lightning multipeer payment
channels which provides better capital efficiency (no inbound liquidity is
required) and liveness (up to half of peers may go offline and the channel can
continue to operate). It also doesn't rely on a penalty mechanism and doesn't
require the use of atomic swaps (HTLC, PTLC etc) and routed payments for scaling
(peers can directly join the multipeer channel instead of establishing a network
of channels locking in the liquidity).




----


Atomic Mr Nuclear
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230820/bfb41b20/attachment.html>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: Nucleus.pdf
Type: application/pdf
Size: 322440 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230820/bfb41b20/attachment.pdf>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 38
*******************************************
