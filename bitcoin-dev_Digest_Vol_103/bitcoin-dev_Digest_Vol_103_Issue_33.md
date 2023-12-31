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

   1. Re: Swift Activation - CTV (Michael Folkson)


----------------------------------------------------------------------

Message: 1
Date: Sat, 30 Dec 2023 13:54:04 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Anthony Towns <aj@erisian.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<7NGPxdCD3faagkDFsyhVnjyXGu_BF3PfRW86QjZxP-nsDY-EvNGlyxXSEA7nf0SYzm5Ql45sA7gDGjKNpqWQoALLUz-MROUZTGjEFtzTdm8=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hey AJ

Thanks for this, pretty much agree with all of it. It seems like a week doesn't go by now without a new individual popping out the woodwork proposing an upcoming activation of CTV with no new PoCs and no new insights. I'm not sure what it is about CTV (versus say other proposals) that it keeps attracting these people that refuse to work on PoCs or anything that drives the research area forward and yet want to try to attempt activation where the success scenario would be a chain split.

> > But "target fixation" [0] is a thing too: maybe "CTV" (and/or "APO") were just a bad approach from the start.

It is hard to discuss APO in a vacuum when this is going on the background but I'm interested in you grouping APO with CTV in this statement. At the time of writing there clearly isn't consensus or advanced PoCs on any of the use cases CTV claims to enable. (One rare exception on the use case front is James O'Beirne's OP_VAULT [0] that requires additional opcodes to OP_CTV). But APO does seem to be the optimal design and have broad consensus in the Lightning community for enabling eltoo/LN-Symmetry. Any other use cases APO enables would be an additional benefit.

I don't think one can seriously think about an *upcoming* activation for APO as there is still more work to do to convince the community that it would be worth the risks of embarking on another activation process. But assuming another year of concerted work on APO and the CTV woodwork of chaos (hopefully) being exhausted do you think an APO activation would be viable in say 2025/2026? Is your hesitancy on APO based on any particular technical concerns or just fatigue from the CTV chaos?

Thanks
Michael

[0]: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-January/021318.html

--
Michael Folkson
Email: michaelfolkson at protonmail.com
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F

Learn about Bitcoin: https://www.youtube.com/@portofbitcoin


On Saturday, 30 December 2023 at 08:05, Anthony Towns via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Huh, this list is still active?
> 
> On Fri, Dec 22, 2023 at 10:34:52PM +0000, alicexbt via bitcoin-dev wrote:
> 
> > I think CTV is not ready for activation yet. Although I want it to be activated and use payment pools, we still have some work to do and AJ is correct that we need to build more apps that use CTV on signet.
> 
> 
> I've said it before, and I'll say it again, but if you want to change
> bitcoin consensus rules, IMO the sensible process is:
> 
> * work out what you think the change should be
> * demonstrate the benefits so everyone can clearly see what they are,
> and that they're worth spending time on
> * review the risks, so that whatever risks there may be are well
> understood, and minimise them
> * iterate on all three of those steps to increase the benefits and
> reduce the risks
> * once "everyone" agrees the benefits are huge and the risks are low,
> work on activating it
> 
> If you're having trouble demonstrating that the benefits really are
> worth spending time on, you probably need to go back to the first step
> and reconsider the proposal. The "covtools" and "op_cat" approaches are
> a modest way of doing that: adding additional opcodes that mesh well
> with CTV, increasing the benefits from making a change.
> 
> But "target fixation" [0] is a thing too: maybe "CTV" (and/or "APO")
> were just a bad approach from the start. Presumably "activate CTV"
> is really intended as a step towards your actual goal, whether that be
> "make it harder for totalitarians to censor payments", "replace credit
> cards", "make lots of money", "take control over bitcoind evelopment",
> or something else. Maybe there's a better step towards some/all of
> whatever those goals may be than "activate CTV". Things like "txhash"
> take that approach and go back to the first step.
> 
> To me, it seems like CTV has taken the odd approach of simultaneously
> maximising (at least perceived) risk, while minimising the potential
> benefits. As far as maximising risk goes, it's taken Greg Maxwell's
> "amusingly bad idea" post from bitcointalk in 2013 [1] and made the bad
> consequence described there (namely, "coin covenants", which left Greg
> "screaming in horror") as the centrepiece of the functionality being
> added, per its motivation section. It then minimises the potential
> benefits that accompany that risk by restricting the functionality being
> provided as far as you can without neutering it entirely. If you wanted
> a recipe for how to propose a change to bitcoin and ensure that it's
> doomed to fail while still gathering a lot of attention, I'm honestly
> not sure how you could come up with a better approach?
> 
> [0] https://en.wikipedia.org/wiki/Target_fixation
> [1] https://bitcointalk.org/index.php?topic=278122.0
> 
> > - Apart from a few PoCs that do not achieve anything big on mainnet, nobody has tried to build PoC for a use case that solves real problems
> 
> 
> One aspect of "minimising the benefits" is that when you make something
> too child safe, it can become hard to actually use the tool at all. Just
> having ideas is easy -- you can just handwave over the complex parts
> when you're whiteboarding or blogging -- the real way to test if a tool
> is fit for purpose is to use it to build something worthwhile. Maybe a
> great chef can create a great meal with an easy-bake oven, but there's
> a reason it's not their tool of choice.
> 
> Cheers,
> aj
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

End of bitcoin-dev Digest, Vol 103, Issue 33
********************************************
