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

   1. Re: Concern about "Inscriptions" (Peter Todd)
   2. Re: Compressed Bitcoin Transactions (Peter Todd)
   3. Re: Compressed Bitcoin Transactions (Tom Briar)
   4. Re: Concern about "Inscriptions" (vjudeu@gazeta.pl)


----------------------------------------------------------------------

Message: 1
Date: Tue, 5 Sep 2023 17:49:43 +0000
From: Peter Todd <pete@petertodd.org>
To: vjudeu@gazeta.pl, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: GamedevAlice <gamedevalice256@gmail.com>
Subject: Re: [bitcoin-dev] Concern about "Inscriptions"
Message-ID: <ZPdqNxf2BsESnpIa@petertodd.org>
Content-Type: text/plain; charset="iso-8859-1"

On Sun, Sep 03, 2023 at 06:01:02PM +0200, vjudeu via bitcoin-dev wrote:
> > Given the current concerns with blockchain size increases due to inscriptions, and now that the lightning network is starting to gain more traction, perhaps people are now more willing to consider a smaller blocksize in favor of pushing more activity to lightning?
> ?
> People will not agree to shrink the maximum block size. However, if you want to kill inscriptions, there is another approach, that could be used to force them into second layers: it is called cut-through, and was described in this topic: https://bitcointalk.org/index.php?topic=281848.0
> ?
> Then, if you have "Alice -> Bob -> ... -> Zack" transaction chain, and for example some inscriptions were created in "Alice -> Bob" transaction, then cut-through could remove those inscriptions, while leaving the payment unaffected, because the proper amount of coins will be received by Zack, as it should be.

You are incorrect: cut-through transactions will not meaningfully affect
inscriptions. While it is true that with fancy cryptography we can prove the
Alice -> ... -> Zack chain, that does not change the fact that Alice -> Bob ->
Zack was mined in the blockchain, and those transactions exist. Anyone running
a full archival node will still have those transactions, and can provide them
(and all their inscription data) to anyone who needs it.

This is not unlike how in Bitcoin right now many people run pruned nodes that
do not have any archival inscription data. Them running those nodes does not
prevent others from running full archival nodes that do make that data
available.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230905/d69e604b/attachment-0001.sig>

------------------------------

Message: 2
Date: Tue, 5 Sep 2023 18:00:33 +0000
From: Peter Todd <pete@petertodd.org>
To: Andrew Poelstra <apoelstra@wpsoftware.net>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID: <ZPdswQ7uAJr35YbC@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Sep 01, 2023 at 01:56:18PM +0000, Andrew Poelstra via bitcoin-dev wrote:
> We can swag what the space savings would be: there are 122MM utxos right
> now, which is a bit under 2^27. So assuming a uniform distribution of
> prefixes we'd need to specify 28 bits to identify a UTXO. To contrast,
> to identify a blockheight we need 20 bits and then maybe 12 more bits to
> specify a TXO within a block. Plus whatever varint overhead we have.
> (I've been working on this project but busy with family stuff and don't
> remember exactly where we landed on the varints for this. I think we
> agreed that there was room for improvement but didn't want to hold up
> posting the rest of the concept because of it.)

Since most transactions spend txouts that are similar in height to each other,
you could save further bits by specifying a reference height and then encoding
the exact txout with a delta.

If you're sending multiple txins or multiple transactions in a single packet,
you could achieve this by starting the packet with the reference block height.

If your application tends to send just a single transaction, you could use a
reference height that is a function of the current time. Since sender and
receiver might not agree on the exact time, you could try slightly difference
reference heights via bruteforcing until the transaction signatures validate.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230905/8a5b529c/attachment-0001.sig>

------------------------------

Message: 3
Date: Tue, 05 Sep 2023 18:30:42 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: Peter Todd <pete@petertodd.org>, Andrew Poelstra
	<apoelstra@wpsoftware.net>, "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<hd13VCUTiTaX_Z4oeZpzwjdVOcmkbcg-kgfThk9b1LUt2YUCEXrwVuEq8BiNWtfzeAafo6GdsrFzGg3pQI5kSjuRc4TtFGmRndvVukAwAiY=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Peter,

Currently, if we?re given a lock time that is non zero, we drop the 16 most significant bits and grind through until we have a valid signature. Therefore I am hesitant to add more fields to grind through, because it can get out of hand in decompression time really quickly. That said our ideal use case for transaction compression is small high security transactions, I doubt they will need a lock time in most cases. Perhaps we should drop grinding the lock time in favor of grinding the block height.

