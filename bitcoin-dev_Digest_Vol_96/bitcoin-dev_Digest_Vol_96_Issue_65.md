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

   1. Encrypted (like BIP38) master private key (Ali Sherief)
   2. Re: Bitcoin Transaction Relay over Nostr (Joost Jager)
   3. Re: Bitcoin Transaction Relay over Nostr (Greg Sanders)


----------------------------------------------------------------------

Message: 1
Date: Tue, 30 May 2023 10:08:02 +0000
From: Ali Sherief <ali@notatether.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Encrypted (like BIP38) master private key
Message-ID:
	<gfD-2LnzCr5aG-DkxduQwI6Qd5zdMMA3quHucZ5g29CJEU6gHu8QSXeHkmtqYcLCdM6iV6HNyxzEduIAz2khQXCpOPQ65wgWr4sphpYGruQ=@notatether.com>
	
Content-Type: text/plain; charset="utf-8"

Just like we have BIPP38 encrypted keys for singular private keys, I was wondering if it would be possible to come up with a way to encrypt an extended private key using reversible encryption.

BIP38 was designed with physical coins in mind, and in particular covers the cases for lot and sequence numbers in detail.

There is a case to be made that in an encrypted extended private key, the lot and sequence numbers can be placed in the HD derivation path. In particular they can be derived like this: m/lot'/sequence' and both of them use hardened derivation.

The advantage would be that coinmakers would only have to generate one master private key during manufacturing instead of a ton of private keys.

But this is not a very convincing advantage so I'd like to hear what is other people's take on this.

-Ali
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230530/59054c47/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 30 May 2023 14:30:51 +0200
From: Joost Jager <joost.jager@gmail.com>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Bitcoin Transaction Relay over Nostr
Message-ID:
	<CAJBJmV-=berWDEeXfLcfyqQQPL5m32St9XUd02bTXJVOHZsM+Q@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi David,


> A block template is an ordered list of raw transactions that can all be
> included in the next block (with some space reserved for a coinbase
> transaction).  A full node can validate those transactions and calculate
> how much fee they pay.  A Nostr relay can simply relay almost[1] any
> template that pays more fees than the previous best template it saw for
> the next block.  That can be more flexible than the current
> implementation of submitblock with package relay which still enforces a
> lot of the rules that helps keep a regular relay node safe from DoS and
> a miner node able to select mineable transactions quickly.
>

Interesting idea! This would also make it easy for external services to try
to do the best possible block building using advanced algorithms. Miners
would just select the best template available from various sources
including nostr.


> A weak block is a block whose header doesn't quite hash to low enough of
> a value to be included on the chain.  It still takes an extraordinary
> amount of hashrate to produce, so it's inherently DoS resistant.  If
> miners are producing block that include transactions not seen by typical
> relay nodes, that can reduce the efficiency and effectiveness of BIP152
> compact block relay, which hurts the profitability of miners of custom
> blocks.  To compensate, miners could relay weak blocks through Nostr to
> full nodes and other miners so that they could quickly relay and accept
> complete blocks that later included the same custom transactions.  This
> would also help fee estimation and provide valuable insights to those
> trying to get their transactions included into the next block.
>

I believe this would be useful right away, wouldn't it? Looking at
mempool.space's block audit, there are definitely blocks that have a
"surprising" content and might take long to download.

The anti-dos measures that you describe for both weak blocks and block
templates seem very robust, but they would require a more intelligent nostr
relay to enforce. Not sure if it is still allowed to call it nostr at that
point. Perhaps it becomes more of a specialised bitcoin relay. btcstr -
"bitcoin stuff transmitted by relays".

Regarding size, the block template and weak block could both be sent in
> BIP152 compact block format as a diff against the expected contents of a
> typical node, allowing Alice to send just a small amount of additional
> data for relay over what she'd have to send anyway for each transaction
> in a package.  (Although it's quite possible that BetterHash or Stratum
> v2 have even better solutions, possibly already implemented.)
>

Sounds like a great way to repurpose what already exists to reduce resource
usage for these additional message types.


