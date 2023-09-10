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

   1. New BIP to align descriptors,	xpub derivation and miniscript
      (Dr Maxim Orlovsky)
   2. Bitcoin Fusion Protocol (BFP) (celeris@use.startmail.com)


----------------------------------------------------------------------

Message: 1
Date: Sun, 10 Sep 2023 17:13:02 +0000
From: Dr Maxim Orlovsky <orlovsky@lnp-bp.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] New BIP to align descriptors,	xpub derivation
	and miniscript
Message-ID:
	<4zh22wKfn7dGB-ZolHCLixP4gv_-gsdkfndbDxdoE7K7yyO-LDMvxZk1UVpp0YTGSRCqGtYlMitSQ5aLP9bIa2wj5Ul38Rw-DmagwxRdWhc=@lnp-bp.org>
	
Content-Type: text/plain; charset=utf-8

Hi,

Script output descriptors ("output descriptors", "wallet descriptors", or 
simply "descriptors") are getting more and more traction. Descriptors work 
in combination with miniscript, extended BIP32 keys (xpub/xprivs 
"descriptors" equipped with origin and derivation information) and are used
to construct new primitives like "wallet templates" used in Ledger and 
BitBox today.

Nevertheless, due to historical reasons, the resulting combination of the 
mentioned technologies is frequently redundant and leaves a lot of 
unspecified caveats, when it is unclear how descriptor with 
internally-conflicting data has to be handled by wallets and/or devices. 
For instance,
- derivation path standards (following BIP44) commit to the type of the 
  script pubkey (P2PKH, P2SH, P2WSH, P2WPKH, P2TR), but the same information
  is present in the descriptor itself;
- each of the public keys within the descriptor replicates the derivation 
  information and information about Bitcoin network (testnet or mainnet);
- if the same signer participates in different miniscript branches, due 
  to miniscript anti-malleability rules a new derivation path has to be used
  in pre-Taproot context (but not in Taproot) -= and multiple contradictory
  approaches exist on how to handle that;
- client-side-validation approach, used by several projects, introduces new
  descriptor-level concepts, like taproot-ebmedded OP_RETURN commitments 
  (so-called "tapret"), which are not handled by existing standards.

As a result, descriptors contain a lot of redundant information, which makes
them bulk, hard to read or type, and impossible to handle in the narrow UI
of hardware wallets.

At LNP/BP Standards Association we'd like to work/coordinate efforts on 
a new BIP proposal removing all the issues above. Before working on the 
BIP proposal text I would like to start by discussing an approach, seeking
Concept (n)ACKs and Approach (n)ACKs from this mail list.


The approach
------------

Existing separate BIP44 standards, committing to a specific form of script
pubkey are made redundant with the introduction of output descriptors. Thus,
I think we need a new BIP44 purpose field which will be used with all 
descriptor formats. The standard must _lexicographically require_ all keys 
to follow the same standard and use the same network and terminal derivation
format. By "lexicographically require" I mean that there must be no 
syntactic option to do otherwise, i.e. the information must not repeat 
within the descriptor for each of the keys and has to be placed in the 
descriptor itself, using prefix (for the network) and suffix (for the 
terminal derivation format):

```
wsh/test(or(
    and(1@[fe569a81//1']xpub1..., 2@[8871bad9//1h]xpub2..., 3@[beafcafe//1']xpub3...), 
    and(older(1000), thresh(2, @1, @2, @3))
))/<0;1>/*
```

Please note that each of the keys appears in the descriptor only once, and
is aliased using the `i@` construction preceding the key origin. These
aliases must be incremental starting from `1` (otherwise the descriptor is
invalid). Each other time the same account xpub is used in some other
condition only the alias should be used.

For the mainnet the prefix must be omitted: `wsh(or...)/<0;1>/*`

The descriptor is used to construct derivation for each of the keys 
in the same way:

`m/89'/network'/account'/branch/<0;1>/*`

where:
- 89' is the purpose - an assumed number for the newly proposed BIP;
- `network'` is either `0'` or `1'` and is taken from the descriptor prefix;
- `account` is taken from the xpub origin in the descriptor (it follows the
  master fingerprint and `//` character) and the last `/<0;1>/*` must match
  the descriptor suffix.
- `branch` part, which is a new segment compared to BIP44. This branch index
  must be always unhardened and is computed from the descriptor, starting 
  with 0 for each key and incrementing each time the same key alias is found
  in the descriptor;
