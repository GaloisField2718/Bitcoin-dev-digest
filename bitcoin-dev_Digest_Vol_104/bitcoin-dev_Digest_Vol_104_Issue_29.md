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

   1. Re: CheckTemplateVerify Does Not Scale Due to UTXO's	Required
      For Fee Payment (Michael Folkson)
   2. Re: BIP number request for wallet policies (Michael Folkson)
   3. Re: One-Shot Replace-By-Fee-Rate (Murch)
   4. Re: CheckTemplateVerify Does Not Scale Due to UTXO's	Required
      For Fee Payment (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Thu, 25 Jan 2024 12:57:52 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: bitcoin-dev@lists.linuxfoundation.org, Lightning Dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's	Required For Fee Payment
Message-ID:
	<4619vs2aZBsW1lr3ihqjM6TdRgx8CuA_wRwXetu7jZZcL8r3oWUy7xOPkT-qJ0xxT79_Ss6it2chOWAAWPJuU8YSCzjaNOd6JvnMvWTBc-c=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Peter

Interesting post. By implicitly committing in advance to the fee paid by the spending transaction CTV is certainly nailing its colors to the CPFP mast rather than operating in a RBF world. And in a future high fee environment (ignoring whatever is driving those high fees, monetary or non-monetary use cases) as you state paying for an additional CPFP transaction is suboptimal rather than just replacing an existing unconfirmed transaction. 

I did a cursory search to look for an in depth technical comparison of CPFP and RBF and I found this from Antoine (Poinsot) on Bitcoin StackExchange [0]. In that he states his view that:

"If most nodes didn't enforce mandatory BIP125 signalling, RBF would be superior in all aspects to CPFP from the perspective of the emitter of transaction. CPFP is much less efficient, and not always possible: you need the transaction to have a change output and (at least at the time of writing [0]) the parent to pass policy checks on its own, for instance if it's below the minimum feerate of most mempools on the network you won't be able to CPFP it at the moment."

I assume that a CTV based LN-Symmetry also has this drawback when compared to an APO based LN-Symmetry? In theory at least an APO based LN-Symmetry could change the fees in every channel update based on what the current market fee rate was at the time of the update. In today's pre LN-Symmetry world you are always going to have justice transactions for revoked states that were constructed when the market fee rate was very different from the present day's market fee rate.

Thanks
Michael


[0]: https://bitcoin.stackexchange.com/questions/117703/comparison-between-cpfp-and-bip125-for-fee-bumping

--
Michael Folkson
Email: michaelfolkson at protonmail.com
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F


Learn about Bitcoin: https://www.youtube.com/@portofbitcoin


On Wednesday, 24 January 2024 at 19:31, Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> CheckTemplateVerify(1) is a proposed covenant opcode that commits to the
> transaction that can spend an output. Namely, # of inputs, # of outputs,
> outputs hash, etc. In practice, in many if not most CTV use-cases intended to
> allow multiple parties to share a single UTXO, it is difficult to impossible to
> allow for sufficient CTV variants to cover all possible fee-rates. It is
> expected that CTV would be usually used with anchor outputs to pay fees; by
> creating an input of the correct size in a separate transaction and including
> it in the CTV-committed transaction; or possibly, via a transaction sponsor
> soft-fork.
> 
> This poses a scalability problem: to be genuinely self-sovereign in a protocol
> with reactive security, such as Lightning, you must be able to get transactions
> mined within certain deadlines. To do that, you must pay fees. All of the
> intended exogenous fee-payment mechanisms for CTV require users to have at
> least one UTXO of suitable size to pay for those fees.
> 
> This requirement for all users to have a UTXO to pay fees negates the
> efficiency of CTV-using UTXO sharing schemes, as in an effort to share a UTXO,
> CTV requires each user to have an extra UTXO. The only realistic alternative is
> to use a third party to pay for the UTXO, eg via a LN payment, but at that
> point it would be more efficient to pay an out-of-band mining fee. That of
> course is highly undesirable from a mining centralization perspective.(2)
> 
> Recommendations: CTV in its current form be abandoned as design foot-gun. Other
> convenant schemes should be designed to work well with replace-by-fee, to avoid
> requirements for extra UTXOs, and to maximize on-chain efficiency.
> 
> 1) https://github.com/bitcoin/bips/blob/deae64bfd31f6938253c05392aa355bf6d7e7605/bip-0119.mediawiki
> 2) https://petertodd.org/2023/v3-transactions-review#anchor-outputs-are-a-danger-to-mining-decentralization
> 
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Thu, 25 Jan 2024 16:49:49 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Antoine Poinsot <darosior@protonmail.com>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BIP number request for wallet policies
Message-ID:
	<0SVGKW4fU_A7VRcY73T7-JaSDHJL62xmgNWKxYeZM57Kgy2XqJpY5PE0EEnDNULDEQYhZPibNZ8mGf2OIcIsT18aYanUl4J64lsuJKe0gZ0=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Just to inform this list, this pull request has since been assigned a BIP number (BIP 388) [0].

