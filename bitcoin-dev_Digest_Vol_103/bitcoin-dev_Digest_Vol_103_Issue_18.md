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

   1. V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Peter Todd)
   2. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Peter Todd)
   3. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Greg Sanders)


----------------------------------------------------------------------

Message: 1
Date: Wed, 20 Dec 2023 17:14:56 +0000
From: Peter Todd <pete@petertodd.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID: <ZYMhEJ3y11tnDOAx@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

V3 transactions(1) is a set of transaction relay policies intended to aim
L2/contracting protocols, namely Lightning. The main aim of V3 transactions is
to solve Rule 3 transaction pinning(2), allowing the use of ephemeral
anchors(3) that do not contain a signature check; anchor outputs that _do_
contain a signature check are not vulnerable to pinning attacks, as only the
intended party is able to spend them while unconfirmed.

The main way that V3 transactions aims to mitigate transaction pinning is with
the following rule:

    A V3 transaction that has an unconfirmed V3 ancestor cannot be larger than
    1000 virtual bytes.

Unfortunately, this rule - and thus V3 transactions - is insufficient to
substantially mitigate transaction pinning attacks.


# The Scenario

To understand why, let's consider the following scenario: Alice has a Lightning
channel with Bob, who has become unresponsive. Alice is using a Lightning
protocol where using V3 commitment transactions with a single OP_TRUE ephemeral
anchor of zero value.  The commitment transaction must be broadcast in a
package, containing both the commitment transaction, and a transaction spending
the anchor output; regardless of the fee of the commitment transaction, this is
a hard requirement, as the zero-valued output is considered non-standard by V3
rules unless spent in the same package.

To pay for the transaction fee of the commitment transaction, Alice spends the
ephemeral output in a 2 input, 1 output, taproot transaction of 152vB in size,
with sufficient feerate Ra to get the transaction mined in what Alice
considers to be a reasonable amount of time.


# The Attack

Enter Mallory. His goal is to grief Alice by forcing her to spend more money
than she intended, at minimum cost. He also maintains well connected nodes,
giving him the opportunity to both learn about new transactions, and quickly
broadcast transactions to a large number of nodes at once.

When Mallory learns about Alice's commitment+anchor spend package, he signs a
replacement anchor spend transaction, 1000vB in size, with a lower feerate Rm
such that the total fee of Alice's anchor spend is <= Mallory's anchor spend
(in fact, the total fee can be even less due to BIP-125 RBF Rule #4, but for
sake of a simple argument we'll ignore this). Next, Mallory broadcast's that
package widely, using his well-connected nodes.

Due to Rule #3, Alice's higher feerate transaction package does not replace
Mallory's lower fee rate, higher absolute fee, transaction package. Alice's
options are now:

1. Wait for Mallory's low feerate transaction to be mined (mempool expiration
   does not help here, as Mallory can rebroadcast it indefinitely).
2. Hope her transaction got to a miner, and wait for it to get mined.
3. Replace it with an even higher fee transaction, spending at least as much
   money as Mallory allocated.

In option #1 and #3, Mallory paid no transaction fees to do the attack.

Unfortunately for Alice, feerates are often quite stable. For example, as I
write this, the feerate required to get into the next block is 162sat/vB, while
the *lowest* feerate transaction to get mined in the past 24 hours is
approximately 80sat/vB, a difference of just 2x.

Suppose that in this circumstance Alice needs to get her commitment transaction
mined within 24 hours. If Mallory used a feerate of 1/2.5th that of Alice,
Mallory's transaction would not have gotten mined in the 24 hour period, with a
reasonable safety margin. Thus the total fee of Mallory's package would have
been 6.6 * 1/2.5 = 2.6x more than Alice's total fee, and to get her transaction
mined prior to her deadline, Alice would have had to pay a 2.6x higher fee than
expected.


## Multi-Party Attack

Mallory can improve the efficiency of his griefing attack by attacking multiple
targets at once. Assuming Mallory uses 1 taproot input and 1 taproot output for
his own funds, he can spend 21 ephemeral anchors in a single 1000vB
transaction.

Provided that the RBF Rule #4 feerate delta is negligible relative to current
feerates, Mallory can build up the attack against multiple targets by
broadcasting replacements with slightly higher feerates as needed to add and
remove Alice's.

The cost of the attack to Mallory is estimating fees incorrectly, and using a
sufficiently high feerate that his transaction does in fact get mined. In that
circumstance, if he's attacking multiple targets, it is likely that all his
transactions would get mined at once. Thus having only a single attack
transaction reduces that worst case cost. Since Mallory can adding and remove
Alice's, he can still force multiple Alice's to spend funds bumping their
transactions.


# Solutions

## Replace-by-Feerate

Obviously, this attack does not work if Rule #3 is removed for small
transactions, allowing Alice's transaction to replace Mallory via
replace-by-feerate. In the common situation where mempools are deep, this is
arguably miner incentive compatible as other transactions at essentially the
same feerate will simply replace the "space" taken up by the griefing
transaction.


## Restrict V3 Children Even Further

If V3 children are restricted to, say, 200vB, the attack is much less effective
as the ratio of Alice vs Mallory size is so small. Of course, this has the
disadvantage of making it more difficult in some cases to find sufficient
UTXO's to pay for fees, and increasing the number of UTXO's needed to fee bump
large numbers of transactions.


# References

1) https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-September/020937.html,
   "[bitcoin-dev] New transaction policies (nVersion=3) for contracting protocols",
   Gloria Zhao, Sep 23 2022

