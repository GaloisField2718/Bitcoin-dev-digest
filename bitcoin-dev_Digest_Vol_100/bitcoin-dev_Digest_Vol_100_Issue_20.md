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

   1. Re: Actuarial System To Reduce Interactivity In	N-of-N (N	>
      2) Multiparticipant Offchain Mechanisms (David A. Harding)
   2. Re: Actuarial System To Reduce Interactivity In	N-of-N (N	>
      2) Multiparticipant Offchain Mechanisms (ZmnSCPxj)
   3. Re: Scaling Lightning With Simple Covenants (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Sun, 17 Sep 2023 14:12:45 -1000
From: "David A. Harding" <dave@dtrt.org>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N	> 2) Multiparticipant Offchain Mechanisms
Message-ID: <EB311DE7-171B-4D58-B6CF-44E6627D8F14@dtrt.org>
Content-Type: text/plain; charset=utf-8



On September 8, 2023 3:27:38 PM HST, ZmnSCPxj via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>Now, suppose that participant A wants B to be assured that
>A will not double-spend the transaction.
>Then A solicits a single-spend signature from the actuary,
>getting a signature M:
>
>    current state                  +--------+----------------+
>    ---------+-------------+       |        | (M||CSV) && A2 |
>             |(M||CSV) && A| ----> |  M,A   +----------------+
>             +-------------+       |        | (M||CSV) && B2 |
>             |(M||CSV) && B|       +--------+----------------+
>             +-------------+
>             |(M||CSV) && C|
>    ---------+-------------+
>
>The above is now a confirmed transaction.

Good morning, ZmnSCPxj.

What happens if A and M are both members of a group of thieves that control a moderate amount of hash rate?  Can A provide the "confirmed transaction" containing M's sign-only-once signature to B and then, sometime[1] before the CSV expiry, generate a block that contains A's and M's signature over a different transaction that does not pay B?  Either the same transaction or a different transaction in the block also spends M's fidelity bond to a new address exclusively controlled by M, preventing it from being spent by another party unless they reorg the block chain.

If the CSV is a significant amount of time in the future, as we would probably want it to be for efficiency, then the thieving group A and M are part of would not need to control a large amount of hash rate to have a high probability of being successful (and, if they were unsuccessful at the attempted theft, they might not even lose anything and their theft attempt would be invisible to anyone outside of their group).

If A is able to double spend back to herself funds that were previously intended to B, and if cut through transactions were created where B allocated those same funds to C, I think that the double spend invalidates the cut-through even if APO is used, so I think the entire mechanism collapses into reputational trust in M similar to the historic GreenAddress.it co-signing mechanim.

Thanks,

-Dave

[1] Including in the past, via a Finney attack or an extended Finney attack supported by selfish mining.  


------------------------------

Message: 2
Date: Mon, 18 Sep 2023 03:37:46 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N	> 2) Multiparticipant Offchain Mechanisms
Message-ID:
	<dsTMsMJ5WkE8-OInpB-9jqgBoDuQbJXV7uGxTGPYQGdfBKhR-edq7HZIuR8aKJ2TwPY6pIV1vAF1BTTMxrn68h0Qa0TfOoQRGZ_OwBfwoUM=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


Good morning Dave,



Sent with Proton Mail secure email.

------- Original Message -------
On Monday, September 18th, 2023 at 12:12 AM, David A. Harding <dave@dtrt.org> wrote:


> 
> On September 8, 2023 3:27:38 PM HST, ZmnSCPxj via bitcoin-dev bitcoin-dev@lists.linuxfoundation.org wrote:
> 
> > Now, suppose that participant A wants B to be assured that
> > A will not double-spend the transaction.
> > Then A solicits a single-spend signature from the actuary,
> > getting a signature M:
> > 
> > current state +--------+----------------+
> > ---------+-------------+ | | (M||CSV) && A2 |
> > |(M||CSV) && A| ----> | M,A +----------------+
> > +-------------+ | | (M||CSV) && B2 |
> > |(M||CSV) && B| +--------+----------------+
> > +-------------+
> > |(M||CSV) && C|
> > ---------+-------------+
> > 
> > The above is now a confirmed transaction.
> 
> 
> Good morning, ZmnSCPxj.
> 
> What happens if A and M are both members of a group of thieves that control a moderate amount of hash rate? Can A provide the "confirmed transaction" containing M's sign-only-once signature to B and then, sometime[1] before the CSV expiry, generate a block that contains A's and M's signature over a different transaction that does not pay B? Either the same transaction or a different transaction in the block also spends M's fidelity bond to a new address exclusively controlled by M, preventing it from being spent by another party unless they reorg the block chain.