Thanks
Michael


[0]: https://github.com/bitcoin/bips/pull/1389

--
Michael Folkson
Email: michaelfolkson at protonmail.com
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F


Learn about Bitcoin: https://www.youtube.com/@portofbitcoin


On Saturday, 16 December 2023 at 14:10, Antoine Poinsot via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> Wallet policies, a standard for implementing support for output descriptors in hardware signing devices was introduced by Salvatore Ingala a year and a half ago [0].
> 
> A pull request to the BIP repository was opened more than a year ago [1]. It's been waiting for a BIP number to be assigned since then.
> 
> There is now 3 majors hardware signing devices using this standard in production (Ledger, BitBox02, Jade). There has been multiple pings on the PR in the past year to get assigned a BIP number.
> 
> It would be nice to hear from the BIP editors about their expectations from the author, so we can move forward with this document specifying what's already become an industry standard.
> 
> Antoine Poinsot
> 
> [0] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020492.html
> [1] https://github.com/bitcoin/bips/pull/1389
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 3
Date: Thu, 25 Jan 2024 16:25:28 -0500
From: Murch <murch@murch.one>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <3384566b-8c6d-4d8c-91b8-a45f17aaec68@murch.one>
Content-Type: text/plain; charset=UTF-8; format=flowed

Hi Peter,

On 1/22/24 17:52, Peter Todd wrote:
> An even simpler fix would be to just require that all unconfirmed inputs 
> in a replacement come from the *same* replaced transaction. That would 
> make certain rare, but economically viable, replacements infeasible. But 
> it would definitely fix the issue.

The replacements spend at most a single unconfirmed input in my infinite 
relay cycle example.

Murch


------------------------------

Message: 4
Date: Thu, 25 Jan 2024 17:49:26 +0000
From: jlspc <jlspc@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's	Required For Fee Payment
Message-ID:
	<Gr0X5c-3nQcx-VLD3eQ-e0DoOFim5gUKeyOF5ViYPfjE030KB4QJ2tVyA4wfY64Um_zo0fTfjqkTN11-RcvDeiAVhE2_9VYcQ3kSGFD1dug=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Peter,

If feerate-dependent timelocks (FDTs) (1) are supported, it would be possible to use CTV to define a transaction with a fixed fee and no anchor outputs, as long as it's racing against a transaction with an FDT.

Regards,
John

(1) https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-December/004254.html




Sent with Proton Mail secure email.

On Wednesday, January 24th, 2024 at 11:31 AM, Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> CheckTemplateVerify(1) is a proposed covenant opcode that commits to the
> transaction that can spend an output. Namely, # of inputs, # of outputs,
> outputs hash, etc. In practice, in many if not most CTV use-cases intended to
> allow multiple parties to share a single UTXO, it is difficult to impossible to
> allow for sufficient CTV variants to cover all possible fee-rates. It is
> expected that CTV would be usually used with anchor outputs to pay fees; by
> creating an input of the correct size in a separate transaction and including
> it in the CTV-committed transaction; or possibly, via a transaction sponsor
> soft-fork.
> 
> This poses a scalability problem: to be genuinely self-sovereign in a protocol
> with reactive security, such as Lightning, you must be able to get transactions
> mined within certain deadlines. To do that, you must pay fees. All of the
> intended exogenous fee-payment mechanisms for CTV require users to have at
> least one UTXO of suitable size to pay for those fees.
> 
> This requirement for all users to have a UTXO to pay fees negates the
> efficiency of CTV-using UTXO sharing schemes, as in an effort to share a UTXO,
> CTV requires each user to have an extra UTXO. The only realistic alternative is
> to use a third party to pay for the UTXO, eg via a LN payment, but at that
> point it would be more efficient to pay an out-of-band mining fee. That of
> course is highly undesirable from a mining centralization perspective.(2)
> 
> Recommendations: CTV in its current form be abandoned as design foot-gun. Other
> convenant schemes should be designed to work well with replace-by-fee, to avoid
> requirements for extra UTXOs, and to maximize on-chain efficiency.
> 
> 1) https://github.com/bitcoin/bips/blob/deae64bfd31f6938253c05392aa355bf6d7e7605/bip-0119.mediawiki
> 2) https://petertodd.org/2023/v3-transactions-review#anchor-outputs-are-a-danger-to-mining-decentralization
> 
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 29
********************************************
