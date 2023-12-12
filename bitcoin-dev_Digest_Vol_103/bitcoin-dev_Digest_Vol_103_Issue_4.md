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

   1. Re: HTLC output aggregation as a mitigation for tx recycling,
      jamming, and on-chain efficiency (covenants) (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Mon, 11 Dec 2023 10:17:23 +0100
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] HTLC output aggregation as a mitigation for
	tx recycling, jamming, and on-chain efficiency (covenants)
Message-ID:
	<CAD3i26B0UAdAbPdNazrQ0RwtorhMM6NnXHkUXqDd3-+mBDLJEA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi, Antoine.

> The attack works on legacy channels if the holder (or local) commitment transaction confirms first, the second-stage HTLC claim transaction is fully malleable by the counterparty.

Yes, correct. Thanks for pointing that out!

> I think one of the weaknesses of this approach is the level of malleability still left to the counterparty, where one might burn in miners fees all the HTLC accumulated value promised to the counterparty, and for which the preimages have been revealed off-chain.

Is this a concern though, if we assume there's no revoked state that
can be broadcast (Eltoo)? Could you share an example of how this would
be played out by an attacker?

> I wonder if a more safe approach, eliminating a lot of competing interests style of mempool games, wouldn't be to segregate HTLC claims in two separate outputs, with full replication of the HTLC lockscripts in both outputs, and let a covenant accepts or rejects aggregated claims with satisfying witness and chain state condition for time lock.

I'm not sure what you mean here, could you elaborate?

> I wonder if in a PTLC world, you can generate an aggregate curve point for all the sub combinations of scalar plausible. Unrevealed curve points in a taproot branch are cheap. It might claim an offered HTLC near-constant size too.

That sounds possible, but how would you deal with the exponential
blowup in the number of combinations?

Cheers,
Johan


