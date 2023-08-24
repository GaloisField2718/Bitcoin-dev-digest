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

   1. Re: Civ Kit: A Peer-to-Peer Electronic Market System
      (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Fri, 30 Jun 2023 04:46:32 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Chris Stewart <chris@suredbits.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Civ Kit: A Peer-to-Peer Electronic Market
	System
Message-ID:
	<CALZpt+GZgnRTpQZOpHQEo5Txt-DJZ+Zu=frm0OkoX6gzhZP-rg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Chris,

Thanks for the review and sorry for the late answer here.

> To summarize, assume we have Mary the Maker, Terry the Taker, and Bob the
bulletin board operator
>
> 1. Mary the Maker publishes a limit order to buy a derivative
> 2. Bob the bulletin board operator has the option to execute against
Mary's order
> 3. If Bob doesn't want to execute against the order, he relays the order
to Terry the Taker (and other subscribers to Bob's market)
> 4. Terry has the option to execute a trade against Mary's limit order
> 5. If Terry decides not to execute, Mary's order sits on the bulletin
board.
>
> I personally don't think this is that big of a concern, if Bob can
collect outsized profits from his trusted position as the bulletin board
operator, Terry will eventually move to other markets because Bob is
> only relaying what Bob perceives to be unprofitable orders.

Yes this is somehow a design assumption of the CivKit architecture, to keep
the migration cost low from a bulletin board to another one, if all the
orders are executed by the "house" based on privileged "market-making"
liquidity, and the outsized profits makes it interesting for another
incumbent to enter into the market, you will spawn competing bulletin
boards showing up.

Note, Terry the maker client might be okay to follow and pay the premium
for access to a market board, if the board has a very consistent policy
protecting against "bad" order wasting timevalue of Terry's liquidity.

> From the perspective of Mary, she is happy. Her order got executed at the
price she specified. Terry is the one that loses here. This model ends up
looking much more like a brokerage rather than an
> exchange market structure. Terry should open up his own brokerage
(bulletin board) and compete on quoting prices with Bob.

Yes, I think this is very expected that you might have tiered services
where you have a market bulletin board specialized in processing
large-scale volume of data (with high-guarantees of fault-tolerance) and
another hand "brokers" which have more content aggregators. The brokerage
service will be harder to "trust-minimized", unless somehow all the Bobs
are publishing their quoting prices in real-time.

> Bob and Terry can then be compared on metrics like execution quality
<https://clearingcustody.fidelity.com/trade-execution-quality>, which then
draws more market activity since they are providing better prices.

Yes, I think this is more or less the type of "board monitoring" algorithms
suggested in section 5 "orderbook risks", though the scoring criterias are
not presented like for the Fidelity definition of quality (i.e price
improvement, execution price, execution speed, effective spread).

One can expect to have this running as a "watchtower" like we have under
deployment for Lightning clients with fluctuating levels of flappyness.

> This. Frontrunning is a good problem to have, that means your market has
active participants and liquidity. Finding what products people are
interested in trading, and giving them a good user experience > is more
important. Everything else will fall in line after that.

While the first approach is the one more described in the CivKit paper,
from the history of peer-to-peer systems bootstrap, relying on social
assumptions like the over-the-counter ones might be more prolific. It might
also be a better user experience when people are exchanging cash versus
satoshis on the ground, or any other physical goods.

Ideally, if the offers data structures and the reputation framework common
between both OTC and "public boards" you might have traffic flows
circulating between both, and users will pick up the trading approach that
fits more the type of trades they wish to engage into. Compatibility of the
key-material for the clients between the different contexts sounds to
matter for smooth bootstrap too.

Best,
Antoine

Le mar. 9 mai 2023 ? 16:09, Chris Stewart <chris@suredbits.com> a ?crit :

> >In traditional finance, front-running is defined as "entering into an
> equity trade, options or future contracts with advance knowledge of a block
> transaction that will influence the price of the underlying security to
> capitlize on the trade" [0]. In Bitcoin/Civkit parlance, a front-running
> could be a board on the discovery of a batch of market offers increasing
> liquidity for a fiat-2-btc pair, seizing the opportunity by forwarding a
> HTLC across a Lightning payment path to enter into the trade, before
> publishing the offer on its board.
>
> To summarize, assume we have Mary the Maker, Terry the Taker, and Bob the
> bulletin board operator
>
> 1. Mary the Maker publishes a limit order to buy a derivative
> 2. Bob the bulletin board operator has the option to execute against
> Mary's order
> 3. If Bob doesn't want to execute against the order, he relays the order
> to Terry the Taker (and other subscribers to Bob's market)
> 4. Terry has the option to execute a trade against Mary's limit order
> 5. If Terry decides not to execute, Mary's order sits on the bulletin
> board.
>
> I personally don't think this is that big of a concern, if Bob can collect
> outsized profits from his trusted position as the bulletin board operator,
> Terry will eventually move to other markets because Bob is only relaying
> what Bob perceives to be unprofitable orders.
>
> From the perspective of Mary, she is happy. Her order got executed at the
> price she specified. Terry is the one that loses here. This model ends up
> looking much more like a brokerage rather than an exchange market
> structure. Terry should open up his own brokerage (bulletin board) and
> compete on quoting prices with Bob.
>
> Bob and Terry can then be compared on metrics like execution quality
> <https://clearingcustody.fidelity.com/trade-execution-quality>, which
> then draws more market activity since they are providing better prices.
>
> >Somehow mass front-running on the board is a "champagne" issue I'll be
> happy to have.
>
> This. Frontrunning is a good problem to have, that means your market has
> active participants and liquidity. Finding what products people are
> interested in trading, and giving them a good user experience is more
> important. Everything else will fall in line after that.
>
>
> On Mon, May 1, 2023 at 1:06?PM Antoine Riard via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> Hi all,
>>
>> One of the most relevant feedback I received on the paper publication was the lack of underscoring front-running resistance as a fundamental property wished for a peer-to-peer marketplace.
>>
>> It is expected the level of front-running resistance aimed by the market participants to be heavily functioned by the types of trades considered: fiat currencies, real goods, services. For some classes of goods, e.g commodities one cannot expect the same level of item liquidity due to cycle of production and exogenous factors like weather. Some types of trades marketplaces might be exposed to far less front-running risks and rather would have to deal with accurate risk modelling of the underlying goods. E.g attest there is a decentralized identifier or any other linkage proof of the physical good existence staying valid for the duration of offer lifetime. Offers conditions themselves might be far more verbose and precise special Bitcoin Script paths to morph the shipment risks.
>>
>> On the other hand, the types of trades like fiat currencies or bitcoin financial contracts (e.g discreet log contracts or submarine swaps), front-running risk by the bulletin board sounds a qualified concern. In traditional finance, front-running is defined as "entering into an equity trade, options or future contracts with advance knowledge of a block transaction that will influence the price of the underlying security to capitlize on the trade" [0]. In Bitcoin/Civkit parlance, a front-running could be a board on the discovery of a batch of market offers increasing liquidity for a fiat-2-btc pair, seizing the opportunity by forwarding a HTLC across a Lightning payment path to enter into the trade, before publishing the offer on its board.
>>
>> I think you have at least two security paradigms to mitigate front-running happening peer-to-peer marketplace. The first one is to duplicate the announcement of the offers to a number of concurrent board operated by independent identities and in parallel monitor the latency. Latency anomalies should be spotted on by watchtower-like infrastructure at the service of makers/takers and in case of repeated anomalies a maker should disqualify the misbehaving board from future announcements. As all statistical mitigation it is not perfect and open the way to some margin of exploitation by the boards, as the watchtower monitoring frequency can be guessed. Additionally, this latency monitoring paradigm sounds to be valid under the assumption that at least one board is "honest" and board might have a holistic interest to silently collude. Running or accessing monitoring infrastructure comes with a new liveliness requirement or additional cost for mobile clients.
>>
>> Another paradigm can be to run the bulletin boards as a federation e.g under Honey Badger BFT as used by Fedimint [1]. The incoming board offers become consensus items that must be announced to all the federations members onion gateway and which are not announced before a consensus proposal has been adopted. The e-cash tokens can be rather Bitcoin-paid credentials required by the board federation for publication. The federation members earn an income as a group to follow the consensus rules and be paid only when there is "consensus" publication. The federation could adopt some "DynFed" techniques to extend the federation set [2]. One can imagine a federation consisting of all the significant market participants, leveling the field for all.
>>
>> Is there another security paradigm direction to mitigate front-running and other asymmetries of information ? I can't immediately imagine more though I believe it stays an interesting open question.
>>
>> In fine, the Civkit proposes a flexible framework for peer-to-peer marketplace, where propagation latency monitoring and federation set and rules can be tweaked as "front-running resistance" parameters, adapting to the types of trades and market participants tolerance. Configuration of those parameters will at the end be function of real-world deployments. Somehow mass front-running on the board is a "champagne" issue  I'll be happy to have.
>>
>> Best,
>> Antoine
>>
>> [0] https://www.finra.org/investors/insights/getting-speed-high-frequency-trading
>> [1] https://fedimint.org/docs/CommonTerms/HBBFTConsensus
>> [2] https://blockstream.com/assets/downloads/pdf/liquid-whitepaper.pdf
>>
>>
>> Le jeu. 13 avr. 2023 ? 15:10, Antoine Riard <antoine.riard@gmail.com> a
>> ?crit :
>>
>>> Hi list,
>>>
>>> We have been working since a while with Nicholas Gregory (Commerce
>>> Block), Ray Youssef (the Built With Bitcoin foundation) and few others on a
>>> new peer-to-peer market system to enable censorship-resistant and
>>> permissionless global trading in all parts of the world. While the design
>>> aims in priority to serve on-ramp/off-ramp trading, it can be extended to
>>> support any kind of trading: goods, services, bitcoin financial derivatives
>>> like discreet log contracts.
>>>
>>> The design combines the Nostr architecture of simple relays announcing
>>> trade orders to their clients with Lightning onion routing infrastructure,
>>> therefore granting high-level of confidentiality to the market
>>> participants. The market boards are Nostr relays with a Lightning gateway,
>>> each operating autonomously and in competition. The market boards can be
>>> runned as a federation however there is no "decentralized orderbook" logged
>>> into the blockchain. The trades are escrowed under Bitcoin Script
>>> contracts, relying on moderations and know your peer oracles for
>>> adjudication.
>>>
>>> The scoring of trades, counterparties and services operators should be
>>> enabled by the introduction of a Web-of-Stakes, assembled from previous
>>> ideas [0]. From the Bitcoin UTXO set servicing as a trustless source of
>>> truth, an economic weight can be assigned to each market entity. This
>>> reputation paradigm could be composed with state-of-the-art Web-of-Trust
>>> techniques like decentralized identifiers [1].
>>>
>>> A consistent incentive framework for service operators is proposed by
>>> the intermediary of privacy-preserving credentials backed by Bitcoin
>>> payments, following the lineaments of IETF's Privacy Pass [2]. Services
>>> operators like market boards and oracles are incentivized to thrive for
>>> efficiency, akin to routing hops on Lightning and miners on the base layer.
>>>
>>> The whitepaper goes deep in the architecture of the system [3] (Thanks
>>> to the peer reviewers!).
>>>
>>> We'll gradually release code and modules, extensively building on top of
>>> the Lightning Dev Kit [4] and Nostr libraries. All according to the best
>>> Bitcoin open-source and decentralized standards established by Bitcoin Core
>>> and we're looking forward to collaborating with everyone in the community
>>> to standardize libraries and guarantee interoperability between clients
>>> with long-term thinking.
>>>
>>> Feedback is very welcome!
>>>
>>> Cheers,
>>> Nick, Ray and Antoine
>>>
>>> [0]
>>> https://lists.linuxfoundation.org/pipermail/lightning-dev/2020-November/002884.html
>>> [1] https://www.w3.org/TR/2022/REC-did-core-20220719/
>>> [2] https://privacypass.github.io
>>> [3] https://github.com/civkit/paper/blob/main/civ_kit_paper.pdf
>>> [4] https://lightningdevkit.org
>>>
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230630/863f1023/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 26
*******************************************
