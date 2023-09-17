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

   1. Re: [Lightning-dev] Scaling Lightning With Simple	Covenants
      (jlspc)
   2. Re: Scaling Lightning With Simple Covenants (jlspc)
   3. Re: Scaling Lightning With Simple Covenants (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Sun, 17 Sep 2023 00:52:13 +0000
From: jlspc <jlspc@protonmail.com>
To: Anthony Towns <aj@erisian.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Scaling Lightning With
	Simple	Covenants
Message-ID:
	<RMoe8oOf6WIwX0yhB-A6-d8Zy5gf56thrD-gkIP5fdSzuR0EjpQo2fMY6FFYz-roCgsY2j0MgQnaF17U0RsUSTkqIRMuhOMjH0LqGlME4wg=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


Hi aj,

I completely agree with your observation that there's an important trust/safety vs. capital-efficiency tradeoff, and I almost completely agree with your analysis.

> (There are probably ways around this with additional complexity: eg,
> you could peer with a dedicated node, and have the timeout path be
> "you+them+timeout", so that while you could steal from casual users who
> don't rollover, you can't steal from your dedicated peer, so that $4.5B
> could be rolled into a channel with them, and used for routing)

Yes, that would work, but I think it's better to have dedicated user B pair with another dedicated user C such that each leaf of the timeout-tree funds a hierarchical channel [1] of the
form (A_i, (B, C)), where A_i is a casual user.
If A_i performs an active rollover, all funds not owned by A_i can *always* be used by B and C to route payments that are unrelated to the casual users in the timeout-tree (including both before and after A_i's funds are drained).
This idea was described in the "Improving Capital Efficiency" section of the post.

Passive rollovers complicate this, as A_i's funds are neither definitely in the old timeout-tree or in the new timeout-tree during the rollover.
However, if one is willing to take on the complexity, it's possible to use *your* (very cool!) idea of funding an HTLC from one of two possible sources, where one of those sources is guaranteed to eventually be available (but the offerer and offeree of the HTLC don't know which one will be available to them) [2][3].
In this case, B and C could use the funds from the old and the new timeout-trees that are not owned by A_i to route payments.
If A_i puts the leaf in the old timeout-tree on-chain, B and C use funds from the new timeout-tree to fund their HTLC (and vice-versa).

Even if hierarchical channels are used to improve the capital efficiency, I think the "thundering herd" problem is a big concern.
This could play out very poorly in practice, as casual users would gain experience with ever larger timeout-trees and not have any problems.
Then, suddenly, a large number of dedicated users collude by failing to roll-over timeout-trees at the same time, and they create enough congestion on the blockchain that they're able to steal a large fraction of the casual users' funds.

I have a proposed change to the Bitcoin consensus rules that I think could address this problem.
Basically, rather than have timeout-trees expire at a given block height, they should expire only after a sufficient number of low-fee blocks have been added to the blockchain after some given block height.
As a result, if dedicated users colluded and tried to steal funds by not rolling-over a group of timeout-trees, the thundering herd of transactions from casual users would push up the fees enough to prevent the timeout-trees from expiring, thus safeguarding the casual user's funds.
In fact, the impact to the dedicated users (in addition to their loss of reputation) would be that their capital would be unavailable to them for a longer period of time.
Thus, this should be effective in deterring dedicated users from attempting such a theft.
On the other hand, when the dedicated users do roll-over funds correctly, there is no delay in the old timeout-trees' expiries, and thus better capital efficiency.

There are lots of details to the idea and I'm currently in the process of writing a paper and post describing it.
A couple more quick details:
* rather than counting low-fee blocks, time is measured in low-fee windows, where the size of the window is programmable (this makes it much harder for dishonest miners to collude with the dedicated users by creating enough fake low-fee blocks, not containing the casual users' higher-fee timeout-tree transactions, to enabe the theft; it also reduces the compute cost for counting the low-fee windows),
* the threshold for a "low-fee" block is programmable,
* there is a bound on how long one keeps waiting for low-fee windows (in order to bound the storage and compute overheads), and
* a similar technique supports relative, rather than absolute, delays.

I think such a mechanism is likely to be useful in many areas, including HTLCs, but that timeout-trees really highlight the need for something like this.

Regards,
John

[1] Law, "Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://github.com/JohnLaw2/ln-hierarchical-channels
[2] Towns, "Re: Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-April/003913.html
[3] Law, "Re: Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-April/003917.html




Sent with Proton Mail secure email.




------------------------------

Message: 2
Date: Sun, 17 Sep 2023 00:56:04 +0000
From: jlspc <jlspc@protonmail.com>
To: Rusty Russell <rusty@rustcorp.com.au>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<djxZBOI49yXSwCjEVPVoBipCliOadhstw8fwfUja4m8bVM3AN79d5luAsXJiva1f8sE0_kXRyLIcv0E_9Wqbwba71woBw3hTehWOQ5JzJ74=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Rusty,

>         I've read the start of the paper on my vacation, and am still
> digesting it.  But even so far, it presents some delightful
> possibilities.

Great!

> As with some other proposals, it's worth noting that the cost of
> enforcement is dramatically increased.  It's no longer one or two txs,
> it's 10+.  If the "dedicated user" contributes some part of the expected
> fee, the capital efficiency is reduced (and we're back to "how much is
> enough?").

Yes, this is certainly an issue, and it affects both settling the channel on-chain and resolving HTLCS on-chain.
The paper has a few ideas about how "short-cut" transactions could be used to address the cost of enforcing HTLCs on-chain.
It may be possible to do something similar for the channel itself, but that's more complex because of the value included in the channel and the potential for channels with different capacities in a single timeout-tree.

> But worst case (dramatic dedicated user failure) it's only a 2x penalty
> on number of onchain txs, which seems acceptable if the network is
> sufficiently mature that these failure events are rare.

> Note also that the (surprisingly common!) "user goes away" case where
> the casual user fails to rollover only returns funds to the dedicated
> user; relying on legal and normal custody policies in this case may be
> preferable to an eternal burden on the UTXO set with the current
> approach!

Agreed.

Thanks,
John

> Thankyou!
> Rusty.





Sent with Proton Mail secure email.




------------------------------

Message: 3
Date: Sun, 17 Sep 2023 00:59:39 +0000
From: jlspc <jlspc@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<5jNOgQZP4xLtap2YxvsoZTXJwqa9wkL_ZdLH5RHlKzpmWdDIJhCm8tqJU8tGL7u36YKPlcJjoDHAbrLYkuXxB3-aPcQhDtovgKuVKkiUhPA=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Antoine,

Thanks for your note. Responses are in-line below:

> Hi John,

> Thanks for the proposal, few feedback after a first look.

> &gt;<i> If Bitcoin and Lightning are to become widely-used, they will have to be adopted by casual users who want to send and receive bitcoin, but &gt; who do not want to go to any effort in order to provide the infrastructure for making payments.
> </i>&gt;<i> Instead, it's reasonable to expect that the Lightning infrastructure will be provided by dedicated users who are far less numerous than
> </i>
> I don't know if it is that simple to classify expected users in
> "casual"-vs"dedicated" and then design protocols accordingly. In
> practice, if you take today Lightning as an example the trust
> assumptions is more a matrix than a dichotomie, e.g you have the
> choice between full-node vs light client to get block-relay,
> large-sized mempool vs small mempool or no mempool at all for fee
> estimations, routing HTLCs or not, running local watchtower or not...
> without all those choices being necessarily interdependent. Generally,
> I would say "tell me your IO disk/bandwidth/CPU performance/fees
> ressources and level of technical knowledge and I'll tell you what
> level of trust-minimization you can afford".

Fair enough.

I'm sure there are users with a wide range of expertise, resources, and interest in supporting Bitcoin.
My main point is that there's a huge pool of potential users that just want payments to work, and they don't want to devote time or hardware resources to making them work (if they can get away with that).
I also think we should do whatever we can to meet their needs.

> &gt;<i> This difference in numbers implies that the key challenge in scaling Bitcoin and Lightning is providing bitcoin and Lightning to casual
> </i>
> &gt;<i> users.
> </i>&gt;<i> As a result, the rest of this post will focus on this challenge.
> </i>
> I think few different scaling notions can be introduced to measure the
> performance of an off-chain construction. Onboarding scaling defining
> how many users can co-exist off-chain, considering throughput limits
> (e.g blocksize, average block interval). Transactional scaling
> defining how many transfers can be performed off-chain per on-chain
> transaction, considering the properties of the off-chain system. Users
> resource scaling defining how much resource a user should mobilize /
> consume (e.g average weight cost for cooperative /  non-cooperative
> close) to make a trust-minimized usage of the off-chain construction.
> I think the proposal is mainly considering onboarding scalability, i.e
> maxing out the number of channels that can be owned by a user though
> it is unclear if other scalability dimensions are weighted in.

Yes, exactly.
I've focused on providing multiple channels to as many casual users as possible.

In terms of other scalability dimensions, I think Lightning does a great job of providing a nearly unbounded number of payments per channel, without requiring on-chain transactions (once the channel is created).
I also think resizing channels can be done fairly effectively off-chain with hierarchical channels [1] (and even better with hierarchical channels within timeout-trees).

> In particular, no known protocol that uses the current Bitcoin
> consensus rules allows a large number (e.g., tens-of-thousands to
> millions) of Lightning channels, each co-owned by a casual user, to be
> created from a single on-chain unspent transaction output (UTXO).

> I?m not sure if this statement is 100% accurate. One could create a
> radixpool with replacing CTV usage with Musig2 where the end
> transactions outputs bear Lightning channel:
> <a href="https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017968.html.">https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017968.html.</a>

> Of course there is no N-party update mechanism to rebalance the
> channel internally and it?s a nightmare if a subranch of transactions
> with some depth hit the chain, though I think it works with today
> Bitcoin consensus rules.

I agree that it's theoretically possible to use signatures to create Lightning channels for a million casual users that are funded by a single UTXO.
I just don't believe that that is possible in practice, due to the need to get a million casual users to sign a transaction where the transaction specifies the casual users that need to sign it.

> The requirement for casual users to sign transactions that specify the
> exact set of casual users whose signatures are required creates a very
> difficult group coordination problem that's not well-suited to the
> behavior of casual users [9, Section 2.2].

> I think you have two more precise problems designated under this group
> coordination problem. One is the dynamic novation of this group, i.e
> how you add / remove user, if possible in a compact fashion. The
> second the dynamic update of the ?account? / channels owned by the
> users of this group, if possible with minimal interactivity.

Yes, changing who pairs with whom and resizing channels are both important problems.

I propose that changing pairings be done only via the creation and expiry of timeout-trees (with users that want to keep pairing with the same dedicated user(s) doing so via passive rollovers).
I propose that channel resizing is mainly done via hierarchical channels, with any resizing that's not possible to do off-chain in that manner being done via creation and expiry of timeout-trees.

With these proposals, it's possible to dramatically limit the interactivity.

For example, if every channel created by a timeout-tree is a hierarchical channel of the form:
* (casual user, (dedicated user, dedicated user)), or
* (dedicated user, (dedicated user, dedicated user)), or
* ((dedicated user, dedicated user), (dedicated user, dedicated user)),
then at most four users ever have to coordinate to update any channel, and at most one of those users is ever a casual user.

> &gt;<i> On the other hand, sometime shortly before E, casual user A_i can use the Lightning Network to send all of their balance in the channel &gt; &gt; (A_i, B) to themselves in some other Lightning channel that is the leaf of some other timeout-tree.
> </i>
> I think there is an uncertainty in this model as there is no guarantee
> that you have a dedicated user ready to be the gateway to route the
> balance, neither the dedicated user have adequate channel topology
> allowing to send the funds in the part of the network you wish to do
> so. And this is unclear what the casual user is left to do if an
> intermediate hop withhold the HTLC in-flight until the timeout-tree
> mature in favor of the dedicated user, iiuc.

> So I think draining is uncertain in a world where jamming is possible,
> even assuming economic mitigation as one might earn more to jam a
> casual user draining than loosing in jamming upfront fees.

I agree that active draining by the casual user is uncertain.
I propose that if the active drain fails, the casual user should put their channel in the old timeout-tree on-chain (so that it won't timeout on them).
Sorry that wasn't clear.

> &gt;<i> Of course, sometime between E - to_self_delay_i and E, A_i should verify that B has created such a new timeout-tree.
> </i>
> I think this requirement is altering the design goal introduced at
> first on casual users ?performing actions at specific times in the
> future? as from my understanding there is no guarantee B broadcast an
> on-chain transaction triggering the move of A funds to the new
> timeout-tree. This becomes unclear when A should take correction
> actions like broadcasting its own control transaction (?) when B fails
> to dos, especially in a world where you have mempool congestion, and
> earlier you?re better it might in term of fee risk.

Ideally, I'd like casual users to only perform actions when they want to send or receive a payment.
Unfortunately, I don't know how to do that.
As a result, I've been forced to add a requirement that each casual user turns on their wallet software for a few minutes (but at a time of their choosing!) every few months (with the exact number of months being selected by the user) [2].
I agree this isn't ideal, but I think it's much better than having them have to perform some action at a specific time or within a very limited time window (such as a day or a week).

> &gt;<i> Fortunately, timeout-trees can be used to provide casual users with immediately-accessible off-chain bitcoin in addition to bitcoin in
> </i>
> I think this is unclear what is meant by ?immediately-accessible?
> here, if they?re confirmed or not. Pre-signed / pre-committed
> transactions at a fixed feerate might still not propagate on the
> network, due to mempool min fee, and the user might have to take
> actions in consequence like access hot wallet and sign a CPFP.

I agree that the bitcoin may not be obtained if the user hasn't signed and submitted a transaction with sufficient fees.
I tried to address this issue in the "Limitations" section of the post (specifically, Limitationss 2 and 3).

I think that getting a reliable transport mechanism for packages is critical.

Getting fees right could be particularly challenging due to the "thundering herd" problem, as _aj_ pointed out.
As I noted in my response to him, I think an additional change to Bitcoin that allows timing based on fee levels could be very helpful.
I'll try to write up the details and get that out as soon as possible.

> &gt;<i> In reality, their on-chain footprint would be dominated by users who don't follow the protocol due to errors, unavailability, or malicious &gt; intent.
> </i>
> The fault-tolerance of such off-chain construction is very unclear i.e
> if for any unavailable or erring user the whole off-chain construction
> ends up on-chain. This is one significant defect in my opinion of the
> radixpool or old school apo channel factory (or even coinpool if no
> time-locked kick-out transaction is used), if one user becomes
> unresponsive after a while.

With a timeout-tree, if the dedicated user(s) funding the tree is unavailable (or makes an error) and fails to rollover a given casual user, that casual user should put their channel in the old timeout-tree on-chain.
If the failure applies to all channels in the timeout-tree, the entire timeout-tree will be forced to go on-chain (thus doubling the number of on-chain transactions as compared to just putting the channels on-chain directly, without a timeout-tree).
Sorry this wasn't made clear.

These costs could be large, but hopefully they're rare as they are failures by dedicated users that can afford to have highly-available hardware and who want to maintain a good reputation.

Separately, HTLCs that are not resolved off-chain have to be put on-chain, but doing so does not force the timeout-tree itself to go on-chain.
If the HTLC control transactions are funded via zero-valued covenant trees (as proposed in the post and paper), putting an HTLC transaction on-chain can also require putting its ancestors in the covenant tree on-chain (thus creating a blow-up that is logarithmic in the number of leaves in the covenant tree).
However, the paper has a proposal for the use of "short-cut" transactions that may be able to eliminate this logarithmic blow-up.

Thanks for your thoughtful comments and please let me know if there's anything else that wasn't clear.

Regards,
John

> Best,

> Antoine

[1] Law, "Resizing Lightning Channels Off-Chain With Hierarchical Channels", https://github.com/JohnLaw2/ln-hierarchical-channels
[2] Law, "Watchtower-Free Lightning Channels For Casual Users", https://github.com/JohnLaw2/ln-watchtower-free

Sent with [Proton Mail](https://proton.me/) secure email.

>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230917/556e2033/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 19
********************************************
