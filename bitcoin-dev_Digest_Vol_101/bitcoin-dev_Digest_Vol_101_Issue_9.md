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

   1. Re: Proposed BIP for MuSig2 PSBT Fields (Jonas Nick)


----------------------------------------------------------------------

Message: 1
Date: Thu, 12 Oct 2023 07:43:21 +0000
From: Jonas Nick <jonasd.nick@gmail.com>
To: Anthony Towns <aj@erisian.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Andrew Chow
	<lists@achow101.com>
Subject: Re: [bitcoin-dev] Proposed BIP for MuSig2 PSBT Fields
Message-ID: <fd7bf294-8f5a-48fc-a415-1f1706b51434@gmail.com>
Content-Type: text/plain; charset=UTF-8; format=flowed

It is true that BIP 327 ("MuSig2") does not include adaptor signatures. The
rationale behind this decision was as follows:
- the BIP is already long and complicated enough without adaptor signatures; it
   should be possible to propose a separate adaptor signature BIP on top in a
   modular fashion
- as far as I know, there's no security proof except for a hard-to-follow sketch
   that I wrote a few years ago [0]
- at the time, there seemed to be a higher demand for single-signer adaptor
   signatures

In spite of the missing specification, we added some version of adaptor
signatures to the libsecp256k1-zkp MuSig2 module in order to allow
experimentation.

As for standardizing MuSig2 adaptor signatures, it seems noteworthy that there
exist alternative designs to the implementation in the libsecp256k1-zkp module:
the current libsecp256k1-zkp PR for (single-signer) Schnorr adaptor signatures
[1] uses a slightly different API. Instead of sending the adaptor point along
with the adaptor signature, the point is extracted from an adaptor signature.
This simplifies the API and reduces communication at the cost of making batch
verification of multiple adaptor sigs impossible.

[0] https://github.com/BlockstreamResearch/scriptless-scripts/pull/24
[1] https://github.com/BlockstreamResearch/secp256k1-zkp/pull/268


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 9
*******************************************
