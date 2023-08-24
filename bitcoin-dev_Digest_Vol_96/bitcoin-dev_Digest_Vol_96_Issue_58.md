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

   1. Re: Ark: An Alternative Privacy-preserving Second	Layer
      Solution (adiabat)
   2. Re: Ark: An Alternative Privacy-preserving Second Layer
      Solution (David A. Harding)


----------------------------------------------------------------------

Message: 1
Date: Wed, 24 May 2023 16:20:35 -0400
From: adiabat <rx@awsomnet.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second	Layer Solution
Message-ID:
	<CAKEeUhg1qeZOv-Lk8SSTxdkgfSee_E6_4fwNV=hfwsxLgwWkUw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi - thanks for the Ark write up; I have a bunch of questions but here's 2:

---
Q1:
"Pool transactions are created by ark service providers perpetually
every 5 seconds"

What exactly happens every 5 seconds?  From the 15.44.21-p-1080.png
diagram [1], a pool transaction is a bitcoin transaction, with all the
inputs coming from the ASP.  My understanding is that every 5 seconds,
we progress from PoolTx(N) to PoolTx(N+1).  Does the ASP sign a new
transaction which spends the same ASP funding inputs as the previous
pool transaction, which is a double spend or fee bump?  Or does it
spend the outputs from the previous PoolTx?

In other words, does PoolTx(2) replace PoolTx(1) RBF-style, spending
the same inputs (call this method A), or does PoolTx(2) spend an
output Of Pooltx(1) such that PoolTx(1) must be confirmed in order for
PoolTx(2) to become valid (method B)?  Or are they completely separate
transactions with unconflicting inputs (method C)?

When the ASP creates a pool transaction, what do they do with it?  Do
they broadcast it to the gossip network?  Or share it with other pool
participants?

With method A, if the ASP shares pool transactions with other people,
there Doesn't seem to be any way to ensure which PoolTx gets
confirmed, invalidating all the other ones.  They're all valid so
whichever gets into a block first wins.

With method B, there seems to be a large on-chain load, with ~120
chained transactions trying to get in every block. This wouldn't play
nicely with mempool standardness and doesn't seem like you could ever
"catch up".

With method C, ASPs would need a pretty large number of inputs but
could recycle them as blocks confirm.  It would cost a lot but maybe
could work.

---
Q2:

The other part I'm missing is: what prevents the ASP from taking all
the money?  Before even getting to vTXOs and connector outputs, from
the diagram there are only ASP inputs funding the pool transaction.
If the pool transaction is confirmed, the vTXOs are locked in place,
since the vTXO output cannot be changed and commits to all
"constrained outs" via OP_CTV.  If the pool transaction is
unconfirmed, the ASP can create & sign a transaction spending all ASP
funding inputs sending the money back to the ASP, or anywhere else.
In this case, users don't have any assurance that their vTXO can ever
turn into a real UTXO; the ASP can "rug-pull" at any time, taking all
the money in the pool.  Adding other inputs not controlled by the ASP
to the transaction wouldn't seem to fix the problem, because then any
user removing their inputs would cancel the whole transaction.

More detail about how these transactions work would be appreciated, thanks!

-Tadge

[1] https://uploads-ssl.webflow.com/645ae2e299ba34372614141d/6467d1f1bf91e0bf2c2eddef_Screen%20Shot%202023-05-19%20at%2015.44.21-p-1080.png


------------------------------

Message: 2
Date: Wed, 24 May 2023 13:02:40 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Burak Keceli <burak@buraks.blog>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second Layer Solution
Message-ID: <3c6c3b8b562bb56bbb855dc2b2b71f78@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

Hi Burak,

Thanks for this really interesting protocol!  I tend to analyze
complicated ideas like this by writing about them in my own words, so
I've pasted my summary of your idea to the end of this email in case
it's useful, either to other people or to you in helping understand my
one concern.

My concern is the same one I think Olaoluwa Osuntokun mentioned on
Twitter[1] and (less clear to me) might be related to ZmnSCPxj's
concern[2]:

It seems to me that receiving a payment on the protocol, including
conditional payments using HTLC, PTLC, or Anchor-TLC, requires waiting
for the transaction containing that payment to confirm to a sufficient
depth (e.g., I'd wait 6 blocks for small payments and longer for huge
payments).  Am I missing something?

My summary of how I think that part of the protocol works is in the
sections labeled "Make an unconditioned payment" and "Make a conditional
payment" below.  In short, it's clear to me how the service provider and
the customer can make instant atomic swaps with each other---they can
either spend instantly cooperatively, or they have to wait for a
timeout.  But how can a receiver of funds be assured that they will
actually get those funds unless there's already a timelock and
cooperative spend path placed on those funds?

-Dave

Rough initial summary of Ark protocol:

Alice runs an Ark service provider.  Every 5 seconds, she broadcasts a
new unconfirmed onchain transaction that pays three outputs (the
three Cs):

1. *Change Output:* money not used for the other two Cs that gets sent
    back to the the transaction creator.

2. *Connector Output:* an output that will be used in a future
    transaction created by Alice as protection against double spends.

3. *Commitment Output:* a CTV-style commitment to a set of outputs that
    can be published later in a descendant transaction (alternatively,
    the commitment output may be spent unilaterally by Alice after 4
    weeks).

