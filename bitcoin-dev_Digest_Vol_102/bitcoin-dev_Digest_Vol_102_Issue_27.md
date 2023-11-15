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

   1. Fwd: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Antoine Riard)
   2. Re: On solving pinning, replacement cycling and mempool
      issues for bitcoin second-layers (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Wed, 15 Nov 2023 17:53:57 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Fwd: OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CALZpt+ERdc5XFyiAyc-3KpU=5Wh1KZTfsNNsLn_Nj60OwqjXTg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> No, that's not a general underlying issue. You've found two separate
issues.

> Furthermore, revoked states are clearly different than HTLCs: they're
> fraudulent, and thus in punishment-using protocols they are always
associated
> with high risks of loss if they do in fact get detected or mined. There's
> probably tweaks we can do to improve this security. But the general
principle
> there is certainly true.

I see your point in saying we have two separate issues, one the on-chain
inclusion of "expired" off-chain output spend (e.g the HTLC-preimage), the
other one the usage of revoked or updated or asymmetric states to jam the
confirmation of a valid off-chain state. I do think the second one would
bring a solution to the first one, as you will be always sure that your
counterparty cannot "replay" an "expired" off-chain output at its advantage.

Even for solving the first issue, I'm not sure op_expire is enough, you
need to expire the worthiness of an off-chain revealed witness secret too
(here the preimage). E.g using short-lived proofs, i.e after a specified
period of time, the proof is no longer convincing.

I still think op_exire is interesting on its own, beyond solving any
security issue. E.g for Discreet Log Contract, one can build a time-bounded
sequential claim of the same output fund among a set of counterparties.

> For a lightning channel to be economical at all in a general routing
> environment, the highest likely fee has to be small enough for it to
represent
> a small percentage of the total value tied up in the Lightning channel.
Tying
> up a small percentage of the overall capacity for future fee usage is not
a
> significant expense.

Sure, I still think this introduces the corollary for lightning nodes that
any payment under the highest likely fee now has a probabilistic security,
where the lightning node should make guesses on the worst-level of mempools
feerate that can happen between the timelock duration of said payment.

> That attack doesn't make sense. HTLCs go to fees at a certain feerate. In
a
> normal environment where there is a constant supply of fee paying
transactions,
> the profit for the miner is not the total HTLC value, but the increase in
> feerate compared to the transactions they had to give up to mine the
commitment
> transaction.

The attack makes sense in an environment where the level of HTLC trimmed as
fees on the commitment transaction renders the feerates of this transaction
more interesting than the marginal known transaction in a miner block
template. If there is an environment where you're always guaranteed there
is a constant supply of fee paying transactions paying a better feerate
than the highest-fee rate that trimmed HTLCs can be a commitment
transaction, of course the attack wouldn't be plausible.

In a world where you have a dynamic blockspace demand market and
asymmetries of information, Lightning routing nodes will be always exposed
to such attacks.

> Second, it's obvious that the total trimmed HTLCs should be limited to
what
> would be a reasonable transaction fee. A situation where you have 80% of
the
> channel value going to fees due to a bunch of small HTLCs is obviously
> ridiculous, and to the extent that existing implementations have this
issue,
> should be fixed.

This is the hard thing, the existence of asymmetries of information in what
is a reasonable transaction fee and what is the level of mempools fee rates
at time of broadcast. One could imagine a consensus change where trimmed
HTLCs not worthy at the last X blocks of feerates are automatically
aggregated or trimmed (think median-time-past though for median fee rates
over X blocks).

> Yes, obviously. But as I said above, it just doesn't make sense for
channels to
> be in a situation where closing them costs a significant % of the channel
value
> in fees, so we're not changing the status quo much.

Evaluation of the significant % of the channel value burned in fees in the
worst-case at time of off-chain state commitment is the hard thing.

> Do you have a concrete attack?

I don't have a concrete attack with sufficient testing to say with a
satisfying level of certainty that I have a concrete attack.

> No, you are missing the point. RBF replacements can use SIGHASH_NOINPUT
to sign
> HTLC refund transactions, removing the need for a set of different HTLC
refund
> transactions for each different feerate of the commitment transaction.

See above, I think this solution with RBF replacement is robust on the
assumption you cannot use the commitment transaction to jam the
HTLC-preimage until your HTLC-refund transaction is valid (under
nLocktime). Though my point here was only about the LN-symmetry states, not
second-stage transactions on top of them.

> I'm making no comment on how to do RBF replacements with LN-Symmetry,
which I
> consider to be a broken idea in non-trusted situations anyway
> Removing justice from Lightning is always going to be hopelessly insecure
when you can't at
> least somewhat trust your counterparty. If your usage of LN-Symmetry is
> sufficiently secure, you probably don't have to worry about them playing
fee
> games with you either.

I agree here that LN-symmetry would be better if you can conserve the
punishment ability.

See
https://lists.linuxfoundation.org/pipermail/lightning-dev/2019-July/002064.html

On the lack of worries about playing fees games with you, see concern above
if your counterparty is a miner, even one with low-hashrate capability.
Here low-hashrate capability can be understood as "do you have a non-null
chance to mine a block as long as a HTLC-output is committed on an
off-chain state only known among off-chain counterparties e.g".
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231115/fbb0ae92/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 15 Nov 2023 18:14:28 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Cc: security@ariard.me
Subject: Re: [bitcoin-dev] On solving pinning, replacement cycling and
	mempool issues for bitcoin second-layers
Message-ID:
	<CALZpt+EYjMhS1HsyZfKNXkQkfoUg2zU9OBSC=v7am5eR_rtJew@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi all,

I think any valid consensus-change based solution to the pinning and
replacement cycling issues for Bitcoin L2s should respect the following
properties / requirements (ideally):
- non-interactive with contribution of your off-chain counterparty
- minimize level of fee-bumping reserve and number of UTXO locked
- block any malicious pinning or replacement cycling as long as you can
compete with ongoing fee rates
- do not make the security of low-value lightning payments conditional on a
probabilistic state of local knowledge of historical mempool
- generalize to N > 2 multi-party off-chain construction
- minimize the witness size by using efficient bitcoin script semantics
- do not give an edge to low-hashrate or coalition of low-hashrate miners
to play fees games with Lightning / L2 nodes
- be composable with a solution to massive force-closure of time-sensitive
off-chain states
- not make it worst things like partial or global mempool partitioning [0]

I think this is already a lot. I had some intuitive solutions aiming to
remove package malleability by using something like the annex and
sighash_anyamount semantic, though after musing on Peter Todd's op_expire
proposal, I wonder if there is not another family of solutions that can be
designed using "moon math" cryptos like short-lived proofs and strictly
enforced sequential time windows.

I don't have any strong design at all, and in any case given the complexity
it would be good to have an end-to-end implementation of any solution, at
the very least see it works well for the Lightning case (chatted with Gleb
out-of-band he's too busy with Erlay for now to research more on those
subjects and on my side bored working more on those issues, sadly I don't
know that many bitcoin, lightning and covenant researchers that understand
that well those problems). I still think pinning and replacement attacks
deserve more real-world mainnet experimentation, under usual
ethical guidelines .

Inviting everyone in the Bitcoin research community to research more on
those pinning, replacement cycling and miners incentives misalignment with
second-layers. Please do so, those issues are serious enough if we wish to
have a reliable fee market in a post-subsidy world and a sustainable
decentralized miner ecosystem in the long-term (well...dumb ordinal
transactions might save the day, though open another wormhole of technical
issues).

Best,
Antoine

[0] See The Ugly scenario here
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/018011.html

Le dim. 22 oct. 2023 ? 03:27, Antoine Riard <antoine.riard@gmail.com> a
?crit :

> Hi,
>
> I think if Gleb Naumenko and myself allocate our research time on this
> issue, we should (hopefully) be able to come with a strong sustainable fix
> to the lightning network, both systematically solving pinnings and
> replacement cycling attacks (and maybe other mempools issues or things
> related like massive force-closure beyond available blockspace can absorb
> before pre-signed transactions timelocks expiration as mentioned in the
> original paper).
>
> I have not yet probed Gleb's mind on this, though we both studied those
> cross-layer issues together as early as 2019 / 2020, and I think we have
> built an intuitive understanding of the problem-space, with both practical
> experience of bitcoin core and rust-lightning codebases and landmark
> research in this area [0] [1]. If Gleb isn't too busy with Erlay in core,
> I'm sure he'll be enthusiastic to contribute research time at his own pace
> (and I might probe a bit of Elichai Turkel time to verify the maths of all
> sustainable lightning fixes we might propose and the risks models). All
> soft commitments and assuming the interest of the bitcoin community.
>
> One good advantage of long-term sustainable fixes, it should
> (optimistically yet to be demonstrated) lower the fee-bumping reserve value
> and number of UTXOs lightning users (and maybe bandwidth) have to lock
> continuously to use this worldwide 24 / 7 payment system.
>
> Reopened the issue on coordinated security issues handling in the LN
> ecosystem:
> https://github.com/lightning/bolts/pull/772
>
> While I'll stay focused on solving the above problems at the base-layer
> where they're best solved, at least I'll stay around for a few months
> making transitions with the younger generation of LN devs.
>
> For transparency, I don't have any strong solution design yet at all,
> neither code, conceptual draft or paper ready, and game-theory and nodes
> network processing resources changes will have to be weighted very
> carefully, all under the bitcoin open and responsible process we currently
> have. Overall, this will take reasonable time (e.g package relay design
> discussions have been started in 2018 and we're only now at the hard
> implementation and review phase) to carry on forward.
>
> Looking forward to hearing thoughts of the Bitcoin and Lightning
> development protocols community.
>
> [0]
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2020-February/002569.html
> [1] https://arxiv.org/pdf/2006.01418.pdf
>
> "They who face calamity without wincing, and who offer the most energetic
> resistance, these, be they States or individuals, are the truest heroes". -
> Thucydides.
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231115/18f2f153/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 27
********************************************
