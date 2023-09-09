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

   1. Re: BIP-????: The Taproot Assets Protocol (Zac Greenwood)


----------------------------------------------------------------------

Message: 1
Date: Thu, 7 Sep 2023 18:31:57 +0200
From: Zac Greenwood <zachgrw@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,  Olaoluwa Osuntokun
	<laolu32@gmail.com>
Subject: Re: [bitcoin-dev] BIP-????: The Taproot Assets Protocol
Message-ID:
	<CAJ4-pED=TOqiwRjHXTPqJ4uVGMHmKz0hRQXUhZbHZjCk4MXW7w@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Laolu,

Could you explain please how facilitating registering non-Bitcoin assets on
the Bitcoin blockchain is beneficial for the Bitcoin economy?

Thanks,
Zac

On Wed, 6 Sep 2023 at 21:02, Olaoluwa Osuntokun via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> After more than a year of tinkering, iterating, simplifying, and
> implementing, I'm excited to officially publish (and request BIP numbers
> for) the Taproot Assets Protocol. Since the initial publishing we've
> retained the same spec/document structure, with the addition of a new BIP
> that describes the vPSBT format (which are PSBTs for the TAP layer). Each
> BIP now also contains a set of comprehensive test vectors (to be further
> expanded over time.
>
> https://github.com/bitcoin/bips/pull/1489
>
> As the complete set of documents is large, we omit them from this email.
>
> The breakdown of the BIPs are as follows:
>
>   * `bip-tap-mssmt`: describes the MS-SMT (Merkle-Sum Sparse Merkle Tree)
>     data structure used to store assets and various proofs.
>
>   * `bip-tap`: describes the Taproot Assets Protocol validation and state
>     transition rules.
>
>   * `bip-tap-addr`: describes the address format used to send and receive
>     assets.
>
>   * `bip-tap-vm`: describes the initial version of the off-chain TAP VM
> used
>     to lock and unlock assets.
>
>   * `bip-tap-vpsbt`: describes a vPSBT (virtual PSBT) which is a series
>     custom types on top of the existing PSBT protocol to facilitate more
>     elaborate asset related transactions.
>
>   * `bip-tap-proof-file`: describes the flat file format which is used to
>     prove and verify the provenance of an asset
>
>   * `bip-tap-universe`: describes the Universe server construct, which is
> an
>     off-chain index into TAP data on-chain, used for: proof distribution,
>     asset boostraping, and asset transaction archiving.
>
> Some highlights of the additions/modifications of the BIPs since the
> initial
> drafts were published last year:
>
>   * Test JSON vectors for each BIP document now included.
>
>   * The Universe construct for initial verification of assets, distributing
>     asset proofs, and transaction archiving is now further specified. A
>     naive and tree based syncing algorithm, along with a standardized
>     REST/gRPC interface are now in place.
>
>   * The asset group key structure (formerly known as asset key families)
> has
>     been further developed. Group keys allow for the creation of assets
> that
>     support ongoing issuance. A valid witness of a group key during the
>     minting process allows otherwise disparate assets to be considered
>     fungible, and nested under the same sub-tree. A group key is itself
> just
>     a taproot output key. This enables complex issuance conditions such as:
>     multi-sig threshold, hash chain reveal, and any other conditions
>     expressible by script (and eventually beyond!).
>
>   * New versioning bytes across the protocol to ensure extensibility and
>     upgradability in a backwards compatible manner where possible. The
> asset
>     metadata format now has been re-worked to only commit to a hash of the
>     serialized meta data. Asset metadata can now also have structured data,
>     key-value or otherwise.
>
>   * Observance of re-org protection for asset proofs. The file format now
>     also uses an incremental hash function to reduce memory requirements
>     when added a new transition to the end of the file.
>
>   * Specification of the vPSBT protocol [1] which is the analogue of normal
>     PSBTs for the TAP layer. The packet format specifies custom key/value
>     pairs for the protocol describes an aggregate TAP transaction. After
> the
>     packet is signed by all participants, it's "anchored" into a normal
>     Bitcoin transaction by committing to the resulting output commitments
>     and witnesses.
>
> We've also made significant advancements in our initial implementation [2],
> with many wallets, explorers, services, and businesses working with us to
> test and iterate on both the protocol and the implementation. We're
> actively
> working on our next major release, which will be a major milestone towards
> the eventual mainnet deployment of the protocol!
>
>
> -- Laolu
>
> [1]: https://lightning.engineering/posts/2023-06-14-virtual-psbt/
> [2]: https://github.com/lightninglabs/taproot-assets
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230907/5796b886/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 7
*******************************************
