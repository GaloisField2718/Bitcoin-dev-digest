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

   1. Re: Pull-req to remove the arbitrary limits on OP_Return
      outputs (Murch)
   2. Re: Blinded 2-party Musig2 (Tom Trevethan)
   3. BIP for Serverless Payjoin (Dan Gould)


----------------------------------------------------------------------

Message: 1
Date: Wed, 9 Aug 2023 15:06:49 +0200
From: Murch <murch@murch.one>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Pull-req to remove the arbitrary limits on
	OP_Return outputs
Message-ID: <03551f0f-272e-2607-e95a-8ec671cbb9f3@murch.one>
Content-Type: text/plain; charset="us-ascii"

An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230809/ae71b50a/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 9 Aug 2023 16:14:36 +0100
From: Tom Trevethan <tom@commerceblock.com>
To: moonsettler <moonsettler@protonmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Blinded 2-party Musig2
Message-ID:
	<CAJvkSsexn06j843+54tyt6P_sypx_bRJN46e4kUYg+uHdcNJeQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

@moonsettler

When anyone receives a coin (either as payment or as part of a swap) they
need to perform a verification of all previous signatures and
corresponding backup txs. If anything is missing, then the verification
will fail. So anyone 'breaking the chain' by signing something
incorrectly simply cannot then send that coin on.

The second point is important. All the 'transfer data' (i.e. new and all
previous backup txs, signatures and values) is encrypted with the new owner
public key. But the server cannot know this pubkey as this would enable it
to compute the full coin pubkey and identify it on-chain. Currently, the
server identifies individual coins (shared keys) with a statechain_id
identifier (unrelated to the coin outpoint), which is used by the coin
receiver to retrieve the transfer data via the API. But this means the
receiver must be sent this identifier out-of-band by the sender, and also
that if anyone else learns it they can corrupt the server key
share/signature chain via the API. One solution to this is to have a second
non-identifying key used only for authenticating with the server. This
would mean a 'statchain address' would then be composed of 2 separate
pubkeys 1) for the shared taproot address and 2) for server authentication.

Thanks,

Tom

On Tue, Aug 8, 2023 at 6:44?PM moonsettler <moonsettler@protonmail.com>
wrote:

> Very nice! Is there an authentication mechanism to avoid 'breaking the
> chain' with an unverifiable new state by a previous owner? Can the current
> owner prove the knowledge of a non-identifying secret he learned as
> recipient to the server that is related to the statechain tip?
>
> BR,
> moonsettler
>
> ------- Original Message -------
> On Monday, August 7th, 2023 at 2:55 AM, Tom Trevethan via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> A follow up to this, I have updated the blinded statechain protocol
> description to include the mitigation to the Wagner attack by requiring the
> server to send R1 values only after commitments made to the server of the
> R2 values used by the user, and that all the previous computed c values are
> verified by each new statecoin owner.
> https://github.com/commerceblock/mercury/blob/master/layer/protocol.md
>
> Essentially, the attack is possible because the server cannot verify that
> the blinded challenge (c) value it has been sent by the user has been
> computed honestly (i.e. c = SHA256(X1 + X2, R1 + R2, m) ), however this CAN
> be verified by each new owner of a statecoin for all the previous
> signatures.
>
> Each time an owner cooperates with the server to generate a signature on a
> backup tx, the server will require that the owner send a commitment to
> their R2 value: e.g. SHA256(R2). The server will store this value before
> responding with it's R1 value. This way, the owner cannot choose the value
> of R2 (and hence c).
>
> When the statecoin is received by a new owner, they will receive ALL
> previous signed backup txs for that coin from the sender, and all the
> corresponding R2 values used for each signature. They will then ask the
> server (for each previous signature), the commitments SHA256(R2) and the
> corresponding server generated R1 value and c value used. The new owner
> will then verify that each backup tx is valid, and that each c value was
> computed c = SHA256(X1 + X2, R1 + R2, m) and each commitment equals
> SHA256(R2). This ensures that a previous owner could not have generated
> more valid signatures than the server has partially signed.
>
> On Thu, Jul 27, 2023 at 2:25?PM Tom Trevethan <tom@commerceblock.com>
> wrote:
>
>>
>> On Thu, Jul 27, 2023 at 9:08?AM Jonas Nick <jonasdnick@gmail.com> wrote:
>>
>>> No, proof of knowledge of the r values used to generate each R does not
>>> prevent
>>> Wagner's attack. I wrote
>>>
>>> > Using Wagner's algorithm, choose R2[0], ..., R2[K-1] such that
>>> > c[0] + ... + c[K-1] = c[K].
>>>
>>> You can think of this as actually choosing scalars r2[0], ..., r2[K-1]
>>> and
>>> define R2[i] = r2[i]*G. The attacker chooses r2[i]. The attack wouldn't
>>> make
>>> sense if he didn't.
>>>
>>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230809/94da0e46/attachment-0001.html>

