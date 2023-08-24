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

   1. Re: Ark: An Alternative Privacy-preserving Second Layer
      Solution (Burak Keceli)


----------------------------------------------------------------------

Message: 1
Date: Fri, 26 May 2023 14:56:00 +0300 (TRT)
From: Burak Keceli <burak@buraks.blog>
To: "David A. Harding" <dave@dtrt.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second Layer Solution
Message-ID:
	<558171558.1686821.1685102160441@eu1.myprofessionalmail.com>
Content-Type: text/plain; charset=UTF-8

Hi David, 

Ark can be used for three purposes:

1. Mixing coins.
Ark is a scalable, footprint-minimal off-chain mixer. People can use Ark to mix their coins with others. This doesn?t require waiting for on-chain confirmations since you?re mixing your own coins with others.

2. Paying lightning invoices
Ark is interoperable with Lightning, and you can use your Ark funds to pay Lightning invoices in a conjoin. This also doesn?t require waiting for on-chain confirmations since you consider your payment ?done? when you obtain the vendor's preimage.

3. Making internal transfers
You can use your Ark funds to make internal money transfers without introducing inbound liquidity assumptions. The recipient-end has to wait for several on-chain confirmations to consider their payment ?final?, however, their payment has immediate availability to them. Recipients can spend their zero-conf funds to pay Lightning invoices in coordination with their service provider. If we want to enable Lightning-style instant settlement assurances for the internal transfers, we need OP_XOR or OP_CAT on the base layer [1].


I think you get the gist of it, but I lost you after ?Bob wants to deposit 1 BTC with Alice.? sorry.

The initial onboarding phase is non-interactive, and there is no PSBT involved. Onboarding (or lifting) is as simple as funding a Bitcoin address. 

Here I have refactored it for you:
Bob wants to deposit 1 BTC with Alice. Bob asks his friend Charlie to send 1 BTC to an on-chain Bitcoin address whose script is:
pk(B) && (older(4 weeks) || pk(A))

 From here, there are several things that Bob can do:
- *Unilaterally withdraw:*
If Alice happens to be non-collaborative or non-responsive, Bob can simply take his 1 BTC back after four weeks. 

- *Collaboratively withdraw:*
Bob and Alice can sign from the 2-of-2 to collaboratively withdraw 1 BTC anytime.

- *Collaboratively trade commitments:*
Alice crafts a transaction containing three outputs; (a) a commitment output, (b) a connector output, and (c) a change output. We call this transaction ?pool?.
(a) commitment output
Commitment output (either using CTV or n-of-n multisig) constrains its descendant transaction to a set of transaction outputs. To simplify things, let?s say there are no other participants in this transaction besides Bob, and the descendant transaction has only one output. We call this output Bob?s vTXO. Bob?s vTXO also constrains (using CTV or 2-of-2 multisig) its descendant transaction to a single transaction output called Bob?s ATLC. Bob?s ATLC contains the following script:
pk(B) && (older(4 weeks) || pk(A))
As you realize ?ATLC? script is identical to the ?Funding address? script. 

(b) connectors output
Connectors output is simply a single-sig output spendable by Alice herself:
pk(A)

Alice locally crafts a descending transaction from this output, spending ?connectors output? to fund a new output. We call this output a ?connector,? which always carries a dust value  and is spendable by Alice herself:
pk(A)

In short, Alice crafts a Bitcoin transaction that spends an input that she controls and funds an output that she controls. Alice does not broadcast this transaction and keeps it secret.

(c) change output
money not used for the other two outputs gets sent back to Alice.

1. Alice places one (or more) input(s) to her ?pool? transaction to supply funds to commitment output, connectors output, change output, and transaction fees.

2. Bob creates an unsigned PSBT, placing the input that Charlie was previously funded.

3. Bob passes his PSBT to Alice. 

4. Alice places one input to PSBT, the ?connector output,?  which is a descendant of the (b) connectors output she is crafting.

5. Alice places one output to PSBT, a single-sig output that sweeps all money to herself (pk(A)).

6. Alice passes PSBT to Bob. Alice and Bob sign the PSBT and keeps this transaction private. This transaction is not valid yet, since the connector?s outpoint context does not exist.

7. Alice signs her one-in, three-out and broadcasts it. 

8. Alice can now claim 1 BTC Charlie has previously funded by revealing the descendant transaction of (b) connectors output. She should claim this before four weeks.
 
9. Bob now has a 1 BTC worth UTXO representation as a descendant of the (a) commitment output (a virtual UTXO). He can unilaterally claim this 1 BTC by revealing the child (Bob?s vTXO) and grandchild (Bob?s ATLC) of the (a) commitments output, then waiting a 24-hour window period.

So far, Charlie polluted on-chain by funding an address, and Alice by claiming funds from that address. Further steps from here will be footprint minimal. 

1. Say, Bob wants to send 1 BTC to Dave. 

2. Alice crafts a transaction containing three outputs; (a) a commitment output, (b) a connector output, and (c) a change output. This time descendant of (a) commitment output is Daves?s vTXO instead of Bob?s. Similarly descendant of Daves?s vTXO is Dave?s ATLC. Dave?s ATLC is:
pk(D) && (older(4 weeks) || pk(A))

3. Alice places one connector output as a descendant of (b) connectors output, just like before. 

4. Alice places one input to her one-in, three-out transaction to supply funds to commitment output, connectors output, change output, and transaction fees.

5. Bob creates an unsigned PSBT, placing his 1-BTC-worth virtual UTXO from the (a) commitment output descendants that Alice previously 

6. Bob passes his PSBT to Alice. 

7. Alice places one input to PSBT, the ?connector output,?  which is a descendant of the (b) connectors output she is crafting. 

8. Alice places one output to PSBT, a single-sig output that sweeps all money to herself (pk(A)).

9. Alice passes PSBT to Bob. Alice and Bob sign the PSBT and keeps this transaction private. 

10. Alice signs her one-in, three-out transaction and broadcasts it. 

11. Bob lets Dave know about this transaction (Alice?s transaction id, Dave?s vTXO output index) out-of-band. 

12. When Dave comes back online, he sees from the out-of-band message that Bob sent him 1-BTC. He then verifies whether Alice?s transaction id exists, whether his vTXO output index is correct, and a set of other validations.

13. If Dave had been online all this time, he would have had to wait for enough confirmations to consider his payment ?final.?

[1] https://eprint.iacr.org/2017/394.pdf


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 61
*******************************************
