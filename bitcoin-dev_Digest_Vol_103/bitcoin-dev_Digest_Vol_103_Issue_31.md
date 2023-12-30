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

   1. Re: Ordinal Inscription Size Limits (Greg Tonoski)
   2. Re: Scaling Lightning Safely With Feerate-Dependent Timelocks
      (David A. Harding)
   3. Re: Scaling Lightning Safely With Feerate-Dependent Timelocks
      (David A. Harding)
   4. Re: Scaling Lightning Safely With Feerate-Dependent Timelocks
      (David A. Harding)
   5. Re: Swift Activation - CTV (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Fri, 29 Dec 2023 13:27:42 +0100
From: Greg Tonoski <gregtonoski@gmail.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID: <980df778-cc94-4f98-8eb1-cbb321883369@gmail.com>
Content-Type: text/plain; charset=UTF-8; format=flowed

> Unfortunately, as near as I can tell there is no sensible way to
> prevent people from storing arbitrary data in witnesses ...

To prevent "from storing arbitrary data in witnesses" is the extreme
case of the size limit discussed in this thread. Let's consider it along
with other (less radical) options in order not to lose perspective, perhaps.

> ...without incentivizing even worse behavior and/or breaking
> legitimate use cases.

I can't find evidence that would support the hypothesis. There had not
been "even worse behavior and/or breaking legitimate use cases" observed
before witnesses inception. The measure would probably restore
incentives structure from the past.

As a matter of fact, it is the current incentive structure that poses
the problem - incentivizes worse behavior ("this sort of data is toxic
to the network") and breaks legitimate use cases like a simple transfer
of BTC.

> If we ban "useless data" then it would be easy for would-be data
> storers to instead embed their data inside "useful" data such as dummy
> signatures or public keys.

There is significant difference when storing data as dummy signatures
(or OP_RETURN) which is much more expensive than (discounted) witness.
Witness would not have been chosen as the storage of arbitrary data if
it cost as much as alternatives, e.g. OP_RETURN.

Also, banning "useless data" seems to be not the only option suggested
by the author who asked about imposing "a size limit similar to OP_RETURN".

> But from a technical point of view, I don't see any principled way to
> stop this.

Let's discuss ways that bring improvement rather than inexistence of a
perfect technical solution that would have stopped "toxic data"/"crap on
the chain". There are at least a few:
- https://github.com/bitcoin/bitcoin/pull/28408
- https://github.com/bitcoin/bitcoin/issues/29146
- deprecate OP_IF opcode.

I feel like the elephant in the room has been brought up. Do you want to
maintain Bitcoin without spam or a can't-stop-crap alternative, everybody?


------------------------------

Message: 2
Date: Fri, 29 Dec 2023 08:11:43 -1000
From: "David A. Harding" <dave@dtrt.org>
To: jlspc <jlspc@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: lightning-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent Timelocks
Message-ID: <62edca3a0c61b7dca5f7dcddf8e33f6a@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-12-28 08:06, jlspc via bitcoin-dev wrote:
> On Friday, December 22nd, 2023 at 8:36 AM, Nagaev Boris
> <bnagaev@gmail.com> wrote:
>> To validate a transaction with FDT [...]
>> a light client would have to determine the median fee
>> rate of the recent blocks. To do that without involving trust, it has
>> to download the blocks. What do you think about including median
>> feerate as a required OP_RETURN output in coinbase transaction?
> 
> Yes, I think that's a great idea!

I think this points to a small challenge of implementing this soft fork 
for pruned full nodes.  Let's say a fee-dependent timelock (FDT) soft 
fork goes into effect at time/block _t_.  Both before and for a while 
after _t_, Alice is running an older pruned full node that did not 
contain any FDT-aware code, so it prunes blocks after _t_ without 
storing any median feerate information about them (not even commitments 
in the coinbase transaction).  Later, well after _t_, Alice upgrades her 
node to one that is aware of FDTs.  Unfortunately, as a pruned node, it 
doesn't have earlier blocks, so it can't validate FDTs without 
downloading those earlier blocks.

I think the simplest solution would be for a recently-upgrade node to 
begin collecting median feerates for new blocks going forward and to 
only enforce FDTs for which it has the data.  That would mean anyone 
depending on FDTs should be a little more careful about them near 
activation time, as even some node versions that nominally enforced FDT 
consensus rules might not actually be enforcing them yet.

Of course, if the above solution isn't satisfactory, upgraded pruned 
nodes could simply redownload old blocks or, with extensions to the P2P 
protocol, just the relevant parts of them (i.e., coinbase transactions 
or, with a soft fork, even just commitments made in coinbase 
transactions[1]).

-Dave

[1] An idea discussed for the segwit soft fork was requiring the witness 
merkle root OP_RETURN to be the final output of the coinbase transaction 
so that all chunks of the coinbase transaction before it could be 
"compressed" into a SHA midstate and then the midstate could be extended 
with the bytes of the OP_RETURN commitment to produce the coinbase 
transaction's txid, which could then be connected to the block header 
using the standard Bitcoin-style merkle inclusion proof.  This would 
allow trailing commitments in even a very large coinbase transaction to 
be communicated in just a few hundred bytes (not including the size of 
the commitments themselves).  This idea was left out of segwit because 
at least one contemporary model of ASIC miner had a hardware-enforced 
requirement to put a mining reward payout in the final output.


------------------------------

Message: 3
Date: Fri, 29 Dec 2023 14:37:14 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Eric Voskuil <eric@voskuil.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent Timelocks
Message-ID: <786297315b27fdecc1a21cc40ef4b993@dtrt.org>
Content-Type: text/plain; charset=UTF-8; format=flowed

On 2023-12-28 08:42, Eric Voskuil via bitcoin-dev wrote:
> Assuming a ?sufficient fraction? of
> one of several economically rational behaviors is a design flaw.

The amount of effort it takes a user to pay additional miners out of
band is likely to increase much faster than probability that the user's
payment will confirm on time.  For example, offering payment to the set
of miners that controls 90% of hash rate will result in confirmation
within 6 blocks 99.9999% of the time, meaning it's probably not worth
putting any effort into offering payment to the other 10% of miners.  If
out of band payments become a significant portion of mining revenue via
a mechanism that results in small miners making significantly less
revenue than large miners, there will be an incentive to centralize
mining even more than it is today.  The more centralized mining is, the
less resistant Bitcoin is to transaction censorship.

We can't prevent people from paying out of band, but we can ensure that
the easiest and most effective way to pay for a transaction is through
in-band fees and transactions that are relayed to every miner who is
interested in them.  If we fail at that, I think Bitcoin losing its
censorship resistance will be inevitable.  LN, coinpools, and channel
factories all strongly depend on Bitcoin transactions not being
censored, so I don't think any security is lost by redesigning them to
additionally depend on reasonably accurate in-band fee statistics.

Miners mining their own transactions, accepting the occasional
out-of-band fee, or having varying local transaction selection policies
are situations that are easily addressed by the user of fee-dependent
timelocks choosing a long window and setting the dependent feerate well
below the maximum feerate they are willing to pay.

-Dave


------------------------------

Message: 4
Date: Fri, 29 Dec 2023 17:11:48 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Nagaev Boris <bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent Timelocks
Message-ID: <7b210ceabf8f5f4b58b2f6b68e6a7037@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-12-29 15:17, Nagaev Boris wrote:
> Feerate-Dependent Timelocks do create incentives to accept out-of-band
> fees to decrease in-band fees and speed up mining of transactions
> using FDT! Miners can make a 5% discount on fees paid out-of-band and
> many people will use it. Observed fees decrease and FDT transactions
> mature faster. It is beneficial for both parties involved: senders of
> transactions save 5% on fees, miners get FDT transactions mined faster
> and get more profits (for the sake of example more than 5%).

Hi Nagaev,

That's an interesting idea, but I don't think that it works due to the 
free rider problem: miner Alice offers a 5% discount on fees paid out of 
band now in the hopes of collecting more than 5% in extra fees later due 
to increased urgency from users that depended on FDTs.  However, 
sometimes the person who actually collects extra fees is miner Bob who 
never offered a 5% discount.  By not offering a discount, Bob earns more 
money on average per block than Alice (all other things being equal), 
eventually forcing her to stop offering the discount or to leave the 
market.

Additionally, if nearly everyone was paying discounted fees out of band, 
participants in contract protocols using FDTs would know to use 
proportionally higher FDT amounts (e.g. 5% over their actual desired 
fee), negating the benefit to miners of offering discounted fees.

-Dave


------------------------------

Message: 5
Date: Sat, 30 Dec 2023 18:05:54 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID: <ZY/PYiO2Yg3FNiYV@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

Huh, this list is still active?

On Fri, Dec 22, 2023 at 10:34:52PM +0000, alicexbt via bitcoin-dev wrote:
> I think CTV is not ready for activation yet. Although I want it to be activated and use payment pools, we still have some work to do and AJ is correct that we need to build more apps that use CTV on signet.

I've said it before, and I'll say it again, but if you want to change
bitcoin consensus rules, IMO the sensible process is:

 * work out what you think the change should be
 * demonstrate the benefits so everyone can clearly see what they are,
   and that they're worth spending time on
 * review the risks, so that whatever risks there may be are well
   understood, and minimise them
 * iterate on all three of those steps to increase the benefits and
   reduce the risks
 * once "everyone" agrees the benefits are huge and the risks are low,
   work on activating it

If you're having trouble demonstrating that the benefits really are
worth spending time on, you probably need to go back to the first step
and reconsider the proposal. The "covtools" and "op_cat" approaches are
a modest way of doing that: adding additional opcodes that mesh well
with CTV, increasing the benefits from making a change.

But "target fixation" [0] is a thing too: maybe "CTV" (and/or "APO")
were just a bad approach from the start. Presumably "activate CTV"
is really intended as a step towards your actual goal, whether that be
"make it harder for totalitarians to censor payments", "replace credit
cards", "make lots of money", "take control over bitcoind evelopment",
or something else. Maybe there's a better step towards some/all of
whatever those goals may be than "activate CTV". Things like "txhash"
take that approach and go back to the first step.

To me, it seems like CTV has taken the odd approach of simultaneously
maximising (at least perceived) risk, while minimising the potential
benefits. As far as maximising risk goes, it's taken Greg Maxwell's
"amusingly bad idea" post from bitcointalk in 2013 [1] and made the bad
consequence described there (namely, "coin covenants", which left Greg
"screaming in horror") as the centrepiece of the functionality being
added, per its motivation section. It then minimises the potential
benefits that accompany that risk by restricting the functionality being
provided as far as you can without neutering it entirely. If you *wanted*
a recipe for how to propose a change to bitcoin and ensure that it's
doomed to fail while still gathering a lot of attention, I'm honestly
not sure how you could come up with a better approach?

[0] https://en.wikipedia.org/wiki/Target_fixation
[1] https://bitcointalk.org/index.php?topic=278122.0

> - Apart from a few PoCs that do not achieve anything big on mainnet, nobody has tried to build PoC for a use case that solves real problems

One aspect of "minimising the benefits" is that when you make something
too child safe, it can become hard to actually use the tool at all. Just
having ideas is easy -- you can just handwave over the complex parts
when you're whiteboarding or blogging -- the real way to test if a tool
is fit for purpose is to use it to build something worthwhile. Maybe a
great chef can create a great meal with an easy-bake oven, but there's
a reason it's not their tool of choice.

Cheers,
aj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 31
********************************************
