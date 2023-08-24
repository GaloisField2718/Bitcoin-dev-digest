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

   1. Stake Certificates and Web-of-Stakes: privacy-preserving
      proving UTXOs attributes in P2P systems (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Thu, 18 May 2023 07:08:46 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Stake Certificates and Web-of-Stakes:
	privacy-preserving proving UTXOs attributes in P2P systems
Message-ID:
	<CALZpt+FRPThy4qwYThXOY_YJWsGKJuCOqpX1Zt_8SqkeA4bQsg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi list,

One obvious usage of zero-knowledge proof cryptosystems in the Bitcoin
ecosystem (e.g Bulletproofs) is the construction of privacy-preserving
UTXO ownership proofs. UTXO ownership proofs are already used in
production across the Lightning ecosystem to authenticate the channels
announcements over the peer-to-peer gossip network. Additionally, UTXO
ownership proofs have been considered in the past for Lightning
jamming mitigations.

This type of mitigations dubbed "Stakes Certificates" while limited as
pure jamming mitigations are very interesting to solve counterparty
search in peer-to-peer marketplaces for decentralized Bitcoin
financial contracts (e.g coinjoins market-matching).

# Stakes Certificates

Stakes Certificates is a protocol (crypto-systems + validation
algorithms) enabling to prove a set of attributes about a UTXO in a
privacy-preserving fashion. Attributes are arbitrary strings about
UTXO characteristics such as the amount in satoshis and the
scriptPubkeys. From access to the UTXO set only, additional attributes
can be asserted such as the Script spending policy, if the
witnessScript (or equivalent for the scriptPubkey type) is revealed by
the prover, I think.

Advanced attributes could be asserted such as the UTXO age in height
or a timestamp in UNIX epoch if a merkle proof to show the inclusion
of the UTXO in the header chain constitutes the encrypted plaintext
beyond the UTXO itself. One more attribute can be the UTXO lineage of
some block-depth N if the chain of spent TXOs is part of the
plaintext, I believe. UTXO lineage can be a criteria of relevance for
coinjoins
marketplace.

The Stakes Certificates protocol flow works in the following way:
- the verifier and prover negotiate the system and security parameters
- the verifier announce constraints to reduce the set of attributes
from the combinations of information universes (e.g "UTXO of amount
superiors to 10000 sats")
- the prover build a statement and a witness corresponding to the set
of attributes selected under the constraints
- the verifier accepts or rejects the pair of statement and witness

Beyond the UTXO attributes, the scheme can respect additional security
properties such as uniqueness, e.g the UTXO should be unique in the
set of UTXOs from a session defined by the verifier. Another security
property can be "value upper bounding" for a series of concurrent
proofs verification. I think it would be logically analogous to a
confidential transaction session where the ledger supply is defined by
the verifier. This property can be useful for a coinjoin coordinator
to enforce some intersection characteristics of UTXO lineage.

Once the Stakes Certificates protocol flow session is over, the
verifier can store the validation result in its internal state. E.g if
it's a Lightning channel announcement, the proved channel can be
stored as a valid entry in the routing database for further
consumptions by the scoring algorithms.

# Web-of-Stakes

On top of the Stake Certificates protocol, a Web-of-Stakes protocol
can be laid out. A Web-of-Stakes protocol enables an entity to prove a
set of attributes for a set of UTXOs across Bitcoin contexts (e.g
combining UTXO attributes across swaps and lightning sessions). The
entity can be composed   from multiple sub-entities, such as a
Lightning Service Provider and its spokes clients.

A Web-of-Stakes protocol flow works in the following way:
- the prover announces a public key respecting some public
verifiability (public verifiability in the sense of a client-server
cryptographic protocol like Privacy Pass)
- the prover realizes a sequence of Stakes Certificates validation
with the verifier where the public key is committed as part of the
statement/witness
- the verifier accumulates the result of each Stakes Certificates
- if the accumulation satisfies verifier authorization policy, a
credential is yielded back to the prover

This Web-of-Stakes protocol can be leveraged to build counterparty and
trades search among peer-to-peer marketplaces where the prover can
selectively reveal attributes of its economic behavior based on the
UTXO footprint in the chain. E.g, a coinjoin maker can choose to
reveal the trace of its past coinjoin contributions as a way to build
"good market faith" for the takers.

This Web-of-Stakes protocol can be combined with modern techniques
from Web-of-Trust like decentralized identifiers where a chain of
signed PGP messages can be transposed in a unique entity "score" as
part of the verifier authorization policy evaluation. E.g, a cluster
of Nostr clients with an interest in collaborative transaction
construction can bless a set of Lightning Service Providers
specialized in splicing.

This Web-of-Stakes protocol can be combined with a client-server
framework for the providence of privacy-preserving credentials e.g
Staking Credentials. E.g a "signature-of-stakes" is generated and
based on the economic weight the credential fee required to publish on
a Nostr relay is adjusted.

# Zero-Knowledge Proofs Protocols

A zero-knowledge proof of knowledge is a protocol in which a prover
can convince a verifier that some statement holds without revealing
any information about why it holds. For Stakes Certificates, the level
of expressivity expected is to be superior to set membership, where a
wide-range of computational statements about the UTXO attributes can
be made.

Zero-knowledge proof systems have been designed under diverse
cryptographic assumptions: collision-resistant hash, elliptic curve
DLP and knowledge of exponent. Each one comes with a set of trade-offs
in terms of size proofs, generation time and verification time. While
the Stakes Certificates can be deployed on hosts and configuration
with different requirements (e.g mobile with low bandwidth), if we
have multiple practical ZKP systems for the Bitcoin use-cases, the
cryptosystems could be negotiated by the clients to suit their
computational resources.

# Applications

Beyond the Web-of-Stakes as a generic application aiming to solve
counterparty search in peer-to-peer marketplace, the Stakes
Certificate protocol can be used for another set of applications.

## Proof-of-liabilites for Ecash Mint

There has been a renewed interest for Chaumian mint across the Bitcoin
ecosystem during the last years. One of the hard issues is ensuring
the supply of ecash tokens does not grow more than the stack of
satoshis represented by the UTXOs. Stakes Certificates could be used
to ensure there has always been a 1-to-1 mapping between the ecash
tokens and the UTXOs ownership.

## Privacy-Preserving Lightning Channel Announcement

The Stakes Certificates could be used to replace the plaintext
Lightning gossip where the Lightning routing hops are announcing all
their connections. With P2TR, the gossip announcement receiver can be
interested to verify some tapscript policy, and as such there is no
third-party able to force-close the channel.

## Scarce Computational Resources in P2P Systems

The UTXOs can be used as DoS mitigations in peer-to-peer systems where
requiring the payment of a fee prevents bootstrapping of its state by
a new participant or there can be exploitable asymmetries, e.g a
Bitcoin node sending spam transactions, where "fresh" UTXOs are
requested in replacement of `min_relay_tx_fee`.

Cheers,
Antoine
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230518/6d3dc98b/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 48
*******************************************
