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

   1. Re: Full Disclosure: CVE-2023-40231 / CVE-2023-40232 /
      CVE-2023-40233 / CVE-2023-40234 "All your mempool are belong to
      us" (Antoine Riard)
   2. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Tue, 17 Oct 2023 02:11:20 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Full Disclosure: CVE-2023-40231 /
	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your mempool are
	belong to us"
Message-ID:
	<CALZpt+GsRfHvABjhkX=eN_1viVw8Jos4=+sBd7vWQJ_VxNta8g@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> I think if you want people to understand this exploit, you need to
explain in more detail how we have a situation where two different parties
can spend the same HTLC txout, without the first party having the right to
spend it via their knowledge of the HTLC-preimage.

If I'm correctly understanding your question, you're asking why we have a
situation where the spend of a HTLC output can be in competition between 2
channel counterparties.

LN commitment transactions have offered HTLC outputs where a counterparty
Alice is pledging to her other counterparty Caroll the HTLC amount in
exchange of a preimage (and Caroll signature).

After the expiration of the HTLC timelock, if the HTLC has not been claimed
on-chain by Caroll, Alice can claim it back with her signature (and the
pre-exchanged Caroll signature).

The exploit works actually in Caroll leveraging her HTLC-preimage
transaction as a replace-by-fee of Alice's HTLC-timeout _after_ the
expiration of the timelock, the HTLC-preimage transaction staying consensus
valid.

There is nothing in the mempool policy rules that prevent this Caroll's
HTLC-preimage of being replaced subsequently, once Alice's HTLC-timeout has
been evicted out the mempool.

The HTLC output does not have any spend candidate remaining for this block.
If this replacement can be successfully repeated until an inbound HTLC on
another Alice's channel expires, the "forward" HTLC can be double-spent.



Le lun. 16 oct. 2023 ? 20:13, Peter Todd <pete@petertodd.org> a ?crit :

>
>
> On October 16, 2023 6:57:36 PM GMT+02:00, Antoine Riard via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
> >(cross-posting mempool issues identified are exposing lightning chan to
> >loss of funds risks, other multi-party bitcoin apps might be affected)
> >
> >As the HTLC-preimage spends an unconfirmed input that was already included
> >in the unconfirmed and unrelated child transaction (rule 2), pays an
> >absolute higher fee of at least the sum paid by the HTLC-timeout and child
> >transaction (rule 3) and the HTLC-preimage feerate is greater than all
> >directly conflicting transactions (rule 6), the replacement is accepted.
> >The honest HTLC-timeout is evicted out of the mempool.
>
> I think if you want people to understand this exploit, you need to explain
> in more detail how we have a situation where two different parties can
> spend the same HTLC txout, without the first party having the right to
> spend it via their knowledge of the HTLC-preimage.
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231017/c71ce504/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 17 Oct 2023 10:34:04 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: "lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 /	CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your	mempool are belong to us"
Message-ID:
	<64VpLnXQLbeoc895Z9aR7C1CfH6IFxPFDrk0om-md1eqvdMczLSnhwH29T6EWCXgiGQiRqQnAYsezbvNvoPCdcfvCvp__Y8BA1ow5UwY2yQ=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Antoine et al.,

Let me try to rephrase the core of the attack.

There exists these nodes on the LN (letters `A`, `B`, and `C` are nodes, `==` are channels):

    A ===== B ===== C

`A` routes `A->B->C`.

The timelocks, for example, could be:

   A->B timeelock = 144
   B->C timelock = 100

The above satisfies the LN BOLT requirements, as long as `B` has a `cltv_expiry_delta` of 44 or lower.

After `B` forwards the HTLC `B->C`, C suddenly goes offline, and all the signed transactions --- commitment transaction and HTLC-timeout transactions --- are "stuck" at the feerate at the time.

At block height 100, `B` notices the `B->C` HTLC timelock is expired without `C` having claimed it, so `B` forces the `B====C` channel onchain.
However, onchain feerates have risen and the commitment transaction and HTLC-timeout transaction do not confirm.

In the mean time, `A` is still online with `B` and updates the onchain fees of the `A====B` channel pre-signed transactions (commitment tx and HTLC-timeout tx) to the latest.

At block height 144, `B` is still not able to claim the `A->B` HTLC, so `A` drops the `A====B` channel onchain.
As the fees are up-to-date, this confirms immediately and `A` is able to recover the HTLC funds.
However, the feerates of the `B====C` pre-signed transactions remain at the old, uncompetitive feerates.

At this point, `C` broadcasts an HTLC-success transaction with high feerates that CPFPs the commitment tx.
However, it replaces the HTLC-timeout transaction, which is at the old, low feerate.
`C` is thus able to get the value of the HTLC, but `B` is now no longer able to use the knowledge of the preimage, as its own incoming HTLC was already confirmed as claimed by `A`.

Is the above restatement accurate?

----

Let me also explain to non-Lightning experts why HTLC-timeout is presigned in this case and why `B` cannot feebump it.

In the Poon-Dryja mechanism, the HTLCs are "infected" by the Poon-Dryja penalty case, and are not plain HTLCs.

A plain HTLC offerred by `B` to `C` would look like this:

    (B && OP_CLTV) || (C && OP_HASH160)

However, on the commitment transaction held by `B`, it would be infected by the penalty case in this way:

    (B && C && OP_CLTV) || (C && OP_HASH160) || (C && revocation)

There are two changes:

* The addition of a revocation branch `C && revocation`.
* The branch claimable by `B` in the "plain" HTLC (`B && OP_CLTV`) also includes `C`.

These are necessary in case `B` tries to cheat and this HTLC is on an old, revoked transaction.
If the revoked transaction is *really* old, the `OP_CLTV` would already impose a timelock far in the past.
This means that a plain `B && OP_CLTV` branch can be claimed by `B` if it retained this very old revoked transaction.

To prevent that, `C` is added to the `B && OP_CLTV` branch.
We also introduce an HTLC-timeout transaction, which spends the `B && C && OP_CLTV` branch, and outputs to:

    (B && OP_CSV) || (C && revocation)

Thus, even if `B` held onto a very old revoked commitment transaction and attempts to spend the timelock branch (because the `OP_CLTV` is for an old blockheight), it still has to contend with a new output with a *relative* timelock.

Unfortunately, this means that the HTLC-timeout transaction is pre-signed, and has a specific feerate.
In order to change the feerate, both `B` and `C` have to agree to re-sign the HTLC-timeout transaction at the higher feerate.

However, the HTLC-success transaction in this case spends the plain `(C && OP_HASH160)` branch, which only involves `C`.
This allows `C` to feebump the HTLC-success transaction arbitrarily even if `B` does not cooperate.

While anchor outputs can be added to the HTLC-timeout transaction as well, `C` has a greater advantage here due to being able to RBF the HTLC-timeout out of the way (1 transaction), while `B` has to get both HTLC-timeout and a CPFP-RBF of the anchor output of the HTLC-timeout transaction (2 transactions).
`C` thus requires a smaller fee to achieve a particular feerate due to having to push a smaller number of bytes compared to `B`.

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 13
********************************************
