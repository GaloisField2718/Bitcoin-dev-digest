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

   1. Re: bip-0127 "Simple Proof-of-Reserves Transactions" (Ademan)


----------------------------------------------------------------------

Message: 1
Date: Tue, 12 Dec 2023 12:21:29 -0600
From: Ademan <ademan555@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, steven@stevenroose.org
Subject: Re: [bitcoin-dev] bip-0127 "Simple Proof-of-Reserves
	Transactions"
Message-ID:
	<CAKwYL5Fu-02SUmdw8u_mkjJDQoC5txi7XTEju6=gL2MFbRBsxw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Everyone,
    I hope this is the correct venue for discussion, I've been vomiting
half-thoughts into #bitcoin-wizards for months now and I realize I should
probably get over my aversion to the permanence of the ML since IRC is too
synchronous.This might be too much about implementation and too little
concept/theory but I'll leave that decision to the ML mods.

I'm in the process of exploring proof-of-reserves, specifically with
bip-0127 and bdk-reserves (does not claim to be a 100% implementation of
bip-0127, only inspired by it) and I had a few questions/comments on the
bip. Maybe a couple of them are worth clarifying in the bip itself (or
maybe they're just dumb questions). These are in order of the bip's text,
but *question 3 is the most important to me.*

1. sha256 vs double sha256?

> the txid part should be SHA-256("Proof-of-Reserves: Some Message") with
the string encoded as UTF-8.

*Are there merits to SHA-256(m) over SHA-256(SHA-256(m)) aside from
marginal efficiency? Any drawbacks?* My immediate gut reaction was that it
should be double sha256 and it looks like the bdk-reserves implementor
agreed. However, I concede my gut (and in fact my brain as well) are not
particularly good at designing and evaluating cryptographic protocols.

2. output script pubkey?

> The transaction MUST have a single output that is the exact sum of all
the inputs

*What should that output's scriptPubkey be?* bdk-reserves selected an
impossible* to spend p2wpkh script, but couldn't it just as easily be an
empty OP_RETURN? I suppose since the entire transaction is invalid, there
is no requirement that the output be unspendable either. *Would it be
beneficial to recommend an output scriptPubkey in the bip?* (or multiple,
one with SHOULD and the other with MAY ?)

3. validating that inputs commit to the commitment input?

> [The remaining inputs] MUST have signatures that commit to the commitment
input (e.g. using SIGHASH_ALL).

With only the final transaction available, validating that all signatures
use SIGHASH_ALL, except for simple cases like p2pkh and p2wpkh is very
difficult. In bdk-reserves we have libbitcoinconsensus available and use it
for validation of non-commitment inputs. Despite the duplicated validation
time, *does it make sense to malleate the commitment input, then
re-validate all inputs, counting any successful validations as failures? *I
think this is generally a good approach, as it will also reject things like
lightning anchor outputs if they managed to persist on chain, but can
anyone think of a false-negative this approach would produce?

Assuming this approach is acceptable, *what would the ideal malleation look
like?* Tentatively I prepended "MALLEATED" to the commitment string and
re-hashed it, but I suppose setting the txid to a constant like 00000...
might work just as well?

4. conveying data in the commitment message?

*Finally, if I want to commit to data in the commitment message, does
anyone have recommendations on format?* This is probably beyond the scope
of the BIP, and a bit of bikeshedding, but I want to commit to a number of
pieces of information in the commitment (such as the current time, and an
identity pubkey which will be used later in my protocol), and the verifier
should retrieve and verify them.

I could construct an ad-hoc format for the message and parse that, but
something like "Proof-of-Reserves: " || base64(json_data) or even simply
"Proof-of-Reserves: " || json_data is attractively simple to implement.
What have other implementors done? Do you have any recommendations? In my
case the challenge doesn't need to be human readable, so any and all
options are usable as far as I can tell.

I suppose alternatively, the prover could communicate this data out of band
(instead of the commitment message directly), and the verifier would use
the same format and algorithm to construct the commitment message, which
means an ad-hoc format would work fine. I think I'm leaning in this
direction now. Thoughts?

Hopefully that is roughly up to the standards of the list, thanks in
advance for any input.

Thanks,
Dan
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231212/3e5fbb3d/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 5
*******************************************
