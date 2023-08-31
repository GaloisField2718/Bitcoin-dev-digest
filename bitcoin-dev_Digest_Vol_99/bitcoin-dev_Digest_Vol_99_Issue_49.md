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

   1. Re: Private Collaborative Custody with FROST (rot13maxi)
   2. Re: Sentinel Chains: A Novel Two-Way Peg (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Tue, 29 Aug 2023 11:51:49 +0000
From: rot13maxi <rot13maxi@protonmail.com>
To: Nick Farrow <nicholas.w.farrow@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Private Collaborative Custody with FROST
Message-ID:
	<NBWGXNsLa372udskPbAr7hS9ba_VcKY1Aq4C4QB8Mf0EFc2N8zDD8H6OwOO5_8n-ESgdsQyDQIK0QFVHhCUe0Uc2oFpZ-zv0P7PirCbS5T0=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Good morning Nick,

Love the direction of this.

> We can achieve this compatibility by having the server sign under a single nonce (not a binding nonce-pair like usual FROST), which is later blinded by the nonce contributions from other signers.

Can you say more about this? It sounds like the blinding is happening post-signing? Or is it happening during the normal nonce commitment trading?

Rijndael

On Mon, Aug 28, 2023 at 3:35 PM, Nick Farrow via bitcoin-dev <[bitcoin-dev@lists.linuxfoundation.org](mailto:On Mon, Aug 28, 2023 at 3:35 PM, Nick Farrow via bitcoin-dev <<a href=)> wrote:

> Hello all,
>
> Some thoughts on private collaborative custody services for Bitcoin.
>
> With multiparty computation multisignatures like FROST [0], it is possible to build a collaborative custodian service that is extremely private for users.
>
> Today's collaborative custodians can see your entire wallet history even if you never require them to help sign a transaction, and they have full liberty to censor any signature requests they deem inappropriate or are coerced into censoring.
>
> With FROST, a private collaborative custodian can hold a key to a multisig while remaining unaware of the public key (and wallet) which they help control. By hiding this public key, we solve the issue of existing collaborative custodians who learn of all wallet transactions even if you never use them.
>
> Further, in the scenario that we do call upon a private collaborative custodian to help sign a transaction, this transaction could be signed **blindly**. Being blind to the transaction request itself and unknowing of past onchain behavior, these custodians have no practical information to enact censorship requests or non-cooperation. A stark contrast to today's non-private collaborative custodians who could very easily be coerced into not collaborating with users.
>
> Enrolling a Private Collaborative Custodian
>
> Each signer in a FROST multisig controls a point belonging to a joint polynomial at some participant index.
>
> Participants in an existing multisig can collaborate in an enrollment protocol (Section 4.1.3 of [1], [2]) to securely generate a new point on this shared polynomial and verifiably communicate it to a new participant, in this case a collaborative custodian.
>
> The newly enrolled custodian should end by sharing their own *public* point so that all other parties can verify it does in-fact lie on the image of the joint polynomial at their index (i.e. belong to the FROST key). (The custodian themselves is unable to verify this, since we want to hide our public key we do not share the image of our joint polynomial with them).
>
> Blind Collaborative Signing
>
> Once the collaborative custodian controls a point belonging to this FROST key, we can now get their help to sign messages.
>
> We believe it to be possible for a signing server to follow a scheme similar to that of regular blind Schnorr signatures, while making the produced signature compatible with the partial signatures from other FROST participants.
>
> We can achieve this compatibility by having the server sign under a single nonce (not a binding nonce-pair like usual FROST), which is later blinded by the nonce contributions from other signers. The challenge also can be blinded with a factor that includes the necessary Lagrange coefficient so that this partial signature correctly combines with the other FROST signatures from the signing quorum.
>
> As an overview, we give a 3rd party a secret share belonging to our FROST key. When we need their help to sign something, we ask them to send us (FROST coordinator) a public nonce, then we create a challenge for them to sign with a blind Schnorr scheme. They sign this challenge, send it back, and we then combine it with the other partial signatures from FROST to form a complete Schnorr signature that is valid under the multisignature's public key.
>
> During this process the collaborative custodian has been unknowing of our public key, and unknowing as to the contents of the challenge which we have requested them to sign. The collaborative signer doesn't even need to know that they are participating in FROST whatsoever.
>
> Unknowing Signing Isn't So Scary
>
> A server that signs arbitrary challenges sounds scary, but each secret share is unique to a particular FROST key. The collaborative custodian should protect this service well with some policy, e.g. user authentication, perhaps involving cooperation from a number of other parties (< threshold) within the multisig. This could help prevent parties from abusing the service to "get another vote" towards the multisig threshold.
>
> Unknowingly collaborating in the signing of bitcoin transactions could be a legal gray area, but it also places you in a realm of extreme privacy that may alleviate you from regulatory and legal demands that are now impossible for you to enforce (like seen with Mullvad VPN [3]). Censorship requests made from past onchain behavior such as coinjoins becomes impossible, as does the enforcement of address or UTXO blocklists.
>
> By having the collaborative custodian sign under some form of blind Schnorr, the server is not contributing any nonce with binding value for the aggregate nonce. Naively this could open up some form of Drijvers attacks which may allow for forgeries (see FROST paper [0]), but I think we can eliminate given the right approach.
>
> Blind Schnorr schemes also introduce attack vectors with multiple concurrent signing requests [4], one idea to prevent this is to disallow simultaneous signing operations at the collaborative custodian. Even though Bitcoin transactions can require multiple signatures, these signatures could be made sequentially with a rejection of any signature request that uses anything other than the latest nonce.
>
> Risks may differ depending on whether the service is emergency-only or for whether it is frequently a participant in signing operations.
>
> -------
>
> Thanks to @LLFOURN for ongoing thoughts, awareness of enrollment protocols, and observation that this can all fall back into a standard Schnorr signature.
>
> Curious for any thoughts, flaws or expansions upon this idea,
>
> Gist of this post, which I may keep updated and add equations:
> https://gist.github.com/nickfarrow/4be776782bce0c12cca523cbc203fb9d/
>
> Nick
>
> -------
>
> References
>
> * [0] FROST: https://eprint.iacr.org/2020/852.pdf
> * [1] A Survey and Refinement of Repairable Threshold Schemes (Enrollment: Section 4.3): https://eprint.iacr.org/2017/1155.pdf
> * [2] Modifying FROST Threshold and Signers: https://gist.github.com/nickfarrow/64c2e65191cde6a1a47bbd4572bf8cf8/
> * [3] Mullvad VPN was subject to a search warrant. Customer data not compromised: https://mullvad.net/en/blog/2023/4/20/mullvad-vpn-was-subject-to-a-search-warrant-customer-data-not-compromised/
> * [4] Blind Schnorr Signatures and Signed ElGamal Encryption in the Algebraic Group Model: https://eprint.iacr.org/2019/877.pdf
> * [5] FROST in secp256kfun: https://docs.rs/schnorr_fun/latest/schnorr_fun/frost/index.html
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230829/adbdd278/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 30 Aug 2023 11:05:03 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: ryan@breen.xyz
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Sentinel Chains: A Novel Two-Way Peg
Message-ID:
	<E9WH5C46HJT_uwLTnliTeZSZPrPwoKQs57muUxPVzaGWCWWriC4m2HGVoagR8dfvRBU_1qGtvlhojqIf_854em3_bJIR6DzAqAGHR6fW_nI=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


Good morning Ryan,


> I appreciate your questions, ZmnSCPxj.
> 
> I will answer your second question first: Mainchain nodes do not ever validate sidechain blocks. Sidechain nodes watch Bitcoin for invalid withdrawals, and publish signed attestations to a public broadcast network (such as Nostr) that a transaction is making an invalid withdrawal. These sidechain nodes are the so-called sentinels.

Let me reiterate my question:

Suppose I trust some sidechain node that is publishing such an attestation.

Then the sidechain node is hacked or otherwise wishes to disrupt the network for its own purposes.
And it attests that a valid sidechain withdrawal is actually invalid.

What happens then?

To the point, suppose that the attestation private key is somehow leaked or determined by a third party that has incentive to disrupt the mainchain network.

And it seems to me that this can be used to force some number of nodes to fork themselves off the network.

This is dangerous as nodes may be monitoring the blockchain for time-sensitive events, such as Lightning Network theft attempts.

Making "fork off bad miners!" a regular occurrence seems dangerous to me.

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 49
*******************************************
