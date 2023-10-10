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

   1. BitVM: Compute Anything on Bitcoin (Robin Linus)
   2. Re: BitVM: Compute Anything on Bitcoin (Anthony Towns)
   3. Re: BitVM: Compute Anything on Bitcoin (Lloyd Fournier)
   4. Re: BitVM: Compute Anything on Bitcoin (symphonicbtc)


----------------------------------------------------------------------

Message: 1
Date: Mon, 9 Oct 2023 15:46:24 +0200
From: Robin Linus <robin@zerosync.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] BitVM: Compute Anything on Bitcoin
Message-ID: <CCA561B6-A2DE-46FD-A2F8-98E0C34A3EEE@zerosync.org>
Content-Type: text/plain;	charset=utf-8

Abstract. BitVM is a computing paradigm to express Turing-complete Bitcoin contracts. This requires no changes to the network?s consensus rules. Rather than executing computations on Bitcoin, they are merely verified, similarly to optimistic rollups. A prover makes a claim that a given function evaluates for some particular inputs to some specific output. If that claim is false, then the verifier can perform a succinct fraud proof and punish the prover. Using this mechanism, any computable function can be verified on Bitcoin. Committing to a large program in a Taproot address requires significant amounts of off-chain computation and communication, however the resulting on-chain footprint is minimal. As long as both parties collaborate, they can perform arbitrarily complex, stateful off-chain computation, without leaving any trace in the chain. On-chain execution is required only in case of a dispute.

https://bitvm.org/bitvm.pdf

------------------------------

Message: 2
Date: Tue, 10 Oct 2023 11:27:08 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Robin Linus <robin@zerosync.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BitVM: Compute Anything on Bitcoin
Message-ID: <ZSSobP+VJSIeXE+U@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Mon, Oct 09, 2023 at 03:46:24PM +0200, Robin Linus via bitcoin-dev wrote:
> Abstract. BitVM is a computing paradigm to express Turing-complete
> Bitcoin contracts.

Please correct me if I'm wrong:

The way I understand this idea is that you take an N-bit claim (in the
given example N=4), and provide a NAND circuit that asserts whether
the claim is valid or not (in the example, if I did the maths right,
valid values take the form xxx0, 1x01, and only three bits were
actually needed). It would be very straightforward afaics to allow
for AND/OR/XOR/etc gates, or to have operations with more than two
inputs/one output.

The model is then a prover/challenger one: where the prover claims to
have a solution, and the verifier issues challenges that the prover
only be able to reply to consistently if the solution is correct. If
the prover doesn't meet the challenge, they lose the funds.

The circuit entails C individual assertions, with two inputs (selected
from either the N inputs bits, or the output of one of the previous
assertions) and a single output. You then encode each of those C
assertions as tapleafs, so that spending a tx via that tapleaf validates
that individual assertion.

You also have an additional tapleaf per input/assertion, that allows
the verifier to claim the funds immediately rather than issue another
challenge if the prover ever gave two inconsistent values for either an
input or the result of one of the assertions.

If the prover tries to cheat -- eg, claiming that 1111 is a valid input
in the example -- then the verifier can run the circuit themselves
offline, establish that it's an invalid, and work backwards from the
tip to establish the error. For example:

   TRUE=NAND(L,D)  -- D is true, so L better be false
   L=NAND(J,A) -- A is true, so J better be true for L to be false
   J=NAND(H,I) -- one of H or I must be false for J to be true,
     prover will have to pick. suppose they pick I.

   I=NAND(G,B) -- B is true, so if I was false, G was true
   G=NAND(A,C) -- can only pass at this point with some of A,C,G
     being given an inconsistent value

So you should need enough challenges to cover the longest circuit path
(call it P) in order to reliably invalidate an attempt to cheat. I guess
if your path isn't "branching" (ie one of the NAND inputs is something
you already have a commitment to) then you can skip back to something
that NAND's two "unknowns", at which point either one of the inputs is
wrong, and you trace it further down, or the output is correct, in which
case you can do a binary search across the NAND's where there wasn't
any branching, which should get you roughly to P=log(C) steps, at which
point you can do a billion gate circuit in ~100 on-chain transactions?

I think the "reponse enabled by challenge revealing a unique preimage"
approach allows you to do all the interesting work in the witness,
which then means you can pre-generate 2-of-2 signatures to ensure the
protocol is followed, without needing CTV/APO.

You'd need to exchange O(C*log(C)) hashes for the challenge hashes as
well as the 2*C commitment hashes, so if you wanted to limit that setup
to 20GB, then 24M gates would be about the max.

I think APO/CTV would let you avoid all the challenge hashes -- you'd
instead construct P challenge txs, and P*C response txs; with the output
of the C responses at level i being the i+1'th challenge, and each
of the tapscripts in the P challenges having a CTV-ish commitment to a
unique response tx. Still a lot of calculation, but less transfer needed.
You'd still need to transfer 2*C hashes for the commitments to each of
the assertions; but 20GB gets you a circuit with about ~300M gates then.

