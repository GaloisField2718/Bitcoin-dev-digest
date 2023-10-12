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
      cut-through update of Taproot leaves (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Thu, 12 Oct 2023 11:31:26 +0200
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Solving CoinPool high-interactivity issue
	with cut-through update of Taproot leaves
Message-ID:
	<CAD3i26BCS36FEBDMxBvBu2nTyLiDDCpmR7Eeu+Ebe3jBx0PvWQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi, Antoine.

A brief update on this:

I created a demo script for the unilateral exit of 2-of-4 participants in a
Coinpool using OP_CCV:
https://github.com/halseth/tapsim/tree/matt-demo/examples/matt/coinpool/v2.
It shows how pubkeys and balances can be committed, how traversal and
modification of the data can be done, and validation of signatures for the
exiting users.

The script in this case is 142 bytes (can likely be optimized 20-30%) and
the witness including the script is 647 bytes. Most of this comes from the
merkle inclusion proofs, so we can expect this to grow by O(m logn) for m
users exiting a pool of n participants.

Regardless of the size, I think that would not matter in most (cooperative)
settings. N participants would jointly create a coinpool using the above
exit scripts, and a cooperative keyspend path. In case some user goes
offline, the remaining, online users can jointly use the unilateral exit
clause and exit into a _new_ coinpool and continue operations when this
transaction confirms.

What would be really interesting, is if we can do the above exit off-chain,
and when the offline user comes back online, we could revert back to the
original coinpool output updating the balances according to updates that
happened while he was offline.

Assuming APO I believe this could work, since the only thing that matters
for the off-chain transactions to remain valid is that the committed
balances and keys remain compatible. If the offline user is able to
unilaterally spend the original output where the remaining users had built
their off-chain coinpool construction ontop, the only thing they need to
change is the merkle inclusion proofs in their jointly signed transactions
(since they now spend from an output where the offline user exited). All
signatures remain valid.

Was this the kind of functionality you were looking for?

Cheers,
Johan



On Thu, Oct 5, 2023 at 9:38?AM Johan Tor?s Halseth <johanth@gmail.com>
wrote:

> Hi,
>
> Yes, one would need to have the <data> be a merkle root of all
> participants' keys and balances. Then, as you say, the scripts would
> have to enforce that one correctly creates new merkle roots according
> to the coin pool rules when spending it.
>
> - Johan
>
> On Thu, Oct 5, 2023 at 3:13?AM Antoine Riard <antoine.riard@gmail.com>
> wrote:
> >
> > Hi Johan,
> >
> > Thanks for the insight.
> >
> > From the proposed semantics of OP_CHECKCONTRACTVERIFY iirc:
> >
> > <data> <index> <pk> <taptree> <flags>
> >
> > I think this is not yet indicated how the participant's pubkeys and
> balances can be disaggregated from <data>, a partial subset push on the
> stack and verifying that corresponding signatures are valid.
> >
> > One requirement of a cut-through update of taproot leaves is to verify
> the authentication of the fan-out balances and pubkeys towards the "online"
> partition. This subset is not known at pool setup, even if the contract or
> tree construct can be equilibrated with some expectation.
> >
> > Otherwise, it sounds OP_CHECKCONTRACTVERIFY could be used to architect
> the proposed design of coinpool and its cut-through mechanism. One hard
> issue sounds to be efficient traversal, inspection and modification of the
> contract <data>.
> >
> > Best,
> > Antoine
> >
> > Le mar. 3 oct. 2023 ? 12:24, Johan Tor?s Halseth <johanth@gmail.com> a
> ?crit :
> >>
> >> Hi, Antoine.
> >>
> >> It sounds like perhaps OP_CHECKCONTRACTVERIFY can achieve what you are
> >> looking for:
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-May/021719.html
> >>
> >> By committing the participants' pubkeys and balances in the dynamic
> >> data instead of the taptree one can imagine a subset of online users
> >> agreeing to pool their aggregated balances in a new output, while the
> >> offline users' funds would remain inaccessible by them in a second
> >> output.
> >>
> >> The way this would work is by spending the coinpool utxo with a
> >> transaction having two outputs: one output that is the "remainder" of
> >> the previous coinpool (the offline users), and the second output the
> >> new coinpool among the online users*.
> >>
> >> When the offline users are back online, they could all agree to
> >> continue using the original coinpool utxo.
> >>
> >> * assuming Eltoo in case an offline user comes back online and double
> >> spends the UTXO.
> >>
> >> - Johan
> >>
> >>
> >> On Wed, Sep 27, 2023 at 12:08?PM Antoine Riard via bitcoin-dev
> >> <bitcoin-dev@lists.linuxfoundation.org> wrote:
> >> >
> >> > Hi Zeeman,
> >> >
> >> > See my comments at the time of OP_EVICT original publication.
> >> >
> >> >
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019939.html
> >> >
> >> > "I think in the context of (off-chain) payment pool, OP_EVICT requires
> >> > participant cooperation *after* the state update to allow a single
> >> > participant to withdraw her funds.
> >> >
> >> > I believe this is unsafe if we retain as an off-chain construction
> security
> >> > requirement that a participant should have the unilateral means to
> enforce
> >> > the latest agreed upon state at any time during the construction
> lifetime".
> >> >
> >> > I think this level of covenant flexibility is still wished for
> CoinPool as a fundamental property, and this is offered by TLUV or
> MERKLESUB.
> >> > On the other hand, I think OP_EVICT introduces this idea of *subgroup
> novation* (i.e `K-of-N`) of a PT2R scriptpubkey.
> >> >
> >> > To the best of my understanding, I think there is not yet any sound
> covenant proposal aiming to combine TLUV and EVICT-like semantics in a
> consistent set of Script primitives to enable "cut-through" updates, while
> still retaining the key property of unilateral withdraw of promised
> balances in any-order.
> >> >
> >> > I might go to work on crafting one, though for now I'm still
> interested to understand better if on-chain "cut-through" is the best
> direction to solve the fundamental high interactivity issue of channel
> factory and payment pool over punishment-based ideas.
> >> >
> >> > Best,
> >> > Antoine
> >> >
> >> > Le mar. 26 sept. 2023 ? 07:51, ZmnSCPxj <ZmnSCPxj@protonmail.com> a
> ?crit :
> >> >>
> >> >> Good morning Antoine,
> >> >>
> >> >> Does `OP_EVICT` not fit?
> >> >>
> >> >>
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019926.html
> >> >>
> >> >> Regards,
> >> >> ZmnSCPxj
> >> >>
> >> >>
> >> >> Sent with Proton Mail secure email.
> >> >>
> >> >> ------- Original Message -------
> >> >> On Monday, September 25th, 2023 at 6:18 PM, Antoine Riard via
> bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> >> >>
> >> >>
> >> >> > Payment pools and channel factories are afflicted by severe
> interactivity constraints worsening with the number of users owning an
> off-chain balance in the construction. The security of user funds is
> paramount on the ability to withdraw unilaterally from the off-chain
> construction. As such any update applied to the off-chain balances requires
> a signature contribution from the unanimity of the construction users to
> ensure this ability is conserved along updates.
> >> >> > As soon as one user starts to be offline or irresponsive, the
> updates of the off-chain balances must have to be halted and payments
> progress are limited among subsets of 2 users sharing a channel. Different
> people have proposed solutions to this issue: introducing a coordinator,
> partitioning or layering balances in off-chain users subsets. I think all
> those solutions have circled around a novel issue introduced, namely
> equivocation of off-chain balances at the harm of construction
> counterparties [0].
> >> >> >
> >> >> > As ZmnSCPxj pointed out recently, one way to mitigate this
> equivocation consists in punishing the cheating pre-nominated coordinator
> on an external fidelity bond. One can even imagine more trust-mimized and
> decentralized fraud proofs to implement this mitigation, removing the need
> of a coordinator [1].
> >> >> >
> >> >> > However, I believe punishment equivocation to be game-theory sound
> should compensate a defrauded counterparty of the integrity of its lost
> off-chain balance. As one cheating counterparty can equivocate in the
> worst-case against all the other counterparties in the construction, one
> fidelity bond should be equal to ( C - 1 ) * B satoshi amount, where C is
> the number of construction counterparty and B the initial off-chain balance
> of the cheating counterparty.
> >> >> >
> >> >> > Moreover, I guess it is impossible to know ahead of a partition or
> transition who will be the "honest" counterparties from the "dishonest"
> ones, therefore this ( C - 1 ) * B-sized fidelity bond must be maintained
> by every counterparty in the pool or factory. On this ground, I think this
> mitigation and other corrective ones are not economically practical for
> large-scale pools among a set of anonymous users.
> >> >> >
> >> >> > I think the best solution to solve the interactivity issue which
> is realistic to design is one ruling out off-chain group equivocation in a
> prophylactic fashion. The pool or factory funding utxo should be edited in
> an efficient way to register new off-chain subgroups, as lack of
> interactivity from a subset of counterparties demands it.
> >> >> >
> >> >> > With CoinPool, there is already this idea of including a user
> pubkey and balance amount to each leaf composing the Taproot tree while
> preserving the key-path spend in case of unanimity in the user group.
> Taproot leaves can be effectively regarded as off-chain user accounts
> available to realize privacy-preserving payments and contracts.
> >> >> >
> >> >> > I think one (new ?) idea can be to introduce taproot leaves
> "cut-through" spends where multiple leaves are updated with a single
> witness, interactively composed by the owners of the spent leaves. This
> spend sends back the leaves amount to a new single leaf, aggregating the
> amounts and user pubkeys. The user leaves not participating in this
> "cut-through" are inherited with full integrity in the new version of the
> Taproot tree, at the gain of no interactivity from their side.
> >> >> >
> >> >> > Let's say you have a CoinPool funded and initially set with Alice,
> Bob, Caroll, Dave and Eve. Each pool participant has a leaf L.x committing
> to an amount A.x and user pubkey P.x, where x is the user name owning a
> leaf.
> >> >> >
> >> >> > Bob and Eve are deemed to be offline by the Alice, Caroll and Dave
> subset (the ACD group).
> >> >> >
> >> >> > The ACD group composes a cut-through spend of L.a + L.c + L.d.
> This spends generates a new leaf L.(acd) leaf committing to amount A.(acd)
> and P.(acd).
> >> >> >
> >> >> > Amount A.(acd) = A.a + A.c + A.d and pubkey P.(acd) = P.a + P.c +
> P.d.
> >> >> >
> >> >> > Bob's leaf L.b and Eve's leaf L.e are left unmodified.
> >> >> >
> >> >> > The ACD group generates a new Taproot tree T' = L.(acd) + L.b +
> L.e, where the key-path K spend including the original unanimity of pool
> counterparties is left unmodified.
> >> >> >
> >> >> > The ACD group can confirm a transaction spending the pool funding
> utxo to a new single output committing to the scriptpubkey K + T'.
> >> >> >
> >> >> > From then, the ACD group can pursue off-chain balance updates
> among the subgroup thanks to the new P.(acd) and relying on the known Eltoo
> mechanism. There is no possibility for any member of the ACD group to
> equivocate with Bob or Eve in a non-observable fashion.
> >> >> >
> >> >> > Once Bob and Eve are online and ready to negotiate an on-chain
> pool "refresh" transaction, the conserved key-path spend can be used to
> re-equilibrate the Taproot tree, prune out old subgroups unlikely to be
> used and provision future subgroups, all with a compact spend based on
> signature aggregation.
> >> >> >
> >> >> > Few new Taproot tree update script primitives have been proposed,
> e.g [2]. Though I think none with the level of flexibility offered to
> generate leaves cut-through spends, or even batch of "cut-through" where M
> subgroups are willing to spend N leaves to compose P new subgroups fan-out
> in Q new outputs, with showing a single on-chain witness. I believe such a
> hypothetical primitive can also reduce the chain space consumed in the
> occurrence of naive mass pool withdraws at the same time.
> >> >> >
> >> >> > I think this solution to the high-interactivity issue of payment
> pools and factories shifts the burden on each individual user to pre-commit
> fast Taproot tree traversals, allowing them to compose new pool subgroups
> as fluctuations in pool users' level of liveliness demand it. Pool
> efficiency becomes the sum of the quality of user prediction on its
> counterparties' liveliness during the construction lifetime. Recursive
> taproot tree spends or more efficient accumulator than merkle tree sounds
> ideas to lower the on-chain witness space consumed by every pool in the
> average non-interactive case.
> >> >> >
> >> >> > Cheers,
> >> >> > Antoine
> >> >> >
> >> >> > [0]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020370.html
> >> >> > [1]
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-August/004043.html
> >> >> > [2]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019420.html
> >> >
> >> > _______________________________________________
> >> > bitcoin-dev mailing list
> >> > bitcoin-dev@lists.linuxfoundation.org
> >> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231012/bca1144c/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 8
*******************************************
