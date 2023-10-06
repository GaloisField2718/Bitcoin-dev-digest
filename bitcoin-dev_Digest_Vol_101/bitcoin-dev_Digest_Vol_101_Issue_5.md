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

   1. Re: Scaling Lightning With Simple Covenants (jlspc)
   2. Re: Draft BIP: OP_TXHASH and OP_CHECKTXHASHVERIFY (Steven Roose)


----------------------------------------------------------------------

Message: 1
Date: Fri, 06 Oct 2023 16:26:33 +0000
From: jlspc <jlspc@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<8rIB8SDRdFLp97JKorrGQ9Rr_v6q9I9-S7mJlWXWineubc_RvfJXhH3nz75DgOpTTwpSo4NEJYpxn2ozEHIVTvajISa03JsVspQWWZWbTzc=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Antoine,

>&gt;<i> "I also think resizing channels can be done fairly effectively off-chain
></i>with hierarchical channels [1] (and even better with hierarchical channels
>within timeout-trees)".

>Yes, transactional scaling of Lightning (i.e how many transfers can be
>performed off-chain per on-chain transaction) sounds good at first sight,
>though in practice liquidity unbalance due to asymmetries in liquidity
>flows among counterparties is a bottleneck. Note, how the on-chain
>splicing for LSP spec upgrade improves on this dimension and where
>"resizing" or "pool rebalancing" aims to keep this off-chain.

Yes, and note that with hierarchical channels you can use HTLCs to send Lightning channel capacity over the Lightning network [1], thus performing channel resizing off-chain between channels that aren't in the same pool.

>&gt;<i> "With these proposals, it's possible to dramatically limit the
></i>interactivity".

>Yes, from my rough understanding of timeout-trees and channel resizing, it
>sounds to suffer from the same issue as Jeremy radix-tree's proposal or
>Christian OG channel factory, namely the lack of fault-tolerance when one
>of the casual user or end of tree balance owner aims to go on-chain. The
>fragmentation cost sounds to be borne by all the users located in the tree
>branch. Note fault-tolerance is one of the key payment pool design goals to
>advance over factories.

Actually, in the case of a timeout-tree, the fragmentation costs imposed by a casual user going on-chain are borne exclusively by the dedicated user who funded the timeout-tree.
This makes it easier to address the problem by making the casual user pay the funder for the fragmentation costs.

I think this is an important issue, so I created a new version of the paper that includes a description of how this can be done [2].
The idea is to require casual users to reveal secrets (hash preimages) that only they know in order to put timeout-tree transactions on-chain.
Then, a fee-penalty output is added to each leaf transaction that pays from the casual user to the funding user an amount that depends on which timeout-tree transactions the casual user put on-chain.
The details are given in the new version of the paper ([2], Section 4.10, pp. 25-28).

>&gt;<i> "I propose that if the active drain fails, the casual user should put
></i>their channel in the old timeout-tree on-chain (so that it won't timeout on
>them). "

>I think there is still some issue there where you need to handle the
>malicious HTLC-withholding case along your multi-hop payment paths and wait
>for the expiration. Then go on-chain to expire the old timeout-tree, which
>might come with a high timevalue cost by default. Not saying keeping
>timevalue cost low is solved for today's Lightning.

This is an excellent point that I hadn't considered.
I think the solution is to perform passive, rather than active, rollovers.
Passive rollovers don't require use of the Lightning network, so they completely eliminate the risk of HTLC-withholding attacks.
I've added this advantage of passive rollovers in the latest version of the paper ([2], Section 4.4, p. 19).

>&gt;<i> "These costs could be large, but hopefully they're rare as they are
></i>failures by dedicated users that can afford to have highly-available
>hardware and who want to maintain a good reputation".

>Yes, though note as soon as a dedicated user starts to have a lot of
>off-chain tree in the hand, and this is observable by adversaries the
>dedicated user becomes an attack target (e.g for channel jamming or
>time-dilation) which substantially alter the trade-offs.

I believe channel jamming and HTLC-withholding attacks can be eliminated by using passive rollovers, as mentioned above.

>&gt;<i> "However, the paper has a proposal for the use of "short-cut"
></i>transactions that may be able to eliminate this logarithmic blow-up".

>Yes "cut-through" to reduce on-chain footprint in mass exit cases has been
>discussed since the early days of off-chain constructions and Taproot /
>Grafroot introduction to the best of my knowledge, see:
><a href="https://tokyo2018.scalingbitcoin.org/transcript/tokyo2018/multi-party-channels-in-the-utxo-model-challenges-and-opportunities">https://tokyo2018.scalingbitcoin.org/transcript/tokyo2018/multi-party-channels-in-the-utxo-model-challenges-and-opportunities</a>

While I see "how do we cut-through to reduce the on-chain footprint in mass exit cases?" listed as an open problem in the above reference, I don't see any specific solutions to that problem in that reference.

The "short-cut" transactions I was referring to are defined in Section 5.4 and pictured in Figure 14 on p. 32 of the revised version of the paper [2].
They are a specific proposal for addressing the logarithmic blow-up of putting a control transaction defined by a covenant tree on-chain.
I agree that this has some similarities to the Graftroot proposal, but I believe it is distinct from proposals for addressing mass exit cases (and in fact it would not work well in those cases).

