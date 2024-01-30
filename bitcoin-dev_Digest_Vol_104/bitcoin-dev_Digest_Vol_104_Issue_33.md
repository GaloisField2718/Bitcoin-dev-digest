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

   1. Re: CheckTemplateVerify Does Not Scale Due to UTXO's Required
      For Fee Payment (Peter Todd)
   2. Re: [Lightning-dev] CheckTemplateVerify Does Not	Scale Due to
      UTXO's Required For Fee Payment (ZmnSCPxj)
   3. Re: [Lightning-dev] CheckTemplateVerify Does Not	Scale Due to
      UTXO's Required For Fee Payment (ZmnSCPxj)
   4. Re: [Lightning-dev] CheckTemplateVerify Does Not Scale Due to
      UTXO's Required For Fee Payment (Anthony Towns)
   5. Re: [Lightning-dev] CheckTemplateVerify Does Not Scale Due to
      UTXO's Required For Fee Payment (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Tue, 30 Jan 2024 04:49:57 +0000
From: Peter Todd <pete@petertodd.org>
To: jlspc <jlspc@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's Required For Fee Payment
Message-ID: <Zbh/9fKrnid/psA/@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Thu, Jan 25, 2024 at 05:49:26PM +0000, jlspc wrote:
> Hi Peter,
> 
> If feerate-dependent timelocks (FDTs) (1) are supported, it would be possible to use CTV to define a transaction with a fixed fee and no anchor outputs, as long as it's racing against a transaction with an FDT.

Fee-rate-dependant timelocks have obvious issues around manipulation of
observed fee-rates by miners. It not unreasonable to say they assume miners are
honest, which is a significant weakening of the economic incentive-based
security model we usually assume in Bitcoin.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240130/f9ee5e19/attachment-0001.sig>

------------------------------

Message: 2
Date: Tue, 30 Jan 2024 05:07:16 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: bitcoin-dev@lists.linuxfoundation.org, Lightning Dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] CheckTemplateVerify Does
	Not	Scale Due to UTXO's Required For Fee Payment
Message-ID:
	<FPf9XHCyxV96ABG154D8WapYmEE8XVFWqpQXBXz7p21xjdOk1Ho_lC4IpUznFbhleS7g_kKhUqsU0gtMT06_zo6B9heKyHfp1P1zfMWkjmA=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8






Sent with Proton Mail secure email.

On Tuesday, January 30th, 2024 at 4:38 AM, Peter Todd <pete@petertodd.org> wrote:

> On Tue, Jan 30, 2024 at 04:12:07AM +0000, ZmnSCPxj wrote:
> 
> > Peter Todd proposes to sign multiple versions of offchain transactions at varying feerates.
> > However, this proposal has the issue that if you are not the counterparty paying for onchain fees (e.g. the original acceptor of the channel, as per "initiator pays" principle), then you have no disincentive to just use the highest-feerate version always, and have a tiny incentive to only store the signature for the highest-feerate version to reduce your own storage costs slightly.
> 
> 
> You are incorrect. Lightning commitments actually come in two different
> versions, for the local and remote sides. Obviously, I'm proposing that fees be
> taken from the side choosing to sign and broadcast the transaction. Which is
> essentially no different from CPFP anchors, where the side choosing to get the
> transaction mined pays the fee (though with anchors, it is easy for both sides
> to choose to contribute, but in practice this almost never seems to happen in
> my experience running LN nodes).

There is a reason why I mention "initiator pays", and it is because the channel opener really ought to pay for onchain fees in general.

For example, I could mount the following attack:

1.  I already have an existing LN node on the network.
2.  I wait for a low-feerate time.
3.  I spin up a new node and initiate a channel funding to a victim node.
4.  I empty my channel with the victim node, sending out my funds to my existing LN node.
5.  I retire my new node forever.

This forces the victim node to use its commitment tx.

If the onchain fee for the commitment tx is paid for by who holds the commitment tx (as in your proposal) then I have forced the victim node to pay an onchain fee.

