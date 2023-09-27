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
   2. Re: Scaling Lightning With Simple Covenants (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Tue, 26 Sep 2023 16:36:26 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Solving CoinPool high-interactivity issue
	with cut-through update of Taproot leaves
Message-ID:
	<CALZpt+Gyo1STD4zrge3yiuC1j_NpJ8ZDYzzzAGCcZpjKw0_9-w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Zeeman,

See my comments at the time of OP_EVICT original publication.

https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019939.html

"I think in the context of (off-chain) payment pool, OP_EVICT requires
participant cooperation *after* the state update to allow a single
participant to withdraw her funds.

I believe this is unsafe if we retain as an off-chain construction security
requirement that a participant should have the unilateral means to enforce
the latest agreed upon state at any time during the construction lifetime".

I think this level of covenant flexibility is still wished for CoinPool as
a fundamental property, and this is offered by TLUV or MERKLESUB.
On the other hand, I think OP_EVICT introduces this idea of *subgroup
novation* (i.e `K-of-N`) of a PT2R scriptpubkey.

To the best of my understanding, I think there is not yet any sound
covenant proposal aiming to combine TLUV and EVICT-like semantics in a
consistent set of Script primitives to enable "cut-through" updates, while
still retaining the key property of unilateral withdraw of promised
balances in any-order.

I might go to work on crafting one, though for now I'm still interested to
understand better if on-chain "cut-through" is the best direction to solve
the fundamental high interactivity issue of channel factory and payment
pool over punishment-based ideas.

Best,
Antoine

Le mar. 26 sept. 2023 ? 07:51, ZmnSCPxj <ZmnSCPxj@protonmail.com> a ?crit :

> Good morning Antoine,
>
> Does `OP_EVICT` not fit?
>
>
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019926.html
>
> Regards,
> ZmnSCPxj
>
>
> Sent with Proton Mail secure email.
>
> ------- Original Message -------
> On Monday, September 25th, 2023 at 6:18 PM, Antoine Riard via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>
> > Payment pools and channel factories are afflicted by severe
> interactivity constraints worsening with the number of users owning an
> off-chain balance in the construction. The security of user funds is
> paramount on the ability to withdraw unilaterally from the off-chain
> construction. As such any update applied to the off-chain balances requires
> a signature contribution from the unanimity of the construction users to
> ensure this ability is conserved along updates.
> > As soon as one user starts to be offline or irresponsive, the updates of
> the off-chain balances must have to be halted and payments progress are
> limited among subsets of 2 users sharing a channel. Different people have
> proposed solutions to this issue: introducing a coordinator, partitioning
> or layering balances in off-chain users subsets. I think all those
> solutions have circled around a novel issue introduced, namely equivocation
> of off-chain balances at the harm of construction counterparties [0].
> >
> > As ZmnSCPxj pointed out recently, one way to mitigate this equivocation
> consists in punishing the cheating pre-nominated coordinator on an external
> fidelity bond. One can even imagine more trust-mimized and decentralized
> fraud proofs to implement this mitigation, removing the need of a
> coordinator [1].
> >
> > However, I believe punishment equivocation to be game-theory sound
> should compensate a defrauded counterparty of the integrity of its lost
> off-chain balance. As one cheating counterparty can equivocate in the
> worst-case against all the other counterparties in the construction, one
> fidelity bond should be equal to ( C - 1 ) * B satoshi amount, where C is
> the number of construction counterparty and B the initial off-chain balance
> of the cheating counterparty.
> >
> > Moreover, I guess it is impossible to know ahead of a partition or
> transition who will be the "honest" counterparties from the "dishonest"
> ones, therefore this ( C - 1 ) * B-sized fidelity bond must be maintained
> by every counterparty in the pool or factory. On this ground, I think this
> mitigation and other corrective ones are not economically practical for
> large-scale pools among a set of anonymous users.
> >
> > I think the best solution to solve the interactivity issue which is
> realistic to design is one ruling out off-chain group equivocation in a
> prophylactic fashion. The pool or factory funding utxo should be edited in
> an efficient way to register new off-chain subgroups, as lack of
> interactivity from a subset of counterparties demands it.
> >
> > With CoinPool, there is already this idea of including a user pubkey and
> balance amount to each leaf composing the Taproot tree while preserving the
> key-path spend in case of unanimity in the user group. Taproot leaves can
> be effectively regarded as off-chain user accounts available to realize
> privacy-preserving payments and contracts.
> >
> > I think one (new ?) idea can be to introduce taproot leaves
> "cut-through" spends where multiple leaves are updated with a single
> witness, interactively composed by the owners of the spent leaves. This
> spend sends back the leaves amount to a new single leaf, aggregating the
> amounts and user pubkeys. The user leaves not participating in this
> "cut-through" are inherited with full integrity in the new version of the
> Taproot tree, at the gain of no interactivity from their side.
> >
> > Let's say you have a CoinPool funded and initially set with Alice, Bob,
> Caroll, Dave and Eve. Each pool participant has a leaf L.x committing to an
> amount A.x and user pubkey P.x, where x is the user name owning a leaf.
> >
> > Bob and Eve are deemed to be offline by the Alice, Caroll and Dave
> subset (the ACD group).
> >
> > The ACD group composes a cut-through spend of L.a + L.c + L.d. This
> spends generates a new leaf L.(acd) leaf committing to amount A.(acd) and
> P.(acd).
> >
> > Amount A.(acd) = A.a + A.c + A.d and pubkey P.(acd) = P.a + P.c + P.d.
> >
> > Bob's leaf L.b and Eve's leaf L.e are left unmodified.
> >
> > The ACD group generates a new Taproot tree T' = L.(acd) + L.b + L.e,
> where the key-path K spend including the original unanimity of pool
> counterparties is left unmodified.
> >
> > The ACD group can confirm a transaction spending the pool funding utxo
> to a new single output committing to the scriptpubkey K + T'.
> >
> > From then, the ACD group can pursue off-chain balance updates among the
> subgroup thanks to the new P.(acd) and relying on the known Eltoo
> mechanism. There is no possibility for any member of the ACD group to
> equivocate with Bob or Eve in a non-observable fashion.
> >
> > Once Bob and Eve are online and ready to negotiate an on-chain pool
> "refresh" transaction, the conserved key-path spend can be used to
> re-equilibrate the Taproot tree, prune out old subgroups unlikely to be
> used and provision future subgroups, all with a compact spend based on
> signature aggregation.
> >
> > Few new Taproot tree update script primitives have been proposed, e.g
> [2]. Though I think none with the level of flexibility offered to generate
> leaves cut-through spends, or even batch of "cut-through" where M subgroups
> are willing to spend N leaves to compose P new subgroups fan-out in Q new
> outputs, with showing a single on-chain witness. I believe such a
> hypothetical primitive can also reduce the chain space consumed in the
> occurrence of naive mass pool withdraws at the same time.
> >
> > I think this solution to the high-interactivity issue of payment pools
> and factories shifts the burden on each individual user to pre-commit fast
> Taproot tree traversals, allowing them to compose new pool subgroups as
> fluctuations in pool users' level of liveliness demand it. Pool efficiency
> becomes the sum of the quality of user prediction on its counterparties'
> liveliness during the construction lifetime. Recursive taproot tree spends
> or more efficient accumulator than merkle tree sounds ideas to lower the
> on-chain witness space consumed by every pool in the average
> non-interactive case.
> >
> > Cheers,
> > Antoine
> >
> > [0]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020370.html
> > [1]
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-August/004043.html
> > [2]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019420.html
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230926/8231a2e7/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 26 Sep 2023 17:42:34 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: jlspc <jlspc@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<CALZpt+Fv8YO8g=7q-au37uU7iF-Qh2sFq-Q99msrGi==E3+06w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi John,

Thanks for the additional insightful comments. See new questions at the end.

> "My main point is that there's a huge pool of potential users that just
want payments to work, and they don't want to devote time or hardware
resources to making them work (if they can away with that)"

Sure, though somehow a "sovereign" casual user will still have to store
signatures and corresponding witnesses for off-chain balances at some
hardware somewhere, or delegate to another set of entities the storage or
on-chain broadcast (e.g watchtower). And then you start to have
interpedency with the timelocks of your off-chain construction and the
"bare minimum" witness space feerate average cost. All efficiency
considerations, ideally which can be laid out to reason on the trade-off of
off-chain constructions.

> "I also think resizing channels can be done fairly effectively off-chain
with hierarchical channels [1] (and even better with hierarchical channels
within timeout-trees)".

Yes, transactional scaling of Lightning (i.e how many transfers can be
performed off-chain per on-chain transaction) sounds good at first sight,
though in practice liquidity unbalance due to asymmetries in liquidity
flows among counterparties is a bottleneck. Note, how the on-chain
splicing for LSP spec upgrade improves on this dimension and where
"resizing" or "pool rebalancing" aims to keep this off-chain.

> "I just don't believe that is possible in practice, due to the need to
get a million casual users to sign a transaction where the transaction
specifies the casual users that need to sign it".

Well, this is not straightforward to pre-commit a subset of casual or
inactive users that need to sign (or do not need to sign). It sounds
achievable with current tree tricks like g'root or entroot for user groups
between 10-to-1000 (maybe more a full proposal would be needed to
estimate). Of course for orders of magnitude in the million, a more
efficient cryptographic accumulator than a Merkle tree would need to be
introduced at the consensus-level.

> "With these proposals, it's possible to dramatically limit the
interactivity".

Yes, from my rough understanding of timeout-trees and channel resizing, it
sounds to suffer from the same issue as Jeremy radix-tree's proposal or
Christian OG channel factory, namely the lack of fault-tolerance when one
of the casual user or end of tree balance owner aims to go on-chain. The
fragmentation cost sounds to be borne by all the users located in the tree
branch. Note fault-tolerance is one of the key payment pool design goals to
advance over factories.

> "I propose that if the active drain fails, the casual user should put
their channel in the old timeout-tree on-chain (so that it won't timeout on
them). "

I think there is still some issue there where you need to handle the
malicious HTLC-withholding case along your multi-hop payment paths and wait
for the expiration. Then go on-chain to expire the old timeout-tree, which
might come with a high timevalue cost by default. Not saying keeping
timevalue cost low is solved for today's Lightning.

> "I agree this isn't ideal, but I think it's much better than having them
have to perform some action at a specific time or within a very limited
time window (such as a day or a week)".

Yes, I think all the other off-chain constructions are encumbering the
casual users to perform some action within a very limited time window, and
as such requires strong liveliness (e.g to watch your counterparty
potential revoked commitment construction). This sounds to me a novel
aspect of TP-channel factories of allowing the casual user to decide when
they have to be on-time.

> "Getting fees right could be particularly challenging due to the
"thundering herd" problem, as _aj_ pointed out".

Yes, the thundering herd issue is explicitly mentioned in the OG Lightning
paper. To the best of my knowledge this is a distinct problem other than
exploitable asymmetries in local node policies and propagation, that it
cannot be fixed by transaction-relay changes.

> "These costs could be large, but hopefully they're rare as they are
failures by dedicated users that can afford to have highly-available
hardware and who want to maintain a good reputation".

Yes, though note as soon as a dedicated user starts to have a lot of
off-chain tree in the hand, and this is observable by adversaries the
dedicated user becomes an attack target (e.g for channel jamming or
time-dilation) which substantially alter the trade-offs.

> "However, the paper has a proposal for the use of "short-cut"
transactions that may be able to eliminate this logarithmic blow-up".

Yes "cut-through" to reduce on-chain footprint in mass exit cases has been
discussed since the early days of off-chain constructions and Taproot /
Grafroot introduction to the best of my knowledge, see:
https://tokyo2018.scalingbitcoin.org/transcript/tokyo2018/multi-party-channels-in-the-utxo-model-challenges-and-opportunities

Few questions from reading Dave's description of TP protocol here:
https://bitcoinops.org/en/newsletters/2023/03/29/#preventing-stranded-capital-with-multiparty-channels-and-channel-factories
.

In the scenario of multiple parties (e.g Alice, Bob, Caroll) owning a state
transaction + control output, what prevents Caroll to double-spend Bob's
revoked state transaction to a destination controlled by her in collusion
with Bob, at the harm of Alice ?

In the scenario of multiple commitment transactions spending the same state
transaction of an offliner user, what prevents Caroll to fake offliness and
equivocate at the harm of Alice or another party ?

Still building my understanding of the TP protocol security model and
seeing where it converges / diverges w.r.t other off-chain constructions
trade-offs.

Best,
Antoine

Le dim. 17 sept. 2023 ? 01:59, jlspc <jlspc@protonmail.com> a ?crit :

> Hi Antoine,
>
> Thanks for your note. Responses are in-line below:
>
> > Hi John,
>
> > Thanks for the proposal, few feedback after a first look.
>
> > &gt;<i> If Bitcoin and Lightning are to become widely-used, they will have to be adopted by casual users who want to send and receive bitcoin, but &gt; who do not want to go to any effort in order to provide the infrastructure for making payments.
> > </i>&gt;<i> Instead, it's reasonable to expect that the Lightning infrastructure will be provided by dedicated users who are far less numerous than
> > </i>
> > I don't know if it is that simple to classify expected users in
> > "casual"-vs"dedicated" and then design protocols accordingly. In
> > practice, if you take today Lightning as an example the trust
> > assumptions is more a matrix than a dichotomie, e.g you have the
> > choice between full-node vs light client to get block-relay,
> > large-sized mempool vs small mempool or no mempool at all for fee
> > estimations, routing HTLCs or not, running local watchtower or not...
> > without all those choices being necessarily interdependent. Generally,
> > I would say "tell me your IO disk/bandwidth/CPU performance/fees
> > ressources and level of technical knowledge and I'll tell you what
> > level of trust-minimization you can afford".
>
> Fair enough.
>
> I'm sure there are users with a wide range of expertise, resources, and interest in supporting Bitcoin.
> My main point is that there's a huge pool of potential users that just want payments to work, and they don't want to devote time or hardware resources to making them work (if they can get away with that).
> I also think we should do whatever we can to meet their needs.
>
> > &gt;<i> This difference in numbers implies that the key challenge in scaling Bitcoin and Lightning is providing bitcoin and Lightning to casual
> > </i>
> > &gt;<i> users.
> > </i>&gt;<i> As a result, the rest of this post will focus on this challenge.
> > </i>
> > I think few different scaling notions can be introduced to measure the
> > performance of an off-chain construction. Onboarding scaling defining
> > how many users can co-exist off-chain, considering throughput limits
> > (e.g blocksize, average block interval). Transactional scaling
> > defining how many transfers can be performed off-chain per on-chain
> > transaction, considering the properties of the off-chain system. Users
> > resource scaling defining how much resource a user should mobilize /
> > consume (e.g average weight cost for cooperative /  non-cooperative
> > close) to make a trust-minimized usage of the off-chain construction.
> > I think the proposal is mainly considering onboarding scalability, i.e
> > maxing out the number of channels that can be owned by a user though
> > it is unclear if other scalability dimensions are weighted in.
>
> Yes, exactly.
> I've focused on providing multiple channels to as many casual users as possible.
>
> In terms of other scalability dimensions, I think Lightning does a great job of providing a nearly unbounded number of payments per channel, without requiring on-chain transactions (once the channel is created).
> I also think resizing channels can be done fairly effectively off-chain with hierarchical channels [1] (and even better with hierarchical channels within timeout-trees).
>
> > In particular, no known protocol that uses the current Bitcoin
> > consensus rules allows a large number (e.g., tens-of-thousands to
> > millions) of Lightning channels, each co-owned by a casual user, to be
> > created from a single on-chain unspent transaction output (UTXO).
>
> > I?m not sure if this statement is 100% accurate. One could create a
> > radixpool with replacing CTV usage with Musig2 where the end
> > transactions outputs bear Lightning channel:
> > <a href="https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017968.html.">https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017968.html.</a>
>
> > Of course there is no N-party update mechanism to rebalance the
> > channel internally and it?s a nightmare if a subranch of transactions
> > with some depth hit the chain, though I think it works with today
> > Bitcoin consensus rules.
>
> I agree that it's theoretically possible to use signatures to create Lightning channels for a million casual users that are funded by a single UTXO.
> I just don't believe that that is possible in practice, due to the need to get a million casual users to sign a transaction where the transaction specifies the casual users that need to sign it.
>
> > The requirement for casual users to sign transactions that specify the
> > exact set of casual users whose signatures are required creates a very
> > difficult group coordination problem that's not well-suited to the
> > behavior of casual users [9, Section 2.2].
>
> > I think you have two more precise problems designated under this group
> > coordination problem. One is the dynamic novation of this group, i.e
> > how you add / remove user, if possible in a compact fashion. The
> > second the dynamic update of the ?account? / channels owned by the
> > users of this group, if possible with minimal interactivity.
>
> Yes, changing who pairs with whom and resizing channels are both important problems.
>
> I propose that changing pairings be done only via the creation and expiry of timeout-trees (with users that want to keep pairing with the same dedicated user(s) doing so via passive rollovers).
> I propose that channel resizing is mainly done via hierarchical channels, with any resizing that's not possible to do off-chain in that manner being done via creation and expiry of timeout-trees.
>
> With these proposals, it's possible to dramatically limit the interactivity.
>
> For example, if every channel created by a timeout-tree is a hierarchical channel of the form:
> * (casual user, (dedicated user, dedicated user)), or
> * (dedicated user, (dedicated user, dedicated user)), or
> * ((dedicated user, dedicated user), (dedicated user, dedicated user)),
> then at most four users ever have to coordinate to update any channel, and at most one of those users is ever a casual user.
>
> > &gt;<i> On the other hand, sometime shortly before E, casual user A_i can use the Lightning Network to send all of their balance in the channel &gt; &gt; (A_i, B) to themselves in some other Lightning channel that is the leaf of some other timeout-tree.
> > </i>
> > I think there is an uncertainty in this model as there is no guarantee
> > that you have a dedicated user ready to be the gateway to route the
> > balance, neither the dedicated user have adequate channel topology
> > allowing to send the funds in the part of the network you wish to do
> > so. And this is unclear what the casual user is left to do if an
> > intermediate hop withhold the HTLC in-flight until the timeout-tree
> > mature in favor of the dedicated user, iiuc.
>
> > So I think draining is uncertain in a world where jamming is possible,
> > even assuming economic mitigation as one might earn more to jam a
> > casual user draining than loosing in jamming upfront fees.
>
> I agree that active draining by the casual user is uncertain.
> I propose that if the active drain fails, the casual user should put their channel in the old timeout-tree on-chain (so that it won't timeout on them).
> Sorry that wasn't clear.
>
> > &gt;<i> Of course, sometime between E - to_self_delay_i and E, A_i should verify that B has created such a new timeout-tree.
> > </i>
> > I think this requirement is altering the design goal introduced at
> > first on casual users ?performing actions at specific times in the
> > future? as from my understanding there is no guarantee B broadcast an
> > on-chain transaction triggering the move of A funds to the new
> > timeout-tree. This becomes unclear when A should take correction
> > actions like broadcasting its own control transaction (?) when B fails
> > to dos, especially in a world where you have mempool congestion, and
> > earlier you?re better it might in term of fee risk.
>
> Ideally, I'd like casual users to only perform actions when they want to send or receive a payment.
> Unfortunately, I don't know how to do that.
> As a result, I've been forced to add a requirement that each casual user turns on their wallet software for a few minutes (but at a time of their choosing!) every few months (with the exact number of months being selected by the user) [2].
> I agree this isn't ideal, but I think it's much better than having them have to perform some action at a specific time or within a very limited time window (such as a day or a week).
>
> > &gt;<i> Fortunately, timeout-trees can be used to provide casual users with immediately-accessible off-chain bitcoin in addition to bitcoin in
> > </i>
> > I think this is unclear what is meant by ?immediately-accessible?
> > here, if they?re confirmed or not. Pre-signed / pre-committed
> > transactions at a fixed feerate might still not propagate on the
> > network, due to mempool min fee, and the user might have to take
> > actions in consequence like access hot wallet and sign a CPFP.
>
> I agree that the bitcoin may not be obtained if the user hasn't signed and submitted a transaction with sufficient fees.
> I tried to address this issue in the "Limitations" section of the post (specifically, Limitationss 2 and 3).
>
> I think that getting a reliable transport mechanism for packages is critical.
>
> Getting fees right could be particularly challenging due to the "thundering herd" problem, as _aj_ pointed out.
> As I noted in my response to him, I think an additional change to Bitcoin that allows timing based on fee levels could be very helpful.
> I'll try to write up the details and get that out as soon as possible.
>
> > &gt;<i> In reality, their on-chain footprint would be dominated by users who don't follow the protocol due to errors, unavailability, or malicious &gt; intent.
> > </i>
> > The fault-tolerance of such off-chain construction is very unclear i.e
> > if for any unavailable or erring user the whole off-chain construction
> > ends up on-chain. This is one significant defect in my opinion of the
> > radixpool or old school apo channel factory (or even coinpool if no
> > time-locked kick-out transaction is used), if one user becomes
> > unresponsive after a while.
>
> With a timeout-tree, if the dedicated user(s) funding the tree is unavailable (or makes an error) and fails to rollover a given casual user, that casual user should put their channel in the old timeout-tree on-chain.
> If the failure applies to all channels in the timeout-tree, the entire timeout-tree will be forced to go on-chain (thus doubling the number of on-chain transactions as compared to just putting the channels on-chain directly, without a timeout-tree).
> Sorry this wasn't made clear.
>
> These costs could be large, but hopefully they're rare as they are failures by dedicated users that can afford to have highly-available hardware and who want to maintain a good reputation.
>
> Separately, HTLCs that are not resolved off-chain have to be put on-chain, but doing so does not force the timeout-tree itself to go on-chain.
> If the HTLC control transactions are funded via zero-valued covenant trees (as proposed in the post and paper), putting an HTLC transaction on-chain can also require putting its ancestors in the covenant tree on-chain (thus creating a blow-up that is logarithmic in the number of leaves in the covenant tree).
> However, the paper has a proposal for the use of "short-cut" transactions that may be able to eliminate this logarithmic blow-up.
>
> Thanks for your thoughtful comments and please let me know if there's anything else that wasn't clear.
>
> Regards,
> John
>
> > Best,
>
> > Antoine
>
> [1] Law, "Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://github.com/JohnLaw2/ln-hierarchical-channels
> [2] Law, "Watchtower-Free Lightning Channels For Casual Users", https://github.com/JohnLaw2/ln-watchtower-free
>
>
>
>
> Sent with Proton Mail <https://proton.me/> secure email.
>
>
>>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230926/f7d10c03/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 23
********************************************
