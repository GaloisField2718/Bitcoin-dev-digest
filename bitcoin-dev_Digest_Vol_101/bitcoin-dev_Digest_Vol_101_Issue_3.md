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

   1. Re: Solving CoinPool high-interactivity issue with
      cut-through update of Taproot leaves (Antoine Riard)
   2. Re: Actuarial System To Reduce Interactivity In N-of-N (N >
      2) Multiparticipant Offchain Mechanisms (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Thu, 5 Oct 2023 02:13:06 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Johan Tor?s Halseth <johanth@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Solving CoinPool high-interactivity issue
	with cut-through update of Taproot leaves
Message-ID:
	<CALZpt+FT3qwP5MaZT4hbGYXvbECsAn7LvNbZC5vP-jGkbpOGVA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Johan,

Thanks for the insight.

>From the proposed semantics of OP_CHECKCONTRACTVERIFY iirc:

<data> <index> <pk> <taptree> <flags>

I think this is not yet indicated how the participant's pubkeys and
balances can be disaggregated from <data>, a partial subset push on the
stack and verifying that corresponding signatures are valid.

One requirement of a cut-through update of taproot leaves is to verify the
authentication of the fan-out balances and pubkeys towards the "online"
partition. This subset is not known at pool setup, even if the contract or
tree construct can be equilibrated with some expectation.

Otherwise, it sounds OP_CHECKCONTRACTVERIFY could be used to architect the
proposed design of coinpool and its cut-through mechanism. One hard issue
sounds to be efficient traversal, inspection and modification of the
contract <data>.

Best,
Antoine

Le mar. 3 oct. 2023 ? 12:24, Johan Tor?s Halseth <johanth@gmail.com> a
?crit :

> Hi, Antoine.
>
> It sounds like perhaps OP_CHECKCONTRACTVERIFY can achieve what you are
> looking for:
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-May/021719.html
>
> By committing the participants' pubkeys and balances in the dynamic
> data instead of the taptree one can imagine a subset of online users
> agreeing to pool their aggregated balances in a new output, while the
> offline users' funds would remain inaccessible by them in a second
> output.
>
> The way this would work is by spending the coinpool utxo with a
> transaction having two outputs: one output that is the "remainder" of
> the previous coinpool (the offline users), and the second output the
> new coinpool among the online users*.
>
> When the offline users are back online, they could all agree to
> continue using the original coinpool utxo.
>
> * assuming Eltoo in case an offline user comes back online and double
> spends the UTXO.
>
> - Johan
>
>
> On Wed, Sep 27, 2023 at 12:08?PM Antoine Riard via bitcoin-dev
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
> >
> > Hi Zeeman,
> >
> > See my comments at the time of OP_EVICT original publication.
> >
> >
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019939.html
> >
> > "I think in the context of (off-chain) payment pool, OP_EVICT requires
> > participant cooperation *after* the state update to allow a single
> > participant to withdraw her funds.
> >
> > I believe this is unsafe if we retain as an off-chain construction
> security
> > requirement that a participant should have the unilateral means to
> enforce
> > the latest agreed upon state at any time during the construction
> lifetime".
> >
> > I think this level of covenant flexibility is still wished for CoinPool
> as a fundamental property, and this is offered by TLUV or MERKLESUB.
> > On the other hand, I think OP_EVICT introduces this idea of *subgroup
> novation* (i.e `K-of-N`) of a PT2R scriptpubkey.
> >
> > To the best of my understanding, I think there is not yet any sound
> covenant proposal aiming to combine TLUV and EVICT-like semantics in a
> consistent set of Script primitives to enable "cut-through" updates, while
> still retaining the key property of unilateral withdraw of promised
> balances in any-order.
> >
> > I might go to work on crafting one, though for now I'm still interested
> to understand better if on-chain "cut-through" is the best direction to
> solve the fundamental high interactivity issue of channel factory and
> payment pool over punishment-based ideas.
> >
> > Best,
> > Antoine
> >
> > Le mar. 26 sept. 2023 ? 07:51, ZmnSCPxj <ZmnSCPxj@protonmail.com> a
> ?crit :
> >>
> >> Good morning Antoine,
> >>
> >> Does `OP_EVICT` not fit?
> >>
> >>
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019926.html
> >>
> >> Regards,
> >> ZmnSCPxj
> >>
> >>
> >> Sent with Proton Mail secure email.
> >>
> >> ------- Original Message -------
> >> On Monday, September 25th, 2023 at 6:18 PM, Antoine Riard via
> bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> >>
> >>
> >> > Payment pools and channel factories are afflicted by severe
> interactivity constraints worsening with the number of users owning an
> off-chain balance in the construction. The security of user funds is
> paramount on the ability to withdraw unilaterally from the off-chain
> construction. As such any update applied to the off-chain balances requires
> a signature contribution from the unanimity of the construction users to
> ensure this ability is conserved along updates.
> >> > As soon as one user starts to be offline or irresponsive, the updates
> of the off-chain balances must have to be halted and payments progress are
> limited among subsets of 2 users sharing a channel. Different people have
> proposed solutions to this issue: introducing a coordinator, partitioning
> or layering balances in off-chain users subsets. I think all those
> solutions have circled around a novel issue introduced, namely equivocation
> of off-chain balances at the harm of construction counterparties [0].
> >> >
> >> > As ZmnSCPxj pointed out recently, one way to mitigate this
> equivocation consists in punishing the cheating pre-nominated coordinator
> on an external fidelity bond. One can even imagine more trust-mimized and
> decentralized fraud proofs to implement this mitigation, removing the need
> of a coordinator [1].
> >> >
> >> > However, I believe punishment equivocation to be game-theory sound
> should compensate a defrauded counterparty of the integrity of its lost
> off-chain balance. As one cheating counterparty can equivocate in the
> worst-case against all the other counterparties in the construction, one
> fidelity bond should be equal to ( C - 1 ) * B satoshi amount, where C is
> the number of construction counterparty and B the initial off-chain balance
> of the cheating counterparty.
> >> >
> >> > Moreover, I guess it is impossible to know ahead of a partition or
> transition who will be the "honest" counterparties from the "dishonest"
> ones, therefore this ( C - 1 ) * B-sized fidelity bond must be maintained
> by every counterparty in the pool or factory. On this ground, I think this
> mitigation and other corrective ones are not economically practical for
> large-scale pools among a set of anonymous users.
> >> >
> >> > I think the best solution to solve the interactivity issue which is
> realistic to design is one ruling out off-chain group equivocation in a
> prophylactic fashion. The pool or factory funding utxo should be edited in
> an efficient way to register new off-chain subgroups, as lack of
> interactivity from a subset of counterparties demands it.
> >> >
> >> > With CoinPool, there is already this idea of including a user pubkey
> and balance amount to each leaf composing the Taproot tree while preserving
> the key-path spend in case of unanimity in the user group. Taproot leaves
> can be effectively regarded as off-chain user accounts available to realize
> privacy-preserving payments and contracts.
> >> >
> >> > I think one (new ?) idea can be to introduce taproot leaves
> "cut-through" spends where multiple leaves are updated with a single
> witness, interactively composed by the owners of the spent leaves. This
> spend sends back the leaves amount to a new single leaf, aggregating the
> amounts and user pubkeys. The user leaves not participating in this
> "cut-through" are inherited with full integrity in the new version of the
> Taproot tree, at the gain of no interactivity from their side.
> >> >
> >> > Let's say you have a CoinPool funded and initially set with Alice,
> Bob, Caroll, Dave and Eve. Each pool participant has a leaf L.x committing
> to an amount A.x and user pubkey P.x, where x is the user name owning a
> leaf.
> >> >
> >> > Bob and Eve are deemed to be offline by the Alice, Caroll and Dave
> subset (the ACD group).
> >> >
> >> > The ACD group composes a cut-through spend of L.a + L.c + L.d. This
> spends generates a new leaf L.(acd) leaf committing to amount A.(acd) and
> P.(acd).
> >> >
> >> > Amount A.(acd) = A.a + A.c + A.d and pubkey P.(acd) = P.a + P.c + P.d.
> >> >
> >> > Bob's leaf L.b and Eve's leaf L.e are left unmodified.
> >> >
> >> > The ACD group generates a new Taproot tree T' = L.(acd) + L.b + L.e,
> where the key-path K spend including the original unanimity of pool
> counterparties is left unmodified.
> >> >
> >> > The ACD group can confirm a transaction spending the pool funding
> utxo to a new single output committing to the scriptpubkey K + T'.
> >> >
> >> > From then, the ACD group can pursue off-chain balance updates among
> the subgroup thanks to the new P.(acd) and relying on the known Eltoo
> mechanism. There is no possibility for any member of the ACD group to
> equivocate with Bob or Eve in a non-observable fashion.
> >> >
> >> > Once Bob and Eve are online and ready to negotiate an on-chain pool
> "refresh" transaction, the conserved key-path spend can be used to
> re-equilibrate the Taproot tree, prune out old subgroups unlikely to be
> used and provision future subgroups, all with a compact spend based on
> signature aggregation.
> >> >
> >> > Few new Taproot tree update script primitives have been proposed, e.g
> [2]. Though I think none with the level of flexibility offered to generate
> leaves cut-through spends, or even batch of "cut-through" where M subgroups
> are willing to spend N leaves to compose P new subgroups fan-out in Q new
> outputs, with showing a single on-chain witness. I believe such a
> hypothetical primitive can also reduce the chain space consumed in the
> occurrence of naive mass pool withdraws at the same time.
> >> >
> >> > I think this solution to the high-interactivity issue of payment
> pools and factories shifts the burden on each individual user to pre-commit
> fast Taproot tree traversals, allowing them to compose new pool subgroups
> as fluctuations in pool users' level of liveliness demand it. Pool
> efficiency becomes the sum of the quality of user prediction on its
> counterparties' liveliness during the construction lifetime. Recursive
> taproot tree spends or more efficient accumulator than merkle tree sounds
> ideas to lower the on-chain witness space consumed by every pool in the
> average non-interactive case.
> >> >
> >> > Cheers,
> >> > Antoine
> >> >
> >> > [0]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020370.html
> >> > [1]
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-August/004043.html
> >> > [2]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019420.html
> >
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231005/92ae2c88/attachment-0001.html>

------------------------------

Message: 2
Date: Thu, 5 Oct 2023 03:12:33 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N > 2) Multiparticipant Offchain Mechanisms
Message-ID:
	<CALZpt+FN4XeGD2Yh7pEUhuFtgMtNgbVKThFgF-fU9pD3sPnc2A@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Zeeman,

