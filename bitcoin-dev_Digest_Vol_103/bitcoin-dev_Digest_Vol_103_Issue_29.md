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

   1. Re: Lamport scheme (not signature) to economize on L1
      (yurisvb@pm.me)
   2. Re: Scaling Lightning Safely With Feerate-Dependent	Timelocks
      (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Fri, 29 Dec 2023 00:30:30 +0000
From: yurisvb@pm.me
To: "G. Andrew Stone" <g.andrew.stone@gmail.com>, Nagaev Boris
	<bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<EKvQwk6gu1g35fnG_QC8zeX6QR9Vr6u3vXqRsbBS1imvt8GgfMP-9lOqFjNG6gWFSVJdmbsFyZ2vL8PhwxRc94EXSNZMEWRDt429S_uWuOE=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Dear all,

Upon a few more days working on my proposed protocol, I've found a way to waive the need for:
1) mining the conventional public key;
2) user broadcasting 2 distinct payloads a few blocks apart;

Up to 66% footprint reduction.

I'll be publishing and submitting it as BIP soon. Those who got interested are more than welcome to get in touch directly.

It's based on my proposed cryptosystem based on the conjectured hardness of factorization of polynomials in finite fields:
https://github.com/Yuri-SVB/FFM-cryptography/

YSVB

Sent with Proton Mail secure email.

On Saturday, December 23rd, 2023 at 1:26 AM, yurisvb@pm.me <yurisvb@pm.me> wrote:


> Dear all,
> 

> Upon second thoughts, I concluded have to issue a correction on my last correspondence. Where I wrote:
> 

> > For 2: a pre-image problem for a function
> > f2_(TX,ECCPUB): {l | l is 'a valid LAMPPRI'} -> {a | a is 'in the format of ADDRs'} X {LSIG}
> > 

> > (notice the nuance: {LSIG} means the singleton containing of only the specific LSIG that was actually public, not 'in the format of LSIGs').
> 

> 

> Please read
> 

> "For 2: a pre-image problem for a function
> f2_(TX,ECCPUB): {l | l is 'a valid LAMPPRI'} -> {a | a is 'in the format of ADDRs'} X {s | s is 'in the format of LSIGs'}"
> 

> 

> instead, and completely disregard the nuance below, which is wrong. I apologize for the mistake, and hope I have made myself clear. Thank you, again for your interest, and I'll be back with formulas for entropy in both cases soon!
> 

> YSVB
> 

> Sent with Proton Mail secure email.
> 

> 

> On Friday, December 22nd, 2023 at 4:32 PM, yurisvb@pm.me yurisvb@pm.me wrote:
> 

> 

> 

> > There are three possible cryptanalysis to LAMPPRI in my scheme:
> > 

> > 1. From ADDR alone before T0-1 (to be precise, publishing of (TX, SIG));
> > 2. From ADDR and (TX, SIG) after T0-1 (to be precise, publishing of (TX, SIG));
> > 3. Outmine the rest of mining community starting from a disadvantage of not less than (T1-T0-1) after T1 (to be precise, at time of publishing of LAMPRI);
> > 

> > ...which bring us back to my argument with Boris: There is something else we missed in our considerations, which you said yourself: ironically, LAMPPUB is never published.
> > 

> > We can have LAMPPUB be 1Mb or even 1Gb long aiming at having rate of collision in HL(.) be negligible (note this is perfectly adherent to the proposition of memory-hard-hash, and would have the additional benefit of allowing processing-storage trade-off). In this case, we really have:
> > 

> > For 1: a pre-image problem for a function
> > f1: {k| k is a valid ECCPRI} X {l | l is a valid LAMPPRI} -> {a | a is in the format of a ADDR}
> > 

> > having as domain the Cartesian product of set of possible ECCPRIs with set of possible LAMPPRIs and counter domain, the set of possible ADDRs.
> > 

> > For 2: a pre-image problem for a function
> > f2_(TX,ECCPUB): {l | l is 'a valid LAMPPRI'} -> {a | a is 'in the format of ADDRs'} X {LSIG}
> > 

> > (notice the nuance: {LSIG} means the singleton containing of only the specific LSIG that was actually public, not 'in the format of LSIGs').
> > 

