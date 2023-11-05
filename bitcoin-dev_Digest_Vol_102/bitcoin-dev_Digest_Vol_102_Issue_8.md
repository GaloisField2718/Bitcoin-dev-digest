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

   1. Re: [Mempool spam] Should we as developers reject
      non-standard Taproot transactions from full nodes?
      (ArmchairCryptologist)
   2. Cold channels and PathCoin redux (AdamISZ)


----------------------------------------------------------------------

Message: 1
Date: Sat, 04 Nov 2023 09:58:48 +0000
From: ArmchairCryptologist <ArmchairCryptologist@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Mempool spam] Should we as developers
	reject	non-standard Taproot transactions from full nodes?
Message-ID:
	<xpDas-5qF-ZRHkgqGiihf5vStfpq3Pjdk1fZeE7CifDHWnolhoRjd-wd50C1ymkVUgNxfL3NXN_XJb8lB-5I2CcdGHi8oOVmOjlA7_9F4mA=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

While I don't necessarily disagree about the block size limit, efforts to increase it in the past has been effectively stonewalled since, as it turns out, all you have to do to not increase it is nothing.

If we are looking to address the current mempool spam in particular, it looks to me that it isn't specifically caused by exploiting taproot to add large amounts of data to the blockchain, there are just a large amount of spam transactions creating dust and moving it around. To the best of my knowledge, this type of spam could to some extent be mitigated by adding a dynamic dust limit, where in addition to today's fixed limit of 546 sats, UTXOs are considered to be dust if they cannot be economically spent at the fee rate of the transaction creating it.

Of course, it complicates matters somehow that you cannot generally know how much data is required to spend a UTXO, especially with taproot, so you'd need to calculate it by assuming that it will require the typical amount of data for a basic UTXO. With the same assumptions used to define the original dust limit, Ignoring that segwit/taproot can be somewhat cheaper, that would be 182 sats per byte.

Say if a transaction has a fee rate of 100 sat/b - the dust limit for UTXOs this transaction creates would then be increased from 546 sats to 18200 sats. So if you want to spam the blockchain with dust, the higher you push the fees, the more sats you need to leave behind in each UTXO.

There are of course pros and cons to such an approach, and you could argue the need to cap it in various ways, but it feels to me that it would be worth considering, especially considering that it is mempool policy rather than consensus critical.

--
Best,
ArmchairCryptologist

------- Original Message -------
On Friday, November 3rd, 2023 at 11:15 AM, Brad Morrison via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> Right now, https://mempool.space/ indicates that there are about 105,000 unconfirmed transactions and that current memory usage is 795 mb of 300 mb.
> ...
> Expanding the block size is the simplest way to expand network capacity and lower transactional costs
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231104/b898413a/attachment-0001.html>

------------------------------

Message: 2
Date: Sat, 04 Nov 2023 16:16:35 +0000
From: AdamISZ <AdamISZ@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Cold channels and PathCoin redux
Message-ID:
	<BKDrklvNfkEmjjzz3M7CmLf74VFA2jYD-c0ozX27QfPAYMpLSAN2chSPfCRiotf8QhiPao6TWzYB-CX-3Xiqk4quAPcFfUsMLKG9gV5W8oQ=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi list,

I've recently spent a lot of time thinking about "PathCoin" ([1] - but I wouldn't recommend reading that *first*, for reasons that will become clear). [3]

I realized that my earlier conceptions were way too specific and there is a wide range of possibilities for transferring coins in this way. One in particular, really stood out, what I'm calling here "Cold channels" - the TLDR if you don't want to read the post is, "payment channels where there is no hot wallet requirement and payments to offline (store-and-forward e.g.) work, but the tradeoff is that you can only pay the whole channel capacity, i.e. fixed denomination". (note that that TLDR did *not* talk about routing, only a variant of a bidi payment channel).

I also would apologize in advance if, as very likely, much of what I'm saying here is well known. But it's better explain in detail, just in case:

CTLCs
======

First I want to focus on this primitive:

(A and CLTV) OR ( S_A and CTV)

