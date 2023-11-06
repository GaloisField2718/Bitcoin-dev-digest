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

   1. Re: ossification and misaligned incentive concerns (JK)
   2. Re: ossification and misaligned incentive concerns (Erik Aronesty)
   3. Re: ossification and misaligned incentive concerns (Ryan Grant)
   4. Re: ossification and misaligned incentive concerns (alicexbt)


----------------------------------------------------------------------

Message: 1
Date: Sun, 5 Nov 2023 15:39:53 +0100
From: JK <jk_14@op.pl>
To: Erik Aronesty <erik@q32.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] ossification and misaligned incentive
	concerns
Message-ID: <21dd55af-ca9d-48b0-b2aa-4a1399f15611@op.pl>
Content-Type: text/plain; charset=UTF-8; format=flowed


I'm worried even more about something else, but still fits into the same 
topic category.


A tax in the form of a direct tax is less acceptable to people than a 
hidden tax. This is human nature, as the saying goes, "What the eye 
doesn't see, the heart doesn't grieve over." A high direct tax (e.g., on 
a one-time transaction) is much more irritating than a tax of the same 
amount but hidden (especially when it affects all cash holders equally, 
as in the case of inflation).

There is no reason to believe that in any alternative financial system, 
it will be different ("This time is different." No, it is not.)

The analogy is clear: a transaction tax is on-chain fee, an inflation 
tax is the block reward. And just in case: miners are only able to 
collect payment for providing network security in an amount equal to the 
sum collected in both of these taxes, and no single satoshi more (the 
principle that "There's no such thing as a free lunch" applies).

Now, a little thought experiment:
Imagine a system that tries to maintain a constant level of difficulty 
and reacts flexibly to changes in difficulty, by modulating the block 
reward level accordingly (using negative feedback).

It is known that the system will oscillate around a certain level of the 
block reward value (around a certain level of inflation) that provides 
the desired level of network security.

Furthermore, Earth is a closed system with finite resources, making it 
hard to imagine a situation where Bitcoin is responsible for e.g. 95%
of global energy consumption (while complaints already arise at 0.1%).

In other words, the level of network security is de facto limited from 
the top, whether we like it or not.

And for a naturally limited and still acceptable level of network 
security (vide: "Change the code, not the climate") - there is a 
corresponding level of inflation.


To sum this up, the most important conclusion to remember is:

For a natural level of network security, there is a natural level of 
inflation.



I'll add a very relevant comment I know from the internet:

"It makes sense. Something akin to what the central banks do by setting 
interest rates, but algorithmic, leading to a 'natural' (rather than 
manipulated) level of inflation. But different, because it's directly 
tied to security. I haven't thought whether it would be an issue if it 
works in one direction only (halvings, but no doublings), but it might. 
When I was learning about Bitcoin, I heard "It costs you nothing to 
store your bitcoin (as opposed to, say, gold). You get security for 
free." and thought it sounded wonderful, but too good to be true. There 
is no free lunch and all that... I understand a lack of inflation is 
aligned with Austrian economics, but the Austrians didn't know a 
monetary system whose security was tied to inflation. So it's a new 
concept to wrap one's head around."
https://stacker.news/items/291420


There is growing awareness of the lack of a free market between active 
and passive participants in Bitcoin and growing awareness of the 
inevitability of the problem that will arise in the future as a result. 
And there is slowly growing acceptance of well-thought-out proposals to 
fix this situation.
The free market is more important than finite supply.


Regards
Jaroslaw


W dniu 03.11.2023 o?19:24, Erik Aronesty via bitcoin-dev pisze:
> currently, there are providers of anonymity?services, scaling services, 
> custody, and other services layered on top of bitcoin using trust-based 
> and federated models.
> 
> as bitcoin becomes more popular, these service providers have 
> increasingly had a louder "voice" in development and maintenance of the 
> protocol
> 
> holders generally want these features
> 
> but service providers have an incentive to maintain a "moat" around 
> their services
> 
> in summary, making privacy, scaling and vaulting "hard" for regular 
> users, keeping it off-chain and federated...? is now incentivised among 
> a vocal, but highly technical, minority
> 
> is anyone else worried about this?
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Sun, 5 Nov 2023 09:59:44 -0500
From: Erik Aronesty <erik@q32.com>
To: JK <jk_14@op.pl>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] ossification and misaligned incentive
	concerns
Message-ID:
	<CAJowKgJhXEBJgOhoOtUrsO_KpFwJ_fRYnZopDEuHCgSx5CzOJg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

I don't believe the narrative that miners provide network security

they provide double spend insurance

and that's it

so that limits the size of the transaction and the number of confirmations
that are required before that transaction is cleared

But it doesn't provide security for the rest of the network.  My private
keys are private and my note is fully validating  ..  and there's nothing
miners can do about that

let's ditch that narrative please



On Sun, Nov 5, 2023, 9:40 AM JK <jk_14@op.pl> wrote:

