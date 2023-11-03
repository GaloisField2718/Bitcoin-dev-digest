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

   1. Re: The Pinning & Replacement Problem Set (Peter Todd)
   2. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Matt Morehouse)
   3. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Antoine Riard)
   4. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Thu, 2 Nov 2023 15:42:29 +0000
From: Peter Todd <pete@petertodd.org>
To: John Carvalho <john@synonym.to>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] The Pinning & Replacement Problem Set
Message-ID: <ZUPDZTSbTBxDnlRa@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Thu, Nov 02, 2023 at 08:58:36AM +0000, John Carvalho via bitcoin-dev wrote:
> Good morning,
> 
> All layers and technologies "on" Bitcoin will fail in situations where
> miners misbehave or the blocks & mempool remain consistently, overly full.
> Consider this as a "law" of Bitcoin/blockchains.
> 
> In hindsight (for you, not me) it was very unwise to start messing with
> mempool policies, like with RBF, mempoolfullrbf. First-seen policy brought
> a fragile harmony and utility to Bitcoin, which we were lucky to have for
> as long as we could.

Replacement cycling has nothing to do with full-rbf. You are being disingenuous
by bringing up your pet topic in relation to this exploit.

In fact, in the anchor channels case, it isn't even possible for the relevant
transactions to turn BIP-125 RBF off, as the 1 block CSV delay forces RBF to be
enabled.

Note that at the moment, the largest pool - AntPool - has full-RBF enabled.
Thus we have at least 40.1% of hash power mining with full-RBF:

AntPool: 28%
Binance Pool: 7.8%
Luxor: 2.5%
BTC.com: 1.8%


Obviously, the sane thing to do is design protocols that are made secure by
clear incentives, rather than vague hopes. Thats why I proposed OP_Expire, a
solution that does not rely on any particular mempool behavior. Indeed, it's a
solution that unlike the current mitigations relying on mempools, has good
resistance to mempool sybil attacks.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231102/d3f95d3c/attachment-0001.sig>

------------------------------

Message: 2
Date: Thu, 2 Nov 2023 17:07:39 +0000
From: Matt Morehouse <mattmorehouse@gmail.com>
To: Peter Todd <pete@petertodd.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CAGyamEXYJN0qGKzWPsN8-T1URqmeTbUH7JJjwuFKMHByCwEG3A@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Thu, Nov 2, 2023 at 6:27?AM Peter Todd via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> On Thu, Nov 02, 2023 at 05:24:36AM +0000, Antoine Riard wrote:
> > Hi Peter,
> >
> > > So, why can't we make the HTLC-preimage path expire? Traditionally, we've
> > tried
> > > to ensure that transactions - once valid - remain valid forever. We do
> > this
> > > because we don't want transactions to become impossible to mine in the
> > event of
> > > a large reorganization.
> >
> > I don't know if reverse time-lock where a lightning spending path becomes
> > invalid after a block height or epoch point solves the more advanced
> > replacement cycling attacks, where a malicious commitment transaction
> > itself replaces out a honest commitment transaction, and the
> > child-pay-for-parent of this malicious transaction is itself replaced out
> > by the attacker, leading to the automatic trimming of the malicious
> > commitment transaction.
>
> To be clear, are you talking about anchor channels or non-anchor channels?
> Because in anchor channels, all outputs other than the anchor outputs provided
> for fee bumping can't be spent until the commitment transaction is mined, which
> means RBF/CPFP isn't relevant.

IIUC, Antoine is talking about a cycling attack of the commitment
transaction itself, not the HTLC transactions.  It seems possible for
future (ephemeral) anchor channels in a world with package relay.

The idea with package relay is that commitment transaction fees will
be zero and that fees will always be paid via CPFP on the anchor
output.

Consider this scenario:  Mallory1 -> Alice -> Mallory2.
Mallory2 claims an HTLC from Alice off chain via the preimage.  Alice
attempts to claim the corresponding HTLC from Mallory1, but Mallory1
refuses to cooperate.  So Alice publishes her commitment transaction
along with a CPFP on the anchor output.  Mallory1 publishes her
competing commitment transaction with a higher CPFP fee on the anchor
output, thereby replacing Alice's package in the mempool.  Mallory1
then replacement-cycles the anchor output child transaction, causing
her commitment transaction to lose its CPFP and the package feerate to
go to zero, which is below the minimum relay fee.  Thus, Mallory1's
commitment transaction is also evicted from the mempool.  Mallory1
repeats this process every time Alice broadcasts her commitment, until
the HTLC timeout expires.  At that point the preimage path becomes
unspendable, and Mallory1 can claim the HTLC via timeout at her
leisure.

>
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 3
Date: Fri, 3 Nov 2023 05:25:24 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CALZpt+GBcqquPtf0YB07Rcy2OS0kUhv86s6g=69VrfSE72cYJQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> To be clear, are you talking about anchor channels or non-anchor channels?
> Because in anchor channels, all outputs other than the anchor outputs
provided
> for fee bumping can't be spent until the commitment transaction is mined,
which
> means RBF/CPFP isn't relevant.

