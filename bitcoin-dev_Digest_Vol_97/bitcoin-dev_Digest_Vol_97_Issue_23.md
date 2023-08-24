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

   1. Re: Standardisation of an unstructured taproot annex (Joost Jager)
   2. Re: Standardisation of an unstructured taproot annex (Joost Jager)
   3. CivKit Node v0.0.1 release - "Sic itur ad astra" (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Tue, 20 Jun 2023 14:30:19 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV-PbDbi_9=z16yq7+cxhOzrfqvbN8=t-Kd3eWx_M5wSoA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi all,

On Sat, Jun 10, 2023 at 9:43?AM Joost Jager <joost.jager@gmail.com> wrote:

> However, the primary advantage I see in the annex is that its data isn't
> included in the calculation of the txid or a potential parent commit
> transaction's txid (for inscriptions). I've explained this at [1]. This
> feature makes the annex a powerful tool for applications that would ideally
> use covenants.
>
> The most critical application in this category, for me, involves
> time-locked vaults. Given the positive reception to proposals such as
> OP_VAULT [2], I don't think I'm alone in this belief. OP_VAULT is probably
> a bit further out, but pre-signed transactions signed using an ephemeral
> key can fill the gap and improve the safeguarding of Bitcoin in the short
> term.
>
> Backing up the ephemeral signatures of the pre-signed transactions on the
> blockchain itself is an excellent way to ensure that the vault can always
> be 'opened'. However, without the annex, this is not as safe as it could
> be. Due to the described circular reference problem, the vault creation and
> signature backup can't be executed in one atomic operation. For example,
> you can store the backup in a child commit/reveal transaction set, but the
> vault itself can be confirmed independently and the backup may never
> confirm. If you create a vault and lose the ephemeral signatures, the funds
> will be lost.
>
> This use case for the annex has been labeled 'speculative' elsewhere. To
> me, every use case appears speculative at this point because the annex
> isn't available. However, if you believe that time-locked vaults are
> important for Bitcoin and also acknowledge that soft forks, such as the one
> required for OP_VAULT, aren't easy to implement, I'd argue that the
> intermediate solution described above is very relevant.
>

To support this use case of the taproot annex, I've create a simple demo
application here: https://github.com/joostjager/annex-covenants

This demo shows how a coin can be spent to a special address from which it
can - at a later stage - only move to a pre-defined final destination. It
makes use of the annex to store the ephemeral signature for the presigned
transaction so that the coin cannot get lost. This is assuming that nodes
do not prune witness data en masse and also that the destination address
itself is known.

The application may not be the most practically useful, but more advanced
covenants such as time-locked vaults can be implemented similarly.

Hopefully this further raises awareness of the on-chain ephemeral signature
backup functionality that the annex uniquely enables.

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230620/d507ce76/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 20 Jun 2023 14:50:47 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Greg Sanders
	<gsanders87@gmail.com>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV9K351SG3FTLF0xxC-y5KV4CD6upiQoir+a3p2KBe4fDA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Antoine,

On Sun, Jun 18, 2023 at 10:32?PM Antoine Riard <antoine.riard@gmail.com>
wrote:

> > * Opt-in annex (every input must commit to an annex even if its is
> empty) -> make sure existing multi-party protocols remain unaffected
>
> By requiring every input to commit to an annex even if it is empty, do you
> mean rejecting a transaction where the minimal annex with its 0x50 tag is
> absent ?
>

No what I meant, and what was mentioned by Greg in a previous email, is
that either none of the inputs have an annex, or all of them have one.

So if you're part of a multi-party transaction and you don't commit to an
annex, you can be sure that no version of that tx will appear where another
signer surprises you with a potentially large annex.

For future protocols that rely on the annex, everyone would need to opt-in
by committing to an annex (which can be empty just to signal opt-in).

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230620/60810c0a/attachment-0001.html>

------------------------------

Message: 3
Date: Wed, 21 Jun 2023 09:14:05 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] CivKit Node v0.0.1 release - "Sic itur ad
	astra"
