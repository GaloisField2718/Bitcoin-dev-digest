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

   1. BIP number request for wallet policies (Antoine Poinsot)
   2. Re: Altruistic Rebroadcasting - A Partial Replacement Cycling
      Mitigation (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Sat, 16 Dec 2023 14:10:08 +0000
From: Antoine Poinsot <darosior@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] BIP number request for wallet policies
Message-ID:
	<qCTW51rFF01GBS4D2xALWGMI_OTJavtqEJ5ztfOD1E65mA-Iwzc0Z8OqmGbGCmi2WxNq85cIMvOXD6qYvGOYGKF_QT5ACRd_E9UmisdIet4=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Wallet policies, a standard for implementing support for output descriptors in hardware signing devices was introduced by Salvatore Ingala a year and a half ago [0].

A pull request to the BIP repository was opened more than a year ago [1]. It's been waiting for a BIP number to be assigned since then.

There is now 3 majors hardware signing devices using this standard in production (Ledger, BitBox02, Jade). There has been multiple pings on the PR in the past year to get assigned a BIP number.

It would be nice to hear from the BIP editors about their expectations from the author, so we can move forward with this document specifying what's already become an industry standard.

Antoine Poinsot

[0] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-May/020492.html
[1] https://github.com/bitcoin/bips/pull/1389


------------------------------

Message: 2
Date: Sun, 17 Dec 2023 10:57:32 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Altruistic Rebroadcasting - A Partial
	Replacement Cycling Mitigation
Message-ID: <ZX7UHOaUKk/+jbS1@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Dec 15, 2023 at 10:29:22PM +0000, Antoine Riard wrote:
> Hi Peter,
> 
> > Altruistic third parties can partially mitigate replacement cycling(1)
> attacks
> > by simply rebroadcasting the replaced transactions once the replacement
> cycle
> > completes. Since the replaced transaction is in fact fully valid, and the
> > "cost" of broadcasting it has been paid by the replacement transactions,
> it can
> > be rebroadcast by anyone at all, and will propagate in a similar way to
> when it
> > was initially propagated. Actually implementing this simply requires code
> to be
> > written to keep track of all replaced transactions, and detect
> opportunities to
> > rebroadcast transactions that have since become valid again. Since any
> > interested third party can do this, the memory/disk space requirements of
> > keeping track of these replacements aren't important; normal nodes can
> continue
> > to operate exactly as they have before.
> 
> I think there is an alternative to altruistic and periodic rebroadcasting
> still solving replacement cycling at the transaction-relay level, namely
> introducing a local replacement cache.
> 
> https://github.com/bitcoin/bitcoin/issues/28699
> 
> One would keep in bounded memory a list of all seen transactions, which
> have entered our mempool at least once at current mempool min fee.

Obviously a local replacement cache is a possibility. The whole point of my
email is to show that a local replacement cache isn't necessarily needed, as
any alturistic party can implement that cache for all nodes.

> For the full-nodes which cannot afford extensive storage in face of
> medium-liquidity capable attackers, could imagine replacement cache nodes
> entering into periodic altruistic rebroadcast. This would introduce a
> tiered hierarchy of full-nodes participating in transaction-relay. I think
> such topology would be more frail in face of any sybil attack or scarce
> inbound slots connections malicious squatting.
> 
> The altruistic rebroadcasting default rate could be also a source of
> amplification attacks, where there is a discrepancy between the feerate of
> the rebroadcast traffic and the current dynamic mempool min fee of the
> majority of network mempools. As such wasting bandwidth for everyone.

1) That is trivially avoided by only broadcasting txs that meet the local
mempool min fee, plus some buffer. There's no point to broadcasting txs that
aren't going to get mined any time soon.

2) BIP-133 feefilter avoids this as well, as Bitcoin Core uses the feefilter
P2P message to tell peers not to send transactions below a threshold fee rate.

https://github.com/bitcoin/bips/blob/master/bip-0133.mediawiki

> Assuming some medium-liquidity or high-liquidity attackers might reveal any
> mitigation as insufficient, as an unbounded number of replacement
> transactions might be issued from a very limited number of UTXOs, all
> concurrent spends. In the context of multi-party time-sensitive protocol,
> the highest feerate spend of an "honest" counterparty might fall under the
> lowest concurrent replacement spend of a malicious counterparty, occupying
> all the additional replacement cache storage.

Did you actually read my email? I worked out the budget required in a
reasonable worst case scenario:

> > Suppose the DoS attacker has a budget equal to 50% of the total block
> > reward.
> > That means they can spend 3.125 BTC / 10 minutes, or 520,833sats/s.
> >
> >     520,833 sats/s
> >     -------------- = 2,083,332 bytes / s
> >     0.25 sats/byte
> >
> > Even in this absurd case, storing a one day worth of replacements would
> > require
> > just 172GB of storage. 256GB of RAM costs well under $1000 these days,
> > making
> > altruistic rebroadcasting a service that could be provided to the network
> > for
> > just a few thousand dollars worth of hardware even in this absurd case.

Here, we're talking about an attacker that has financial resources high enough
to possibly do 51% attacks. And even in that scenario, storing the entire
replacement database in RAM costs under $1000

The reality is such an attack would probably be limited by P2P bandwidth, not
financial resources, as 2MB/s of tx traffic would likely leave mempools in an
somewhat inconsistent state across the network due to bandwidth limitations.
And that is *regardless* of whether or not anyone implements alturistic tx
broadcasting.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231217/6d8a0ff7/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 8
*******************************************
