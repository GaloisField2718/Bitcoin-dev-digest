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

   1. Re: Ordinal Inscription Size Limits (Erik Aronesty)
   2. Re: Swift Activation - CTV (Erik Aronesty)
   3. Re: Ordinal Inscription Size Limits (Brad Morrison)


----------------------------------------------------------------------

Message: 1
Date: Mon, 1 Jan 2024 11:08:29 -0500
From: Erik Aronesty <erik@q32.com>
To: Brad Morrison <bradmorrison@sonic.net>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID:
	<CAJowKg+sRPMqyY8pzepqc7w5ZeCdxz75_teBgsNNsta4FKeR1g@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

>
> .
>
> In the USA, where I am, large businesses like UBER, Lyft, and many major
> telecom, cable, & electric utilities process huge volumes of regular and
> irregular credit card payments on a monthly basis. Almost none oft hose
> transactions are completed in bitcoin.
>


Unfortunately block size is not the limiting factor

Main chain transactions have to be broadcast and stored on every node in
the network which, as you know, cannot scale to the level of Uber payments

Lighting and possibly ark are solutions to this problem

Both require covenant tech of some kind to scale properly (nonrecursive is
fine)

Covenant tech (any will do, arguing about which is bike shedding at this
point) allows people to share utxos and yet still maintain sovereignty over
their assets





>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240101/26ebcdc1/attachment-0001.html>

------------------------------

Message: 2
Date: Mon, 1 Jan 2024 12:11:24 -0500
From: Erik Aronesty <erik@q32.com>
To: Michael Folkson <michaelfolkson@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Anthony Towns
	<aj@erisian.com.au>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<CAJowKg+CQWiHxcJLPE7bHbfwGo3WGQSqBNAQU-aEyCJH8YGO3w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

1. Claiming that something that isn't activated (unusable) isn't used as a
non-argument

2. Talking about activation methods is orthogonal.  Bip8 is fine.

3. Covenants allow trustless utxos sharing and also are needed for
vaulting.  The numerous use cases are documented, built out and on signet
to my knowledge.  Check out utxos.org for a good list

3. No need to discuss wild extremes that are unrelated to ctvs well
documented utility.  Plus multi-sig allows governments to encumber (or
accidentally ruin) destination addresses just like covenants.

4. "Best tool for the job" is not the bar. "Safe for all" and "useful for
some" is the bar. Like any opcodes or tech Bitcoin has deployed in the
past.  Changing the bar is not up for discussion.


CTV has already been demonstrated "useful for some".  The question that
needs to be answered is whether there are any specific objections to safety.









On Mon, Jan 1, 2024, 11:37 AM Michael Folkson <michaelfolkson@protonmail.com>
wrote:

> Hi Erik
>
> > So what exactly are the risks of CTV over multi-sig?
>
> It is a strange comparison. Multisig is active onchain and is being used
> today for all sorts of things including Lightning and setups that address
> risk of single key loss or malicious signing. When discussing risks of CTV
> there are all sorts of risks that don't apply to multisig. These include
> that it is never used for any of its speculated use cases (multisig is
> being used today), other proposals end up being used instead of it (I'm not
> sure there were or are competing proposals so that multisig stops being
> used, MuSig2 maybe?), chain split risks with activation if there isn't
> consensus to activate it etc. Plus usage of complex (non covenant) scripts
> that fully utilize Taproot trees is still low today. Going straight to
> covenants (imposing restrictions on *where*? funds can be sent) and not
> bothering with imposing all the restrictions you'd like on *how*? funds
> can be spent in the first place seems to me to be putting the cart before
> the horse. Covenants don't ultimately solve the key management issue, they
> just move it from the pre spending phase to the post spending phase. So the
> benefits (although non-zero) aren't as obvious as some of the covenant
> advocates are suggesting. And although CTV is a limited covenant (some
> argue too limited) covenants taken to wild extremes could create all sorts
> of second order effects where funds can't be spent because of complex
> combinations of covenants. Even the strongest CTV proponent seems to
> suggest that the introduction of covenants wouldn't end with CTV.
>
> The way to reduce implementation risk for a use case of a particular
> proposal is to build out that use case and see if CTV is the best tool for
> the job. Repeatedly trying to activate CTV when there isn't consensus for
> it to be activated does not reduce that implementation risk in any way,
> shape or form.
>
> Thanks
> Michael
>
>
> --
> Michael Folkson
> Email: michaelfolkson at protonmail.com
> GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
>
> Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
>
> On Saturday, 30 December 2023 at 08:59, Erik Aronesty via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> So what exactly are the risks of CTV over multi-sig?
>
>
>>
>>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240101/87ac6b11/attachment-0001.html>

