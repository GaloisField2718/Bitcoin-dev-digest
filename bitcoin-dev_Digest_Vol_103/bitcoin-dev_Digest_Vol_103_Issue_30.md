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

   1. Re: Scaling Lightning Safely With Feerate-Dependent	Timelocks
      (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Thu, 28 Dec 2023 18:19:06 +0000
From: jlspc <jlspc@protonmail.com>
To: Eric Voskuil <eric@voskuil.org>
Cc: Antoine Riard <antoine.riard@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>,
	lightning-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent	Timelocks
Message-ID:
	<dkAxjJIFndwa9WN8Hgrp92I3l3IH0SGRhheMntDfaaDjGTOOnv0s8zIivWE0yiHhh9ty0TQ_IUvkg9Zrs2KFjdSoH1_DrvCymhxA9hF-6Ko=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Eric,

I agree that users can pay miners offchain and miners can create blocks where the difference between inputs and outputs exceeds the fees paid (by mining their own transactions). I model that behavior as dishonest mining. Onchain fees seem to reflect congestion for now, but it's true that FDTs rely on having a sufficient fraction of honest miners.

Regards,
John

Sent with [Proton Mail](https://proton.me/) secure email.

On Friday, December 22nd, 2023 at 8:09 PM, Eric Voskuil <eric@voskuil.org> wrote:

> The fees paid to mine the set of transactions in a given block are known only to the miner that produced the block. Assuming that tx inputs less outputs represents an actual economic force is an error.
>
> e
>
>> On Dec 22, 2023, at 09:24, jlspc via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> ?
>>
>> Hi Antoine,
>>
>> Thanks for your thoughtful response.
>>
>> Comments inline below:
>>
>>> Hi John,
>>
>>> While the idea of using sliding reaction window for blockchain congestion
>>> detection has been present in the "smart contract" space at large [0] and
>>> this has been discussed informally among Lightning devs and covenant
>>> designers few times [1] [2], this is the first and best formalization of
>>> sliding-time-locks in function of block fee rates for Bitcoin I'm aware
>>> off, to the best of my knowledge.
>>
>> Thanks!
>>
>>> Here my understanding of the feerate-dependent timelock proposal.
>>
>>> A transaction cannot be included in a block:
>>> - height-based or epoch-based absolute or relative timelocks are not
>>> satisfied according to current consensus rules (bip68 and bip 113 and
>>> implementation details)
>>> - less than `block_count` has a block median-feerate above the
>>> median-feerate of the `window_size` period
>>
>> It's a little bit different from that.
>> The transaction cannot be included in the blockchain until after an aligned window W of window_size blocks where:
>> 1) W starts no sooner than when the height-based or epoch-based absolute and/or relative timelocks have been satisfied, and
>> 2) W contains fewer than block_count blocks with median feerate greater than feerate_value_bound.
>>
>> Note that the aligned window cannot start until the absolute and/or relative timelocks have been satisfied and the transaction itself has to come after the aligned window.
>> However, once such an aligned window exists in the blockchain, the transaction can appear at any later time (and not just within a window that itself meets the block_count and feerate_value_bound limitations).
>>
>>> A median feerate is computed for each block.
>>> (This is unclear to me if this is the feerate for half of the block's
>>> weight or the median feerate with all weight units included in the
>>> block as the sample)
>>
>> A feerate F is the median feerate of a block B if F is the largest feerate such that the total size of the transactions in B with feerate greater or equal to F is at least 2 million vbytes.
>>
>>> From then, you have 3 parameters included in the nSequence field.
>>> - feerate_value_bound
>>> - window_size
>>> - block_count
>>
>>> Those parameters can be selected by the transaction builder (and
>>> committed with a signature or hash chain-based covenant).
>>> As such, off-chain construction counterparties can select the
>>> feerate_value_bound at which their time-sensitive transaction
>>> confirmation will be delayed.
>>
>>> E.g let's say you have a LN-penalty Alice-Bob channel. Second-stage
>>> HTLC transactions are pre-signed with feerate_value_bound at 100 sat /
>>> vbytes.
>>> The window_size selected is 100 blocks and the block_count is 70 (this
>>> guarantees tampering-robustness of the feerate_value_bound in face of
>>> miners coalitions).
>>
>>> There is 1 BTC offered HTLC pending with expiration time T, from Alice to Bob.
>>
>>> If at time T, the per-block median feerate of at least 70 blocks over
>>> the latest 100 block is above 100 sat / vbytes, any Alice's
>>> HTLC-timeout or Bob's HTLC-preimage cannot be included in the chain.
>>
>> The rules are actually:
>> 1) wait until time T, then
>> 2) wait until the start of a full aligned window W with 100 consecutive blocks that starts no earlier than T and that has fewer than 70 blocks with median feerate above 100 sats/vbyte.
>> (The values 100, 70, and 100 cannot actually be selected in the implementation in the paper, but that's a technical detail and could be changed if the FDT is specified in the annex, as you propose.)
>>
>>> From my understanding, Feerate-Dependent Timelocks effectively
>>> constitute the lineaments of a solution to the "Forced Expiration
>>> Spam" as described in the LN paper.
>>
>> Great!
>>
>>> I think you have few design caveats to be aware off:
>>> - for current LN-penalty, the revokeable scripts should be modified to
>>> ensure the CSV opcode inspect the enforcement of FDT's parameters, as
>>> those revokeable scripts are committed by all parties
>>
>> Yes, definitely.
>>
>>> - there should be a delay period at the advantage of one party
>>> otherwise you still a feerate-race if the revocation bip68 timelock
>>> has expired during the FDT delay
>>
>>> As such, I believe the FDT parameters should be enriched with another
>>> parameter : `claim_grace_period`, a new type of relative timelock of
>>> which the endpoint should be the `feerate_value_bound` itself.
>>
>> I'm not sure I'm following your proposal.
>> Are you suggesting that the transaction with the FDT has to wait an additional claim_grace_period in order to allow conflicting transactions from the other party to win the race?
>> For example, assume the HTLC-success transaction has a higher feerate than the feerate_value_bound, and the conflicting HTLC-timeout transaction has an FDT with the feerate_value_bound (and suitable window_size and block_count parameters to defend against miner attacks).
>> In this case, is the worry that the HTLC-success and HTLC-timeout transactions could both be delayed until there is a window W that meets the FDT's feerate_value_bound, window_size and block_count parameters, at which point they would race against each other and either could win?
>> Is the reason to delay the HTLC-timeout by an additional claim_grace_period to guarantee that the HTLC-success transaction will win the race?
>> If so, I don't think it's needed, given the exact definition of the FDT proposal.
>> This is because *during* the window W that meets the FDT's requirements, the HTLC-success transaction should get mined into one of the blocks in W that has a median feerate no larger than feerate_value_bound, assuming honest miners.
>> The assumption of honest miners is resolved by setting the window_size and block_count parameters appropriately.
>> Does that make sense?
>>
>>> I think it works in terms of consensus chain state, validation
>>> resources and reorg-safety are all the parameters that are
>>> self-contained in the spent FDT-encumbered transaction itself.
>>> If the per-block feerate fluctuates, the validity of the ulterior
>>> FDT-locked transactions changes too, though this is already the case
>>> with timelock-encumbered transactions.
>>
>>> (One corollary for Lightning, it sounds like all the channels carrying
>>> on a HTLC along a payment path should have the same FDT-parameters to
>>> avoid off-chain HTLC double-spend, a risk not clearly articulated in
>>> the LN paper).
>>
>> It's interesting that you focused on securing HTLCs, as I was focused on securing LN channel state (e.g., getting the right Commitment tx) and factory state.
>> The challenge with using FDTs to secure HTLCs is that you need a way to specify a sequence of FDTs (corresponding to the hops in a LN payment) that expire with enough time between them and with a low feerate period between them.
>> For example, consider a payment with n hops, where hop i has an HTLC that expires at time T_i, and where hop n is the last hop.
>> Without FDTs, one would select expiries such that T_i + cltv_expiry_delta_i < T_(i-1).
>> With FDTs, one can't just use the same T_i's and add an FDT that follows that T_i, because the feerate could be high until well after the first few T_i's are reached.
>> For example, assume T_n, T_(n-1) and T_(n-2) all occur before feerates fall below the feerate_value_bound.
>> In this case, the HTLC-timeout TXs for hops n, n-1 and n-2 would all be delayed until the feerates fell, and then they would all be able to be put onchain at the same time (without the required cltv_expiry_deltas between them).
>>
>> One attempt to solve this would be to add another parameter that specifies how many blocks to wait after fees have falled below the feerate_value_bound (like the claim_grace_perid, if I understand it correctly).
>> However, that doesn't solve the problem because the congestion could start, and the feerate_value_bound could be exceeded, at any time.
>> For example, the feerate_value_bound could first be exceeded just after T_(n-1), in which case the fees would be too high to put the HTLC-success transaction onchain in hop T_(n-2).
>>
>> What we really need is the ability to ensure that there have been enough low feerate expiries, each separated by the required cltv_expiry_delta.
>> This can be achieved by adding a new parameter, number_of_windows, that specifies how many low feerate windows W_1, W_2, etc., are required, all of which meet the feerate_value_bound, window_size and block_count parameters (and all of which start no later than when the standard absolute and relative timelocks have been satisfied).
>> With this new parameter, lower numbered hops (closer to the sender) can use larger values of number_of_windows in order to guarantee low feerate periods that meet the required cltv_expiry_deltas.
>>
>> For example, assume feerate_value_bound is 256 sats/vbyte, window_size is 256, and block_count is 64.
>> Then, give the HTLC-timeout transaction in hop i an absolute timelock of T_n (the timelock for hop n) and an FDT with number_of_windows equal to (n-i+1) (and with feerate_value_bound, window_size and block_count as above).
>> In this case, as long as each cltv_expiry_delta is less than window_size - block_count = 192, then in each hop the party offered the HTLC can put their HTLC-success transaction onchain in a low feerate block after they have seen the hash preimage for at least cltv_expiry_delta blocks.
>> (In practice, the parameters could be tweaked a bit to break the association between hops, such as by using more restrictive feerate_value_bounds and/or block_counts as one gets closer to the source, and by increasing the number_of_windows parameter by more than one per hop as one gets closer to the source.)
>>
>>> Given the one more additional parameter `claim_grace_period`, I think
>>> it would be wiser design to move all the FDT parameters in the bip341
>>> annex.
>>> There is more free bits room there and additionally you can have
>>> different FDT parameters for each of your HTLC outputs in a single LN
>>> transaction, if combined with future covenant mechanisms like HTLC
>>> aggregation [3].
>>> (The current annex design draft has been designed among others to
>>> enable such "block-feerate-lock-point" [4] [5])
>>
>> I like your idea of putting the FDT parameters in the annex.
>> This is required if we add the number_of_windows parameter that I mentioned above.
>>
>> In addition to finding enough bits in the transaction to hold the FDT parameters, there is a cost to increasing the parameters, namely the memory required to verify transactions with FDTs.
>> In the proposal in the paper, FDTs could be specified with 14 bits, so there were only 2^14 = 16k different values for which the starting block of the most recent aligned window satisfying those parameters has to be stored in order to quickly verify FDTs.
>> Assuming 4 bytes to store the starting block of a window, that's just 64k bytes of DRAM.
>> If we add a 6-bit number_of_windows parameter, that increases the storage by a factor of 64 to 4MB.
>> That's still pretty small, but we have to be careful to not make this too expensive.
>>
>>> I cannot assert that the FDT proposal makes the timeout-tree protocol
>>> more efficient than state-of-the-art channel factories and payment
>>> pool constructions.
>>> Still from my understanding, all those constructions are sharing
>>> frailties in face of blockchain congestion and they would need
>>> something like FDT.
>>
>> I agree that FDTs don't make timeout-trees more competitive against any other factory protoocol.
>> I also agree that FDTs can be used to make all of the LN channel and factory protocools safer.
>> If we extend the idea to include a number_of_windows parameter, then we should even be able to make HTLCs safer.
>>
>>> I'm truly rejoicing at the idea that we have now the start of a
>>> proposal solving one of the most imperative issues of Lightning and
>>> other time-sensitive use-cases.
>>
>> I'm very happy you see it that way.
>> Please let me know what you think of the number_of_windows idea, and if you have any other ideas for making HTLCs safer.
>>
>> Regards,
>> John
>>
>> Sent with [Proton Mail](https://proton.me/) secure email.
>>
>> On Sunday, December 17th, 2023 at 3:01 PM, Antoine Riard <antoine.riard@gmail.com> wrote:
>>
>>> Hi John,
>>>
>>> While the idea of using sliding reaction window for blockchain congestion detection has been present in the "smart contract" space at large [0] and this has been discussed informally among Lightning devs and covenant designers few times [1] [2], this is the first and best formalization of sliding-time-locks in function of block fee rates for Bitcoin I'm aware off, to the best of my knowledge.
>>>
>>> Here my understanding of the feerate-dependent timelock proposal.
>>>
>>> A transaction cannot be included in a block:
>>> - height-based or epoch-based absolute or relative timelocks are not satisfied according to current consensus rules (bip68 and bip 113 and implementation details)
>>> - less than `block_count` has a block median-feerate above the median-feerate of the `window_size` period
>>>
>>> A median feerate is computed for each block.
>>> (This is unclear to me if this is the feerate for half of the block's weight or the median feerate with all weight units included in the block as the sample)
>>>
>>> From then, you have 3 parameters included in the nSequence field.
>>> - feerate_value_bound
>>> - window_size
>>> - block_count
>>>
>>> Those parameters can be selected by the transaction builder (and committed with a signature or hash chain-based covenant).
>>> As such, off-chain construction counterparties can select the feerate_value_bound at which their time-sensitive transaction confirmation will be delayed.
>>>
>>> E.g let's say you have a LN-penalty Alice-Bob channel. Second-stage HTLC transactions are pre-signed with feerate_value_bound at 100 sat / vbytes.
>>> The window_size selected is 100 blocks and the block_count is 70 (this guarantees tampering-robustness of the feerate_value_bound in face of miners coalitions).
>>>
>>> There is 1 BTC offered HTLC pending with expiration time T, from Alice to Bob.
>>>
>>> If at time T, the per-block median feerate of at least 70 blocks over the latest 100 block is above 100 sat / vbytes, any Alice's HTLC-timeout or Bob's HTLC-preimage cannot be included in the chain.
>>>
>>> From my understanding, Feerate-Dependent Timelocks effectively constitute the lineaments of a solution to the "Forced Expiration Spam" as described in the LN paper.
>>>
>>> I think you have few design caveats to be aware off:
>>> - for current LN-penalty, the revokeable scripts should be modified to ensure the CSV opcode inspect the enforcement of FDT's parameters, as those revokeable scripts are committed by all parties
>>> - there should be a delay period at the advantage of one party otherwise you still a feerate-race if the revocation bip68 timelock has expired during the FDT delay
>>>
>>> As such, I believe the FDT parameters should be enriched with another parameter : `claim_grace_period`, a new type of relative timelock of which the endpoint should be the `feerate_value_bound` itself.
>>>
>>> I think it works in terms of consensus chain state, validation resources and reorg-safety are all the parameters that are self-contained in the spent FDT-encumbered transaction itself.
>>> If the per-block feerate fluctuates, the validity of the ulterior FDT-locked transactions changes too, though this is already the case with timelock-encumbered transactions.
>>>
>>> (One corollary for Lightning, it sounds like all the channels carrying on a HTLC along a payment path should have the same FDT-parameters to avoid off-chain HTLC double-spend, a risk not clearly articulated in the LN paper).
>>>
>>> Given the one more additional parameter `claim_grace_period`, I think it would be wiser design to move all the FDT parameters in the bip341 annex.
>>> There is more free bits room there and additionally you can have different FDT parameters for each of your HTLC outputs in a single LN transaction, if combined with future covenant mechanisms like HTLC aggregation [3].
>>> (The current annex design draft has been designed among others to enable such "block-feerate-lock-point" [4] [5])
>>>
>>> I cannot assert that the FDT proposal makes the timeout-tree protocol more efficient than state-of-the-art channel factories and payment pool constructions.
>>> Still from my understanding, all those constructions are sharing frailties in face of blockchain congestion and they would need something like FDT.
>>>
>>> I'm truly rejoicing at the idea that we have now the start of a proposal solving one of the most imperative issues of Lightning and other time-sensitive use-cases.
>>> (Note, I've not reviewed the analysis and game-theory in the face of miners collusion / coalition, as I think the introduction of a `claim_grace_period` is modifying the fundamentals).
>>>
>>> Best,
>>> Antoine
>>>
>>> [0]
>>> https://fc22.ifca.ai/preproceedings/119.pdf
>>> [1]
>>> https://github.com/ariard/bitcoin-contracting-primitives-wg/blob/main/meetings/meetings-18-04.md
>>> [2]
>>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-November/022180.html
>>> [3]
>>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-October/022093.html
>>> [4]
>>> https://github.com/bitcoin-inquisition/bitcoin/pull/9
>>>
>>> [5]
>>> https://github.com/bitcoin/bips/pull/1381
>>>
>>> Le ven. 15 d?c. 2023 ? 09:20, jlspc via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> a ?crit :
>>>
>>>> TL;DR
>>>> =====
>>>> * All known Lightning channel and factory protocols are susceptible to forced expiration spam attacks, in which an attacker floods the blockchain with transactions in order to prevent honest users from putting their transactions onchain before timelocks expire.
>>>> * Feerate-Dependent Timelocks (FDTs) are timelocks that automatically extend when blockchain feerates spike.
>>>>   - In the normal case, there's no spike in feerates and thus no tradeoff between capital efficiency and safety.
>>>>   - If a dishonest user attempts a forced expiration spam attack, feerates increase and FDTs are extended, thus penalizing the attacker by keeping their capital timelocked for longer.
>>>>   - FDTs are tunable and can be made to be highly resistant to attacks from dishonest miners.
>>>> * Of separate interest, an exact analysis of the risk of double spend attacks is presented that corrects an error in the original Bitcoin whitepaper.
>>>>
>>>> Overview
>>>> ========
>>>>
>>>> Because the Lightning protocol relies on timelocks to establish the correct channel state, Lightning users could lose their funds if they're unable to put their transactions onchain quickly enough.
>>>> The original Lightning paper [1] states that "[f]orced expiration of many transactions may be the greatest systemic risk when using the Lightning Network" and it uses the term "forced expiration spam" for an attack in which a malicious party "creates many channels and forces them all to expire at once", thus allowing timelocked transactions to become valid.
>>>> That paper also says that the creation of a credible threat against "spamming the blockchain to encourage transactions to timeout" is "imperative" [1].
>>>>
>>>> Channel factories that create multiple Lightning channels with a single onchain transaction [2][3][4][5] increase this risk in two ways.
>>>> First, factories allow more channels to be created, thus increasing the potential for many channels to require onchain transactions at the same time.
>>>> Second, channel factories themselves use timelocks, and thus are vulnerable to a "forced expiration spam" attack.
>>>>
>>>> In fact, the timelocks in Lightning channels and factories are risky even without an attack from a malicious party.
>>>> Blockchain congestion is highly variable and new applications (such as ordinals) can cause a sudden spike in congestion at any time.
>>>> As a result, timelocks that were set when congestion was low can be too short when congestion spikes.
>>>> Even worse, a spike in congestion could be self-reinforcing if it causes malicious parties to attack opportunistically and honest parties to put their channels onchain due to the heightened risk.
>>>>
>>>> One way to reduce the risk of a
>>
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231228/970787cf/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 30
********************************************
