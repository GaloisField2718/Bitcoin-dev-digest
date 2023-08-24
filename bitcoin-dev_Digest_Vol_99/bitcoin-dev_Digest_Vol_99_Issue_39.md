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

   1. Re: Serverless Payjoin (alicexbt)
   2. BIP-119 UASF (alicexbt)
   3. Re: Sentinel Chains: A Novel Two-Way Peg (ryan@breen.xyz)


----------------------------------------------------------------------

Message: 1
Date: Sun, 20 Aug 2023 17:13:33 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Dan Gould <d@ngould.dev>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Serverless Payjoin
Message-ID:
	<8qSa5NNuqF64Yg-R-OvO34IYBI0efPOUYYGrFBwvhsDuRMdQzcA6joTi0BNdBkoGgZQgBut257mfwX1e-bDdExlmcxdtRrSjCtWYPBlne6M=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Dan,

May be too late to reply. Sorry.

Based on our last communication, I wanted to share these points after reading https://payjoin.substack.com/p/serverless-payjoin-gets-its-wings so that other can also evaluate them:

1) I don't think NIP 4 has any security issues. Maybe privacy issues. Its just metadata leak which should be okay if a new npub is used every time users do payjoin. Message itself will remain secret because it's encrypted.
2) Backwards compatibility due to npub, relay etc. shared in payjoin URI as implemented by Kukks. Not sure how to fix this.
3) Relays have no incentive to anything malicious if multiple relays are used. Although I am still not clear what malicious activity can they do with encrypted messages.
4) IP address is an issues with lot of projects and this can be managed by users or wallet implementation with the use of RiseupVPN, Tor, i2p etc.
5) Random padding suggested by a few senior devs makes sense.

/dev/fd0

floppy disk guy