> It is inefficient to express functions in simple NAND circuits. Programs
> can be expressed more efficiently by using more high-level opcodes. E.g.,
> Bitcoin script supports adding 32-bit numbers, so we need no binary
> circuit for that.

I don't think that really works, though? You need a way of committing
to the 32-bit number in a way that allows proof of equivocation; but
without something like OP_CHECKFROMSTACK, I don't think we really have
that. You could certainly have 2**K hashes to allow a K-bit number,
but I think you'd have a hard time enumerating even three 16bit numbers
into a 4MB tapscript even.

CSFS-ish behaviour would let you make the commitments by signature,
so you wouldn't need to transfer hashes in advance at all, I think.

Cheers,
aj


------------------------------

Message: 3
Date: Tue, 10 Oct 2023 12:06:10 +1100
From: Lloyd Fournier <lloyd.fourn@gmail.com>
To: Robin Linus <robin@zerosync.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BitVM: Compute Anything on Bitcoin
Message-ID:
	<CAH5Bsr2XaUfYy+gPiSuQaMcxK43CNsR2apKYMTkF1sX3U9Jzbw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Robin,

Fascinating result.
Is it possible to give us an example of a protocol that uses BitVM that
couldn't otherwise be built? I'm guessing it's possible to exchange Bitcoin
to someone who can prove they know some input to a binary circuit that
gives some output.

Thanks!

LL

On Tue, 10 Oct 2023 at 01:05, Robin Linus via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Abstract. BitVM is a computing paradigm to express Turing-complete Bitcoin
> contracts. This requires no changes to the network?s consensus rules.
> Rather than executing computations on Bitcoin, they are merely verified,
> similarly to optimistic rollups. A prover makes a claim that a given
> function evaluates for some particular inputs to some specific output. If
> that claim is false, then the verifier can perform a succinct fraud proof
> and punish the prover. Using this mechanism, any computable function can be
> verified on Bitcoin. Committing to a large program in a Taproot address
> requires significant amounts of off-chain computation and communication,
> however the resulting on-chain footprint is minimal. As long as both
> parties collaborate, they can perform arbitrarily complex, stateful
> off-chain computation, without leaving any trace in the chain. On-chain
> execution is required only in case of a dispute.
>
> https://bitvm.org/bitvm.pdf
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231010/0c90da1e/attachment-0001.html>

------------------------------

Message: 4
Date: Tue, 10 Oct 2023 01:12:28 +0000
From: symphonicbtc <symphonicbtc@proton.me>
To: Robin Linus <robin@zerosync.org>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] BitVM: Compute Anything on Bitcoin
Message-ID:
	<HC0rwsiXAJBptIP0S-a5XNFcNAg5sk0ihUDHkjxfxbDiKZh9idX7UX4I73sZk2iHsXa5rVpI4_4m59B0hiDrYjXKh9wFwJvMZcH6GNZVMek=@proton.me>
	
Content-Type: text/plain; charset=utf-8

Hello Robin,

I'm very interested in this development, as I've been longing for arbitrary smart contracts on bitcoin for a while. I've got a couple questions I'd like to ask, on behalf of myself and some others I've been discussing this with.

1. Do you have plans to implement a high-level language that can compile down to this or maybe adapt some existing VM to make these scripts? I'm sure many would love to get their hands on something a bit more workable to test this out.

2. What are the expected computational costs of establishing the tapleaves for these scripts? Is it feasible to do complex things like ECDSA signature checking, etc? I worry that the hardware required to use this tech will be a barrier in it's widespread use.

3. Would it be possible to implement existing zero-knowledge proof constructs on BitVM, and would that make verification simpler? I.e. instead of verifying your program directly with BitVM, have your program be written in some ZKP VM, and just have the proof verification execute on BitVM

4. What are the expected costs of resolving a fraud for a program? I assume this is quite nuanced and has to do with the exact circumstances of the program, but would it be possible for you to provide some examples of how this might go down for some simple programs to aid comprehension?

Thanks,
Symphonic

Sent with Proton Mail secure email.

------- Original Message -------
On Monday, October 9th, 2023 at 1:46 PM, Robin Linus via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Abstract. BitVM is a computing paradigm to express Turing-complete Bitcoin contracts. This requires no changes to the network?s consensus rules. Rather than executing computations on Bitcoin, they are merely verified, similarly to optimistic rollups. A prover makes a claim that a given function evaluates for some particular inputs to some specific output. If that claim is false, then the verifier can perform a succinct fraud proof and punish the prover. Using this mechanism, any computable function can be verified on Bitcoin. Committing to a large program in a Taproot address requires significant amounts of off-chain computation and communication, however the resulting on-chain footprint is minimal. As long as both parties collaborate, they can perform arbitrarily complex, stateful off-chain computation, without leaving any trace in the chain. On-chain execution is required only in case of a dispute.
> 
> https://bitvm.org/bitvm.pdf
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 6
*******************************************
