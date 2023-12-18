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

   1. Lamport scheme (not signature) to economize on L1 (yurisvb@pm.me)
   2. Re: Addressing the possibility of profitable fee	manipulation
      attacks (alicexbt)


----------------------------------------------------------------------

Message: 1
Date: Mon, 18 Dec 2023 01:37:23 +0000
From: yurisvb@pm.me
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Lamport scheme (not signature) to economize on
	L1
Message-ID:
	<nvbG12_Si7DVx9JbnnAvZbNdWk7hDQA23W1TXMkfYoU2iBA95Z1HzRnXgyiwFhDBmdi_rWL0dPllX1M9N9YZPDV47VgYADNd7CQA9CkAuX0=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Dear colleagues,

After having mentioned it in?a Twitter Space?a few moments ago, I felt the need to share the idea with you even just as a draft. Utilizing?Lamport Scheme?(not?signature) for better byte-efficiency in L1:

1.  Have signing keys consist of the current ECC key AND a Lamport chain;
    

2.  For signing of a transaction, broadcast a tuple consisting of?

1.  the plain transaction,?
2.  hash of the previous Lamport chain concatenated to the transaction
3.  commitment signed by ECC freezing its UTXO and promising that in a few blocks time the pre image of hash will be published.

4.  a and b (but not c) are buried in coinbase session of a block B1 by miner M1;
5.  If upon maturity, such pre-image is not broadcasted, signed commitment is buried in the next block and executed. As a consequence, frozen UTXO pays B1 for a and b being buried at M1's coinbase?and?miner M2 for burying it [the commitment] in a block B2 subsequent to maturity;
6.  If pre-image is broadcasted before maturity, it is buried in another block B2', pays for itself, pays M1 for burying a adn b at B1 and pays whatever else was determined in the plain transaction of item 2.a.


The whole point is that, in the typical use case in which pre-image of hash is, in fact, successfully broadcasted before maturity, commitment, the only ECC signature in this protocol is discarded, and only two Lamport hashes end up being buried at L1.

To push economy even further, we could implement a memory-hard hash like Argon2 to do the same entropy-processing trade-off already utilized for passwords, so we could have hashes of, say 12 bytes, making it 24 in total, down from 136 from ECC.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/28462563/attachment.html>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/28462563/attachment.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/28462563/attachment.sig>

------------------------------

Message: 2
Date: Mon, 18 Dec 2023 06:26:28 +0000
From: alicexbt <alicexbt@protonmail.com>
To: ArmchairCryptologist <ArmchairCryptologist@protonmail.com>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Addressing the possibility of profitable
	fee	manipulation attacks
Message-ID:
	<XwBIMrHjY7N3DkEDVgxTHI3W3BRhijP7d4Lr7jUiR6E_fPxxPF0YyeKXwwsFiKBNjvM9NVSHrCwXwZhLr69hsYxVDkT_NUXzyN6NvQjM6FE=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi ArmchairCryptologist,

Bitcoin is working as expected and I don't see any 'manipulation' attacks in the bidding for block space. Maybe we aren't used to such demand for blockspace on bitcoin. Additionally, fingerprinting based on fee rates and timing to attribute transactions to a single person is inaccurate. Various services, such as unisat, are used for deploying and minting BRC20 tokens based on region, community etc. Consequently, a service broadcasting Bitcoin transactions might appear as a single individual.

With regards to UTXO set, IBD for machines with enough RAM seems to be unaffected, however I have not done benchmarking to compare IBD before and after inscriptions with less dbcache. Also the number of full nodes have increased in last one year.

> However, in practice, the attack appears to rely on exploiting the inherent decay used by fee estimation algorithms that are based on historical fee data. This causes many wallets to create transactions that overpay the necessarily next-block fee by a significant amount - for example, the morning after the 700 sat/vB flood on December 16th, Bitcoin Core was still giving a six-block estimate of 529 sat/vB even though <250 sat/vB transactions were being mined. 

Bitcoin Core fee estimation has known issues since years, and I would not recommended it for actual use, except for testing purposes.

Related discussion: https://github.com/bitcoin/bitcoin/issues/27995

