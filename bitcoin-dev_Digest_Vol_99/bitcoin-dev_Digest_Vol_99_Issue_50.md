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

   1. Re: Blinded 2-party Musig2 (Tom Trevethan)
   2. Re: Private Collaborative Custody with FROST (Nick Farrow)


----------------------------------------------------------------------

Message: 1
Date: Wed, 30 Aug 2023 11:52:05 +0100
From: Tom Trevethan <tom@commerceblock.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Blinded 2-party Musig2
Message-ID:
	<CAJvkSsfcp2shLjEdwRKtBJBO+wiV=m5X_Ys1sTwUZKZWg9-HeQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

An update on progress on the development of the blinded two-party Schnorr
scheme for statechains.

As stated previously, we believe that one-more-signature and Wagner attacks
are mitigated by the client committing the values of the blinding nonce
used (labeled f) and the value of R2 used in a signing session to the
server before the server responds with their value of R1. Then each time
the generated signature is verified (in our application this is a new
statecoin owner), the verifier retrieves the commitments and blinded
challenge value from the server (c, SHA256(f) and SHA256(R2)) and f and R2
from the co-signer, and verifies that the blinded challenge value c = f +
SHA256(X, R1 + R2 + f.X, m) and the commitments match f,R2. This ensures
the signer cannot have chosen the values of f and R2 after the value of R1
is randomly generated by the server.

This scheme has been implemented in a forked version of the secp256k1-zkp
library: https://github.com/ssantos21/secp256k1-zkp where a new function
has been added secp256k1_blinded_musig_nonce_process (
https://github.com/ssantos21/secp256k1-zkp/blob/ed08ad7603f211fdf39b5f6db9d7e99cf048a56c/src/modules/musig/session_impl.h#L580
) which is required for the client generation of the blinded challenge
value.

One issue that came up and had to be solved was ensuring the R (curve
point) is even (in MuSig2 the secret nonce is negated if R is odd) with the
point f.X added (and f committed to). We will add a complete explanation of
this to the updated spec.

The scheme is implemented in a blind server:
https://github.com/ssantos21/blinded-musig-sgx-server

And client:
https://github.com/ssantos21/blinded-musig2-client

Any comments or questions appreciated.

On Mon, Aug 7, 2023 at 1:55?AM Tom Trevethan <tom@commerceblock.com> wrote:

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
> computed c = SHA256(X1 + X2, R1 + R2, m)  and each commitment equals
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
>>>  >   Using Wagner's algorithm, choose R2[0], ..., R2[K-1] such that
>>>  >    c[0] + ... + c[K-1] = c[K].
>>>
>>> You can think of this as actually choosing scalars r2[0], ..., r2[K-1]
>>> and
>>> define R2[i] = r2[i]*G. The attacker chooses r2[i]. The attack wouldn't
>>> make
>>> sense if he didn't.
>>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230830/a084cbf0/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 30 Aug 2023 14:16:28 +0200
From: Nick Farrow <nicholas.w.farrow@gmail.com>
To: rot13maxi <rot13maxi@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Private Collaborative Custody with FROST
Message-ID:
	<CAO1LTYX33q979c2QV+4JFJBTZAGZooWVprs6gUNvDUFFjJxY=A@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hey Rijndael,

Here are some rough ideas for a draft scheme that I think will help explain
this better.

We begin by taking a single public nonce `D` from the collaborative signing
server to form a nonce pair for FROST `(D, 0)`.

This is then used to build the aggregate FROST nonce `R` which the signer
set `S` is going to sign under:
```
R_i = D_i * (E_i)^?_i
R = Product[R_i, i in S]
```
This aggregate FROST nonce is now blinded by the contributions from other
signers (collaborative custodian doesn't know the other participant's
nonces)

Now with our FROST public key `X`, this aggregate nonce `R`, and a message
`m` corresponding to our planned Bitcoin transaction input, we calculate
the corresponding challenge `c` we need signed.

```
c = H(R || X || m)
```