------------------------------

Message: 3
Date: Wed, 09 Aug 2023 17:32:54 +0000
From: Dan Gould <d@ngould.dev>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] BIP for Serverless Payjoin
Message-ID: <7B11AE34-27A7-46ED-95BF-66CA13BA26F3@ngould.dev>
Content-Type: text/plain; charset=utf-8

Hi all,

The Serverless Payjoin idea has come a long way toward formal specification of a Payjoin version 2. In the spirit of BIP 2, I?m sharing an intermediate draft of the BIP here before opening a draft on GitHub for the BIP editors, and before this exact specification has a complete reference implementation. The draft does reference two proof of concept payjoin implementations, one demonstrating use of symmetric cryptography, and the other asynchronous messaging and backwards compatibility.

I?ve updated the Serverless Payjoin gist to reflect this draft specification https://gist.github.com/DanGould/243e418752fff760c9f6b23bba8a32f9 in order to preserve the edit history before opening a bips PR.

The specifics have changed significantly compared to the first mailing list post to reflect feedback. Looking forward to hear your thoughts.

Dan

<pre>
BIP: ???
Layer: Applications
Title: Payjoin Version 2: Serverless Payjoin
Author: Dan Gould <d@ngould.dev>
Status: Draft
Replaces: 78
Type: Standards Track
Created: 2023-08-08
License: BSD-2-Clause
</pre>

==Abstract==

This document proposes a backwards-compatible second version of the payjoin protocol described in [[bip-0078.mediawiki|BIP 78]], allowing complete payjoin receiver functionality including payment output substitution without requiring them to host a secure public endpoint. This requirement is replaced with an untrusted third-party relay and streaming clients which communicate using an asynchronous protocol and authenticated encrypted payloads.

==Copyright==

This BIP is licensed under the 2-clause BSD license.

==Motivation==

Payjoin solves the sole privacy problem left open in the bitcoin paper, that transactions with multiple inputs "necessarily reveal that their inputs were owned by the same owner." Breaking that common-input ownership assumption and others requires input from multiple owners. Cooperative transaction construction also increases transaction throughput by providing new opportunity for payment batching and transaction cut-through.

Version 1 coordinates payjoins over a public server endpoint secured by either TLS or Tor onion hidden service hosted by the receiver. Version 1 is synchronous, so both sender and reciever must be online simultaneously to payjoin. Both requirements present significant barriers for all but sophisticated server operators or those wallets with complex Tor integration. These barriers are [[https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-January/018358.html|regarded]] as limits to payjoin adoption.

The primary goal of this proposal is to provide a practical coordination mechanism to be adopted in a vast majority of wallet environments. This is realized as a simple protocol built on bitcoin URI requests, web standards, common crypto, and minimal dependencies.

===Relation to BIP 78 (Payjoin version 1)===

The message payloads in this version parrallel those used in BIP 78 while being encapsulated in authenticated encryption, forgoing HTTP messaging for WebTransport streaming of asynchronus interactions, and leveraging PSBT version 2.

