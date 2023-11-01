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

   1. Re: Examining ScriptPubkeys in Bitcoin Script (Anthony Towns)
   2. Re: Actuarial System To Reduce Interactivity In	N-of-N (N >
      2) Multiparticipant Offchain Mechanisms (AdamISZ)


----------------------------------------------------------------------

Message: 1
Date: Tue, 31 Oct 2023 23:05:01 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Rusty Russell <rusty@rustcorp.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID: <ZUD7fZnrDb2GGvY5@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Sat, Oct 28, 2023 at 03:19:30PM +1030, Rusty Russell via bitcoin-dev wrote:

[Quoted text has been reordered]

> > I think there's two reasons to think about this approach:
> >  (a) we want to do vault operations specifically,

> I'm interested in vaults because they're a concrete example I can get my
> head around.  Not because I think they'll be widely used!

I don't think that's likely to make for a very productive discussion: we
shouldn't be changing consensus to support toy examples, after all. If
there's a *useful* thing to do that would be possible with similar
consensus changes, lets discuss that thing; if there's nothing useful
that needs these consensus changes, then lets discuss something useful
that doesn't need consensus changes instead.

To me, it seems pretty likely that if you're designing an API where
you don't expect anyone to actually use it for anything important, then
you're going to end up making pretty bad API -- after all, why put in
the effort to understand the use case and make a good API if you're sure
it will never be useful anyway?

There are some articles on API design that I quite like:

  https://ozlabs.org/~rusty/index.cgi/tech/2008-03-30.html
  https://ozlabs.org/~rusty/index.cgi/tech/2008-04-01.html

I'd rate the "lets have a mass of incomprehensible script that no one
really understands and is incredibly dangerous to modify, and just make it
a template" approach as somewhere between "3. Read the documentation and
you'll get it right" (at best) and "-5 Do it right and it will sometimes
break at runtime" (more likely).

Anyway, for the specific examples:

> But AFAICT there are multiple perfectly reasonable variants of vaults,
> too.  One would be:
>
> 1. master key can do anything
> 2. OR normal key can send back to vault addr without delay
> 3. OR normal key can do anything else after a delay.

I don't think there's any point having (2) here unless you're allowing for
consolidation transactions (two or more vault inputs spending to a single
output that's the same vault), which you've dismissed as a party trick.

> Another would be:
> 1. normal key can send to P2WPKH(master)
> 2. OR normal key can send to P2WPKH(normal key) after a delay.

I don't think there's any meaningful difference here between (2) here
and (3) above -- after the delay, you post one transaction spending
to p2wpkh(normal) signed by the normal key, then immediately post a
second transaction spending that new output, which is also signed with
the normal key, so you've just found a way of saying "normal key can do
anything else after a delay" that takes up more blockspace.

Both these approaches mirror the model that kanzure posted about in 2018
[0] (which can already be done via presigned transactions) and they share
the same fundamental flaw [1], namely that once someone compromises the
"normal key", all they have to do is wait for the legitimate owner to
trigger a spend, at which point they can steal the funds by racing the
owner, with the owner having no recourse beyond burning most of the
vault's funds to fees.

(I think the above two variants are meaningfully worse than kanzure's
in that someone with the normal key just needs to wait for the vault
utxo to age, at which point they can steal the funds immediately. In
kanzure's model, you first need to broadcast a trigger transaction,
then wait for it to age before funds can be stolen, which isn't the
greatest protection, but it at least adds some difficulty)

[0] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-August/017229.html
[1] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-August/017231.html
    also, https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020284.html

If you don't mind that flaw, you can setup a vault along the lines of
kanzure's design with BIP 345 fairly simply:

  A: ipk=master,
     tapscript=<normal> SWAP OVER CHECKSIGVERIFY 1 "CHECKSIGVERIFY 144 CSV" OP_VAULT
       (witness values: <revault-amt> <revault-idx> <spend-idx> <sig>)

  B: ipk=master
     tapscript=<normal> CHECKSIGVERIFY 144 CSV

You put funds into the vault by creating a utxo with address "A", at which
point you can do anything with the funds via the master key, or you can
trigger an unvault via the normal key, moving funds to address "B", which
then has a 144 block delay before it can be spent via the normal key.

That also natively supports vault spends that only include part of the
vault value, or that combine two or more (compatible) vaults into a
single payment.

To avoid the flaw, you need to precommit to the spend that you're
authorising, while still allowing clawback/recovery by the owner. One
way to make that work with BIP 345 is using BIP 119's CTV to force a
precommitment to the spend:

  A: ipk=master,
     tapscript=<masterspkhash> OP_VAULT_RECOVER
     tapscript=<normal> CHECKSIGVERIFY 1 "CTV DROP 144 CSV" OP_VAULT
       (witness values: <revault-amt> <revault-idx> <spend-idx> <spendcommit> <sig>)

  B: ipk=master
     tapscript=<masterspkhash> OP_VAULT_RECOVER
     tapscript=<spendcommit> CTV DROP 144 CSV

Once you have funds in the vault in address A, you can spend them directly
via a key path spend with the master private key, or you can make
them only spendable via the master key via the OP_VAULT_RECOVER path,
or you can do a precommitted spend via the OP_VAULT path by including
"spendcommit", the CTV hash of where you want to send funds to. That
moves funds into address B, which again can be recovered to the master
key via the first two paths, or after a day you can use the CTV path to
complete the vault withdrawal.

Again, that natively supports vault spends that only include part of
the vault value, or that combine two or more (compatible) vaults into
a single payment.

> Oh, oracles like this are the first CSFS use case I've heard of that
> doesn't seem like abusing signatures to do hashing; nice!
>
> (Seems like there should be a way to do this without CSFS, but I can't
> see it...)

It's not really a novel observation: oracles are the third item listed
on the optech topic page for CSFS [2]...

The scriptless way of getting similar functionality is via discreet
log contracts [3], where the oracle with public key P, picks an event,
publishes a unique (hardened) public key R for that event, and when
the outcome of the event (m) is known, publishes 's' such that sG = R +
H(R,P,m)*P, so that (R,s) is a valid BIP 340 schnorr signature for
message m and pubkey P. That can then be used via an adaptor signature
eg to make on-chain contracts [4], eg.

[2] https://bitcoinops.org/en/topics/op_checksigfromstack/

[3] https://www.dlc.wiki/
    https://bitcoinops.org/en/topics/discreet-log-contracts/

[4] https://suredbits.com/category/discreet-log-contracts/
    https://atomic.finance/blog/discreet-log-contracts/

Cheers,
aj


------------------------------

Message: 2
Date: Tue, 31 Oct 2023 22:12:20 +0000
From: AdamISZ <AdamISZ@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N > 2) Multiparticipant Offchain Mechanisms
Message-ID:
	<kUmZIImH6VJ8pd1WdqSJiWtNIIuKAI7ZxvUUH2_DPHOZofN1zcZK_mJXBSGlKQ2OoSevQIVBWcZkH1m1oFCrBDPdzkIE9UjxZLbQ-RvUJcU=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Antoine, Zman and list,