Like regular blind schnorr, we also want to blind this challenge so that
the signing server cannot recognize it onchain.

The challenge can be blinded with a factor that includes the necessary
Lagrange coefficient so that the partial signature correctly combines with
the other FROST signatures from the signing quorum. Using their participant
index `i` and the set of signing parties `S`
```
c' = ?_i_S * c
```

Note: if this `?_i_S` is the sole challenge blinding factor, it is
important that we give the collaborative custodian a non-trivial (random)
participant index such that they cannot lookup onchain challenges
multiplied by common Lagrange coefficients to match the challenge they
signed.

Now we have formed the challenge, we get the server to sign under the
regular Schnorr singing equation using their FROST secret share `s_i` and
nonce secret `d_i`:

```
z_i = d_i + (e_i * ?_i) + ?_i * s_i * c # FROST signing equation
= d_i + (0 * ?_i) + s_i * c' # Since we're signing for binonce commitment
(D, 0)
= d_i + s_i * c'
```

Once we have this partial signature, we get the other `t-1` participants to
undertake FROST signing. We take the collaborative custodian's signature
and combine it with the other partial signatures to form a complete Schnorr
signature for the message valid under the group's FROST key.

Again, security needs a serious assessment. Especially because we're
dropping the binding factor in the collaborative custodian's nonce. It's
likely crucial that collaborative signing sessions are not done in parallel
and transaction inputs are signed one at a time.

Hope that explains the ideas for blinding and FROST compatibility better!

Nick

On Tue, Aug 29, 2023 at 1:52?PM rot13maxi <rot13maxi@protonmail.com> wrote:

