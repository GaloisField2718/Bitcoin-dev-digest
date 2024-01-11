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
   2. Introducing a version field to BIP39 mnemonic phrases (Leslie)


----------------------------------------------------------------------

Message: 1
Date: Tue, 09 Jan 2024 15:31:37 +0000
From: Tom Briar <tombriar11@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Compressed Bitcoin Transactions
Message-ID:
	<IFgPQiCptuVM6I5AsCE6VFrPMsGzBMK3x78GHlupJj12-rBloASYdafdBzyjSKC0H0EWLG2NNBzu1wEyYyyl1VzMmjW3nO7M-9OJpMxoEMM=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi,

After reviewing all the feedback and writing a reference implementation, I have linked the updated schema and a Draft PR for a reference Implementation to Bitcoin Core.

Some of the major changes consist of: 

Removing the grinding of the nLocktime in favor of a relative block height, which all of the Compressed Inputs use.
And the use of a second kind of Variable Integer.


Compressed Transaction Schema:

compressed_transactions.md

Reference Impl/Draft PR:

https://github.com/bitcoin/bitcoin/pull/29134

Thanks-
Tom.

=== begin compressed_transactions.md ===

# Compressed Transaction Schema
By (Tom Briar) and (Andrew Poelstra)

## 1. Abstract

With this Transaction Compression Schema we use several methods to compress transactions,
including dropping data and recovering it on decompression by grinding until we obtain
valid signatures.

The bulk of our size savings come from replacing the prevout of each input by a block
height and index. This requires the decompression to have access to the blockchain, and
also means that compression is ineffective for transactions that spend unconfirmed or
insufficiently confirmed outputs.

Even without compression, Taproot keyspends are very small: as witness data they
include only a single 64/65-byte signature and do not repeat the public key or
any other metadata. By using pubkey recovery, we obtain Taproot-like compression
for legacy and Segwit transactions.

The main applications for this schema are for steganography, satellite/radio broadcast, and
other low bandwidth channels with a high CPU availability on decompression. We
assume users have some ability to shape their transactions to improve their
compressibility, and therefore give special treatment to certain transaction forms.

This schema is easily reversible except for compressing the Txid/Vout input pairs(Method 4).
Compressing the input Txid/Vout is optional, and without it still gleans 50% of the
total compression. This allows for the additional use case of P2P communication.

## 2. Methods

The four main methods to achieve a lower transactions size are:

1. packing transaction metadata before the transaction and each of its inputs and
outputs to determine the structure of the following data.
2. replacing 32-bit numeric values with either variable-length integers (VarInts) or compact-integers (CompactSizes).
3. using compressed signatures and public key recovery upon decompression.
4. replacing the 36-byte txid/vout pair with a blockheight and output index.

Method 4 will cause the compressed transaction to be undecompressable if a block
reorg occurs at or before the block it's included in. Therefore, we'll only compress
the Txid if the transaction input is at least one hundred blocks old.


## 3 Schema

### 3.1 Primitives

| Name             | Width     | Description |
|------------------|-----------|-------------|
| CompactSize      | 1-5 Bytes | For 0-253, encode the value directly in one byte. For 254-65535, encode 254 followed by 2 little-endian bytes. For 65536-(2^32-1), encode 255 followed by 4 little-endian bytes. |
| CompactSize flag | 2 Bits    | 1, 2 or 3 indicate literal values. 0 indicates that the value will be encoded in a later CompactInt. |
| VarInt           | 1+ Bytes  | 7-bit little-endian encoding, with each 7-bit word encoded in a byte. The highest bit of each byte is 1 if more bytes follow, and 0 for the last byte. |
| VLP-Bytestream   | 2+ Bytes  | A VarInt Length Prefixed Bytestream. Has a VarInt prefixed to determine the length. |

### 3.2 General Schema

