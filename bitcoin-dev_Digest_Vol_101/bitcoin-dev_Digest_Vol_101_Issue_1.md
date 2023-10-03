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

   1. Re: MATT: [demo] Optimistic execution of arbitrary programs
      (Anthony Towns)
   2. Re: MATT: [demo] Optimistic execution of arbitrary	programs
      (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Tue, 3 Oct 2023 01:10:08 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Johan Tor?s Halseth <johanth@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] MATT: [demo] Optimistic execution of
	arbitrary programs
Message-ID: <ZRrdULpZ2nYaDOV7@erisian.com.au>
Content-Type: text/plain; charset=iso-8859-1

On Fri, Sep 29, 2023 at 03:14:25PM +0200, Johan Tor?s Halseth via bitcoin-dev wrote:
> TLDR; Using the proposed opcode OP_CHECKCONTRACTVERIFY and OP_CAT, we
> show to trace execution of the program `multiply` [1] and challenge
> this computation in O(n logn) on-chain transactions:

"O(n log n)" sounds wrong? Isn't it O(P + log(N)) where P is the size
of the program, and N is the number of steps (rounded up to a power of 2)?

You say:

> node = h( start_pc|start_i|start_x|end_pc|end_i|end_x|h( h(sub_node1)|h(sub_node2) )

But I don't think that works -- I think you want to know h(sub_node1)
and h(sub_node2) directly, so that you can compare them to the results
you get if you run the computation, and choose the one that's incorrect.
Otherwise you've got a 50/50 chance of choosing the subnode that's
actually correct, and you'll only be able to prove a mistake with
1/2**N odds?

Not a big change, it just becomes 32B longer (and drops some h()s):

  node = start_pc|start_i|start_x|end_pc|end_i|end_x|h(sub_node1)|h(sub_node2)
  leaf = start_pc|start_i|start_x|end_pc|end_i|end_x|null

I'm not seeing what forces the prover to come up with a balanced state
tree -- if they don't have to have a balanced tree, then I think there
are many possible trees for the same execution trace, and again it would
become easy to hide an error somewhere the challenger can't find. Adding a
"start_stepcount" and "end_stepcount" would probably remedy that?

There seems to be an error in the "what this would look like for 4 state
transitions" diagram -- the second node should read "0|0|2 -> 0|1|4"
(combining its two children), not "0|0|2 -> 1|0|2" matching its left
child.

I'm presuming that the counterparty verifies they know the program (ie,
all the leaves in the contract taptree) before agreeing to the contract
in the first place. I think that's fine.

Cheers,
aj



------------------------------

Message: 2
Date: Tue, 3 Oct 2023 09:53:08 +0200
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Anthony Towns <aj@erisian.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] MATT: [demo] Optimistic execution of
	arbitrary	programs
Message-ID:
	<CAD3i26BKejHjQ5-+H=oC6FzF7RAP-2keW1iwo8TY+FEoGNwk3Q@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi, aj. Thanks for taking a look!

> "O(n log n)" sounds wrong? Isn't it O(P + log(N)) where P is the size
> of the program, and N is the number of steps (rounded up to a power of 2)?

Thanks, you are right. That's a typo, it should indeed be O(log n). n
being the number of steps in the program. I think P doesn't matter
here, as we never put the whole program on-chain, just break it down
into n steps.

> > node = h( start_pc|start_i|start_x|end_pc|end_i|end_x|h( h(sub_node1)|h(sub_node2) )
> But I don't think that works -- I think you want to know h(sub_node1)
> and h(sub_node2) directly, so that you can compare them to the results
> you get if you run the computation, and choose the one that's incorrect.

This denotes only how to create the commitment. When we traverse the
tree, the node scripts enforce that h(sub_n
ode{1,2}) that is consistent with the commitment is in the witness,
achieving exactly what you suggest.

> I'm not seeing what forces the prover to come up with a balanced state
> tree

To achieve this the participants agree up front (when the contract is
created) what is the exact length of the trace (or equivalent the
depth of the tree). If the actual execution is shorter, we fill the
rest with no-ops.

This means that we know the moment the challenge protocol starts the
transactions that are going to be played (kinda like a CTV tree), so
if one of the participants creates a trace from a non-balanced state
tree, it will be rejected by the script at that level. It is indeed
important that the state tree is built in a deterministic way.

> There seems to be an error in the "what this would look like for 4 state
> transitions" diagram -- the second node should read "0|0|2 -> 0|1|4"

Yes, fixed! Thanks :)

- Johan


On Mon, Oct 2, 2023 at 5:10?PM Anthony Towns <aj@erisian.com.au> wrote:
>
> On Fri, Sep 29, 2023 at 03:14:25PM +0200, Johan Tor?s Halseth via bitcoin-dev wrote:
> > TLDR; Using the proposed opcode OP_CHECKCONTRACTVERIFY and OP_CAT, we
> > show to trace execution of the program `multiply` [1] and challenge
> > this computation in O(n logn) on-chain transactions:
>
> "O(n log n)" sounds wrong? Isn't it O(P + log(N)) where P is the size
> of the program, and N is the number of steps (rounded up to a power of 2)?
>
> You say:
>
> > node = h( start_pc|start_i|start_x|end_pc|end_i|end_x|h( h(sub_node1)|h(sub_node2) )
>
> But I don't think that works -- I think you want to know h(sub_node1)
> and h(sub_node2) directly, so that you can compare them to the results
> you get if you run the computation, and choose the one that's incorrect.
> Otherwise you've got a 50/50 chance of choosing the subnode that's
> actually correct, and you'll only be able to prove a mistake with
> 1/2**N odds?
>
> Not a big change, it just becomes 32B longer (and drops some h()s):
>
>   node = start_pc|start_i|start_x|end_pc|end_i|end_x|h(sub_node1)|h(sub_node2)
>   leaf = start_pc|start_i|start_x|end_pc|end_i|end_x|null
>
> I'm not seeing what forces the prover to come up with a balanced state
> tree -- if they don't have to have a balanced tree, then I think there
> are many possible trees for the same execution trace, and again it would
> become easy to hide an error somewhere the challenger can't find. Adding a
> "start_stepcount" and "end_stepcount" would probably remedy that?
>
> There seems to be an error in the "what this would look like for 4 state
> transitions" diagram -- the second node should read "0|0|2 -> 0|1|4"
> (combining its two children), not "0|0|2 -> 1|0|2" matching its left
> child.
>
> I'm presuming that the counterparty verifies they know the program (ie,
> all the leaves in the contract taptree) before agreeing to the contract
> in the first place. I think that's fine.
>
> Cheers,
> aj
>


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 1
*******************************************
