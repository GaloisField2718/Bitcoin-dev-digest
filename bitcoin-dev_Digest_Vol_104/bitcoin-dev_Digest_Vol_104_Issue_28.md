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

   1. CheckTemplateVerify Does Not Scale Due to UTXO's Required For
      Fee Payment (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Wed, 24 Jan 2024 19:31:07 +0000
From: Peter Todd <pete@petertodd.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's Required For Fee Payment
Message-ID: <ZbFle6n0Zu3yUV8o@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

CheckTemplateVerify(1) is a proposed covenant opcode that commits to the
transaction that can spend an output. Namely, # of inputs, # of outputs,
outputs hash, etc. In practice, in many if not most CTV use-cases intended to
allow multiple parties to share a single UTXO, it is difficult to impossible to
allow for sufficient CTV variants to cover all possible fee-rates. It is
expected that CTV would be usually used with anchor outputs to pay fees; by
creating an input of the correct size in a separate transaction and including
it in the CTV-committed transaction; or possibly, via a transaction sponsor
soft-fork.

This poses a scalability problem: to be genuinely self-sovereign in a protocol
with reactive security, such as Lightning, you must be able to get transactions
mined within certain deadlines. To do that, you must pay fees. All of the
intended exogenous fee-payment mechanisms for CTV require users to have at
least one UTXO of suitable size to pay for those fees.

This requirement for all users to have a UTXO to pay fees negates the
efficiency of CTV-using UTXO sharing schemes, as in an effort to share a UTXO,
CTV requires each user to have an extra UTXO. The only realistic alternative is
to use a third party to pay for the UTXO, eg via a LN payment, but at that
point it would be more efficient to pay an out-of-band mining fee. That of
course is highly undesirable from a mining centralization perspective.(2)

Recommendations: CTV in its current form be abandoned as design foot-gun. Other
convenant schemes should be designed to work well with replace-by-fee, to avoid
requirements for extra UTXOs, and to maximize on-chain efficiency.

1) https://github.com/bitcoin/bips/blob/deae64bfd31f6938253c05392aa355bf6d7e7605/bip-0119.mediawiki
2) https://petertodd.org/2023/v3-transactions-review#anchor-outputs-are-a-danger-to-mining-decentralization

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240124/0d0368b7/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 28
********************************************
