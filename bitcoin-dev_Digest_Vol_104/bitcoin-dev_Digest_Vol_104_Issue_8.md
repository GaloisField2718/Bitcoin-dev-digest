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

   1. Re: Compressed Bitcoin Transactions (Tom Briar)


----------------------------------------------------------------------

Message: 1
Date: Fri, 05 Jan 2024 15:06:01 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: Tom Briar <tombriar11@protonmail.com>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<xk6TD_XVlJodelVrD6HTzj-YZ6MaRJ8lU_ugEddOixoQfCmn59oQYKw-QZOwjL7b_LENm1Jza4NtBKAaXWqwHwcOOyvwlUbJuKw7f5lkm1s=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi,

After reviewing all the feedback and writing a reference implementation, I have linked the updated schema and a Draft PR for a reference Implementation to Bitcoin Core.

Some of the major changes consist of:

- Removing the grinding of the nLocktime in favor of a relative block height, which all of the Compressed Inputs use.
- And the use of a second kind of Variable Integer.

Compressed Transaction Schema:

[compressed_transactions.md](https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md)

Reference Impl/Draft PR:

https://github.com/bitcoin/bitcoin/pull/29134

Thanks-Tom.

Text of Compressed_Transactions.md:

Compressed Transaction Schema

By (Tom Briar) and (Andrew Poelstra)

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#1-abstract1. Abstract

With this Transaction Compression Schema we use several methods to compress transactions, including dropping data and recovering it on decompression by grinding until we obtain valid signatures.

The bulk of our size savings come from replacing the prevout of each input by a block height and index. This requires the decompression to have access to the blockchain, and also means that compression is ineffective for transactions that spend unconfirmed or insufficiently confirmed outputs.

Even without compression, Taproot keyspends are very small: as witness data they include only a single 64/65-byte signature and do not repeat the public key or any other metadata. By using pubkey recovery, we obtain Taproot-like compression for legacy and Segwit transactions.

The main applications for this schema are for steganography, satellite/radio broadcast, and other low bandwidth channels with a high CPU availability on decompression. We assume users have some ability to shape their transactions to improve their compressibility, and therefore give special treatment to certain transaction forms.

This schema is easily reversible except when compressing the Txid/Vout input pairs(Method 4). Compressing the input Txid/Vout is optional, and without it still gleans 50% of the total compression. This allows for the additional use case of P2P communication.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#2-methods2. Methods

The four main methods to achieve a lower transactions size are:

- packing transaction metadata before the transaction and each of its inputs and outputs to determine the structure of the following data.
- replacing 32-bit numeric values with either variable-length integers (VarInts) or compact-integers (CompactSizes).
- using compressed signatures and public key recovery upon decompression.
- replacing the 36-byte txid/vout pair with a blockheight and output index.

Method 4 will cause the compressed transaction to be undecompressable if a block reorg occurs at or before the block it's included in. Therefore, we'll only compress the Txid if the transaction input is at least one hundred blocks old.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#3-schema3 Schema

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#31-primitives3.1 Primitives

Name	Width	Description
CompactSize	1-5 Bytes	For 0-253, encode the value directly in one byte. For 254-65535, encode 254 followed by 2 little-endian bytes. For 65536-(2^32-1), encode 255 followed by 4 little-endian bytes.
CompactSize flag	2 Bits	1, 2 or 3 indicate literal values. 0 indicates that the value will be encoded in a later CompactInt.
VarInt	1+ Bytes	7-bit little-endian encoding, with each 7-bit word encoded in a byte. The highest bit of each byte is 1 if more bytes follow, and 0 for the last byte.
VLP-Bytestream	2+ Bytes	A VarInt Length Prefixed Bytestream. Has a VarInt prefixed to determine the length.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#32-general-schema3.2 General Schema

Name	Width	Description
Transaction Metadata	1 Byte	Information on the structure of the transaction. See Section 3.3.
Version	0-5 Bytes	An optional CompactSize containing the transactions version.
Input Count	0-5 Bytes	An optional CompactSize containing the transactions input count.
Output Count	0-5 Bytes	An optional CompactSize containing the transactions output count.
LockTime	0-5 Bytes	An optional CompactSize containing the transaction LockTime if its non zero.
Minimum Blockheight	1-5 Bytes	A VarInt containing the Minimum Blockheight of which the transaction locktime and input blockheights are given as offsets.
Input Metadata+Output Metadata	1+ Bytes	A Encoding containing metadata on all the inputs and then all the outputs of the transaction. For each input see Section 3.4, for each output see Section 3.5.
Input Data	66+ Bytes	See Section 3.6 for each input.
Output Data	3+ Bytes	See Section 3.7 for each output.

