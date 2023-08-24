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

   1. Ark: An Alternative Privacy-preserving Second Layer	Solution
      (Burak Keceli)


----------------------------------------------------------------------

Message: 1
Date: Mon, 22 May 2023 10:54:03 +0300 (TRT)
From: Burak Keceli <burak@buraks.blog>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Ark: An Alternative Privacy-preserving Second
	Layer	Solution
Message-ID:
	<1300890009.1516890.1684742043892@eu1.myprofessionalmail.com>
Content-Type: text/plain; charset="utf-8"

Hi list,
I'm excited to publicly publish a new second-layer protocol design I've been working on over the past few months called Ark.
 
Ark is an alternative second-layer scaling approach that allows the protocol users to send and receive funds without introducing liquidity constraints. This means a recipient can get paid without an onboarding setup, such as acquiring inbound liquidity. The protocol also consumes orders of magnitude less on-chain footprint than Lightning, as there is no concept of opening and closing channels.
 
Ark has a UTXO set that lives off the chain. These UTXOs are referred to as virtual UTXOs or vTXOs in short. Virtual UTXOs are like short-lived notes that expire after four weeks. Users must spend their vTXOs upon receiving them within this four-week timeframe or return them to themselves to reset the four-week timer. Virtual UTXOs live under a shared UTXO and can be revealed on-chain.
 
When a payment is made on the protocol, existing vTXOs are redeemed, and new vTXOs are created, similar to how on-chain funds flow. To improve the anonymity set of the coin ownership, vTXOs values are restricted to a set of sats values ranging from one sat to a million sats.
 
Users can acquire vTXOs from someone who already owns them or use a process called lifting, an atomic two-way peg mechanism that doesn't require trust. Lifting lets users lift their on-chain UTXOs off the chain for a 1:1 virtual UTXO. Users can unilaterally redeem a virtual UTXO for an on-chain UTXO without asking for cooperation. 
 
When sending funds, users coin-select & destroy their virtual UTXOs and create new ones for the recipient (plus change) in an off-chain mixing round. Keys for each new virtual UTXO are tweaked with a shared secret that reveals proof of payment when spent. The payment destination is a dedicated well-known public key similar to silent payments; however, the payment trace is obfuscated through plain tweaking and blinded mixing.
 
Ark enables anonymous, off-chain payments through an untrusted intermediary called the Ark Service Provider (ASP). ASPs are always-on servers that provide liquidity to the network and charge liquidity fees, similar to how Lightning service providers work. ASPs on Ark are both (1) liquidity providers, (2) blinded coinjoin coordinators, and (3) Lightning service providers. ASPs main job is to create rapid, blinded coinjoin sessions every five seconds, also known as pools. A user joins a pool session to make a payment, initially coin-selecting and registering their vTXOs to spend, registering vTXOs for intended recipients, and finally co-signing from their vTXOs to redeem them.
 
Ark can be built on Bitcoin today, but we have to compromise on non-interactivity to do so. Recipients must be online to sign from n-of-n multisig to constrain the outputs of a shared UTXO, outputs as in vTXOs. With this approach, users won?t be able to receive offline payments; they need to self-host an Ark client (like Lightning). To make Ark work without running a server, we need a covenant primitive such as BIP-118 or BIP-119. 
 
BIP-118 ANYPREVOUTANYSCRIPT can constrain outputs of a spending transaction by hardcoding a 65-byte signature and a 33-byte unknown public key type in a script. Alternatively, BIP-119 CTV can directly constrain transaction outputs to a template hash. Other alternatives would be (1) TXHASH, (2) CAT + CSFS + TAGGEDHASH, or (3) XOR + CSFS + TAGGEDHASH combinations. 
 
Ark uses a new locktype primitive called txlock to ensure the absolute atomicity of a transfer schedule. Txlock is a condition in which only the existence of a mutually agreed transaction identifier can unlock the condition. A txlock condition could be satisfied by a hypothetical opcode called OP_CHECKPREVTXIDFROMTHEUTXOSETVERIFY. However, Ark uses an alternative approach to achieving the same outcome using connectors. Connectors are a special output type on the protocol. The primitive is that if we want the Bitcoin script to check if a particular transaction id exists, we simply attach an output from that transaction into our spending transaction and check a pre-signed signature against prevouts of our spending transaction. The connector outpoint in the sighash preimage commits to the transaction id for which we want to satisfy the txlock condition. In the Ark context, this is the pool transaction containing vTXOs of intended recipients. Txlocks are used in Anchor Time Locked Contra
 cts (ATLCs) to provide an atomic single-hub payment schedule.
 