Here A is a pubkey for signing (OP_CHECKSIG style, say), and S_A is just an image of a secret that A holds (as is well known, locking to *just* a preimage is never safe, but here we don't do that).

Calling this from now on "CTLC" for "Covenant Time Locked Contract". As for BIP119 vs alternatives, I've been coding with that but I don't *think* anything I say here is relying on that specific version of a covenant op code. It will continue to be "CTV" here.

CTLC chain
======

By chaining those together for a set of participants (e.g. A,B,C,D,E) we can essentially control the flow of money a bit like airlocks - it moves forward specifically when transferring the secret preimages of S_A, S_B, ... :

(A and CLTV) OR ( S_A and CTV) -> (B and CLTV) OR ( S_B and CTV) -> (C and CLTV) OR ( S_C and CTV) -> (D and CLTV) OR ( S_D and CTV) -> E


Optimistic PathCoin
======

This naturally gives us the first, and I think simplest, variant of PathCoin: A can *spontaneously* choose a path A-B-C-D-E (assuming pubkeys are known, and the secrets S_X can easily be done with tweaks, let's say), set up the CTV chain, fund the coin and then effect payment to B by sending S_A, who can send to C with sending S_B etc etc. This variant is still nearly as limited in value as what I originally suggested, with different tradeoffs. Coin denomination fixed, path fixed, *but* it doesn't require a penalty, and doesn't require an initial coordination/signing session. The negative, if "spontaneous", is pretty nasty: whoever finally spends the coin on chain has to broadcast the CTLC chain, so you don't save chain space and the privacy gain is not really so hot either.

Instructive to compare that with Rubin's congestion control concept: here, the spends are not all guaranteed. On the negative side, here, we cannot build trees instead of single paths, because we have a double spend risk from privately shared secrets between colluders.

Re the negatives of "if spontaneous" - we will get into this next.

Cold channels
======

The simplest kind of path (that requires least coordination) is just a 2-cycle: A-B-A-B-A-B etc. This pattern exists, but is fairly uncommon, in a customer-service provider scenario, and, for a typical case, the service provider will be an online server so we don't need some kind of offline version of a payment channel there.

However what if it is more of a p2p relationship between two non-professional entities? (As is often seen in the real world Lightning network). We lift the above CTLC chain "offchain" in the usual manner:

Fund a 2 of 2 (AB) multisig, then presign the initial funding of the start of the CTLC chain. (Here is where "if spontaneous" is not true - A and B must coordinate to *setup*, and to *close*, but not to pay).

To close cooperatively, overwrite the CTLC chain to avoid broadcasting the whole chain uh .. on chain :)

This construction looks attractive because:

1. Payments do not require the receiver to be online, because state update is unilateral. They could be sent (literally just a 32 byte secret in the simplest case) e.g. in a store and forward mechanism, or handed over on a USB stick. The crappy home node that falls offline for 24 hours will not fail (at least, if we use long time locks for such "cold channels").
2. There is no hot signing-wallet requirement after setup (though, the two parties do need to defend their corresponding secret preimages of S_{[A,B]_n} from each other).

What about routing? I haven't thought about it, probably typical atomicity techniques do apply, but this structure is limited with its fixed denomination, so I'm not sure if there is or isn't something to pursue there.

Re: that fixed denom., perhaps using a lot of such channels at once is useful to at least ameliorate that.

Private pathcoin
======

For completeness I see the original penalty-based setup as in [1] as being interesting specifically in that (a) ownership is not timelocked, (b) it sorta(?) has much better privacy because spends of the pathcoin itself are pure p2tr keypath spends, and (c) there are interesting hybrids, as explained in the comment to the gist [2]. But I'll keep these ideas to one side, as I think the optimistic variant, especially offchain in a channel, are the most interesting.

Cheers,
AdamISZ/ waxwing

[1] https://gist.github.com/AdamISZ/b462838cbc8cc06aae0c15610502e4da
[2] https://gist.github.com/AdamISZ/b462838cbc8cc06aae0c15610502e4da?permalink_comment_id=4748805#gistcomment-4748805
[3] I should also note I did code up a proof of concept of the original version here: https://github.com/AdamISZ/pathcoin-poc




------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 8
*******************************************
