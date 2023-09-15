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

   1. Re: Concrete MATT opcodes (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Wed, 13 Sep 2023 21:25:07 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: symphonicbtc <symphonicbtc@proton.me>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Concrete MATT opcodes
Message-ID:
	<CALZpt+Ha5fWoLyf_gn1Q9FChxuOM3EgiCy76LACS-p7tQva-Bw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Symphonic,

I'm not aware of any theory of the "mining firm" (in the coasian sense)
that would give the lineaments of the cost / income structure of a lambda
mining operation, and from which to predict how a change in the withhold
mined coins impact the long-term sustainability of their business,
especially incorporating relationships with electricity providers and
mining chips makers.

On the impact of disregarding OFAC sanctioned txs, this sounds correct that
as long as this is a minority of economic transactions that a mining
operation can censor, they can afford to stay in business and not lose
long-term blockspace issuance. If the regulation enforcement cost starts to
be too high, they can move to a jurisdiction where regulation costs are
lower [0].

This is indeed a good remark that is unclear if additional constructs and
smart contracts would incentive block-reorgs or transactions censoring
attitudes, or even if we would see "lightning-bounty" transactions
constructs happening generating an economic equilibrium between censorship
and confirmation. I think this is an area deserving more research for sure.

This is unclear if reduction of the timewarp attack too could modify the
miners incentives equilibrium [1].

In the end I can only agree that miners and full-nodes operators incentives
should be a built-in protection in case of consensus upgrades substantially
altering the Bitcoin deep security model. The thing is this model is very
unclear to the best of my knowledge and I don't think anyone has taken time
to formalize it from the years of blocksize wars from then to analyze
carefully proposed covenant upgrades.

Best,
Antoine

[0] Side-note and IANA disclaimer. On the application to US OFAC by Bitcoin
economic entities operators, there is a huge uncertainty if naive
application of OFAC is respecting the EU GDPR, the article 8 of the CEDH
and what is left of Roe vs Wade in the US in terms of constitutional
protections. If you're a human right activist, you have time to dedicate
yourself on years-long issues and you have the dual-level of legal and
technical expertise, I would invite you to open litigations against mining
pools and chainanalysis companies in this space. While European and US
jurisdictions have clear traditional constitutional protections and legal
remedies to protect the end-users zone of data autonomy, I'm incredibly
worried w.r.t to non-Western based jurisdictions less concerned with human
rights, where chainanalysis companies might do ethically concerning things.

[1] Putting back
https://bitcoinops.org/en/topics/consensus-cleanup-soft-fork/ on the
consensus upgrade table I think it would be great to address Bitcoin
consensus "technical debt" and simplify the design and analysis of
covenants and second-layers protocols.


Le lun. 14 ao?t 2023 ? 15:07, symphonicbtc <symphonicbtc@proton.me> a
?crit :

> > I think cross-input inspection (not cross-input signature aggregation
> which is different) is opening a pandora box in terms of "malicious"
> off-chain contracts than one could design. E.g miners bribing contracts to
> censor the confirmation of time-sensitive lightning channel transactions,
> where the bribes are paid on the hashrate distribution of miners during the
> previous difficulty period, thanks to the coinbase pubkey.
> >
> > See https://blog.bitmex.com/txwithhold-smart-contracts/ and
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-February/021395.html
>
> Hi Antoine,
>
> These two papers make a lot of incorrect assumptions about bitcoins
> security model. The assumption of the existence of constructs such as
> oracles or altchains for ?trustless? out-of-band payments opens the door
> for plenty of things that in reality are not possible without sacrificing
> security. The assumption that these constructs ?minimize? miner / attacker
> trust is no better than assuming the existence of an oracle that can simply
> perform the entire attack.
>
> Moreover, even the limited examples of attacks that do not use these
> constructs completely overlook the fact that bitcoins security model is
> dependent on the preservation of the nash equilibrium between miners. Not
> only is it disincentivized for miners to engage in any form of censorship,
> because they can all be fired by node-runners at any time, it is also not
> in miners interests to reorg the chain if say an anonymous miner mines some
> transactions that were being censored. Sustained, successful censorship in
> any capacity assumes that bitcoin is compromised, a 51% attack has
> occurred, and necessitates a change in PoW algorithm. A sufficient CSV in
> LN-like protocols is always sufficient to avoid being attacked in this way.
>
> The addition of most forms of covenant does not assist any of these
> attacks afaict because they already make assumptions rendering them invalid.
>
>
> Symphonic
>
> ------- Original Message -------
> On Monday, August 14th, 2023 at 3:00 AM, Antoine Riard via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>
> > Hi Salvatore,
> > > This also allows inspection of other inputs, that was not possible
> with the original opcodes.
> >
> > I think cross-input inspection (not cross-input signature aggregation
> which is different) is opening a pandora box in terms of "malicious"
> off-chain contracts than one could design. E.g miners bribing contracts to
> censor the confirmation of time-sensitive lightning channel transactions,
> where the bribes are paid on the hashrate distribution of miners during the
> previous difficulty period, thanks to the coinbase pubkey.
> >
> > See https://blog.bitmex.com/txwithhold-smart-contracts/ and
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-February/021395.html
> >
> > I wonder if we might face the dilemma of miners censorship attacks, if
> we wish to have more advanced bitcoin contracts, though I think it would be
> safe design practice to rule out those types of concerns thanks to smart
> bitcoin contracting primitives.
> >
> > I think this is a common risk to all second-layers vaults, lightning
> channels and payment pools.
> >
> > > A flag can disable this behavior"
> >
> > More than a binary flag like a matrix could be introduced to encode
> subset of introspected inputs /outputs to enable sighash_group-like
> semantic:
> >
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019243.html
> >
> > > There are two defined flags:
> > > - CCV_FLAG_CHECK_INPUT = 1: if present, <index> refers to an input;
> > > otherwise, it refers to an output.
> > > - CCV_FLAG_IGNORE_OUTPUT_AMOUNT = 2: only defined when _CHECK_INPUT
> > > is absent, it disables the deferred checks logic for amounts.
> >
> > Or even beyond a matrix, it could be a set of "tags". There could be a
> generalized tag for unstructured data, and another one for bitcoin
> transaction / script data types (e.g scriptpubkey, amount, nsequence,
> merkle branch) that could be fetched from the taproot annex.
> >
> > > After the evaluation of all inputs, it is verified that each output's
> > > amount is greater than or equal to the total amount in the bucket
> > > if that output (validation of the deferred checks).
> >
> > At the very least, I think for the payment pool, where you're
> fanning-out satoshis value from a subset of inputs to another subset of
> outputs, I think you would need more malleability here.
> >
> > > It is unclear if all the special values above will be useful in
> > > applications; however, as each special case requires very little added
> > > code, I tried to make the specs as flexible as possible at this time.
> >
> > I think this generic framework is interesting for joinpool / coinpool /
> payment pool, as you can check that any withdrawal output can be committed
> as part of the input scriptpubkey, and spend it on
> blessed-with-one-participant-sig script. There is still a big open question
> if it's efficient in terms of witness space consumed.
> >
> > That said, I still think you would need at least ANYPREVOUT and more
> malleability for the amount transfer validation as laid out above.
> >
> > Looking on the `DeferredCheck` framework commit, one obvious low-level
> concern is the DoS risk for full-nodes participating in transaction-relay,
> and that maybe policy rules should be introduced to keep the worst-CPU
> input in the ranges of current transaction spend allowed to propagate on
> the network today.
> >
> > Thanks for the proposal,
> >
> > Best,
> > Antoine
> >
> >
> >
> > Le dim. 30 juil. 2023 ? 22:52, Salvatore Ingala via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> a ?crit :
> >
> > > Hi all,
> > >
> > > I have put together a first complete proposal for the core opcodes of
> > > MATT [1][2].
> > > The changes make the opcode functionally complete, and the
> > > implementation is revised and improved.
> > >
> > > The code is implemented in the following fork of the
> > > bitcoin-inquisition repo:
> > >
> > > https://github.com/Merkleize/bitcoin/tree/checkcontractverify
> > >
> > > Therefore, it also includes OP_CHECKTEMPLATEVERIFY, as in a
> > > previous early demo for vaults [3].
> > >
> > > Please check out the diff [4] if you are interested in the
> > > implementation details. It includes some basic functional tests for
> > > the main cases of the opcode.
> > >
> > > ## Changes vs the previous draft
> > >
> > > These are the changes compared to the initial incomplete proposal:
> > > - OP_CHECK{IN,OUT}CONTRACTVERIFY are replaced by a single opcode
> > > OP_CHECKCONTRACTVERIFY (CCV). An additional `flags` parameter allows
> > > to specify if the opcode operates on an input or an output.
> > > This also allows inspection of other inputs, that was not possible
> > > with the original opcodes.
> > > - For outputs, the default behavior is to have the following deferred
> > > checks mechanism for amounts: all the inputs that have a CCV towards
> > > the same output, have their input amounts summed, and that act as a
> > > lower bound for that output's amount.
> > > A flag can disable this behavior. [*]
> > > - A number of special values of the parameters were defined in order
> > > to optimize for common cases, and add some implicit introspection.
> > > - The order of parameters is modified (particularly, <data> is at the
> > > bottom of the arguments, as so is more natural when writing Scripts).
> > >
> > > ## Semantics
> > >
> > > The new OP_CHECKCONTRACTVERIFY takes 5 parameters from the stack:
> > >
> > > <data>, <index>, <pk>, <taptree>, <flags>
> > >
> > > The core logic of the opcode is as follows:
> > >
> > > "Check if the <index>-th input/output's scriptPubKey is a P2TR
> > > whose public key is obtained from <pk>, (optionally) tweaked with
> > > <data>, (optionally) tap-tweaked with <taptree>".
> > >
> > > The following are special values of the parameters:
> > >
> > > - if <pk> is empty, it is replaced with a fixed NUMS point. [**]
> > > - if <pk> is -1, it is replaced with the current input's taproot
> > > internal key.
> > > - if <index> is -1, it is replaced with the current input's index.
> > > - if <data> is empty, the data tweak is skipped.
> > > - if <taptree> is empty, the taptweak is skipped.
> > > - if <taptree> is -1, it is replaced with the current input's root
> > > of the taproot merkle tree.
> > >
> > > There are two defined flags:
> > > - CCV_FLAG_CHECK_INPUT = 1: if present, <index> refers to an input;
> > > otherwise, it refers to an output.
> > > - CCV_FLAG_IGNORE_OUTPUT_AMOUNT = 2: only defined when _CHECK_INPUT
> > > is absent, it disables the deferred checks logic for amounts.
> > >
> > > Finally, if both the flags CCV_FLAG_CHECK_INPUT and
> > > CCV_FLAG_IGNORE_OUTPUT_AMOUNT are absent:
> > > - Add the current input's amount to the <index>-th output's bucket.
> > >
> > > After the evaluation of all inputs, it is verified that each output's
> > > amount is greater than or equal to the total amount in the bucket
> > > if that output (validation of the deferred checks).
> > >
> > > ## Comment
> > >
> > > It is unclear if all the special values above will be useful in
> > > applications; however, as each special case requires very little added
> > > code, I tried to make the specs as flexible as possible at this time.
> > >
> > > With this new opcode, the full generality of MATT (including the fraud
> > > proofs) can be obtained with just two opcodes: OP_CHECKCONTRACTVERIFY
> > > and OP_CAT.
> > > However, additional opcodes (and additional introspection) would
> > > surely benefit some applications.
> > >
> > > I look forward to your comments, and to start drafting a BIP proposal.
> > >
> > > Best,
> > > Salvatore Ingala
> > >
> > >
> > > [*] - Credits go to James O'Beirne for this approach, taken from his
> > > OP_VAULT proposal. I cherry-picked the commit containing the
> > > Deferred Checks framework.
> > > [**] - The same NUMS point suggested in BIP-0341 was used.
> > >
> > >
> > > References:
> > >
> > > [1] - https://merkle.fun/
> > > [2] -
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021182.html
> > > [3] -
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021588.html
> > > [4] -
> https://github.com/bitcoin-inquisition/bitcoin/compare/24.0...Merkleize:bitcoin:checkcontractverify
> > > _______________________________________________
> > > bitcoin-dev mailing list
> > > bitcoin-dev@lists.linuxfoundation.org
> > > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230913/493f4fe1/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 16
********************************************
