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

   1. Re: Actuarial System To Reduce Interactivity In N-of-N (N >
      2) Multiparticipant Offchain Mechanisms (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Mon, 11 Sep 2023 07:02:13 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N > 2) Multiparticipant Offchain Mechanisms
Message-ID:
	<CALZpt+ECDxM5mD3e0UjsS+r+E+xYLim-yUYoJ_P9Vpjk32_pPA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Zeeman


> What we can do is to add the actuary to the contract that
> controls the funds, but with the condition that the
> actuary signature has a specific `R`.

> As we know, `R` reuse --- creating a new signature for a
> different message but the same `R` --- will leak the
> private key.

> The actuary can be forced to put up an onchain bond.
> The bond can be spent using the private key of the actuary.
> If the actuary signs a transaction once, with a fixed `R`,
> then its private key is still safe.

> However, if the actuary signs one transaction that spends
> some transaction output, and then signs a different
> transaction that spends the same transaction output, both
> signatures need to use the same fixed `R`.
> Because of the `R` reuse, this lets anyone who expected
> one transaction to be confirmed, but finds that the other
> one was confirmed, to derive the secret key of the
> actuary from the two signatures, and then slash the bond
> of the actuary.

>From my understanding, if an off-chain state N1 with a negotiated group of
40 is halted in the middle of the actuary's R reveals due to the 40th
participant non-interactivity, there is no guarantee than a new off-chain
state N1' with a new negotiated group of 39 (from which evicted 40th's
output is absent) do not re-use R reveals on N1. So for the actuary bond
security,  I think the R reveal should only happen once all the group
participants have revealed their own signature. It sounds like some loose
interactivity is still assumed, i.e all the non-actuary participants must
be online at the same time, and lack of contribution is to blame as you
have a "flat" off-chain construction (i.e no layering of the promised
off-chain outputs in subgroups to lower novation interactivity).

More fundamentally, I think this actuarial system does not solve the
"multi-party off-chain state correction" problem as there is no guarantee
that the actuary does not slash the bond itself. And if the bond is guarded
by users' pubkeys, there is no guarantee that the user will cooperate after
the actuary equivocation is committed to sign a "fair" slashing transaction.

Best,
Antoine

Le sam. 9 sept. 2023 ? 02:28, ZmnSCPxj via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

