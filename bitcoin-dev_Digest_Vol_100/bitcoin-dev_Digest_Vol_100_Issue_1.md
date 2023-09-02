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

   1. Compressed Bitcoin Transactions (Tom Briar)
   2. Re: Compressed Bitcoin Transactions (Andrew Poelstra)
   3. Re: Compressed Bitcoin Transactions (Fabian)
   4. Re: Compressed Bitcoin Transactions (Fabian)


----------------------------------------------------------------------

Message: 1
Date: Thu, 31 Aug 2023 21:30:16 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<WJoM7dyrk0o8ujOZOo462r66wS2Kl3L1ZZRodvaLK-HKEUc90yvwOqXbUUrGbV1lk6cOywTqLoCyHzk2Tm3TtBFyUL0NZ6D7v9NmTXypJPA=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hey everyone,

I've been working on a way to compress bitcoin transactions for transmission throughsteganography, satellite broadcasting,
and other low bandwidth channels with high CPU availability on decompression.

[compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)

In the document I describe a compression schema that's tailored for the most common transactions single parties are likely to make.
In every case it falls back such that no transaction will become malformed or corrupted.
Here's a PR for implementing this schema.

[2023 05 tx compression](https://github.com/TomBriar/bitcoin/pull/3)
Thanks-
Tom.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230831/a40bc759/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 1 Sep 2023 00:49:36 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Tom Briar <tombriar11@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID: <ZPE1IDggzquwP+WN@camus>
Content-Type: text/plain; charset="us-ascii"

On Thu, Aug 31, 2023 at 09:30:16PM +0000, Tom Briar via bitcoin-dev wrote:
> Hey everyone,
> 
> I've been working on a way to compress bitcoin transactions for transmission throughsteganography, satellite broadcasting,
> and other low bandwidth channels with high CPU availability on decompression.
> 
> [compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)
> 
> In the document I describe a compression schema that's tailored for the most common transactions single parties are likely to make.
> In every case it falls back such that no transaction will become malformed or corrupted.
> Here's a PR for implementing this schema.
> 
> [2023 05 tx compression](https://github.com/TomBriar/bitcoin/pull/3)

Hey Tom,


Thank you for posting this. Could you put together a chart with some
size numbers so we can get a picture of how strong this compression is?

I understand that because this is targeted at stego/satellite
applications where the user is expected to "shape" their transaction,
that you won't get great numbers if you just look at the historical
chain or try to analyze "average" transactions. But it would be great to
post a chart with uncompressed/compressed sizes for "optimum"
transactions. At the very least, a 2-in-2-out wpkh transaction, and a
2-in-2-out Taproot transaction.

Since the scheme includes explicit support for p2sh-wpkh and p2pkh it
would also be great to see numbers for those, though they're less common
and less interesting.


Cheers
Andrew



-- 
Andrew Poelstra
Director of Research, Blockstream
Email: apoelstra at wpsoftware.net
Web:   https://www.wpsoftware.net/andrew

The sun is always shining in space
    -Justin Lewis-Webster

-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 488 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230901/1a0ba0e7/attachment-0001.sig>

------------------------------

Message: 3
Date: Fri, 01 Sep 2023 10:24:54 +0000
From: Fabian <fjahr@protonmail.com>
To: Tom Briar <tombriar11@protonmail.com>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<KSmH1MBTPLuXMF4TWbWq6vaft_K_7IZS2YcoZ1iHwtHY06It1DjExVgSdrLBMQZA8mLGz8xdOzyXRHAZ2qCAugwG8gMtEGsGj-XNTPN0v0w=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Tom,

without having gone into the details yet, thanks for the great effort you have put into this research and implementation already!

> The bulk of our size savings come from replacing the prevout of each input by a block height and index.

Have you also considered using just an index from a sorted UTXO set instead? The potential additional space saving might be minor but this would make the scheme compatible with pruning. I had this on my list as a future research topic but didn't get around to it yet.

Thanks,
Fabian
------- Original Message -------
On Thursday, August 31st, 2023 at 11:30 PM, Tom Briar via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hey everyone,
>
> I've been working on a way to compress bitcoin transactions for transmission throughsteganography, satellite broadcasting,
> and other low bandwidth channels with high CPU availability on decompression.
>
> [compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)
>
> In the document I describe a compression schema that's tailored for the most common transactions single parties are likely to make.
> In every case it falls back such that no transaction will become malformed or corrupted.
> Here's a PR for implementing this schema.
>
> [2023 05 tx compression](https://github.com/TomBriar/bitcoin/pull/3)
> Thanks-
> Tom.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230901/5c5c8657/attachment.html>

------------------------------

Message: 4
Date: Fri, 01 Sep 2023 10:43:26 +0000
From: Fabian <fjahr@protonmail.com>
To: Tom Briar <tombriar11@protonmail.com>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<WnWsR9fDRLeWb6XZXWys_sqIuVlIfQG1K8MJdPiy22d1yIZcJnh3xrT7NMEDzmzoNCAYVr5fWa8j9JauSlF4tSEA1BwJ51VBgC65bJjiOeE=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Tom,

I realized I simplified my message a bit too much. Of course an index of the UTXO set would also need a height, so I rather meant some kind of composite reference I guess. An index alone might be enough if a height has been pre-agreed which could still be compatible with the use-cases you might have in mind, this might be very interesting in combination with assumeutxo. Otherwise a short hash could be used but then I also think your current scheme might be more space efficient than this.

Fabian
------- Original Message -------
On Friday, September 1st, 2023 at 12:24 PM, Fabian <fjahr@protonmail.com> wrote:

> Hi Tom,
>
> without having gone into the details yet, thanks for the great effort you have put into this research and implementation already!
>
>> The bulk of our size savings come from replacing the prevout of each input by a block height and index.
>
> Have you also considered using just an index from a sorted UTXO set instead? The potential additional space saving might be minor but this would make the scheme compatible with pruning. I had this on my list as a future research topic but didn't get around to it yet.
>
> Thanks,
> Fabian
> ------- Original Message -------
> On Thursday, August 31st, 2023 at 11:30 PM, Tom Briar via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> Hey everyone,
>>
>> I've been working on a way to compress bitcoin transactions for transmission throughsteganography, satellite broadcasting,
>> and other low bandwidth channels with high CPU availability on decompression.
>>
>> [compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)
>>
>> In the document I describe a compression schema that's tailored for the most common transactions single parties are likely to make.
>> In every case it falls back such that no transaction will become malformed or corrupted.
>> Here's a PR for implementing this schema.
>>
>> [2023 05 tx compression](https://github.com/TomBriar/bitcoin/pull/3)
>> Thanks-
>> Tom.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230901/ea64af6d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 1
*******************************************
