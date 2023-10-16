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

   1. Re: Actuarial System To Reduce Interactivity In	N-of-N (N	>
      2) Multiparticipant Offchain Mechanisms (ZmnSCPxj)
   2. Re: BitVM: Compute Anything on Bitcoin (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Sun, 15 Oct 2023 13:36:00 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N	> 2) Multiparticipant Offchain Mechanisms
Message-ID:
	<6I7jG9PNNaWUZ8OnqAAQg0TJQ9PwGvD05iXYSOuN0XiezIJCChGlsxKZ30RwYfpeKlJyj7gB_rq1kPSR8UX6tOm-X7zanL_MXVrGEon3txc=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning list,

I have been thinking further on this with regards to BitVM.

By my initial analyses, it seems that BitVM *cannot* be used to improve this idea.

What we want is to be able to restrict the actuary to only signing for a particular spend exactly once.
The mechanism proposed in the original post is to force `R` reuse by fixing `R`.
This requires a change in Bitcoin consensus on top of `SIGHASH_ANYPREVOUT` (which is desirable not only for its enablement of Decker-Russell-Osuntokun, which is multiparticipant, but also makes it more convenient as we can make changes in the offchain mechanism state asynchronously with the participants and actuary signing off on new transactions; we can "lock" the next state to some set of transactions occurring, then have the actuary "confirm" new transactions by signing them, then have the signature still be valid on the new state due to `SIGHASH_ANYPREVOUT` ignoring the actual input transaction ID).

The best I have been able to come up with is to have a program that checks if two signatures sign different things but have the same public key.
If this program validates, then the actuary is known to have cheated and we can arrange for the actuary to lose funds if this program validates.
However, BitVM triggers on DIShonest execution of the program, so that program cannot be used as-is.
Honest execution of the program leads to the BitVM contract resolving via timeout.
I have tried to figure out some way to change the "polarity" of the logic so that the actuary is punished, but it requires that the actuary act as validator instead of prover (and the aggrieved participant who was expecting the actuary to not violate the sign-only-once is the prover, which makes little sense, as the participant can challenge the actuary and force it to put up funds, then neglect to actually prove anything and enter the default timeout case where the prover gets the funds --- it has to be the actuary in the prover position, only getting back its funds after a timeout).

The opposite of showing that there exists two signatures with different messages but the same public key is to show that there does not exist any other signatures with a different message but same public key.
If such a program were written, then it would be trivial to make that program pass by simply denying it an input of any other signature, and an actuary in prover position can always commit to an input that lacks the second signature it made.

The actuary can run a program *outside* of BitVM, so it is also pointless to have the signing algorithm be written in BitVM.

Finally, in the actuarial system, the actuary is supposed to provide *something* that would make a transaction be immediately confirmable, instead of after a timeout.
But in BitVM, the *something* that the prover provides that makes some transaction immediately confirmable is to provide a dishonest execution of a BitVM program; it is the timeout that is the honest execution of the BitVM program.
In addition, the actuary should be restricted so that it can only show this for *one* transaction, and not for any other transactions.
There are more possible dishonest executions of a BitVM program than just one, but only one honest execution, which is the opposite of what we want.

So, so far, I have not been able to figure out how to use BitVM to replace the current forced `R` reuse mechanism for preventing multiple times the actuary commits.


Regards,
ZmnSCPxj


------------------------------

Message: 2
Date: Sun, 15 Oct 2023 15:15:49 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Robin Linus <robin@zerosync.org>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] BitVM: Compute Anything on Bitcoin
Message-ID:
	<0J6o-j9oKRfD8-D3VURz4e1Ke8-DD3YhHQu4QvElrwd84meA1yvTs9KdQaTatpAfgXAPLfGn78MxitDT1AF76UE4yy53Ym6rOyy0B-4ey5k=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Robin et al,

It strikes me that it may be possible to Scriptless Script BitVM, replacing hashes and preimages with points and scalars.

For example, equivocation of bit commitments could be done by having the prover put a slashable fund behind a pubkey `P` (which is a point).
This slashable fund could be a 2-of-2 between prover and verifier `P && V`.

