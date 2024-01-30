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

   1. Re: [Lightning-dev] CheckTemplateVerify Does Not	Scale Due to
      UTXO's Required For Fee Payment (ZmnSCPxj)
   2. Re: [Lightning-dev] CheckTemplateVerify Does Not Scale Due to
      UTXO's Required For Fee Payment (Peter Todd)
   3. Re: CheckTemplateVerify Does Not Scale Due to UTXO's Required
      For Fee Payment (Peter Todd)
   4. Re: CheckTemplateVerify Does Not Scale Due to UTXO's Required
      For Fee Payment (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Tue, 30 Jan 2024 04:12:07 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Michael Folkson <michaelfolkson@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org, Lightning Dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] CheckTemplateVerify Does
	Not	Scale Due to UTXO's Required For Fee Payment
Message-ID:
	<9tVZA3A4x-GZB5wQ1kMUoyyYXqvGS4MP4iDrLx1FCFHly-MU--II8evpgdcf2Xb9JZWDsY0kEB8r9dClzPrOk_V8EiWtHms8fvlunZQNGrA=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Michael et al,

> 
> I assume that a CTV based LN-Symmetry also has this drawback when compared to an APO based LN-Symmetry? In theory at least an APO based LN-Symmetry could change the fees in every channel update based on what the current market fee rate was at the time of the update. In today's pre LN-Symmetry world you are always going to have justice transactions for revoked states that were constructed when the market fee rate was very different from the present day's market fee rate.

This is the same in the future Decker-Russell-Osuntokun ("eltoo" / "LN-Symmetry") world as in the current Poon-Dryja ("LN-punishment").

Every *commitment* transaction in Poon-Dryja commits to a specific fee rate, which is why it it problematic today.
The *justice* transaction is single-signed and can (and SHOULD!) be RBF-ed (e.g. CLN implements an aggressive *justice* transaction RBF-ing written by me).

However, the issue is that every *commitment* transaction commits to a specific feerate today, and if the counterparty is offline for some time, the market feerate may diverge tremendously from the last signed feerate.

The same issue will still exist in Decker-Russell-Osuntokun --- the latest pair of update and state transactions will commit to a specific feerate.
If the counterparty is offline for some time, the market feerate may diverge tremendously from the last signed feerate.

Anchor commitments Fixes This by adding an otherwise-unnecessary change output (called "anchor output") for both parties to be able to attach a CPFP transaction.
However, this comes at the expense of increased blockspace usage for the anchor outputs.

Peter Todd proposes to sign multiple versions of offchain transactions at varying feerates.
However, this proposal has the issue that if you are not the counterparty paying for onchain fees (e.g. the original acceptor of the channel, as per "initiator pays" principle), then you have no disincentive to just use the highest-feerate version always, and have a tiny incentive to only store the signature for the highest-feerate version to reduce your own storage costs slightly.
In addition, it is also incentive-incompatible for the party that pays onchain fees to withhold signatures for the higher-fee versions, because if you are the party who does not pay fees and all you hold are the complete signatures for the lowest-fee version (because the counterparty does not want to trust you with signatures for higher-fee versions because you will just abuse it), then you will need anchor outputs again to bump up the fee.

The proposal from Peter Todd might work if both parties share the burden for paying the fees.
However, this may require that both parties always bring in funds on all channel opens, i.e. no single-sided funding.
I have also not considered how this game would play out, though naively, it seems to me that if both parties pay onchain fees "fairly" for some definition of "fair" (how to define "fair" may be problematic --- do they pay equal fees or proportional to their total funds held in the channel?) then it seems to me okay to have multi-feerate-version offchain txes (regardless of using Poon-Dryja or Decker-Russell-Osuntokun).
However, there may be issues with hosting HTLCs; technically HTLCs are nested inside a larger contract (the channel) and if so, do you need a separate transaction to resolve them (Poon-Dryja does!) and do you also have to multi-feerate *in addition to* multi-feerate the outer transaction (e.g. commitment transaction in Poon-Dryja) resulting in a O(N * N) transactions for N feerates?


Regards,
ZmnSCPxj


------------------------------

