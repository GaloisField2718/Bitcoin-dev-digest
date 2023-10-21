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

   1. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Matt Corallo)
   2. OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer by
      Letting Transactions Expire Safely (Peter Todd)
   3. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Peter Todd)
   4. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Olaoluwa Osuntokun)


----------------------------------------------------------------------

Message: 1
Date: Fri, 20 Oct 2023 17:05:48 -0400
From: Matt Corallo <lf-lists@mattcorallo.com>
To: Matt Morehouse <mattmorehouse@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>, Peter Todd
	<pete@petertodd.org>
Cc: security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <1a84a36c-ec23-43b5-9a61-1aafdc188892@mattcorallo.com>
Content-Type: text/plain; charset=UTF-8; format=flowed

Sadly this only is really viable for pre-anchor channels. With anchor channels the attack can be 
performed by either side of the closure, as the HTLCs are now, at max, only signed 
SIGHASH_SINGLE|ANYONECANPAY, allowing you to add more inputs and perform this attack even as the 
broadcaster.

I don't think its really viable to walk that change back to fix this, as it also fixed plenty of 
other issues with channel usability and important edge-cases.

I'll highlight that fixing this issue on the lightning end isn't really the right approach generally 
- we're talking about a case where a lightning counterparty engineered a transaction broadcast 
ordering such that miners are *not* including the optimal set of transactions for fee revenue. Given 
such a scenario exists (and its not unrealistic to think someone might wish to engineer such a 
situation), the fix ultimately needs to lie with Bitcoin Core (or other parts of the mining stack).

Now, fixing this in the Bitcoin Core stack is no trivial deal - the reason for this attack is to 
keep enough history to fix it Bitcoin Core would need unbounded memory. However, its not hard to 
imagine a simple external piece of software which monitors the mempool for transactions which were 
replaced out but which may be able to re-enter the mempool later with other replacements and store 
them on disk. From there, this software could optimize the revenue of block template selection, 
while also accidentally fixing this issue.

Matt

On 10/20/23 2:35 PM, Matt Morehouse via bitcoin-dev wrote:
> I think if we apply this presigned fee multiplier idea to HTLC spends,
> we can prevent replacement cycles from happening.
> 
> We could modify HTLC scripts so that *both* parties can only spend the
> HTLC via presigned second-stage transactions, and we can always sign
> those with SIGHASH_ALL.  This will prevent the attacker from adding
> inputs to their presigned transaction, so (AFAICT) a replacement
> cycling attack becomes impossible.
> 
> The tradeoff is more bookkeeping and less fee granularity when
> claiming HTLCs on chain.
> 
> On Fri, Oct 20, 2023 at 11:04?AM Peter Todd via bitcoin-dev
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
>>
>> On Fri, Oct 20, 2023 at 10:31:03AM +0000, Peter Todd via bitcoin-dev wrote:
>>> As I have suggested before, the correct way to do pre-signed transactions is to
>>> pre-sign enough *different* transactions to cover all reasonable needs for
>>> bumping fees. Even if you just increase the fee by 2x each time, pre-signing 10
>>> different replacement transactions covers a fee range of 1024x. And you
>>> obviously can improve on this by increasing the multiplier towards the end of
>>> the range.
>>
>> To be clear, when I say "increasing the multiplier", I mean, starting with a
>> smaller multiplier at the beginning of the range, and ending with a bigger one.
>>
>> Eg feebumping with fee increases pre-signed for something like:
>>
>>      1.1
>>      1.2
>>      1.4
>>      1.8
>>      2.6
>>      4.2
>>      7.4
>>
>> etc.
>>
>> That would use most of the range for smaller bumps, as a %, with larger % bumps
>> reserved for the end where our strategy is changing to something more
>> "scorched-earth"
>>
>> And of course, applying this idea properly to commitment transactions will mean
>> that the replacements may have HTLCs removed, when their value drops below the
>> fees necessary to get those outputs mined.
>>
>> Note too that we can sign simultaneous variants of transactions that deduct the
>> fees from different party's outputs. Eg Alice can give Bob the ability to
>> broadcast higher and higher fee txs, taking the fees from Bob's output(s), and
>> Bob can give Alice the same ability, taking the fees from Alice's output(s). I
>> haven't thought through how this would work with musig. But you can certainly
>> do that with plain old OP_CheckMultisig.
>>
>> --
>> https://petertodd.org 'peter'[:-1]@petertodd.org
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Sat, 21 Oct 2023 00:09:16 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior: Making
	HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZTMWrJ6DjxtslJBn@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Mon, Oct 16, 2023 at 05:57:36PM +0100, Antoine Riard via bitcoin-dev wrote:
> Here enter a replacement cycling attack. A malicious channel counterparty
> can broadcast its HTLC-preimage transaction with a higher absolute fee and
> higher feerate than the honest HTLC-timeout of the victim lightning node
> and triggers a replacement. Both for legacy and anchor output channels, a
> HTLC-preimage on a counterparty commitment transaction is malleable, i.e
> additional inputs or outputs can be added. The HTLC-preimage spends an
> unconfirmed and unrelated to the channel parent transaction M and conflicts
> its child.

