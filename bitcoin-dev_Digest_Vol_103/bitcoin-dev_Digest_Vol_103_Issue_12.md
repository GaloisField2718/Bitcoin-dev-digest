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

   1. Re: Addressing the possibility of profitable fee manipulation
      attacks (Nagaev Boris)
   2. BIP: output descriptors for PSBT (SeedHammer Team)


----------------------------------------------------------------------

Message: 1
Date: Sun, 17 Dec 2023 21:30:19 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: ArmchairCryptologist <ArmchairCryptologist@protonmail.com>,
	Bitcoin Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Addressing the possibility of profitable
	fee manipulation attacks
Message-ID:
	<CAFC_Vt7jYUUYi4yZqtBZ-wTyjgSH9ddPA+J0xUz6-C__cSa0kA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Sun, Dec 17, 2023 at 1:47?PM ArmchairCryptologist via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> Critically, this means that the higher the ratio of the hashrate is participating, the lower the cost of the attack. If 100% of miners participate with a ratio of transactions equal to their hashrate, the cost of the attack is zero, since every participating miner will get back on average 100% of the fees they contributed, and 0% of the fees will be lost to honest miners (of which there are none).

It would not be an equilibrium, because each of them can increase his
profit by not participating. He can still collect fees from
fee-stuffing transactions of others and high fees from transactions of
normal users.

> Observe also that miners would not have to actively coordinate or share funds in any way to participate. If a miner with 10% of the participating hashrate contributes 10% of the fee-stuffing transactions, they would also get back on average 10% of the total fees paid by transactions that are included in blocks mined by participating miners, giving them 10% of the profits. As such, each participating miner would simply have to watch the mempool to verify that the other participating miners are still broadcasting their agreed rate/ratio of transactions, the rest should average out over time.

He can pretend to have less hashrate and mine some blocks under the
table. For example, a miner who has 10% real hash rate could say to
other colluding miners that he only has 5%. Another 5% are secretly
allocated to a new pool. So his share of costs of fee-stuffing
transactions decreases, while he actually collects the same amount of
fees using both public and secret parts of his hash rate. Eventually
every rational participant of this collusion will do this and the
ratio of participating miners will decrease.

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 2
Date: Mon, 18 Dec 2023 00:52:44 +0000
From: SeedHammer Team <team@seedhammer.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: "me@achow101.com" <me@achow101.com>
Subject: [bitcoin-dev] BIP: output descriptors for PSBT
Message-ID:
	<HaI6GNtG_c6uCqCEB3YTs8_OWeq-6g0k5mQLz3g3bTHu-sHtbVLBnV_rI9yjZ-N0oc7ir_5M_8Ykb1HgG4EUeyyVlgXulXMdW2Ok10YFFtI=@seedhammer.com>
	
Content-Type: text/plain; charset="utf-8"

Hi,

This is a draft of a BIP that adds a PSBT_GLOBAL_OUTPUT_DESCRIPTOR field
for transferring output descriptors between wallets. The full text is reproduced below,
which is also hosted on GitHub:

https://github.com/seedhammer/bips/blob/master/bip-psbt-descriptors.mediawiki

An implementation is here: https://github.com/seedhammer/bip-psbt-descriptors

Live playground: https://go.dev/play/p/JrpWF0A9dxD

<pre>
BIP: ?
Layer: Applications
Title: PSBT Encoded Output Descriptors
Author: SeedHammer <team@seedhammer.com>
License: BSD-2-Clause
</pre>

==Introduction==

===Abstract===

A BIP 174 PSBT may contain an extended key for deriving input and output
addresses. This document proposes an additional field for PSBTs to represent
arbitrary BIP 380 output script descriptors.

To support transfer of output descriptors outside signing flows, the proposal
makes the unsigned transaction optional.

===Copyright===

This BIP is licensed under the BSD 2-clause license.

===Motivation===

A BIP 380 output descriptor is a textual representation of a set of output
scripts, such that Bitcoin wallets may agree on the scripts and addresses
to provide the user. However, a descriptor string by itself is not ideal for
transferring between wallets: it lacks a machine recognizable header and cannot
represent metadata such as name and birth block.

The PSBT encoding gives us a self-describing file format, metadata as well as a
compact, binary representation of keys. Assuming most wallets already implements
the PSBT format, the additional implementation overhead of this extension is
expected to be low.

==Specification==

The new global type is defined as follows:

{|
! Name
! <tt><keytype></tt>
! <tt><keydata></tt>
! <tt><keydata></tt> Description
! <tt><valuedata></tt>
! <tt><valuedata></tt> Description
|-
| Output Descriptor
| <tt>PSBT_GLOBAL_OUTPUT_DESCRIPTOR = 0x07</tt>
| <tt><compact size uint birth block><bytes></tt>
| The earliest block height that may contain transactions for the descriptor, optionally followed by the UTF-8 encoded name of the descriptor.
| <tt><bytes descriptor></tt>
| The output descriptor in BIP380 format without inline keys.
|-
|}

When PSBT_GLOBAL_OUTPUT_DESCRIPTOR is present, multiple PSBT_GLOBAL_XPUB entries are
allowed.

When PSBT_GLOBAL_OUTPUT_DESCRIPTOR is present, the presence of PSBT_GLOBAL_UNSIGNED_TX
is optional. Note that this is a relaxation of the PSBT specification.