For the four CompactSize listed above we could use a more compact bit encoding for these but they are already a fall back for the bit encoding of the Transaction Metadata.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#33-transaction-metadata3.3 Transaction Metadata

Name	Width	Description
Version	2 Bits	A CompactSize flag for the transaction version.
Input Count	2 Bits	A CompactSize flag for the transaction input count.
Output Count	2 Bits	A CompactSize flag for the transaction output count.
LockTime	1 Bit	A Boolean to indicate if the transaction has a LockTime.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#34-input-metadata3.4 Input Metadata

Name	Width	Description
Compressed Signature	1 Bit	Signature compression flag. For P2TR: 1 for keyspend, 0 for scriptspend; For P2SH: 0 for p2sh, 1 for p2sh-wpkh.
Standard Hash	1 Bit	A flag to determine if this Input's Signature Hash Type is standard (0x00 for Taproot, 0x01 for Legacy/Segwit).
Standard Sequence	2 Bits	A CompactSize flag for the inputs sequence. Encode literal values as follows: 1 = 0x00000000, 2 = 0xFFFFFFFE, 3 = 0xFFFFFFFF.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#351-output-metadata3.5.1 Output Metadata

Name	Width	Description
Encoded Script Type	3 Bits	Encoded Script Type.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#352-script-type-encoding3.5.2 Script Type encoding

Script Type	Value
Uncompressed P2PK	0b000
Compressed P2PK	0b001
P2PKH	0b010
P2SH	0b011
P2WSH	0b100
P2WPKH	0b101
P2TR	0b110
Uncompressed Custom Script	0b111

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#36-input-data3.6 Input Data

Name	Width	Description
Sequence	0-5 Bytes	An Optional VarInt containing the sequence if it was non-standard.
Txid Blockheight	1-5 Bytes	A VarInt Either containing 0 if this an uncompressed input, or it contains the offset from Minimum Blockheight for this Txid.
Txid/Signature Data	65+ Bytes	Txid/Signatures are determined to be uncompressed either by the output script of the previous transaction, or if the Txid Blockheight is zero. For each Compressed Txid/Signature See Section 3.6.1. For each Uncompressed Txid/Signature See Section 3.6.2.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#361-compressed-txidsignature-data3.6.1 Compressed Txid/Signature Data

Name	Width	Description
Txid Block Index	1-5 Bytes	A VarInt containing the flattened index from the Txid Blockheight for the Vout.
Signature	64 Bytes	Contains the 64 byte signature.
Hash Type	0-1 Bytes	An Optional Byte containing the Hash Type if it was non-standard.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#362-uncompressed-txidsignature-data3.6.2 Uncompressed Txid/Signature Data

Name	Width	Description
Txid	32 Bytes	Contains the 32 byte Txid.
Vout	1-5 Bytes	A CompactSize Containing the Vout of the Txid.
Signature	2+ Bytes	A VLP-Bytestream containing the signature.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#37-output-data3.7 Output Data

Name	Width	Description
Output Script	2+ Bytes	A VLP-Bytestream containing the output script.
Amount	1-9 Bytes	A VarInt containing the output amount.

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#4-ideal-transaction4 Ideal Transaction

The target transaction for the most optimal compression was chosen based off the most common transactions that are likely to be used for purposes that requires the best compression.

Field	Requirements	Possible Savings
Version	Less than four	30 Bits
Input Count	Less then four	30 Bits
Output Count	Less then four	30 Bits
LockTime	0	30 Bits
Input Sequence	0x00, 0xFFFFFFFE, or 0xFFFFFFFF	62 Bits For Each Input
Input Txid	Compressed Outpoint	23-31 Bytes For Each Input
Input Vout	Compressed Outpoint	(-1)-3 Bytes For Each Input
Input Signature	Non-custom Script Signing	40-72 Bytes For Each Legacy Input
Input Hash Type	0x00 for Taproot, 0x01 for Legacy	7 Bits For Each Input
Output Script	Non-custom Scripts	2-5 Bytes For Each Output
Output Amount	No Restrictions	(-1)-7 Bytes For Each Output

