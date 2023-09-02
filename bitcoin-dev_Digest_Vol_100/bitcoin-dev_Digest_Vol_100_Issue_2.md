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

   1. Re: Compressed Bitcoin Transactions (Andrew Poelstra)
   2. Re: Compressed Bitcoin Transactions (Tom Briar)
   3. Re: Compressed Bitcoin Transactions (Jonas Schnelli)
   4. Re: Compressed Bitcoin Transactions (Tom Briar)


----------------------------------------------------------------------

Message: 1
Date: Fri, 1 Sep 2023 13:56:18 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Fabian <fjahr@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID: <ZPHtgiJQ4Yqrr941@camus>
Content-Type: text/plain; charset="us-ascii"

Hi Fabian,

We did consider indexing all txos -- even, amusingly, by using ordinals --
but decided that the extra index requirements for the decompressor (which
otherwise just requires a bit of extra CPU cycles but nothing beyond a
normal Core node).

A while ago we looked into putting the whole UTXOset into a trie so that
we could do prefix lookups. I think we discarded this idea for the same
reason, and because it could lead to surprising behavior for users since
a compressed tx might get invalidated by some UTXO showing up whose
prefix is too close to one of its inputs. Where "prefix" likely means
some special-purpose hash of the prevout that users will never otherwise
encounter.

We were also a bit put off by the data structure complexity since the
UTXO set no longer fits in RAM so it takes nontrivial effort to
implement a new index :) plus it drops our chances of getting code into
Core by a very large factor.

We can swag what the space savings would be: there are 122MM utxos right
now, which is a bit under 2^27. So assuming a uniform distribution of
prefixes we'd need to specify 28 bits to identify a UTXO. To contrast,
to identify a blockheight we need 20 bits and then maybe 12 more bits to
specify a TXO within a block. Plus whatever varint overhead we have.
(I've been working on this project but busy with family stuff and don't
remember exactly where we landed on the varints for this. I think we
agreed that there was room for improvement but didn't want to hold up
posting the rest of the concept because of it.)


The TL;DR is that we probably save a little less than a byte per input,
on average, which is not trivial but probably not worth the decreased
UX and greatly increased implementation complexity.


Best
Andrew