All key expressions in the PSBT_GLOBAL_OUTPUT_DESCRIPTOR descriptor string must be
specified as references on the form <tt>@<index></tt> where <tt>index</tt> is
the 0-based index into the ordered list of PSBT_GLOBAL_XPUB entries. An index
out of range is invalid.

A PSBT_GLOBAL_OUTPUT_DESCRIPTOR with inline keys is invalid<ref>'''Why not allow inline
keys?'''
Allowing inline keys risks incompatible implementations that omit parsing of referenced
keys.</ref><ref>'''What about named <tt>pk(NAME)</tt> references?'''
Named references would allow Miniscript descriptors as-is in PSBT_GLOBAL_OUTPUT_DESCRIPTOR.
They are left out because they complicate decoders and can trivially be replaced by indexed
references. However, if key names are deemed desirable for display purposes, they could be
squeezed into <tt><keydata></tt> of PSBT_GLOBAL_XPUB entries.</ref>.

Key references may be followed by derivation paths as specified in BIP 389.

==Test Vectors==

===Invalid Cases===

A descriptor with a key reference out of bounds.
Descriptor: wpkh(@0/*)
Hex encoded PSBT: 70736274ff0207000a77706b682840302f2a29000000

A descriptor with an invalid UTF-8 name.
Hex encoded PSBT: 70736274ff05070061c57a0a77706b682840302f2a2953010488b21e041c0ae906800000025afed56d755c088320ec9bc6acd84d33737b580083759e0a0ff8f26e429e0b77028342f5f7773f6fab374e1c2d3ccdba26bc0933fc4f63828b662b4357e4cc3791bec0fbd814c5d8729748000080000000800000008002000080000000

A descriptor with an inline key.
Hex encoded PSBT: 70736274ff0207008e77706b68285b64633536373237362f3438682f30682f30682f32685d7870756236446959726652774e6e6a655834764873574d616a4a56464b726245456e753867415739764475517a675457457345484531367347576558585556314c42575145317943546d657072534e63715a3357373468715664674462745948557633654d3457325445556870616e2f2a29000000

===Valid Cases===

A 2-of-3 multisig descriptor
Descriptor: wsh(sortedmulti(2,@0/<0;1>/*,@1/<0;1>/*,@2/<0;1>/*))
Name: Satoshi's Stash
Birth block: 123456789012345
Key 0: [dc567276/48h/0h/0h/2h]xpub6DiYrfRwNnjeX4vHsWMajJVFKrbEEnu8gAW9vDuQzgTWEsEHE16sGWeXXUV1LBWQE1yCTmeprSNcqZ3W74hqVdgDbtYHUv3eM4W2TEUhpan
Key 1: [f245ae38/48h/0h/0h/2h]xpub6DnT4E1fT8VxuAZW29avMjr5i99aYTHBp9d7fiLnpL5t4JEprQqPMbTw7k7rh5tZZ2F5g8PJpssqrZoebzBChaiJrmEvWwUTEMAbHsY39Ge
Key 2: [c5d87297/48h/0h/0h/2h]xpub6DjrnfAyuonMaboEb3ZQZzhQ2ZEgaKV2r64BFmqymZqJqviLTe1JzMr2X2RfQF892RH7MyYUbcy77R7pPu1P71xoj8cDUMNhAMGYzKR4noZ
Hex encoded PSBT: 70736274ff1907ff79df0d86487000005361746f73686927732053746173683477736828736f727465646d756c746928322c40302f3c303b313e2f2a2c40312f3c303b313e2f2a2c40322f3c303b313e2f2a292953010488b21e0418f8c2e7800000026b3a4cfb6a45f6305efe6e0e976b5d26ba27f7c344d7fc7abef7be2d06d52dfd021c0b479ecf6e67713ddf0c43b634592f51c037b6f951fb1dc6361a98b1e5735e0f8b515314dc5672764800008000000080000000800200008053010488b21e04221eb5a080000002c887c72d9d8ac29cddd5b2b060e8b0239039a149c784abe6079e24445db4aa8a0397fcf2274abd243d42d42d3c248608c6d1935efca46138afef43af08e971289657009d2b14f245ae384800008000000080000000800200008053010488b21e041c0ae906800000025afed56d755c088320ec9bc6acd84d33737b580083759e0a0ff8f26e429e0b77028342f5f7773f6fab374e1c2d3ccdba26bc0933fc4f63828b662b4357e4cc3791bec0fbd814c5d8729748000080000000800000008002000080000000

==Rationale==

<references/>

==Compatibility==

PSBTs without a PSBT_GLOBAL_UNSIGNED_TX will be rejected by software expecting
it. However, such PSBTs are not intended to be used in a signing flow and so do
not pose a compatibility risk.

PSBTs with multiple PSBT_GLOBAL_XPUBs may be rejected by software that expects a
single extended key whose derived addresses match (some of) the input and output
addresses.

== Reference Implementation==

There is a [https://github.com/seedhammer/bip-psbt-descriptors Go implementation]
for development and testing purposes. Don't use it in production, because it only
validates the PSBT format, not the descriptor itself.

==Acknowledgments==

This specification builds upon and supercedes the bip-wallet-policies draft BIP
by specifying a serialization format for compact descriptors. It also uses the
indexed key references from that BIP, as well as examples and test vectors.

Thank you,
E
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231218/9d03d3a7/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 12
********************************************
