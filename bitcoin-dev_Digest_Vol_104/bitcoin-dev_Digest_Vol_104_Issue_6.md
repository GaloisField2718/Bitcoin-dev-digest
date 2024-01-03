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

   1. Re: Swift Activation - CTV (Erik Aronesty)
   2. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Peter Todd)
   3. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Peter Todd)
   4. Re: Swift Activation - CTV (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Tue, 2 Jan 2024 09:32:29 -0500
From: Erik Aronesty <erik@q32.com>
To: Michael Folkson <michaelfolkson@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Anthony Towns
	<aj@erisian.com.au>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<CAJowKgK4nQWjaJ96P-E1yABCVOnTxyAGEwuYFUa9WRD8=6U4TA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Tue, Jan 2, 2024, 8:52 AM Michael Folkson <michaelfolkson@protonmail.com>
wrote:

> In the interests of time I'll just pick two to respond to but I don't
> agree with any of your points.
>
> > Covenants allow trustless utxos sharing and also are needed for
> vaulting. The numerous use cases are documented, built out and on signet to
> my knowledge. Check out utxos.org for a good list
>
> Your knowledge is incorrect. As far as I know in the getting on for 2
> years since the first CTV activation talk/attempt literally no one has
> built out a CTV use case and demonstrated it on signet with the possible
> exception of James O'Beirne's OP_VAULT which requires other new opcodes in
> addition to CTV.
>

Nice example, thanks.

>
> > 4. "Best tool for the job" is not the bar. "Safe for all" and "useful
> for some" is the bar.
>

This is the bar, ant CTV has passed it with vaulting alone.

If you want to avoid a chain split with an activation attempt (it is
> possible you don't care but if you do) you have to address concerns others
> have with a particular proposal.
>

You haven't mentioned one safety concern.  It's hard to tell if you have
any.  There is, of course, the elephant in the room with CTV that is a true
concern that nobody talks about.

The real danger of CTV isn't whether it's the best, and we know it's
nonrecursive.  And we can use BIP8, so that isn't an issue either.

And we already have shitcoins on BTC, so sapio shouldn't be your issue (
https://github.com/sapio-lang/sapio)

Why exactly is your problem?  You yourself have admitted it's useful for
vaulting, and for reducing the cost of lightning onboarding, even though
you ignored the dozens of other use cases enumerated in detail on utxos.org
and elsewhere.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240102/f37629d1/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 2 Jan 2024 23:18:11 +0000
From: Peter Todd <pete@petertodd.org>
To: Gloria Zhao <gloriajzhao@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Greg Sanders
	<gsanders87@gmail.com>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID: <ZZSZs16f1q6i3oLV@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Jan 02, 2024 at 11:12:05AM +0000, Gloria Zhao wrote:
> Hi Peter,
> 
> > You make a good point that the commitment transaction also needs to be
> included
> > in my calculations. But you are incorrect about the size of them.
> 
> > With taproot and ephemeral anchors, a typical commitment transaction
> would have
> > a single-sig input (musig), two taproot outputs, and an ephemeral anchor
> > output.  Such a transaction is only 162vB, much less than 1000vB.
> 
> Note that these scenarios are much less interesting for commitment
> transactions with no HTLC outputs, so 162 isn't what I would use for the
> minimum.

What scenarios you consider "interesting" is not relevant. You can't pick an
arbitrary minimum based on an interesting scenario. You should pick an actual
relevant minimum.

So with that in mind, let's ask the question: Do we think it's common for
channels to be force closed without HTLCs pending? I believe the answer is
likely to be yes, because channels are only used some of the time.

Can we verify that? Well, I just checked my node, and out of the past 15 force
closes, 12 had no HTLCs outstanding. 2 had one HTLC outstanding, and 1 had 2
HTLCs.

I also checked a big node I'm connected to, fixedfloat. Again, out of the past
15 force closes, 11 had no HTLCs outstanding, with 4 having 1 HTLC
outstanding... but of those only 2 HTLCs were profitable to collect. The other
half cost more money in fees than the HTLC value.

Looks to me like the supermajority of force closes are the most boring type.
And those numbers would be even more tilted in that direction if Lightning
implementations had better economics management.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240102/86b1a36f/attachment-0001.sig>

------------------------------

Message: 3
Date: Tue, 2 Jan 2024 23:43:01 +0000
From: Peter Todd <pete@petertodd.org>
To: Gloria Zhao <gloriajzhao@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Greg Sanders
	<gsanders87@gmail.com>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID: <ZZSfhQ3KD1uK8T45@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Tue, Jan 02, 2024 at 11:12:05AM +0000, Gloria Zhao wrote:
> Hi Peter,
> 
> > You make a good point that the commitment transaction also needs to be
> included
> > in my calculations. But you are incorrect about the size of them.
> 
> > With taproot and ephemeral anchors, a typical commitment transaction
> would have
> > a single-sig input (musig), two taproot outputs, and an ephemeral anchor
> > output.  Such a transaction is only 162vB, much less than 1000vB.
> 
> Note that these scenarios are much less interesting for commitment
> transactions with no HTLC outputs, so 162 isn't what I would use for the
> minimum.

<snip, replied to in another email>

> So, I apologize for not using a more accurate minimum, though I think this
> helps illustrate the 100x reduction of v3 a lot better.
> While I think the true minimum is higher, let's go ahead and use your
> number N=162vB.
> - Alice is happy to pay 162sat/vB * (162 + 152vB) = 50,868sat
> - In a v3 world, Mallory can make the cost to replace 80sat/vB * (1000vB) +
> 152 = 80,152sat
>     - Mallory succeeds, forcing Alice to pay 80,152 - 50,868 = *29,284sat*
> more
> - In a non-v3 world, Mallory can make the cost to replace 80sat/vB *
> (100,000vB) + 152 = 8,000,152sat
>     - Mallory succeeds, forcing Alice to pay 8,000,152 - 50,868 = *7,949,284sat
> *more (maxed out by the HTLC amount)
> 
> As framed above, what we've done here is quantify the severity of the
> pinning damage in the v3 and non-v3 world by calculating the additional
> fees Mallory can force Alice to pay using Rule 3. To summarize this
> discussion, at the lower end of possible commitment transaction sizes,
> pinning is possible but is restricted by 100x, as claimed.

Also, you're writeup is still missing a very important point: existing
Lightning anchor channels solved pinning by having a CHECKSIG. Only the parties
with the right to spend the anchor channel can do that, and all other outputs
are unspendable until the commitment transaction confirms.

So the question is not whether or not V3 transactions can improve pinning
compared to a hypothetical protocol with vulnerabilities. The question, for
Lightning, is how much better or worse V3 transactions would be than the status
quo. So far, they look like the difference is marginal at best, quite possibly
worse.

Now, with other protocols, maybe we could make an argument that V3 transactions
is worthwhile and for those protocols no other solution is possible. But you
have not attempted to make that argument in the documentation provided in your
pull-req(s).

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240102/b1eb5b6c/attachment-0001.sig>

------------------------------

Message: 4
Date: Wed, 3 Jan 2024 18:36:02 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID: <ZZUcckQkd7K9wIka@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Sat, Dec 30, 2023 at 01:54:04PM +0000, Michael Folkson via bitcoin-dev wrote:
> > > But "target fixation" [0] is a thing too: maybe "CTV" (and/or "APO") were just a bad approach from the start.
> It is hard to discuss APO in a vacuum when this is going on the background but I'm interested in you grouping APO with CTV in this statement. ... But APO does seem to be the optimal design and have broad consensus in the Lightning community for enabling eltoo/LN-Symmetry. Any other use cases APO enables would be an additional benefit.

I guess I'm really just reiterating/expanding on Russell's thoughts from
two years ago:

  https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-January/019813.html

CTV and APO both take the approach of delineating a small, precise piece
of functionality that is thought to be useful in known ways, and making
that available for use within Bitcoin. But doing incremental consensus
changes every time we discover new features that we'd like to add to
wallet/L2 software is kind of clumsy, and perhaps we should be looking
at more general approaches that allow more things at once.

Beyond that, APO also follows the design of satoshi's ANYONECANPAY,
which allows attaching other inputs. There's a decent argument to be
made that that's a bad design choice (and was perhaps a bad choice
for ANYONECANPAY as well as APO), and that committing to the number of
inputs would still be a valable thing to do (in that it minimises how
much third parties can manipulate your tx, and reduces the potential for
rbf pinning). A consequence of that is that once if you fix the number
of inputs to one and already know the input you're spending, you avoid
txid malleability. See https://github.com/bitcoin/bips/pull/1472 eg.

Cheers,
aj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 6
*******************************************