>
> I'm worried even more about something else, but still fits into the same
> topic category.
>
>
> A tax in the form of a direct tax is less acceptable to people than a
> hidden tax. This is human nature, as the saying goes, "What the eye
> doesn't see, the heart doesn't grieve over." A high direct tax (e.g., on
> a one-time transaction) is much more irritating than a tax of the same
> amount but hidden (especially when it affects all cash holders equally,
> as in the case of inflation).
>
> There is no reason to believe that in any alternative financial system,
> it will be different ("This time is different." No, it is not.)
>
> The analogy is clear: a transaction tax is on-chain fee, an inflation
> tax is the block reward. And just in case: miners are only able to
> collect payment for providing network security in an amount equal to the
> sum collected in both of these taxes, and no single satoshi more (the
> principle that "There's no such thing as a free lunch" applies).
>
> Now, a little thought experiment:
> Imagine a system that tries to maintain a constant level of difficulty
> and reacts flexibly to changes in difficulty, by modulating the block
> reward level accordingly (using negative feedback).
>
> It is known that the system will oscillate around a certain level of the
> block reward value (around a certain level of inflation) that provides
> the desired level of network security.
>
> Furthermore, Earth is a closed system with finite resources, making it
> hard to imagine a situation where Bitcoin is responsible for e.g. 95%
> of global energy consumption (while complaints already arise at 0.1%).
>
> In other words, the level of network security is de facto limited from
> the top, whether we like it or not.
>
> And for a naturally limited and still acceptable level of network
> security (vide: "Change the code, not the climate") - there is a
> corresponding level of inflation.
>
>
> To sum this up, the most important conclusion to remember is:
>
> For a natural level of network security, there is a natural level of
> inflation.
>
>
>
> I'll add a very relevant comment I know from the internet:
>
> "It makes sense. Something akin to what the central banks do by setting
> interest rates, but algorithmic, leading to a 'natural' (rather than
> manipulated) level of inflation. But different, because it's directly
> tied to security. I haven't thought whether it would be an issue if it
> works in one direction only (halvings, but no doublings), but it might.
> When I was learning about Bitcoin, I heard "It costs you nothing to
> store your bitcoin (as opposed to, say, gold). You get security for
> free." and thought it sounded wonderful, but too good to be true. There
> is no free lunch and all that... I understand a lack of inflation is
> aligned with Austrian economics, but the Austrians didn't know a
> monetary system whose security was tied to inflation. So it's a new
> concept to wrap one's head around."
> https://stacker.news/items/291420
>
>
> There is growing awareness of the lack of a free market between active
> and passive participants in Bitcoin and growing awareness of the
> inevitability of the problem that will arise in the future as a result.
> And there is slowly growing acceptance of well-thought-out proposals to
> fix this situation.
> The free market is more important than finite supply.
>
>
> Regards
> Jaroslaw
>
>
> W dniu 03.11.2023 o 19:24, Erik Aronesty via bitcoin-dev pisze:
> > currently, there are providers of anonymity services, scaling services,
> > custody, and other services layered on top of bitcoin using trust-based
> > and federated models.
> >
> > as bitcoin becomes more popular, these service providers have
> > increasingly had a louder "voice" in development and maintenance of the
> > protocol
> >
> > holders generally want these features
> >
> > but service providers have an incentive to maintain a "moat" around
> > their services
> >
> > in summary, making privacy, scaling and vaulting "hard" for regular
> > users, keeping it off-chain and federated...  is now incentivised among
> > a vocal, but highly technical, minority
> >
> > is anyone else worried about this?
> >
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231105/90aaa832/attachment-0001.html>

------------------------------

Message: 3
Date: Sun, 5 Nov 2023 21:00:07 +0000
From: Ryan Grant <bitcoin-dev@rgrant.org>
To: Erik Aronesty <erik@q32.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] ossification and misaligned incentive
	concerns
Message-ID:
	<CAMnpzfoFXo=ruGX7m+PEi1-PVkZWA5u+_ggHMHJzPpFVUH-ywg@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Fri, Nov 3, 2023 at 8:59?PM Erik Aronesty via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> is anyone else worried about this?

Yes. +1


------------------------------

Message: 4
Date: Sun, 05 Nov 2023 18:43:18 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Erik Aronesty <erik@q32.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] ossification and misaligned incentive
	concerns
Message-ID:
	<GX-kBpIk-vgpoFHURyyNZTdxcfvNhMx9cSnKgBB6SRz6lggoivBTqt81IwZSAjFSPv-nVKE0_ZX6pzEGFS7bZRoJI6TXqmCxwU6HI28AnfE=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Erik,

> currently, there are providers of anonymity services, scaling services, custody, and other services layered on top of bitcoin using trust-based and federated models.
> 
> as bitcoin becomes more popular, these service providers have increasingly had a louder "voice" in development and maintenance of the protocol

> is anyone else worried about this?

Yes. I share your concerns about the growing influence of centralized service providers on Bitcoin's development. Although there is nothing much we can do about it especially 
when trusted, centralized, custodial, federated etc. projects keep getting funded. Only solution is to build better things and be positive.

Example: Everyone is aware of the risks involved in a project that takes custody of funds, provide privacy without KYC. There are several examples from past in which similar 
projects with some volume ended up getting shutdown by governments. With [covenants and statechains][0], it is possible to use bitcoin (p2p ecash) with privacy and involves no custody.

There are other [benefits][1] of payment pools (w/ covenants) in terms of privacy. Hopefully we agree to do soft fork in next year or so.

[0]: https://github.com/AdamISZ/pathcoin-poc
[1]: https://gnusha.org/bitcoin-wizards/2019-05-21.log

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Friday, November 3rd, 2023 at 11:54 PM, Erik Aronesty via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> currently, there are providers of anonymity services, scaling services, custody, and other services layered on top of bitcoin using trust-based and federated models.
> 
> as bitcoin becomes more popular, these service providers have increasingly had a louder "voice" in development and maintenance of the protocol
> 
> holders generally want these features
> 
> but service providers have an incentive to maintain a "moat" around their services
> 
> in summary, making privacy, scaling and vaulting "hard" for regular users, keeping it off-chain and federated... is now incentivised among a vocal, but highly technical, minority
> 
> is anyone else worried about this?


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 9
*******************************************
