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

   1. Re: New BIP to align descriptors,	xpub derivation and
      miniscript (Antoine Poinsot)
   2. Re: Trustless 2-way-peg without softfork (G. Andrew Stone)
   3. Re: Actuarial System To Reduce Interactivity In	N-of-N (N >
      2) Multiparticipant Offchain Mechanisms (ZmnSCPxj)


----------------------------------------------------------------------

Message: 1
Date: Mon, 11 Sep 2023 12:03:59 +0000
From: Antoine Poinsot <darosior@protonmail.com>
To: Dr Maxim Orlovsky <orlovsky@lnp-bp.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] New BIP to align descriptors,	xpub
	derivation and miniscript
Message-ID:
	<2rp3BsP6bOyUTJeJhdylDfUGyBV2SCBSsiVsK0nNSH3Nky3yYXGeLN_TbwTeaNTVAv5E_DIgbGI83rVVG7jwSBOMAzM3P226xydeIaSn9i8=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Maxim,

That does not sound compelling. Let's go through your points.

First you point how some wallets supporting descriptors keep vague BIP44 compatibility. There are multiple reasons for this, but first you say that the derivation path "commits to" (i think you mean describe? that's rather what you want for a backup) output types such as P2WSH or P2TR. It's incorrect. That's the whole point of descriptors. There are standardized paths for Taproot *keyspend* and weird multisig P2WSH templates. But you can't keep an infinite list of BIP44 templates for all the scripts it's possible to use under those output types.
As for the reasons for keeping BIP44 compatibility in some wallets:
- It makes sense for some output types to keep compatibility with non-descriptor wallets. For instance see how the Bitcoin Core wallet uses BIP86 for Taproot keyspend despite it being descriptor-based. [0]
- Some signing devices whitelist the paths you can extract an xpub from without user confirmation. (It's the case of Ledger and the reason we have to resort to using legacy BIP48-derived paths in Liana.)

You then go to point out how it's useless to use legacy standards within descriptors. Sure, but that doesn't call for one more unscalable legacy standard. Just don't use it if you can afford to? I'd even go for `m/network'/account'/<0;1>/*` (rather than your `m/89'/network'/account'/branch/<0;1>/*`) if Ledger would let us.

You third point is about how you can't reuse public keys across spending paths within a Miniscript. But it doesn't prevent you from reusing the same signer, you can simply:
- Derive a different hardened xpub from the signing device for each occurrence (cumbersome); or
- Query a single xpub from the device and then append an unhardened derivation step. To reduce the number of steps you can even reuse the multipath step. (`xpub/<0;1>/*` for the first appearance, then `xpub/<2;3>/*`, `xpub/<4;5>/*`, ...)

(Small correction passing by: you mention the Miniscript duplicate key check doesn't apply under Taproot context, but it absolutely does. I think you meant across Taproot branches, but keep in mind you can have multiple spending paths within a single leaf.)

Your final point is about how your client-side validation project introduces some "descriptor-level concepts" which are not handled by current standards. If your new standard is incompatible with descriptors, fix it instead of trying to convince all existing wallets to become aware of it?

Cheers,
Antoine

[0] The motivation section of BIP86 says it all. https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki#motivation


------- Original Message -------
On Sunday, September 10th, 2023 at 7:13 PM, Dr Maxim Orlovsky via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Hi,
> 
> Script output descriptors ("output descriptors", "wallet descriptors", or
> simply "descriptors") are getting more and more traction. Descriptors work
> in combination with miniscript, extended BIP32 keys (xpub/xprivs
> "descriptors" equipped with origin and derivation information) and are used
> to construct new primitives like "wallet templates" used in Ledger and
> BitBox today.
> 
> Nevertheless, due to historical reasons, the resulting combination of the
> mentioned technologies is frequently redundant and leaves a lot of
> unspecified caveats, when it is unclear how descriptor with
> internally-conflicting data has to be handled by wallets and/or devices.
> For instance,
> - derivation path standards (following BIP44) commit to the type of the
> script pubkey (P2PKH, P2SH, P2WSH, P2WPKH, P2TR), but the same information
> is present in the descriptor itself;
> - each of the public keys within the descriptor replicates the derivation
> information and information about Bitcoin network (testnet or mainnet);
> - if the same signer participates in different miniscript branches, due
> to miniscript anti-malleability rules a new derivation path has to be used
> in pre-Taproot context (but not in Taproot) -= and multiple contradictory
> approaches exist on how to handle that;
> - client-side-validation approach, used by several projects, introduces new
> descriptor-level concepts, like taproot-ebmedded OP_RETURN commitments
> (so-called "tapret"), which are not handled by existing standards.
> 
> As a result, descriptors contain a lot of redundant information, which makes
> them bulk, hard to read or type, and impossible to handle in the narrow UI
> of hardware wallets.
> 
> At LNP/BP Standards Association we'd like to work/coordinate efforts on
> a new BIP proposal removing all the issues above. Before working on the
> BIP proposal text I would like to start by discussing an approach, seeking
> Concept (n)ACKs and Approach (n)ACKs from this mail list.
> 
> 
> The approach
> ------------
> 
> Existing separate BIP44 standards, committing to a specific form of script
> pubkey are made redundant with the introduction of output descriptors. Thus,
> I think we need a new BIP44 purpose field which will be used with all
> descriptor formats. The standard must lexicographically require all keys
> to follow the same standard and use the same network and terminal derivation
> format. By "lexicographically require" I mean that there must be no
> syntactic option to do otherwise, i.e. the information must not repeat
> within the descriptor for each of the keys and has to be placed in the
> descriptor itself, using prefix (for the network) and suffix (for the
> terminal derivation format):
> 
> ```
> wsh/test(or(
> and(1@[fe569a81//1']xpub1..., 2@[8871bad9//1h]xpub2..., 3@[beafcafe//1']xpub3...),
> and(older(1000), thresh(2, @1, @2, @3))
> ))/<0;1>/*
> 
> ```
> 
> Please note that each of the keys appears in the descriptor only once, and
> is aliased using the `i@` construction preceding the key origin. These
> aliases must be incremental starting from `1` (otherwise the descriptor is
> invalid). Each other time the same account xpub is used in some other
> condition only the alias should be used.
> 
> For the mainnet the prefix must be omitted: `wsh(or...)/<0;1>/*`
> 
> 
> The descriptor is used to construct derivation for each of the keys
> in the same way:
> 
> `m/89'/network'/account'/branch/<0;1>/*`
> 
> 
> where:
> - 89' is the purpose - an assumed number for the newly proposed BIP;
> - `network'` is either `0'` or `1'` and is taken from the descriptor prefix;
> - `account` is taken from the xpub origin in the descriptor (it follows the
> master fingerprint and `//` character) and the last `/<0;1>/*` must match
> 
> the descriptor suffix.
> - `branch` part, which is a new segment compared to BIP44. This branch index
> must be always unhardened and is computed from the descriptor, starting
> with 0 for each key and incrementing each time the same key alias is found
> in the descriptor;
> - `<0;1>` may contain only 0, 1 index, unless a dedicated BIP extending
> 
> the meaning of this segment is filed. One such case may be the use of
> a change index for storing an associated state in client-side-validation,
> like in RGB protocol, where indexes 9 and 10 are used to represent the
> assignation of an external state or the presence of a tapret commitment.
> It is important to require the standardization of new change indexes since
> without that wallets unaware of clinet-side-validation may spend the UTXO
> and burn the external state.
> 
> 
> Reference implementation
> ------------------------
> 
> Once the approach is acknowledged by the mailing list the reference
> implementation will be written on Rust and deployed with MyCitadel wallet
> (https://mycitadel.io), which is the only wallet supporting since spring
> 2022 combination of all three: descriptors, miniscript and taproot (there
> are more descriptor/miniscript wallets which have appeared over the last
> year, but they are still lacking taproot support AFAIK).
> 
> 
> Kind regards,
> Maxim Orlovsky
> LNP/BP Standards Association
> https://www.lnp-bp.org/
> 
> GitHub: @dr-orlovsky
> Nostr: npub13mhg7ksq9efna8ullmc5cufa53yuy06k73q4u7v425s8tgpdr5msk5mnym
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Mon, 11 Sep 2023 11:26:52 -0400
From: "G. Andrew Stone" <g.andrew.stone@gmail.com>
To: Dr Maxim Orlovsky <orlovsky@lnp-bp.org>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Trustless 2-way-peg without softfork
Message-ID:
	<CAHUwRvtadqomqDpWBuOwjJR7ftsTpE_-C4mPVAg0j3HqR6vFUw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Any chance of a quick tldr to pique our interest by explaining how exactly
this works "and the protocol will reach consensus on whether the state
reported by the oracle is correct" in presumably a permissionless,
anonymous, decentralized fashion, and what caveats there are?

Regards,
Andrew

On Sun, Sep 10, 2023 at 4:06?PM Dr Maxim Orlovsky via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi,
>
> Several years ago my team from Pandora Project working on
> censorship-resistant distributed machine learning proposed Prometheus: a
> protocol for high-load computing on top of Bitcoin. The protocol operates
> as a multi-party game setting where an oracle ("worker") is provided with
> an arbitrary computationally complex task (any Turing-complete computing,
> machine learning training or inference etc) and the network is able to
> reach a consensus on whether a result reported by the worker is true. The
> consensus is reached via optional rounds of verification and arbitrage. The
> protocol is cryptoeconomically-safe, i.e. has a proven Nash equilibrium.
> The protocol was later transferred to LNP/BP Standards Association (
> https://lnp-bp.org) and was kept in a backlog of what can be done in a
> future as a layer on top of Bitcoin.
>
> I'd like to emphasize that Prometheus works on Bitcoin, requires just
> several Bitcoin tx per task, and _doesn't require any soft fork_. All
> economic setting is done with Bitcoin as a means of payment, and using
> existing Bitcoin script capabilities.
>
> Link to the paper describing the protocol: <
> https://github.com/Prometheus-WG/prometheus-spec/blob/master/prometheus.pdf
> >
>
> Only today I have realized that Prometheus protocol can be used to build
> cryptoeconomically-safe (i.e. trustless) 2-way-peg on the Bitcoin
> blockchain without any soft-forks: a "worker" in such a case acts as an
> oracle for some extra-bitcoin system (sidechain, client-side-validated
> protocol, zk rollup etc) validating it, and the protocol will reach
> consensus on whether the state reported by the oracle is correct.
>
> In other words, this is an alternative to BIP-300 and other similar
> soft-forks having the only purpose of doing 2-way pegs. It also enables the
> two-way trustless transfer of Bitcoins between Bitcoin blockchain, RGB and,
> in a future, potential new layer 1 called "prime" (to learn more about
> prime you can check my Baltic Honeybadger talk <
> https://www.youtube.com/live/V3vvybsc1A4?feature=shared&t=23631>).
>
>
> Kind regards,
> Dr Maxim Orlovsky
> Twitter: @dr_orlovsky
> Nostr: npub13mhg7ksq9efna8ullmc5cufa53yuy06k73q4u7v425s8tgpdr5msk5mnym
>
> LNP/BP Standards Association
> Twitter: @lnp_bp
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230911/3196df1f/attachment-0001.html>

------------------------------

Message: 3
Date: Tue, 12 Sep 2023 09:41:18 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Actuarial System To Reduce Interactivity In
	N-of-N (N > 2) Multiparticipant Offchain Mechanisms
Message-ID:
	<6iN_WxykhKvHyD1bZRwbbPnePA36zekfcmUFDAchzjw6j7uSYXVmhrHRBhvAU-igU4AAGAggcV1FI9ScujGOZN8fN1GRZWN5u8rs1FMpSCQ=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Antoine,


> Hi Zeeman
> 
> > What we can do is to add the actuary to the contract that
> > controls the funds, but with the condition that the
> > actuary signature has a specific `R`.
> 
> > As we know, `R` reuse --- creating a new signature for a
> > different message but the same `R` --- will leak the
> > private key.
> 
> > The actuary can be forced to put up an onchain bond.
> > The bond can be spent using the private key of the actuary.
> > If the actuary signs a transaction once, with a fixed `R`,
> > then its private key is still safe.
> 
> > However, if the actuary signs one transaction that spends
> > some transaction output, and then signs a different
> > transaction that spends the same transaction output, both
> > signatures need to use the same fixed `R`.
> > Because of the `R` reuse, this lets anyone who expected
> > one transaction to be confirmed, but finds that the other
> > one was confirmed, to derive the secret key of the
> > actuary from the two signatures, and then slash the bond
> > of the actuary.
> 
> From my understanding, if an off-chain state N1 with a negotiated group of 40 is halted in the middle of the actuary's R reveals due to the 40th participant non-interactivity, there is no guarantee than a new off-chain state N1' with a new negotiated group of 39 (from which evicted 40th's output is absent) do not re-use R reveals on N1. So for the actuary bond security, I think the R reveal should only happen once all the group participants have revealed their own signature. It sounds like some loose interactivity is still assumed, i.e all the non-actuary participants must be online at the same time, and lack of contribution is to blame as you have a "flat" off-chain construction (i.e no layering of the promised off-chain outputs in subgroups to lower novation interactivity).

Yes, there is some loose interactivity assumed.

However:

* The actuary is always online and can gather signatures for the next state in parallel with signing new transactions on top of the next state.
  * This is why `SIGHASH_ANYPREVOUT` is needed, as the transactions on top of the next state might spend either the actual next state (if the next state is successfully signed), or the current state plus additional transactions (i.e. the transaction that move from current state to next state) (if the next state fails to get fully signed and the participants decide to give up on the next state getting signed).

> More fundamentally, I think this actuarial system does not solve the "multi-party off-chain state correction" problem as there is no guarantee that the actuary does not slash the bond itself. And if the bond is guarded by users' pubkeys, there is no guarantee that the user will cooperate after the actuary equivocation is committed to sign a "fair" slashing transaction.

Indeed.

One can consider that the participants other than the actuary would generate a single public key known by the participants.
But then only one sockpuppet of the actuary is needed to add to the participant set.

Basically, the big issue is that the actuary needs to bond a significant amount of funds to each participant, and that bond is not part of the funding of the construction.

Other ways of ensuring single-use can be replaced, if that is possible.
Do you know of any?

Regards,
ZmnSCPxj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 15
********************************************
