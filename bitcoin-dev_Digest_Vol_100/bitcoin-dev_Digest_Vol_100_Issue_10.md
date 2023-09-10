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

   1. Re: [Lightning-dev] Scaling Lightning With Simple	Covenants
      (Anthony Towns)
   2. Re: Parameters in BIP21 URIs (Lucas Ontivero)
   3. Formosa - Expansion on BIP39 as proposed BIP (yurisvb@pm.me)


----------------------------------------------------------------------

Message: 1
Date: Mon, 11 Sep 2023 10:56:40 +1000
From: Anthony Towns <aj@erisian.com.au>
To: jlspc <jlspc@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Scaling Lightning With
	Simple	Covenants
Message-ID: <ZP5lyA9CCUf138ve@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Fri, Sep 08, 2023 at 06:54:46PM +0000, jlspc via Lightning-dev wrote:
> TL;DR
> =====

I haven't really digested this, but I think there's a trust vs
capital-efficiency tradeoff here that's worth extracting.

Suppose you have a single UTXO, that's claimable by "B" at time T+L,
but at time T that UTXO holds funds belonging not only to B, but also
millions of casual users, C_1..C_1000000. If B cheats (eg by not signing
any further lightning updates between now and time T+L), then each
casual user needs to drop their channel to the chain, or else lose all
their funds. (Passive rollovers doesn't change this -- it just moves the
responsibility for dropping the channel to the chain to some other
participant)

That then faces the "thundering herd" problem -- instead of the single
one-in/one-out tx that we expected when B is doing the right thing,
we're instead seeing between 1M and 2M on-chain txs as everyone recovers
their funds (the number of casual users multiplied by some factor that
depends on how many outputs each internal tx has).

But whether an additional couple of million txs is a problem depends
on how long a timeframe they're spread over -- if it's a day or two,
then it might simply be impossible; if it's over a year or more, it
may not even be noticable; if it's somewhere in between, it might just
mean you're paying a modest amount in additional fees than you'd have
normally expected.

Suppose that casual users have a factor in mind, eg "If worst comes to
worst, and everyone decides to exit at the same time I do, I want to be
sure that only generates 100 extra transactions per block if everyone
wants to recover their funds prior to B being able to steal everything".

Then in that case, they can calculate along the following lines: 1M users
with 2-outputs per internal tx means 2M transactions, divide that by 100
gives 20k blocks, at 144 blocks per day, that's 5 months. Therefore,
I'm going to ensure all my funds are rolled over to a new utxo while
there's at least 5 months left on the timeout.

That lowers B's capital efficiency -- if all the causal users follow
that policy, then B is going to own all the funds in Fx for five whole
months before it can access them. So each utxo here has its total
lifetime (L) actually split into two phases: an active lifetime LA of
some period, and an inactive lifetime of LI=5 months, which would have
been used by everyone to recover their funds if B had attempted to block
normal rollover. The capital efficiency is then reduced by a factor of
1/(1+LA/LI). (LI is dependent on the number of users, their willingness
to pay high fees to recover their funds, and global blockchain capacity,
LA is L-LI, L is your choice)

Note that casual users can't easily reduce their LI timeout just by
having the provider split them into different utxos -- if the provider
cheats/fails, that's almost certainly a correlated across all their
utxos, and all the participants across each of those utxos will need
to drop to the chain to preserve their funds, each competing with each
other for confirmation.

Also, if different providers collude, they can cause problems: if you
expected 2M transactions over five months due to one provider failing,
that's one thing; but if a dozen providers fail simultaneously, then that
balloons up to perhaps 24M txs over the same five months, or perhaps 25%
of every block, which may be quite a different matter.

Ignoring that caveat, what do numbers here look like? If you're a provider
who issues a new utxo every week (so new customers can join without too
much delay), have a million casual users as customers, and target LA=16
weeks (~3.5 months), so users don't need to rollover too frequently,
and each user has a balanced channel with $2000 of their own funds,
and $2000 of your funds, so they can both pay and be paid, then your
utxos might look like:

   active_1 through active_16: 62,500 users each; $250M balance each
   inactive_17 through inactive_35: $250M balance each, all your funds,
      waiting for timeout to be usable

That's:
  * $2B of user funds
  * $2B of your funds in active channels
  * $4.5B of your funds locked up, waiting for timeout

In that case, only 30% of the $6.5B worth of working capital that you've
dedicated to lightning is actually available for routing.

Optimising that formula by making LA as large as possible doesn't
necessarily work -- if a casual user spends all their funds and
disappears prior to the active lifetime running out, then those
funds can't be easily spent by B until the total lifetime runs out,
so depending on how persistent your casual users are, I think that's
another way of ending up with your capital locked up unproductively.
(There are probably ways around this with additional complexity: eg,
you could peer with a dedicated node, and have the timeout path be
"you+them+timeout", so that while you could steal from casual users who
don't rollover, you can't steal from your dedicated peer, so that $4.5B
could be rolled into a channel with them, and used for routing)

You could perhaps also vary the timeout at different layers of the
internal tree -- if you have 500k users with a $10 balance, and give them
a timeout of 16 weeks, and give the remaining 500k with an average $2000
balance a timeout of 26 weeks, then each will calculate LI=10 weeks,
and the $10 folks will rollover at 1.5 months, and the remainder will
rollover at about 4 months; but your idle balance will be $5M for 20
weeks plus $1B for 10 weeks, rather than $1.005B for 20 weeks.