2) https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki#implementation-details,
   "The replacement transaction pays an absolute fee of at least the sum paid by the original transactions."

3) https://github.com/instagibbs/bips/blob/ephemeral_anchor/bip-ephemeralanchors.mediawiki

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231220/cf107467/attachment-0001.sig>

------------------------------

Message: 2
Date: Wed, 20 Dec 2023 19:48:59 +0000
From: Peter Todd <pete@petertodd.org>
To: Gloria Zhao <gloriajzhao@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID: <ZYNFK5V5e9PnT9eL@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Wed, Dec 20, 2023 at 07:13:22PM +0000, Gloria Zhao wrote:
> The "damage" of the pin can quantified by the extra fees Alice has to pay.
> 
> For a v3 transaction, Mallory can attach 1000vB at 80sat/vB. This can
> increase the cost of replacement to 80,000sat.
> For a non-v3 transaction, Mallory can attach (101KvB - N) before maxing out
> the descendant limit.
> Rule #4 is pretty negligible here, but since you've already specified
> Alice's child as 152vB, she'll need to pay Rule #3 + 152sats for a
> replacement.
> 
> Let's say N is 1000vB. AFAIK commitment transactions aren't usually smaller
> than this:

You make a good point that the commitment transaction also needs to be included
in my calculations. But you are incorrect about the size of them.

With taproot and ephemeral anchors, a typical commitment transaction would have
a single-sig input (musig), two taproot outputs, and an ephemeral anchor
output.  Such a transaction is only 162vB, much less than 1000vB.

In my experience, only a minority of commitment transactions that get mined
have HTLCs outstanding; even if there is an HTLC outstanding, that only gets us
up to 206vB.

> > Mallory can improve the efficiency of his griefing attack by attacking
> multiple
> > targets at once. Assuming Mallory uses 1 taproot input and 1 taproot
> output for
> > his own funds, he can spend 21 ephemeral anchors in a single 1000vB
> > transaction.
> 
> Note that v3 does not allow more than 1 unconfirmed parent per tx.

Ah, pity, I had misremembered that restriction as being removed, as that is a
potentially significant improvement in scenarios where you need to do things
like deal with a bunch of force closes at once.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231220/530e85c3/attachment-0001.sig>

------------------------------

Message: 3
Date: Wed, 20 Dec 2023 15:16:25 -0500
From: Greg Sanders <gsanders87@gmail.com>
To: Peter Todd <pete@petertodd.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID:
	<CAB3F3DuKxw_osQcW++GeasGVEedcZ16inqrQPoAWQiF4HsGbdw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Peter,

Thanks for taking the time to understand the proposal and give thoughtful
feedback.

With this kind of "static" approach I think there are fundamental
limitations because
the user has to commit "up front" how large the CPFP later will have to be.
1kvB
is an arbitrary value that is two orders of magnitude less than the
possible package
size, and allows fairly flexible amounts of inputs(~14 taproot inputs
IIRC?) to effectuate a CPFP.
I'd like something much more flexible, but we're barely at whiteboard stage
for alternatives and
they probably require more fundamental work. So within these limits, we
have to pick some number,
and it'll have tradeoffs.

When I think of "pinning potential", I consider not only the parent size,
and not
only the maximum child size, but also the "honest" child size. If the honest
user does relatively poor utxo management, or the commitment transaction
is of very high value(e.g., lots of high value HTLCs), the pin is
essentially zero.
If the honest user ever only have one utxo, then the "max pin" is effective
indeed.

> Alice would have had to pay a 2.6x higher fee than
expected.

I think that's an acceptable worst case starting point, versus the status
quo which is ~500-1000x+.
Not great, not terrible.

Cheers,
Greg


On Wed, Dec 20, 2023 at 2:49?PM Peter Todd via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> On Wed, Dec 20, 2023 at 07:13:22PM +0000, Gloria Zhao wrote:
> > The "damage" of the pin can quantified by the extra fees Alice has to
> pay.
> >
> > For a v3 transaction, Mallory can attach 1000vB at 80sat/vB. This can
> > increase the cost of replacement to 80,000sat.
> > For a non-v3 transaction, Mallory can attach (101KvB - N) before maxing
> out
> > the descendant limit.
> > Rule #4 is pretty negligible here, but since you've already specified
> > Alice's child as 152vB, she'll need to pay Rule #3 + 152sats for a
> > replacement.
> >
> > Let's say N is 1000vB. AFAIK commitment transactions aren't usually
> smaller
> > than this:
>
> You make a good point that the commitment transaction also needs to be
> included
> in my calculations. But you are incorrect about the size of them.
>
> With taproot and ephemeral anchors, a typical commitment transaction would
> have
> a single-sig input (musig), two taproot outputs, and an ephemeral anchor
> output.  Such a transaction is only 162vB, much less than 1000vB.
>
> In my experience, only a minority of commitment transactions that get mined
> have HTLCs outstanding; even if there is an HTLC outstanding, that only
> gets us
> up to 206vB.
>
> > > Mallory can improve the efficiency of his griefing attack by attacking
> > multiple
> > > targets at once. Assuming Mallory uses 1 taproot input and 1 taproot
> > output for
> > > his own funds, he can spend 21 ephemeral anchors in a single 1000vB
> > > transaction.
> >
> > Note that v3 does not allow more than 1 unconfirmed parent per tx.
>
> Ah, pity, I had misremembered that restriction as being removed, as that
> is a
> potentially significant improvement in scenarios where you need to do
> things
> like deal with a bunch of force closes at once.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231220/3fcbd455/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 18
********************************************