Either way assuming both parties agree on the block height(which is a must right now) having a single block height for the transaction might save us several bytes.

I?m working on adding an ideal transaction spec to the doc right now.

Thanks!-
Tom.

On Tue, Sep 5, 2023 at 12:00 PM, Peter Todd via bitcoin-dev <[bitcoin-dev@lists.linuxfoundation.org](mailto:On Tue, Sep 5, 2023 at 12:00 PM, Peter Todd via bitcoin-dev <<a href=)> wrote:

> On Fri, Sep 01, 2023 at 01:56:18PM +0000, Andrew Poelstra via bitcoin-dev wrote:
>> We can swag what the space savings would be: there are 122MM utxos right
>> now, which is a bit under 2^27. So assuming a uniform distribution of
>> prefixes we'd need to specify 28 bits to identify a UTXO. To contrast,
>> to identify a blockheight we need 20 bits and then maybe 12 more bits to
>> specify a TXO within a block. Plus whatever varint overhead we have.
>> (I've been working on this project but busy with family stuff and don't
>> remember exactly where we landed on the varints for this. I think we
>> agreed that there was room for improvement but didn't want to hold up
>> posting the rest of the concept because of it.)
>
> Since most transactions spend txouts that are similar in height to each other,
> you could save further bits by specifying a reference height and then encoding
> the exact txout with a delta.
>
> If you're sending multiple txins or multiple transactions in a single packet,
> you could achieve this by starting the packet with the reference block height.
>
> If your application tends to send just a single transaction, you could use a
> reference height that is a function of the current time. Since sender and
> receiver might not agree on the exact time, you could try slightly difference
> reference heights via bruteforcing until the transaction signatures validate.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230905/6a89bf00/attachment-0001.html>

------------------------------

Message: 4
Date: Wed, 06 Sep 2023 10:00:53 +0200
From: vjudeu@gazeta.pl
To: Peter Todd <pete@petertodd.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: GamedevAlice <gamedevalice256@gmail.com>
Subject: Re: [bitcoin-dev] Concern about "Inscriptions"
Message-ID:
	<190339336-6f25cc7bcdad38e568613dcec5ff1039@pmq7v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> that does not change the fact that Alice -> Bob -> Zack was mined in the blockchain, and those transactions exist
?
If you use it in that way, then cut-through is pointless. The whole point of using it is scaling. If you have only "Alice -> Zack" transaction, that is included in some block, then cut-through is really useful. In other cases, if you include all transactions anyway, and create only a proof for some nodes, then it doesn't scale, because you have to always process those transactions in the middle, while there is no need to do so. It is needed only during batching, to prevent double-spending, but if it is deeply confirmed, then who needs something that doesn't scale?
?
Also, going in that direction is a natural consequence of enabling full-RBF: transactions will be replaced, which means mempool-level-batching (ideally non-interactive, done automatically by nodes) will be next, sooner or later.
?
On 2023-09-05 19:49:51 user Peter Todd <pete@petertodd.org> wrote:
On Sun, Sep 03, 2023 at 06:01:02PM +0200, vjudeu via bitcoin-dev wrote: > > Given the current concerns with blockchain size increases due to inscriptions, and now that the lightning network is starting to gain more traction, perhaps people are now more willing to consider a smaller blocksize in favor of pushing more activity to lightning? > ? > People will not agree to shrink the maximum block size. However, if you want to kill inscriptions, there is another approach, that could be used to force them into second layers: it is called cut-through, and was described in this topic: https://bitcointalk.org/index.php?topic=281848.0 > ? > Then, if you have "Alice -> Bob -> ... -> Zack" transaction chain, and for example some inscriptions were created in "Alice -> Bob" transaction, then cut-through could remove those inscriptions, while leaving the payment unaffected, because the proper amount of coins will be received by Zack, as it should be. You are incorrect: cut-through transactions wil
 l not meaningfully affect inscriptions. While it is true that with fancy cryptography we can prove the Alice -> ... -> Zack chain, that does not change the fact that Alice -> Bob -> Zack was mined in the blockchain, and those transactions exist. Anyone running a full archival node will still have those transactions, and can provide them (and all their inscription data) to anyone who needs it. This is not unlike how in Bitcoin right now many people run pruned nodes that do not have any archival inscription data. Them running those nodes does not prevent others from running full archival nodes that do make that data available. -- https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230906/8b4c08ec/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 5
*******************************************
