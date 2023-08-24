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

   1. Re: Standardisation of an unstructured taproot annex (Joost Jager)
   2. Re: Standardisation of an unstructured taproot annex (Joost Jager)
   3. Re: Standardisation of an unstructured taproot annex (Joost Jager)


----------------------------------------------------------------------

Message: 1
Date: Sat, 3 Jun 2023 09:49:36 +0200
From: Joost Jager <joost.jager@gmail.com>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV9JYYOSJXbzhrGTrv3jf_qGoLRbq9COgbBmuinpNAOhDg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi David,

On Sat, Jun 3, 2023 at 3:08?AM David A. Harding <dave@dtrt.org> wrote:

> Out of curiosity, what features and benefits are available today?  I
> know Greg Sanders wants to use annex data with LN-Symmetry[1], but
> that's dependent on a soft fork of SIGHASH_ANYPREVOUT.  I also heard you
> mention that it could allow putting arbitrary data into a witness
> without having to commit to that data beforehand, but that would only
> increase the efficiency of witness stuffing like ordinal inscriptions by
> only 0.4% (~2 bytes saved per 520 bytes pushed) and it'd still be
> required to create an output in order to spend it.
>

Indeed, there's a minor efficiency gain in the reveal transaction witness,
but I think the real advantage is that it eliminates the need to publish
and pay for the commit transaction in the first place. Any spend of a
taproot UTXO can be supplemented with arbitrary data in just a single
transaction.


> Is there some other way to use the annex today that would be beneficial
> to users of Bitcoin?


The removal of the need for a commitment transaction also enables the
inclusion of data within a single transaction that relies on its own
transaction identifier (txid). This is possible because the txid
calculation does not incorporate the annex, where the data would be housed.
This feature can be beneficial in scenarios that require the emulation of
covenants through the use of presigned transactions involving an ephemeral
signer.

For instance, one can establish a time-locked vault using 2-of-2 multisig
presigned transactions in which one of the signers is ephemeral [1]. After
signing, the private key is discarded, leaving only the signature. To
ensure the signature is never lost, it can be stored as a backup in the
annex of the transaction that the presigned transaction spends. Such an
operation would not be possible with a commit/reveal inscription.

[1] https://github.com/LedgerHQ/app-bitcoin-new/issues/153
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/76c769ae/attachment-0001.html>

------------------------------

Message: 2
Date: Sat, 3 Jun 2023 10:06:37 +0200
From: Joost Jager <joost.jager@gmail.com>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV_UR9ND2vK1+BVeKQ==xdsamJ_7U-X4LH67J9g57UrkTw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Sat, Jun 3, 2023 at 9:49?AM Joost Jager <joost.jager@gmail.com> wrote:

> The removal of the need for a commitment transaction also enables the
> inclusion of data within a single transaction that relies on its own
> transaction identifier (txid). This is possible because the txid
> calculation does not incorporate the annex, where the data would be housed.
> This feature can be beneficial in scenarios that require the emulation of
> covenants through the use of presigned transactions involving an ephemeral
> signer.
>

I think this avoidance of a circular reference is also why LN-Symmetry uses
the annex?

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/defc2cc7/attachment-0001.html>

------------------------------

Message: 3
Date: Sat, 3 Jun 2023 11:14:27 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV8Vt_LLH-AEo-fCCs+S6uSy9UwC6QBakWY5tzn9Utwb8w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

HI Greg,

On Sat, Jun 3, 2023 at 3:14?AM Greg Sanders <gsanders87@gmail.com> wrote:

> Attempting to summarize the linked PR:
>
> I think the biggest remaining issue to this kind of idea, which is why I
> didn't propose it for mainnet,
> is the fact that BIP341/342 signature hashes do not cover *other* inputs'
> annex fields, which we
> briefly discussed here
> https://github.com/bitcoin-inquisition/bitcoin/pull/22#discussion_r1143382264
> .
>
> This means that in a coinjoin like scenario, even if the other joining
> parties prove they don't have any
> crazy script paths, a malicious party can make the signed transaction into
> a maximum sized transaction
> package, causing griefing. The mitigation in the PR I linked was to limit
> it to 126 bytes, basically punting
> on the problem by making the grief vector small. Another solution could be
> to make annex usage "opt-in"
> by requiring all inputs to commit to an annex to be relay-standard. In
> this case, you've opted into a possible
> vector, but at least current usage patterns wouldn't be unduly affected.
> For those who opt-in, perhaps the first
> order of business would be to have a field that limits the total
> transaction weight, by policy only?
>
> Some logs related to that here:
> https://gist.github.com/instagibbs/7406931d953fd96fea28f85be50fc7bb
>
> Related discussion on possible BIP118 modifications to mitigate this in
> tapscript-spending circumstances:
> https://github.com/bitcoin-inquisition/bitcoin/issues/19
>

While solutions such as making annex usage opt-in or imposing size
limitations may initially appear effective, they may also inadvertently
foster a false sense of security, as they lack alignment with economic
incentives.

Relying solely on policy enforcement merely transfers responsibility to the
miners, without necessarily aligning their incentives with the broader
network health. This situation is reminiscent of the challenges encountered
with opt-in rbf. Despite signaling for non-replaceability, miners began
accepting replacements probably due to the enticing higher fee incentives.
At least that's how I picked up this development. Businesses that relied on
zero-confirmation payments were unexpectedly affected, leading to
undesirable outcomes.

While we can define policy rules, miners will ultimately operate in a
manner that maximizes their profits. Consequently, if a miner identifies an
opportunity to bolster their fees by replacing an annex transaction,
they're likely to seize it, regardless of any policy rules. This might not
be readily apparent currently with a limited number of pools dominating
block production, but it is my hope that mining will be more decentralized
in the future.

Depending on policy to mitigate this annex malleability vector could
mislead developers into believing their transactions are immune to
replacement, when in fact they might not be. This potential misalignment
could result in developers and businesses constructing systems based on
assumptions that could be compromised in the future, mirroring the
situation that unfolded with zero-confirmation payments and rbf.

It may thus be more prudent to permit the utilization of the annex without
restrictions, inform developers of its inherent risks, and acknowledge that
Bitcoin, in its present state, might not be ideally suited for certain
types of applications?

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/4b064f42/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 5
******************************************