> If nothing else, I think Nostr could provide an interesting playground
> for experimenting with various relay and mining ideas we've talked about
> for years, so thanks again for working on this!
>

I think so too! The main question on my mind though is how to actually make
this work. There is a bit of a chicken-egg problem here with users and
miners possibly waiting for each other to adopt.

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230530/1f001ed5/attachment-0001.html>

------------------------------

Message: 3
Date: Tue, 30 May 2023 09:30:32 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Joost Jager <joost.jager@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Bitcoin Transaction Relay over Nostr
Message-ID:
	<CAB3F3DuoOdTAypfqptU94E_j4oNJuBwZHPifo8mmDxTOaSeyNQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Joost, David,

In my mind, weak blocks' main benefit would be that it improves block relay
by giving PoW-hints on what are in miner's mempools. Non-standard
transactions could even be cached(even if not validated until block
inclusion), which would tolerate more heterogeneity in policies without
drastically increasing relay times. Of course, it can also have the side
effect of gossiping better transaction packages, though I think this would
be a ton of work to really take advantage of. Perhaps we might be able to
do better in a post-cluster-mempool world, gossiping chunks.

At present I think energy would be best spent writing a weak blocks BIP
proposal, since one has never been written before(?), and it would be
fairly trivial to swap out p2p things with RPC calls if so desired for fast
experimentation over alternative relays.

Cheers,
Greg



On Tue, May 30, 2023 at 8:58?AM Joost Jager via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi David,
>
>
>> A block template is an ordered list of raw transactions that can all be
>> included in the next block (with some space reserved for a coinbase
>> transaction).  A full node can validate those transactions and calculate
>> how much fee they pay.  A Nostr relay can simply relay almost[1] any
>> template that pays more fees than the previous best template it saw for
>> the next block.  That can be more flexible than the current
>> implementation of submitblock with package relay which still enforces a
>> lot of the rules that helps keep a regular relay node safe from DoS and
>> a miner node able to select mineable transactions quickly.
>>
>
> Interesting idea! This would also make it easy for external services to
> try to do the best possible block building using advanced algorithms.
> Miners would just select the best template available from various sources
> including nostr.
>
>
>> A weak block is a block whose header doesn't quite hash to low enough of
>> a value to be included on the chain.  It still takes an extraordinary
>> amount of hashrate to produce, so it's inherently DoS resistant.  If
>> miners are producing block that include transactions not seen by typical
>> relay nodes, that can reduce the efficiency and effectiveness of BIP152
>> compact block relay, which hurts the profitability of miners of custom
>> blocks.  To compensate, miners could relay weak blocks through Nostr to
>> full nodes and other miners so that they could quickly relay and accept
>> complete blocks that later included the same custom transactions.  This
>> would also help fee estimation and provide valuable insights to those
>> trying to get their transactions included into the next block.
>>
>
> I believe this would be useful right away, wouldn't it? Looking at
> mempool.space's block audit, there are definitely blocks that have a
> "surprising" content and might take long to download.
>
> The anti-dos measures that you describe for both weak blocks and block
> templates seem very robust, but they would require a more intelligent nostr
> relay to enforce. Not sure if it is still allowed to call it nostr at that
> point. Perhaps it becomes more of a specialised bitcoin relay. btcstr -
> "bitcoin stuff transmitted by relays".
>
> Regarding size, the block template and weak block could both be sent in
>> BIP152 compact block format as a diff against the expected contents of a
>> typical node, allowing Alice to send just a small amount of additional
>> data for relay over what she'd have to send anyway for each transaction
>> in a package.  (Although it's quite possible that BetterHash or Stratum
>> v2 have even better solutions, possibly already implemented.)
>>
>
> Sounds like a great way to repurpose what already exists to reduce
> resource usage for these additional message types.
>
>
>> If nothing else, I think Nostr could provide an interesting playground
>> for experimenting with various relay and mining ideas we've talked about
>> for years, so thanks again for working on this!
>>
>
> I think so too! The main question on my mind though is how to actually
> make this work. There is a bit of a chicken-egg problem here with users and
> miners possibly waiting for each other to adopt.
>
> Joost
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230530/5d9a838f/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 65
*******************************************