Bob wants to deposit 1 BTC with Alice.  He sends her an unsigned PSBT
with an input of his and a change output.  She updates the PSBT with a
commitment output that refunds Bob the 1 BTC and a connector output with
some minimum value.  They both sign the PBST and it is broadcast.  We'll
ignore fees in our examples, both onchain transaction fees and fees paid
to Alice.

 From here, there are several things that Bob can do:

- *Unilaterally withdraw:* Bob can spend from the commitment output to
   put his refund onchain.  The refund can only be spent after a 24-hour
   time delay, allowing Bob to optionally come to an agreement with Alice
   about how to spend the funds before Bob can spend them unilaterally
   (as we'll see in a moment).  For example, the script might be[3]:

     pk(B) && (older(1 day) || pk(A))

- *Collaboratively withdraw:* as seen above, Bob has the ability to come
   to a trustless agreement with Alice about how to spend his funds.
   They can use that ability to allow Bob to trade his (unpublished) UTXO
   for a UTXO that Alice funds and broadcasts.  For example:

     - Alice creates an unsigned PSBT that uses as one of its inputs the
       connector from Bob's deposit transaction.  This will ensure that
       any attempt by Bob to double-spend his deposit transaction will
       invalidate this withdrawal transaction, preventing Bob from being
       able to steal any of Alice's funds.

         Also included in Alice's unsigned PSBT is another connector
         output plus the output that pays Bob his 1 BTC.

     - Bob receives Alice's unsigned PSBT and creates a separate PSBT
       that includes his unpublished UTXO as an input, giving its value
       to Alice in an output.  The PSBT also includes as an input the
       connector output from Alice's PSBT.  This will ensure that any
       attempt by Alice to double spend her transaction paying him will
       invalidate his transaction paying her.

     - Bob signs his PSBT and gives it to Alice.  After verifying it,
       Alice signs her PSBT and broadcasts it.

- *Collaboratively trade commitments:* as mentioned, the commitment
   output that pays Bob may be claimed instead by Alice after 4 weeks, so
   Bob will need to either withdraw or obtain a new commitment within 
that
   time.  To trade his existing commitment for a new commitment looks
   similar to the collaborative withdrawal procedure but without the
   creation of an immediately-spendable onchain output:

     - Alice creates an unsigned PSBT that uses as one of its inputs the
       connector from Bob's deposit transaction, again preventing double
       spending by Bob.  Alice also includes a new connector and a new
       commitment that again allows Bob to later claim 1 BTC.

     - Bob receives Alice's PSBT and creates a PSBT transferring his
       existing commitment to her, with the new connector again being
       included as an input to ensure atomicity.

     - Bob signs; Alice signs and broadcasts.

- *Make an unconditioned payment:* using the mechanisms described above,
   it's possible to make either an onchain payment or an offchain
   payment---just have Carol receive the new output or commitment rather
   than Bob.  That payment would have no conditions (except its
   atomicity).

- *Make a conditional payment:* imagine that Carol knows a secret (e.g.
   a preimage) that Bob is willing to pay for.

      - Alice creates an unsigned PSBT depending on the connector from
        Bob's deposit transaction and creating a new connector.  The PSBT
        includes an output paying Carol (either onchain or via a
        commitment) with an HTLC, allowing Carol to claim the funds if 
she
        reveals the secret or allowing Bob to claim the funds after a
        timeout.

      - Bob receives Alice's PSBT and creates a PSBT transferring his
        existing commitment to her with the HTLC condition attached and,
        again, with connectors being used to ensure atomicity.

      - Bob signs; Alice signs and broadcasts.

      - Carol can settle her HTLC by either revealing the secret onchain
        or by trading her commitment containing the HTLC clause for a
        commitment from Alice that doesn't contain the clause (which
        Alice will only accept by learning the secret, since Alice has
        to settle with Bob).  Alice can then either settle onchain or
        trade commitments with Bob after giving him the secret.

- *Do nothing for 4 weeks:* if Bob does nothing for four weeks, Alice
   can claim the funds from the commitment output (i.e., takes his
   money).

     If Bob did actually do something, and if every other user who also
     had an unpublished output in the commitment transaction did
     something, then they all exchanged their portion of the funds in
     this output to Alice, so Alice can now claim all of those funds
     onchain in a highly efficient manner.

Regarding the connector outputs, although all of the examples above show
Alice directly spending from the connector output in Bob's deposit
transaction, atomicity is also ensured if Alice spends from any output
descended from Bob's connector output.  Connector outputs from different
deposits can be used as inputs into the same transaction, merging their
histories.  This allows all operations made by Alice to be fully atomic,
ensuring that she doesn't lose any money during a reorg of any length.

Users are not so well protected during reorgs, e.g. if Bob double-spends
a transaction whose funds were later used in a payment to Carol, then
Carol loses the money.  For this reason, Alice will probably want to
prove to users that no funds they receive in a payment derive from any
deposit less than safe_confirmation_depth blocks.

[1] https://twitter.com/roasbeef/status/1661266771784126464

[2] 
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-May/021710.html

[3] 
https://min.sc/#c=pk%28B%29%20%26%26%20%28older%281%20day%29%20%7C%7C%20pk%28A%29%29


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 58
*******************************************
