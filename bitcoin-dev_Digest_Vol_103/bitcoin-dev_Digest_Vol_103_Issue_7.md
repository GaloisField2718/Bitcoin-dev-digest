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

   1. Re: Altruistic Rebroadcasting - A Partial Replacement Cycling
      Mitigation (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Fri, 15 Dec 2023 22:29:22 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Altruistic Rebroadcasting - A Partial
	Replacement Cycling Mitigation
Message-ID:
	<CALZpt+HLoomKZn=QsBZ-4M-WSDzjEA_p1nzk9N=+R4MveeAOFQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Peter,

> Altruistic third parties can partially mitigate replacement cycling(1)
attacks
> by simply rebroadcasting the replaced transactions once the replacement
cycle
> completes. Since the replaced transaction is in fact fully valid, and the
> "cost" of broadcasting it has been paid by the replacement transactions,
it can
> be rebroadcast by anyone at all, and will propagate in a similar way to
when it
> was initially propagated. Actually implementing this simply requires code
to be
> written to keep track of all replaced transactions, and detect
opportunities to
> rebroadcast transactions that have since become valid again. Since any
> interested third party can do this, the memory/disk space requirements of
> keeping track of these replacements aren't important; normal nodes can
continue
> to operate exactly as they have before.

I think there is an alternative to altruistic and periodic rebroadcasting
still solving replacement cycling at the transaction-relay level, namely
introducing a local replacement cache.

https://github.com/bitcoin/bitcoin/issues/28699

One would keep in bounded memory a list of all seen transactions, which
have entered our mempool at least once at current mempool min fee.

For the full-nodes which cannot afford extensive storage in face of
medium-liquidity capable attackers, could imagine replacement cache nodes
entering into periodic altruistic rebroadcast. This would introduce a
tiered hierarchy of full-nodes participating in transaction-relay. I think
such topology would be more frail in face of any sybil attack or scarce
inbound slots connections malicious squatting.

The altruistic rebroadcasting default rate could be also a source of
amplification attacks, where there is a discrepancy between the feerate of
the rebroadcast traffic and the current dynamic mempool min fee of the
majority of network mempools. As such wasting bandwidth for everyone.

Assuming some medium-liquidity or high-liquidity attackers might reveal any
mitigation as insufficient, as an unbounded number of replacement
transactions might be issued from a very limited number of UTXOs, all
concurrent spends. In the context of multi-party time-sensitive protocol,
the highest feerate spend of an "honest" counterparty might fall under the
lowest concurrent replacement spend of a malicious counterparty, occupying
all the additional replacement cache storage.

Best,
Antoine

Le sam. 9 d?c. 2023 ? 10:09, Peter Todd via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

> While this seems like a reasonably obvious idea, I couldn't find a previous
> example of it published on bitcoin-dev or elsewhere. So for the ability to
> cite
> it, I'll publish it now.
>
>
> # Summary
>
> Altruistic third parties can partially mitigate replacement cycling(1)
> attacks
> by simply rebroadcasting the replaced transactions once the replacement
> cycle
> completes. Since the replaced transaction is in fact fully valid, and the
> "cost" of broadcasting it has been paid by the replacement transactions,
> it can
> be rebroadcast by anyone at all, and will propagate in a similar way to
> when it
> was initially propagated. Actually implementing this simply requires code
> to be
> written to keep track of all replaced transactions, and detect
> opportunities to
> rebroadcast transactions that have since become valid again. Since any
> interested third party can do this, the memory/disk space requirements of
> keeping track of these replacements aren't important; normal nodes can
> continue
> to operate exactly as they have before.
>
>
> # Background
>
> To recall, a replacement cycling attack has three basic stages:
>
> 0) Target transaction tx0_a is broadcast, spending one or more outputs
> 1) Attacker broadcasts double-spend tx0_b, spending an additional output
>    under the attacker's control
> 2) Attacker broadcasts double-spend tx1, double-spending only the
> additional
>    input, resulting in the original input set not being spent
>
> Replacement cycling is a potential threat any time two or more parties
> have the
> ability to spend a single txout, and rendering that output _unspent_ is
> harmful. For example, replacement cycling is an attack on lightning HTLCs,
> because it can result in an HTLC pre-image not being observed by a party
> until
> after the HTLC expires. Similarly, replacement cycling is a potential
> attack on
> signatureless anchor outputs, as it can allow third parties to revoke a
> CPFP
> anchor spend, making the parent transaction(s) unminable.
>
>
> # Altruistic Rebroadcasting
>
> Bitcoin Core keeps no records of replaced transactions. Thus after the
> replacement cycling attack is complete, tx0_a has been entirely purged
> from a
> Bitcoin Core node's mempool, and all inputs to tx0_a are unspent. Thus it
> is
> just as valid to broadcast as before.
>
>
> ## Resources Required
>
> Let's suppose we have a DoS attacker who is constantly broadcasting
> replacement
> in an effort to overwhelm nodes performing altruistic rebroadcasting. The
> BIP-125 RBF rules require that a replacement transaction pay for the
> bandwidth
> used by the replacement. On Bitcoin Core, this defaults to 1sat/vByte.
> Assuming
> the attacking transactions are ~100% witness bytes, that is ~0.25sats/byte
> of
> relay bandwidth per peer.
>
> Suppose the DoS attacker has a budget equal to 50% of the total block
> reward.
> That means they can spend 3.125 BTC / 10 minutes, or 520,833sats/s.
>
>     520,833 sats/s
>     -------------- = 2,083,332 bytes / s
>     0.25 sats/byte
>
> Even in this absurd case, storing a one day worth of replacements would
> require
> just 172GB of storage. 256GB of RAM costs well under $1000 these days,
> making
> altruistic rebroadcasting a service that could be provided to the network
> for
> just a few thousand dollars worth of hardware even in this absurd case.
>
> It's notable that miners may in fact want to run replacement rebroadcasting
> software themselves, to ensure they are not missing any valid, profitable,
> transactions. In the context of a large mining pool, the additional cost
> over
> running a regular node may be affordable.
>
>
> ## Limitations
>
> At the moment, Bitcoin Core propagates transactions purely via INV
> announcements; there is no set reconciliation mechanism to synchronize
> mempools
> between peers. If an INV announcement is missed for some reason, it's quite
> possible that the transaction will be missed. Thus rebroadcasting may be
> defeated if the % of nodes who do *not* have the transaction at the time of
> rebroadcast is below the percolation threshold. Indeed, with good timing
> and a
> sybil attack, an attacker may be able to deliberately trigger this
> condition.
>
> Improvements like the Transaction Announcements Reconciliation(2) BIP may
> be
> able to mitigate this issue, by ensuring that regardless of the timing of
> replacements, the rebroadcast transaction eventually reaches all nodes via
> the
> reconciliation process.
>
>
> # References
>
> 1)
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-October/021999.html
> 2)
> https://github.com/naumenkogs/bips/blob/bip_0330_updates/bip-0330.mediawiki
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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231215/a8e8e13e/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 7
*******************************************