This is why the initial design for openv1 is "initiator pays".
In the above attack scenario, the commitment tx held by the victim node, under "initiator pays", has its onchain fee paid by me, thus the victim is not forced to pay the unilateral close fee, I am the one forced to pay it.
They do still need to pay fees to get their now-onchain funds back into Lightning, but at least more of the onchain fees (the fees to unilaterally close the channel with the now-dead node) is paid by the attacker.

On the other hand, it may be possible that "initiator pays" can be dropped.
In this attack scenario, the victim node should really require a non-zero reserve anyway that is proportional to the channel size, so that the attacker needs to commit some funds to the victim until the victim capitulates and unilaterally closes.
In addition, to repeat this attack, I need to keep opening channels to the victim and thus pay onchain fees for the channel open.

So it may be that your proposal is sound; possibly the "initiator pays" advantage in this attack scenario is small enough that we can sacrifice it for multi-fee-version.

I should note that under Decker-Russell-Osuntokun the expectation is that both counterparties hold the same offchain transactions (hence why it is sometimes called "LN-symmetry").
However, there are two ways to get around this:

1.  Split the fee between them in some "fair" way.
    Definition of "fair" wen?
2.  Create an artificial asymmetry: flip a bit of `nSequence` for the update+state txes of one counterparty, and have each side provide signatures for the tx held by its counterparty (as in Poon-Dryja).
    This lets you force that the party that holds a particular update+state tx is the one that pays fees.

> > In addition, it is also incentive-incompatible for the party that pays onchain fees to withhold signatures for the higher-fee versions, because if you are the party who does not pay fees and all you hold are the complete signatures for the lowest-fee version (because the counterparty does not want to trust you with signatures for higher-fee versions because you will just abuse it), then you will need anchor outputs again to bump up the fee.
> 
> 
> That is also incorrect. If the protocol demands multiple fee variants exist,
> the state of the lightning channel simply doesn't advance until all required
> fee-variants are provided. Withholding can't happen any more than someone could
> "withhold" a state by failing to provide the last byte of a commitment
> transaction: until the protocol state requirements have been fufilled in full,
> the previous state remains in effect.

No, I am referring to a variation of your proposal where the side paying the fees in "initiator pays" gets full signatures for all feerate-versions but the other side gets only the full signatures for the lowest-fee version.

If you can build the multi-version proposal with both sides contributing fees or with the one exiting the channel paying the fee, then this variation is unnecessary and you can ignore this paragraph.

Regards,
ZmnSCPxj


------------------------------

Message: 3
Date: Tue, 30 Jan 2024 05:17:04 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org, Lightning Dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] CheckTemplateVerify Does
	Not	Scale Due to UTXO's Required For Fee Payment
Message-ID:
	<pohquEzgZZA_d4N8NGyF0RNOYNQUn1mEoYLsawgmKL1r_oWXfK2Y4D7VfaK47b2RQ9KNvdsv_pIKahSXyJpWHTHshv_0XJi-jgMo6paN0mI=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


> I should note that under Decker-Russell-Osuntokun the expectation is that both counterparties hold the same offchain transactions (hence why it is sometimes called "LN-symmetry").
> However, there are two ways to get around this:
> 
> 1. Split the fee between them in some "fair" way.
> Definition of "fair" wen?
> 2. Create an artificial asymmetry: flip a bit of `nSequence` for the update+state txes of one counterparty, and have each side provide signatures for the tx held by its counterparty (as in Poon-Dryja).
> This lets you force that the party that holds a particular update+state tx is the one that pays fees.

No, wait, #2 does not actually work as stated.
Decker-Russell-Osuntokun uses `SIGHASH_NOINPUT` meaning the `nSequence` is not committed in  the signature and can be malleated.

Further, in order for update transactions to be able to replace one another, the amount output of the update transaction needs to be the same value as the input of the update transaction --- meaning cannot deduct the fee from the channel, at least for the update tx.
This forces the update transaction to be paid for by bringing in an external UTXO owned by whoever constructed the update transaction (== whoever started the closing).