https://github.com/TomBriar/bitcoin/blob/2023-05--tx-compression/doc/compressed_transactions.md#5-test-vectors5 Test Vectors

Transaction	Before Compression	Possible Savings	After Compression
2-(input/output) Taproot	312 Bytes	78-124 Bytes and 2 Bits	190-226 Bytes
2-(input/output) Legacy	394 Bytes	118-196 Bytes and 2 Bits	176-244 Bytes

Taproot (Uncompressed)

020000000001028899af77861ede1ee384c333974722c96eabba8889506725b00735fc35ba41680000000000000000008899af77861ede1ee384c333974722c96eabba8889506725b00735fc35ba41680000000000000000000288130000000000002251206b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda00f000000000000225120dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd20140f3d9bcc844eab7055a168a62f65b8625e3853fad8f834d5c82fdf23100b7b871cf48c2c956e7d76cdd367bbfefe496c426e64dcfeaef800ab9893142050714b6014081c15fe5ed6b8a0c0509e871dfbb7784ddb22dd33b47f3ad1a3b271d29acfe76b5152b53ed29a7f6ea27cb4f5882064da07e8430aacafab89a334b32780fcb2700000000

Taproot (Compressed)

2a81de3177d8019c2ef3d9bcc844eab7055a168a62f65b8625e3853fad8f834d5c82fdf23100b7b871cf48c2c956e7d76cdd367bbfefe496c426e64dcfeaef800ab9893142050714b6019c2e81c15fe5ed6b8a0c0509e871dfbb7784ddb22dd33b47f3ad1a3b271d29acfe76b5152b53ed29a7f6ea27cb4f5882064da07e8430aacafab89a334b32780fcb276b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dd8827dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd2a01f

Legacy (Uncompressed)

02000000000102c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc549000000000000000000c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc5490000000000000000000288130000000000002251206b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda00f000000000000225120dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd202473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618702473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618700000000

Legacy (Compressed)

2ad1e53044d801ae276c0002473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd461870001ae276c0002473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd46187006b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dd8827dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd2a01f

On Tuesday, September 5th, 2023 at 2:30 PM, Tom Briar via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi Peter,
>
> Currently, if we?re given a lock time that is non zero, we drop the 16 most significant bits and grind through until we have a valid signature. Therefore I am hesitant to add more fields to grind through, because it can get out of hand in decompression time really quickly. That said our ideal use case for transaction compression is small high security transactions, I doubt they will need a lock time in most cases. Perhaps we should drop grinding the lock time in favor of grinding the block height.
>
> Either way assuming both parties agree on the block height(which is a must right now) having a single block height for the transaction might save us several bytes.
>
> I?m working on adding an ideal transaction spec to the doc right now.
>
> Thanks!-
> Tom.
>
> On Tue, Sep 5, 2023 at 12:00 PM, Peter Todd via bitcoin-dev <[bitcoin-dev@lists.linuxfoundation.org](mailto:On Tue, Sep 5, 2023 at 12:00 PM, Peter Todd via bitcoin-dev <<a href=)> wrote:
>
>> On Fri, Sep 01, 2023 at 01:56:18PM +0000, Andrew Poelstra via bitcoin-dev wrote:
>>> We can swag what the space savings would be: there are 122MM utxos right
>>> now, which is a bit under 2^27. So assuming a uniform distribution of
>>> prefixes we'd need to specify 28 bits to identify a UTXO. To contrast,
>>> to identify a blockheight we need 20 bits and then maybe 12 more bits to
>>> specify a TXO within a block. Plus whatever varint overhead we have.
>>> (I've been working on this project but busy with family stuff and don't
>>> remember exactly where we landed on the varints for this. I think we
>>> agreed that there was room for improvement but didn't want to hold up
>>> posting the rest of the concept because of it.)
>>
>> Since most transactions spend txouts that are similar in height to each other,
>> you could save further bits by specifying a reference height and then encoding
>> the exact txout with a delta.
>>
>> If you're sending multiple txins or multiple transactions in a single packet,
>> you could achieve this by starting the packet with the reference block height.
>>
>> If your application tends to send just a single transaction, you could use a
>> reference height that is a function of the current time. Since sender and
>> receiver might not agree on the exact time, you could try slightly difference
>> reference heights via bruteforcing until the transaction signatures validate.
>>
>> --
>> https://petertodd.org 'peter'[:-1]@petertodd.org
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240105/d16d28f7/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 8
*******************************************
