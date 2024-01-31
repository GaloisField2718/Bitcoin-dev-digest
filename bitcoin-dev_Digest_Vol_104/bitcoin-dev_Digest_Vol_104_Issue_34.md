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

   1. Re: One-Shot Replace-By-Fee-Rate (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Wed, 31 Jan 2024 08:40:12 +0000
From: Peter Todd <pete@petertodd.org>
To: Murch <murch@murch.one>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <ZboHbJyfayUNTgKj@petertodd.org>
Content-Type: text/plain; charset="utf-8"

On Sun, Jan 28, 2024 at 12:27:06PM -0500, Murch via bitcoin-dev wrote:
> I agree in the detail, but not about the big picture. You are right that
> it?s a problem that `tx_LM` and `tx_HS` spend the same input and therefore
> are direct conflicts.
> 
> Luckily, it is unnecessary for my scenario that `tx_LM` and `tx_HS`
> conflict. The scenario only requires that `tx_LM` conflicts with `tx_LL` and
> `tx_RBFr`. `tx_HS` is supposed to get dropped indirectly per the conflict
> with `tx_LL`.
> 
> It seems to me that my example attack should work when a third confirmed
> input `c3` is introduced as follows:
> `tx_LM` spends `c3` instead of `c2`, and `tx_RBFr` spends both `c2` and
> `c3`, which allows the following four conflicts:
> 
> - `tx_HS` and `tx_RBFr` conflict on spending `c2`
> - `tx_HS` and `tx_LS` conflict on spending `tx_LL:0`
> - `tx_LL` and `tx_LM` conflict on spending `c1`
> - `tx_LM` and `tx_RBFr` conflict on spending `c3`
> 
> `tx_RBFr` would end up slightly bigger and therefore have a bigger fee, but
> otherwise the number should work out fine as they are.
> I have not verified this yet (thanks for sharing your code), but I might be
> able to take another look in the coming week if you haven?t by then.
> 
> It seems to me that my main point stands, though: the proposed RBFr rules
> would enable infinite replacement cycles in combination with the existing
> RBF rules.

Yes, *that* version of the attack does work, and I was able to succesfully
create a modified version of the previous script that demonstrates it on a
regtest node.

The attack is still exploiting a failure of our current RBF rules: the
replacement of tx_RBFr with tx_HS represents a fee-rate/mining score decrease
that replaces a more profitable transaction, tx_RBFR, with an much less
profitable transaction, ts_HS. Notably, I belive that sdaufter's "Enforce
incentive compatibility" pull-req(1) would reject it, though I haven't actually
tested that.

To fix this issue I've added a commit(2) to the libre-relay-v26.0 branch that
rejects replacements that spend unconfirmed inputs if the replacement is
conflicting with multiple transactions at once.


Let's look at why this change fixes the issue, making cycles impossible.

Bitcoin Core already uses the term "mining score" to try to measure the
profitability of a transaction. We'll define a similar measure, fee-rate-depth,
a tuple consisting of the raw fee-rate of a transaction and the depth of the
transaction, in terms of the maximum depth of unconfirmed parents that must be
mined for the transaction to be mined. The fee-rate-depth is improved if the
fee-rate is increased and/or the depth is decreased.

For example suppose we have the following unconfirmed transaction graph:

    t1 <- t2 <- t3

The depth of t1 is 0, as it only spends confirmed inputs. The depth of t2 is 1,
as it spends a 0-depth transaction, and the depth of t3 is 2, as it spends a
1-depth transaction.

Suppose we have a new transaction, t2b, that conflicts with t2, and with
fee-rates t2 < t2b < t3. Assuming that the total fee paid by t2b is high
enough, an RBF replacement is allowed:

    t1 <- t2b

While t3 paid a higher fee-rate than t2b, the fee-rate-depth has still
improved, because the depth of t2b is less than the depth of t3.


With this new change, is the fee-rate-depth always improved? Yes.

Rule #6/PaysMoreThanConflicts ensures that the fee-rate of direct conflicts is
always improved by the replacement. With *indirect* conflicts, while the
fee-rate may or may not be improved, the *depth* is improved, because we are
replacing a deeper transaction with a shallower transaction.

Secondly, for direct replacements the modified HasNoNewUnconfirmed function
ensures that the depth of fee-rate-depth is never made worse by prohibiting the
replacement of shallower transactions with deeper transactions. This is
impossible because with the new rule, if a transaction has any unconfirme
dinputs at all - a non-zero depth - only a single transaction is allowed to be
replaced at a time. Thus at worse the depth will remain constant, while rule #6
will ensure that the fee-rate is improved.


Obviously, we could probably improve on this further with more nuanced rules.
But the HasNoNewUnconfirmed fix is simple to implement, and in practice
shouldn't affect very many use-cases. Pretty much all replacements of
transactions spending unconfirmed outputs is for CPFP, and I'm not actually
aware of any wallets that try to batch CPFP transactions together. There
probably are some. But it's certainly not common. That's sufficient for the
purposes of Libre Relay, whose replace-by-fee-rate implementation is intended
as a prototype to validate the idea.

1) https://github.com/bitcoin/bitcoin/pull/26451
2) https://github.com/petertodd/bitcoin/commit/fec7965277c2287d3eaba59fdc5b75729bd4838a

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240131/9c85eb49/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 34
********************************************