>  (N > 2) Multiparticipant Offchain Mechanisms
>
> Introduction
> ============
>
> The blockchain layer of Bitcoin provides an excellent non-interactivity:
> users can go offline, then come online, synchronize, and broadcast
> transactions to the mempool.
> Always-online miners then get the transactions and add them to blocks,
> thereby confirming them.
>
> There are two important properties here:
>
> * Users do not need to be persistently online, only online when they
>   need to create and send a transaction.
> * Miners only dictate transaction ordering (i.e. which of two
>   conflicting transactions "comes first" and the second one is thus
>   invalid), and do ***not*** have custody of any user funds at all.
>
> Both properties are difficult to achieve for offchain mechanisms like
> 2-participant Lightning channels.
> But without these two properties, the requirement to be interative
> and thus always online creates additional friction in the use of the
> technology.
>
> When we move on from 2-participant offchain mechanisms ("channels")
> and towards N > 2, the interactivity problem is exacerbated.
> Generally, it is not possible to advance the state of an offchain
> mechanism that uses N-of-N signing without all users being online
> simultaneously.
>
> In this writeup, I present a new role that N-of-N offchain mechanisms
> can include.
> This role, the actuary role, is similar to the role of miners on the
> blockchain: they have high uptime (so users can connect to them to
> send a transaction "for confirmation") and they only decide
> transaction ordeering and do ***not*** have custody of the coins.
>
> Required Softforks
> ------------------
>
> To enable the actuary role I propose here, we need to have two
> softforks:
>
> * `SIGHASH_ANYPREVOUT`
> * `OP_CHECKSEPARATEDSIG`
>   - Instead of accepting `(R, s)` signature as a single stack item,
>     this accepts `s` and `R` as two separate stack items.
>
> I expect that neither is significantly controversial.
> Neither seems to modify miner incentives, and thus isolates the
> new role away from actual miners.
>
> I will describe later how both are used by the proposed mechanism.
>
> Actuaries In An N-of-N Offchain Mechanism
> =========================================
>
> Mechanisms like Decker-Wattenhofer, Poon-Dryja, and
> Decker-Russell-Osuntokun ("eltoo") can have an N-of-N signatory
> set.
> I will not discuss them deeply, other than to note that
> Decker-Russell-Osuntokun requires `SIGHAH_ANYPREVOUT`, supports
> N > 2 (unlike Poon-Dryja), and does not require significant
> number of transactions with varaible relative locktimes in the
> unilateral close case (unlike Decker-Wattenhofer).
>
> Using an N-of-N signatory set provides te following important
> advantage:
>
> * It is a consensus, not a democracy: everyone needs to agree.
>   - Thus, even a majority cannot force you to move funds you
>     own against your will.
>     The other side of "not your keys, not your coins" is
>     "your keys, your coins": if your key is necessary
>     because you are one of the N signatories, then funds inside
>     the mechanism are *your coins* and thus ***not*** custodial.
>
> The drawback of N-of-N signatories is that **all** N participants
> need to come together to sign a new state of the mechanism.
> If one of the N participants is offline, this stalls the protocol.
>
> An Offchain "Mempool"
> ---------------------
>
> At any time, an offchain mechanism such as Decker-Russell-Osuntokun
> will have a "current state", the latest set of transaction outputs
> that, if you unilateral close at that point, will be instantiated
> onchain.
>
> Thus, we can consider that the state of the mechanism is a set of
> pairs of Bitcoin SCRIPT and number of satoshis.
>
> These are instantiated as *actual* transaction outputs on some
> transaction that can be pushed onchain in a unilateral close
> situation.
>
> Suppose there are N (N > 2) participants in an offchain mechanism.
>
> Now suppose that one of the participants owns some funds in a
> simple single-sig contract in the current state of the offchain
> mechanism.
> Suppose that participant ("A") wants to send money to another
> participant ("B").
> Then participant A can "just" create an ordinary Bitcoin
> transaction that spends the appropriate transaction output from
> the current state, and sends money to participant B.
>
>     current state               +--------+--------------+
>     ---------+-----------+      |        |      A2      | (change output)
>              |     A     | ---> |        +--------------+
>              +-----------+      |        |      B2      |
>              |     B     |      +--------+--------------+
>              +-----------+
>              |     C     |
>     ---------+-----------+
>
> Now, B can "accept" this transaction is real, but ***only*** if
> B trusts A to not double-spend.
> Participant A can still construct a different transaction that
> spends that output but does ***not*** give any funds to
> participant B.
>
> Thus, this transaction is "unconfirmed", or in other words,
> would be in a "mempool" waiting to be confirmed.
>
> How do we "confirm" this transaction?
>
> In order to confirm this transaction, we apply the transaction
> to the current state of the mechanism: it is an atomic operation
> that deletes transaction output A and insersts two transaction
> outputs A2 and B2.
> This results in a new state.
> Then, all the participants (A, B, and C) need to sign off on the
> new state and invalidate the current state, replacing the current
> state to the new state.
>
> By moving to the new state, we effectively "cut through" the
> transactions that were in the "mempool" of the offchain mechanism.
> The cut-through transactions can then be forgotten forever, and
> more importantly ***do not have to be published to anyone***.
> Even a third party trying to validate the state of the offchain
> mechanism does **not** need to know about such old transactions
> that were already cut through.
> This is an important scaling property.
>
> Now, as mentioned above, the problem is that the N participants
> need to be online in order to advance the state and perform the
> cut-through.
> If one of the participants is offline, then none of the "mempool"
> transactions can confirm.
>
> So the question I raise now is: can we create a new role, an
> actuary, that is able to "confirm" transactions (i.e. indicate
> that a transction output has been spent by a specific
> transaction, and thus a conflicting transaction is no longer
> valid), but is otherwise unable to spend the funds (i.e.
> non-custodial)?
>
> K-of-N Non-Solution
> -------------------
>
> A common proposal is to have a federation of k-of-n that is
> trusted by participants.
>
> That way, even if some of the signatories are offline, the
> mechanism is "robust" in the sense that the state can still
> advance, and in-"mempool" transactions get "confirmed".
>
> The problem with this is that this is blatantly custodial.
> ***Any*** k-of-n mechanism ***MUST*** be custodial, as you
> cannot be sure that the k participants are actually not
> owned by a single participant which can now spend all your
> precious precious funds.
>
> Thus, this writeup completely rejects any k-of-n solution
> for state updates.
> We require that:
>
> * State updates are always signed N-of-N by all involved
>   participants.
> * Somehow we want to have a smaller threshold to *commit*
>   to having individual transactions in the *next* state,
>   and to reject double-spends of inputs to transactions
>   that have been committed.
>
> Actuary Role
> ------------
>
> Let us now define what we want the actuary role to be able
> to do and **NOT** do:
>
> * The actuary is able to select exactly one transaction
>   that spends a transaction output, i.e. it enforces
>   against double-spend.
> * The actuary is **NOT** able to spend funds unilaterally
>   by itslf, or with cooperation with participants that
>   do not otherwise have signing authorization for a
>   transaction output.
> * The actuary is **NOT** able to hostage funds, i.e. if
>   it stops responding, any single one participant can
>   drop the mechanism onchain and get actury-confirmed
>   (i.e. before the actuary stops responding) transactions
>   confirmed onchain, and thus able to recover their
>   funds.
>
> ### Ensuring Single-Spend
>
> We can have the actuary indicate that it has selected a
> transaction by also requiring that the actuary sign that
> transaction.
>
> We thus want to prevent the actuary from signing for the
> same output, but a different transaction.
>
> What we can do is to add the actuary to the contract that
> controls the funds, but with the condition that the
> actuary signature has a specific `R`.
>
> As we know, `R` reuse --- creating a new signature for a
> different message but the same `R` --- will leak the
> private key.
>
> The actuary can be forced to put up an onchain bond.
> The bond can be spent using the private key of the actuary.
> If the actuary signs a transaction once, with a fixed `R`,
> then its private key is still safe.
>
> However, if the actuary signs one transaction that spends
> some transaction output, and then signs a different
> transaction that spends the same transaction output, both
> signatures need to use the same fixed `R`.
> Because of the `R` reuse, this lets anyone who expected
> one transaction to be confirmed, but finds that the other
> one was confirmed, to derive the secret key of the
> actuary from the two signatures, and then slash the bond
> of the actuary.
>
> Thus, we need an `OP_CHECKSEPARATEDSIG` opcode.
> This takes three stack items, instead of two: `s`,
> `R`, and the public key.
>
> Then, an actual transaction output can indicate a specific
> `R` in a SCRIPT that includes `OP_CHECKSEPARATEDSIG`.
> This forces a specific `R` to be used, and thus requires
> the actuary to only sign once.
> This then enforces single-spend.
>
> ### Ensuring Non-Custodial
>
> This is simple: By ensuring that the onchain funding
> transaction output, which backs the entire mechanism, is
> an N-of-N of all participants, we can ensure that the
> actuary cannot spend the funds.
>
> Thus, by using N-of-N of all participants, we have
> consensus, and thus it is unnecessary for any participant
> to trust anyone else: they do not need to trust the
> actuary, or a quorum of signatories.
>
> As noted, this has the drawback that all N participants
> now need to sign off on each updtae of the offchain
> mechanism.
>
> However, the actuary serves a role:
>
> * While a new state is not yet signed off on by all
>   participants, it can sign individual transactions to
>   "confirm" them, with the assurance that they cannot
>   assist a double-spend since if they assist a
>   double-spend they lose their bond.
> * Participants can go online and offline at any time,
>   and the actuary can solicit and store their signatures
>   for to-be-next state.
>   Once it has solicited a complete N-of-N set for the
>   to-be-next state, it can then declare a new state and
>   hand the complete signature set to participants the
>   next time they come online.
>
> These reduce the onlineness requirement on participants.
>
> ### Ensuring Non-hostage
>
> We want the following property:
> If the actuary stops responding, then the participants
> can decide to drop the mechanism onchain, and recover
> their funds despite the actuary disappearing.
>
> Thus, the actuary cannot hostage the funds by refusing
> to confirm transactions: if the actuary refuses to
> confirm transactions, the participants can drop the
> mechanism onchain and just use the blockchain layer.
> This would suck, but the actuary still cannot hostage
> the funds held by the participants: the participants
> have a way to escape the mechanism.
>
> Crucially, we want the property that if we have some
> transactions that spend outputs from the current
> state, that were previously signed off by the actuary
> (i.e. "confirmed"), then when we drop onchain, we can
> drop those transactions onchain as well, with the
> assurance that other participants cannot replace them
> with an alternate version.
>
> To implement this, the SCRIPT of all outputs hosted
> inside the offchain mechanism are "infected" with
> `(sign-only-once(M) || CSV) && C`, where
> `M` is the actuary pubkey, `sign-only-once(M)` means
> that we enforce `R` reuse so that the actuary cannot
> sign the same output with different transactions
> (and thus ensure single-spend), and `C` is the
> "base", uninfected contract.
>
> For example, a hashlocked timelocked contract from A
> to B would have a "base" contract of:
>
>     (B && preimage(hash)) || (A && CLTV)
>
> And would have an "infected" contract of:
>
>     (sign-only-once(M) && CSV) && ((B && preimage(hash)) || (A && CLTV))
>
> For Taproot tapleaves, all tapleaves need to be infected.
> In addition, the `sign-only-once(M)` needs to use the same
> `R` for all tapleaves as well, so that signing for one
> branch cannot be used for another branch.
> The pointlocked branch cannot be used, but given current
> plans for `SIGHASH_ANYPREVOUT`, you need to sign
> `SIGHASH_ANYPREVOUT` because the actual transaction that
> gets confirmed can have a different transaction ID due to
> the Decker-Russell-Osuntokun.
>
> If the actaury stops responding, participants can
> publish the most recent state, as well as transactions
> that were "confirmed" by the actuary.
> Crucially, the transactions confirmed by the actuary
> have a time advantage, because they are signed by the
> actuary and we have a logical OR with the CSV;
> unconfirmed transactions need to wait for the CSV
> relative timeout before they can be confirmed onchain.
> Thus, if before it disappeared, the actuary signed some
> transactions and thus "confirmed" them, the participants
> can also confirm them onchain, and it is significantly
> less likely that another version of those transactions
> can get confirmed onchain in that situation.
> Thus, participants can rely on the "confirmation" of
> the actuary.
>
> Worked Example
> ==============
>
> Let us copy the initial state above, where there are three
> participants, A B C.
> In the below, M is the actuary, and the "M" here includes a
> fixed `R` nonce, to ensure that M can only sign once, and if
> M signs multiple times, it risks losing its bonded coins.
>
>     current state
>     ---------+-------------+
>              |(M||CSV) && A|
>              +-------------+
>              |(M||CSV) && B|
>              +-------------+
>              |(M||CSV) && C|
>     ---------+-------------+
>
> In the above, the "base" contracts are simple single-signature
> `A` / `B` / `C` conracts.
>
> While we show only `M`, in fact each `M` requirement also
> enforces single-spend for `M`.
> Each output also has a different `R` that is issused by the
> actuary.
>
> (for example, each participant can give the base contract
> serialization to the actuary, who then HMACs it with its own
> private key to generate a `r` then does `R = r * G`, so that
> the actuary does not need to remember the exact `R` each time,
> only whether it signed for a particular contract-amount pair.)
>
> Suppose that A decides to send some money to B.
> It creates a transaction spending the `A` output and creates
> two new outputs:
>
>     current state                  +--------+----------------+
>     ---------+-------------+       |        | (M||CSV) && A2 |
>              |(M||CSV) && A| ----> |    A   +----------------+
>              +-------------+       |        | (M||CSV) && B2 |
>              |(M||CSV) && B|       +--------+----------------+
>              +-------------+
>              |(M||CSV) && C|
>     ---------+-------------+
>
> In the above the `A` in the input side of the new transaction
> indicates a signature from participant A, fulfilling the base
> contract `A`.
>
> As the transaction is only signed by `A`, it is not yet
> confirmed.
> If the mechanism is dropped onchain, the participants must
> wait for the CSV timeout before it can be confirmed onchain,
> which reflects the fact that the transaction, inside the
> offchain mechanism, was not yet confirmed at this point.
>
> Now, suppose that participant A wants B to be assured that
> A will not double-spend the transaction.
> Then A solicits a single-spend signature from the actuary,
> getting a signature M:
>
>     current state                  +--------+----------------+
>     ---------+-------------+       |        | (M||CSV) && A2 |
>              |(M||CSV) && A| ----> |  M,A   +----------------+
>              +-------------+       |        | (M||CSV) && B2 |
>              |(M||CSV) && B|       +--------+----------------+
>              +-------------+
>              |(M||CSV) && C|
>     ---------+-------------+
>
> The above is now a confirmed transaction.
>
> Suppose at this point the offchain mechanism is dropped
> onchain.
> In that case, it is now immediately possible to also confirm
> the above transaction.
>
> Suppose that A tries to double-spend the transaction by signing
> another transaction spending the `A` output, but giving all of
> it to a new output `A3`.
> Because of the single-spend signature requirement, the actuary
> cannot safely sign this alternative version without losing its
> bonded amount.
>
>     current state                  +--------+----------------+
>     ---------+-------------+       |        | (M||CSV) && A2 |
>              |(M||CSV) && A| -+--> |  M,A   +----------------+
>              +-------------+  |    |        | (M||CSV) && B2 |
>              |(M||CSV) && B|  |    +--------+----------------+
>              +-------------+  |
>              |(M||CSV) && C|  |    +--------+----------------+
>     ---------+-------------+  +--> |    A   | (M||CSV) && A3 |
>                                    +--------+----------------+
>
> The transaction that is signed by the actuary M is the one that
> can be confirmed onchain immediately as soon as the current
> state transaction is confirmed, because the signature allows
> skipping the CSV requirement.
> However, the transaction that is signed only by participant A,
> in an attempt to double-spend the transaction, will need to
> wait out the CSV delay.
> The actuary M will never sign this alternate transaction, as
> `R` reuse will cause it to lose control of its private key and
> allow slashing of its bond.
>
> So, let us suppose that the actuary M decides to "cut through"
> the trasnaction it signed.
> The actuary M proposes to each of the participants to update
> the state of the offchain mechanism.
>
>     current state                  +--------+----------------+
>     ---------+-------------+       |        | (M||CSV) && A2 |
>              |(M||CSV) && A| ----> |  M,A   +----------------+
>              +-------------+       |        | (M||CSV) && B2 |
>              |(M||CSV) && B|       +--------+----------------+
>              +-------------+
>              |(M||CSV) && C|
>     ---------+-------------+
>
>     next state
>     ---------+----------------+
>              | (M||CSV) && A2 |
>     ---------+----------------+
>              | (M||CSV) && B2 |
>     ---------+----------------+
>              | (M||CSV) && B  |
>     ---------+----------------+
>              | (M||CSV) && C  |
>     ---------+----------------+
>
> It is not necessary for all the participants to come online
> simultaneously just to sign the new state.
> THe actuary can keep track of this new state on behalf of
> the participants, as well as the total signatures of all the
> N participants.
>
> Each participant still must validate that the next state
> contains the outputs they expect.
> However, they do not need to validate ***all*** outputs.
> For instance, participant C knows that it did not spend
> any funds, and did not receive any funds; it only cares
> that the next state still contains the `C` contract it
> expects.
> Participant A needs to validate the A2 and B2 exist,
> while participant B needs to validate the B2 and B outputs.
>
> ***This is important as it reduces the bandwidth requirements
> on the participants.***
> It is not necessary for the participants to validate *all*
> transactions, only that the participants validate the
> existence of outputs it expects to have been confirmed by
> the actaury.
> This is an important scaling advantage over e.g. a sidechain,
> where sidechain participants really ought to validate *all*
> transactions in the sidechain, not just the set they care
> about.
>
> Unlike the sidechain case, every participant needs to sign
> off on each state update.
> This means that as long as each participant does minimal
> protection of themselves, they can simply rely on the other
> participants being selfishly checking for their own expected
> outputs.
>
> If the actuary tries to cheat and create a next state that
> is not valid, then at least one participant will simply
> refuse to sign the next state, and drop the current state
> (and any transactions based on the current state) onchain.
> Thus, the N-of-N signatory set becomes an important
> optimization!
>
> In the above example, the actuary actually faithfully
> set the correct next state.
> So eventually all the participants get to go online and
> provide their signature shares, so that the mechanism
> advances and the next state becomes the current state:
>
>     current state
>     ---------+----------------+
>              | (M||CSV) && A2 |
>     ---------+----------------+
>              | (M||CSV) && B2 |
>     ---------+----------------+
>              | (M||CSV) && B  |
>     ---------+----------------+
>              | (M||CSV) && C  |
>     ---------+----------------+
>
> Against Custodiality
> ====================
>
> I think that people who want to actually improve Bitcoin
> MUST first strive as much as possible to ***avoid***
> custodians.
>
> Custodiality is easy.
>
> Escaping custody once you are custodied is almost impossible.
>
> Thus, it is important to ***avoid*** a custodial solution
> in our designs for Bitcoin.
>
> For example, Drivechains effectively makes miners the
> custodians of sidechain coins.
>
> Yes, there are incentives for miner custodians to not steal
> the sidechain coins.
>
> But far better to be able to say "it is not even possible for
> the miner to steal the coins in this mechanism at all".
>
> Do not give roles more rights than the minimum they absolute
> need to do their work!
> This is basic cybersecurity.
>
> We MUST avoid giving miners more control over **any** blockchain
> coins than what they already have.
> Miners currently can censor, and it is difficult to remove that
> ability without removing the ability to decide whether to confirm
> some transaction or not, since it is not possible to prove that
> you do not know a transaction.
> But currently miners cannot outright steal any funds.
>
> Giving more rights allows hackers who manage to take on the
> miner role (e.g. because the miner has bad opsec, or the hacker
> is the dictatorial warlord of the local government and has shot
> the miner to death and taken over their mine) to attack the
> system.
> Then, any analysis that "but miner roles have an incentive to
> not attack sidechains!" would not apply, as the hacker got the
> miner role outside of the normal miner expected incentives;
> the hacker incentives may not match the incentives of a "real"
> miner.
>
> Better if miners cannot attack at all, so that hackers that
> invalidly gain their role cannot attack, either.
>
> Similarly, the actuary role is given only the ability to decide
> to confirm or not confirm transactions.
> In particular the actuary role in this scheme is ***NOT***
> given the ability to move funds without consent of the purported
> owners of the value.
>
> This requires consensus, i.e. N-of-N signatories.
> However, the actuary is also overloaded so that it is the only
> entity that needs to have high uptime.
> Participants can drop online and offline, and the actuary
> coordinates the creation of new states.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230911/affe847b/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 14
********************************************