> My proposed solution to this would be to add partial transaction fee burning. 

NACK

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

On Sunday, December 17th, 2023 at 11:11 AM, ArmchairCryptologist via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> ** Motivation **
> As everyone already knows, over the last seven months or so, the size of the mempool as well as transaction fees of on the bitcoin network have both been abnormally high. This tend has generally been ascribed to the introduction of ordinals, and while this may be both technically and actually true, disregarding the debate of whether ordinals is a "valid use" or the blockchain or not, the specific patterns we are seeing for some of these transactions have been making me somewhat suspicious that there could be other underlying motivations for this trend.
> 
> Crucially, as other people have noted, the dust UTXOs these ordinals transactions leave behind combined with the fact that consolidation transactions are being priced out due to persistent high fees is also causing the size of the UTXO set to blow up. As you can see on the chart below, on April 30 2023 there were roughly 90M UTXOs, while as of this writing roughly 7 months later, there are more than 140M. Practically, this means that over the course of the last year, the chainstate as stored by Bitcoin Core has increased from ~5GB to ~9GB.
> 
> See https://www.blockchain.com/explorer/charts/utxo-count - the 3Y chart makes the sudden change in the rate of increase very obvious. More than twice the number of UTXOs has been added in the last six months than in the preceding two and a half years.
> 
> While it is certainly not constant, if you watch the fee rates and timing of when transactions are broadcast using a live view of the mempool like mempool.space, you can see that especially during periods of low mempool influx like early mornings on weekends, there tends to be large bursts (often several hundred kvB worth) of tiny ordinals/BRC-20 transactions with a single dust UTXO broadcast right after each block is found, with a fee set moderately higher than the current average of the top of the mempool, which makes it highly likely that this is done by a single actor. There may of course be legitimate explanations for these patterns, like that they are simply taking advantage of the lower fees, but the impression they leave me is that they seem deliberately timed and priced to pad blocks during such periods to prevent the mempool from draining, under the guise of "minting" BRC-20 tokens.
> 
> For example, in the two-minute span between blocks #820562 and #820563 from Sunday December 10th, over a thousand of these transactions were broadcast:
> 
> https://mempool.space/block/000000000000000000015d5065ea2ade8bfd0bb9483835c907e34dd969854345
> https://mempool.space/block/000000000000000000001ae267367ade834627df7b119a2710091b3f5d8c1a88
> 
> Most of these transactions have been in the 30-60 sat/vB range, with occasional periods of increasingly higher-fee transactions going higher. The morning of Saturday December 16th is a good example of the latter, where there was an ~8 hour flood where the fees were pushed all the way up to 700 sat/vB. These are particularly suspicious, seeing as it would not make much sense to "take advantage of lower fees" by flooding transactions with fees increasingly and systematically set this much higher than the best next-block fee at this time of the week. There are many blocks during this period with noticeable large clusters of these high-fee BRC-20 transactions - for example, see #821428 and #821485:
> 
> https://mempool.space/block/000000000000000000011dd74372ff2d5fdec5e7431340a160b0304f3f145e82
> https://mempool.space/block/00000000000000000000653a2389a42549943c859e414f451f86944ac60b411b
> 
> You would think that if someone were in fact making a large volume of transactions specifically to inflate the transaction fees, they would eventually run out of funds to do so. In other words, considering how long this trend has been going on, they would either need to have exceptionally deep pockets, or directly profit from the transaction fees being high. This line of thought lead me to consider the possibility that such patterns could be indicative of ongoing fee manipulation by either a large miner or a consortium of miners, and whether such manipulation could be practically profitable, even with a minority hashrate. While miners have always had the ability to pad their own blocks with junk transactions, it seems to be generally assumed that at the very least there would be an opportunity cost of doing so, and that it would therefore would be unprofitable. The general ability to pad all blocks with junk transactions would of course both be much more severe and much less obviou
 s. So if this were the case, I believe it would break a fundamental assumption to the design of Bitcoin - seeing as transaction fees are central to prevent DoS attacks on the blockchain, if such an attack could be done in a way where both the base costs and opportunity costs are fully (or more than) recouped, we have a problem.