Regards,
ZmnSCPxj


------------------------------

Message: 4
Date: Tue, 30 Jan 2024 15:55:09 +1000
From: Anthony Towns <aj@erisian.com.au>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: Lightning Dev <lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] CheckTemplateVerify Does
	Not Scale Due to UTXO's Required For Fee Payment
Message-ID: <ZbiPPSz9vvIxtJSU@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Tue, Jan 30, 2024 at 05:17:04AM +0000, ZmnSCPxj via bitcoin-dev wrote:
> 
> > I should note that under Decker-Russell-Osuntokun the expectation is that both counterparties hold the same offchain transactions (hence why it is sometimes called "LN-symmetry").
> > However, there are two ways to get around this:
> > 
> > 1. Split the fee between them in some "fair" way.
> > Definition of "fair" wen?
> > 2. Create an artificial asymmetry: flip a bit of `nSequence` for the update+state txes of one counterparty, and have each side provide signatures for the tx held by its counterparty (as in Poon-Dryja).
> > This lets you force that the party that holds a particular update+state tx is the one that pays fees.
> 
> No, wait, #2 does not actually work as stated.
> Decker-Russell-Osuntokun uses `SIGHASH_NOINPUT` meaning the `nSequence` is not committed in the signature and can be malleated.

BIP 118 as at March 2021 (when it defined NOINPUT rather than APO):

] The transaction digest algorithm from BIP 143 is used when verifying a
] SIGHASH_NOINPUT signature, with the following modifications:
]
]     2. hashPrevouts (32-byte hash) is 32 0x00 bytes
]     3. hashSequence (32-byte hash) is 32 0x00 bytes
]     4. outpoint (32-byte hash + 4-byte little endian) is
]        set to 36 0x00 bytes
]     5. scriptCode of the input is set to an empty script
]        0x00

BIP 143:

] A new transaction digest algorithm is defined, but only applicable to sigops in version 0 witness program:
]
]   Double SHA256 of the serialization of:
] ...
]      2. hashPrevouts (32-byte hash)
]      3. hashSequence (32-byte hash)
]      4. outpoint (32-byte hash + 4-byte little endian) 
]      5. scriptCode of the input (serialized as scripts inside CTxOuts)
] ...
]      7. nSequence of the input (4-byte little endian)

So nSequence would still have been committed to per that proposal.
Dropping hashSequence just removes the commitment to the other inputs
being spent by the tx.

Cheers,
aj


------------------------------

Message: 5
Date: Tue, 30 Jan 2024 08:40:41 +0000
From: Peter Todd <pete@petertodd.org>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org, Lightning Dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] CheckTemplateVerify Does
	Not Scale Due to UTXO's Required For Fee Payment
Message-ID: <Zbi2CcSb7cQjqMQk@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Jan 30, 2024 at 05:07:16AM +0000, ZmnSCPxj wrote:
> Sent with Proton Mail secure email.
> 
> On Tuesday, January 30th, 2024 at 4:38 AM, Peter Todd <pete@petertodd.org> wrote:
> 
> > On Tue, Jan 30, 2024 at 04:12:07AM +0000, ZmnSCPxj wrote:
> > 
> > > Peter Todd proposes to sign multiple versions of offchain transactions at varying feerates.
> > > However, this proposal has the issue that if you are not the counterparty paying for onchain fees (e.g. the original acceptor of the channel, as per "initiator pays" principle), then you have no disincentive to just use the highest-feerate version always, and have a tiny incentive to only store the signature for the highest-feerate version to reduce your own storage costs slightly.
> > 
> > 
> > You are incorrect. Lightning commitments actually come in two different
> > versions, for the local and remote sides. Obviously, I'm proposing that fees be
> > taken from the side choosing to sign and broadcast the transaction. Which is
> > essentially no different from CPFP anchors, where the side choosing to get the
> > transaction mined pays the fee (though with anchors, it is easy for both sides
> > to choose to contribute, but in practice this almost never seems to happen in
> > my experience running LN nodes).
> 
> There is a reason why I mention "initiator pays", and it is because the channel opener really ought to pay for onchain fees in general.