Anchor Time Locked Contracts (ATLCs) are conditional payments used on the Ark protocol. When a vTXO was created in the first place, an ATLC was attached to it, similar to how an eltoo:trigger is attached to a funding output during Eltoo channel formation. When a vTXO is spent, the pre-attached ATLC connects to a connector to form a txlock. 
 
This txlock formation ensures that, for the attached ATLC to be claimed by the service provider, the outpoint context of its connector must remain unchanged. In other words, Ark service providers should not double-spend pool transactions they create. This provides an atomic payout construction for senders, as payout vTXOs nest under the same transaction of connectors. The link between connectors and newly created vTXOs is obfuscated through blinded mixing between those.
 
?Pool transactions are created by Ark service providers perpetually every five seconds, which are effectively blinded, footprint-minimal, rapid coinjoin rounds. ASP funds the pool with their own on-chain funds in exchange for vTXOs redemptions. Therefore, the pool transaction that hits on-chain has only one or a few inputs the ASP provides. The pool transaction has three outputs: vTXOs output, connectors output, and ASP change. Service providers place vTXOs for the intended recipients to claim (under the vTXOs output) and connectors for senders to connect (under the connectors output) in their pool transactions.
 
The first output of the pool transaction, vTXOs output, contains newly created vTXOs of the coinjoin round. vTXOs are bundled and nested under this shared output and can be revealed on-chain. vTXOs output expires four weeks after its creation, and once it expires, the ASP who funded this output in the first place can solely sweep it. Nested vTXOs under the vTXOs output are expected to be redeemed by their owners in this window period. Nested vTXOs may be revealed in this four-week timeframe if the factory operator happens to be non-collaborative or non-responsive for a long period. Upon revealing a vTXO, a unilateral exit window can be triggered by attaching the pre-signed ATLC, similar to Eltoo. In the optimistic big picture, however, the final result is almost always a pool transaction with few inputs and three outputs where pool content is rarely revealed on-chain. Therefore, vTXOs & connectors remain almost always off the chain.

Ark can interoperate with Lightning by attaching HTLCs and PTLCs to a pool transaction, just like ATLCs and connectors. The attached HTLCs live under another shared UTXO called the HTLCs outputs, which also expire after four weeks. Ark service providers forward HTLCs to the broader Lightning Network the moment after they them to their pool transaction. This means Ark service providers are also Lightning service providers. Ark users can also get paid from Lightning using HTLC-nested vTXOs.
 
Ark is an open network where anyone can run their own ASP infrastructure. This means a user can have a vTXO set associated with different ASPs. The Ark protocol design allows users to pay lightning invoices from different vTXO sources using multi-part payments (MPP). Upon attaching HTLCs (or PTLCs) to multiple pools operated by various ASPs, HTLCs can be forwarded to the end destination via MPP.
 
A pool transaction can be double-spent by the Ark service provider while it remains in the mempool. However, in the meantime, the recipient can pay a lightning invoice with their incoming zero-conf vTXOs, so it?s a footgun for the service operator to double-spend in this case. 
 
A transfer schedule from a sender to a receiver is atomic in nature. ASPs cannot redeem senders' vTXOs if they double-spend recipients' vTXOs under the mutually agreed pool transaction id. A future extension of Ark can utilize a hypothetical data manipulation opcode (OP_XOR or OP_CAT) to constrain the ASP's nonce in their signatures to disincentivize double-spending. Users can forge ASP's signature to claim their previously redeemed vTXOs if a double-spend occurs in a pool transaction. This is effectively an inbound liquidity-like tradeoff without compromising on the protocol design.
 
On Ark, payments are credited every five seconds but settled every ten minutes. Payments are credited immediately because users don?t have to wait for on-chain confirmations to spend their zero-conf vTXOs further. They can hand over zero-conf vTXOs to others or pay lightning invoices with them. This is because the ASP who can double-spend users' incoming vTXOs is the same ASP who routes Lightning payments. 
 
You can find more info at https://arkpill.me/deep-dive https://www.arkpill.me/deep-dive.
 
- Burak
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230522/2609b1b5/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 52
*******************************************