> 
> Just to be clear - I'm not saying with any certainty that such an attack is currently ongoing, has taken place in the past, or will take place in the future. Providing hard evidence of such would be difficult or impossible, so this should be considered pure conjecture based on circumstantial evidence. As such, seeing as conspiracy theories are generally unhelpful, I will ultimately only consider whether an attack such as this could be theoretically profitable. All the transactions observed may very well be "legit" in the sense that they have nothing to do with fee manipulation, but for the sake of argument we will run some numbers under the hypothesis that this is the ultimate goal, even if it is in fact coincidental.
> 
> 
> ** A short analysis, of the napkin kind **
> 
> Simply put, and trivially, such an attack would be profitable if the net fees the participating miners spend on fee-stuffing transactions is less than the increase in fees the participating miners can collect from "real" transactions.
> 
> The cost for carrying out the attack primarily has three factors: the ratio of participating miners, the ratio of fee-stuffing transactions required to maintain full blocks with a high fee level, and the per-transaction fees required for these.
> 
> The ratio of participating miners is important since it determines how much of the spent fees are lost to miners that do not participate in the attack. If 20% of the hashrate participates, on average 20% of blocks will be mined by these miners, recouping these fees. Which means the net amount of fees spent on the attack in this case is 80% of the gross fees spent on the creating these transactions - the remaining fraction of the fees would be collected by the honest miners instead.
> 
> Critically, this means that the higher the ratio of the hashrate is participating, the lower the cost of the attack. If 100% of miners participate with a ratio of transactions equal to their hashrate, the cost of the attack is zero, since every participating miner will get back on average 100% of the fees they contributed, and 0% of the fees will be lost to honest miners (of which there are none).
> 
> The ratio of fee-stuffing transactions required to maintain full blocks with a high fee level and their required fees would vary over time - weekends have fewer transactions, for example, and consistently high fees would likely reduce the number of people attempting to use the blockchain at all. Note however that in the degenerate case where all miners are participating, these two factors would be much less important, since all spent fees are recouped anyway, so it would only affect the absolute number of fees spent for real transactions.
> 
> 
> If all real transactions were fee-optimal, using low-balled fees based on the current mempool only and actively using fee bumping to barely squeak into a block, the total cost of the attack per block could be easily approximated as: (ratio of fee-stuffing transactions lost to honest miners) * (ratio of fee-stuffing transactions to real transactions) * (total block transaction fees)
> 
> However, in practice, the attack appears to rely on exploiting the inherent decay used by fee estimation algorithms that are based on historical fee data. This causes many wallets to create transactions that overpay the necessarily next-block fee by a significant amount - for example, the morning after the 700 sat/vB flood on December 16th, Bitcoin Core was still giving a six-block estimate of 529 sat/vB even though <250 sat/vB transactions were being mined. This means that the actual cost would likely be much lower. Seeing as this would be difficult to model, we would need to estimate the absolute cost to maintain a 100% block fillrate with high fees over time based on observations and some guesswork. Looking at the bursts of transactions we have seeing over the last few months during low-influx periods, most of them are in the 40-60 sat/vB range, so it seems reasonable to conclude that you can maintain this high fee level with transactions averaging ~50 sat/vB.
> 
> The increase in fees that can be collected from real transactions is also difficult to model. There is an opportunity cost for participating miners from mining their own fee-stuffing transactions instead of legitimate transactions, and it would depend greatly both on how many transactions are willing to outbid the fee-stuffing transactions at a particular fee level, the decay rate used by fee-estimation algorithms, as well as the cascading fee-related effects of blocks being full 100% of the time, leading to low-fee transactions never being mined. Due to the non-homogeneous nature of the ecosystem, estimating these factors individually would require a lot of (weak) assumptions, but we can make some higher-level estimates based on real-world data by comparing the fees collected from mined transactions today compared to fees collected a year ago.
> 
> See https://www.blockchain.com/explorer/charts/transaction-fees - if we use the 30D average, we were at around 20 BTC/day a year ago compared to around 150 BTC/day when this was written. With 144 blocks per day, this is approximately 0.14 BTC/block a year ago, and 1.05 BTC/block right now.
> 
> The gross profit for the attack would then simply be: ( (total average block transaction fees with attack) - (total average block transaction fees without attack) ) * (ratio of blocks mined by participating miners)
> 
> Using these numbers, the cost of a hypothetical attack would have to be on average less than 0.9 BTC per block mined by participating miners to be profitable.
> 
> So let's plug in some hypothetical numbers, using these assumptions together with the current real-world data under the hypothesis that such an attack is currently taking place, and that the current fee spike can be explained by it.
> 
> If we assume that 20% of miners participate in the attack and they need to fill on average 20% of each block (200 kvB) with an average transaction fee of 50 sat/vB to effectively maintain high fees:
> 
> The average cost per block would be 50 sat/vB * 200000 vB = 0.1 BTC
> 
> The gross profit would be 0.9 BTC * 0.2 = 0.18 BTC averaged per block
> 
> This gives a net profit of 0.18 BTC - 0.1 BTC = 0.08 BTC averaged per block
> 
> Which would result in an average daily net profit shared among the participating miners of 144 * 0.08 = 11.52 BTC, or around US$ 500K at today's price. (Non-participating miners would of course profit as well.)
> 
> Just to emphasize - the profits are averaged over all blocks mined on the network, not just the ones mined by participating miners, since the cost is incurred on every block regardless of who mines it. With these numbers, these participating miners would have a loss of 0.1 BTC per block they did not mine, and a gain of 0.8 BTC for every block they did mine, with 20% of the hashrate obviously averaging 1 in every 5 blocks - or somewhat restated, 4 * -0.1 + 0.8 = 5 * 0.08 = 0.4 BTC per 5 blocks.
> 
> If you keep the other hypothetical factors constant, the break-even numbers in this example would be an average fee-stuffing transaction fee of 90 sat/B, 11.1% participating miners, or 36% required fill rate.
> Observe also that miners would not have to actively coordinate or share funds in any way to participate. If a miner with 10% of the participating hashrate contributes 10% of the fee-stuffing transactions, they would also get back on average 10% of the total fees paid by transactions that are included in blocks mined by participating miners, giving them 10% of the profits. As such, each participating miner would simply have to watch the mempool to verify that the other participating miners are still broadcasting their agreed rate/ratio of transactions, the rest should average out over time.
> 
> In short, I believe this is a real problem. The premise of this analysis is based on conjecture and casual observation which is vulnerable to confirmation bias, and obviously cannot be considered proof that anything fishy is going on at present. However, regardless of the intent of these transactions, their existence and effect on the fee is obvious for everyone to see, so I feel relatively safe to conclude that under certain conditions where blocks are mostly full most of the time, a small-ish minority hashrate could potentially manipulate the network fees for a significant profit with no active coordination. As we are seeing, this would cause both unnecessarily high fees for people wanting to use the blockchain, and long-term issues with a bloated UTXO set that affects both fully archiving and pruning Bitcoin Core nodes as well as all other software that needs to keep a record of unspent transactions. In my opinion, it is necessary to address this.
> 
> 
> ** A possible solution, with some caveats **
> 
> My proposed solution to this would be to add partial transaction fee burning. If 50% or more of transaction fees were burned, this should effectively curtail any incentive miners have for padding blocks with junk transactions in general, as it would both significantly reduce the amount of spent fees they would be able to recoup, and also reduce the amount of benefit they gain from the transaction fees being high. The burn rate would however necessarily have to be less than 100%, otherwise miners would not be incentivized to include any transactions at all, and might as well be mining empty blocks.
> 
> While this change by itself could be implemented with a soft fork, miners would be (highly) unlikely to accept such a change, since it would directly reduce the profits even for honest miners. However, this solution could effectively complement arguments made by Peter Todd and others regarding the future of block subsidy, which in short go along the lines that block subsidy halvings should be stopped at some point with a hard fork, leaving a perpetual fixed subsidy per block. By itself this would arguably make Bitcoin into an inflationary currency, which many people object to, but if you combine it with partial fee burning, it could very well become deflationary instead depending on how the fee market develops, while still providing a guaranteed minimum reward per block. This would effectively alleviate the danger of a deficient fee market compromising the security of the blockchain due to low miner rewards at some point in the future, while only adding an "about" to the statement 
 "there will only ever be 21 million coins".
