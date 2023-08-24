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
      (Greg Sanders)
   2. Re: Standardisation of an unstructured taproot annex
      (Greg Sanders)
   3. Re: Standardisation of an unstructured taproot annex (Joost Jager)
   4. Re: Standardisation of an unstructured taproot annex (Joost Jager)


----------------------------------------------------------------------

Message: 1
Date: Sat, 3 Jun 2023 08:05:59 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Joost Jager <joost.jager@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAB3F3Dugso9MUqr5hMMorL7FargPPspiof+0-qkYGnP_SLyELg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> I think this avoidance of a circular reference is also why LN-Symmetry
uses the annex?

The annex trick specifically is used to force the publication of the
missing piece of the control block corresponding to the new taproot output.
This is to maintain the node's O(1) state while also keeping 0.5RTT channel
updates. Could have also been done with a dangling OP_RETURN, with the
associated restrictions on which sighashes you can use since you now have
to commit to multiple outputs(disallows SIGHASH_SINGLE).

There's also a fair exchange protocol that obviates the need for it using
signature adapters, but the requisite APIs don't exist yet, and doesn't
lend itself naturally to 3+ party scenarios.

> Depending on policy to mitigate this annex malleability vector could
mislead developers into believing their transactions are immune to
replacement, when in fact they might not be.

The issue I'm talking about is where someone's transaction is denied entry
into the mempool entirely because a counter-party decided to put in a
strictly worse transaction for miners by bloating the weight of it, not
adding fees. A strictly worse "API" for paying miners for no gain seems
like a bad trade to me, especially when there are reasonable methods for
mitigating this.

> It may thus be more prudent to permit the utilization of the annex
without restrictions, inform developers of its inherent risks, and
acknowledge that Bitcoin, in its present state, might not be ideally suited
for certain types of applications?

Mempool policy should be an attempt to bridge the gap between node anti-DoS
and an entity's ability to pay miners more via feerate-ordered queue. I
don't think the answer to this problem is to zero out all ability to limit
the sizes of multi-party, multi-input transactions for speculative use
cases.

Greg



On Sat, Jun 3, 2023 at 7:31?AM Joost Jager via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> On Sat, Jun 3, 2023 at 9:49?AM Joost Jager <joost.jager@gmail.com> wrote:
>
>> The removal of the need for a commitment transaction also enables the
>> inclusion of data within a single transaction that relies on its own
>> transaction identifier (txid). This is possible because the txid
>> calculation does not incorporate the annex, where the data would be housed.
>> This feature can be beneficial in scenarios that require the emulation of
>> covenants through the use of presigned transactions involving an ephemeral
>> signer.
>>
>
> I think this avoidance of a circular reference is also why LN-Symmetry
> uses the annex?
>
> Joost
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/00985f2b/attachment-0001.html>

------------------------------

Message: 2
Date: Sat, 3 Jun 2023 08:43:38 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Joost Jager <joost.jager@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAB3F3Dvm1KAHN2OoA_av2WE1=WZ0hNU6paAtN6c9L6+QFw6pfw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

No in this case the txid is identical. Only the wtxid is malleated, with
annex data stuffed to max transaction size.

Cheers,
Greg

On Sat, Jun 3, 2023, 8:36 AM Joost Jager <joost.jager@gmail.com> wrote:

> > Depending on policy to mitigate this annex malleability vector could
>> mislead developers into believing their transactions are immune to
>> replacement, when in fact they might not be.
>>
>> The issue I'm talking about is where someone's transaction is denied
>> entry into the mempool entirely because a counter-party decided to put in a
>> strictly worse transaction for miners by bloating the weight of it, not
>> adding fees. A strictly worse "API" for paying miners for no gain seems
>> like a bad trade to me, especially when there are reasonable methods for
>> mitigating this.
>>
>
> Just to expand this, an example would be a transaction with inputs A' and
> B' signed by two parties A and B. A has a fully signed transaction in
> hands, but can't publish it because B created and published an alternative
> version of it with a large annex for input B'. Wouldn't miners just accept
> A's version because it's fee rate is higher? I am looking at this case
> assuming the user has a direct connection to a miner, ignoring any
> potential concerns related to p2p transport.
>
> Joost
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/49e83857/attachment-0001.html>

------------------------------

Message: 3
Date: Sat, 3 Jun 2023 14:35:51 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV8G4cS1Utr7WQskv4xFG0hAZ9-W8Gv5kRBdJmhuTgbBkw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

>
> > Depending on policy to mitigate this annex malleability vector could
> mislead developers into believing their transactions are immune to
> replacement, when in fact they might not be.
>
> The issue I'm talking about is where someone's transaction is denied entry
> into the mempool entirely because a counter-party decided to put in a
> strictly worse transaction for miners by bloating the weight of it, not
> adding fees. A strictly worse "API" for paying miners for no gain seems
> like a bad trade to me, especially when there are reasonable methods for
> mitigating this.
>

Just to expand this, an example would be a transaction with inputs A' and
B' signed by two parties A and B. A has a fully signed transaction in
hands, but can't publish it because B created and published an alternative
version of it with a large annex for input B'. Wouldn't miners just accept
A's version because it's fee rate is higher? I am looking at this case
assuming the user has a direct connection to a miner, ignoring any
potential concerns related to p2p transport.

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/08c8c4df/attachment.html>

------------------------------

Message: 4
Date: Sat, 3 Jun 2023 14:55:27 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV_H6a-pBcwCjJh+tjs-3SOCJu0SUura=mufagcENMjp3Q@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Sat, Jun 3, 2023 at 2:43?PM Greg Sanders <gsanders87@gmail.com> wrote:

> No in this case the txid is identical. Only the wtxid is malleated, with
> annex data stuffed to max transaction size.
>

This doesn't sound incentive compatible? While gathering context, I did
find https://github.com/bitcoin/bitcoin/pull/24007. Apparently closed
because of a lack of use case. But perhaps the desire to not limit the
annex can revive that proposal?

Joost

>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/a01c286a/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 6
******************************************