Message: 2
Date: Tue, 30 Jan 2024 04:38:26 +0000
From: Peter Todd <pete@petertodd.org>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org, Lightning Dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] CheckTemplateVerify Does
	Not Scale Due to UTXO's Required For Fee Payment
Message-ID: <Zbh9Qqk2jK0tqKgp@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Jan 30, 2024 at 04:12:07AM +0000, ZmnSCPxj wrote:
> Peter Todd proposes to sign multiple versions of offchain transactions at varying feerates.
> However, this proposal has the issue that if you are not the counterparty paying for onchain fees (e.g. the original acceptor of the channel, as per "initiator pays" principle), then you have no disincentive to just use the highest-feerate version always, and have a tiny incentive to only store the signature for the highest-feerate version to reduce your own storage costs slightly.

You are incorrect. Lightning commitments actually come in two different
versions, for the local and remote sides. Obviously, I'm proposing that fees be
taken from the side choosing to sign and broadcast the transaction. Which is
essentially no different from CPFP anchors, where the side choosing to get the
transaction mined pays the fee (though with anchors, it is easy for both sides
to choose to contribute, but in practice this almost never seems to happen in
my experience running LN nodes).

> In addition, it is also incentive-incompatible for the party that pays onchain fees to withhold signatures for the higher-fee versions, because if you are the party who does not pay fees and all you hold are the complete signatures for the lowest-fee version (because the counterparty does not want to trust you with signatures for higher-fee versions because you will just abuse it), then you will need anchor outputs again to bump up the fee.

That is also incorrect. If the protocol demands multiple fee variants exist,
the state of the lightning channel simply doesn't advance until all required
fee-variants are provided. Withholding can't happen any more than someone could
"withhold" a state by failing to provide the last byte of a commitment
transaction: until the protocol state requirements have been fufilled in full,
the previous state remains in effect.

> However, there may be issues with hosting HTLCs; technically HTLCs are nested inside a larger contract (the channel) and if so, do you need a separate transaction to resolve them (Poon-Dryja does!) and do you also have to multi-feerate *in addition to* multi-feerate the outer transaction (e.g. commitment transaction in Poon-Dryja) resulting in a O(N * N) transactions for N feerates?

I covered HTLCs in my blog post on the subject; I would suggest you read it in
full. There are multiple potential options to deal with HTLC feerates to avoid
the obvious N^2 problem:

https://petertodd.org/2023/v3-transactions-review#htlcs-and-replace-by-fee

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240130/f286ccae/attachment-0001.sig>

------------------------------

Message: 3
Date: Tue, 30 Jan 2024 04:41:30 +0000
From: Peter Todd <pete@petertodd.org>
To: alicexbt <alicexbt@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's Required For Fee Payment
Message-ID: <Zbh9+oNDuPEapFwQ@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Sat, Jan 27, 2024 at 05:50:27PM +0000, alicexbt wrote:
> Hi Peter,
> 
> In addition to the various methods shared by Brandon, users also have the option of using multiple templates, each with different fee rates. While this introduces some trade-offs, it remains a possibility that some users might prefer.

I mentioned this possibility in the email that you are replying to. It is
difficult to impossible to implement in many (but not all!) CTV-using
constructions because you get an exponential "blow-up" of possible fee
variants.

> OP_IF
>     //Template-A
>    OP_PUSHBYTES_32 HASH1 OP_CHECKTEMPLATEVERIFY
> OP_ELSE
>     //Template-B
>    OP_PUSHBYTES_32 HASH2 OP_CHECKTEMPLATEVERIFY
> OP_ENDIF

Note that with taproot, it is more efficient to do this via taproot leafs than
with IF statements.