> 
> For example, if the collected fees in the year prior to such a hard fork being implemented were on average 1 BTC per block, and it was decided to burn 50% of the fees, the subsidy could be increased by a fixed 0.5 BTC which would not be affected by halvings. In other words, when the current subsidy starts approaching zero, we would be left with a perpetual static subsidy of 0.5 BTC and change per block, without drastically affecting the total coin supply. Worst case, if fees collapsed entirely we would have an inflation of ~0.1% per year?(0.5 BTC/block * 144 blocks/day * 365 days/year = 26280 BTC/year) not taking permanently lost coins into account, while on the other hand, if fees went higher still then the deflation would not have a fixed limit, unless an absolute limit for burned fees per block was added.
> 
> 
> I did briefly consider the possibility of doing this with a soft fork instead, where the "burned" fees were instead transferred into a special "subsidy fund address" that would be drawn from by miners to effectively increase the block subsidy, but seeing as this would not remove the correlation between intentionally inflating fees and increasing miner rewards, I don't believe this would actually address this attack. For the same reason, adding a dynamic subsidy based on historic fee rates would have the same problem, so it would necessarily have to be a fixed additional subsidy.
> 
> It is important to emphasize that if the goal is to fully address this type of miner attack in general, increasing the blocksize would NOT be a viable solution by itself. If the blocksize increase is large enough and the fraction of participating miners is low enough, then yes, it would probably thwart it, but if the majority (or all) miners participated, it would have little (or no) effect unless the blocksize was unbounded, which does not seem like a good idea. While the absolute amount of fees the miners would need to spend for fee stuffing would of course increase, the fraction of spent fees miners would recoup would not change, so if 100% of miners participated, 100% of fees used in the attack would still be recouped regardless of the absolute number of transactions it would take to fill a block. Furthermore, the absolute number of transactions willing to outbid them would not change, so the extra fees gathered from the attack would remain the same as well.
> 
> Additionally, if the attack continued, the rate of increase of the size of the UTXO set would likely increase by a similar factor as the blocksize increase. As such, any blocksize increase at all would in my opinion necessarily have to be combined with partial fee burning - possibly dynamic, based on the size of each block - to prevent exacerbating potential attacks that excessively and unnecessarily bloat the size of the UTXO set. It would however be natural add a modest and scaling increase as part of the same fork, seeing as the fee burning change would resolve the main argument against it, since adding data to the blockchain would now always have a guaranteed cost even for miners.
> 
> Changing fee estimation algorithms across the board to not take historical fee data into account, eliminating the long-term decaying fee effects observed after short-term flooding of high-fee transactions, would of course significantly help prevent such attacks from being profitable in the first place without requiring any sort of fork. As such, I believe this should also be done as a short-term makeshift solution. A less exploitable estimate could be made by limiting the algorithms to only use the current mempool state and influx rate, as well as possibly the estimated current blockrate and the arrival times of recent blocks. Additionally, wallets could pre-sign a number of replacement transactions spending the same UTXO(s) with gradually increasing fees up to a maximum specified by the user, and automatically broadcast them in order as the state of the mempool changed. And I'm sure there are additional strategies that could be used here as well to make the ecosystem more fee-opti
 mal in general.
> 
> 
> 
> Unfortunately, as long as some parties still use historic fee data for their fee estimation, the attack could still be effective up to a point. Payment providers like BitPay for example currently specify that you need to use a historically high fee for the initial transaction for it to be accepted, and does not recognize replacement transactions that bump the fee.
> 
> 
> If you made it this far, thanks for reading my wall. Please let me know if you find any serious mistakes in my assumptions and/or math that invalidate the whole premise, so I can stop thinking about it.
> 
> --
> Sincerely,
> ArmchairCryptologist


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 13
********************************************
