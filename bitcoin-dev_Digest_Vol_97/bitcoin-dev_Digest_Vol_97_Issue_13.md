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

   1. Re: Standardisation of an unstructured taproot annex
      (Antoine Riard)
   2. Re: Standardisation of an unstructured taproot annex (Joost Jager)


----------------------------------------------------------------------

Message: 1
Date: Sat, 10 Jun 2023 01:23:36 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Joost Jager <joost.jager@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CALZpt+FyVQpMAf-gPmUgh6ORqa2K59iKZKsa3Qm2Fw_U+GHC3Q@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Joost,

Thanks for detailing why a '0' as free-form, without any additional
constraints offers valuable engineering properties as of today.

>From a taproot annex design perspective, I think this could be very
valuable if you have a list of unstructured data use-cases you're thinking
about ? As raised on the BIP proposal, those unstructured data use-cases
could use annex tags with the benefit to combine multiple "types" of
unstructured data in a single annex payload. As you're raising smaller bits
of unstructured data might not afford the overhead though my answer with
this observation would be to move this traffic towards some L2 systems ? In
my mind, the default of adding a version byte for the usage of unstructured
data comes with the downside of having future consensus enabled use-cases
encumbering by the extended witness economic cost.

About the annex payload extension attack described by Greg. If my
understanding of this transaction-relay jamming griefing issue is correct,
we can have an annex tag in the future where the signer is committing to
the total weight of the transaction, or even the max per-input annex size ?
This should prevent a coinjoin or aggregated commitment transaction
counterparty to inflate its annex space to downgrade the overall
transaction feerate, I guess. And I think this could benefit unstructured
data use-cases too.

Best,
Antoine

Le ven. 2 juin 2023 ? 22:18, Joost Jager via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

> Hi,
>
> As it stands, the taproot annex is consensus valid but non-standard. The
> conversations around standardization seem to be leaning towards the
> adoption of a flexible Type-Length-Value (TLV) format [1]. There's no doubt
> that this approach has considerable potential. However, settling on an
> exact format may require a significant amount of time.
>
> In the interim, the benefits of making the annex available in a
> non-structured form are both evident and immediate. By allowing developers
> to utilize the taproot annex without delay, we can take advantage of its
> features today, without the need to wait for the finalization of a more
> lengthy standardization process.
>
> With this in view, I am proposing that we define any annex that begins
> with '0' as free-form, without any additional constraints. This strategy
> offers several distinct benefits:
>
> Immediate utilization: This opens the door for developers to make use of
> the taproot annex for a variety of applications straight away, thus
> eliminating the need to wait for the implementation of TLV or any other
> structured format.
>
> Future flexibility: Assigning '0'-beginning annexes as free-form keeps our
> options open for future developments and structure improvements. As we
> forge ahead in determining the best way to standardize the annex, this
> strategy ensures we do not limit ourselves by setting its structure in
> stone prematurely.
>
> Chainspace efficiency: Non-structured data may require fewer bytes
> compared to a probable TLV format, which would necessitate the encoding of
> length even when there's only a single field.
>
> In conclusion, adopting this approach will immediately broaden the
> utilization scope of the taproot annex while preserving the possibility of
> transitioning to a more structured format in the future. I believe this is
> a pragmatic and efficient route, one that can yield substantial benefits in
> both the short and long term.
>
> Joost
>
> [1] https://github.com/bitcoin/bips/pull/1381
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230610/2249fe52/attachment-0001.html>

------------------------------

Message: 2
Date: Sat, 10 Jun 2023 09:43:52 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV9SGXaf90X4oyTx7o+DG4-P58gUyiCGz+K08XZAOFBf2g@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Antoine,

On Sat, Jun 10, 2023 at 2:23?AM Antoine Riard <antoine.riard@gmail.com>
wrote:

> From a taproot annex design perspective, I think this could be very
> valuable if you have a list of unstructured data use-cases you're thinking
> about ?
>

The annex's list of unstructured data use-cases includes existing data
storage uses that utilize OP_RETURN or inscriptions. Consider ordinals,
timestamps, and any other data already stored on the chain. These
applications would immediately benefit from the annex's improved space
efficiency.

However, the primary advantage I see in the annex is that its data isn't
included in the calculation of the txid or a potential parent commit
transaction's txid (for inscriptions). I've explained this at [1]. This
feature makes the annex a powerful tool for applications that would ideally
use covenants.

The most critical application in this category, for me, involves
time-locked vaults. Given the positive reception to proposals such as
OP_VAULT [2], I don't think I'm alone in this belief. OP_VAULT is probably
a bit further out, but pre-signed transactions signed using an ephemeral
key can fill the gap and improve the safeguarding of Bitcoin in the short
term.

Backing up the ephemeral signatures of the pre-signed transactions on the
blockchain itself is an excellent way to ensure that the vault can always
be 'opened'. However, without the annex, this is not as safe as it could
be. Due to the described circular reference problem, the vault creation and
signature backup can't be executed in one atomic operation. For example,
you can store the backup in a child commit/reveal transaction set, but the
vault itself can be confirmed independently and the backup may never
confirm. If you create a vault and lose the ephemeral signatures, the funds
will be lost.

This use case for the annex has been labeled 'speculative' elsewhere. To
me, every use case appears speculative at this point because the annex
isn't available. However, if you believe that time-locked vaults are
important for Bitcoin and also acknowledge that soft forks, such as the one
required for OP_VAULT, aren't easy to implement, I'd argue that the
intermediate solution described above is very relevant.


> As raised on the BIP proposal, those unstructured data use-cases could use
> annex tags with the benefit to combine multiple "types" of unstructured
> data in a single annex payload. As you're raising smaller bits of
> unstructured data might not afford the overhead though my answer with this
> observation would be to move this traffic towards some L2 systems ? In my
> mind, the default of adding a version byte for the usage of unstructured
> data comes with the downside of having future consensus enabled use-cases
> encumbering by the extended witness economic cost.
>

When it comes to the trade-offs associated with various encodings, I fully
acknowledge their existence. The primary motivation behind my proposal to
adopt a simple approach to the Taproot annex is to avoid a potentially long
standardization process. While I am not entirely familiar with the
decision-making process of Bitcoin Core, my experience with other projects
suggests that simpler changes often encounter less resistance and can be
implemented more swiftly. Perhaps I am being overly cautious here, though.


> About the annex payload extension attack described by Greg. If my
> understanding of this transaction-relay jamming griefing issue is correct,
> we can have an annex tag in the future where the signer is committing to
> the total weight of the transaction, or even the max per-input annex size ?
> This should prevent a coinjoin or aggregated commitment transaction
> counterparty to inflate its annex space to downgrade the overall
> transaction feerate, I guess. And I think this could benefit unstructured
> data use-cases too.
>

Regarding the potential payload extension attack, I believe that the
changes proposed in the [3] to allow tx replacement by smaller witness
would provide a viable solution?

Joost

[1]
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-June/021737.html
[2] https://github.com/bitcoin/bips/pull/1421
[3] https://github.com/bitcoin/bitcoin/pull/24007
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230610/4a037e1d/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 13
*******************************************
