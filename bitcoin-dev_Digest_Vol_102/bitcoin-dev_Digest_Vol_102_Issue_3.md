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

   1. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Antoine Riard)
   2. The Pinning & Replacement Problem Set (John Carvalho)


----------------------------------------------------------------------

Message: 1
Date: Thu, 2 Nov 2023 05:24:36 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CALZpt+GQ9g-uwAGYogdaJcinVHRxs4=67hML78KbramJg=davA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Peter,

> So, why can't we make the HTLC-preimage path expire? Traditionally, we've
tried
> to ensure that transactions - once valid - remain valid forever. We do
this
> because we don't want transactions to become impossible to mine in the
event of
> a large reorganization.

I don't know if reverse time-lock where a lightning spending path becomes
invalid after a block height or epoch point solves the more advanced
replacement cycling attacks, where a malicious commitment transaction
itself replaces out a honest commitment transaction, and the
child-pay-for-parent of this malicious transaction is itself replaced out
by the attacker, leading to the automatic trimming of the malicious
commitment transaction.

I think this attack scenario is exposed here:
https://github.com/ariard/bitcoin/commits/2023-10-test-mempool-2

If this scenario is correct, there is not only a need for a solution that
expires the htlc-preimage spending path, but also channel commitment ones.
I think you have a difficulty as both channel commitments can be
legitimately valid under lightning protocol semantics, where both
counterparties cannot trust the other one to broadcast a commitment state
in a timely fashion, to subsequently claim time-sensitive HTLCs.

Of course, one might come with the observation that the time-sensitive
HTLCs might be safeguarded under the new reverse time-lock semantic, though
I think you're just switching the security risk from one counterparty to
the other one. Now, the forwarding node might receive the preimage
off-chain from the payee, and then block any attempt of the payee to
broadcast its commitment transaction to claim the inbound HTLC, before the
reverse time-lock kicks out.

I believe another line of solution could to remove any counterparty
malleability in the setting of a package total fees and have fee-bumping
reserves pre-committed, though intuitively this sounds to come with the
downside of a high-level of total reserve for each channel.

Best,
Antoine

Le sam. 21 oct. 2023 ? 01:09, Peter Todd <pete@petertodd.org> a ?crit :