------- Original Message -------
On Monday, January 23rd, 2023 at 2:20 AM, Dan Gould via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Hi all,
> 
> I'm publishing a payjoin upgrade in response to a request from this list. The payjoin receiver no longer has to run a public server. They lean on a relay for the connection and share a symmetric-key for security rather than a TLS certificate or a Tor hidden service.
> 
> I think this work raises a greater problem which is that payjoin assumes synchronous communication while it?s an asynchronous world.
> 
> I added the full write-up in plain text below, though I recommend reading the gist for improved formatting and in order to benefit from future edits:
> https://gist.github.com/DanGould/243e418752fff760c9f6b23bba8a32f9
> 
> Best regards,
> Dan
> 
> 
> 
> Serverless Payjoin
> 
> 
> Receive surveillance-busting bitcoin transfers without hosting a secure endpoint
> 
> 
> 
> OVERVIEW
> 
> 
> Payjoin[1] solves the sole privacy problem left open in the bitcoin paper, that transactions with multiple inputs "necessarily reveal that their inputs were owned by the same owner."[2] Breaking that common-input ownership assumption requires contributions from multiple owners via interaction, namely hosting a server endpoint secured by a certificate on the receiving side. This problem has been singled out on this list as a barrier to greater payjoin adoption.[3]
> 
> Instead of a peer-hosted endpoint, this scheme weilds a TURN[4] relay for connectivity and symmetric cryptography for security. Without a replacement for secured networking, the relay could steal funds. Aside from a pre-shared secret and relayed networking, the protocol takes the same form as the existing BIP 78 payjoin spec.
> 
> 
> 
> BASIC SCHEME
> 
> 
> The recipient requests that the relay allocate them an endpoint at which they may be reached by UDP. Once allocated, they listen on it. They then generate a 256-bit key, psk. Out of band, they share a BIP 21[5] payjoin uri including their unique relay allocation endpoint in the pj query parameter and psk in a new psk query parameter.
> 
> The sender constructs their request containing an original PSBT as in BIP 78. Instead of sending it over TLS or Tor, they follow noise framework NNpsk0[6] pattern. They encrypt the request using psk alongside an ephemeral sender key and MAC. The resulting ciphertext ensures message secrecy and integrity when relayed to the recipient by the pj endpoint.
> 
> The pay-to-endpoint protocol proceeds to produce a payjoin as in BIP 78 except that messages are secured by the noise NNpsk0 pattern rather than TLS or Tor.
> 
> 
> 
> IMPROVEMENTS
> 
> 
> HTTP/3
> 
> TURN defaults to UDP. In order to adhere to the BIP 78 protocol HTTP messaging, HTTP/3 should be used on top of TURN/UDP.
> Offline Asynchronous Payjoins
> 
> It may be possible for a relay to hold a requeust for an offline payjoin peer until that peer comes online. However, the BIP 78 spec recommends broadcasting request PSBTs in the case of an offline counterparty. Doing so exposes a na?ve, surveillance-vulnerable transaction which payjoin intends to avoid. More research needs to be done before such a protocol can be recommended.
> 
> 
> Nostr
> 
> While a custom Nostr relay could in theory replace the TURN relay while sharing shnorr crypto with bitcoin, it would require another protocol to synchronize networking, since Nostr makes no assumptions about whether a peer is online or not, and a careful cryptography audit to secure. TURN and Noise are already well understood, tested, and have production library support across multiple popular languages and other bitcoin-related projects. Noise even has tooling for formal verification. Nostr relays may prove more likely to allow public access and more robust if we figure out async payjoin, however.
> 
> 
> 
> NOTEWORTHY DETAILS
> 
> 
> Attack vectors
> 
> Since TURN relays can be used for any kind of internet traffic they are vulnerable to the tragedy of the commons. Relay operators may impose authentication requirements for endpoint allocation provisions.
> 
> Since psk is a symmetric key, the first message containing the sender's original PSBT does not have forward secrecy.
> 
> 
> Network Privacy
> 
> Peers will only see the IP address of the TURN relay but not their peer's. TURN relays may be made available via Tor hidden service in addition to IP to allow either of the peers to protect their IP with Tor without forcing the other to use it too.
> 
> 
> 
> IMPLEMENTATION
> 
> 
> I've published working proof of concept sender, receiver clients and relay code in rust[7]
> 
> 
> 
> ACKNOWLEDGEMENTS
> 
> 
> Deepest gratitude to Ethan Heilman for sitting down with me to help get to the bottom of the requirements of this problem, to Ruben Somsen for this slick format, and to all those engaged in defending the right to privacy.
> 
> 
> 
> REFERENCES
> 
> 
> [1] BIP 78 A Simple Payjoin Proposal, Nicolas Doier:
> https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki
> 
> [2] Bitcoin: A Peer-to-Peer Electronic Cash System, Satoshi Nakamoto:
> https://chaincase.app/bitcoin.pdf
> 
> [3] [bitcoin-dev] PayJoin adoption, Craig Raw:
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-January/018358.html
> 
> [4] RFC 5766: Traversal Using Relays around NAT (TURN):
> https://www.rfc-editor.org/rfc/rfc5766
> 
> [5] BIP 21 URI Scheme, Nils Schneider, Matt Corallo:
> https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki
> 
> [6] Noise Explorer: NNpsk0:
> https://noiseexplorer.com/patterns/NNpsk0
> 
> [7] Serverless PayJoin PoC:
> https://github.com/chaincase-app/payjoin/pull/21
> 
> 
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Sun, 20 Aug 2023 17:46:01 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] BIP-119 UASF
Message-ID:
	<Sd0HdkW021oxOx3N5nLA-gJr6bgGEZUNXbrGSmwJMXntc6nVWC5Hackx3C5PTQMfP-B1vwC9A14cDlkCu3K986oHD57ivIAxxdTC8JInZgY=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Bitcoin Developers,

Note: This email is inspired from https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-March/018538.html written by Chris Belcher

Lets compare all covenant proposals:

https://docs.google.com/spreadsheets/d/1YL5ttNb6-SHS6-C8-1tHwao1_19zNQ-31YWPAHDZgfo/edit#gid=0

Why general and recursive covenants are controversial:

https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-February/019976.html

Why I prefer CTV over APO?

- LN symmetry can be achieved with CSFS later if there is really a demand apart from twitter
- CTV improves LN
- CTV does not change how sighash works still we get covenants
- Less bytes
- More tooling
- Not recursive
- Not limited to taproot
- Other differences

MASF or speedy trial allows miners to coordinate and signal "readiness". This is misunderstood by lot of users as miners can always refuse to follow new consensus rules even after signaling or economics nodes can reject blocks with new consensus rules later.