------------------------------

Message: 3
Date: Mon, 01 Jan 2024 05:33:02 -0800
From: Brad Morrison <bradmorrison@sonic.net>
To: Erik Aronesty <erik@q32.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID: <bda67a7ba6432b080d9c45e15cb80372@sonic.net>
Content-Type: text/plain; charset="us-ascii"

Erik, 

Fees AKA costs are the best spam control system and I thank you for
highlighting that. 

However, I think that bitcoin has yet to receive sufficient payments
usage to challenge credit card payments system when it comes to a race
to the bottom in terms of processing transactional fees. 

In the USA, where I am, large businesses like UBER, Lyft, and many major
telecom, cable, & electric utilities process huge volumes of regular and
irregular credit card payments on a monthly basis. Almost none oft hose
transactions are completed in bitcoin. 

A focus on lowering fees by increasing the block size by 10x is the
simplest method to start accepting more payments in bitcoin from larger
businesses. 

Brad

On 2023-12-30 01:58, Erik Aronesty via bitcoin-dev wrote:

> Bitcoin already has a spam prevention system called "fees".   I don't believe it's insufficient.  The only issue is the stochastic nature of its effectiveness 
> 
> Which can be resolved with things like payment pools, tree payments (https://utxos.org/uses/scaling/), etc. 
> 
> On Fri, Dec 29, 2023, 9:33 AM Greg Tonoski via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote: 
> 
>>> Unfortunately, as near as I can tell there is no sensible way to
>>> prevent people from storing arbitrary data in witnesses ...
>> 
>> To prevent "from storing arbitrary data in witnesses" is the extreme
>> case of the size limit discussed in this thread. Let's consider it along
>> with other (less radical) options in order not to lose perspective, perhaps.
>> 
>>> ...without incentivizing even worse behavior and/or breaking
>>> legitimate use cases.
>> 
>> I can't find evidence that would support the hypothesis. There had not
>> been "even worse behavior and/or breaking legitimate use cases" observed
>> before witnesses inception. The measure would probably restore
>> incentives structure from the past.
>> 
>> As a matter of fact, it is the current incentive structure that poses
>> the problem - incentivizes worse behavior ("this sort of data is toxic
>> to the network") and breaks legitimate use cases like a simple transfer
>> of BTC.
>> 
>>> If we ban "useless data" then it would be easy for would-be data
>>> storers to instead embed their data inside "useful" data such as dummy
>>> signatures or public keys.
>> 
>> There is significant difference when storing data as dummy signatures
>> (or OP_RETURN) which is much more expensive than (discounted) witness.
>> Witness would not have been chosen as the storage of arbitrary data if
>> it cost as much as alternatives, e.g. OP_RETURN.
>> 
>> Also, banning "useless data" seems to be not the only option suggested
>> by the author who asked about imposing "a size limit similar to OP_RETURN".
>> 
>>> But from a technical point of view, I don't see any principled way to
>>> stop this.
>> 
>> Let's discuss ways that bring improvement rather than inexistence of a
>> perfect technical solution that would have stopped "toxic data"/"crap on
>> the chain". There are at least a few:
>> - https://github.com/bitcoin/bitcoin/pull/28408
>> - https://github.com/bitcoin/bitcoin/issues/29146
>> - deprecate OP_IF opcode.
>> 
>> I feel like the elephant in the room has been brought up. Do you want to
>> maintain Bitcoin without spam or a can't-stop-crap alternative, everybody?
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240101/74c4e4f1/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 4
*******************************************