Then the prover provides a bit-0 point commitment `B`, which is a point.
If the prover wants to assert that this specific bit is 0, it has to provide `b` such that `B = b * G`.
If the prover wants to instead assert that this bit is 1, it has to provide `b + p` such that `B = b * G` and `P = p * G`.
If `b` (and therefore `B`) is chosen uniformly at random, if it makes exactly one of these assertions (that the bit is 0, or that the bit is 1) then it does not reveal `p`.
But if it equivocates and asserts both, it reveals `b` and `b + p` and the verifier can get the scalar `p`, which is also the private key behind `P` and thus can get the fund `P && V`.

To create a logic gate commitment, we have the prover and validator provide public keys for each input-possibility and each output-possibility, then use MuSig to combine them.
For example, suppose we have a NAND gate with inputs I, J and output K.
We have:

* `P[I=0]` and `V[I=0]`, which are the public keys to use if input I is 0.
* `P[I=1]` and `V[I=1]`, which are the public keys to use if input I is 1.
* ...similar for input `J` and output `K`.

In the actual SCRIPT, we take `MuSig(P[I=0], V[I=0])` etc.
For a SCRIPT to check what the value of `I` is, we would have something like:

```
OP_DUP <MuSig(P[I=1], V[I=1])> OP_CHECKSIG
OP_IF
  OP_DROP
  <1>
OP_ELSE
  <MuSig(P[I=0], V[I=0])> OP_CHECKSIGVERIFY
  <0>
OP_ENDIF
```

We would duplicate the above (with appropriate `OP_TOALTSTACK` and `OP_FROMALTSTACK`) for input `J` and output `K`, similar to Fig.2 in the paper.

The verifier then provides adaptor signatures, so that for `MuSig(P[I=1], V[I=1])` the prover can only complete the signature by revealing the `b + p` for `I`.
Similar for `MuSig(P[I=0], V[I=0])`, the verifier provides adaptor signatures so that the prover can only complete the signature by revealing the `b` for `I`.
And so on.
Thus, the prover can only execute the SCRIPT by revealing the correct commitments for `I`, `J`, and `K`, and any equivocation would reveal `p` and let the verifier slash the fund of `P`.

Providing the adaptor signatures replaces the "unlock" of the challenge-response phase, instead of requiring a preimage from the verifier.

The internal public key that hides the Taproot tree containing the above logic gate commitments could be `MuSig(P, V)` so that the verifier can stop and just take the funds by a single signature once it has learned `p` due to the prover equivocating.

Not really sure if this is super helpful or not.
Hashes are definitely less CPU to compute.

For example, would it be possible to have the Tapleaves be *just* the wires between NAND gates instead of NAND gates themselves?
So to prove a NAND gate operation with inputs `I` and `J` and output `K`, the prover would provide bit commitments `B` for `B[I]`, `B[J]`, and `B[K]`, and each tapleaf would be just the bit commitment SCRIPT for `I`, `J`, and `K`.
The prover would have to provide `I` and `J`, and commit to those, and then verifier would compute `K = ~(I & J)` and provide *only* the adaptor signature for `MuSig(P[K=<result>], V[K=<result>])`, but not the other side.

In that case, it may be possible to just collapse it down to `MuSig(P, V)` and have the verifier provide individual adaptor signatures.
For example, the verifier can first challenge the prover to commit to the value of `I` by providing two adaptor signatures for `MuSig(P, V)`, one for the scalar behind `B[I]` and the other for the scalar behind `B[I] + P`.
The prover completes one or the other, then the verifier moves on to `B[J]` and `B[J] + P`.
The prover completes one or the other, then the verifier now knows `I` and `J` and can compute the supposed output `K`, and provides only the adaptor signature for `MuSig(P, V)` for the scalar behind `B[K]` or `B[K] + P`, depending on whether `K` is 0 or 1.

That way, you only really actually need Schnorr signatures without having to use Tapleaves at all.
This would make BitVM completely invisible on the blockchain, even in a unilateral case where one of the prover or verifier stop responding.

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 10
********************************************
