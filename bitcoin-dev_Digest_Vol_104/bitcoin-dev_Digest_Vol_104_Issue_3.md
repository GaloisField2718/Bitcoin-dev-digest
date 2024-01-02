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

   1. Re: Lamport scheme (not signature) to economize on L1
      (David A. Harding)
   2. Re: Swift Activation - CTV (Michael Folkson)
   3. Re: V3 Transactions are still vulnerable to significant tx
      pinning griefing attacks (Gloria Zhao)


----------------------------------------------------------------------

Message: 1
Date: Mon, 01 Jan 2024 08:57:13 -1000
From: "David A. Harding" <dave@dtrt.org>
To: yurisvb@pm.me
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID: <7d364adaed1457855a40522f73f3adfe@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2024-01-01 00:17, yurisvb@pm.me wrote:
> I'm afraid I didn't understand your objection. [...]
> I suspect my proposed scheme can be
> implemented with available, existing Bitcoin infrastructure.

Is a soft fork or a hard fork required?  If so, the proposal will need a 
lot of peer review and user acceptance.

What are the benefits of your proposal?  As I understand it, the benefit 
is smaller transactions.  How much smaller will they be in terms of 
vbytes?  For example, a transaction today with one input performing a 
taproot keypath spend and one taproot-paying output is 111 vbytes[1].  
What will be the total onchain size of an equivalent one-input, 
one-output transaction using your scheme?

My comment (not objection) is that modest decreases in onchain data size 
may not provide a significant enough benefit to attract reviewers and 
interested users, especially if a proposal is complicated by a 
dependencies on many things that have not previously been included in 
Bitcoin (such as new hash functions).

If I'm deeply misunderstanding your proposal and my questions don't make 
sense, I'd very much appreciate a clarification about what your proposal 
does.

Thanks,

-Dave

[1] https://bitcoinops.org/en/tools/calc-size/


------------------------------

Message: 2
Date: Mon, 01 Jan 2024 16:37:35 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Erik Aronesty <erik@q32.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Anthony Towns
	<aj@erisian.com.au>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<JjjvS5JDzMsm_gr9M1li4rhxJbQroFXfC8CvIYkHsncrYTB9K723Ds68KnPPm7rKyDgvVdMcUoeg8QQgRKlPsaOSvp5vc6OjB_-TiQZ5iWE=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Erik

> So what exactly are the risks of CTV over multi-sig?

It is a strange comparison. Multisig is active onchain and is being used today for all sorts of things including Lightning and setups that address risk of single key loss or malicious signing. When discussing risks of CTV there are all sorts of risks that don't apply to multisig. These include that it is never used for any of its speculated use cases (multisig is being used today), other proposals end up being used instead of it (I'm not sure there were or are competing proposals so that multisig stops being used, MuSig2 maybe?), chain split risks with activation if there isn't consensus to activate it etc. Plus usage of complex (non covenant) scripts that fully utilize Taproot trees is still low today. Going straight to covenants (imposing restrictions on where? funds can be sent) and not bothering with imposing all the restrictions you'd like on how? funds can be spent in the first place seems to me to be putting the cart before the horse. Covenants don't ultimately solve the key m
 anagement issue, they just move it from the pre spending phase to the post spending phase. So the benefits (although non-zero) aren't as obvious as some of the covenant advocates are suggesting. And although CTV is a limited covenant (some argue too limited) covenants taken to wild extremes could create all sorts of second order effects where funds can't be spent because of complex combinations of covenants. Even the strongest CTV proponent seems to suggest that the introduction of covenants wouldn't end with CTV.

The way to reduce implementation risk for a use case of a particular proposal is to build out that use case and see if CTV is the best tool for the job. Repeatedly trying to activate CTV when there isn't consensus for it to be activated does not reduce that implementation risk in any way, shape or form.

Thanks
Michael