The basic problem here is after the HTLC-timeout path becomes spendable, the
HTLC-preimage path remains spendable. That's bad, because in this case we want
spending the HTLC-preimage - if possible - to have an urgency attached to it to
ensure that it happens before the previous HTLC-timeout is mined.

So, why can't we make the HTLC-preimage path expire? Traditionally, we've tried
to ensure that transactions - once valid - remain valid forever. We do this
because we don't want transactions to become impossible to mine in the event of
a large reorganization.

A notable example of this design philosophy is seen in Bitcoin's rules around
coinbase outputs: they only become spendable after 100 more blocks have been
found; a 100 block reorg is quite unlikely.

Enter the OP_Expire and the Coinbase Bit soft-fork upgrade.


# Coinbase Bit

By redefining a bit of the nVersion field, eg the most significant bit, we can
apply coinbase-like txout handling to arbitrary transactions. Such a
transaction's outputs would be treated similarly to a coinbase transaction, and
would be spendable only after 100 more blocks had been mined. Due to this
requirement, these transactions will pose no greater risk to reorg safety than
the existing hazard of coinbase transactions themselves becoming invalid.

Note how such a transaction is non-standard right now, ensuring compatibility
with existing nodes in a soft-fork upgrade.


# OP_Expire

Redefining an existing OP_Nop opcode, OP_Expire would terminate script
evaluation with an error if:

1) the Coinbase Bit was not set; or
2) the stack is empty; or
3) the top item on the stack was >= the block height of the containing block

This is conceptually an AntiCheckLockTimeVerify: where CLTV _allows_ a txout to
become spendable in a particular way in the future, Expire _prevents_ a txout
from being spent in a particular way.

Since OP_Expire requires the Coinbase Bit to be set, the reorg security of
OP_Expire-using transactions is no worse than transactions spending miner
coinbases.


# How HTLC's Would Use OP_Expire

Whenever revealing the preimage on-chain is necessary to the secure functioning
of the HTLC-using protocol, we simply add an appropriate OP_Expire to the
pre-image branch of the script along the lines of:

    If
        <expiry height> Expire Drop
        Hash <digest> EqualVerify
        <pubkey> CheckSig
    ElseIf
        # HTLC Expiration conditions
        ...
    EndIf

Now the party receiving the pre-image has a deadline. Either they get a
transaction spending the preimage mined, notifying the other party via the
blockchain itself, or they fail to get the preimage mined in time, reverting
control to the other party who can spend the HTLC output at their leisure,
without strict time constraints.

Since the HTLC-expired branch does *not* execute OP_Expire, the transaction
spending the HTLC-expired branch does *not* need to set the Coinbase Bit. Thus
it can be spent in a perfectly normal transaction, without restrictions.


# Delta Encoding Expiration

Rather than having a specific Coinbase Bit, it may also be feasible to encode
the expiration height as a delta against a block-height nLockTime. In this
variant, OP_Expire would work similarly to OP_CheckLockTimeVerify, by checking
that the absolute expiration height was <= the requested expiration, allowing
multiple HTLC preimage outputs to be spent in one transaction.

If the top 16-bits were used, the maximum period a transaction could be valid
would be:

    2^16 blocks / 144 blocks/day = 455 days

In this variant, a non-zero expiration delta would enable expiration behavior,
as well as the coinbase-like output spending restriction. The remaining 16-bits
of nVersion would remain available for other meanings.

Similar to how CLTV and CSV verified nLockTime and nSequence respectively,
verifying an expiration height encoded in the nVersion has the advantage of
making an expiration height easy to detect without validating scripts.

While Lightning's HTLC-success transactions currently use nLockTime=0, AFAIK
there is no reason why they could not set nLockTime to be valid in the next
block, allowing delta encoding to be used.


## Reusing Time-Based nLockTime

Reusing time-based nLockTime's prior to some pre-2009 genesis point for
expiration is another possibility (similar to how Lightning makes use of
time-based nLockTime for signalling). However I believe this is not as
desirable as delta encoding or a coinbase bit, as it would prevent transactions
from using block nLockTime and expiration at the same time. It would also still
require a coinbase bit or nVersion increase to ensure expiration-using
transactions are non-standard.


# Mempool Behavior

Obviously, mempool logic will need to handle transactions that can expire
differently than non-expiring transactions. One notable consideration is that
nodes should require higher minimum relay fees for transactions close to their
expiration height to ensure we don't waste bandwidth on transactions that have
no potential to be mined. Considering the primary use-case, it is probably
acceptable to always require a fee rate high enough to be mined in the next
block.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/6ef2425f/attachment-0001.sig>

------------------------------

Message: 3
Date: Sat, 21 Oct 2023 00:15:21 +0000
From: Peter Todd <pete@petertodd.org>
To: Matt Corallo <lf-lists@mattcorallo.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <ZTMYGcRvHh0Iwe2y@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 05:05:48PM -0400, Matt Corallo wrote:
> Sadly this only is really viable for pre-anchor channels. With anchor
> channels the attack can be performed by either side of the closure, as the
> HTLCs are now, at max, only signed SIGHASH_SINGLE|ANYONECANPAY, allowing you
> to add more inputs and perform this attack even as the broadcaster.
> 
> I don't think its really viable to walk that change back to fix this, as it
> also fixed plenty of other issues with channel usability and important
> edge-cases.

