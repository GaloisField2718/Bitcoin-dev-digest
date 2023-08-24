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

   1. Full-RBF Peering Bitcoin Core v24.1 Released (Peter Todd)
   2. Re: A payout scheme for a non custodial mining pool
      (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Sun, 21 May 2023 21:21:33 +0000
From: Peter Todd <pete@petertodd.org>
To: Michael Ford <fanquake@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Full-RBF Peering Bitcoin Core v24.1 Released
Message-ID: <ZGqLXaa4aiyGdVaH@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, May 19, 2023 at 11:56:14AM +0100, Michael Ford via bitcoin-dev wrote:
> Bitcoin Core version 24.1 is now available from:
> 
>   <https://bitcoincore.org/bin/bitcoin-core-24.1/>

Available from: https://github.com/petertodd/bitcoin/tree/full-rbf-v24.1

eg:

    git clone -b full-rbf-v24.1 https://github.com/petertodd/bitcoin.git

What is this? It's Bitcoin Core v24.1, with Antoine Riard's full-rbf peering
code, and some additional minor updates to it. This does two things for
full-rbf nodes:

1) Advertises a FULL_RBF service bit when mempoolfullrbf=1 is set.
2) Connects to four additional FULL_RBF peers.

Doing this ensures that a core group of nodes are reliably propagating full-rbf
replacements. We don't need everyone to run this. But it'd be helpful if more
people did.

As for why you should run full-rbf, see my blog post:

https://petertodd.org/2023/why-you-should-run-mempoolfullrbf


We even have hats! :D

https://twitter.com/peterktodd/status/1659996011086110720/photo/1

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230521/7de5e4eb/attachment-0001.sig>

------------------------------

Message: 2
Date: Mon, 22 May 2023 02:27:41 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: F M <fmerli1@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] A payout scheme for a non custodial mining
	pool
Message-ID:
	<CALZpt+FbcKNKYUvRzcVxGxtOtUP1u-oNo5rWW2ChOBD-HW5DmQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Lorban,

The RFC is very clear and consistent on presenting payments pools in
the context of non-custodial mining pools, congrats to the authoring
team.

Few feedbacks, on the technical definition of a payment pool, the
common idea between all payment pools ideas presented so far
(Joinpool, Radixpool, Coinpool) is the pool tree (what you're calling
the payment tree) enabling a compact withdrawal from the pool, with
more or less conservation of the pooling after a withdrawal.

In 2., for the observation of the group of properties, there is one
more which matters a lot if you would like to have off-chain novation
of the pool tree, it's replay security, where a pool participant
cannot replay its withdrawal, partially or in whole, after withdrawing
all its balances.

In 2.1, "as, for an integer n, the n! rapidly grows in size, it
follows that the number of pre-signed transactions that has to be
computed rapidly becomes too large"."This problem seems to not have
been considered in [14]". The factorial complexity of the number of
states (transactions/balances) in function of the number pool
participants is mentioned in a footnote of the paper: "These
restrictions could be also achieved by pre-signing all possible
sequences of state transitions (producing, storing and exchanging all
these signatures), which scales poorly (factorial) with the number of
participants." and in the original mail post about Coinpool:
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017964.html
:)

In 2.7, in the rational about using ANYPREVOUT, I think if you're
using the ANYPREVOUT variant, the spent output amount is committed by
the signature digest and I think this is introducing an
interdependency between the validity of the payment tree and the block
template of transactions, as in function of this latter the coinbase
reward fluctuates ? I believe ANYPREVOUTANYSCRIPT is better as there
is no such
commitment to the spent amount/scriptPubkey iirc.

About the attacks, effectively the lack of cooperation of pool
participants to enable cooperative withdrawal is a huge DoS factor, it
can be fought by fees to enter in the pool. Another deterrence is the
timelocking of the balance in case of non-cooperative closure. Past
force-closure of pools can be consumed as a proof of good-conduct by
future co-participants in a payment pool.

Best,
Antoine


Le mer. 3 mai 2023 ? 17:05, F M via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