Instead of doing this we could do a UASF in which things are clear that economic nodes enforce consensus rules and miners or majority of miners at this point wont go against bitcoin communities including nodes with some economic activity.

If there is a positive feedback, we could work on building UASF client for activation and bitcoin core can follow.

/dev/fd0

floppy disk guy


------------------------------

Message: 3
Date: Sat, 19 Aug 2023 14:58:15 -0400
From: ryan@breen.xyz
To: Ruben Somsen <rsomsen@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Sentinel Chains: A Novel Two-Way Peg
Message-ID: <2BFA7EE8-2E0E-45A3-AC11-8E57F99EC775@breen.xyz>
Content-Type: text/plain; charset="utf-8"

Thank you for the feedback, Ruben. I have a question.

Could you please clarify what qualifies as a fraud proof in this concept? As I envision it, there is no cryptographic proof involved at all.

In the context of a Sentinel chain, the sidechain's full nodes monitor Bitcoin mempools and blocks for withdrawals that violate the rules of the sidechain's consensus (such as thefts or incorrect balances). When the sidechain's full nodes detect an invalid withdrawal on Bitcoin, they publish a signed attestation to a public broadcast network (Nostr in this case). Participating Bitcoin full nodes and miners monitor the network for these attestations and subsequently reject the offending transactions. The process doesn't involve the presentation of proof because it's a distributed trust relationship.

While Bitcoin full nodes could decide to operate their own sidechain nodes, we aim not to make this a requirement (addressing the long-standing sidechain dilemma). Bitcoin full nodes and miners wishing to participate can instead choose a distributed trust network comprising operators of sidechain full nodes that they trust. For instance, if they decide to follow 100 well-respected sidechain node operators, they might collectively agree that if 75 of them issue an attestation indicating that a transaction violates sidechain withdrawal rules, then that transaction should be deemed invalid by their node. Withdrawals are assumed valid if no public attestations are present.

Furthermore, I'm uncertain about what potential data availability issue that might arise from this. Since there are no alterations to Bitcoin Core's validation logic, when a full node operator starts a new node from the genesis block, they will validate the proof of work of the longest chain and remain blissfully unaware that the transactions within the blocks are even associated with a sidechain.