> > Notice that, whatever advantage of 2 over 1 has to be compensated by the perspective of having the protocol be successfully terminated before the attack being carried out.
> > 

> > For 3: Equivalente of a double-spending attack with, in the worst case, not less than (T1-T0-1) blocks in advantage for the rest of the community.
> > 

> > When I have the time, I'll do the math on what is the entropy on each case, assuming ideal hashes, but taking for granted the approximation given by Boris, we would have half of size of ADDR as strength, not half of LAMPPRI, so mission accomplished!
> > 

> > Another ramification of that is we can conceive a multi-use version of this scheme, in which LAMPPRI is the ADDR resulting of a previous (ECCPUB, LAMPPUB) pair. The increased size of LAMPPRI would be compensated by one entire ADDR less in the blockchain. Namely, we'd have an extra marginal reduction of 12 bytes per use (possibly more, depending on how much more bytes we can economize given that added strength).
> > 

> > YSVB.
> > 

> > On Friday, December 22nd, 2023 at 5:52 AM, G. Andrew Stone g.andrew.stone@gmail.com wrote:
> > 

> > > Does this affect the security model WRT chain reorganizations? In the classic doublespend attack, an attacker can only redirect UTXOs that they spent. With this proposal, if I understand it correctly, an attacker could redirect all funds that have "matured" (revealed the previous preimage in the hash chain) to themselves. The # blocks to maturity in your proposal becomes the classic "embargo period" and every coin spent by anyone between the fork point and the maturity depth is available to the attacker to doublespend?
> > > 

> > > On Thu, Dec 21, 2023, 8:05?PM Yuri S VB via bitcoin-dev bitcoin-dev@lists.linuxfoundation.org wrote:
> > > 

> > > > You are right to point out that my proposal was lacking defense against rainbow-table, because there is a simple solution for it:
> > > > To take nonces from recent blocks, say, T0-6, ..., T0-13, for salting LSIG, and ECCPUB to salt LAMPPUB. Salts don't need to be secret, only unknown by the builder of rainbow table while they made it, which is the case, since here we have 8*32=256 bits for LSIG, and the entropy of ECCPUB in the second.
> > > > 

> > > > With rainbow table out of our way, there is only brute-force analysis to mind. Honestly, Guess I should find a less 'outrageously generous' upper bound for adversary's model, than just assume they have a magic wand to convert SHA256 ASICS into CPU with the same hashrate for memory- and serial-work-hard hashes (therefore giving away hash hardness). That's because with such 'magic wand' many mining pools would, not only be capable of cracking 2^48 hashes far within the protocol's prescribed 48 hours, but also 2^64 within a block time, which would invalidate a lot of what is still in use today.
> > > > 

> > > > Please, allow me a few days to think that through.
> > > > 

> > > > YSVB
> > > > 

> > > > Sent with Proton Mail secure email.
> > > > 

> > > > On Wednesday, December 20th, 2023 at 10:33 PM, Nagaev Boris bnagaev@gmail.com wrote:
> > > > 

> > > > > On Tue, Dec 19, 2023 at 6:22?PM yurisvb@pm.me wrote:
> > > > > 

> > > > > > Thank you for putting yourself through the working of carefully analyzing my proposition, Boris!
> > > > > > 

> > > > > > 1) My demonstration concludes 12 bytes is still a very conservative figure for the hashes. I'm not sure where did you get the 14 bytes figure. This is 2*(14-12) = 4 bytes less.
> > > > > 

> > > > > I agree. It should have been 12.
> > > > > 

> > > > > > 2) Thank you for pointing out that ECCPUB is necessary. That's exactly right and I failed to realize that. To lessen the exposure, and the risk of miner of LSIG, it can be left to be broadcast together with LAMPPRI.
> > > > > > 

> > > > > > 3) I avail to advocate for economizing down the fingerprint to just 128 bits for the weakest-link-principle, since 128 bits is a nearly ubiquitous standard, employed even by the majority of seeds. Not an argument against plain Schnorr, because Schnorr keys could use it too, but, compared with current implementations, we have that would be 20-16=4 bytes less.
> > > > > 