Indeed, the fidelity bond of M would need to be separately locked to `(M && B) || (M && CSV(1 year))`, and the actuary would need to lock new funds before the end of the time period or else the participants would be justified in closing the mechanism with the latest state.

And of course the bond would have to be replicated for each participant `A`, `B`, `C`.... as well, reducing scalability.

If possible, I would like to point attention at developing alternatives to the "sign-only-once" mechanism.

Basically: the point is that we want a mechanism that allows the always-online party (the "actuary") to *only* select transactions, and not move coins otherwise.
This is the nearest I have managed to get, without dropping down to a proof-of-work blockchain.

As noted, in a proof-of-work blockchain, the miners (the always-online party of the blockchain) can only select transactions, and cannot authorize moves without consent of the owners.
That is what we would want to replicate somehow, to reduce interactivity requirements.

Regards,
ZmnSCPxj


------------------------------

Message: 3
Date: Mon, 18 Sep 2023 04:14:55 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: jlspc <jlspc@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<ql7ySzsei1xUnRrnl_XnQ8kDqPy3G7xaTv__4pi9VtX5bFUCnmgu-2YfkjPnuqqDaYgTlviM-R0v1Vvt1hWTTP2eIaHyCKoA25l20y0wTLM=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning John,

> On the other hand, if the consensus rules are changed to allow even simple covenants, this scaling bottleneck is eliminated.
> The key observation is that with covenants, a casual user can co-own an off-chain Lightning channel without having to sign all (or any) of the transactions on which it depends.
> Instead, a UTXO can have a covenant that guarantees the creation of the casual user's channel.
> The simplest way to have a single UTXO create channels for a large number of casual users is to put a covenant on the UTXO that forces the creation of a tree of transactions, the leaves of which are the casual users' channels.
> 
> While such a covenant tree can create channels for millions of casual users without requiring signatures or solving a difficult group coordination problem, it's not sufficient for scaling.
> The problem is that each channel created by a covenant tree has a fixed set of owners, and changing the ownership of a channel created by a covenant tree requires putting the channel on-chain.
> Therefore, assuming that all casual users will eventually want to pair with different dedicated users (and vice-versa), the covenant tree doesn't actually provide any long-term scaling benefit.
> 
> Fortunately, real long-term scaling can be achieved by adding a deadline after which all non-leaf outputs in the covenant tree can be spent without having to meet the conditions of the covenant.
> The resulting covenant tree is called a "timeout-tree" [9, Section 5.3].
> 
> Let A_1 ... A_n denote a large number of casual users, let B be a dedicated user, and let E denote some fixed time in the future.
> User B creates a timeout-tree with expiry E where:
> ?* leaf i has an output that funds a Lightning channel owned by A_i and B, and
> ?* after time E, each non-leaf output in the covenant tree can also be spent by user B without having to meet the conditions of the covenant.

I think, based solely on the description above, that it is not safe for dedicated user `B` to create this, unless it gets a signature from `A_i`.

Basically, suppose the entire thing is single-funded from `B`.
(Funding from `A_i` requires that each `A_i` that wants to contribute be online at the time, at which point you might as well just use signatures instead of `OP_CHECKTEMPLATEVERIFY`.)

If a particular `A_i` never contacts `B` but *does* get the entire path from the funding TXO to the `A_i && B` output confirmed, then the funds that `B` allocated are locked, ***unless*** `B` got a unilateral close signature from `A_i` to spend from `A_i && B`.
Thus, `A_i` still needs to be online at the time `B` signs the funding transaction that anchors the entire tree.

(This is why many people lost funds when they went and implemented `multifundchannel` by themselves --- you need to ensure that all the counterparties in the same batch of openingshave given you unilateral close signatures ***before*** you broadcast the funding transaction.
And in principle, whether the channels are represented onchain by a single transaction output, or multiple separate ones on the same transaction, is immaterial --- the funder still needs a unilateral close signature from the fundee.)

The alternative is to also infect the leaf itself with a lifetime `(A_i && B) || (B && CLTV)`.
This is essentially a Spilman channel variant, which is what we use in swap-in-potentiam, BTW.

If so, then `B` can dedicate that leaf output to a separate 1-input 1-output transaction that takes the `(A_i && B)` branch and spends to a plain `A && B` Lightning channel.
`B` can fund the tree, then when `A_i` comes online and is wiling to accept the channel from `B`, that is when `A_i` creates two signatures:

* For the transaction spending `(A_i && B) || (B && CLTV)` (taking the `A_i && B` branch) to  spend to the `A && B`.
* For the unilateral close transaction from the above output.

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 20
********************************************