- `<0;1>` may contain only 0, 1 index, unless a dedicated BIP extending 
  the meaning of this segment is filed. One such case may be the use of 
  a change index for storing an associated state in client-side-validation,
  like in RGB protocol, where indexes 9 and 10 are used to represent the
  assignation of an external state or the presence of a tapret commitment.
  It is important to require the standardization of new change indexes since
  without that wallets unaware of clinet-side-validation may spend the UTXO
  and burn the external state.


Reference implementation
------------------------

Once the approach is acknowledged by the mailing list the reference 
implementation will be written on Rust and deployed with MyCitadel wallet 
(https://mycitadel.io), which is the only wallet supporting since spring
2022 combination of all three: descriptors, miniscript and taproot (there 
are more descriptor/miniscript wallets which have appeared over the last 
year, but they are still lacking taproot support AFAIK).


Kind regards,
Maxim Orlovsky
LNP/BP Standards Association
https://www.lnp-bp.org/

GitHub: @dr-orlovsky
Nostr: npub13mhg7ksq9efna8ullmc5cufa53yuy06k73q4u7v425s8tgpdr5msk5mnym



------------------------------

Message: 2
Date: Sun, 10 Sep 2023 17:21:26 -0000
From: celeris@use.startmail.com
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin Fusion Protocol (BFP)
Message-ID: <169436648600.20.13269452997265912796@startmail.com>
Content-Type: text/plain; charset="utf-8"


    # Bitcoin Fusion Protocol (BFP)
    
    ## Motivation
    
    This work builds upon, and slightly modifies the previous Sidechains paper by Adam Back et. al [1] to address theft concerns raised by ZmnSCPxj [2] and others [3]. Additionally, this work is motivated by recent discussion suggesting that Bitcoin users give miners ownership over all Bitcoins sent to Drivechains [4] by "leaning in" to the challenges that all sidechain-like proposals face, as opposed to mitigating the risks as best as possible at the protocol level.
    
    The proposal herein is a high-level conceptual proposal, not a low-level technical proposal. It is being sent to the list because as far as the author is aware, these suggestions have not been made before. It is up to those with intimate knowledge of the inner workings and limitations of Bitcoin to decide how, if at all, to adapt this proposal to Bitcoin's constraints.
    
    ## BFP Summary
    
    We describe the following mechanisms (some new, some from the Sidechains paper):
    
    1. Before transferring coins from Chain A to B we lock them on Chain A by creating a special transaction that says, "these coins are being sent to Chain B". The fact that the coins are locked is stored in a merkle tree for easy verification by other chains.
    2. On Chain B, a transaction is created to transfer the tokens containing an SPV proof. Once accepted as part of the chain, the SPV proof from Chain A cannot be reused. We recommend, to reduce the storage costs of remembering proofs, that proofs older than 30 days be rejected (see "Missing details"). Only transfers for which at least 95% of the connected full nodes respond with a valid SPV proof will be accepted into a block to reduce the risk of forks.
      - Note: refer to the Sidechains paper [1] for details on the "confirmation period" and "contest period" in Section 3.2.
    3. Connecting approved blockchains is accomplished through a vote. If Chain A wishes to fuse with Chain B, it first conducts a supermajority vote to do so. If the proposal passes on Chain A, this fact is sent in a special proposal transaction asking the Chain B consensus group ("miners") to vote on the request to fuse together. If a supermajority on Chain B votes "yes" (say, at over 70% approval), over a certain time window (say 3 weeks), then the chains are "fused" and are authorized to transfer coins to each other. This is similar to how IBC [5] works.
    4. Light client verification requirements on miners and full nodes. All miners and full nodes on Chain A must run light client software for Chain B, and vice versa, in order to validate (with SPV-level security) that incoming coins from the other chain have valid proofs. They must remember recent lock proofs so that they cannot be reused. The light clients must be fully synced with the other chains before the miner publishes a block, so that it can verify the transfer occurred in a recent block on the other chain. These light clients must communicate with the full nodes of the chain they are validating so that they can catch any fabrications made by miners.
    5. Other chains can have arbitrary consensus mechanisms, and are in fact encouraged to use something other than Nakamoto consensus so that a different consensus group can build the other chain.
    
    ## Differences with Sidechains paper
    
    The main differences involve the light client requirements. If a standardized light client protocol can be developed and enforced to validate sidechains, then the likelihood of theft can reduced significantly. The reason theft is more likely to occur with the original Sidechains proposal is that mainchain miners do not connect to sidechain full nodes. This proposal "fuses" chains together to minimize the likelihood of theft by requiring that fused chains validate each other through a light client protocol that communicates with the full nodes of the fused chain.
    
    It further enforces that full nodes of Chain B use the generalized light client protocol to reject blocks mined by Chain B miners if those blocks contain transfers from Chain A that cannot be verified by Chain A full nodes. See "Theft attempts" below for more details.
    
    Because there is a single generic light client protocol that can be used to validate any sidechain, full nodes and miners of a chain can immediately begin to validate newly "fused" sidechains. The light client protocol is designed purposefully to support additional arbitrary consensus protocols. Although at the start it may only support one consensus protocol, through upgrades of the full node software it can be modified to support arbitrary consensus protocols on an as-needed basis (like PoS, etc.).
    
    ## Advantages over other proposals
    
    1. Users do not give up custody of their coins to miners.
    2. Users do not need to wait months to get their Bitcoin transferred between one chain to another. The transfer can happen in minutes or hours, depending on various security parameter considerations (like block production rate, value transferred, etc.).
    3. There is no incentivisation of miner centralization. In fact, this proposal increases decentralization by encouraging different mining groups to form around other chains using different consensus algorithms.
    4. There is no need for an on-chain constant transaction-per-block overhead from fused chains. A tiny amount of off-chain storage space is needed by full nodes to keep track of recently used SPV proofs and sidechain headers.
    5. It is possible for users to send coins from one sidechain to another without going through the main chain. Some other proposals support this feature too, but not all, so it's worth mentioning.
    
    ## Tradeoffs and security considerations
    
    ### Theft attempts
    
    A miner on Chain B could insert a provably invalid transfer transaction for coins that were were not actually locked on Chain A.
    
    In this case, other miners on Chain B that detect the fraud must not build on this block and Chain B full nodes must also reject the block.
    
    Both miners and full nodes must ensure that they are connected to at least 7 different full nodes per fused chain. They should use a "diversity metric" to pick the IPs that they connect to, so that they are not connecting to 7 IPs on the same subnet (if at all possible). At least 95% of these must respond with a valid SPV proof for a transfer to be considered valid. The number 7 is chosen because some number must be picked and 7 seems reasonable to the author (not too small, but also not so large that it becomes burdensome on full nodes). Theory and real-world testing might suggest a different number. If the node cannot establish this minimum number of connections to any particular fused chain, it should warn the user of the increased risk of being unable to properly validate either chain.
    
    Although unlikely, it is also theoretically possible that a chain may decide to vote to fuse a sidechain that is purposefully designed for the sole purpose of stealing any coins sent to it, or a sidechain that later falls under the full control of a malicious entity. In this situation, both the miners and all full nodes on the fraudulent chain lie. In such a situation, any coins sent to this chain can be stolen. However, this unlikely situation would be detected, and mitigations are still possible. Full nodes on the parent chain could decide to blacklist the fradulent sidechain and refuse to accept blocks containing transactions from it (potentially causing the parent chain to grind to a halt until good miners -- who also refuse to accept transactions from the sidechain -- take over). There could be a vote to "defuse" from the sidechain. And finally, we note that the maximum damage in this worst-case scenario is still significantly less than the worst-case scenario of alternative
  proposals like Drivechain [4] where the possibility of stolen funds is greater and exists equally for every drivechain for the following reasons:
    
    1. In BFP (and Sidechains), coins are locked and an SPV proof is required to unlock them. In Drivechains, all coins sent to drivechains are given to Bitcoin miners from the outset via the so-called "hashrate escrow".
    2. In BFP, there is the very distinct and clear possibility that many diverse groups are responsible for the security of the overall system, and the compromise of any one of these groups only affects the specific sidechain. For example, if there are 10 sidechains, there are potentially 10 different consensus groups involved. However, in Drivechain, there is a single group responsible for the security of all drivechains and the mainchain. At the moment that group consists of two companies [6].
    
    ### Lost funds
    
    If Chain A locks coins and sends them to Chain B, but Chain B doesn't accept them for whatever reason, then it is possible for the coins to become forever lost.
    
    The 30 day window allows for the possibility of resending the transaction with a higher fee, but if after 30 days from the original locking transaction the coins are still not transferred to the receiving chain, they are locked forever. This is unlikely but not impossible.
    
    It might be possible to improve this proposal in some way by adding a new "proof of non-inclusion"[7,8] to allow for the recovery of the lost funds. Alternatively, the 30 day window could be removed completely, at extra storage cost to full nodes for having to remember all SPV proofs.
    
    ### Increased fork risk
    
    This proposal increases the amount of outgoing connections traffic that a full node must initiate in order to fully validate blocks. Traffic is increased with each additional fused chain. If, for some reason, the full node is not able to communicate with the honest full nodes of every fused chain, it might not be able to validate every block and therefore is at increased risk of forking off and being unable to continue validating new blocks.
    
    ## Missing details
    
    As stated, this proposal is not a fully specified proposal. It is a seed intended to spark discussion and further iteration, building on the wonderful work of the original Sidechain proposal authors. To that end, the following details must be filled in:
    
    1. The precise nature of the generalized light client protocol and how it can be designed to expand to support different consensus algorithms (not just PoW).
    2. Just how significant of a fork risk is introduced here and mechanisms by which it could be reduced.
    3. How much storage could be expected for having to remember all SPV proofs (to prevent re-use). If it's insignificant, then the 30 day window should be removed.
    
    ## Conclusion
    
    This proposal is given to the community to improve and expand upon as it sees fit.
    
    The author of this proposal summary will not be filling in the technical details nor sending in an implementation. The point of this proposal is to show that there is a Bitcoin-way to do multi-chain ? if the Bitcoin community wants that feature and wishes to keep the Bitcoin spirit alive.
    
    ```
                                     .                                         
                                -#-  ##                                        
                              .-=%%+*##=...   .....                            
                            .=*#######+-=++::-+-+*=---::.                      
                          :*#######%%%#*##.  ::---==++=---::                   
                        :+####*+::-++%%%#. .=-:--=-+=-+#****#+.                
                      :=+++*+==*+::--+%%+   =+-+-==+=-=++*####*                
                     :++++*#-=-=*:-:+*%%-   :--+--==--**-=-*####:              
                   :-***++###+*++==+#%%+    .=====---=+=-=-+####+              
                -=++++*##*****#**###%%*#:    ..-=-:-++##+---+#####+:           
              :=+++++*#*#%#*+=#########==+-..=-:::  :=+*+###########*+         
          :-=++++***#%%%%#**=:.*#%%%%%#-::   .--++-----  :-#*#########*=:      
         -+#*++++*#+=#%%#++***-  .::...            .:. =**###*###########=     
        =*+****#*=. .##******#:                       -*#####*#**=:+#######:   
       =##*****-     :  =*##*=                        .=#####+*++=  :*#####+.  
     :.+#*-::.          =*##                            .****.:      .--=+*##= 
    *#*+:               -==+*-.                       .=***#+             -+##*
    ```
    
    ## References
    
    - [1] [https://blockstream.com/sidechains.pdf](https://blockstream.com/sidechains.pdf)
    - [2] [https://zmnscpxj.github.io/sidechain/weakness/index.html](https://zmnscpxj.github.io/sidechain/weakness/index.html)
    - [3] [https://diyhpl.us/~bryan/papers2/bitcoin/Drivechains,%20sidechains%20and%20hybrid%202-way%20peg%20designs%20-%20Sergio%20Lerner%20-%202016.pdf](https://diyhpl.us/~bryan/papers2/bitcoin/Drivechains,%20sidechains%20and%20hybrid%202-way%20peg%20designs%20-%20Sergio%20Lerner%20-%202016.pdf)
    - [4] [https://www.drivechain.info](https://www.drivechain.info)
    - [5] [https://ibcprotocol.org](https://ibcprotocol.org)
    - [6] [https://www.blockchain.com/explorer/charts/pools?timespan=24hrs](https://www.blockchain.com/explorer/charts/pools?timespan=24hrs)
    - [7] [https://crypto.stackexchange.com/questions/53991/is-there-a-cryptographic-solution-to-provide-a-proof-of-exclusion](https://crypto.stackexchange.com/questions/53991/is-there-a-cryptographic-solution-to-provide-a-proof-of-exclusion)
    - [8] [https://old.reddit.com/r/cryptography/comments/u3s341/proofofexclusion_data_structure/](https://old.reddit.com/r/cryptography/comments/u3s341/proofofexclusion_data_structure/)
      
    

  

-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230910/0eb57d97/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 11
********************************************