> On Mon, Oct 16, 2023 at 05:57:36PM +0100, Antoine Riard via bitcoin-dev
> wrote:
> > Here enter a replacement cycling attack. A malicious channel counterparty
> > can broadcast its HTLC-preimage transaction with a higher absolute fee
> and
> > higher feerate than the honest HTLC-timeout of the victim lightning node
> > and triggers a replacement. Both for legacy and anchor output channels, a
> > HTLC-preimage on a counterparty commitment transaction is malleable, i.e
> > additional inputs or outputs can be added. The HTLC-preimage spends an
> > unconfirmed and unrelated to the channel parent transaction M and
> conflicts
> > its child.
>
> The basic problem here is after the HTLC-timeout path becomes spendable,
> the
> HTLC-preimage path remains spendable. That's bad, because in this case we
> want
> spending the HTLC-preimage - if possible - to have an urgency attached to
> it to
> ensure that it happens before the previous HTLC-timeout is mined.
>
> So, why can't we make the HTLC-preimage path expire? Traditionally, we've
> tried
> to ensure that transactions - once valid - remain valid forever. We do this
> because we don't want transactions to become impossible to mine in the
> event of
> a large reorganization.
>
> A notable example of this design philosophy is seen in Bitcoin's rules
> around
> coinbase outputs: they only become spendable after 100 more blocks have
> been
> found; a 100 block reorg is quite unlikely.
>
> Enter the OP_Expire and the Coinbase Bit soft-fork upgrade.
>
>
> # Coinbase Bit
>
> By redefining a bit of the nVersion field, eg the most significant bit, we
> can
> apply coinbase-like txout handling to arbitrary transactions. Such a
> transaction's outputs would be treated similarly to a coinbase
> transaction, and
> would be spendable only after 100 more blocks had been mined. Due to this
> requirement, these transactions will pose no greater risk to reorg safety
> than
> the existing hazard of coinbase transactions themselves becoming invalid.
>
> Note how such a transaction is non-standard right now, ensuring
> compatibility
> with existing nodes in a soft-fork upgrade.
>
>
> # OP_Expire
>
> Redefining an existing OP_Nop opcode, OP_Expire would terminate script
> evaluation with an error if:
>
> 1) the Coinbase Bit was not set; or
> 2) the stack is empty; or
> 3) the top item on the stack was >= the block height of the containing
> block
>
> This is conceptually an AntiCheckLockTimeVerify: where CLTV _allows_ a
> txout to
> become spendable in a particular way in the future, Expire _prevents_ a
> txout
> from being spent in a particular way.
>
> Since OP_Expire requires the Coinbase Bit to be set, the reorg security of
> OP_Expire-using transactions is no worse than transactions spending miner
> coinbases.
>
>
> # How HTLC's Would Use OP_Expire
>
> Whenever revealing the preimage on-chain is necessary to the secure
> functioning
> of the HTLC-using protocol, we simply add an appropriate OP_Expire to the
> pre-image branch of the script along the lines of:
>
>     If
>         <expiry height> Expire Drop
>         Hash <digest> EqualVerify
>         <pubkey> CheckSig
>     ElseIf
>         # HTLC Expiration conditions
>         ...
>     EndIf
>
> Now the party receiving the pre-image has a deadline. Either they get a
> transaction spending the preimage mined, notifying the other party via the
> blockchain itself, or they fail to get the preimage mined in time,
> reverting
> control to the other party who can spend the HTLC output at their leisure,
> without strict time constraints.
>
> Since the HTLC-expired branch does *not* execute OP_Expire, the transaction
> spending the HTLC-expired branch does *not* need to set the Coinbase Bit.
> Thus
> it can be spent in a perfectly normal transaction, without restrictions.
>
>
> # Delta Encoding Expiration
>
> Rather than having a specific Coinbase Bit, it may also be feasible to
> encode
> the expiration height as a delta against a block-height nLockTime. In this
> variant, OP_Expire would work similarly to OP_CheckLockTimeVerify, by
> checking
> that the absolute expiration height was <= the requested expiration,
> allowing
> multiple HTLC preimage outputs to be spent in one transaction.
>
> If the top 16-bits were used, the maximum period a transaction could be
> valid
> would be:
>
>     2^16 blocks / 144 blocks/day = 455 days
>
> In this variant, a non-zero expiration delta would enable expiration
> behavior,
> as well as the coinbase-like output spending restriction. The remaining
> 16-bits
> of nVersion would remain available for other meanings.
>
> Similar to how CLTV and CSV verified nLockTime and nSequence respectively,
> verifying an expiration height encoded in the nVersion has the advantage of
> making an expiration height easy to detect without validating scripts.
>
> While Lightning's HTLC-success transactions currently use nLockTime=0,
> AFAIK
> there is no reason why they could not set nLockTime to be valid in the next
> block, allowing delta encoding to be used.
>
>
> ## Reusing Time-Based nLockTime
>
> Reusing time-based nLockTime's prior to some pre-2009 genesis point for
> expiration is another possibility (similar to how Lightning makes use of
> time-based nLockTime for signalling). However I believe this is not as
> desirable as delta encoding or a coinbase bit, as it would prevent
> transactions
> from using block nLockTime and expiration at the same time. It would also
> still
> require a coinbase bit or nVersion increase to ensure expiration-using
> transactions are non-standard.
>
>
> # Mempool Behavior
>
> Obviously, mempool logic will need to handle transactions that can expire
> differently than non-expiring transactions. One notable consideration is
> that
> nodes should require higher minimum relay fees for transactions close to
> their
> expiration height to ensure we don't waste bandwidth on transactions that
> have
> no potential to be mined. Considering the primary use-case, it is probably
> acceptable to always require a fee rate high enough to be mined in the next
> block.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231102/f934831c/attachment.html>

------------------------------

Message: 2
Date: Thu, 2 Nov 2023 08:58:36 +0000
From: John Carvalho <john@synonym.to>
To: Bitcoin-Dev Mailing List <bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] The Pinning & Replacement Problem Set
Message-ID:
	<CAHTn92z9RhrHd=quYwfbj9y9gvA4aGX=JGNv9UggR4cWSZE9Xw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Good morning,

All layers and technologies "on" Bitcoin will fail in situations where
miners misbehave or the blocks & mempool remain consistently, overly full.
Consider this as a "law" of Bitcoin/blockchains.

In hindsight (for you, not me) it was very unwise to start messing with
mempool policies, like with RBF, mempoolfullrbf. First-seen policy brought
a fragile harmony and utility to Bitcoin, which we were lucky to have for
as long as we could.

The engineers intentionally broke this. Mempoofullrbf washes away the
ability for users to express their intent on whether to pin or replace a
transaction, and now Lightning has BOTH pinning and replacement problems.
You could argue this was inevitable. The point here is that layers have
mempool and miner problems.

Core has a few choices here, as I see it:

1. They can try to revert mempoolfullrbf and re-establish first-seen
policy. Hard to say whether this would work, or whether it would be
enough...

2. They can create additional policies that are enforced by default that
allow people to flag how they want their txn handled, as in, a "pin this"
vs "replace this" aspect to every txn. This is probably the best option, as
it allows miners to know what people want and give it to them. This is
utility, thus incentive-compatible.

3. Remove all policy and let the market evolve to deal with the chaos.
Which is similar to the next option: do nothing.

4. Do nothing and allow a fractured mempool environment to evolve where
large businesses form private contracts with miners and pools to support
their own unsupported policies, so they can provide better experiences to
customers and users.

5. Invent some miracle magical crypto cure that I am not capable of
imagining at this time.

I disclaim some ignorance to details of how other mempool research might
affect these options and problems, but I am skeptical the dynamics
discussed here can be removed entirely.

--John Carvalho
CEO, Synonym.to <http://synonym.to/>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231102/e0d1521d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 3
*******************************************