> Good morning Nick,
>
> Love the direction of this.
>
> > We can achieve this compatibility by having the server sign under a
> single nonce (not a binding nonce-pair like usual FROST), which is later
> blinded by the nonce contributions from other signers.
>
> Can you say more about this? It sounds like the blinding is happening
> post-signing? Or is it happening during the normal nonce commitment trading?
>
> Rijndael
>
> On Mon, Aug 28, 2023 at 3:35 PM, Nick Farrow via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org
> <On+Mon,+Aug+28,+2023+at+3:35+PM,+Nick+Farrow+via+bitcoin-dev+%3C%3Ca+href=>>
> wrote:
>
> Hello all,
>
> Some thoughts on private collaborative custody services for Bitcoin.
>
> With multiparty computation multisignatures like FROST [0], it is possible
> to build a collaborative custodian service that is extremely private for
> users.
>
> Today's collaborative custodians can see your entire wallet history even
> if you never require them to help sign a transaction, and they have full
> liberty to censor any signature requests they deem inappropriate or are
> coerced into censoring.
>
> With FROST, a private collaborative custodian can hold a key to a multisig
> while remaining unaware of the public key (and wallet) which they help
> control. By hiding this public key, we solve the issue of existing
> collaborative custodians who learn of all wallet transactions even if you
> never use them.
>
> Further, in the scenario that we do call upon a private collaborative
> custodian to help sign a transaction, this transaction could be signed
> **blindly**. Being blind to the transaction request itself and unknowing of
> past onchain behavior, these custodians have no practical information to
> enact censorship requests or non-cooperation. A stark contrast to today's
> non-private collaborative custodians who could very easily be coerced into
> not collaborating with users.
>
>
> Enrolling a Private Collaborative Custodian
>
> Each signer in a FROST multisig controls a point belonging to a joint
> polynomial at some participant index.
>
> Participants in an existing multisig can collaborate in an enrollment
> protocol (Section 4.1.3 of [1], [2]) to securely generate a new point on
> this shared polynomial and verifiably communicate it to a new participant,
> in this case a collaborative custodian.
>
> The newly enrolled custodian should end by sharing their own *public*
> point so that all other parties can verify it does in-fact lie on the image
> of the joint polynomial at their index (i.e. belong to the FROST key). (The
> custodian themselves is unable to verify this, since we want to hide our
> public key we do not share the image of our joint polynomial with them).
>
>
> Blind Collaborative Signing
>
> Once the collaborative custodian controls a point belonging to this FROST
> key, we can now get their help to sign messages.
>
> We believe it to be possible for a signing server to follow a scheme
> similar to that of regular blind Schnorr signatures, while making the
> produced signature compatible with the partial signatures from other FROST
> participants.
>
> We can achieve this compatibility by having the server sign under a single
> nonce (not a binding nonce-pair like usual FROST), which is later blinded
> by the nonce contributions from other signers. The challenge also can be
> blinded with a factor that includes the necessary Lagrange coefficient so
> that this partial signature correctly combines with the other FROST
> signatures from the signing quorum.
>
> As an overview, we give a 3rd party a secret share belonging to our FROST
> key. When we need their help to sign something, we ask them to send us
> (FROST coordinator) a public nonce, then we create a challenge for them to
> sign with a blind Schnorr scheme. They sign this challenge, send it back,
> and we then combine it with the other partial signatures from FROST to form
> a complete Schnorr signature that is valid under the multisignature's
> public key.
>
> During this process the collaborative custodian has been unknowing of our
> public key, and unknowing as to the contents of the challenge which we have
> requested them to sign. The collaborative signer doesn't even need to know
> that they are participating in FROST whatsoever.
>
>
> Unknowing Signing Isn't So Scary
>
> A server that signs arbitrary challenges sounds scary, but each secret
> share is unique to a particular FROST key. The collaborative custodian
> should protect this service well with some policy, e.g. user
> authentication, perhaps involving cooperation from a number of other
> parties (< threshold) within the multisig. This could help prevent parties
> from abusing the service to "get another vote" towards the multisig
> threshold.
>
> Unknowingly collaborating in the signing of bitcoin transactions could be
> a legal gray area, but it also places you in a realm of extreme privacy
> that may alleviate you from regulatory and legal demands that are now
> impossible for you to enforce (like seen with Mullvad VPN [3]). Censorship
> requests made from past onchain behavior such as coinjoins becomes
> impossible, as does the enforcement of address or UTXO blocklists.
>
> By having the collaborative custodian sign under some form of blind
> Schnorr, the server is not contributing any nonce with binding value for
> the aggregate nonce. Naively this could open up some form of Drijvers
> attacks which may allow for forgeries (see FROST paper [0]), but I think we
> can eliminate given the right approach.
>
> Blind Schnorr schemes also introduce attack vectors with multiple
> concurrent signing requests [4], one idea to prevent this is to disallow
> simultaneous signing operations at the collaborative custodian. Even though
> Bitcoin transactions can require multiple signatures, these signatures
> could be made sequentially with a rejection of any signature request that
> uses anything other than the latest nonce.
>
> Risks may differ depending on whether the service is emergency-only or for
> whether it is frequently a participant in signing operations.
>
> -------
>
> Thanks to @LLFOURN for ongoing thoughts, awareness of enrollment
> protocols, and observation that this can all fall back into a standard
> Schnorr signature.
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
> * [1] A Survey and Refinement of Repairable Threshold Schemes (Enrollment:
> Section 4.3): https://eprint.iacr.org/2017/1155.pdf
> * [2] Modifying FROST Threshold and Signers:
> https://gist.github.com/nickfarrow/64c2e65191cde6a1a47bbd4572bf8cf8/
> * [3] Mullvad VPN was subject to a search warrant. Customer data not
> compromised:
> https://mullvad.net/en/blog/2023/4/20/mullvad-vpn-was-subject-to-a-search-warrant-customer-data-not-compromised/
> * [4] Blind Schnorr Signatures and Signed ElGamal Encryption in the
> Algebraic Group Model: https://eprint.iacr.org/2019/877.pdf
> * [5] FROST in secp256kfun:
> https://docs.rs/schnorr_fun/latest/schnorr_fun/frost/index.html
>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230830/d2aba048/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 50
*******************************************