I think the distinction is irrelevant here as pre-anchor channel if I have
one spendable HTLC output spend and I gain knowledge of my counterparty
commitment transaction from networks mempools, the spend is malleable and
can be used as a CPFP. If you assume anchor channels, you have 2 anchor
outputs as long both parties have balance outputs or pending HTLCs.

Though pre-anchor, legacy channels the counterparty commitment transaction
will have to be attached with a fee under min mempool fee for the
replacement cycling to happen, and let network congestion happen.

I think the more interesting case is a future world with package relay
deployed at the p2p level and anchor output on the lightning-side. Here the
most advanced replacement as illustrated in the test can happen (where
commitment has an anchor output - see L125).

Best,
Antoine

Le jeu. 2 nov. 2023 ? 06:26, Peter Todd <pete@petertodd.org> a ?crit :

> On Thu, Nov 02, 2023 at 05:24:36AM +0000, Antoine Riard wrote:
> > Hi Peter,
> >
> > > So, why can't we make the HTLC-preimage path expire? Traditionally,
> we've
> > tried
> > > to ensure that transactions - once valid - remain valid forever. We do
> > this
> > > because we don't want transactions to become impossible to mine in the
> > event of
> > > a large reorganization.
> >
> > I don't know if reverse time-lock where a lightning spending path becomes
> > invalid after a block height or epoch point solves the more advanced
> > replacement cycling attacks, where a malicious commitment transaction
> > itself replaces out a honest commitment transaction, and the
> > child-pay-for-parent of this malicious transaction is itself replaced out
> > by the attacker, leading to the automatic trimming of the malicious
> > commitment transaction.
>
> To be clear, are you talking about anchor channels or non-anchor channels?
> Because in anchor channels, all outputs other than the anchor outputs
> provided
> for fee bumping can't be spent until the commitment transaction is mined,
> which
> means RBF/CPFP isn't relevant.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231103/12097818/attachment.html>

------------------------------

Message: 4
Date: Fri, 3 Nov 2023 05:27:54 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Matt Morehouse <mattmorehouse@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>, security@ariard.me
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CALZpt+EhE=06bg8eph0bJ+bGvoJFSCEkXwmegbUNQcLSr_ACuw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> The idea with package relay is that commitment transaction fees will
> be zero and that fees will always be paid via CPFP on the anchor
> output.

Yes, even if multiple commitment transactions are pre-signed with a RBF
range of more than zero, an attacker can always select the lowest fees
pre-signed states and adjust in consequence the CPFP paid, and then evict
out the bumping CPFP.

Le jeu. 2 nov. 2023 ? 17:07, Matt Morehouse <mattmorehouse@gmail.com> a
?crit :

> On Thu, Nov 2, 2023 at 6:27?AM Peter Todd via bitcoin-dev
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
> >
> > On Thu, Nov 02, 2023 at 05:24:36AM +0000, Antoine Riard wrote:
> > > Hi Peter,
> > >
> > > > So, why can't we make the HTLC-preimage path expire? Traditionally,
> we've
> > > tried
> > > > to ensure that transactions - once valid - remain valid forever. We
> do
> > > this
> > > > because we don't want transactions to become impossible to mine in
> the
> > > event of
> > > > a large reorganization.
> > >
> > > I don't know if reverse time-lock where a lightning spending path
> becomes
> > > invalid after a block height or epoch point solves the more advanced
> > > replacement cycling attacks, where a malicious commitment transaction
> > > itself replaces out a honest commitment transaction, and the
> > > child-pay-for-parent of this malicious transaction is itself replaced
> out
> > > by the attacker, leading to the automatic trimming of the malicious
> > > commitment transaction.
> >
> > To be clear, are you talking about anchor channels or non-anchor
> channels?
> > Because in anchor channels, all outputs other than the anchor outputs
> provided
> > for fee bumping can't be spent until the commitment transaction is
> mined, which
> > means RBF/CPFP isn't relevant.
>
> IIUC, Antoine is talking about a cycling attack of the commitment
> transaction itself, not the HTLC transactions.  It seems possible for
> future (ephemeral) anchor channels in a world with package relay.
>
> The idea with package relay is that commitment transaction fees will
> be zero and that fees will always be paid via CPFP on the anchor
> output.
>
> Consider this scenario:  Mallory1 -> Alice -> Mallory2.
> Mallory2 claims an HTLC from Alice off chain via the preimage.  Alice
> attempts to claim the corresponding HTLC from Mallory1, but Mallory1
> refuses to cooperate.  So Alice publishes her commitment transaction
> along with a CPFP on the anchor output.  Mallory1 publishes her
> competing commitment transaction with a higher CPFP fee on the anchor
> output, thereby replacing Alice's package in the mempool.  Mallory1
> then replacement-cycles the anchor output child transaction, causing
> her commitment transaction to lose its CPFP and the package feerate to
> go to zero, which is below the minimum relay fee.  Thus, Mallory1's
> commitment transaction is also evicted from the mempool.  Mallory1
> repeats this process every time Alice broadcasts her commitment, until
> the HTLC timeout expires.  At that point the preimage path becomes
> unspendable, and Mallory1 can claim the HTLC via timeout at her
> leisure.
>
> >
> >
> > --
> > https://petertodd.org 'peter'[:-1]@petertodd.org
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231103/5aebc862/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 4
*******************************************
