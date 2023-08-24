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

   1. Re: Concrete MATT opcodes (Salvatore Ingala)


----------------------------------------------------------------------

Message: 1
Date: Wed, 9 Aug 2023 10:38:48 +0200
From: Salvatore Ingala <salvatore.ingala@gmail.com>
To: Johan Tor?s Halseth <johanth@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Concrete MATT opcodes
Message-ID:
	<CAMhCMoEoSiGPBczQerBe1TDJvo2Gkf4gbXOPUayKkNLsC_y4SQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Johan,

Thanks a lot for the comments, and the independent implementation!

> - For the opcode parameter ordering, it feels unnatural for the two
> tweaks (data, taptree) to be separated by the internal key. A more
> natural ordering of parameters IMO would be (of course this is all
> subjective):
> <data> <taptree> <internalkey> <index> <flags> OP_CCV.
>
> If you disagree, I would love some rationale for the ordering you
> chose! (looks like you also changed it again after your last post?).

The main concern for the reordering was to put <data> at the bottom,
as that's typically passed via the witness stack.

I put the <index> right next, as I suspect there are use cases for
specifying via the witness what is the input index where a certain
(CCV-encumbered) UTXO is to be found, or which output should funds
be sent to, instead of hard-coding this in the script. This might
help in designing contracts that are more flexible in the way they
are spent, for example by allowing batching their transactions.

Instead, I expect the other parameters to almost always be hardcoded,
or propagated from the current input with the <-1> special values.

I agree that your ordering is more aesthetically pleasing, though.

> I'm wondering what other use cases you had in mind for the deferred
> output amount check? Maybe I have missed something, but if not it
> would perhaps be better to leave out the amount preservation check, or
> go the extra mile and propose a more powerful amount introspection
> machinery.

Yes, the deferred output amount check is not enough for coinpools;
however, it comes at no cost if we have a <flags> parameter anyway,
as OP_2 (value for CCV_IGNORE_OUTPUT_AMOUNT) is a single byte opcode.

The intent of preserving amounts for many-to-one contracts (vaults),
or the one-to-one cases (channels, any 2-party contract, etc.) seems
common enough to deserve 1 bit in the flags, IMHO.
Efforts to define and add explicit introspection to cover your
(exciting!) use cases can proceed independently, but I don't think
they would nullify the advantages of this (optional) feature of CCV.

Best,
Salvatore
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230809/72053c9c/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 20
*******************************************