The BIP 78 standard allows for an [[https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki#unsecured-payjoin-server|unsecured payjoin server|]] to operate separately from the so-called "payment server" responsible for generating [[https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki|BIP 21]] request URIs. Because BIP 78 messages are neither authenticated nor encrypted a malicious unsecured payjoin server is able to modify the Payjoin PSBT in flight, thus requiring [[payment output substitition]] to be disabled. Output substitition is useful for a number of block space optimizations, including payment batching and transaction cut-through. This proposal introduces authentication and encryption to secure output substition while using a relay without compromising sender or receiver privacy.

Although unsecured payjoin server separation is mentioned in BIP 78, no known specification or implementation of one exists. This document specifies one to be backwards compatible with version 1 senders. Receivers responding to version 1 senders must disable output substitution their payloads are plaintext so they may payjoin without the risk of the relay stealing funds.

The protocols in this document reuse BIP 78's BIP 21 URI parameters. A Fallback PSBT timeout parameter is introduced which may also help coordinate the synchronous version 1 protocol.

===Relation to Stowaway===

[[https://code.samourai.io/wallet/ExtLibJ/-/blob/develop/doc/cahoots/STOWAWAY.md|Stowaway]] is a payjoin coordination mechanism which depends on Tor, a third-party relay, and the [[https://samouraiwallet.com/paynym|PayNym]] [[https://github.com/bitcoin/bips/blob/master/bip-0047.mediawiki|BIP 47]] Payment codes directory for subdirectory identification and encryption. The payjoin version 2 protocol uses one-time symmetric keys for relay subdirectory identification, authentication, and encryption instead of BIP 47 public keys derived from the wallet. Payjoin version 2 also supports asynchronous messaging, in contrast to online Stowaway's synchronous HTTP-based messaging. Offline stowaway may depends on manual message passing rather than an asynchronous network protocol. Successful Stowaway execution results in 2-output transactions, while BIP 79, 78, and this work may produce batched transactions with many outputs.

==Specification==

===Overview===

Payjoin requests are made using familiar BIP 21 URIs. Instead of a public HTTP endpoint, this scheme allows a WebTransport client to enroll with a relay server to receive payjoin. Relays may optionally require an authorization credential before allocating resources in order to prevent DoS attacks. Sender and receiver payloads are buffered at the relay to support asynchronous interaction. Symmetric authenticated encryption (ChaCha20-Poly1305 AEAD) prevents the relay from snooping on message contents or forging messages. Aside from a pre-shared secret and relayed asynchronus networking, the version 2 messaging takes much the same form as the existing BIP 78 specification.

===Basic scheme===

The recipient first generates a 256-bit key <code>psk</code>. This pre-shared key will be the basis of end-to-end authenticated encryption and identification of a particular payjoin over the relay.

Rather than hosting a public server, they start a streaming session to receive messages and allocate a subdirectory from which to relay messages. The first message must include the first 4 bytes of the Sha256 hash of their <code>psk</code> to be enrolled as a subdirectory identifier. The next message streamed from the relay to sender includes the enrolled subdirectory payjoin endpoint. After enrollment, they await a payjoin request on a session identified by the subdirectory. Out of band, the receiver shares a [[https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki|BIP 21]] payjoin uri including the relay endpoint in the <code>pj=</code> query parameter and the pre-shared key in a new <code>psk=</code> query parameter.

The sender constructs an encrypted and authenticated payload containing a PSBT and optional parameters similar to BIP 78. The resulting ciphertext ensures message secrecy and integrity when streamed to the recipient by the relay-hosted subdirectory <code>pj=</code> endpoint.

The sender's request is relayed to the receiver over a streaming session at the subdirectory identified by the hash of <code>psk</code>. Messages are secured by symmetric cipher rather than TLS or Onion routing session key. Sender and receiver may experience network interruption and proceed with the protocol since their request and response are buffered at the Payjoin relay subdirectory.

===Payjoin version 2 messaging===

Payjoin v2 messages use [[https://github.com/bitcoin/bips/blob/master/bip-0370.mediawiki|BIP 370 PSBT v2]] format to fascilitate PSBT mutation.

The payjoin version 2 protocol takes the following steps:

* The recipient sends the first 4 bytes of <code>H(psk)</code> and optional authentication credential according to [[#receiver-relay-enrollment|receiver relay enrollment]] protocol. It may go offline and replay enrollment to come back online.
* Out of band, the receiver of the payment, shares a bitcoin URI with the sender including a <code>pj=</code> query parameter describing the relay subdirectory endpoint and <code>psk=</code> parameter with base64 encoded 256-bit secret key. To support version 1 senders the relay acts as an unsecured payjoin server so <code>pjos=0</code> must be specified in the URI. Version 2 senders may safely allow output substitution regardless.
* The sender creates a valid PSBT according to [[https://github.com/bitcoin/bips/blob/master/bip-0078#receivers-original-psbt-checklist|the receiver checklist]] formatted as PSBTv2. We call this the <code>Fallback PSBT</code>. This Fallback PSBT and optional sender parameters are encrypted and authenticated with the <code>psk</code> using ChaCha20Poly1305 and streamed to the relay subdirectory endpoint.
* The sender awaits a response from the relay stream containing an encrypted <code>Payjoin PSBT</code>. It can replay the <code>Fallback PSBT</code> to request a response if it goes offline.
* The request is stored in the receiver's subdirectory buffer.
* Once the receiver is online, it awaits a stream of request updates from the relay. The receiver decrypts aund authenticates the payload then checks it according to [[https://github.com/bitcoin/bips/blob/master/bip-0078#receivers-original-psbt-checklist|the receiver checklist]]. It updates it to include new signed inputs and outputs invalidating sender signatures, and may adjust the fee. We call this the <code>Payjoin PSBT</code>.
* It responds with the <code>Payjoin PSBT</code> encrypted then authenticated under <code>psk</code> using ChaCha20Poly1305.
* The relay awaits a connection from the sender if it goes offline. Upon connection, it relays the encrypted <code>Payjoin PSBT</code> to the sender.
* The sender validates the <code>Payjoin PSBT</code> according to [[#senders-payjoin-psbt-checklist|the sender checklist]], signs its inputs and broadcasts the transaction to the Bitcoin network.

The encrypted Fallback PSBT and Payjoin PSBT payloads are sent as bytes.

The Fallback PSBT MUST:

* Include complete UTXO data.
* Be signed.
* Exclude unnecessary fields such as global xpubs or keypath information. <!-- I believe PSBTv2 obviates this requirement -->
* Set input and output Transaction Modifiable Flags to 1
* Be broadcastable.

The Fallback PSBT MAY:

* Include outputs unrelated to the sender-receiver transfer for batching purposes.
* Set SIGHASH_SINGLE Transaction Modifiable Flags flags to 1

The Payjoin PSBT MUST:

* Include all inputs from the Fallback PSBT.
* Include all outputs which do not belong to the receiver from the Fallback PSBT.
* Include complete UTXO data.

The Payjoin PSBT sender MAY:

* Add, remove or modify Fallback PSBT outputs under the control of the receiver (i.e. not sender change).

The Payjoin PSBT MUST NOT:

* Shuffle the order of inputs or outputs; the additional outputs or additional inputs must be inserted at a random index.
* Decrease the absolute fee of the original transaction.

===Receiver's Payjoin PSBT checklist===

Other than requiring PSBTv2 the receiver checklist is the same as the [[https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki#receivers-original-psbt-checklist|the BIP 78 receiver checklist]]

===Sender's Payjoin PSBT checklist===

The version 2 sender's checklist is largely the same as the [[https://github.com/bitcoin/bips/blob/master/bip-0078#senders-payjoin-proposal-checklist|the BIP 78 checklist]] with the exception that it expects ALL utxo data to be filled in. BIP 78 required sender inputs UTXO data to be excluded from the PSBT which has caused many headaches since it required the sender to add them back to the Payjoin proposal PSBT. Version 2 has no such requirement.

===Relay interactions===

The Payjoin Relay provides a rendezvous point for sender and receiver to meet. It stores Payjoin payloads to support asynchronous communication. It is available on the open internet over HTTPS to accept both WebTransport for Payjoin version 2, accepting encrypted payloads, and optionally HTTP/1.1 to support backwards compatible Payjoin version 1 requests.

===Receiver interactions===

====Relay enrollment====

Receivers must enroll to have resources allocated on a relay. Sessions may begin by having a receiver send the first 4 bytes of the Sha256 hash of their <code>psk</code> to the relay. The receiver returns the subdirectory endpoint url. Enrollment may be replayed in case the receiver goes offline.

Optionally, before returning the uri the receiver may request an authentication token by presenting a message containing only the word <code>Authenticate: <description></code> after which the receiver is required to submit an <code>Authenticate: <token></code> including the token from the Relay out of band. If authentication fails an error is returned.

In the case a relay is operated by an exchange, it may give out authentication tokens for users of its app, or may require some proof of work out of band. Tokens should be anonymous credentials from the relay describing the parameters of their authorization. Specific credentialing is out of the scope of this proposal.

====Receiver Payjoin PSBT response====

The receiver streams the base64 Payjoin PSBT as encrypted bytes from ChaCha20Poly1305 under <code>psk</code>.

===Sender interactions===

The sender starts a WebTransport session with the relay at the Payjoin endpoint URI provided by the receiver. It sends the following payload and awaits a relayed response payload from the receiver.

====Version 2 Fallback PSBT request====

The version 2 Fallback PSBT Payload is constructed in JSON before being encrypted as follows.

<pre>
{
"psbt": "<fallback_psbt_data_base64>",
"params": {
"param1": "<value1>",
"param2": "<value1>",
...
}
}
</pre>

The payload must be encrypted using ChaCha20Poly1305 by the sender using the <code>psk</code>.

====Version 1 Fallback PSBT request====

The message should be the same as version 2 but unencrypted, as version 1 is unaware of encryption when using an unsecured payjoin server. The Relay should convert the PSBT to PSBTv2 and construct the JSON payload from the HTTP request body and optional query parameters. Upon receiving an unencrypted PSBTv2 response from a receiver, it should convert it to PSBTv0 for compatibility with BIP 78.

===Asynchronous relay buffers===

Each receiver subdirectory on the relay server has a buffer for requests and one for responses. Each buffer updates listeners through awaitable events so that updates are immediately apparent to relevant client sessions.

===BIP 21 receiver parameters===

A major benefit of BIP 78 payjoin over other coordination mechanisms is its compatibility with the universal BIP 21 bitcoin URI standard.

This proposal defines the following new [[https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki|BIP 21 URI]] parameters:

* <code>psk</code>: the pre-shared symmetric key for encryption and authentication with ChaCha20-Poly1305
* <code>exp</code>: represents a request expiration after which the receiver reserves the right to broadcast the Fallback and ignore requests.

BIP 78's BIP 21 payjoin parameters are also valid for version 2.

===Optional sender parameters===

When the payjoin sender posts the original PSBT to the receiver, it can optionally specify the following HTTP query string parameters:

* <code>v</code>: represents the version number of the payjoin protocol that the sender is using. This version is <code>2</code>.

BIP 78's optional query parameters are also valid as version 2 parameters.

==Rationale==

===Request expiration & fallback===

The relay may hold a request for an offline payjoin peer until that peer comes online. However, the BIP 78 spec recommends broadcasting request PSBTs in the case of an offline counterparty. Doing so exposes a na?ve, surveillance-vulnerable transaction which payjoin intends to avoid.

The existing BIP 78 protocol has to be synchronous only for automated endpoints which may be vulnerable to probing attacks. It can cover this tradeoff by demanding a fallback transaction that would not preserve privacy the same way as a payjoin. BIP 21 URI can communicate a request expiration to alleviate both of these problems. Receivers may specify a deadline after which they will broadcast this fallback with a new expiration parameter <code>exp=</code>. <!-- I also like to for timeout, but it's hard to coordinate in an asynchronous way -->

===WebTransport===

Many transport protocols are good candidates for Serverless Payjoin functionality, but WebTransport stands out in its ability to stream and take advantage of QUIC's performance in mobile environments. In developing this BIP, serverless payjoin proofs of concept using TURN, HTTP/1.1 long polling, WebSockets, Magic Wormhole, and Nostr have been made. Streaming allows the relay to have more granular and asynchronous understanding of the state of the peers, and this protcol is designed specifically to address the shortcomings of an HTTP protocol's requirement to receive from a reliable, always-online connection.

While WebTransport and HTTP/3 it is built on are relatively new, widespread support across browsers assures me that it is being accepted as a standard and even has a fallback to HTTP/2 environments. Being built on top of QUIC allows it to multiplex connections from a relay to multiple peers which may prove advantageous for later payjoin protocols between more than two participants contributing inputs, such as those used to fund a lightning node with channels from multiple sources in one transaction, or those with threat models more similar to ZeroLink CoinJoin.

While Nostr is fascinating from the perspective of censorship resistance, the backwards compatibility with Payjoin v1 would mean only custom Nostr Payjoin relays exposing an https endpoint would be suitable. Nostr transport is also limited by the performance of WebSockets, being an abstraction on top of that protocol. If Nostr authentication were used instead of a symmetric <code>psk</code> then those keys would also need to be communicated out of band and complicate the protocol. There is nothing stopping a new version of this protocol or a NIP making Payjoin version 2 possible over Nostr should Payjoin censorship become a bottleneck in the way of adoption.

WebTransport is already shipped in both Firefox, Chrome, h3 in Rust, Go, and all popular languages. There is also [[https://w3c.github.io/p2p-webtransport/|a working draft for full P2P WebTransport]] without any relay, which a future payjoin protocol may make use of.

===ChaCha20Poly1305 AEAD===

This authenticated encryption with additional data [[https://en.wikipedia.org/wiki/ChaCha20-Poly1305|algorithm]] is standardized in RFC 8439 and has high performance. ChaCha20Poly1305 AEAD seems to be making its way into bitcoin by way of [[https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki|BIP 324]] as well. The protocol has widespread support in browsers, OpenSSL and libsodium. AES-GCM is more widespread but is both older, slower, and not a dependency in bitcoin software.

secp256k1 asymmetric cryptography could be used, but symmetric encryption allows for many fewer messages to be sent, a single ephemeral key, and seems suitable given the one time use of BIP 21 URIs for Payjoin. Payjoin already requires base64 encoding for PSBTs, so we have it available to encode the 256-bit <code>psk</code> in the BIP 21 parameter.

===PSBT Version 2===

The PSBT version 1 protocol was replaced because it was not designed to have inputs and outputs be mutated. Payjoin mutates the PSBT, so BIP 78 uses a hack where a new PSBT is created by the receiver instead of mutating it. This can cause some strange behaviors from signers who don't know where to look to find the scripts that they are accountable for. PSBT version 2 makes mutating a PSBT's inputs and outputs trivial. It also eliminates the transaction finalization step. Receivers who do not understand PSBT version 1 may choose to reject Payjoin version 1 requests and only support PSBT version 2.

===Attack vectors===

Since relays store arbitrary encrypted payloads to the tragedy of the commons and denial of service attacks. Relay operators may impose an authentication requirement before they provide relay service to receivers to mitigate such attacks.

Since <code>psk</code> is a symmetric key, the first message containing the sender's original PSBT does not have forward secrecy. Since relay buffers are associated with a single ephemeral relay directory, to support request-response simplicity of version 1, this seems appropriate.

Since the Fallback PSBT is valid, even where <code>exp=</code> is specified, the receiver may broadcast it and lose out on ambiguous privacy protection from payjoin at any time. Though unfortunate, this is the typical bitcoin transaction flow today anyhow.

===Network privacy===

Unlike BIP 78 implementations, sender and receiver peers will only see the IP address of the relay, not their peer's. Relays may be made available via Tor hidden service or Oblivious HTTP in addition to IP / DNS to allow either of the peers to protect their IP from the relay with without requiring both peers to use additional network security dependencies.

==Backwards compatibility==

The receivers advertise payjoin capabilities through [[https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki|BIP21's URI Scheme]].

Senders not supporting payjoin will just ignore the <code>pj=</code> parameter and proceed to typical address-based transaction flows. <code>req-pj=</code> may be used to compel payjoin. 

Receivers may choose to support version 1 payloads. Version 2 payjoin URIs should enable <code>pjos=0</code> so that these v1 senders disable output substitution since the v1 messages are neither encrypted nor authenticated, putting them at risk for man-in-the-middle attacks otherwise. The relay protocol should carry on as normal, validating based on HTTP headers and constructing an unencrypted Version 2 payload from optional query parameters, and PSBT in the body.

The BIP 78 error messages are already JSON formatted, so it made sense to rely on the same dependency for these payloads and error messages.

==Reference implementation==

An early proof of concept draft reference implementation can be found at https://github.com/payjoin/rust-payjoin/pull/78. It implements an asynchronous payment flow using WebSockets using PSBTv1 without encryption. Another reference can be found at https://github.com/payjoin/rust-payjoin/pull/21 which uses HTTP long polling for transport and Noise NNpsk0 for crypto. Recently, I've come to realize the rationale for WebTransport, PSBTv2, and ChaCha20-Poly1305 AEAD substitutions and am working on an implementation including this exact specification, but wanted to get early feedback on this design in the spirit of BIP 2.

==Acknowledgements==

Thank you to OpenSats for funding this pursuit, to Human Rights Foundation for putting a bounty on it and funding invaluable BOB Space space support, who I owe a thank you to as well. Thank you to Ethan Heilman, Nicolas Dorier, Kukks, nopara73, Kristaps Kaupe, Kixunil, /dev/fd0/, Craig Raw, Mike Schmidt, Murch, D?vid Moln?r, Lucas Ontiviero, and uncountable twitter plebs for feedback that has turned this idea from concept into draft, to Mike Jarmuz for suggesting that I write a BIP, and to Satsie for writing the "All About BIPS" zine which I've referenced a number of times in the drafting process. Thanks to Armin Sabouri, Ron Stoner, and Johns Beharry for hacking on the first iOS Payjoin receiver and uncovering the problem that this solves in the first place.


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 21
*******************************************