> > > > > I think that the digest size for hash should be 2x key size for
> > > > > symmetric encryption. To find a collision (= break) for a hash
> > > > > function with digest size 128 bits one needs to calculate ~ 2^64
> > > > > hashes because of the birthday paradox.
> > > > > 

> > > > > > 4) [Again, argument against plain, because it cuts for both sides:] To economize even further, there is also the entropy-derivation cost trade-off of N times costlier derivation for log2(N) less bits. If applied to the Address, we could shave away another byte.
> > > > > > 

> > > > > > 5) T0 is just the block height of burying of LSIG doesn't need to be buried. T2 can perfectly be hard-coded to always be the block equivalent of T0 + 48 hours (a reasonable spam to prevent innocent defaulting on commitment due to network unavailability). T1 is any value such as T0 < T1 < T2, (typically T1 <= T0+6) of user's choosing, to compromise between, on one hand, the convenience of unfreezing UTXO and having TX mining completed ASAP and, on the other, avoiding the risk of blockchain forking causing LAMPPRI to be accidentally leaked in the same block height as LSIG, which allows for signatures to be forged. So this is 16 bytes less.
> > > > > > 

> > > > > > Miners would keep record of unconfirmed BL's, because of the reward of mining either possible outcome of it (successful transaction or execution of commitment). Everything is paid for.
> > > > > > 

> > > > > > So, unless I'm forgetting something else, all other variables kept equal, we have 20 bytes lighter than Schnorr; and up to 25 bytes less the current implementation of Schnorr, if items 3 and 4 are implemented too. Already we have a reduction of between 21% and 26%, while, so far, nobody in the mailing list has disputed how 'outrageously' conservative the 12 bytes figure is.
> > > > > 

> > > > > 26% reduction of block space utilization would be great, but the price
> > > > > of relying on 12 bytes hashes (only need 2^48 hashes to find a
> > > > > collision) is too much for that, IMHO.
> > > > > 

> > > > > Another consideration is about 12 byte hashes. Let's try to figure out
> > > > > if they are resistant to rainbow table attack by a large organization.
> > > > > Let's assume that the rainbow table has a chain length of 1024^3 (billion).
> > > > > What storage size is needed? 2^96 * 12 / 1024^3 = 900 exabytes.
> > > > > Both chain length and storage size seems prohibitively high for today,
> > > > > but tomorrow the hash function can be optimized, memory can be
> > > > > optimized, storage can become cheaper etc. And this attack may be
> > > > > affordable for state level attackers.
> > > > > 

> > > > > > Any other objections?
> > > > > > 

> > > > > > YSVB
> > > > > 

> > > > > --
> > > > > Best regards,
> > > > > Boris Nagaev_______________________________________________
> > > > > bitcoin-dev mailing list
> > > > > bitcoin-dev@lists.linuxfoundation.org
> > > > > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231229/619987ee/attachment-0001.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231229/619987ee/attachment-0001.sig>

------------------------------

Message: 2
Date: Thu, 28 Dec 2023 18:06:00 +0000
From: jlspc <jlspc@protonmail.com>
To: Nagaev Boris <bnagaev@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent	Timelocks
Message-ID:
	<IhmJ-631z02S9ZjKb4VtaqVWa_W9U0s1Tnn2fhhGGMlXPUD4r5E08UX-N0iYaXTAk4s_90pemkdCRurPZIQjT9WE9gQSHPKbdpcn4aN_-Vs=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Boris,

Responses inline below:


Sent with Proton Mail secure email.

On Friday, December 22nd, 2023 at 8:36 AM, Nagaev Boris <bnagaev@gmail.com> wrote:


> Hi John!
> 
> I have two questions regarding the window, which are related.
> 
> 1. Why is the window aligned? IIUC, this means that the blocks mined
> since the latest block whose height is divisible by window_size do not
> affect transaction's validity. So a recent change of fees does not
> reflect if a transaction can be confirmed.

FDTs are not based on the most recent window; instead, an FDT requires that there exist *some* aligned window between when the child transaction's absolute and relative timelocks were satisfied and the current block. The alignment requirement allows one to prove tighter security bounds over a given time period. For example, 2 consecutive aligned 64-block windows give dishonest miners 2 chances to create artificial aligned low-feerate windows, but 65 chances to create such windows if alignment isn't required.