> /dev/fd0
> floppy disk guy
> 
> Sent with Proton Mail secure email.
> 
> On Wednesday, January 24th, 2024 at 7:31 PM, Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> > CheckTemplateVerify(1) is a proposed covenant opcode that commits to the
> > transaction that can spend an output. Namely, # of inputs, # of outputs,
> > outputs hash, etc. In practice, in many if not most CTV use-cases intended to
> > allow multiple parties to share a single UTXO, it is difficult to impossible to
> > allow for sufficient CTV variants to cover all possible fee-rates. It is
> > expected that CTV would be usually used with anchor outputs to pay fees; by
> > creating an input of the correct size in a separate transaction and including
> > it in the CTV-committed transaction; or possibly, via a transaction sponsor
> > soft-fork.
> > 
> > This poses a scalability problem: to be genuinely self-sovereign in a protocol
> > with reactive security, such as Lightning, you must be able to get transactions
> > mined within certain deadlines. To do that, you must pay fees. All of the
> > intended exogenous fee-payment mechanisms for CTV require users to have at
> > least one UTXO of suitable size to pay for those fees.
> > 
> > This requirement for all users to have a UTXO to pay fees negates the
> > efficiency of CTV-using UTXO sharing schemes, as in an effort to share a UTXO,
> > CTV requires each user to have an extra UTXO. The only realistic alternative is
> > to use a third party to pay for the UTXO, eg via a LN payment, but at that
> > point it would be more efficient to pay an out-of-band mining fee. That of
> > course is highly undesirable from a mining centralization perspective.(2)
> > 
> > Recommendations: CTV in its current form be abandoned as design foot-gun. Other
> > convenant schemes should be designed to work well with replace-by-fee, to avoid
> > requirements for extra UTXOs, and to maximize on-chain efficiency.
> > 
> > 1) https://github.com/bitcoin/bips/blob/deae64bfd31f6938253c05392aa355bf6d7e7605/bip-0119.mediawiki
> > 2) https://petertodd.org/2023/v3-transactions-review#anchor-outputs-are-a-danger-to-mining-decentralization
> > 
> > --
> > https://petertodd.org 'peter'[:-1]@petertodd.org
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240130/f938ba2b/attachment-0001.sig>

------------------------------

Message: 4
Date: Tue, 30 Jan 2024 04:46:27 +0000
From: Peter Todd <pete@petertodd.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's Required For Fee Payment
Message-ID: <Zbh/I+7NIoAmlEt8@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Jan 26, 2024 at 10:28:54PM -0800, Brandon Black wrote:
> Hi Peter,
> 
> On 2024-01-24 (Wed) at 19:31:07 +0000, Peter Todd via bitcoin-dev wrote:
> > It is
> > expected that CTV would be usually used with anchor outputs to pay fees; by
> > creating an input of the correct size in a separate transaction and including
> > it in the CTV-committed transaction; or possibly, via a transaction sponsor
> > soft-fork.
> > 
> > This poses a scalability problem: to be genuinely self-sovereign in a protocol
> > with reactive security, such as Lightning, you must be able to get transactions
> > mined within certain deadlines. To do that, you must pay fees. All of the
> > intended exogenous fee-payment mechanisms for CTV require users to have at
> > least one UTXO of suitable size to pay for those fees.
> 
> I understand your reservations with regard to CTV-based protocols for
> scaling bitcoin and lightning. Fortunately, the "user gotta have a UTXO"
> concern is readily answered (and you actually gave one answer to
> approximately the same concern from me when we discussed lightning
> fees): If the user's balance inside the protocol is not sufficient to
> pay exit fees then they aren't going to try to exit; so their
> in-protocol balance can be used to pay fees. With ephemeral anchors
> throughout the tree, an exiting user would spend their leaf UTXO, and
> the ephemeral anchors along the path to their leaf to create a package
> of the necessary fee rate to facilitate their timely exit.
> 
> Alternatively, users entering into a channel tree protocol (e.g. Timeout
> Trees) can have their leaf include a second UTXO commitment which would
> create a fee-paying output exactly when they need it; without causing a
> scaling problem.

You are assuming a specific type of CTV use-case. Not all CTV use-cases have
this property, which is why I called this a footgun: attractive, but likely to
lead to protocol designs with unexpected flaws.

Secondly, anchor outputs/CPFP is significantly less efficient than RBF, due to
the extra bytes required for the CPFP transaction. As I explained in the email
you are replying to, this is a danger to mining decentralization because it
requires less bytes to pay fees with out-of-band fee payments.

It is much better to deal with fees now, before CTV is standardized as-is, in a
way that allows for efficient fee payment via RBF rather than locking in
inefficient CPFP designs that invite out-of-band fees.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240130/eece6231/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 32
********************************************