> Basically, the big issue is that the actuary needs to bond a significant
amount of funds to each participant, and that bond is not part of the
funding of the construction.
>
> Other ways of ensuring single-use can be replaced, if that is possible.
> Do you know of any?

As explained in the other post, if you wish to ensure lack of equivocation
of an off-chain state I think you're left between updating dynamically the
subgroup of balance keys *on-chain* (i.e use the blockchain as an
anti-double spend oracle) or ensure any equivocation can be punished as
soon as one party gains knowledge of two commitment signatures.

I think you can design a fraud proof system encumbering each channel
factory or pool balance by leveraging OP_CHECKSIGFROMSTACK and the spent
outpoint committed as a partial transaction template. However, the amount
of satoshis that should be locked in such fidelity bonds must be equal to
the counterparty initial balance multiplied by the remaining
counterparties, as one can cheat against every other party (assuming there
is no shared communication channel where equivocation can be observed).

E.g if your factory has 1000 participants and your balance is 10 000
satoshis, you *must* lock up 10 000 000 in fidelity bonds while only 1 /
1000th of the amount can be leveraged as off-chain contract or payment.

Of course pre-nominated coordinator reduces the burden from the full *flat*
fidelity bond, though it has to be weighed with coordinator unavailability
occurence where each participant has to withdraw his balance on-chain, and
bears the fee cost.