>
> https://docs.google.com/document/d/1qiOOSOT7epX658_nhjz-jj0DlnSRvytemOv_u_OtMcc/edit?usp=sharing
>
>
> Dear community,
>
> In the last months there have been several discussions about the topic of
> covenants and payment pools
>
> [0]. It has been difficult to approach these topics as it seems that there
> is no agreement in a precise
>
> definition on what is a covenant or what is a payment pool. This is
> probably due to the great generality
>
> of these two concepts. Perhaps, a good approach to study them is to look
> at some different use-cases
>
> and see which are the properties that appear more often and enclose them
> in a clear definition. About
>
> payment pools, that may be considered themself as a covenant, we
> specialized further, studying a payment
>
> pool?s scheme that may be used for the miners of a mining pool in order to
> share the ownership of the
>
> coinbase reward [1]. This would make the pool non-custodial.
>
> The main pools now are custodial, in the sense that they collect the
> rewards of mining, and use them
>
> subsequently to pay the miners. As there are few large pools that find
> almost all the blocks, custodial
>
> polls increase the level of centralization in a protocol born to be
> decentralized and consensus ruled.
>
> This is why we generally want non-custodial pools.
>
> The only non-custodial payment pool that appeared is P2Pool, active some
> years ago, that was also decentralized.
>
> In P2Pool, the miners were paid directly by an output of the coinbase
> transaction. This implies a very
>
> large coinbase, preventing the inclusion of more transactions in the
> block, and therefore collecting
>
> less fees and making the mining less profitable, compared to a custodial
> pool. This makes the P2Pool
>
> payout scheme inappropriate considering also that there is big effort in
> keeping blockchain light, with
>
> several off-chain protocols.
>
> Our scheme uses ANYPREVOUT signatures and it is based on the idea of
> payment trees. A payment tree is
>
> a tree of transactions that redistributes the funds to the payment pool
> participants, having their address
>
> to the leaves. The root contains the funds of the payment pool on n-of-n
> multisig. We allow payment trees
>
> for future payment pools, in which the input?s references of the
> transactions are left empty and the
>
> signatures are ANYPREVOUT.
>
> This makes it possible to safely create a payment pool, merge two payment
> pools and withdraw funds from
>
> a payment pool.
>
> Why do we use ANYPREVOUT? Most payment pool structures use precompiled
> transactions for allowing safe
>
> withdrawal. The signatures of these transactions clearly commits to the
> extranonce of the coinbase. So,
>
> if the payment pool is set for the co-ownership of the mining reward,
> there must be a set of precompiled
>
> transactions for every extranonce tried by every miner, that may not be
> feasible.
>
> The use of ANYPREVOUT allow the miners to collectively construct a payment
> tree that ?waits? the rewards,
>
> in the case that some miners finds a block. This payment tree is unique
> for all miners.
>
> We assume the pool to be centralized, even though our payment pool scheme
> perhaps can be generalized
>
> to decentralized pools. We compared the average space occupied on the
> blockchain and compared with the
>
> one of P2Pool. The results seem to be promising in this aspect, and are
> even better if the Pool is KYC.
>
> Clearly, this is just a very brief summary of our work, that is enclosed
> and labeled as an RFC. So, every
>
> remark or comment may be very appreciated.
>
>
> Authors:
>
>    -
>
>    Lorban (HRF), https://github.com/lorbax/, lorenzo.bonax@gmail.com
>    -
>
>    Fi3, https://github.com/fi3/
>    -
>
>    Rachel Rybarczyk (Galaxy Digital), https://github.com/rrybarczyk
>
> PS
> Please note that although the linked document bears some resemblance to a
> research paper, it is presented as an RFC. We chose to publish it as an RFC
> because it is not intended to be a comprehensive work.
>
> [0]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-July/020763.html
>
> [1]
> https://docs.google.com/document/d/1qiOOSOT7epX658_nhjz-jj0DlnSRvytemOv_u_OtMcc/edit?usp=sharing
>
>
>
>
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230522/8f480697/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 51
*******************************************