What are anchor outputs used for other than increasing fees?

Because if we've pre-signed the full fee range, there is simply no need for
anchor outputs. Under any circumstance we can broadcast a transaction with a
sufficiently high fee to get mined.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/371342e7/attachment-0001.sig>

------------------------------

Message: 4
Date: Fri, 20 Oct 2023 17:18:58 -0700
From: Olaoluwa Osuntokun <laolu32@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID:
	<CAO3Pvs9jUr8cw0Dz35oHLREzSeMCbGyFkUDt0w8EFoW1RVZHzw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> Let's say you have Alice, Bob and Caroll all "honest" routing hops
> targeted by an attacker. They all have 3 independent 10 000 sats HTLC
> in-flight on their outbound channels.

> It is replaced by Mallory at T+2 with a HTLC-preimage X of 200 000 sats (+
> rbf penalty 1 sat / vb rule 4). Alice's HTLC-timeout is out of network
> mempools.

> Bob broadcasts her HTLC-timeout of 200 000 sats at T+3. It is replaced by
> Mallory at T+4 with her HLTC-preimage Y of 200 000 sats (+ rbf penalty 1
> sat / vb rule 4 * 2). Bob's HTLC-timeout is out of network mempools.

IIRC correctly, in your scenario, you're dealing with Carol -> Bob -> Alice.
Mallory can only replace an HTLC-timeout transaction if she's directly
connected with the peer she's targeting via a direct channel. She cannot
unilaterally replace any transaction in the mempool solely with knowledge of
the preimage. All HTLC transactions are two party contracts, with the public
keys of both participants hard coded into the contract. A third party cannot
unilaterally sweep an HTLC given only a preimage.

I think it's worth taking a minute to step back here so we can establish
some fundamental context. Once the timelock of an HTLC expires, and the
receiver has direct knowledge of the preimage, a bidding war begins.  If the
receiver is able to confirm their success transaction in time, then they
gain the funds, and the sender is able to pipeline the preimage backwards in
the route, making all parties whole. If the sender is the one that wins out,
then it's as if nothing happened, sans the fees paid at the last mile, all
other hops are able to safely cancel their HTLC back on the chain.

As mentioned elsewhere in the thread, most implementations today will watch
the mempool for preimages, so they can resolve the incoming HTLC as quickly
as possible off chain. The attack described critically relies on the ability
of an attacker to pull off very precise transaction replacement globally
across "the mempool". If any of the honest parties see the preimage, in the
mempool, then the attack ends as they can settle back off chain, and if
their timeout is able to confirm first, then the defender has actually
gained funds.

In addition, such an attack needs to be executed perfectly, for hours if not
days. Within the LN, all nodes set a security parameter, the CLTV delta,
that dictates how much time they have before the outgoing and incoming HTLCs
expire. Increasing this value makes the attack more difficult, as they must
maintain the superposition of: fees low enough to not get mined, but high
enough to replace the defender's transaction, but not _too_ high, as then
it'll be mined and everything is over. With each iteration, the attacker is
also forced to increase the amount of fees they pay, increasing the likely
hood that the transaction will be mined. If mined, the attack is moot.

As mentioned in the OP, one thing the attacker can do is try and locate the
defender's node to launch the replacement attack directly in their mempool.
However, by replacing directly in the mempool of the defender, the defender
will learn of the preimage! They can use that to just settle everything
back, thereby completing the payment, and stopping the attack short. Even
ignoring direct access to the defender's mempool, the attacker needs to
somehow iteratively execute the replacement across a real network, with all
the network jitter, propagation delay, and geographic heterogeneity that
entails. If they're off by milliseconds, then either a confirmation occurs,
or the preimage is revealed in the mempool. A canned local regtest env is
one thing, the distributed system that is the Internet is another.

Returning back to the bidding war: for anchor channels, the second level
HTLCs allow the defender to attach arbitrary inputs for fee bumping
purposes. Using this, they can iteratively increase their fee (via RBF) as
the expiry deadline approaches. With each step, they further increase the
cost for the attacker. On top of that, this attack cannot be launched
indiscriminately across the network. Instead, it requires per-node set up by
the attacker, as they need to consume UTXOs to create a chain of
transactions they'll use to launch the replacement attack. These also need
to be maintained in a similar state of non-confirming superposition.

That's all to say that imo, this is a rather fragile attack, which requires:
per-node setup, extremely precise timing and execution, non-confirming
superposition of all transactions, and instant propagation across the entire
network of the replacement transaction (somehow also being obscured from the
PoV of the defender). The attack can be launched directly with a miner, or
"into" their mempool, but that weakens the attack as if the miner broadcasts
any of the preimage replacement transactions, then the defender can once
again use that to extract the preimage and settle the incoming HTLC.

-- Laolu
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231020/44ff6813/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 30
********************************************
