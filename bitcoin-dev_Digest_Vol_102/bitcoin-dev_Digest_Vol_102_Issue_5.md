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

   1. Re: [Mempool spam] Should we as developers reject
      non-standard Taproot transactions from full nodes? (Brad Morrison)
   2. Re: [Mempool spam] Should we as developers reject
      non-standard Taproot transactions from full nodes? (Melvin Carvalho)


----------------------------------------------------------------------

Message: 1
Date: Fri, 03 Nov 2023 03:15:58 -0700
From: Brad Morrison <bradmorrison@sonic.net>
To: Melvin Carvalho <melvincarvalho@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Mempool spam] Should we as developers
	reject non-standard Taproot transactions from full nodes?
Message-ID: <46e412585ce8143727c40c66edae83e0@sonic.net>
Content-Type: text/plain; charset="utf-8"

Melvin/all, 

You make good points about high network fees being disruptive. 

What is more disruptive are spikes & valleys (instability) that last
longer than the mempool cycle can handle. 

Right now, https://mempool.space/ indicates that there are about 105,000
unconfirmed transactions and that current memory usage is 795 mb of 300
mb. 

We could compare the bitcoin networks' ability to process transactions
to the California Independent System Operator's (CAISO -
https://www.caiso.com/Pages/default.aspx) task of ensuring the CA
electrical grid stays supplied with the least expensive electricity
available and does not get overloaded, nor has to export too much
electrical power to other grids in times of surplus. 

A big part of doing that is noticing past trends and preparing for
future growth, if that is the goal. 

Expanding the block size is the simplest way to expand network capacity
and lower transactional costs. 

Thank you, 

Brad

On 2023-05-08 09:37, Melvin Carvalho via bitcoin-dev wrote:

> po 8. 5. 2023 v 13:55 odes?latel Ali Sherief via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> napsal: 
> 
>> Hi guys, 
>> 
>> I think everyone on this list knows what has happened to the Bitcoin mempool during the past 96 hours. Due to side projects such as BRC-20 having such a high volume, real bitcoin transactions are being priced out and that is what is causing the massive congestion that has arguable not been seen since December 2017. I do not count the March 2021 congestion because that was only with 1-5sat/vbyte. 
>> 
>> Such justifiably worthless ("worthless" is not even my word - that's how its creator described them[1]) tokens threaten the smooth and normal use of the Bitcoin network as a peer-to-pear digital currency, as it was intended to be used as. 
>> 
>> If the volume does not die down over the next few weeks, should we take an action? The bitcoin network is a triumvirate of developers, miners, and users. Considering that miners are largely the entities at fault for allowing the system to be abused like this, the harmony of Bitcoin transactions is being disrupted right now. Although this community has a strong history of not putting its fingers into pies unless absolutely necessary - an example being during the block size wars and Segwit - should similar action be taken now, in the form of i) BIPs and/or ii) commits into the Bitcoin Core codebase, to curtail the loophole in BIP 342 (which defines the validation rules for Taproot scripts) which has allowed these unintended consequences? 
>> 
>> An alternative would be to enforce this "censorship" at the node level and introduce a run-time option to instantly prune all non-standard Taproot transactions. This will be easier to implement, but won't hit the road until minimum next release. 
>> 
>> I know that some people will have their criticisms about this, absolutists/libertarians/maximum-freedom advocates, which is fine, but we need to find a solution for this that fits everyone's common ground. We indirectly allowed this to happen, which previously wasn't possible before. So we also have a responsibility to do something to ensure that this kind of congestion can never happen again using Taproot.
> 
> This is a nuanced and sensitive topic that has been discussed previously, as far back as 2010, in a conversation between Gavin and Satoshi: 
> 
> https://bitcointalk.org/index.php?topic=195.msg1617#msg1617 
> 
> Gavin: That's a cool feature until it gets popular and somebody decides it would be fun to flood the payment network with millions of transactions to transfer the latest Lady Gaga video to all their friends...
> Satoshi: That's one of the reasons for transaction fees.  There are other things we can do if necessary. 
> 
> High fees could be viewed as disruptive to the network, but less disruptive than regular large reorgs, or a network split. 
> 
> It might be beneficial to brainstorm the "other things we can do if necessary". 
> 
> A simple observation is that increasing the block size could make it more challenging to spam, though it may come at the expense of some decentralization. 
> 
>> -Ali 
>> 
>> --- 
>> 
>> [1]: https://www.coindesk.com/consensus-magazine/2023/05/05/pump-the-brcs-the-promise-and-peril-of-bitcoin-backed-tokens/ [1] 
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
 

Links:
------
[1]
https://www.coindesk.com/consensus-magazine/2023/05/05/pump-the-brcs-the-promise-and-peril-of-bitcoin-backed-tokens/?outputType=amp
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231103/6ba1404a/attachment.html>

------------------------------

Message: 2
Date: Fri, 3 Nov 2023 11:39:23 +0100
From: Melvin Carvalho <melvincarvalho@gmail.com>
To: Brad Morrison <bradmorrison@sonic.net>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Mempool spam] Should we as developers
	reject non-standard Taproot transactions from full nodes?
Message-ID:
	<CAKaEYhKhsd0FKmGhfSSQ+2-P6GKLk2rAFrBJrpNaza0PuWApeQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

p? 3. 11. 2023 v 11:16 odes?latel Brad Morrison <bradmorrison@sonic.net>
napsal:

> Melvin/all,
>
> You make good points about high network fees being disruptive.
>
> What is more disruptive are spikes & valleys (instability) that last
> longer than the mempool cycle can handle.
>
> Right now, https://mempool.space/ indicates that there are about 105,000
> unconfirmed transactions and that current memory usage is 795 mb of 300 mb.
>
> We could compare the bitcoin networks' ability to process transactions to
> the California Independent System Operator's (CAISO -
> https://www.caiso.com/Pages/default.aspx) task of ensuring the CA
> electrical grid stays supplied with the least expensive electricity
> available and does not get overloaded, nor has to export too much
> electrical power to other grids in times of surplus.
>
> A big part of doing that is noticing past trends and preparing for future
> growth, if that is the goal.
>
> Expanding the block size is the simplest way to expand network capacity
> and lower transactional costs.
>

The block size is a sensitive topic, as it has been used as an attack
vector in the past.  It is now a loaded topic baked into the mythology of
the project.  Discourse on the topic benefit from a dispassionate analysis
of the technical trade-offs and what properties of the network they affect.

There exists an attack on bitcoin where the lowest fee rises to make it
much harder to participate.  You could imagine a well funded attack,
creating fees of, say, 10,000 sats/vbyte, for a period of time.

While this could be viewed as positive from one lens (miners benefit),
there would at least be a vocal minority, legitimately arguing that this is
disruptive to the ordinary function of the network.

It's worth recognizing that a bigger block size makes this kind of
disruptive attack more expensive.

It's a tricky topic because of the history, and because some of the "spam"
may be seen by some as legitimate.

I think in the long-term miners and users will treat the fee auction in new
ways, with the use of AI algorithms.  Trillions are transmitted through the
bitcoin network.  A fraction of that is captured.  As the block subsidy
goes away over the next 2 decades, it might lead to a kind of "AI mexican
standoff" where the highest value transactions pay a bit more for priority
transfers.  AI will likely change the game theory, and we'll find out how,
over the next 2 epochs.

If that is the case, then block size can increase with hardware advances,
while maintaining much valued decentralized properties of the network.  In
this regard we probably would benefit from things like stratumv2 and
utreexo being rolled out first.


> Thank you,
>
> Brad
>
>
>
> On 2023-05-08 09:37, Melvin Carvalho via bitcoin-dev wrote:
>
>
>
> po 8. 5. 2023 v 13:55 odes?latel Ali Sherief via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> napsal:
>
>> Hi guys,
>>
>> I think everyone on this list knows what has happened to the Bitcoin
>> mempool during the past 96 hours. Due to side projects such as BRC-20
>> having such a high volume, real bitcoin transactions are being priced out
>> and that is what is causing the massive congestion that has arguable not
>> been seen since December 2017. I do not count the March 2021 congestion
>> because that was only with 1-5sat/vbyte.
>>
>> Such justifiably worthless ("worthless" is not even my word - that's how
>> its creator described them[1]) tokens threaten the smooth and normal use of
>> the Bitcoin network as a peer-to-pear digital currency, as it was intended
>> to be used as.
>>
>> If the volume does not die down over the next few weeks, should we take
>> an action? The bitcoin network is a triumvirate of developers, miners, and
>> users. Considering that miners are largely the entities at fault for
>> allowing the system to be abused like this, the harmony of Bitcoin
>> transactions is being disrupted right now. Although this community has a
>> strong history of not putting its fingers into pies unless absolutely
>> necessary - an example being during the block size wars and Segwit - should
>> similar action be taken now, in the form of i) BIPs and/or ii) commits into
>> the Bitcoin Core codebase, to curtail the loophole in BIP 342 (which
>> defines the validation rules for Taproot scripts) which has allowed these
>> unintended consequences?
>>
>> An alternative would be to enforce this "censorship" at the node level
>> and introduce a run-time option to instantly prune all non-standard Taproot
>> transactions. This will be easier to implement, but won't hit the road
>> until minimum next release.
>>
>> I know that some people will have their criticisms about this,
>> absolutists/libertarians/maximum-freedom advocates, which is fine, but we
>> need to find a solution for this that fits everyone's common ground. We
>> indirectly allowed this to happen, which previously wasn't possible before.
>> So we also have a responsibility to do something to ensure that this kind
>> of congestion can never happen again using Taproot.
>>
>
> This is a nuanced and sensitive topic that has been discussed previously,
> as far back as 2010, in a conversation between Gavin and Satoshi:
>
> https://bitcointalk.org/index.php?topic=195.msg1617#msg1617
>
> Gavin: That's a cool feature until it gets popular and somebody decides it
> would be fun to flood the payment network with millions of transactions to
> transfer the latest Lady Gaga video to all their friends...
> Satoshi: That's one of the reasons for transaction fees.  There are other
> things we can do if necessary.
>
> High fees could be viewed as disruptive to the network, but less
> disruptive than regular large reorgs, or a network split.
>
> It might be beneficial to brainstorm the "other things we can do if
> necessary".
>
> A simple observation is that increasing the block size could make it more
> challenging to spam, though it may come at the expense of some
> decentralization.
>
>
>>
>> -Ali
>>
>> ---
>>
>> [1]:
>> https://www.coindesk.com/consensus-magazine/2023/05/05/pump-the-brcs-the-promise-and-peril-of-bitcoin-backed-tokens/
>> <https://www.coindesk.com/consensus-magazine/2023/05/05/pump-the-brcs-the-promise-and-peril-of-bitcoin-backed-tokens/?outputType=amp>
>>
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231103/ce3992f7/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 5
*******************************************
