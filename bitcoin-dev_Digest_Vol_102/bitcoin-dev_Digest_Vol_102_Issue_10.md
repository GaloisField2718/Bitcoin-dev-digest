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


----------------------------------------------------------------------

Message: 1
Date: Sun, 5 Nov 2023 18:25:47 +0100
From: JK <jk_14@op.pl>
To: Erik Aronesty <erik@q32.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] ossification and misaligned incentive
	concerns
Message-ID: <8443b179-2d24-4e77-9ff6-c5f51af545aa@op.pl>
Content-Type: text/plain; charset=UTF-8; format=flowed


Ok, instead of (maybe too general) term "network security," - I may 
change it into a more precise term then:
"security of Store-of-Value"

Of course, your private keys are private and your note is fully 
validating...

...but: miners provide security of Store-of-Value property. Miners 
simply ensure keeping intact the purchasing power of Bitcoins stored on 
your private keys. And it's really difficult to dispute this simple fact.

"Contact with Europeans in the 19th century first provided the Yapese at 
Palau with iron tools, that made the cutting and shaping of the stones 
*** much easier ***. Not much later, the Yapese made deals with 
Europeans to use their ships to transport the stones back to Yap. These 
arrangements enabled the manufacture of much larger and heavier rai 
stones, up to 4 meters in diameter, as well of a larger number of them. 
However, these "modern" stones were *** less valuable *** than more 
ancient ones"
https://en.wikipedia.org/wiki/Rai_stones#Manufacturing_after_European_contact

much easier "mining" of rai stones/Bitcoins => less valuable rai 
stones/Bitcoins

And as we can see - it's not the matter of belief or disbelief.
I really hope this simple example is ultimately enough to put an end to 
the narrative that miners do not provide security of Bitcoin - if they 
do provide the security of one of most important Bitcoin's property.



W dniu 05.11.2023 o?15:59, Erik Aronesty pisze:
> I don't believe the narrative that miners provide network security
> 
> they provide double spend insurance
> 
> and that's it
> 
> so that limits the size of the transaction and the number of 
> confirmations that are required before that transaction is cleared
> 
> But it doesn't provide security for the rest of the network.? My private 
> keys are private and my note is fully validating? ..? and there's 
> nothing miners can do about that
> 
> let's ditch that narrative please
> 
> 
> 
> On Sun, Nov 5, 2023, 9:40 AM JK <jk_14@op.pl <mailto:jk_14@op.pl>> wrote:
> 
> 
>     I'm worried even more about something else, but still fits into the
>     same
>     topic category.
> 
> 
>     A tax in the form of a direct tax is less acceptable to people than a
>     hidden tax. This is human nature, as the saying goes, "What the eye
>     doesn't see, the heart doesn't grieve over." A high direct tax
>     (e.g., on
>     a one-time transaction) is much more irritating than a tax of the same
>     amount but hidden (especially when it affects all cash holders equally,
>     as in the case of inflation).
> 
>     There is no reason to believe that in any alternative financial system,
>     it will be different ("This time is different." No, it is not.)
> 
>     The analogy is clear: a transaction tax is on-chain fee, an inflation
>     tax is the block reward. And just in case: miners are only able to
>     collect payment for providing network security in an amount equal to
>     the
>     sum collected in both of these taxes, and no single satoshi more (the
>     principle that "There's no such thing as a free lunch" applies).
> 
>     Now, a little thought experiment:
>     Imagine a system that tries to maintain a constant level of difficulty
>     and reacts flexibly to changes in difficulty, by modulating the block
>     reward level accordingly (using negative feedback).
> 
>     It is known that the system will oscillate around a certain level of
>     the
>     block reward value (around a certain level of inflation) that provides
>     the desired level of network security.
> 
>     Furthermore, Earth is a closed system with finite resources, making it
>     hard to imagine a situation where Bitcoin is responsible for e.g. 95%
>     of global energy consumption (while complaints already arise at 0.1%).
> 
>     In other words, the level of network security is de facto limited from
>     the top, whether we like it or not.
> 
>     And for a naturally limited and still acceptable level of network
>     security (vide: "Change the code, not the climate") - there is a
>     corresponding level of inflation.
> 
> 
>     To sum this up, the most important conclusion to remember is:
> 
>     For a natural level of network security, there is a natural level of
>     inflation.
> 
> 
> 
>     I'll add a very relevant comment I know from the internet:
> 
>     "It makes sense. Something akin to what the central banks do by setting
>     interest rates, but algorithmic, leading to a 'natural' (rather than
>     manipulated) level of inflation. But different, because it's directly
>     tied to security. I haven't thought whether it would be an issue if it
>     works in one direction only (halvings, but no doublings), but it might.
>     When I was learning about Bitcoin, I heard "It costs you nothing to
>     store your bitcoin (as opposed to, say, gold). You get security for
>     free." and thought it sounded wonderful, but too good to be true. There
>     is no free lunch and all that... I understand a lack of inflation is
>     aligned with Austrian economics, but the Austrians didn't know a
>     monetary system whose security was tied to inflation. So it's a new
>     concept to wrap one's head around."
>     https://stacker.news/items/291420 <https://stacker.news/items/291420>
> 
> 
>     There is growing awareness of the lack of a free market between active
>     and passive participants in Bitcoin and growing awareness of the
>     inevitability of the problem that will arise in the future as a result.
>     And there is slowly growing acceptance of well-thought-out proposals to
>     fix this situation.
>     The free market is more important than finite supply.
> 
> 
>     Regards
>     Jaroslaw
> 
> 
>     W dniu 03.11.2023 o?19:24, Erik Aronesty via bitcoin-dev pisze:
>      > currently, there are providers of anonymity?services, scaling
>     services,
>      > custody, and other services layered on top of bitcoin using
>     trust-based
>      > and federated models.
>      >
>      > as bitcoin becomes more popular, these service providers have
>      > increasingly had a louder "voice" in development and maintenance
>     of the
>      > protocol
>      >
>      > holders generally want these features
>      >
>      > but service providers have an incentive to maintain a "moat" around
>      > their services
>      >
>      > in summary, making privacy, scaling and vaulting "hard" for regular
>      > users, keeping it off-chain and federated...? is now incentivised
>     among
>      > a vocal, but highly technical, minority
>      >
>      > is anyone else worried about this?
>      >
>      > _______________________________________________
>      > bitcoin-dev mailing list
>      > bitcoin-dev@lists.linuxfoundation.org
>     <mailto:bitcoin-dev@lists.linuxfoundation.org>
>      > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>     <https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev>
> 


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 10
********************************************