Anyway, I think that's an interesting way of capturing a big concern
with this sort of approach (namely, "what happens if the nice, scalable
path doesn't work, and we have to dump *LOTS* of stuff onchain") in a
measurable way.

Cheers,
aj



------------------------------

Message: 2
Date: Fri, 8 Sep 2023 15:07:11 +0000
From: Lucas Ontivero <lucasontivero@gmail.com>
To: kiminuo <kiminuo@protonmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Parameters in BIP21 URIs
Message-ID:
	<CALHvQn1bt_TP17b3trEH7rE8TDreKGHgduQx3s0gxSYnMcKTqQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Kiminuo, this was discussed here: https://github.com/bitcoin/bips/pull/49


On Fri, Sep 8, 2023 at 2:39?PM kiminuo via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> [Formatted version of this post is here:
> https://gist.github.com/kiminuo/cc2f19a4c5319e439fc7be8cbe5a39f9]
>
> Hi all,
>
> BIP 21 [https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki]
> defines a URI scheme for making Bitcoin payments and the purpose of the URI
> scheme is to enable users to easily make payments by simply clicking links
> on webpages or scanning QR Codes. An example of a BIP21 URI is:
>
>
> bitcoin:bc1qd4fxq8y8c7qh76gfnvl7amuhag3z27uw0w9f8p?amount=0.004&label=Kiminuo&message=Donation
>
> Now to make it easier, these URIs are typically clickable. Bitcoin wallets
> register the "bitcoin" URI scheme so that a BIP21 URI is parsed and data
> are pre-filled in a form to send your bitcoin to a recipient. Notably,
> wallets do not send your bitcoin once you click a BIP21 URI, there is still
> a confirmation step that requires user's attention. Very similar experience
> is with a QR code that encodes a BIP21 URI where one just scans a QR code
> and data is, again, pre-filled in a wallet's UI for your convenience.
>
> While working on Wasabi's BIP21 implementation I noticed that based on the
> BIP21 grammar [
> https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki#abnf-grammar],
> it is actually allowed to specify URI parameters multiple times. This means
> that the following URI is actually valid:
>
> bitcoin:bc1qd4fxq8y8c7qh76gfnvl7amuhag3z27uw0w9f8p?amount=0.004&label=Kiminuo&message=Donation&amount=1.004
> (note that the 'amount' parameter is specified twice)
>
> Bitcoin Core implements "the last value wins" behavior[^3] so amount=1.004
> will be taken into account and not "amount=0.004"[^4]. However, in general,
> the fact that the same parameter can be specified multiple times can lead
> to a confusion for users and developers[^1][^2]. In the worst case, it
> might be exploited by some social engineering attempts by attempting to
> craft a 'clever' BIP21 URI and exploting behavior of a particular wallet
> software. For the record, I'm not aware that it actually happens, so this
> is rather a concern.
>
> The main question of this post is: Is it useful to allow specifying BIP21
> parameters multiple times or is it rather harmful?
>
> Regards,
> K.
>
> [^1]: https://github.com/JoinMarket-Org/joinmarket-clientserver/pull/1510
> [^2]:
> https://github.com/MetacoSA/NBitcoin/blob/93ef4532b9f2ea52b2c910266eeb6684f3bd25de/NBitcoin/Payment/BitcoinUrlBuilder.cs#L74-L78
> [^3]: I added a test to that effect in
> https://github.com/bitcoin/bitcoin/pull/27928/files, see
> https://github.com/bitcoin/bitcoin/blob/83719146047947e588aa0c7b5eee02f44884553d/src/qt/test/uritests.cpp#L68-L73
> .
> [^4]: You can test your wallet's behavior by scanning the last image here
> https://github.com/zkSNACKs/WalletWasabi/pull/10578#issue-1687564404 (or
> directly
> https://user-images.githubusercontent.com/58662979/265389405-16893ce8-7c19-4262-bb60-5fd711336685.png
> ).
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230908/0e44a479/attachment.html>

------------------------------

Message: 3
Date: Sun, 10 Sep 2023 15:49:27 +0000
From: yurisvb@pm.me
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, "luke_bipeditor@dashjr.org"
	<luke_bipeditor@dashjr.org>, "karljohan-alm@garage.co.jp"
	<karljohan-alm@garage.co.jp>
Subject: [bitcoin-dev] Formosa - Expansion on BIP39 as proposed BIP
Message-ID:
	<F4cs-RJRQYBXhjoS9fc_cUc93yLrkQS5DNQAeFRHrLEQ5bScCjKSnaqN-IcXb16fxqO053muqFCx8_GzzKN5XCGCIHD9Ir1_baI5voKYfOo=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Dear Mr. Dash Jr,?Kalle Alm and other members of Bitcoin dev mailing list,

Upon receiving several?constructive, technical, generous?pieces of feedback, and a few more months of continued development, I feel now ready to formally file Formosa, my proposed expansion of BIP39 changing from words to themed sentences, as Bitcoin Improvement Proposal.


-   Documentation according to BIP2:?https://github.com/Yuri-SVB/formosa/blob/master/bip.mediawiki
-   Additional references:?https://linktr.ee/formosat3


In advance, thank you for the time, attention and dedication of everyone involved!
Faithfully yours, Yuri S Villas Boas
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230910/53ebdff3/attachment.html>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230910/53ebdff3/attachment.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230910/53ebdff3/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 10
********************************************