The whole line of thinking here is interesting but indeed my first question was "who does the penalty of the actuary go to?" and yeah, it seems we're still fairly stuck there.

re:

> However, the amount of satoshis that should be locked in such fidelity bonds must be equal to the counterparty initial balance multiplied by the remaining counterparties, as one can cheat against every other party (assuming there is no shared communication channel where equivocation can be observed). E.g if your factory has 1000 participants and your balance is 10 000 satoshis, you *must* lock up 10 000 000 in fidelity bonds while only 1 / 1000th of the amount can be leveraged as off-chain contract or payment.

.. just wanted to point out that I was able to address this in PathCoin [1]. I found a way to avoid the linear dependence of total fidelity bond on number of participants, but only under severe restriction: using CTV/covenant (not so severe), but also, fixing order of transfer (ultra severe!). i.e. a coin of 10k sats only needs a lock up of 10k + delta sats from each participant that spends it (if you don't spend it then of course you don't strictly need to lock up anything).

the mechanism is, whimsically, similar to a series of airlocks: each scriptPubKey looks like [(A and CLTV) OR (T_A and CTV)] -> [(B and CLTV) OR (H(B) and T_A and CTV)] -> [(C and CLTV) OR (H(C) and T_A and CTV)] -> ...

The arrows -> indicate what the CTV points to; T_A is a point corresponding to an adaptor t_A, so that a spend of the pathcoin to A reveals t_A, the privkey of T_A, and the H() terms are locks, so that, when B transfers the pathcoin to C, he also transfers the preimage of H(B), so that the second scriptPubKey above can be spent to the third immediately, because C knows the preimage of H(B) as well as t_A as per previous.

Clearly, in a more flexible design, this might not be super interesting, but perhaps it gives a clue on a direction forward.

I tried to look for "reuse pathcoin fidelity bonds/penalty bonds across different pathcoins in parallel or in series" ideas but I continually hit against the same character of problems as you describe here, either double spend problems, or collusion problems. Only the above ultra-simple fixed-path seems to be stable.