| Name                           | Width           | Description |
|--------------------------------|-----------------|-------------|
| Transaction Metadata           | 1 Byte    | Information on the structure of the transaction. See Section 3.3. |
| Version                        | 0-5 Bytes | An optional CompactSize containing the transactions version. |
| Input Count                    | 0-5 Bytes | An optional CompactSize containing the transactions input count. |
| Output Count                   | 0-5 Bytes | An optional CompactSize containing the transactions output count. |
| LockTime                       | 0-5 Bytes | An optional CompactSize containing the transaction LockTime if its non zero. |
| Minimum Blockheight            | 1-5 Bytes | A VarInt containing the Minimum Blockheight of which the transaction locktime and input blockheights are given as offsets. |
| Input Metadata+Output Metadata | 1+ Bytes  | A Encoding containing metadata on all the inputs and then all the outputs of the transaction. For each input see Section 3.4, for each output see Section 3.5. |
| Input Data                     | 66+ Bytes | See Section 3.6 for each input. |
| Output Data                    | 3+ Bytes  | See Section 3.7 for each output. |

For the four CompactSize listed above we could use a more compact bit encoding for these but they are already a fall back for the bit encoding of the Transaction Metadata.

### 3.3 Transaction Metadata

| Name         | Width  | Description |
|--------------|--------|-------------|
| Version      | 2 Bits | A CompactSize flag for the transaction version. |
| Input Count  | 2 Bits | A CompactSize flag for the transaction input count. |
| Output Count | 2 Bits | A CompactSize flag for the transaction output count. |
| LockTime     | 1 Bit  | A Boolean to indicate if the transaction has a LockTime. |

### 3.4 Input Metadata

| Name                 | Width  | Description |
|----------------------|--------|-------------|
| Compressed Signature | 1 Bit  | Signature compression flag. For P2TR: 1 for keyspend, 0 for scriptspend; For P2SH: 0 for p2sh, 1 for p2sh-wpkh. |
| Standard Hash        | 1 Bit  | A flag to determine if this Input's Signature Hash Type is standard (0x00 for Taproot, 0x01 for Legacy/Segwit). |
| Standard Sequence    | 2 Bits | A CompactSize flag for the inputs sequence. Encode literal values as follows: 1 = 0x00000000, 2 = 0xFFFFFFFE, 3 = 0xFFFFFFFF. |

### 3.5.1 Output Metadata

| Name                | Width  | Description |
|---------------------|--------|-------------|
| Encoded Script Type | 3 Bits | Encoded Script Type. |

#### 3.5.2 Script Type encoding

| Script Type                | Value |
|----------------------------|-------|
| Uncompressed P2PK          | 0b000 |
| Compressed P2PK            | 0b001 |
| P2PKH                      | 0b010 |
| P2SH                       | 0b011 |
| P2WSH                      | 0b100 |
| P2WPKH                     | 0b101 |
| P2TR                       | 0b110 |
| Uncompressed Custom Script | 0b111 |

### 3.6 Input Data

| Name                    | Width     | Description |
|-------------------------|-----------|-------------|
| Sequence                | 0-5 Bytes | An Optional VarInt containing the sequence if it was non-standard. |
| Txid Blockheight        | 1-5 Bytes | A VarInt Either containing 0 if this an uncompressed input, or it contains the offset from Minimum Blockheight for this Txid. |
| Txid/Signature Data     | 65+ Bytes | Txid/Signatures are determined to be uncompressed either by the output script of the previous transaction, or if the Txid Blockheight is zero. For each Compressed Txid/Signature See Section 3.6.1. For each Uncompressed Txid/Signature See Section 3.6.2. |

### 3.6.1 Compressed Txid/Signature Data

| Name              | Width     | Description |
|-------------------|-----------|-------------|
| Txid Block Index  | 1-5 Bytes | A VarInt containing the flattened index from the Txid Blockheight for the Vout. |
| Signature         | 64 Bytes  | Contains the 64 byte signature. |
| Hash Type         | 0-1 Bytes | An Optional Byte containing the Hash Type if it was non-standard.|

