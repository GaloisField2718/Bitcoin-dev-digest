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

   1. Re: Merkleize All The Things (Salvatore Ingala)


----------------------------------------------------------------------

Message: 1
Date: Sun, 28 May 2023 12:24:14 +0200
From: Salvatore Ingala <salvatore.ingala@gmail.com>
To: Johan Tor?s Halseth <johanth@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Merkleize All The Things
Message-ID:
	<CAMhCMoHSonS2_wcCZYH9FhC5B5UCgf26JPhkK13pZCbo3ZO7JQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Johan,

Exciting to finally see some merkleization, which was only confined
within the meme, up to this point!

> A simpler way IMO, would be to make OP_CICV and OP_COCV symmetrical:
> Have OP_CICV take an optional taproot and do the same check as is
> done for the output: Q == tweak(tweak(X,D), T).

I think that's an excellent suggestion, which I was already exploring
for a different purpose: bringing externally signed data onto the
stack. My goal there was to allow eltoo-style replacement.

Until recently, I thought that a clean/efficient version of eltoo
would require OP_CHECKSIGFROMSTACK or ANYPREVOUT. However, extending
OP_CHECKINPUTCONTRACTVERIFY to enable introspection of other inputs
allows a reasonable workaround: producing a separate UTXO signed with
ANYONECANPAY, with the required data embedded as usual. Spending that
UTXO together with the channel's UTXO allows one to get that data
on the stack (with its signature already checked by consensus rules).
I drafted this idea in a gist [1].

Remark: it still seems easier (and probably slightly more efficient)
to build eltoo replacement with CSFS or APO in addition to MATT
opcodes.

A possible semantics for OP_CHECKINPUTCONTRACTVERIFY could then be
exactly symmetrical to that of OP_CHECKOUTPUTCONTRACTVERIFY, with
the exception that the special input index -1 would represent the
current input.

Pushing this further, another option that could be be worth exploring
is to have a single OP_CHECK_IN_OUT_CONTRACT_VERIFY opcode, with the
same semantics as OP_CHECKOUTPUTCONTRACTVERIFY from [2], but with an
additional `flags` argument, which is a bitmap where:
- the lowest-significant bit determines if the index refers to inputs
  or outputs (where input index -1 refers to the current input)
- the second bit specifies if amounts should be preserved with
  deferred checks as described in [2] (only applicable to outputs)
- other bits are OP_SUCCESS and reserved for future behaviors.

This would make the opcodes 1-2 bytes larger, but might allow greater
flexibility, and keep some room for future extensions.

> 2.To make fully functioning CoinPools, one would need functionality
> similar to OP_MERKLESUB[4]: remove some data from the merkle tree,
> and remove a key from the aggregated internal key.

It seems likely that efficient use of the taproot internal pubkey with
"dynamic key aggregation" is not possible with the current semantics
(unless one ventures into the fraud proof machinery, which seems
overkill!).

However, in constructions with MATT opcodes, I would never expect the
need for data to be stored in the taptree. In particular, for the case
of CoinPools, the pubkeys of the members could also be stored in the
embedded data, having a single "unilateral withdrawal" tapleaf.
Removing a key would then amount to replacing it with a fixed NUMS key
and computing the new root (re-using the same Merkle proof).
Note that this is not a lot costlier than using a tapleaf per user:
instead of paying the cost for the Merkle proof in the control block,
you pay for it explicitly in the Script witness.

Therefore, I would expect there to be reasonable CoinPools designs
without additional opcodes ? but I am only moderately confident as
this is beyond the level of sophistication I've been exploring so far.

Best,
Salvatore

[1] - https://gist.github.com/bigspider/041ebd0842c0dcc74d8af087c1783b63
[2] -
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021588.html
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230528/e5be3369/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 63
*******************************************
