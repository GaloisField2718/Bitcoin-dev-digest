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

   1. Re: [Lightning-dev] Scaling Lightning With Simple	Covenants
      (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Wed, 15 Nov 2023 19:59:37 +0000
From: jlspc <jlspc@protonmail.com>
To: Anthony Towns <aj@erisian.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Scaling Lightning With
	Simple	Covenants
Message-ID:
	<8fg80wYc1iQdw_Fcn4Ub3U6Xo4I1ukx8VVT2rVsodp5av_y5wGk0biWXILfyn-TFsglELcAgJyhaUN9PY5KO3xPhu-SCOO-vNvVt9-ZJCLc=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi aj,

A few more thoughts on this trust/safety vs. capital efficiency tradeoff:

> Optimising that formula by making LA [the channel's active lifetime] as large as possible doesn't
> necessarily work -- if a casual user spends all their funds and
> disappears prior to the active lifetime running out, then those
> funds can't be easily spent by B until the total lifetime runs out,
> so depending on how persistent your casual users are, I think that's
> another way of ending up with your capital locked up unproductively.

The risk of the casual user spending all of their funds can be addressed by having the casual user prepay the cost-of-capital fees for the dedicated user's funds for the entire lifetime of the channel.
Then, whenever the dedicated user's funds increase or decrease (due to a send or receive by the casual user), a corresponding prepayment adjustment is included in the new balances defined by the send or receive HTLC.
With prepayments, the dedicated user can safely agree to a long active lifetime for the channel.

In the paper, I assumed an active lifetime of 110,000 blocks (about 2.1 years), but allowed the casual users to obtain a new channel every 10,000 blocks (about 2.5 months) by staggering their timeout-trees ([1], Sec. 4.8 and 5).
The paper includes a rollover period (which covers the casual user's unavailability for up to 2.5 months) in addition to the timeout-tree's active lifetime (25 months) and inactive lifetime (1 week for putting leaves onchain, which definitely introduces risk).

Here are some rough calculations if one wants to eliminate risk by making the inactive lifetime long enough to put all leaves of all timeout-trees onchain before the timeout-trees' expiries:

TIME BOUND ON NUMBER OF LEAVES:
------------------------------
There are approximately 52,500 blocks / year, each with at most 4M vbytes, for a total of approximately 210B = 2.1 * 10^11 vbytes per year.
If each leaf requires an average (when all leaves in a tree are put onchain) of 2,100 vbytes, then 2.1 * 10^11 / 2,100 = 10^8 = 100M leaves can be put onchain in 1 year with full block capacity devoted to leaves, and in 1/x years with a fraction of x capacity devoted to leaves.
Therefore, at x = 0.5 capacity:
    50M leaves can be put onchain per year
    100M leaves can be put onchain in 2 years
    1B leaves can be put onchain in 20 years
    10B leaves can be put onchain in 200 years
    100B leaves can be put onchain in 2,000 years

Assuming an active lifetime of 2.1 years, adding an inactive period of 2 years may be plausible, depending on the cost of capital.
Therefore, scaling to 100M or so leaves (across all timeout-trees) while maintaining the ability to put all leaves onchain may be doable.

On the other hand, an inactive period of 20 years seems unreasonable.
As a result, scaling to billions of leaves probably requires trading off safety vs. capital efficiency (as you noted).

FEERATE BOUND ON NUMBER OF LEAVES:
---------------------------------
If each leaf requires a maximum (when only that leaf is put onchain) of 10,500 vbytes and the feerate is at least 2 satoshis / vbyte, then each leaf must be worth at least 21,000 satoshis (or else the dedicated user may not have an incentive to be honest, as the casual user would lose funds by putting their leaf onchain).
There are at most 2.1 * 10^15 satoshis in existence, so there can be at most 2.1 * 10^15 / 21,000 = 10^11 = 100B leaves.

I wrote a small python3 program for analyzing scalability given the requirement that all timeout-tree leaves can be put onchain.

The trickiest part was figuring out how to quantify the onchain fees caused by increasing the fraction of each block that's devoted to casual users putting their leaves onchain.
I wanted a function that multiplies the base feerate by a factor of 1 when no leaves are put onchain and by a factor approaching infinity when nearly all of the block space is devoted to leaves.
I started with the function Fe/(1-x), where Fe is the base feerate (without leaves put onchain) and x is the fraction of block space devoted to putting leaves onchain.
This function has the desired behavior when x is near 0 or 1, and it doubles the base feerate when half the block space is devoted to leaves.
In reality, the feerate probably increases faster than that, so I added an exponent to capture how quickly the feerate grows:

    feerate = Fe/(1-x)^Ex where Ex is an arbitrary exponent.

The program has the following tunable parameters:
* Ac: length (in blocks) of active lifetime of each TT (timeout-tree)
* Ro: length (in blocks) of rollover period of each TT (provides for casual user's unavailability)
* AS: average size (in vbytes) of transactions required to put one TT leaf onchain when all leaves in TT are put onchain
* MS: maximum size (in vbytes) of transactions required to put one TT leaf onchain when only one leaf in TT is put onchain
* Fe: feerate (in sats/vbyte) assuming 0% of block contains TT leaves
* Ex: exponent controlling rate of growth of feerates as TT leaves are added to blocks
* Pr: probability TTs are put on-chain
* Le: number of leaves of all TTs
* Va: value (in bitcoins) of all TT leaves put together, where each TT leaf has equal funds and during its active lifetime each leaf's funds are equally divided between:
        1) casual user's immediate bitcoin,
        2) casual user's Lightning balance, and
        3) dedicated user's Lightning balance
* Co: cost of capital (in fraction of funders' capital/year) for allocating the funders' capital to TTs

The program calculates the inactive lifetime (that is, the time for putting all timeout-tree leaves onchain) by minimizing the dedicated users' cost-of-capital plus the expected cost of putting leaves onchain.
In all cases, it takes the safe approach of making the inactive lifetime long enough for all leaves to be onchain before the timeout-tree expires.

There's a lot of guesswork in setting the parameters, but assuming the following values:
Ac: 110,000 blocks
Ro: 10,000 blocks
AS: 2,100 vbytes
MS: 10,500 vbytes
Fe: 10 sats/vbyte
Ex: 4.0 (so fees increase to 160 sats/vbyte if half the block space is devoted to TT leaves)
Pr: 0.01 (a 1% chance that the TTs will have to be put onchain)
Le: 100,000,000 leaves (channels)
Va: 10,000,000 BTC
Co: 0.01 (a 1% annual cost of capital for associating capital with a given casual user, while still using that capital to route unrelated payments)
results in devoting up to 0.65 of the blockspace for TT leaves, an inactive lifetime (SecurityDelay) of 1.55 years, and an expected overall cost (ExpectedOverheadFraction) of 0.025 (2.5%) of the casual user's funds.

The program and some sample inputs and outputs are on GitHub [2].
The parameter values shown above are in line 63 of the file in_tt_analysis01.csv and the results are in line 72 of the file out_tt_analysis01.xlsx.

Of course, there are other limits to scalability, such as the rate at which HTLCs timeout and have to be put onchain.
I just wanted to get a sense of when the trust/safety vs. capital efficiency tradeoff you identified becomes inevitable.

Regards,
John




Sent with Proton Mail secure email.



------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 28
********************************************