> On Aug 19, 2023, at 10:35 AM, Ruben Somsen <rsomsen@gmail.com> wrote:
> 
> Hi Ryan,
> 
> Thanks for taking the time to write a proposal. As is often the case, these ideas aren't actually as novel as you might think. What you describe here is known as "fraud proofs". The crucial problem it doesn't address is "data availability".
> 
> The general idea behind fraud proofs is that if you commit to every computational step (note Bitcoin currently doesn't, but could), anyone can succinctly reveal erroneous steps (e.g. 1+1=3), thus convincing everyone the state transition (i.e. block) is invalid. This works if a bunch of people have all the data and are willing to construct and spread the fraud proofs, but what if nobody has the data?
> 
> When someone claims data is unavailable, the only way to verify this claim is by downloading the data. You can't just ban this peer for false claims either, since the data might have actually been unavailable when the claim was made but then became available. In essence this means malicious peers can cause you to download all data, meaning you effectively haven't saved any bandwidth.
> 
> It should be noted that fraud proofs could still reduce the need for computation (i.e. you download all data, but only verify the parts for which you receive fraud notifications), so it can still provide some form of scaling.
> 
> As a bit of history, fraud proofs were actually briefly considered for inclusion into segwit, but were abandoned due to the data availability issue: https://bitcoincore.org/en/2016/01/26/segwit-benefits/#update-2016-10-19
> 
> And finally, there is a way to address the data availability issue, which I describe here (PoW fraud proofs/softchains, though note I am currently of the opinion it's better used for low-bandwidth mainchain nodes instead of for sidechains): https://gist.github.com/RubenSomsen/7ecf7f13dc2496aa7eed8815a02f13d1
> 
> In theory you can also do data availability sampling through the use of erasure codes, but that gets very complex and brittle.
> 
> Hope this helps.
> 
> Cheers,
> Ruben
> 
> On Sat, Aug 19, 2023 at 4:29?PM Ryan Breen via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org <mailto:bitcoin-dev@lists.linuxfoundation.org>> wrote:
>> Recent discussions on social media regarding drivechains have prompted me to consider the implementation of a two-way sidechain peg within the Bitcoin protocol. I would like to propose what I believe may be a novel solution to this issue.
>> 
>> I have previously written about here on my blog: https://ursus.camp/bitcoin/2023/08/10/sidechains.html
>> And here is the Stacker News discussion: https://stacker.news/items/222480
>> 
>> Nevertheless, I will hit the high points of the concept here:
>> 
>> The most challenging problem that BIP-300 aims to address is how to establish a two-way peg without involving a multisig federation and without requiring miners and full nodes to possess knowledge about the sidechain or run a sidechain node. This is, in fact, a very difficult nut to crack.
>> 
>> The method adopted by BIP-300 involves conducting sidechain withdrawals directly through the miners. To prevent miners from engaging in theft, the proposal mandates a three-month period for peg-outs, during which all miners vote on the peg-out. The intention here is to allow the community to respond in the event of an incorrect peg-out or theft. The miners are expected to be responsive to community pressure and make the correct decisions. To streamline this process of social consensus, withdrawals are grouped into one large bundle per three month period.
>> 
>> Despite criticisms of this proposal, I find it to be a viable and likely effective solution. After all, Bitcoin's underlying mechanism is fundamentally rooted in social consensus, with the only question being the extent of automation. Nonetheless, I believe we now possess tools that can improve this process, leading to the concept of Sentinel chains.
>> 
>> The core idea is that sidechain nodes function as Sentinels, notifying full nodes of thefts via a secondary network. These sidechain nodes monitor the current state of Bitcoin blocks and mempool transactions, actively searching for peg-outs that contravene sidechain consensus in order to steal funds. They transmit invalid transactions or blocks to public Nostr servers. Bitcoin full nodes wishing to partake in sidechain consensus can run a small daemon alongside Bitcoin Core. This daemon can monitor public Nostr nodes for messages about invalid transactions and then instruct Bitcoin Core, via RPC calls, to ignore and not forward those invalid transactions.
>> 
>> Full nodes can choose any group of individuals or organizations to receive updates from Nostr. For instance, a full node might choose to trust a collective of 100 sidechain nodes consisting of a mix of prominent companies and individuals in the sidechain's sphere. Rather than relying on a single trusted group, full nodes form their own decentralized web of trust.
>> 
>> This reverses the conventional model of two-way pegged sidechains. Instead of requiring nodes to monitor sidechains, sidechains now monitor nodes. In this sense, it is akin to drivechains, with the difference being that peg-outs could be instantaneous and individual, without the need for the three-month gradual social consensus. Furthermore, a single daemon can be configured to monitor notifications from any number of Sentinel chains, rendering this solution highly scalable for numerous sidechains.
>> 
>> In summary, drivechains:
>> 
>> - Require an initial consensus soft fork
>> - Treat each new sidechain as a miner-activated soft fork (easier to deploy but more centralized)
>> - Feature withdrawals occurring in three-month periods
>> - Involve withdrawals in bundles
>> - Exclude Bitcoin full nodes from participation in sidechain consensus
>> - Are currently production-ready
>> 
>> Sentinel chains:
>> 
>> - Require no initial soft fork of any kind
>> - Permit each new sidechain to be miner-activated OR user-activated (more challenging to deploy but more decentralized)
>> - Allow instantaneous withdrawals
>> - Facilitate individual withdrawals
>> - Enable Bitcoin full nodes to engage in consensus
>> - Are only at the concept stage
>> 
>> Sentinel chains could potentially offer substantial advantages over other forms of two-way pegs, primarily in terms of speed and efficiency of consensus. Moreover, they align more closely with Bitcoin's principles by ensuring that power remains within the realm of full nodes. Lastly, they shield Core-only users from potential bug consequences stemming from consensus changes directly implemented in Bitcoin Core, possibly fulfilling the long-awaited promise of a fully opt-in soft fork.
>> 
>> 
>> Ryan Breen
>> Twitter: ursuscamp
>> Email: ryan @ breen.xyz <http://breen.xyz/>
>> Web: https://ursus.camp <https://ursus.camp/>
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org <mailto:bitcoin-dev@lists.linuxfoundation.org>
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev

-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230819/31ff4b51/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 39
*******************************************
