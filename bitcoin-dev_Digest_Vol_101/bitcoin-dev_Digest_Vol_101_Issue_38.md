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

   1. Re: [Lightning-dev] OP_Expire and Coinbase-Like	Behavior:
      Making HTLCs Safer by Letting Transactions Expire Safely (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Mon, 23 Oct 2023 11:10:56 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] OP_Expire and Coinbase-Like
	Behavior: Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<o2Dp_FkSCCwB6Mo9dePXgvxwQeKcmDwK_fNK6bhHPrsYIC6KaoeTtfHh8kv2NGHqkJhppNmEvRZGTly1Zs3Of1gIfl76iNQgCZaNJ-bJqgE=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi all,

This was discussed partially on the platform formerly known as twitter, but an alternate design goes like this:

* Add an `nExpiryTime` field in taproot annex.
  * This indicates that the transaction MUST NOT exist in a block at or above the height specified.
  * Mempool should put txes buckets based on `nExpiryTime`, and if the block is reached, drop all the buckets with `nExpiryTime` less than that block height.
* Add an `OP_CHECKEXPIRYTIMEVERIFY` opcode, mostly similar in behavior to `OP_EXPIRE` proposed by Peter Todd:
  * Check if `nExpiryTime` exists and has value equal or less than the stack top.

The primary difference is simply that while Peter proposes an implicit field for the value that `OP_EXPIRE` will put in `CTransaction`, I propose an explicit field for it in the taproot annex.

The hope is that "explicit is better than implicit" and that the design will be better implemented as well by non-Bitcoin-core implementations, as the use of tx buckets is now explicit in treating the `nExpiryTime` field.

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 38
********************************************