### 3.6.2 Uncompressed Txid/Signature Data

| Name      | Width     | Description |
|-----------|-----------|-------------|
| Txid      | 32 Bytes  | Contains the 32 byte Txid. |
| Vout      | 1-5 Bytes | A CompactSize Containing the Vout of the Txid. |
| Signature | 2+ Bytes  | A VLP-Bytestream containing the signature. |

### 3.7 Output Data

| Name          | Width     | Description |
|---------------|-----------|-------------|
| Output Script | 2+ Bytes  | A VLP-Bytestream containing the output script. |
| Amount        | 1-9 Bytes | A VarInt containing the output amount. |

## 4 Ideal Transaction

The target transaction for the most optimal compression was chosen
based off the most common transactions that are likely to be used
for purposes that requires the best compression.

| Field           | Requirements                      | Possible Savings                  |
|-----------------|-----------------------------------|-----------------------------------|
| Version         | Less than four                    | 30 Bits                           |
| Input Count     | Less then four                    | 30 Bits                           |
| Output Count    | Less then four                    | 30 Bits                           |
| LockTime        | 0                                 | 30 Bits                           |
| Input Sequence  | 0x00, 0xFFFFFFFE, or 0xFFFFFFFF   | 62 Bits For Each Input            |
| Input Txid      | Compressed Outpoint               | 23-31 Bytes For Each Input        |
| Input Vout      | Compressed Outpoint               | (-1)-3 Bytes For Each Input       |
| Input Signature | Non-custom Script Signing         | 40-72 Bytes For Each Legacy Input |
| Input Hash Type | 0x00 for Taproot, 0x01 for Legacy | 7 Bits For Each Input             |
| Output Script   | Non-custom Scripts                | 2-5 Bytes For Each Output         |
| Output Amount   | No Restrictions                   | (-1)-7 Bytes For Each Output      |

## 5 Test Vectors

| Transaction              | Before Compression | Possible Savings         | After Compression |
|--------------------------|--------------------|--------------------------|-------------------|
| 2-(input/output) Taproot | 312 Bytes          | 78-124 Bytes and 2 Bits  | 190-226 Bytes     |
| 2-(input/output) Legacy  | 394 Bytes          | 118-196 Bytes and 2 Bits | 176-244 Bytes     |

Taproot (Uncompressed)

020000000001028899af77861ede1ee384c333974722c96eabba8889506725b00735fc35ba41680000000000000000008899af77861ede1ee384c333974722c96eabba8889506725b00735fc35ba41680000000000000000000288130000000000002251206b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda00f000000000000225120dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd20140f3d9bcc844eab7055a168a62f65b8625e3853fad8f834d5c82fdf23100b7b871cf48c2c956e7d76cdd367bbfefe496c426e64dcfeaef800ab9893142050714b6014081c15fe5ed6b8a0c0509e871dfbb7784ddb22dd33b47f3ad1a3b271d29acfe76b5152b53ed29a7f6ea27cb4f5882064da07e8430aacafab89a334b32780fcb2700000000


Taproot (Compressed)

2ab0dd0177d801ad1cf3d9bcc844eab7055a168a62f65b8625e3853fad8f834d5c82fdf23100b7b871cf48c2c956e7d76cdd367bbfefe496c426e64dcfeaef800ab9893142050714b601ad1c81c15fe5ed6b8a0c0509e871dfbb7784ddb22dd33b47f3ad1a3b271d29acfe76b5152b53ed29a7f6ea27cb4f5882064da07e8430aacafab89a334b32780fcb276b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda608dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd29e20


Legacy (Uncompressed)

02000000000102c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc549000000000000000000c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc5490000000000000000000288130000000000002251206b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda00f000000000000225120dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd202473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618702473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618700000000


Legacy (Compressed)(Uncompressed Txid/Vout)