On Fri, Sep 01, 2023 at 10:24:54AM +0000, Fabian via bitcoin-dev wrote:
> Hi Tom,
> 
> without having gone into the details yet, thanks for the great effort you have put into this research and implementation already!
> 
> > The bulk of our size savings come from replacing the prevout of each input by a block height and index.
> 
> Have you also considered using just an index from a sorted UTXO set instead? The potential additional space saving might be minor but this would make the scheme compatible with pruning. I had this on my list as a future research topic but didn't get around to it yet.
> 
> Thanks,
> Fabian
> ------- Original Message -------
> On Thursday, August 31st, 2023 at 11:30 PM, Tom Briar via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> > Hey everyone,
> >
> > I've been working on a way to compress bitcoin transactions for transmission throughsteganography, satellite broadcasting,
> > and other low bandwidth channels with high CPU availability on decompression.
> >
> > [compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)
> >
> > In the document I describe a compression schema that's tailored for the most common transactions single parties are likely to make.
> > In every case it falls back such that no transaction will become malformed or corrupted.
> > Here's a PR for implementing this schema.
> >
> > [2023 05 tx compression](https://github.com/TomBriar/bitcoin/pull/3)
> > Thanks-
> > Tom.

> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230901/9169334e/attachment-0001.sig>

------------------------------

Message: 2
Date: Fri, 01 Sep 2023 14:12:09 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: Andrew Poelstra <apoelstra@wpsoftware.net>, Fabian
	<fjahr@protonmail.com>, "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<MBu12LnjA_GBVBrMQOBmMSopJCR3ZE0aOUhUFcTORmKjIvGm4gxfBzJGQrNgMkG99b4Z6mPEAkSU7PlHs2n6AzYYw4dw5FOovc0oJimrYvs=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Fabian,

Yes as Andrew said, creating a prefix tree is going to take up more space then simply the block height and then an index for the UTXO in the block. We removed the vout from the encoding by doing almost exactly what you said per block where it?s a flattened index over all the transactions and their outputs.

Andrews numbers on the required bits is accurate with 19 for the block height and 12 for the flattened index on average, although I suppose we can significantly reduce the number of bits required by the block height by having a bit indicate weather the block height is over 500000 or something similar.

Thanks-
Tom.

On Fri, Sep 1, 2023 at 7:56 AM, Andrew Poelstra <[apoelstra@wpsoftware.net](mailto:On Fri, Sep 1, 2023 at 7:56 AM, Andrew Poelstra <<a href=)> wrote:

> Hi Fabian,
>
> We did consider indexing all txos -- even, amusingly, by using ordinals --
> but decided that the extra index requirements for the decompressor (which
> otherwise just requires a bit of extra CPU cycles but nothing beyond a
> normal Core node).
>
> A while ago we looked into putting the whole UTXOset into a trie so that
> we could do prefix lookups. I think we discarded this idea for the same
> reason, and because it could lead to surprising behavior for users since
> a compressed tx might get invalidated by some UTXO showing up whose
> prefix is too close to one of its inputs. Where "prefix" likely means
> some special-purpose hash of the prevout that users will never otherwise
> encounter.
>
> We were also a bit put off by the data structure complexity since the
> UTXO set no longer fits in RAM so it takes nontrivial effort to
> implement a new index :) plus it drops our chances of getting code into
> Core by a very large factor.
>
> We can swag what the space savings would be: there are 122MM utxos right
> now, which is a bit under 2^27. So assuming a uniform distribution of
> prefixes we'd need to specify 28 bits to identify a UTXO. To contrast,
> to identify a blockheight we need 20 bits and then maybe 12 more bits to
> specify a TXO within a block. Plus whatever varint overhead we have.
> (I've been working on this project but busy with family stuff and don't
> remember exactly where we landed on the varints for this. I think we
> agreed that there was room for improvement but didn't want to hold up
> posting the rest of the concept because of it.)
>
> The TL;DR is that we probably save a little less than a byte per input,
> on average, which is not trivial but probably not worth the decreased
> UX and greatly increased implementation complexity.
>
> Best
> Andrew
>
> On Fri, Sep 01, 2023 at 10:24:54AM +0000, Fabian via bitcoin-dev wrote:
>> Hi Tom,
>>
>> without having gone into the details yet, thanks for the great effort you have put into this research and implementation already!
>>
>> > The bulk of our size savings come from replacing the prevout of each input by a block height and index.
>>
>> Have you also considered using just an index from a sorted UTXO set instead? The potential additional space saving might be minor but this would make the scheme compatible with pruning. I had this on my list as a future research topic but didn't get around to it yet.
>>
>> Thanks,
>> Fabian
>> ------- Original Message -------
>> On Thursday, August 31st, 2023 at 11:30 PM, Tom Briar via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>>
>> > Hey everyone,
>> >
>> > I've been working on a way to compress bitcoin transactions for transmission throughsteganography, satellite broadcasting,
>> > and other low bandwidth channels with high CPU availability on decompression.
>> >
>> > [compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)
>> >
>> > In the document I describe a compression schema that's tailored for the most common transactions single parties are likely to make.
>> > In every case it falls back such that no transaction will become malformed or corrupted.
>> > Here's a PR for implementing this schema.
>> >
>> > [2023 05 tx compression](https://github.com/TomBriar/bitcoin/pull/3)
>> > Thanks-
>> > Tom.
>
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
> --
> Andrew Poelstra
> Director of Research, Blockstream
> Email: apoelstra at wpsoftware.net
> Web: https://www.wpsoftware.net/andrew
>
> The sun is always shining in space
> -Justin Lewis-Webster
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230901/8d193e28/attachment-0001.html>

------------------------------

Message: 3
Date: Fri, 1 Sep 2023 18:56:22 +0200
From: Jonas Schnelli <dev@jonasschnelli.ch>
To: Tom Briar <tombriar11@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID: <CFB5479C-DCA9-492A-B5D9-06EFA415C47B@jonasschnelli.ch>
Content-Type: text/plain;	charset=us-ascii

Hi Tom

> I've been working on a way to compress bitcoin transactions for transmission through steganography, satellite broadcasting, 

Interesting. Some size numbers (vs plain, vs gzip) would be nice.

Maybe add a definition to your BIP that makes clear when NOT to use height/index due to risk of reorgs (similar to BIP136).

/j

------------------------------

Message: 4
Date: Fri, 01 Sep 2023 17:05:17 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: Jonas Schnelli <dev@jonasschnelli.ch>,
	"bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<zsCJFHf4O7dzsefVLHDTtxBVR-ozIAh5R0JQkSU83TmKpvhZrjz7K7pvonvTQS_XEuxVxILK8EErqeM_VIJ0dz1AiUjaA_HKn3enwpSXV3c=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Jonas,

I?m working to get numbers based on both historical data and from fuzz tests but I?m in the middle of updating the code to match the doc, I should have it finished before the end of the week.

We estimate that 100 blocks is safe from reorg, that is the same policyfor spending coin base transactions, in the PR I add a compressrawtransaction RPC endpoint that has that limit built in and will warn the user that the TxIdis uncompresssed due to it not being old enough. That said I?ll add it into the doc in case anyone adds onto it.

Thanks for the feedback!-

Tom.

On Fri, Sep 1, 2023 at 10:56 AM, Jonas Schnelli <[dev@jonasschnelli.ch](mailto:On Fri, Sep 1, 2023 at 10:56 AM, Jonas Schnelli <<a href=)> wrote:

> Hi Tom
>
>> I've been working on a way to compress bitcoin transactions for transmission through steganography, satellite broadcasting,
>
> Interesting. Some size numbers (vs plain, vs gzip) would be nice.
>
> Maybe add a definition to your BIP that makes clear when NOT to use height/index due to risk of reorgs (similar to BIP136).
>
> /j
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230901/66a683b8/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 2
*******************************************