>Few questions from reading Dave's description of TP protocol here:
><a href="https://bitcoinops.org/en/newsletters/2023/03/29/#preventing-stranded-capital-with-multiparty-channels-and-channel-factories">https://bitcoinops.org/en/newsletters/2023/03/29/#preventing-stranded-capital-with-multiparty-channels-and-channel-factories</a>
>.

>In the scenario of multiple parties (e.g Alice, Bob, Caroll) owning a state
>transaction + control output, what prevents Caroll to double-spend Bob's
>revoked state transaction to a destination controlled by her in collusion
>with Bob, at the harm of Alice ?

Nothing prevents Bob from putting a revoked State transaction on-chain, and nothing prevents Carol from spending the first control output of that revoked State transaction in any manner she wishes.
Doing so would allow Carol to obtain a tunable penalty (namely, the value of the first control output of Bob's revoked State transaction), but it would not harm Alice in any way.
Spending that output keeps Bob from being able to put his Commitment transaction on-chain.
On the other hand, Alice can still put her Commitment transaction on-chain, and her payment from that Commitment transaction is unchanged, so she has not been harmed in any way.

For example, see Figure 18 on p. 29 of [1].
If Bob puts a revoked ST_Bh on-chain (where h < i and i is the current state number) and Carol spends the first control output of ST_Bh, Bob cannot put COM_Bi on-chain, but Alice can still put ST_Ai and COM_Ai on-chain.

>In the scenario of multiple commitment transactions spending the same state
>transaction of an offliner user, what prevents Caroll to fake offliness and
>equivocate at the harm of Alice or another party ?

There is never a case where multiple commitment transactions can spend an output from the same state transaction.
For example, see Figure 18 on p. 29 of [1].
Each user's State transaction can only be spent by the same user's Commitment transaction (e.g., COM_Ai spends an output from ST_Ai, COM_Bi spends an output from ST_Bi, and COM_Ci spends an output fromn ST_Ci).
Furthermore, each Commitment transaction (at the 3-user hierarchical channel level) requires signatures from all 3 users in order to spend the value output from the Funding transaction F, so only the correct Commitment transaction can spend that output.

>Still building my understanding of the TP protocol security model and
>seeing where it converges / diverges w.r.t other off-chain constructions
>trade-offs.

Thanks for doing the deep-dive on these protocols!

Regards,
John

[1] Law, "Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://github.com/JohnLaw2/ln-hierarchical-channels
[2] Law, "Scaling Lightning With Simple Covenants, version 1.2", https://github.com/JohnLaw2/ln-scaling-covenants

Sent with [Proton Mail](https://proton.me/) secure email.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231006/7fda378a/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 6 Oct 2023 18:38:22 +0100
From: Steven Roose <steven@roose.io>
To: Steven Roose via bitcoin-dev
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Draft BIP: OP_TXHASH and
	OP_CHECKTXHASHVERIFY
Message-ID: <211ab58c-707e-97bb-241b-6fe809fd2bdb@roose.io>
Content-Type: text/plain; charset="utf-8"; Format="flowed"

I updated the draft BIP with a proposed reference implementation and a 
link to an implementation of a caching strategy.

It shows that it's possible to achieve TXHASH in a way that after each 
large tx element (scripts, annexes) has been hashed exactly once, 
invocations of TXHASH have clear constant upper limits on the number of 
bytes hashes.

Link to the draft BIP in above e-mail and link to the cache impl here: 
https://github.com/stevenroose/rust-bitcoin/blob/txhash/bitcoin/src/blockdata/script/txhash.rs


On 9/30/23 12:44, Steven Roose via bitcoin-dev wrote:
>
> Hey all
>
>
> The idea of TXHASH has been around for a while, but AFAIK it was never 
> formalized. After conversations with Russell, I worked on a 
> specification and have been gathering some feedback in the last 
> several weeks.
>
> I think the draft is in a state where it's ready for wider feedback 
> and at the same time I'm curious about the sentiment in the community 
> about this idea.
>
> The full BIP text can be found in the attachment as well as at the 
> following link:
> https://github.com/bitcoin/bips/pull/1500
>
> I will summarize here in this writing.
>
> *What does the BIP specify?*
>
>   * The concept of a TxFieldSelector, a serialized data structure for
>     selecting data inside a transaction.
>       o The following global fields are available:
>           + version
>           + locktime
>           + number of inputs
>           + number of outputs
>           + current input index
>           + current input control block
>       o For each input, the following fields are available:
>           + previous outpoint
>           + sequence
>           + scriptSig
>           + scriptPubkey of spending UTXO
>           + value of spending UTXO
>           + taproot annex
>       o For each output, the following fields are available:
>           + scriptPubkey
>           + value
>       o There is support for selecting inputs and outputs as follows:
>           + all in/outputs
>           + a single in/output at the same index as the input being
>             executed
>           + any number of leading in/outputs up to 2^14 - 1 (16,383)
>           + up to 64 individually selected in/outputs (up to 2^16 or
>             65,536)
>       o The empty byte string is supported and functions as a default
>         value which commits to everything except the previous
>         outpoints and the scriptPubkeys of the spending UTXOs.
>
>   * An opcode OP_TXHASH, enabled only in tapscript, that takes a
>     serialized TxFieldSelector from the stack and pushes on the stack
>     a hash committing to all the data selected.
>
>   * An opcode OP_CHECKTXHASHVERIFY, enabled in all script contexts,
>     that expects a single item on the stack, interpreted as a 32-byte
>     hash value concatenated with (at the end) a serialized
>     TxFieldSelector. Execution fails is the hash value in the data
>     push doesn't equal the calculated hash value based on the
>     TxFieldSelector.
>
>   * A consideration for resource usage trying to address concerns
>     around quadratic hashing. A potential caching strategy is outlined
>     so that users can't trigger excessive hashing.
>       o Individual selection is limited to 64 items.
>       o Selecting "all" in/outputs can mostly use the same caches as
>         sighash calculations.
>       o For prefix hashing, intermediate SHA256 contexts can be stored
>         every N items so that at most N-1 items have to be hashed when
>         called repeatedly.
>       o In non-tapscript contexts, at least 32 witness bytes are
>         required and because (given the lack of OP_CAT) subsequent
>         calls can only re-enforce the same TxFieldSelector, no
>         additional limitations are put in place.
>       o In tapscript, because OP_TXHASH doesn't require 32 witness
>         bytes and because of a potential addition of operations like
>         OP_CAT, the validation budget is decreased by 10 for every
>         OP_TXHASH or OP_CHECKTXHASHVERIFY operation.
>
>
> *What does this achieve?*
>
>   * Since the default TxFieldSelector is functionally equivalent to
>     OP_CHECKTEMPLATEVERIFY, with no extra bytes required, this
>     proposal is a strict upgrade of BIP-119.
>
>   * The flexibility of selecting transaction fields and in/output
>     (ranges), makes this construction way more useful
>       o when designing protocols where users want to be able to add
>         fees to their transactions without breaking a transaction chain;
>       o when designing protocols where users construct transactions
>         together, each providing some of their own in- and outputs and
>         wanting to enforce conditions only on these in/outputs.
>
>   * OP_TXHASH, together with OP_CHECKSIGFROMSTACK (and maybe OP_CAT*)
>     could be used as a replacement for almost arbitrarily complex
>     sighash constructions, like SIGHASH_ANYPREVOUT.
>
>   * Apart from being able to enforce specific fields in the
>     transaction to have a pre-specified value, equality can also be
>     enforced, which can f.e. replace the desire for opcodes like
>     OP_IN_OUT_VALUE.*
>
>   * The same TxFieldSelector construction would function equally well
>     with a hypothetical OP_TX opcode that directly pushes the selected
>     fields on the stack to enable direct introspection.
>
>
> *What are still open questions?*
>
>   * Does the proposal sufficiently address concerns around resource
>     usage and quadratic hashing?
>
>   * *: Miraculously, once we came up with all possible fields that we
>     might consider interesting, we filled exactly 16 spots. There is
>     however one thing that I would have liked to be optionally
>     available and I am unsure of which side to take in the proposal.
>     This is including the TxFieldSelector as part of the hash. Doing
>     so no longer makes the hash only represent the value being hashed,
>     but also the field selector that was used; this would no longer
>     make it possible to proof equality of fields. If a txhash as
>     specified here would ever be used as a signature hash, it would
>     definitely have to be included, but this could be done after the
>     fact if OP_CAT was available. For signature hashes, the hash
>     should ideally be somehow tagged, so we might need OP_CAT, or
>     OP_CATSHA256 or something anyway.
>
>       * A solution could be to take an additional bit from each of the
>         two "in/output selector" bytes, and assign to this bit "commit
>         to total number of in/outputs" (instead of having 2 bits for
>         this in the first byte).
>           o This would free up 2 bits in the first byte, one of which
>             could be used for including the TxFieldSelector in the
>             hash and the other one could be left free (OP_SUCCESS) to
>             potentially revisit later-on.
>           o This would limit the number of selectable leading
>             in/outputs to 8,191 and the number of individually
>             selectable in/outputs to 32, both of which seem reasonable
>             or maybe even more desirable from a resource usage
>             perspective.
>
>   * General feedback of how people feel towards a proposal like this,
>     which could either be implemented in a softfork as is, like
>     BIP-119 or be combined in a single softfork with
>     OP_CHECKSIGFROMSTACK and perhaps OP_CAT, OP_TWEAKADD and/or a
>     hypothetical OP_TX.
>
>
> This work is just an attempt to make some of the ideas that have been 
> floating around into a concrete proposal. If there is community 
> interest, I would be willing to spend time to adequately formalize 
> this BIP and to work on an implementation for Bitcoin Core.
>
>
> Looking forward to your thoughts
>
> Steven
>
>
>
>
>
>
>
>
>
>
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231006/23d4dac4/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 5
*******************************************