2a8efefefe7f44d800c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc549006c0002473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618700c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc549006c0002473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd461876b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda608dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd29e20



=== end compressed_transactions.md ===

On Friday, January 5th, 2024 at 10:19 AM, Andrew Poelstra via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Thanks Tom.
> 
> It looks like you posted a text-scrape of the rendered markdown, which
> is hard to read. For posterity here is the full text.
> 
> Best
> Andrew
> 
> 
> === begin compressed_transactions.md ===
> 
> # Compressed Transaction Schema
> By (Tom Briar) and (Andrew Poelstra)
> 
> ## 1. Abstract
> 
> With this Transaction Compression Schema we use several methods to compress transactions,
> including dropping data and recovering it on decompression by grinding until we obtain
> valid signatures.
> 
> The bulk of our size savings come from replacing the prevout of each input by a block
> height and index. This requires the decompression to have access to the blockchain, and
> also means that compression is ineffective for transactions that spend unconfirmed or
> insufficiently confirmed outputs.
> 
> Even without compression, Taproot keyspends are very small: as witness data they
> include only a single 64/65-byte signature and do not repeat the public key or
> any other metadata. By using pubkey recovery, we obtain Taproot-like compression
> for legacy and Segwit transactions.
> 
> The main applications for this schema are for steganography, satellite/radio broadcast, and
> other low bandwidth channels with a high CPU availability on decompression. We
> assume users have some ability to shape their transactions to improve their
> compressibility, and therefore give special treatment to certain transaction forms.
> 
> This schema is easily reversible except for compressing the Txid/Vout input pairs(Method 4).
> Compressing the input Txid/Vout is optional, and without it still gleans 50% of the
> total compression. This allows for the additional use case of P2P communication.
> 
> ## 2. Methods
> 
> The four main methods to achieve a lower transactions size are:
> 
> 1. packing transaction metadata before the transaction and each of its inputs and
> outputs to determine the structure of the following data.
> 2. replacing 32-bit numeric values with either variable-length integers (VarInts) or compact-integers (CompactSizes).
> 3. using compressed signatures and public key recovery upon decompression.
> 4. replacing the 36-byte txid/vout pair with a blockheight and output index.
> 
> Method 4 will cause the compressed transaction to be undecompressable if a block
> reorg occurs at or before the block it's included in. Therefore, we'll only compress
> the Txid if the transaction input is at least one hundred blocks old.
> 
> 
> ## 3 Schema
> 
> ### 3.1 Primitives
> 
> Name
> 
> Width
> 
> Description
> 
> CompactSize
> 
> 1-5 Bytes
> 
> For 0-253, encode the value directly in one byte. For 254-65535, encode 254 followed by 2 little-endian bytes. For 65536-(2^32-1), encode 255 followed by 4 little-endian bytes.
> 
> CompactSize flag
> 
> 2 Bits
> 
> 1, 2 or 3 indicate literal values. 0 indicates that the value will be encoded in a later CompactInt.
> 
> VarInt
> 
> 1+ Bytes
> 
> 7-bit little-endian encoding, with each 7-bit word encoded in a byte. The highest bit of each byte is 1 if more bytes follow, and 0 for the last byte.
> 
> VLP-Bytestream
> 
> 2+ Bytes
> 
> A VarInt Length Prefixed Bytestream. Has a VarInt prefixed to determine the length.
> 
> ### 3.2 General Schema
> 
> Name
> 
> Width
> 
> Description
> 
> --------------------------------
> 
> -----------------
> 
> -------------
> 
> Transaction Metadata
> 
> 1 Byte
> 
> Information on the structure of the transaction. See Section 3.3.
> 
> Version
> 
> 0-5 Bytes
> 
> An optional CompactSize containing the transactions version.
> 
> Input Count
> 
> 0-5 Bytes
> 
> An optional CompactSize containing the transactions input count.
> 
> Output Count
> 
> 0-5 Bytes
> 
> An optional CompactSize containing the transactions output count.
> 
> LockTime
> 
> 0-5 Bytes
> 
> An optional CompactSize containing the transaction LockTime if its non zero.
> 
> Minimum Blockheight
> 
> 1-5 Bytes
> 
> A VarInt containing the Minimum Blockheight of which the transaction locktime and input blockheights are given as offsets.
> 
> Input Metadata+Output Metadata
> 
> 1+ Bytes
> 
> A Encoding containing metadata on all the inputs and then all the outputs of the transaction. For each input see Section 3.4, for each output see Section 3.5.
> 
> Input Data
> 
> 66+ Bytes
> 
> See Section 3.6 for each input.
> 
> Output Data
> 
> 3+ Bytes
> 
> See Section 3.7 for each output.
> 
> For the four CompactSize listed above we could use a more compact bit encoding for these but they are already a fall back for the bit encoding of the Transaction Metadata.
> 
> ### 3.3 Transaction Metadata
> 
> Name
> 
> Width
> 
> Description
> 
> --------------
> 
> --------
> 
> -------------
> 
> Version
> 
> 2 Bits
> 
> A CompactSize flag for the transaction version.
> 
> Input Count
> 
> 2 Bits
> 
> A CompactSize flag for the transaction input count.
> 
> Output Count
> 
> 2 Bits
> 
> A CompactSize flag for the transaction output count.
> 
> LockTime
> 
> 1 Bit
> 
> A Boolean to indicate if the transaction has a LockTime.
> 
> ### 3.4 Input Metadata
> 
> Name
> 
> Width
> 
> Description
> 
> ----------------------
> 
> --------
> 
> -------------
> 
> Compressed Signature
> 
> 1 Bit
> 
> Signature compression flag. For P2TR: 1 for keyspend, 0 for scriptspend; For P2SH: 0 for p2sh, 1 for p2sh-wpkh.
> 
> Standard Hash
> 
> 1 Bit
> 
> A flag to determine if this Input's Signature Hash Type is standard (0x00 for Taproot, 0x01 for Legacy/Segwit).
> 
> Standard Sequence
> 
> 2 Bits
> 
> A CompactSize flag for the inputs sequence. Encode literal values as follows: 1 = 0x00000000, 2 = 0xFFFFFFFE, 3 = 0xFFFFFFFF.
> 
> ### 3.5.1 Output Metadata
> 
> Name
> 
> Width
> 
> Description
> 
> ---------------------
> 
> --------
> 
> -------------
> 
> Encoded Script Type
> 
> 3 Bits
> 
> Encoded Script Type.
> 
> #### 3.5.2 Script Type encoding
> 
> Script Type
> 
> Value
> 
> ----------------------------
> 
> -------
> 
> Uncompressed P2PK
> 
> 0b000
> 
> Compressed P2PK
> 
> 0b001
> 
> P2PKH
> 
> 0b010
> 
> P2SH
> 
> 0b011
> 
> P2WSH
> 
> 0b100
> 
> P2WPKH
> 
> 0b101
> 
> P2TR
> 
> 0b110
> 
> Uncompressed Custom Script
> 
> 0b111
> 
> ### 3.6 Input Data
> 
> Name
> 
> Width
> 
> Description
> 
> -------------------------
> 
> -----------
> 
> -------------
> 
> Sequence
> 
> 0-5 Bytes
> 
> An Optional VarInt containing the sequence if it was non-standard.
> 
> Txid Blockheight
> 
> 1-5 Bytes
> 
> A VarInt Either containing 0 if this an uncompressed input, or it contains the offset from Minimum Blockheight for this Txid.
> 
> Txid/Signature Data
> 
> 65+ Bytes
> 
> Txid/Signatures are determined to be uncompressed either by the output script of the previous transaction, or if the Txid Blockheight is zero. For each Compressed Txid/Signature See Section 3.6.1. For each Uncompressed Txid/Signature See Section 3.6.2.
> 
> ### 3.6.1 Compressed Txid/Signature Data
> 
> Name
> 
> Width
> 
> Description
> 
> -------------------
> 
> -----------
> 
> -------------
> 
> Txid Block Index
> 
> 1-5 Bytes
> 
> A VarInt containing the flattened index from the Txid Blockheight for the Vout.
> 
> Signature
> 
> 64 Bytes
> 
> Contains the 64 byte signature.
> 
> Hash Type
> 
> 0-1 Bytes
> 
> An Optional Byte containing the Hash Type if it was non-standard.
> 
> ### 3.6.2 Uncompressed Txid/Signature Data
> 
> Name
> 
> Width
> 
> Description
> 
> -----------
> 
> -----------
> 
> -------------
> 
> Txid
> 
> 32 Bytes
> 
> Contains the 32 byte Txid.
> 
> Vout
> 
> 1-5 Bytes
> 
> A CompactSize Containing the Vout of the Txid.
> 
> Signature
> 
> 2+ Bytes
> 
> A VLP-Bytestream containing the signature.
> 
> ### 3.7 Output Data
> 
> Name
> 
> Width
> 
> Description
> 
> ---------------
> 
> -----------
> 
> -------------
> 
> Output Script
> 
> 2+ Bytes
> 
> A VLP-Bytestream containing the output script.
> 
> Amount
> 
> 1-9 Bytes
> 
> A VarInt containing the output amount.
> 
> ## 4 Ideal Transaction
> 
> The target transaction for the most optimal compression was chosen
> 
> based off the most common transactions that are likely to be used
> 
> for purposes that requires the best compression.
> 
> Field
> 
> Requirements
> 
> Possible Savings
> 
> -----------------
> 
> -----------------------------------
> 
> -----------------------------------
> 
> Version
> 
> Less than four
> 
> 30 Bits
> 
> Input Count
> 
> Less then four
> 
> 30 Bits
> 
> Output Count
> 
> Less then four
> 
> 30 Bits
> 
> LockTime
> 
> 0
> 
> 30 Bits
> 
> Input Sequence
> 
> 0x00, 0xFFFFFFFE, or 0xFFFFFFFF
> 
> 62 Bits For Each Input
> 
> Input Txid
> 
> Compressed Outpoint
> 
> 23-31 Bytes For Each Input
> 
> Input Vout
> 
> Compressed Outpoint
> 
> (-1)-3 Bytes For Each Input
> 
> Input Signature
> 
> Non-custom Script Signing
> 
> 40-72 Bytes For Each Legacy Input
> 
> Input Hash Type
> 
> 0x00 for Taproot, 0x01 for Legacy
> 
> 7 Bits For Each Input
> 
> Output Script
> 
> Non-custom Scripts
> 
> 2-5 Bytes For Each Output
> 
> Output Amount
> 
> No Restrictions
> 
> (-1)-7 Bytes For Each Output
> 
> ## 5 Test Vectors
> 
> Transaction
> 
> Before Compression
> 
> Possible Savings
> 
> --------------------------
> 
> --------------------
> 
> --------------------------
> 
> 2-(input/output) Taproot
> 
> 312 Bytes
> 
> 78-124 Bytes and 2 Bits
> 
> 2-(input/output) Legacy
> 
> 394 Bytes
> 
> 118-196 Bytes and 2 Bits
> 
> Taproot (Uncompressed)
> 
> ```
> 
> 020000000001028899af77861ede1ee384c333974722c96eabba8889506725b00735fc35ba41680000000000000000008899af77861ede1ee384c333974722c96eabba8889506725b00735fc35ba41680000000000000000000288130000000000002251206b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda00f000000000000225120dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd20140f3d9bcc844eab7055a168a62f65b8625e3853fad8f834d5c82fdf23100b7b871cf48c2c956e7d76cdd367bbfefe496c426e64dcfeaef800ab9893142050714b6014081c15fe5ed6b8a0c0509e871dfbb7784ddb22dd33b47f3ad1a3b271d29acfe76b5152b53ed29a7f6ea27cb4f5882064da07e8430aacafab89a334b32780fcb2700000000
> 
> ```
> 
> Taproot (Compressed)
> 
> ```
> 
> 2a81de3177d8019c2ef3d9bcc844eab7055a168a62f65b8625e3853fad8f834d5c82fdf23100b7b871cf48c2c956e7d76cdd367bbfefe496c426e64dcfeaef800ab9893142050714b6019c2e81c15fe5ed6b8a0c0509e871dfbb7784ddb22dd33b47f3ad1a3b271d29acfe76b5152b53ed29a7f6ea27cb4f5882064da07e8430aacafab89a334b32780fcb276b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dd8827dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd2a01f
> 
> ```
> 
> Legacy (Uncompressed)
> 
> ```
> 
> 02000000000102c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc549000000000000000000c583fe4f934a0ed87e4d082cd52967cc774b943fbb2e21378ec18b926b8dc5490000000000000000000288130000000000002251206b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dda00f000000000000225120dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd202473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618702473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd4618700000000
> 
> ```
> 
> Legacy (Compressed)
> 
> ```
> 
> 2ad1e53044d801ae276c0002473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd461870001ae276c0002473044022000d1c81efcf6d20d87253749bcef8bf1be7ba51ccdf7a3b328174ea874226c3c02202d810c20f92d49c821eaa6e3a9ec7d764e0e71006e572d6ea96b631bd921767c0121037833d05665f3b21c479583ee12c6c573d1f25977dedfae12c70c18ec9dd46187006b10142cffb29e9d83f63a77a428be41f96bd9b6ccc9889e4ec74927058b41dd8827dd00ac641dc0f399e62a6ed6300aba1ec5fa4b3aeedf1717901e0d49d980efd2a01f
> 
> ```
> 
> --
> 
> Andrew Poelstra
> 
> Director of Research, Blockstream
> 
> Email: apoelstra at wpsoftware.net
> 
> Web: https://www.wpsoftware.net/andrew
> 
> The sun is always shining in space
> 
> -Justin Lewis-Webster
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Wed, 10 Jan 2024 14:28:29 +0000
From: Leslie <0300dbdd1b@protonmail.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Introducing a version field to BIP39 mnemonic
	phrases