--
Michael Folkson
Email: michaelfolkson at [protonmail.com](http://protonmail.com/)
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F

Learn about Bitcoin: https://www.youtube.com/@portofbitcoin

On Saturday, 30 December 2023 at 08:59, Erik Aronesty via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> So what exactly are the risks of CTV over multi-sig?
>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240101/f99b7312/attachment.html>

------------------------------

Message: 3
Date: Tue, 2 Jan 2024 11:12:05 +0000
From: Gloria Zhao <gloriajzhao@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Greg Sanders
	<gsanders87@gmail.com>
Subject: Re: [bitcoin-dev] V3 Transactions are still vulnerable to
	significant tx pinning griefing attacks
Message-ID:
	<CAFXO6=JuMwFjy-Q9h3U8dTr_4TvDjusFFX6orVhXvCG_G8WbOA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Peter,

> You make a good point that the commitment transaction also needs to be
included
> in my calculations. But you are incorrect about the size of them.

> With taproot and ephemeral anchors, a typical commitment transaction
would have
> a single-sig input (musig), two taproot outputs, and an ephemeral anchor
> output.  Such a transaction is only 162vB, much less than 1000vB.

Note that these scenarios are much less interesting for commitment
transactions with no HTLC outputs, so 162 isn't what I would use for the
minimum.

Looking at expected weights in bolt 3 (
https://github.com/lightning/bolts/blob/master/03-transactions.md#expected-weight-of-the-commitment-transaction)
with 1 HTLC and anchors, we get (900 + 172 * num-htlc-outputs + 224
weight)/4 = 324vB.

So, I apologize for not using a more accurate minimum, though I think this
helps illustrate the 100x reduction of v3 a lot better.
While I think the true minimum is higher, let's go ahead and use your
number N=162vB.
- Alice is happy to pay 162sat/vB * (162 + 152vB) = 50,868sat
- In a v3 world, Mallory can make the cost to replace 80sat/vB * (1000vB) +
152 = 80,152sat
    - Mallory succeeds, forcing Alice to pay 80,152 - 50,868 = *29,284sat*
more
- In a non-v3 world, Mallory can make the cost to replace 80sat/vB *
(100,000vB) + 152 = 8,000,152sat
    - Mallory succeeds, forcing Alice to pay 8,000,152 - 50,868 = *7,949,284sat
*more (maxed out by the HTLC amount)

As framed above, what we've done here is quantify the severity of the
pinning damage in the v3 and non-v3 world by calculating the additional
fees Mallory can force Alice to pay using Rule 3. To summarize this
discussion, at the lower end of possible commitment transaction sizes,
pinning is possible but is restricted by 100x, as claimed.

Best,
Gloria

On Wed, Dec 20, 2023 at 9:11?PM Peter Todd <pete@petertodd.org> wrote:

> On Wed, Dec 20, 2023 at 03:16:25PM -0500, Greg Sanders wrote:
> > Hi Peter,
> >
> > Thanks for taking the time to understand the proposal and give thoughtful
> > feedback.
> >
> > With this kind of "static" approach I think there are fundamental
> > limitations because
> > the user has to commit "up front" how large the CPFP later will have to
> be.
> > 1kvB
> > is an arbitrary value that is two orders of magnitude less than the
> > possible package
> > size, and allows fairly flexible amounts of inputs(~14 taproot inputs
> > IIRC?) to effectuate a CPFP.
>
> Why would you need so many inputs to do a CPFP if they all have to be
> confirmed? The purpose of doing a CPFP is to pay fees to get another
> transaction mined. Unless you're in some degenerate, unusual, situation
> where
> you've somehow ended up with just some dust left in your wallet, dust that
> is
> barely worth its own fees to spend, one or maybe two UTXOs are going to be
> sufficient for a fee payment.
>
> I had incorrectly thought that V3 transctions allowed for a single up-to
> 1000vB
> transaction to pay for multiple parents at once. But if you can't do that,
> due
> to the restriction on unconfirmed inputs, I can't see any reason to have
> such a
> large limit.
>
> > I'd like something much more flexible, but we're barely at whiteboard
> stage
> > for alternatives and
> > they probably require more fundamental work. So within these limits, we
> > have to pick some number,
> > and it'll have tradeoffs.
> >
> > When I think of "pinning potential", I consider not only the parent size,
> > and not
> > only the maximum child size, but also the "honest" child size. If the
> honest
> > user does relatively poor utxo management, or the commitment transaction
> > is of very high value(e.g., lots of high value HTLCs), the pin is
> > essentially zero.
> > If the honest user ever only have one utxo, then the "max pin" is
> effective
> > indeed.
>
> Which is the situation you would expect in the vast majority of cases.
>
> > > Alice would have had to pay a 2.6x higher fee than
> > expected.
> >
> > I think that's an acceptable worst case starting point, versus the status
> > quo which is ~500-1000x+.
>
> No, the status quo is signed anchors, like Lightning already has with
> anchor
> channels. Those anchors could still be zero-valued. But as long as there
> is a
> signature associated with them, pinning isn't a problem as only the
> intended
> party can spend them.
>
> Note BTW that existing Lightning anchor channels inefficiently use two
> anchor
> outputs when just one is sufficient:
>
>
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-December/004246.html
>     [Lightning-dev] The remote anchor of anchor channels is redundant
>     Peter Todd, Dec 13th, 2023
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240102/302c697d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 3
*******************************************
