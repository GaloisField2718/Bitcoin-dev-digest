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

   1. One-Shot Replace-By-Fee-Rate (Peter Todd)
   2. Re: BIP process friction (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Thu, 18 Jan 2024 18:23:39 +0000
From: Peter Todd <pete@petertodd.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <Zalsq+Nq7RRr/CAR@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

Reposting this blog post here for discussion:

https://petertodd.org/2024/one-shot-replace-by-fee-rate

---
layout: post
title:  "One-Shot Replace-by-Fee-Rate"
date:   2024-01-18
tags:
- bitcoin
- rbf
- pinning
---

Currently Bitcoin Core implements a Replace-by-Fee (RBF) policy, where
transactions are not replaced unless the new transaction pays at least a higher
total fee than the replaced transaction, regardless of fee-rate.

When RBF was first implemented over 8 years ago this was a reasonable,
conservative, default. However, since then we've found that strictly requiring
a higher absolute fee creates the potential for [transaction
pinning](https://bitcoinops.org/en/topics/transaction-pinning/) attacks in
contracting protocols such as Lightning; replacing transactions based on
*fee-rate* would make it possible[^bip125-rule-5-pinning] to eliminate these
attacks by eliminating BIP-125 Rule #3 pinning.

[^bip125-rule-5-pinning]: The other notable pinning attack against RBF is to cause BIP-125 Rule #5 to be exceeded. But that is easily solved by just rejecting transactions that would make transactions already in the mempool to be irreplaceable.

Here we will propose an incentive compatible solution, One-Shot
Replace-By-Fee-Rate, that mitigates prior concerns over replace-by-fee-rate
policies by allowing the replacement to only happen when it would immediately
bring a transaction close enough to the top of the mempool to be mined in the
next block or so. Finally, we will show that both one-shot and pure
replace-by-fee-rate policies sufficiently resist bandwidth exhaustion attacks
to be implementable.

*Thanks goes to [Fulgur Ventures](https://fulgur.ventures/) for sponsoring this
research. They had no editorial control over the contents of this post and did
not review it prior to publication.*


<div markdown="1" class="post-toc">
# Contents
{:.no_toc}
0. TOC
{:toc}
</div>

## Background

### The Expected Return of an Unconfirmed Transaction

Suppose there exists a transaction that pays a fee of $$F$$ at a fee-rate $$r$$.
What is the expected return $$E$$ of that transaction to miners as a whole? If
the transaction pays a fee-rate high enough to definitely get mined in the next
block, the answer seems obvious: $$E = F$$. The transaction will be mined, and
miners as a whole will earn the entire $$F$$ fee.

But what if that transaction pays a lower fee-rate? For example, as I write
this, [mempool.space](https://mempool.space) reports that their mempool
contains $$535\mathrm{MvB}$$ of transactions, enough that a typical Bitcoin
Core node with its typical $$300\mathrm{MB}$$ mempool size limit would reject
transactions paying less than $$22.9\frac{\mathrm{sat}}{\mathrm{vB}}$$.

If a transaction has a fee-rate of $$23\frac{\mathrm{sat}}{\mathrm{vB}}$$, just
barely enough to get into a default mempool, what is that transaction worth to
miners? How do we even answer this question?

Intuitively it seems obvious that the low fee-rate transaction should be worth less than the high fee-rate transaction, because
the low fee-rate transaction probably won't be mined for days, or even weeks, if ever.
Certainly, in a shorter time frame, a transaction at the bottom of the mempool
does not directly represent income to the miner.

We can think about this a bit more rigorously by observing that because block
finding is a Poisson Process, **even if** we ignore the supply of new
transactions, the probability that a transaction $$n$$ blocks deep is mined in
a time interval $$t$$ is the probability that $$N \ge n$$ blocks are found in
the time interval $$t$$. That probability rapidly diminishes as $$n$$
increases, because it's less and less likely for so many blocks to be found in
a short period of time.


### Unconfirmed Transactions are Honest Signals

Do low fee-rate transactions have a value? Yes!

Assuming your node is well connected, unconfirmed transactions in your mempool
are *honest signals*: because unconfirmed transactions *could* be mined,
they're clear evidence that if you wish your transaction to be mined sooner, you
need to offer an even higher fee-rate. There's a constant supply of people with
high time preference who want their transactions mined in a short period of
time. So low fee-rate transactions indirectly increase the revenue of miners in
the short term, because they force higher time preference transactors to outbid
them.

Note how I said a higher fee-rate, not fee: because it maximizes revenue to mine
transactions in fee-rate order, fee-rate is what matters in terms of priority.


### Expected Return vs Fee-Rate

Suppose we now have *two* different conflicting transactions, $$a$$ and $$b$$.
Suppose that the total size of $$a$$ is $$100000\mathrm{vB}$$, and pays
$$23\frac{\mathrm{sat}}{\mathrm{vB}}$$, for a total fee of
$$2300000\mathrm{sat}$$. Meanwhile $$b$$ has a size of just $$150\mathrm{vB}$$,
and pays $$15000\frac{\mathrm{sat}}{\mathrm{vB}}$$, for a total fee of
$$2250000\mathrm{sat}$$.

It seems intuitive that transaction $$b$$ is the one the miner should accept to
maximize revenue. It pays a *far* higher fee-rate, almost certainly high enough
to be mined in the next block. $$a$$ might never get mined, in part because
another miner might mine $$b$$ first[^mempool-consensus]. Yet currently, Bitcoin Core will reject
$$b$$, because BIP-125 Rule #3 requires a transaction to pay a higher *total* fees
than the replacement!

[^mempool-consensus]: There is no such thing as *the* mempool: every miner (and node) has their own mempool, and there's no mechanism to synchronize mempools beyond the best-effort broadcasting of transactions. The need for consensus is why we have the blockchain in the first place.

Conversely if transaction $$b$$ was broadcast first, transaction $$a$$ would
not be accepted even though it pays a higher total fee: Bitcoin Core does not
allow a transaction to be replaced unless the replacement pays a higher
fee-rate.


## One-Shot Replace-by-Fee-Rate

We can mitigate Rule #3 transaction pinning in a miner-incentive compatible way
by replacing transactions (or alternatively, transaction packages) that do
*not* qualify for replacement based on the existing rules, if they qualify under
these alternative rules:

1. The new transaction (package) has a fee-rate more than $$r$$ times higher
   than the fee-rate of the transactions it replaces.
2. The new transaction (package) has a sufficiently high fee-rate to place it
   into the upper $$N$$ blocks worth of the mempool.
3. The *highest mineable replaced fee-rate* is *not* high enough to place the
   replaced transactions in the upper $$N$$ blocks of the mempool. Highest mineable
   replaced fee-rate in this context refers to the fee-rate a miner can obtain by
   mining one or more of the replaced transactions, taking unconfirmed parents[^unconfirmed-parents]
   into account.

[^unconfirmed-parents]: For example, if transation $$a$$ is spent by $$b$$, and the fee-rate $$r_a \ge r_b$$, then the fee-rate of $$a$$ is the highest mineable replaced fee-rate. On the other hand, if $$r_a < r_b$$, then the highest minable replaced fee-rate is computed as the CPFP package of $$a$$ and $$b$$. We refer to this as a *mineable* fee-rate because while the fee-rate of $$b$$ may be higher, a miner can't obtain that fee-rate directly: $$a$$ must also be mined.

Setting $$r = 1.25$$ and $$N = 1$$ would be reasonable.

Provided that a small $$N$$ is chosen, this alternative Replace-by-Fee-Rate
mechanism solves BIP-125 Rule #3 transaction pinning for contracting protocols
such as Lightning because:

1. If the one-shot RBFr replacement conditions *are* met, the higher fee-rate
   intended transaction replaces the pin, and will be mined in the near future.
2. If the replacement conditions are *not* met, the pin must already have a
   sufficiently high fee-rate to be mined "soon", allowing the protocol to make
   forward progress anyway.

This works because contracting protocols are not secure if they absolutely
depend on the highest fee/fee-rate transaction being mined. Mempools don't have
consensus, so it's impossible to guarantee that a particular transaction gets
mined when more than one transaction is possible. But, contracting protocols do
require forward progress to be made, defined as transactions getting mined. So
as long as we can ensure that a transaction is mined, the protocol can make
progress.

For miners, these one-shot RBFr rules are reasonably incentive compatible
because:

1. In the typical case where fees are reasonably steady, there is a constant
   supply of new transactions created by people who want those transactions to be
   mined in the near future.
2. The old transaction did *not* have a high enough fee-rate to be mined soon.
   Thus the value to the miner of that transaction was not the fees themselves.
   But rather, the *fee-rate*, which new, high time preference, bidders have to outbid.
3. The new transaction *does* have a high enough fee-rate to be mined soon.
   Which means other high time preference transactors will have to outbid it, or
   alternatively, the transactions it pushed further down the mempool.
4. Contracting protocols, in particular Lightning-like protocols, are
   profitable to miners because they allow many layer 2 transactions to pay for
   the transaction fees of a single layer 1 transaction. Adopting rules that
   allow these protocols to work better will, in the long run, increase miner revenue.
5. It is sufficient for only a subset of miners to run replace-by-fee-rate
   policies, as well-designed contracting protocols only need to make forward
   progress eventually, prior to deadlines being reached.

Remember that we are *not* claiming that one-shot RBFr is always perfectly
incentive compatible; no one set of rules could ever be perfectly incentive
compatible in all possible scenarios. We are simply claiming that on average,
in the situations where these rules are active, miners make more money.

Finally node runners should adopt these rules because:

1. If we assume node runners are donating their bandwidth to be used for the
   good of Bitcoin users and miners, all the above arguments apply.
2. These rules are usually a strict increase in the number of transactions that nodes
   propagate to miners; replace-by-fee-rate policies propagate
   transactions that otherwise would not have been propagated.


## Denial of Service Attacks

### The Status Quo

The amount of bandwidth transactors can consume by broadcasting Bitcoin
transactions must be limited. But even without transaction replacement, the
exact way these limits work is non-obvious.

You might think that the minimum relay fee implements a direct *cost* that must
be paid to use up bandwidth, if you assume that any transaction will eventually
be mined. But in fact this is **not** true! There are a variety of ways that a
previously broadcast transaction might become impossible to mine due to a
double spend of one of the inputs, by a transaction that did not pay the full
cost of the minimum relay fee for that transaction.

For example, an attacker could broadcast a large, $$400{\small,}000\mathrm{byte}$$, low fee-rate
transaction that violates [Ocean](https://ocean.xyz/) mining pool's
restrictions on data carrying transactions. Almost all relay nodes will relay
this transaction, using up relay bandwidth. But at some point in the future,
the attacker can give Ocean a much smaller transaction spending one of that
large, low fee-rate, transaction's inputs. It will eventually be mined, creating a conflict
that invalidates the large transaction, at a much lower cost than the
total fees the large transaction was supposed to pay.

Similarly, an attacker could broadcast a large, low fee-rate, transaction while
simultaneously sending a small double-spend directly to a mining pool. With
good timing, the super-majority of nodes will waste bandwidth broadcasting the
large transaction, which is eventually removed from mempools when the small
transaction is mined at low cost.


How much is such an attacker paying? Interestingly, the worst case is made a bit worse
worse if the [ephemeral anchors](https://github.com/instagibbs/bips/blob/7d79c5692bb745bf158f2d8f8e4979d80ad07e58/bip-ephemeralanchors.mediawiki)
proposal is implemented. So for the purpose of conservatively analyzing a worst
case situation, we will assume the attacker makes use of the most efficient
possible version of ephemeral anchors, a bare `scriptPubKey` spent by an
`OP_True`. If ephemeral anchors is *not* implemented, all of the steps below
can be done nearly as efficiently via P2SH outputs with the spending script
`OP_True`.

0. Attacker creates $$N$$ ephemeral anchor outputs.[^creating-ephemeral-anchors]
1. Attacker broadcasts $$N$$, $$404{\small,}000\mathrm{byte}$$ transaction packages[^transaction-package-limit] with fee-rate
   low enough to not be mined any time soon, in such a way that the transactions
   is *not* accepted by some hash power. Each transaction spends an ephemeral
   anchor output.
2. Attacker spends those $$N$$ ephemeral anchor outputs in a transaction paying
   market fee-rates rates.

[^transaction-package-limit]: The relevant limit here is *not* the total size of a single transaction, because more than one transaction can be replaced at a time. Rather it's the default descendant size limit, which is slightly higher than the maximum transaction size. Note that in reality our $$404{\small,}000\mathrm{byte}$$ figure is a slight overestimate as the descendant size limit has units of virtual bytes rather than bytes.

[^creating-ephemeral-anchors]: This may require the cooperation of a mining pool willing to mine non-standard transactions.

Spending each ephemeral output requires an additional $$41\mathrm{vB}$$ per
output spent, and creating an ephemeral output, an additional $$9\mathrm{vB}$$.
Thus the attacker has broadcast $$404{\small,}000\mathrm{bytes}$$ while
paying for just $$50\mathrm{vB}$$, a $$\frac{1}{8080}$$ cost
reduction[^cost-reduction] over the intended minimum relay fee.

[^cost-reduction]: Assuming that the fee-rate paid by the spending and creation of the outputs was the same. This might not be the case as the attacker could setup the outputs to be spent in advance.

Remember, we are *not* analyzing replace-by-fee-rate here! We're just looking
at what is *already possible* with Bitcoin Core. Or at least, almost already
possible, as `OP_True` P2SH outputs cost only a bit more.

So why isn't this attack happening? Let's work out how much it costs, using the
current Bitcoin price and current lower-bound mining fees:

$$\frac{50\mathrm{vB}}{404{\small,}000\mathrm{B}} \times \frac{30\mathrm{sat}}{\mathrm{vB}} \times \frac{40{\small,}000 \mathrm{USD}}{100{\small,}000{\small,}000\mathrm{sats}} \approx \frac{1485 \mathrm{USD}}{\mathrm{GB}}$$

Even Digital Ocean charges just
$$0.01\frac{\mathrm{USD}}{\mathrm{GB}}$$[^digital-ocean-bandwidth-cost]. So if
you wanted to DoS attack all ~20,000 publicly reachable nodes, you'd be
spending only $$200\frac{\mathrm{USD}}{\mathrm{GB}}$$. This isn't an entirely
fair comparison, as relaying transactions also uses up bandwidth on non-public
nodes. But it is an indication that there are probably cheaper and more
effective ways to attack Bitcoin.

[^digital-ocean-bandwidth-cost]: [Bandwidth Billing](https://docs.digitalocean.com/products/billing/bandwidth/), accessed Jan 15th 2024. Specifically the *excess* bandwidth charge, ignoring the bandwidth included per month. There are many other hosting providers offering even cheaper bandwidth.


#### Conflicting Versions

Attackers can further multiply the bandwidth usage of their attack by
simultaneously broadcasting multiple conflicting versions of the large
transaction to different nodes, where each conflict pays the same fee/fee-rate.
At the points in the node network graph where the conflicts "meet", nodes will
end up downloading multiple versions from their peers, again increasing
bandwidth usage by the number of conflicts each node sees.

Analyzing this case is more difficult, as the impact depends on network
topology, and the attacker has to use more of their own bandwidth broadcasting
the conflicting transactions. But in a perfectly executed attack, a node might
receive one conflicting version per peer; public nodes have, by default, up to
125 connections, and non-public nodes have, by default, 8 outgoing transaction
relaying peers.

Even in the 125x public node case it would probably be cheaper to try to DoS
attack all publicly accessible nodes via an unsophisticated packet flood.


#### Re-using Third Party Outputs

An attacker can make use of others' transactions rather than creating their own
transaction outputs to reduce cost. This of course *is* a transaction pinning
attack! Doing this is possible against unsigned anchor outputs, as well as
transactions signed with `SIGHASH_ANYONECANPAY`. However for the purpose of
using up relay bandwidth this attack strategy is inherently limited by two
factors:

1. There usually aren't that many suitable victim transactions being broadcast, limiting the total bandwidth that can be consumed.
2. The attacker has to intercept the victim transactions prior to them being widely broadcast, and somehow get their "bloated" versions of those transactions widely broadcast first.


#### Fill and Dump Attack

In addition to using up bandwidth an attacker could also use transaction
invalidation to fill, and then empty, mempools at less cost than the full fees
required to broadcast the "fill" transactions. In fact, any attack that tries
to use up a significant amount of relay bandwidth by mining conflicting
transactions will have this effect by default, as conflicts can only invalidate
transactions when blocks are mined.

Filling mempools requires access to large amounts of capital. Bitcoin Core
implements the mempool size limit in terms of *RAM* usage, not serialized
bytes, so exactly what the default $$300\mathrm{MB}$$ limit means depends on
CPU architecture. But for sake of argument, let's say that the limit works out
to approximately $$75\mathrm{MvB}$$ worth of transactions, and the attacker is
"filling" $$70\mathrm{MvB}$$ worth, to avoid getting their transactions
actually mined. Even at $$10\frac{\mathrm{sat}}{\mathrm{vB}}$$ the attacker
needs:

$$70\mathrm{MvB} \times \frac{10\mathrm{sat}}{\mathrm{vB}} \times \frac{40{\small,}000 \mathrm{USD}}{100{\small,}000{\small,}000\mathrm{sats}} = 280{\small,}000 \mathrm{USD}$$

An obvious question is, what exactly does this attack accomplish? Transactions
that are outbid can simply be rebroadcast by anyone once mempools have space
again; while the transactions are in mempools the attacker is legitimately outbidding those
transactions, and they could hypothetically be mined. Arguably the transactions
are driving up fees overall. But unless the attacker wants to bid high enough
that their "fill" transactions actually get mined, the attacker isn't having
any direct impact on the higher fee part of mempools that is actually getting
mined.


### Is One Shot Replace-By-Fee-Rate Similar To The Status Quo?

Yes.

As we have shown above, an attacker can already broadcast large transactions
that are invalidated by smaller transactions that pay less total fees. With
one-shot replace-by-fee-rate the attack becomes a little less challenging to
pull off, as it can be done generically, rather than with a target mining pool.
But either way, the real limiting factor to the attack is that it is *still* a
very expensive way to use up bandwidth.

With regard to the fill-and-dump attack, again the attacker is able to do
fill-and-dump cycles more frequently than once per block with one-shot
replace-by-fee-rate. But again, we have to ask what does the attacker get out
of this other than bandwidth consumption, and possibly confusing some badly
written fee estimation code?


### Pure Replace-By-Fee-Rate

What if we don't have the one-shot condition? Is a pure replace-by-fee-rate
policy viable from a DoS attack perspective? This is an important question
because:

1. An initial prototype is easier to implement without the one-shot feature, and compatible with nodes/miners who choose to do something more sophisticated.
2. Pure replace-by-fee-rate is simpler for users to understand.
3. In a rising fee-rate environment, the one-shot policy may degrade to pure replace-by-fee-rate.

Provided that the minimum fee-rate ratio, $$r$$ is sufficiently high the total
number of plausible replacements is limited. For example, even starting at just
$$1\frac{\mathrm{sat}}{\mathrm{vB}}$$, $$r = 1.25$$ results in:

$$1\frac{\mathrm{sat}}{\mathrm{vB}} \times 1.25^{30} \approx 808\frac{\mathrm{sat}}{\mathrm{vB}}$$

That's sufficient to get into the next block at any point in time in Bitcoin's
history, for a mere 30x theoretical increase in bandwidth, by an attacker who
is going to have to tie up thousands of dollars worth of BTC just to broadcast
a few megabytes worth of transactions. And that example is unrealistic, as
minimum relay fees were never actually that low during Bitcoin's high fee
events.

It's probably worth trying out pure replace-by-fee-rate in a Bitcoin Core fork,
especially if $$r$$ is set to a more conservative value, e.g. $$r=2$$.


## Impact on Coinjoins

Replace-by-fee-rate does introduce a new way to double-spend low fee-rate
coinjoin transactions at lower cost than outbidding the entire fee paid by the
coinjoin. This is most relevant to Wasabi, which typically creates coinjoin
transactions with hundreds of inputs and outputs; other coinjoin
implementations create much smaller transactions.

However, double-spending is not a new attack. There are already other cheap
ways to cause coin-join rounds to fail, including other types of double-spend
attacks, and cheapest of all, simply failing to complete the coinjoin protocol
by failing to provide a signature where required. Wasabi deals with this by
imposing a cost on the attacker, by blacklisting UTXO's that fail to complete a
coinjoin round for a period of time; the majority of Wasabi coinjoin rounds
fail due to one of the parties failing to sign in time.

Simply failing to sign is generally a cheaper attack than double-spending, as
any type of double-spend requires fees to be paid per round disrupted. Thus
replace-by-fee-rate is unlikely to pose a significant threat to coinjoin
protocols.


## Footnotes
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240118/3dd8f8c4/attachment-0001.sig>

------------------------------

Message: 2
Date: Fri, 19 Jan 2024 10:46:10 +1000
From: Anthony Towns <aj@erisian.com.au>
To: "David A. Harding" <dave@dtrt.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID: <ZanGUhKRJY2pgZuf@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Thu, Jan 18, 2024 at 05:41:14AM -1000, David A. Harding via bitcoin-dev wrote:
> Question: is there a recommended way to produce a shorter identifier for
> inline use in reading material?  For example, for proposal
> BIN-2024-0001-000, I'm thinking:
> 
> - BIN24-1 (references whatever the current version of the proposal is)
> - BIN24-1.0 (references revision 0)
> 
> I think that doesn't look too bad even if there are over 100 proposals a
> year, with some of them getting into over a hundred revisions:
> 
> - BIN24-123
> - BIN24-123.123

Having lived through y2k, two-digit years give me the ick, but otherwise
sure.

Cheers,
aj, that's how the kids who didn't live through y2k say it, right?


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 22
********************************************