Message-ID:
	<CdTY_9q1MdmLQ9iU7lIfS-14ibPGbuvlGFiXTdG5OzgaDolAsI2Pp3YXFmjU_o1XbijZmJA1mc4CCm1JMvsfLu5PDBdHYJuOcvgMMkxgpL0=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

<pre>
BIP:
Layer: Applications
Title: Versioned BIP39 Mnemonic Phrases
Author: Leslie <0300dbdd1b@protonmail.com>
Status: None
Type: Standards Track
Created: 2024-01-10
</pre>

## Abstract

This BIP proposes an enhancement to the BIP39 mnemonic phrases by introducing a version field.
The version field will be a 32-bit field, prepended to the entropy of the BIP39 mnemonic phrase.
The first 24 bits are for general purposes, and the subsequent 8 bits are for defining the version used.

## Motivation
The current implementation of BIP39 mnemonic phrases lacks a crucial feature: versioning.
This omission has been identified as a significant design flaw, affecting the robustness and future-proofness of the mnemonic phrase generation and usage.
Notable community members and projects have expressed concerns over this shortcoming:

>The lack of versioning is a serious design flaw in this proposal. On this basis alone I would recommend against use of this proposal.

\- [Greg Maxwell 2017-03-14](https://github.com/bitcoin/bips/wiki/Comments:BIP-0039/fd2ddb6d840c6a91c98a29146b9a62d6a65d03bf)

Furthermore, the absence of a version number in BIP39 seed phrases poses risks and inefficiencies in wallet software development and backward compatibility:

>BIP39 seed phrases do not include a version number. This means that software should always know how to generate keys and addresses. BIP43 suggests that wallet software will try various existing derivation schemes within the BIP32 framework. This is extremely inefficient and rests on the assumption that future wallets will support all previously accepted derivation methods. If, in the future, a wallet developer decides not to implement a particular derivation method because it is deprecated, then the software will not be able to detect that the corresponding seed phrases are not supported, and it will return an empty wallet instead. This threatens users funds.
>
>For these reasons, Electrum does not generate BIP39 seeds.

\- [Electrum Documentation 2017-01-27](https://electrum.readthedocs.io/en/latest/seedphrase.html#motivation)

The proposed BIP aims to address these concerns by introducing a version field in the BIP39 mnemonic phrases.
The introduction of versioning is expected to enhance the mnemonic's adaptability to future changes, improve the efficiency of wallet software in handling different derivation methods, and secure users funds by reducing the risk of incompatibilities between mnemonic phrases and wallet implementations.

## Generating the Mnemonic

In this proposal, we build upon the structure of BIP39 to include a versioned enhancement in the mnemonic generation process. The mnemonic encodes entropy, as in BIP39, but with a flexible approach to the size of the initial entropy (ENT).

### Version Field Inclusion:

1. **Initial Entropy Generation:**
The initial entropy of ENT bits is generated, where ENT can be any size as long as it is a multiple of 32 bits.

2. **Version Field Prepending:**
A crucial addition to this process is the prepending of a 32-bit version field to the initial entropy. This field is composed of:
- The first 24 bits are reserved for general purposes, which can be utilized for various enhancements or specific wallet functionalities.
- The remaining 8 bits are designated for specifying the version of the BIP39 standard.

3. **Checksum Calculation:**
A checksum is generated following the BIP39 method: taking the first (ENT + VF ) / 32 bits of the SHA256 hash of the combined entropy (initial entropy plus the 32-bit version field). This checksum is then appended to the combined entropy.

4. **Concatenation and Splitting:**
The combined entropy, including the initial entropy, version field, and checksum, is split into groups of 11 bits. Each group of bits corresponds to an index in the BIP39 wordlist.

5. **Mnemonic Sentence Formation:**
The mnemonic sentence is formed by converting these 11-bit groups into words using the standard BIP39 wordlist.

## Compatibility Considerations

- **Backward Compatibility:** Systems designed for BIP39, unaware of the 32-bit extension, will interpret the mnemonic as a 'Legacy' BIP39 phrase.
- **Forward Compatibility:** The versioning mechanism prepares systems for future modifications to the BIP39 standard, facilitating seamless integration.

## Dictionary Dependency

Wallets will still require access to the predefined BIP39 dictionary to retrieve the version of the mnemonic seed and validate the checksum.

> ? It's noteworthy that the BIP39 English wordlist includes specific words that software can use to identify the mnemonic's version number in a user-friendly manner, reducing dependence on the wordlist for version recognition.
>
> One way to achieve this is by assigning the first 22
> bits of the reserved field to match these words.
>
> 11110010110 11111111101 : version zero
> 11110010110 10011010101 : version one
> 11110010110 11101011101 : version two
> 11110010110 11100001000 : version three
> ...
> 11110010110 01101111001 : version hundred

## Changing Derivation Methods

The introduction of mnemonic versioning provides the flexibility to adopt alternative entropy derivation methods in the future. While BIP39 currently uses PBKDF2 for key stretching, future versions could employ different mechanisms to meet evolving cryptographic standards and requirements.

> ? Changing the derivation method in versioned mnemonics could lead to compatibility issues with older software.

## References
1. [Bitcoin Improvement Proposals. BIP39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)2. [bip39-versioned](https://github.com/lukechilds/bip39-versioned)
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240110/4ac23028/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 11
********************************************