Best,
Antoine

Le mar. 12 sept. 2023 ? 10:41, ZmnSCPxj <ZmnSCPxj@protonmail.com> a ?crit :

> Good morning Antoine,
>
>
> > Hi Zeeman
> >
> > > What we can do is to add the actuary to the contract that
> > > controls the funds, but with the condition that the
> > > actuary signature has a specific `R`.
> >
> > > As we know, `R` reuse --- creating a new signature for a
> > > different message but the same `R` --- will leak the
> > > private key.
> >
> > > The actuary can be forced to put up an onchain bond.
> > > The bond can be spent using the private key of the actuary.
> > > If the actuary signs a transaction once, with a fixed `R`,
> > > then its private key is still safe.
> >
> > > However, if the actuary signs one transaction that spends
> > > some transaction output, and then signs a different
> > > transaction that spends the same transaction output, both
> > > signatures need to use the same fixed `R`.
> > > Because of the `R` reuse, this lets anyone who expected
> > > one transaction to be confirmed, but finds that the other
> > > one was confirmed, to derive the secret key of the
> > > actuary from the two signatures, and then slash the bond
> > > of the actuary.
> >
> > From my understanding, if an off-chain state N1 with a negotiated group
> of 40 is halted in the middle of the actuary's R reveals due to the 40th
> participant non-interactivity, there is no guarantee than a new off-chain
> state N1' with a new negotiated group of 39 (from which evicted 40th's
> output is absent) do not re-use R reveals on N1. So for the actuary bond
> security, I think the R reveal should only happen once all the group
> participants have revealed their own signature. It sounds like some loose
> interactivity is still assumed, i.e all the non-actuary participants must
> be online at the same time, and lack of contribution is to blame as you
> have a "flat" off-chain construction (i.e no layering of the promised
> off-chain outputs in subgroups to lower novation interactivity).
>
> Yes, there is some loose interactivity assumed.
>
> However:
>
> * The actuary is always online and can gather signatures for the next
> state in parallel with signing new transactions on top of the next state.
>   * This is why `SIGHASH_ANYPREVOUT` is needed, as the transactions on top
> of the next state might spend either the actual next state (if the next
> state is successfully signed), or the current state plus additional
> transactions (i.e. the transaction that move from current state to next
> state) (if the next state fails to get fully signed and the participants
> decide to give up on the next state getting signed).
>
> > More fundamentally, I think this actuarial system does not solve the
> "multi-party off-chain state correction" problem as there is no guarantee
> that the actuary does not slash the bond itself. And if the bond is guarded
> by users' pubkeys, there is no guarantee that the user will cooperate after
> the actuary equivocation is committed to sign a "fair" slashing transaction.
>
> Indeed.
>
> One can consider that the participants other than the actuary would
> generate a single public key known by the participants.
> But then only one sockpuppet of the actuary is needed to add to the
> participant set.
>
> Basically, the big issue is that the actuary needs to bond a significant
> amount of funds to each participant, and that bond is not part of the
> funding of the construction.
>
> Other ways of ensuring single-use can be replaced, if that is possible.
> Do you know of any?
>
> Regards,
> ZmnSCPxj
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231005/c29d68dc/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 3
*******************************************