> 
> 2. Does it make sense to have a global window_size? This would save
> space in FDT (= in transaction) and simplify verification, especially
> for a non-aligned window case (see 1). An array of integers of size
> window_size would be sufficient to give answer to a question if there
> were at least x blocks among window_size latest blocks with median fee
> rate <= y, using O(1) time per query.
> 

The ability to tune the window size allows for a trade-off between latency and security (also, see my response above about alignment). 

> Moving on to another topic, what are the implications for light
> clients? A light client can validate current timelocks without
> downloading whole blocks, because they depend on timestamps and block
> height only, the information from block headers. To validate a
> transaction with FDT or to choose FDT parameters for its own
> transaction, a light client would have to determine the median fee
> rate of the recent blocks. To do that without involving trust, it has
> to download the blocks. What do you think about including median
> feerate as a required OP_RETURN output in coinbase transaction? A
> block without it would be invalid (new consensus rule). A light client
> can rely on median feerate value from coinbase transaction,
> downloading only one tx instead of the whole block.

Yes, I think that's a great idea!

Regards,
John

> 
> On Fri, Dec 15, 2023 at 6:20?AM jlspc via bitcoin-dev
> bitcoin-dev@lists.linuxfoundation.org wrote:
> 
> > TL;DR
> > =====
> > * All known Lightning channel and factory protocols are susceptible to forced expiration spam attacks, in which an attacker floods the blockchain with transactions in order to prevent honest users from putting their transactions onchain before timelocks expire.
> > * Feerate-Dependent Timelocks (FDTs) are timelocks that automatically extend when blockchain feerates spike.
> > - In the normal case, there's no spike in feerates and thus no tradeoff between capital efficiency and safety.
> > - If a dishonest user attempts a forced expiration spam attack, feerates increase and FDTs are extended, thus penalizing the attacker by keeping their capital timelocked for longer.
> > - FDTs are tunable and can be made to be highly resistant to attacks from dishonest miners.
> > * Of separate interest, an exact analysis of the risk of double spend attacks is presented that corrects an error in the original Bitcoin whitepaper.
> > 
> > Overview
> > ========
> > 
> > Because the Lightning protocol relies on timelocks to establish the correct channel state, Lightning users could lose their funds if they're unable to put their transactions onchain quickly enough.
> > The original Lightning paper [1] states that "[f]orced expiration of many transactions may be the greatest systemic risk when using the Lightning Network" and it uses the term "forced expiration spam" for an attack in which a malicious party "creates many channels and forces them all to expire at once", thus allowing timelocked transactions to become valid.
> > That paper also says that the creation of a credible threat against "spamming the blockchain to encourage transactions to timeout" is "imperative" [1].
> > 
> > Channel factories that create multiple Lightning channels with a single onchain transaction [2][3][4][5] increase this risk in two ways.
> > First, factories allow more channels to be created, thus increasing the potential for many channels to require onchain transactions at the same time.
> > Second, channel factories themselves use timelocks, and thus are vulnerable to a "forced expiration spam" attack.
> > 
> > In fact, the timelocks in Lightning channels and factories are risky even without an attack from a malicious party.
> > Blockchain congestion is highly variable and new applications (such as ordinals) can cause a sudden spike in congestion at any time.
> > As a result, timelocks that were set when congestion was low can be too short when congestion spikes.
> > Even worse, a spike in congestion could be self-reinforcing if it causes malicious parties to attack opportunistically and honest parties to put their channels onchain due to the heightened risk.
> > 
> > One way to reduce the risk of a forced expiration spam attack is to use longer timelocks that give honest users more time to put their transactions onchain.
> > However, long timelocks limit the ability to dynamically reassign the channel's (or factory's) funds, thus creating a tradeoff between capital efficiency and safety [6].
> > While long timelocks could maintain safety for small numbers of channels, supporting billions (or tens of billions) of channels while maintaining safety is probably impossible [7].
> > 
> > Another way to reduce risk is to impose a penalty on an attacker.
> > Some channel protocols, such as the original Lightning protocol [1], a version of the two-party eltoo protocol [8], the fully-factory-optimized protocol [9], and the tunable-penalty channel protocol [10] include such penalties.
> > In addition, the tunable-penalty and single-commitment factory protocols [4] support penalties.
> > However, as was noted in the original Lightning paper [1], penalties don't eliminate the risk of a forced expiration spam attack.
> > Furthermore, existing penalty-based factory protocols [4] have limited scalability, as they depend on getting large numbers of casual users to coordinate and co-sign transactions [11][5].
> > 
> > In contrast, the timeout-tree protocol [5] scales via simple covenants (enabled by support for CheckTemplateVerify, AnyPrevOut, or a similar change to the Bitcoin consensus rules).
> > As a result, a single timeout-tree can support millions of channels and one small transaction per block can fund timeout-trees with tens of billions of offchain channels [5].
> > However, timeout-trees don't support penalties, and like all other known factory protocols [2][3][4], timeout-trees rely on timelocks.
> > 
> > Therefore, if the need to protect against forced expiration spam was already "imperative" for the original Lightning channel protocol [1], the use of scalable channel factories will make such protection indispensable.
> > 
> > This post proposes a change to Bitcoin's consensus rules that allows the length of a timelock to depend on the feerate being charged for putting transactions onchain.
> > Such Feerate-Dependent Timelocks (FDTs) can be used to make the above channel and factory protocols resistant to sudden spikes in blockchain congestion.
> > In the normal case, when there's no spike in congestion, FDTs don't extend the lengths of timelocks and thus don't create a tradeoff between capital efficiency and safety.
> > On the other hand, when congestion spikes, FDTs extend the lengths of timelocks and thus penalize the owner of the timelocked capital by reducing its efficiency.
> > Therefore, FDTs can be viewed as creating a penalty for spamming the blockchain, thus reducing the likelihood of such an attack even if the channel (or factory) protocol being used doesn't have an explicit penalty mechanism.
> > 
> > FDTs have other uses, including reducing the risk of having to pay unexpectedly high fees during a congestion spike, improving the accuracy of fee-penalties [5] and reducing the risk of one-shot receives [12].
> > 
> > Of separate interest, the analysis of FDTs given here leads to an exact analysis of the risk of double spend attacks that corrects an error in the original Bitcoin whitepaper [13].
> > 
> > A more complete description and analysis of FDTs is given in a paper [14].
> > 
> > Feerate-Dependent Timelock (FDT) Proposal
> > =========================================
> > 
> > A Feerate-Dependent Timelock (FDT) is created by encoding a feerate upper bound in a transaction's nSequence field.
> > A transaction with an FDT cannot be put onchain until:
> > 1) its absolute timelock encoded in its nLocktime field (and its relative timelock encoded in the same nSequence field, if present) has been satisfied, and
> > 2) the prevailing feerate has fallen below the FDT's feerate upper bound.
> > As a result, FDTs are automatically extended when the feerate for putting transactions onchain spikes (such as would occur during a forced expiration spam attack).
> > 
> > In order to determine the prevailing feerate, the median feerate of each block is calculated as the feerate (in satoshis/vbyte) that is paid for at least half of the block's vbytes.
> > 
> > If all miners were honest, a single block with a low median feerate would be enough to guarantee that congestion is low.
> > However, even a small fraction of dishonest miners would be able to occasionally mine a block with an artificially low feerate.
> > As a result, it isn't safe to wait for one block (or some other fixed number of blocks) with a low feerate in order to guarantee that honest users have had an opportunity to put their transactions onchain.
> > 
> > Instead, an FDT requires that some maximum number of blocks within an aligned window of consecutive blocks have a high median feerate.
> > The FDT proposal uses 14 currently masked-off bits in the nSequence field to express the FDT's three parameters:
> > * feerate_value,
> > * window_size, and
> > * block_count.
> > An aligned window of window_size blocks satisfies the FDT's parameters if it has fewer than block_count blocks with median feerate above feerate_value.
> > A transaction with an FDT can only be put onchain after an aligned window that satisfies the FDT's parameters and starts no earlier than when the transaction's absolute timelock (and corresponding relative timelock, if present) is satisfied.
> > 
> > In addition, the CheckSequenceVerify (CSV) operator is extended to enforce the desired feerate_value, window_size and block_count.
> > The details are given in the paper [14].
> > 
> > Safe Lightning Channels And Factories
> > =====================================
> > 
> > In order to protect a channel or factory protocol against forced expiration spam attacks, the protocol's timelocks are made to be feerate-dependent.
> > This is done by selecting a feerate_value (such as 4 times the current feerate) that would be caused by a forced expiration spam attack, along with the desired window_size and block_count parameters.
> > 
> > It's also possible to create multiple conflicting transactions with different FDTs (with later timelocks allowing higher feerates) in order to avoid timelocks that will never expire if feerates remain high permanently.
> > 
> > Other Uses
> > ==========
> > 
> > FDTs have uses in addition to protecting channel and factory protocols from forced expiration spam attacks.
> > 
> > For example, FDTs can protect users that are racing against timelocks from having to pay an unexpectedly high feerate due to temporary feerate fluctuations [14].
> > In addition, FDTs can be used to improve the accuracy of fee-penalties that are assessed when a casual user puts their timeout-tree leaf onchain [14](Section 4.10 of [5]).
> > Finally, FDTs can be used to allow a casual user to submit a transaction to the blockchain without having to then monitor the blockchain for a sudden spike in feerates, thus reducing the risk of one-shot receives [14][12].
> > 
> > Analysis
> > ========
> > 
> > FDT Implementation Cost
> > -----------------------
> > In order to verify an FDT, nodes have to determine whether or not there is an aligned window with a sufficient number of low-feerate blocks after the FDT's absolute timelock (and corresponding relative timelock, if present) is satisfied.
> > Therefore, if a node knows the starting block of the most recent aligned window that satisfies the FDT's feerate_value, window_size, and block_count parameters, the node can compare that starting block with the FDT's timelocks to verify the FDT.
> > Because the FDT parameters can be expressed using 14 bits, nodes only have to keep track of the starting block for 2^14 = 16k different low-feerate windows.
> > The starting block for each such window can be stored in 4 bytes, so 16k * 4B = 64kB of memory allows a node to verify an FDT in constant time.
> > (In practice, slightly more memory could be used in order to accommodate a reordering of the most recent 1k blocks.)
> > Therefore, DRAM that costs less than one cent, plus a small constant number of computations, suffice to verify an FDT.
> > 
> > FDT Dishonest Miner Attacks
> > ---------------------------
> > The window_size and block_count parameters can be selected to balance between:
> > 1) latency,
> > 2) the feerate paid by honest users, and
> > 3) security against dishonest miners.
> > At one extreme, if dishonest miners are of no concern, window_size and block_count can be set to 1, so the FDT can be satisfied when the first block with a sufficiently low feerate is mined.
> > At the other extreme, if dishonest miners are of great concern, window_size can be set to 16k and block_count can be set to 1024, in which case dishonest miners with 45% of the hashpower would have less than a 10^-33 chance of dishonestly mining enough blocks in a given window to satisfy the FDT prior to the honest users being able to get their transactions onchain [14].
> > 
> > Double Spend Attacks
> > --------------------
> > While it's unrelated to FDTs, the analysis of FDTs' resistance to dishonest miner attacks can also be used to analyze the risk of double spend attacks.
> > 
> > The original Bitcoin whitepaper [13] includes an analysis of the probability of a double spend attack in which a dishonest party colludes with dishonest miners in order to undo a bitcoin transaction and steal the goods purchased with that transaction.
> > That analysis correctly shows that the probability of success of a double spend attack falls exponentially with z, the depth of the transaction that's being double spent.
> > However, there are two problems with that analysis:
> > 1) it is approximate, and
> > 2) it ignores the possibility of the dishonest miners using pre-mining.
> > 
> > The first problem was addressed by Grunspan and Perez-Marco [15].
> > However, it doesn't appear that the second problem has been addressed previously.
> > 
> > Exact formulas for the risk of double spend attacks, including pre-mining, are given in the paper [14] and programs that implement those formulas are available on GitHub [16].
> > 
> > The effect of including pre-mining only becomes apparent when a large fraction of the miners are dishonest.
> > For example, Nakamoto estimates the required value of z to guarantee at most a 0.1% chance of a successful double spend, and Grunspan and Perez-Marco give exact values assuming no pre-mining.
> > Those results, plus exact results with pre-mining, are as follows:
> > 
> > % dishonest Estimated z w/o Exact z w/o Exact z w/
> > miners pre-mining [13] pre-mining [15] pre-mining [14]
> > =========== =============== =============== ===============
> > 10 5 6 6
> > 15 8 9 9
> > 20 11 13 13
> > 25 15 20 20
> > 30 24 32 33
> > 35 41 58 62
> > 40 89 133 144
> > 45 340 539 589
> > 
> > It's important to note that the above results with pre-mining assume that the time of the double spend attack is not selected by the attacker.
> > If the attacker can select when to perform the attack, they are guaranteed to succeed given any value of z, but the expected time required to perform the attack grows exponentially with z [14].
> > 
> > Conclusions
> > ===========
> > 
> > Securing Lightning channels and channel factories against forced expiration spam attacks is imperative.
> > 
> > Feerate-Dependent Timelocks (FDTs) provide this security without forcing the timelocks to be extended in the typical case, thus avoiding a capital efficiency vs. safety tradeoff.
> > Furthermore, a dishonest user who tries to use a forced expiration spam attack to steal funds is penalized by having their funds timelocked for a longer period, thus discouraging such attacks.
> > Finally, FDTs can be made to be highly resistant to attacks by dishonest miners.
> > 
> > FDTs have other uses, including the reduction of feerate risk and the calculation of fee-penalties.
> > 
> > While implementing FDTs requires some additional DRAM and computation, the costs are extremely small.
> > Given these advantages and their low costs, it's hoped that the Bitcoin consensus rules will be changed to support FDTs.
> > 
> > Regards,
> > John
> > 
> > [1] Poon and Dryja, The Bitcoin Lightning Network, https://lightning.network/lightning-network-paper.pdf
> > [2] Burchert, Decker and Wattenhofer, "Scalable Funding of Bitcoin Micropayment Channel Networks", http://dx.doi.org/10.1098/rsos.180089
> > [3] Decker, Russell and Osuntokun. "eltoo: A Simple Layer2 Protocol for Bitcoin", https://blockstream.com/eltoo.pdf
> > [4] Law, "Efficient Factories For Lightning Channels", https://github.com/JohnLaw2/ln-efficient-factories
> > [5] Law, "Scaling Lightning With Simple Covenants", https://github.com/JohnLaw2/ln-scaling-covenants
> > [6] Towns, "Re: Scaling Lightning With Simple Covenants", https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-September/021943.html
> > [7] Law, "Re: Scaling Lightning With Simple Covenants", https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-November/022175.html
> > [8] Towns, "Two-party eltoo w/ punishment", https://lists.linuxfoundation.org/pipermail/lightning-dev/2022-December/003788.html
> > [9] Law, "Factory-Optimized Channel Protocols For Lightning", https://github.com/JohnLaw2/ln-factory-optimized
> > [10] Law, "Lightning Channels With Tunable Penalties", https://github.com/JohnLaw2/ln-tunable-penalties
> > [11] Riard, "Solving CoinPool high-interactivity issue with cut-through update of Taproot leaves", https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-September/021969.html
> > [12] Law, "Watchtower-Free Lightning Channels For Casual Users", https://github.com/JohnLaw2/ln-watchtower-free
> > [13] Nakamoto. "Bitcoin: A Peer-to-Peer Electronic Cash System", http://bitcoin.org/bitcoin.pdf
> > [14] Law, "Scaling Lightning Safely With Feerate-Dependent Timelocks", https://github.com/JohnLaw2/ln-fdts
> > [15] Grunspan and Perez-Marco, "Double Spend Races", CoRR, vol. abs/1702.02867, http://arxiv.org/abs/1702.02867v3
> > [16] Law, https://github.com/JohnLaw2/ln-fdts
> > 
> > Sent with Proton Mail secure email.
> > 
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> 
> 
> 
> 
> --
> Best regards,
> Boris Nagaev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 29
********************************************