I do have a suspicion that APO can indeed be a big part of any solution to this thorny problem (haven't thought about it for a while).

[1] https://gist.github.com/AdamISZ/b462838cbc8cc06aae0c15610502e4da

Cheers,
waxwing/AdamISZ



Sent with Proton Mail secure email.

------- Original Message -------
On Wednesday, 4 October 2023 at 20:12, Antoine Riard via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Hi Zeeman,
> > Basically, the big issue is that the actuary needs to bond a significant amount of funds to each participant, and that bond is not part of the funding of the construction.
> >
> > Other ways of ensuring single-use can be replaced, if that is possible.
> > Do you know of any?
> 
> As explained in the other post, if you wish to ensure lack of equivocation of an off-chain state I think you're left between updating dynamically the subgroup of balance keys *on-chain* (i.e use the blockchain as an anti-double spend oracle) or ensure any equivocation can be punished as soon as one party gains knowledge of two commitment signatures.
> 
> I think you can design a fraud proof system encumbering each channel factory or pool balance by leveraging OP_CHECKSIGFROMSTACK and the spent outpoint committed as a partial transaction template. However, the amount of satoshis that should be locked in such fidelity bonds must be equal to the counterparty initial balance multiplied by the remaining counterparties, as one can cheat against every other party (assuming there is no shared communication channel where equivocation can be observed).
> 
> E.g if your factory has 1000 participants and your balance is 10 000 satoshis, you *must* lock up 10 000 000 in fidelity bonds while only 1 / 1000th of the amount can be leveraged as off-chain contract or payment.
> 
> Of course pre-nominated coordinator reduces the burden from the full *flat* fidelity bond, though it has to be weighed with coordinator unavailability occurence where each participant has to withdraw his balance on-chain, and bears the fee cost.
> 
> Best,
> Antoine
> 
> Le mar. 12 sept. 2023 ? 10:41, ZmnSCPxj <ZmnSCPxj@protonmail.com> a ?crit :
> 
> > Good morning Antoine,
> > 
> > 
> > > Hi Zeeman
> > >
> > > > What we can do is to add the actuary to the contract that
> > > > controls the funds, but with the condition that the
> > > > actuary signature has a specific `R`.
> > >
> > > > As we know, `R` reuse --- creating a new signature for a
> > > > different message but the same `R` --- will leak the
> > > > private key.
> > >
> > > > The actuary can be forced to put up an onchain bond.
> > > > The bond can be spent using the private key of the actuary.
> > > > If the actuary signs a transaction once, with a fixed `R`,
> > > > then its private key is still safe.
> > >
> > > > However, if the actuary signs one transaction that spends
> > > > some transaction output, and then signs a different
> > > > transaction that spends the same transaction output, both
> > > > signatures need to use the same fixed `R`.
> > > > Because of the `R` reuse, this lets anyone who expected
> > > > one transaction to be confirmed, but finds that the other
> > > > one was confirmed, to derive the secret key of the
> > > > actuary from the two signatures, and then slash the bond
> > > > of the actuary.
> > >
> > > From my understanding, if an off-chain state N1 with a negotiated group of 40 is halted in the middle of the actuary's R reveals due to the 40th participant non-interactivity, there is no guarantee than a new off-chain state N1' with a new negotiated group of 39 (from which evicted 40th's output is absent) do not re-use R reveals on N1. So for the actuary bond security, I think the R reveal should only happen once all the group participants have revealed their own signature. It sounds like some loose interactivity is still assumed, i.e all the non-actuary participants must be online at the same time, and lack of contribution is to blame as you have a "flat" off-chain construction (i.e no layering of the promised off-chain outputs in subgroups to lower novation interactivity).
> > 
> > Yes, there is some loose interactivity assumed.
> > 
> > However:
> > 
> > * The actuary is always online and can gather signatures for the next state in parallel with signing new transactions on top of the next state.
> > * This is why `SIGHASH_ANYPREVOUT` is needed, as the transactions on top of the next state might spend either the actual next state (if the next state is successfully signed), or the current state plus additional transactions (i.e. the transaction that move from current state to next state) (if the next state fails to get fully signed and the participants decide to give up on the next state getting signed).
> > 
> > > More fundamentally, I think this actuarial system does not solve the "multi-party off-chain state correction" problem as there is no guarantee that the actuary does not slash the bond itself. And if the bond is guarded by users' pubkeys, there is no guarantee that the user will cooperate after the actuary equivocation is committed to sign a "fair" slashing transaction.
> > 
> > Indeed.
> > 
> > One can consider that the participants other than the actuary would generate a single public key known by the participants.
> > But then only one sockpuppet of the actuary is needed to add to the participant set.
> > 
> > Basically, the big issue is that the actuary needs to bond a significant amount of funds to each participant, and that bond is not part of the funding of the construction.
> > 
> > Other ways of ensuring single-use can be replaced, if that is possible.
> > Do you know of any?
> > 
> > Regards,
> > ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 1
*******************************************