Message-ID:
	<CALZpt+EGfF_=0voijO3=D0fzs2+uSC5ZGf=F1HmKoDiVUw43KQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Bitcoin Devs,

Proud to announce the first release of CivKit Node, a basic Nostr relay
with additional features to have a functional peer-to-peer market board,
written in Rust [0]. This is a very raw release as since we published the
paper back in April, we've been reached out by a bunch of folks asking how
they could contribute by code, or start to integrate CivKit in their Nostr
and Lightning peer-to-peer market clients [1].

Current release is CLI-only, just implementing basic NIP 01 support and is
full of bugs and todos, has not been tested on a lot of platforms and still
works as a local host for a lot of things [2]. There is a sample Nostr
client binary joined for deployment and testing purposes and an utility
binary to manage the node with a gRPC interface. Such an interface should
lay the groundwork to build one or more GUI applications on top, as it's a
recurring and consistent request from the community.

There is an experimental integration with BOLT8 Noise transport (thanks to
LDK), where one can connect to another CivKit Node has a peer, Idea is to
unify the communication infrastructure between Nostr and Lightning, and as
such have a single market of p2p service providers (watchtower, state
backup, boards) benefiting from network law effect. Beyond sharing all the
work between Lightning and Nostr ecosystem in terms of spamming
mitigations, careful crypto engineering (e.g onion routing) and
privacy-preserving monetary credentials [3].

With this released out, I think we'll go for sound onion routing support,
BOLT12 offers, the set of fundamental NIPs like NIP-09, NIP-16, NIP-33 and
others, and integration with a notary protocol (e.g Mainstay). Still, we
would like to listen to our users and we'll plumber features in the
function of relevant feedback collected from the community. One key lesson
from years contributing on LDK, we do not want to stay in a "purist
developer" ivory tower to avoid hard-to-integrate APIs, and make the
"product management" of the project owned by the community to ensure we're
building for the real-world of unstable and constrained mobile clients.

Once we have communication infrastructure and hopefully credentials
framework working, I think we'll start to have more serious development of
the CivKit functionaries services themselves (e.g market bulletin boards,
rank proof servers and moderation oracles in the paper parlance). Though
again, if folks want to start more custom services on top of CivKit Node,
we'll see what we can do, there is a brave new world to explore with Nostr
and Lightning maturation.

For the historical note, peer-to-peer market features were present in
Bitcoin Core circa 2010 (in fact before the ref client was dubbed Core).
Those features were removed by commit 5253d1ab "strip out unfinished
product, review and market stuff" by Satoshi [4]. Retrospectively, it was a
good insight as Core has evolved as a complex beast enough and careful
layerization is one of the best learning from the 50 years of Internet
history. Still, censorship-resistant and large-scale peer-to-peer markets
sounds still one of the missing blocks of the Bitcoin protocol stack.

Looking forward to growing the Bitcoin and Lightning internal economies by
an order of magnitude or two with the CivKit Node, if the kharma is with us.

All works are released under MIT/Apache licenses and we aim to bind to the
best open-source development standards as set by Bitcoin Core and the Linux
kernel communities and we're welcoming anyone strongly willing to build
with passion and love.

I think for the future, we'll do the announcement on its own communication
channel, whatever a new mailing list, or something experimental on top of
Nostr groups, Still, if we innove in terms of cryptography we're aiming to
have things standardized under BIPs.

"Sic itur ad astra" -
Block 000000000000000000053fd09a45f48e747f281122021edc2f7e97efcdd66248

Cheers,
Antoine

[0] https://github.com/civkit/civkit-node
[1]
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021556.html
[2] Of course, there are gazillins of things to implement, please open an
issue on the repository directly rather to yell something doesn't work.
[3]
https://lists.linuxfoundation.org/pipermail/lightning-dev/2023-May/003964.html
[4] https://github.com/bitcoin/bitcoin/commit/5253d1ab
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230621/7e720924/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 23
*******************************************
