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

   1. Announcing B'SST: Bitcoin-like Script Symbolic Tracer
      (Dmitry Petukhov)
   2. Re: Sentinel Chains: A Novel Two-Way Peg (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Wed, 30 Aug 2023 14:07:53 +0200
From: Dmitry Petukhov <dp@simplexum.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Announcing B'SST: Bitcoin-like Script Symbolic
	Tracer
Message-ID: <20230830140753.574d2ab9@simplexum.com>
Content-Type: text/plain; charset=US-ASCII

Hello list,

I have released B'SST: Bitcoin-like Script Symbolic Tracer

It can be found at https://github.com/dgpv/bsst

B'SST analyses Bitcoin and Elements scripts by symbolically executing
all possible execution paths, and tracking constraints that opcodes
impose on values they operate on. It then outputs a report based on
this analysis.

It can do analysis with the help of Z3 theorem prover [1]. With Z3
enabled, analysis will take more time, but all the features that depend
on SMT solver can be employed. By default, the analysis does not use
Z3, so it is fast, but not nearly as thorough.

Regarding the analysis performed, there are limitations and caveats.
Please refer to README.md in the repo at [0] for details.

I am aware of only one project that has aimed to do this type of
analysis before - the "SCRIPT Analyser" [2], but it had no updates in
its github repo for 5 years. Compared to [2], B'SST is more thorough in
its effort to match the reference interpreter closely, and it also uses
SMT solver, while [2] has used prolog for constraints solving.

Elements script interpreter [3], which is an extension of Bitcoin
script interpreter, was used as reference.

As an illustration of what information the analysis can provide, for
this rather contrieved example script:

7 ADD DUP 3 5 WITHIN
IF 0x00 ELSE 0 ENDIF
EQUALVERIFY 2DUP EQUALVERIFY SUB 0 EQUAL

The analysis report will show that:

- The first branch of IF will always fail
- Witness 0 must be -7 for script to succeed,
- Possible values for witness 1 and 2 are -1
- Result of last EQUAL is always true (because this condition was
  already checked by second EQUALVERIFY)

For more extensive example, please look at the report [5] for a rather
complex Elements script [4]

Plugins to implement custom opcodes are supported, please see "Custom
opcodes" section in README.md

B'SST is released under Prosperity Public License 3.0.0, which is a
"Free for non-commercial use" license, with a trial period for
commercial use and exemptions for educational institutions, public
research organizations, etc. Please refer to LICENSE.md file in the
repo at [0] for details.

[0] https://github.com/dgpv/bsst
[1] https://github.com/Z3Prover/z3
[2] https://github.com/RKlompUU/SCRIPTAnalyser
[3] https://github.com/ElementsProject/elements/blob/master/src/script/interpreter.cpp
[4] https://github.com/fuji-money/tapscripts/blob/with-annotations-for-bsst/beta/mint-mint.tapscript
[5] https://gist.github.com/dgpv/b57ecf4d9e3d0bfdcc2eb9147c9b9abf


------------------------------

Message: 2
Date: Thu, 31 Aug 2023 00:16:25 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: ryan@breen.xyz
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Sentinel Chains: A Novel Two-Way Peg
Message-ID:
	<1vNs5QDY6fY_t7bjbY_4gSaYHv0xxDuSkN3eFbW_qM8Q_1-Iwcf3u2AkG7JTQQ__9RxbnhDAI0A5TisV6e1pv_i4hDcj9AVKJZSnLxWu66E=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Ryan, et al.,

My long-ago interest in sidechains was the hope that they would be a scaling solution.

However, at some point I thought "the problem is that blockchains cannot scale, sidechains means MORE blockchains that cannot scale, what was I thinking???"
This is why I turned my attention to Lightning, which is a non-blockchain mechanism for scaling blockchains.

The only other reason for sidechains is to develop new features.

However, any actually useful features should at some point get onto the "real" Bitcoin.
In that case, a sidechain would "only" be useful as a proof-of-concept.
And in that case, a federated sidechain among people who can slap the back of the heads of each other in case of bad behavior would be sufficient to develop and prototype a feature.

--

In any case, if you want to consider a "user-activated" sidechain feature, you may be interested in an old idea, "mainstake", by some obscure random with an unpronouncable name: https://zmnscpxj.github.io/sidechain/mainstake/index.html

Here are some differences compared to e.g. drivechains:

* Mainchain miners cannot select the builder of the next sidechain block, without increasing their required work (possibly dropping them below profitability).
  More specifically:
  * If they want to select a minority (< 50%) sidechain block builder, then their difficulty increases by at least one additional bit.
    The number of bits added is basically the negative log2 of the share of the sidechain block builder they want to select.
  * The intent is to make it very much more unpalatable for a sidechain block builder to pay fees to the mainchain miner to get its version of the sidechain block confirmed.
    A minority sidechain block builder that wants to lie to the mainchain about a withdrawal will find that the fees necessary to convince a miner to select them are much higher than the total fees of a block.
    This better isolates sidechain conflicts away from mainchain miners.
* Miners can censor the addition of new mainstakes or the renewal of existing mainstakes.
  However, the same argument of censorship-resistance should still apply here (< 51% cannot reliably censor, and >=51% *can* censor but that creates an increasing feerate for censored transactions that encourages other potential miners to evict the censor).
  * In particular, miners cannot censor sidechain blocks easily (part of the isolation above), though they *can* censor new mainstakers that are attempting to evict mainstakers that are hostile to a sidechain.

There are still some similarities.
Essentially, all sidechain funds are custodied by a set of anonymous people.

One can consider as well that fund distribution is unlikely to be well-distributed, and thus it is possible that a small number of very large whales can simply take over some sidechain with small mainstakers and outright steal the funds in it, making them even richer.
(Consider how the linked write-up mentions "PoW change" much, much too often, I am embarassed for this foolish pseudonymous writer)

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 51
*******************************************