On Tue, Nov 21, 2023 at 3:39?AM Antoine Riard <antoine.riard@gmail.com> wrote:
>
> Hi Johan,
>
> Few comments.
>
> ## Transaction recycling
> The transaction recycling attack is made possible by the change made
> to HTLC second level transactions for the anchor channel type[8];
> making it possible to add fees to the transaction by adding inputs
> without violating the signature. For the legacy channel type this
> attack was not possible, as all fees were taken from the HTLC outputs
> themselves, and had to be agreed upon by channel counterparties during
> signing (of course this has its own problems, which is why we wanted
> to change it).
>
> The attack works on legacy channels if the holder (or local) commitment transaction confirms first, the second-stage HTLC claim transaction is fully malleable by the counterparty.
>
> See https://github.com/lightning/bolts/blob/master/03-transactions.md#offered-htlc-outputs (only remote_htlcpubkey required)
>
> Note a replacement cycling attack works in a future package-relay world too.
>
> See test: https://github.com/ariard/bitcoin/commit/19d61fa8cf22a5050b51c4005603f43d72f1efcf
>
> > The idea of HTLC output aggregation is to collapse all HTLC outputs on
> > the commitment to a single one. This has many benefits (that I?ll get
> > to), one of them being the possibility to let the spender claim the
> > portion of the output that they?re right to, deciding how much should
> > go to fees. Note that this requires a covenant to be possible.
>
> Another advantage of HTLC output aggregation is the reduction of fee-bumping reserves requirements on channel counterparties, as second-stage HTLC transactions have common fields (nVersion, nLocktime, ...) *could* be shared.
>
> > ## A single HTLC output
> > Today, every forwarded HTLC results in an output that needs to be
> > manifested on the commitment transaction in order to claw back money
> > in case of an uncooperative channel counterparty. This puts a limit on
> > the number of active HTLCs (in order for the commitment transaction to
> > not become too large) which makes it possible to jam the channel with
> > small amounts of capital [1]. It also turns out that having this limit
> > be large makes it expensive and complicated to sweep the outputs
> > efficiently [2].
>
> > Instead of having new HTLC outputs manifest for each active
> > forwarding, with covenants on the base layer one could create a single
> > aggregated output on the commitment. The output amount being the sum
> > of the active HTLCs (offered and received), alternatively one output
> > for received and one for offered. When spending this output, you would
> > only be entitled to the fraction of the amount corresponding to the
> > HTLCs you know the preimage for (received), or that has timed out
> > (offered).
>
> > ## Impacts to transaction recycling
> > Depending on the capabilities of the covenant available (e.g.
> > restricting the number of inputs to the transaction) the transaction
> > spending the aggregated HTLC output can be made self sustained: the
> > spender will be able to claim what is theirs (preimage or timeout) and
> > send it to whatever output they want, or to fees. The remainder will
> > go back into a covenant restricted output with the leftover HTLCs.
> > Note that this most likely requires Eltoo in order to not enable fee
> > siphoning[7].
>
> I think one of the weaknesses of this approach is the level of malleability still left to the counterparty, where one might burn in miners fees all the HTLC accumulated value promised to the counterparty, and for which the preimages have been revealed off-chain.
>
> I wonder if a more safe approach, eliminating a lot of competing interests style of mempool games, wouldn't be to segregate HTLC claims in two separate outputs, with full replication of the HTLC lockscripts in both outputs, and let a covenant accepts or rejects aggregated claims with satisfying witness and chain state condition for time lock.
>
> > ## Impacts to slot jamming
> > With the aggregated output being a reality, it changes the nature of
> > ?slot jamming? [1] significantly. While channel capacity must still be
> > reserved for in-flight HTLCs, one no longer needs to allocate a
> > commitment output for each up to some hardcoded limit.
>
> > In today?s protocol this limit is 483, and I believe most
> > implementations default to an even lower limit. This leads to channel
> > jamming being quite inexpensive, as one can quickly fill a channel
> > with small HTLCs, without needing a significant amount of capital to
> > do so.
>
> > The origins of the 483 slot limits is the worst case commitment size
> > before getting into unstandard territory [3]. With an aggregated
> > output this would no longer be the case, as adding HTLCs would no
> > longer affect commitment size. Instead, the full on-chain footprint of
> > an HTLC would be deferred until claim time.
>
> > Does this mean one could lift, or even remove the limit for number of
> > active HTLCs? Unfortunately, the obvious approach doesn?t seem to get
> > rid of the problem entirely, but mitigates it quite a bit.
>
> Yes, protocol limit of 483 is a long-term limit on the payment throughput of the LN, though as an upper bound we have the dust limits and mempool fluctuations rendering irrelevant the claim of such aggregated dust outputs. Aggregated claims might give a more dynamic margin of what is a tangible and trust-minimized HTLC payment.
>
> > ### Slot jamming attack scenario
> > Consider the scenario where an attacker sends a large number of
> > non-dust* HTLCs across a channel, and the channel parties enforce no
> > limit on the number of active HTLCs.
>
> > The number of payments would not affect the size of the commitment
> > transaction at all, only the size of the witness that must be
> > presented when claiming or timing out the HTLCs. This means that there
> > is still a point at which chain fees get high enough for the HTLC to
> > be uneconomical to claim. This is no different than in today?s spec,
> > and such HTLCs will just be stranded on-chain until chain fees
> > decrease, at which point there is a race between the success and
> > timeout spends.
>
> > There seems to be no way around this; if you want to claim an HTLC
> > on-chain, you need to put the preimage on-chain. And when the HTLC
> > first reaches you, you have no way of predicting the future chain fee.
> > With a large number of uneconomical HTLCs in play, the total BTC
> > exposure could still be very large, so you might want to limit this
> > somewhat.
>
> > * Note that as long as the sum of HTLCs exceeds the dust limit, one
> > could manifest the output on the transaction.
>
> Unless we introduce sliding windows during which the claim periods of an HTLC can be claimed and freeze accordingly the HTLC-timeout path.
>
> See: https://fc22.ifca.ai/preproceedings/119.pdf
>
> Bad news: you will need off-chain consensus on the feerate threshold at which the sliding windows kick-out among all the routing nodes participating in the HTLC payment path.
>
> > ## The good news
> > With an aggregated HTLC output, the number of HTLCs would no longer
> > impact the commitment transaction size while the channel is open and
> > operational.
>
> > The marginal cost of claiming an HTLC with a preimage on-chain would
> > be much lower; no new inputs or outputs, only a linear increase in the
> > witness size. With a covenant primitive available, the extra footprint
> > of the timeout and success transactions would no longer exist.
>
> > Claiming timed out HTLCs could still be made close to constant size
> > (no preimage to present), so no additional on-chain cost with more
> > HTLCs.
>
> I wonder if in a PTLC world, you can generate an aggregate curve point for all the sub combinations of scalar plausible. Unrevealed curve points in a taproot branch are cheap. It might claim an offered HTLC near-constant size too.
>
> > ## The bad news
> > The most obvious problem is that we would need a new covenant
> > primitive on L1 (see below). However, I think it could be beneficial
> > to start exploring these ideas now in order to guide the L1 effort
> > towards something we could utilize to its fullest on L2.
>
> > As mentioned, even with a functioning covenant, we don?t escape the
> > fact that a preimage needs to go on-chain, pricing out HTLCs at
> > certain fee rates. This is analogous to the dust exposure problem
> > discussed in [6], and makes some sort of limit still required.
>
> Ideally such covenant mechanisms would generalize to the withdrawal phase of payment pools, where dozens or hundreds of participants wish to confirm their non-competing withdrawal transactions concurrently. While unlocking preimage or scalar can be aggregated in a single witness, there will still be a need to verify that each withdrawal output associated with an unlocking secret is present in the transaction.
>
> Maybe few other L2s are answering this N-inputs-to-M-outputs pattern with advanced locking scripts conditions to satisfy.
>
> > ### Open question
> > With PTLCs, could one create a compact proof showing that you know the
> > preimage for m-of-n of the satoshis in the output? (some sort of
> > threshold signature).
>
> > If we could do this we would be able to remove the slot jamming issue
> > entirely; any number of active PTLCs would not change the on-chain
> > cost of claiming them.
>
> See comments above, I think there is a plausible scheme here you just generate all the point combinations possible, and only reveal the one you need at broadcast.
>
> > ## Covenant primitives
> > A recursive covenant is needed to achieve this. Something like OP_CTV
> > and OP_APO seems insufficient, since the number of ways the set of
> > HTLCs could be claimed would cause combinatorial blowup in the number
> > of possible spending transactions.
>
> > Personally, I?ve found the simple yet powerful properties of
> > OP_CHECKCONTRACTVERIFY [4] together with OP_CAT and amount inspection
> > particularly interesting for the use case, but I?m certain many of the
> > other proposals could achieve the same thing. More direct inspection
> > like you get from a proposal like OP_TX[9] would also most likely have
> > the building blocks needed.
>
> As pointed out during the CTV drama and payment pool public discussion years ago, what would be very useful to tie-break among all covenant constructions would be an efficiency simulation framework. Even if the same semantic can be achieved independently by multiple covenants, they certainly do not have the same performance trade-offs (e.g average and worst-case witness size).
>
> I don't think the blind approach of activating many complex covenants at the same time is conservative enough in Bitcoin, where one might design "malicious" L2 contracts, of which the game-theory is not fully understood.
>
> See e.g https://blog.bitmex.com/txwithhold-smart-contracts/
>
> > ### Proof-of-concept
> > I?ve implemented a rough demo** of spending an HTLC output that pays
> > to a script with OP_CHECKCONTRACTVERIFY to achieve this [5]. The idea
> > is to commit to all active HTLCs in a merkle tree, and have the
> > spender provide merkle proofs for the HTLCs to claim, claiming the sum
> > into a new output. The remainder goes back into a new output with the
> > claimed HTLCs removed from the merkle tree.
>
> > An interesting trick one can do when creating the merkle tree, is
> > sorting the HTLCs by expiry. This means that one in the timeout case
> > claim a subtree of HTLCs using a single merkle proof (and RBF this
> > batched timeout claim as more and more HTLCs expire) reducing the
> > timeout case to constant size witness (or rather logarithmic in the
> > total number of HTLCs).
>
> > **Consider it an experiment, as it is missing a lot before it could be
> > usable in any real commitment setting.
>
> I think this is an interesting question if more advanced cryptosystems based on assumptions other than the DL problem could constitute a factor of scalability of LN payment throughput by orders of magnitude, by decoupling number of off-chain payments from the growth of the on-chain witness size need to claim them, without lowering in security as with trimmed HTLC due to dust limits.
>
> Best,
> Antoine
>
> Le jeu. 26 oct. 2023 ? 20:28, Johan Tor?s Halseth via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> a ?crit :
>>
>> Hi all,
>>
>> After the transaction recycling has spurred some discussion the last
>> week or so, I figured it could be worth sharing some research I?ve
>> done into HTLC output aggregation, as it could be relevant for how to
>> avoid this problem in a future channel type.
>>
>> TLDR; With the right covenant we can create HTLC outputs that are much
>> more chain efficient, not prone to tx recycling and harder to jam.
>>
>> ## Transaction recycling
>> The transaction recycling attack is made possible by the change made
>> to HTLC second level transactions for the anchor channel type[8];
>> making it possible to add fees to the transaction by adding inputs
>> without violating the signature. For the legacy channel type this
>> attack was not possible, as all fees were taken from the HTLC outputs
>> themselves, and had to be agreed upon by channel counterparties during
>> signing (of course this has its own problems, which is why we wanted
>> to change it).
>>
>> The idea of HTLC output aggregation is to collapse all HTLC outputs on
>> the commitment to a single one. This has many benefits (that I?ll get
>> to), one of them being the possibility to let the spender claim the
>> portion of the output that they?re right to, deciding how much should
>> go to fees. Note that this requires a covenant to be possible.
>>
>> ## A single HTLC output
>> Today, every forwarded HTLC results in an output that needs to be
>> manifested on the commitment transaction in order to claw back money
>> in case of an uncooperative channel counterparty. This puts a limit on
>> the number of active HTLCs (in order for the commitment transaction to
>> not become too large) which makes it possible to jam the channel with
>> small amounts of capital [1]. It also turns out that having this limit
>> be large makes it expensive and complicated to sweep the outputs
>> efficiently [2].
>>
>> Instead of having new HTLC outputs manifest for each active
>> forwarding, with covenants on the base layer one could create a single
>> aggregated output on the commitment. The output amount being the sum
>> of the active HTLCs (offered and received), alternatively one output
>> for received and one for offered. When spending this output, you would
>> only be entitled to the fraction of the amount corresponding to the
>> HTLCs you know the preimage for (received), or that has timed out
>> (offered).
>>
>> ## Impacts to transaction recycling
>> Depending on the capabilities of the covenant available (e.g.
>> restricting the number of inputs to the transaction) the transaction
>> spending the aggregated HTLC output can be made self sustained: the
>> spender will be able to claim what is theirs (preimage or timeout) and
>> send it to whatever output they want, or to fees. The remainder will
>> go back into a covenant restricted output with the leftover HTLCs.
>> Note that this most likely requires Eltoo in order to not enable fee
>> siphoning[7].
>>
>> ## Impacts to slot jamming
>> With the aggregated output being a reality, it changes the nature of
>> ?slot jamming? [1] significantly. While channel capacity must still be
>> reserved for in-flight HTLCs, one no longer needs to allocate a
>> commitment output for each up to some hardcoded limit.
>>
>> In today?s protocol this limit is 483, and I believe most
>> implementations default to an even lower limit. This leads to channel
>> jamming being quite inexpensive, as one can quickly fill a channel
>> with small HTLCs, without needing a significant amount of capital to
>> do so.
>>
>> The origins of the 483 slot limits is the worst case commitment size
>> before getting into unstandard territory [3]. With an aggregated
>> output this would no longer be the case, as adding HTLCs would no
>> longer affect commitment size. Instead, the full on-chain footprint of
>> an HTLC would be deferred until claim time.
>>
>> Does this mean one could lift, or even remove the limit for number of
>> active HTLCs? Unfortunately, the obvious approach doesn?t seem to get
>> rid of the problem entirely, but mitigates it quite a bit.
>>
>> ### Slot jamming attack scenario
>> Consider the scenario where an attacker sends a large number of
>> non-dust* HTLCs across a channel, and the channel parties enforce no
>> limit on the number of active HTLCs.
>>
>> The number of payments would not affect the size of the commitment
>> transaction at all, only the size of the witness that must be
>> presented when claiming or timing out the HTLCs. This means that there
>> is still a point at which chain fees get high enough for the HTLC to
>> be uneconomical to claim. This is no different than in today?s spec,
>> and such HTLCs will just be stranded on-chain until chain fees
>> decrease, at which point there is a race between the success and
>> timeout spends.
>>
>> There seems to be no way around this; if you want to claim an HTLC
>> on-chain, you need to put the preimage on-chain. And when the HTLC
>> first reaches you, you have no way of predicting the future chain fee.
>> With a large number of uneconomical HTLCs in play, the total BTC
>> exposure could still be very large, so you might want to limit this
>> somewhat.
>>
>> * Note that as long as the sum of HTLCs exceeds the dust limit, one
>> could manifest the output on the transaction.
>>
>> ## The good news
>> With an aggregated HTLC output, the number of HTLCs would no longer
>> impact the commitment transaction size while the channel is open and
>> operational.
>>
>> The marginal cost of claiming an HTLC with a preimage on-chain would
>> be much lower; no new inputs or outputs, only a linear increase in the
>> witness size. With a covenant primitive available, the extra footprint
>> of the timeout and success transactions would no longer exist.
>>
>> Claiming timed out HTLCs could still be made close to constant size
>> (no preimage to present), so no additional on-chain cost with more
>> HTLCs.
>>
>> ## The bad news
>> The most obvious problem is that we would need a new covenant
>> primitive on L1 (see below). However, I think it could be beneficial
>> to start exploring these ideas now in order to guide the L1 effort
>> towards something we could utilize to its fullest on L2.
>>
>> As mentioned, even with a functioning covenant, we don?t escape the
>> fact that a preimage needs to go on-chain, pricing out HTLCs at
>> certain fee rates. This is analogous to the dust exposure problem
>> discussed in [6], and makes some sort of limit still required.
>>
>> ### Open question
>> With PTLCs, could one create a compact proof showing that you know the
>> preimage for m-of-n of the satoshis in the output? (some sort of
>> threshold signature).
>>
>> If we could do this we would be able to remove the slot jamming issue
>> entirely; any number of active PTLCs would not change the on-chain
>> cost of claiming them.
>>
>> ## Covenant primitives
>> A recursive covenant is needed to achieve this. Something like OP_CTV
>> and OP_APO seems insufficient, since the number of ways the set of
>> HTLCs could be claimed would cause combinatorial blowup in the number
>> of possible spending transactions.
>>
>> Personally, I?ve found the simple yet powerful properties of
>> OP_CHECKCONTRACTVERIFY [4] together with OP_CAT and amount inspection
>> particularly interesting for the use case, but I?m certain many of the
>> other proposals could achieve the same thing. More direct inspection
>> like you get from a proposal like OP_TX[9] would also most likely have
>> the building blocks needed.
>>
>> ### Proof-of-concept
>> I?ve implemented a rough demo** of spending an HTLC output that pays
>> to a script with OP_CHECKCONTRACTVERIFY to achieve this [5]. The idea
>> is to commit to all active HTLCs in a merkle tree, and have the
>> spender provide merkle proofs for the HTLCs to claim, claiming the sum
>> into a new output. The remainder goes back into a new output with the
>> claimed HTLCs removed from the merkle tree.
>>
>> An interesting trick one can do when creating the merkle tree, is
>> sorting the HTLCs by expiry. This means that one in the timeout case
>> claim a subtree of HTLCs using a single merkle proof (and RBF this
>> batched timeout claim as more and more HTLCs expire) reducing the
>> timeout case to constant size witness (or rather logarithmic in the
>> total number of HTLCs).
>>
>> **Consider it an experiment, as it is missing a lot before it could be
>> usable in any real commitment setting.
>>
>>
>> [1] https://bitcoinops.org/en/topics/channel-jamming-attacks/#htlc-jamming-attack
>> [2] https://github.com/lightning/bolts/issues/845
>> [3] https://github.com/lightning/bolts/blob/aad959a297ff66946effb165518143be15777dd6/02-peer-protocol.md#rationale-7
>> [4] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021182.html
>> [5] https://github.com/halseth/tapsim/blob/b07f29804cf32dce0168ab5bb40558cbb18f2e76/examples/matt/claimpool/script.txt
>> [6] https://lists.linuxfoundation.org/pipermail/lightning-dev/2021-October/003257.html
>> [7] https://github.com/lightning/bolts/issues/845#issuecomment-937736734
>> [8] https://github.com/lightning/bolts/blob/8a64c6a1cef979b3f0cecb00ba7a48c2d28b3588/03-transactions.md?plain=1#L333
>> [9] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020450.html
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 4
*******************************************