You make a good point that Lightning channels *should* work that way. But even
right now they do not: Lightning commitment transactions pay a fixed, generally
low, fee-rate just high enough to propagate (and often lower) and are expected
to be brought up to full fee-rate via the anchor outputs.

Either side can pay the fees using the anchor outputs. And in practice, it's
quite common for the initiator to *not* pay the supermajority of the fees.

Furthermore, the proposals floating around for V3 transactions and Lightning is
to double-down on this design, with the commitment transaction paying no fees
at all and anchor outputs (and CPFP) being always used.

> For example, I could mount the following attack:
> 
> 1.  I already have an existing LN node on the network.
> 2.  I wait for a low-feerate time.
> 3.  I spin up a new node and initiate a channel funding to a victim node.
> 4.  I empty my channel with the victim node, sending out my funds to my existing LN node.
> 5.  I retire my new node forever.
> 
> This forces the victim node to use its commitment tx.
> 
> If the onchain fee for the commitment tx is paid for by who holds the commitment tx (as in your proposal) then I have forced the victim node to pay an onchain fee.

Again, Lightning channels *right* now work this way too. I personally have done
steps #1 to #5 the other day on the same laptop I'm writing this email on. Due
to a glitch in channel closing, the cooperative close failed, and at the moment
the recipient has a 10sat/VB commitment transaction with a fee below most
mempools' minrelayfee. Their balance was ~2 million sats, and my local balance
was just ~20k sats, and the commitment transaction was signed with the default
10sat/vB fee, which is well below the minrelayfee, let alone competitive.

If the receipient wants their ~2 million sats any time soon they're going to
have to CPFP the commitment transaction to get it up to about 30sat/vB, at
which point they've paid the supermajority of the cost even though they're the
receipient. Personally, I've shut down that node for good (I archived .lnd) and
I'll check back in a month or two to see if they ever get their funds.

> This is why the initial design for openv1 is "initiator pays".

...and that design clearly went out the window with anchor channels.

> In the above attack scenario, the commitment tx held by the victim node, under "initiator pays", has its onchain fee paid by me, thus the victim is not forced to pay the unilateral close fee, I am the one forced to pay it.
> They do still need to pay fees to get their now-onchain funds back into Lightning, but at least more of the onchain fees (the fees to unilaterally close the channel with the now-dead node) is paid by the attacker.
> 
> On the other hand, it may be possible that "initiator pays" can be dropped.
> In this attack scenario, the victim node should really require a non-zero reserve anyway that is proportional to the channel size, so that the attacker needs to commit some funds to the victim until the victim capitulates and unilaterally closes.
> In addition, to repeat this attack, I need to keep opening channels to the victim and thus pay onchain fees for the channel open.
> 
> So it may be that your proposal is sound; possibly the "initiator pays" advantage in this attack scenario is small enough that we can sacrifice it for multi-fee-version.

No, RBF channels have nothing to do with whether or not the "initiator pays".

If you want to have the RBF concept, and initator pays, you just need to
negotiate a minimum fee rate that you take out of the initiators balance. That
aspect of the design is orthogonal to how exactly the rest of the fees are
paid, and the concept of negotiating a minimum fee for the commitment
transaction to pay is relevant to all forms of anchor channels too.

> No, I am referring to a variation of your proposal where the side paying the fees in "initiator pays" gets full signatures for all feerate-versions but the other side gets only the full signatures for the lowest-fee version.

...and no-one is proposing that variation for the obvious reason that the
receipient has no incentive not to use the full fee-rate every time.

Indeed, a hypothetical CPFP version of this variation would have the exact same
incentive issue.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240130/262de51e/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 33
********************************************
