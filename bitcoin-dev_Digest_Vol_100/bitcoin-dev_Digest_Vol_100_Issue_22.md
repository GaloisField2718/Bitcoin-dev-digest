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

   1. Solving CoinPool high-interactivity issue with cut-through
      update of Taproot leaves (Antoine Riard)
   2. Re: Solving CoinPool high-interactivity issue with
      cut-through update of Taproot leaves (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Mon, 25 Sep 2023 19:18:36 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Solving CoinPool high-interactivity issue with
	cut-through update of Taproot leaves
Message-ID:
	<CALZpt+F26bArqU7aZj8VN-zDN-3_VZS1K1ibaJOeCrsLDL2_4Q@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Payment pools and channel factories are afflicted by severe interactivity
constraints worsening with the number of users owning an off-chain balance
in the construction. The security of user funds is paramount on the ability
to withdraw unilaterally from the off-chain construction. As such any
update applied to the off-chain balances requires a signature contribution
from the unanimity of the construction users to ensure this ability is
conserved along updates.

As soon as one user starts to be offline or irresponsive, the updates of
the off-chain balances must have to be halted and payments progress are
limited among subsets of 2 users sharing a channel. Different people have
proposed solutions to this issue: introducing a coordinator, partitioning
or layering balances in off-chain users subsets. I think all those
solutions have circled around a novel issue introduced, namely equivocation
of off-chain balances at the harm of construction counterparties [0].

As ZmnSCPxj pointed out recently, one way to mitigate this equivocation
consists in punishing the cheating pre-nominated coordinator on an external
fidelity bond. One can even imagine more trust-mimized and decentralized
fraud proofs to implement this mitigation, removing the need of a
coordinator [1].

However, I believe punishment equivocation to be game-theory sound should
compensate a defrauded counterparty of the integrity of its lost off-chain
balance. As one cheating counterparty can equivocate in the worst-case
against all the other counterparties in the construction, one fidelity bond
should be equal to ( C - 1 ) * B satoshi amount, where C is the number of
construction counterparty and B the initial off-chain balance of the
cheating counterparty.

Moreover, I guess it is impossible to know ahead of a partition or
transition who will be the "honest" counterparties from the "dishonest"
ones, therefore this ( C - 1 ) * B-sized fidelity bond must be maintained
by every counterparty in the pool or factory. On this ground, I think this
mitigation and other corrective ones are not economically practical for
large-scale pools among a set of anonymous users.

I think the best solution to solve the interactivity issue which is
realistic to design is one ruling out off-chain group equivocation in a
prophylactic fashion. The pool or factory funding utxo should be edited in
an efficient way to register new off-chain subgroups, as lack of
interactivity from a subset of counterparties demands it.

With CoinPool, there is already this idea of including a user pubkey and
balance amount to each leaf composing the Taproot tree while preserving the
key-path spend in case of unanimity in the user group. Taproot leaves can
be effectively regarded as off-chain user accounts available to realize
privacy-preserving payments and contracts.

I think one (new ?) idea can be to introduce taproot leaves "cut-through"
spends where multiple leaves are updated with a single witness,
interactively composed by the owners of the spent leaves. This spend sends
back the leaves amount to a new single leaf, aggregating the amounts and
user pubkeys. The user leaves not participating in this "cut-through" are
inherited with full integrity in the new version of the Taproot tree, at
the gain of no interactivity from their side.

Let's say you have a CoinPool funded and initially set with Alice, Bob,
Caroll, Dave and Eve. Each pool participant has a leaf L.x committing to an
amount A.x and user pubkey P.x, where x is the user name owning a leaf.

Bob and Eve are deemed to be offline by the Alice, Caroll and Dave subset
(the ACD group).

The ACD group composes a cut-through spend of L.a + L.c + L.d. This spends
generates a new leaf L.(acd) leaf committing to amount A.(acd) and P.(acd).

Amount A.(acd) = A.a + A.c + A.d and pubkey P.(acd) = P.a + P.c + P.d.

Bob's leaf L.b and Eve's leaf L.e are left unmodified.

The ACD group generates a new Taproot tree T' = L.(acd) + L.b + L.e, where
the key-path K spend including the original unanimity of pool
counterparties is left unmodified.

The ACD group can confirm a transaction spending the pool funding utxo to a
new single output committing to the scriptpubkey K + T'.

>From then, the ACD group can pursue off-chain balance updates among the
subgroup thanks to the new P.(acd) and relying on the known Eltoo
mechanism. There is no possibility for any member of the ACD group to
equivocate with Bob or Eve in a non-observable fashion.

Once Bob and Eve are online and ready to negotiate an on-chain pool
"refresh" transaction, the conserved key-path spend can be used to
re-equilibrate the Taproot tree, prune out old subgroups unlikely to be
used and provision future subgroups, all with a compact spend based on
signature aggregation.

Few new Taproot tree update script primitives have been proposed, e.g [2].
Though I think none with the level of flexibility offered to generate
leaves cut-through spends, or even batch of "cut-through" where M subgroups
are willing to spend N leaves to compose P new subgroups fan-out in Q new
outputs, with showing a single on-chain witness. I believe such a
hypothetical primitive can also reduce the chain space consumed in the
occurrence of naive mass pool withdraws at the same time.

I think this solution to the high-interactivity issue of payment pools and
factories shifts the burden on each individual user to pre-commit fast
Taproot tree traversals, allowing them to compose new pool subgroups as
fluctuations in pool users' level of liveliness demand it. Pool efficiency
becomes the sum of the quality of user prediction on its counterparties'
liveliness during the construction lifetime. Recursive taproot tree spends
or more efficient accumulator than merkle tree sounds ideas to lower the
on-chain witness space consumed by every pool in the average
non-interactive case.

Cheers,
Antoine

[0]
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020370.html
[1]
https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-August/004043.html
[2]
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019420.html
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230925/77e3936d/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 26 Sep 2023 06:50:50 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Solving CoinPool high-interactivity issue
	with	cut-through update of Taproot leaves
Message-ID:
	<OUAbM8ii-HE8M-kRAkMvdDkbiwKuG_wcYlrvC276eIsKXcW6Yh6iNcxy_PtchHNL3jIIc-nz-ucv2H11EznrZbYhKqyVPhE8__GeIDLxPNw=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Antoine,

Does `OP_EVICT` not fit?

https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019926.html

Regards,
ZmnSCPxj


Sent with Proton Mail secure email.

------- Original Message -------
On Monday, September 25th, 2023 at 6:18 PM, Antoine Riard via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Payment pools and channel factories are afflicted by severe interactivity constraints worsening with the number of users owning an off-chain balance in the construction. The security of user funds is paramount on the ability to withdraw unilaterally from the off-chain construction. As such any update applied to the off-chain balances requires a signature contribution from the unanimity of the construction users to ensure this ability is conserved along updates.
> As soon as one user starts to be offline or irresponsive, the updates of the off-chain balances must have to be halted and payments progress are limited among subsets of 2 users sharing a channel. Different people have proposed solutions to this issue: introducing a coordinator, partitioning or layering balances in off-chain users subsets. I think all those solutions have circled around a novel issue introduced, namely equivocation of off-chain balances at the harm of construction counterparties [0].
> 
> As ZmnSCPxj pointed out recently, one way to mitigate this equivocation consists in punishing the cheating pre-nominated coordinator on an external fidelity bond. One can even imagine more trust-mimized and decentralized fraud proofs to implement this mitigation, removing the need of a coordinator [1].
> 
> However, I believe punishment equivocation to be game-theory sound should compensate a defrauded counterparty of the integrity of its lost off-chain balance. As one cheating counterparty can equivocate in the worst-case against all the other counterparties in the construction, one fidelity bond should be equal to ( C - 1 ) * B satoshi amount, where C is the number of construction counterparty and B the initial off-chain balance of the cheating counterparty.
> 
> Moreover, I guess it is impossible to know ahead of a partition or transition who will be the "honest" counterparties from the "dishonest" ones, therefore this ( C - 1 ) * B-sized fidelity bond must be maintained by every counterparty in the pool or factory. On this ground, I think this mitigation and other corrective ones are not economically practical for large-scale pools among a set of anonymous users.
> 
> I think the best solution to solve the interactivity issue which is realistic to design is one ruling out off-chain group equivocation in a prophylactic fashion. The pool or factory funding utxo should be edited in an efficient way to register new off-chain subgroups, as lack of interactivity from a subset of counterparties demands it.
> 
> With CoinPool, there is already this idea of including a user pubkey and balance amount to each leaf composing the Taproot tree while preserving the key-path spend in case of unanimity in the user group. Taproot leaves can be effectively regarded as off-chain user accounts available to realize privacy-preserving payments and contracts.
> 
> I think one (new ?) idea can be to introduce taproot leaves "cut-through" spends where multiple leaves are updated with a single witness, interactively composed by the owners of the spent leaves. This spend sends back the leaves amount to a new single leaf, aggregating the amounts and user pubkeys. The user leaves not participating in this "cut-through" are inherited with full integrity in the new version of the Taproot tree, at the gain of no interactivity from their side.
> 
> Let's say you have a CoinPool funded and initially set with Alice, Bob, Caroll, Dave and Eve. Each pool participant has a leaf L.x committing to an amount A.x and user pubkey P.x, where x is the user name owning a leaf.
> 
> Bob and Eve are deemed to be offline by the Alice, Caroll and Dave subset (the ACD group).
> 
> The ACD group composes a cut-through spend of L.a + L.c + L.d. This spends generates a new leaf L.(acd) leaf committing to amount A.(acd) and P.(acd).
> 
> Amount A.(acd) = A.a + A.c + A.d and pubkey P.(acd) = P.a + P.c + P.d.
> 
> Bob's leaf L.b and Eve's leaf L.e are left unmodified.
> 
> The ACD group generates a new Taproot tree T' = L.(acd) + L.b + L.e, where the key-path K spend including the original unanimity of pool counterparties is left unmodified.
> 
> The ACD group can confirm a transaction spending the pool funding utxo to a new single output committing to the scriptpubkey K + T'.
> 
> From then, the ACD group can pursue off-chain balance updates among the subgroup thanks to the new P.(acd) and relying on the known Eltoo mechanism. There is no possibility for any member of the ACD group to equivocate with Bob or Eve in a non-observable fashion.
> 
> Once Bob and Eve are online and ready to negotiate an on-chain pool "refresh" transaction, the conserved key-path spend can be used to re-equilibrate the Taproot tree, prune out old subgroups unlikely to be used and provision future subgroups, all with a compact spend based on signature aggregation.
> 
> Few new Taproot tree update script primitives have been proposed, e.g [2]. Though I think none with the level of flexibility offered to generate leaves cut-through spends, or even batch of "cut-through" where M subgroups are willing to spend N leaves to compose P new subgroups fan-out in Q new outputs, with showing a single on-chain witness. I believe such a hypothetical primitive can also reduce the chain space consumed in the occurrence of naive mass pool withdraws at the same time.
> 
> I think this solution to the high-interactivity issue of payment pools and factories shifts the burden on each individual user to pre-commit fast Taproot tree traversals, allowing them to compose new pool subgroups as fluctuations in pool users' level of liveliness demand it. Pool efficiency becomes the sum of the quality of user prediction on its counterparties' liveliness during the construction lifetime. Recursive taproot tree spends or more efficient accumulator than merkle tree sounds ideas to lower the on-chain witness space consumed by every pool in the average non-interactive case.
> 
> Cheers,
> Antoine
> 
> [0] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020370.html
> [1] https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-August/004043.html
> [2] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019420.html


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 22
********************************************
