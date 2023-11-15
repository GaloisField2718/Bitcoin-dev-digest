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

   1. Re: Future of the bitcoin-dev mailing list (Ali Sherief)
   2. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Peter Todd)
   3. Re: Future of the bitcoin-dev mailing list (Overthefalls)


----------------------------------------------------------------------

Message: 1
Date: Tue, 14 Nov 2023 12:32:50 +0000
From: Ali Sherief <ali@notatether.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID:
	<dYhdxKm2HRMk3Z3Qc5rxgxIwI_IMdSMW5pvXEEdIkrnQMRuK7As-O-t5CR3D6W1FHMyA62IA3qrnxltx3D-RMln5KWdz3CPYFWUzFiriGCs=@notatether.com>
	
Content-Type: text/plain; charset=utf-8

I find Google Groups especially repugnant not not only because what has already been mentioned, but Google Groups has a quite clunky and annoying user interface that makes it difficult for me to find anything or interest in there.

Usenet was migrated to Google Groups for some reason, and it's very difficult to search for anything of particular interest using that site.

Not to mention that Google Groups also contains a larger amount of spam (w.r.t value), so arguably the moderation burden will be higher.

It is necessary to try to find a way to keep the discussion on a mail server, since a migration off of it will render many users' email clients useless for this purpose.

- Ali

> On Mon, 13 Nov 2023 18:51:26 +0000, alicexbt <alicexbt@protonmail.com> wrote:
>
> Hi Overthefalls,
>
> +1
>
> Using google for bitcoin mailing list is not good. It feels embarrassing that some developers that built and maintained the only decentralized network used to settle uncensored payments and some of them even working on nostr, can't build their own mailing list which is better than present mailing list. I have some ideas but it seems the influential developers have already decided and wont accept anything.
>
> Nostr can be used to build a mailing list which also allows anyone to send emails apart from publishing events from different clients. We just need a new NIP so that nostr relays understand its a different event. There can be multiple front end with different levels of moderation to hide some emails and ultimately one will be used the most. It can use multiple relays and relays share some information in NIP 11 which can include an email address.
>
> /dev/fd0
> floppy disk guy
>
> Sent with Proton Mail secure email.
>
> On Monday, November 13th, 2023 at 8:35 PM, Overthefalls via bitcoin-dev bitcoin-dev@lists.linuxfoundation.org wrote:
>
> > On Tue, 2023-11-07 at 09:37 -0600, Bryan Bishop via bitcoin-dev wrote:
> >
> > > Google Groups is another interesting option,
> >
> > I don't think I'm the only person on this list that is strongly opposed to using google for anything. They are too big and they have their hand in everything, and their eyes (and analytics) on everything.
> >
> > I remember when there were virtually no gmail email addresses that posted to this list. Suddenly in 2020 or 2021, we had an influx of gmail subscribers and posters. That didn't escape me then and it is not lost on me now.
> >
> > Email is great for public discussion for many reasons. The fact that everyone gets a copy of the data, there is no single central authority that can edit emails once they have been sent out. Anyone can archive email messages, they can generally store or publish the data anywhere they like. That is not the case with web forum content.
> >
> > I like the lightning anti-spam fee idea. That would encourage me to finally adopt lightning, and it would, I'm sure, produce some interesting results for the list.
> >
> > I don't think email should be out of the question. Does anyone besides kanzure@gmail.com think that sticking with email is out of the question?
> >
> > Let's do what's necessary to stick with email.


------------------------------

Message: 2
Date: Tue, 14 Nov 2023 19:50:04 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZVPPbNdmPxahOGqA@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Mon, Nov 13, 2023 at 02:18:16AM +0000, Antoine Riard wrote:
> Your two latest mails.
> 
> > The problem that OP_Expire aims to solve is the fact that Carol could
> prevent
> > Bob from learning about the preimage in time, while still getting a
> chance to
> > use the preimage herself. OP_Expire thoroughly solves that problem by
> ensuring
> > that the preimage is either broadcast in the blockchain in a timely
> fashion, or
> > becomes useless.
> 
> I respectfully disagree - There is a more general underlying issue for
> outdated states in multi-party off-chain constructions, where any "revoked"
> or "updated" consensus-valid state can be used to jam the latest off-chain
> agreed-on, through techniques like replacement cycling or pinning.

No, that's not a general underlying issue. You've found two separate issues.

Furthermore, revoked states are clearly different than HTLCs: they're
fraudulent, and thus in punishment-using protocols they are always associated
with high risks of loss if they do in fact get detected or mined. There's
probably tweaks we can do to improve this security. But the general principle
there is certainly true.

> > My suggestion of pre-signing RBF replacements, without anchor outputs,
> and with
> > all outputs rendered unspendable with 1 CSV, is clearly superior: there
> are
> > zero degrees of freedom to the attacker, other than the possibility of
> > increasing the fee paid or broadcasting a revoked commitment. The latter
> of
> > course risks the other party punishing the fraud.
> 
> Assuming the max RBF replacement is pre-signed at 200 sats / vb, with
> commitment transaction of ~268 vbytes and at least one second-stage HTLC
> transaction of ~175 vbytes including witness size, a channel counterparty
> must keep at worst a fee-bumping reserve of 35 268 sats, whatever payment
> value.

For a lightning channel to be economical at all in a general routing
environment, the highest likely fee has to be small enough for it to represent
a small percentage of the total value tied up in the Lightning channel. Tying
up a small percentage of the overall capacity for future fee usage is not a
significant expense.

> As of today, any payment under $13 has to become trimmed HTLCs.
> Trimmed HTLCs are coming with their own wormhole of issues, notably making
> them a target to be stolen by low-hashrate capabilities attackers [0].
> 
> [0]
> https://lists.linuxfoundation.org/pipermail/lightning-dev/2020-May/002714.html

That attack doesn't make sense. HTLCs go to fees at a certain feerate. In a
normal environment where there is a constant supply of fee paying transactions,
the profit for the miner is not the total HTLC value, but the increase in
feerate compared to the transactions they had to give up to mine the commitment
transaction.

Second, it's obvious that the total trimmed HTLCs should be limited to what
would be a reasonable transaction fee. A situation where you have 80% of the
channel value going to fees due to a bunch of small HTLCs is obviously
ridiculous, and to the extent that existing implementations have this issue,
should be fixed.

For RBF fee bumping, obviously you can take the increased channel fees from the
party choosing to broadcast the commitment transaction.

> > This does have the practical problem that a set of refund transactions
> will
> > also need to be signed for each fee variant. But, eg, signing 10x of each
> isn't
> > so burdensome. And in the future that problem could be avoided with
> > SIGHASH_NOINPUT, or replacing the pre-signed refund transaction mechanism
> with
> > a covenant.
> 
> I think if you wish to be safe against fees griefing games between
> counterparties, both counterparties have to maintain their own fee-bumping
> reserves, which make channel usage less capital efficient, rather than
> being drawn from a common reserve.

Yes, obviously. But as I said above, it just doesn't make sense for channels to
be in a situation where closing them costs a significant % of the channel value
in fees, so we're not changing the status quo much.

> > Using RBF rather than CPFP with package relay also has the advantage of
> being
> > more efficient, as no blockspace needs to be consumed by the anchor
> outputs or
> > transactions spending them. Of course, there are special circumstances
> where
> > BIP125 rules can cause CPFP to be cheaper. But we can easily fix that, eg
> by
> > reducing the replacement relay fee, or by delta-encoding transaction
> updates.
> 
> It is left as an exercise to the reader how to break the RBF approach for
> LN channels as proposed.

Do you have a concrete attack?

> > As SIGHASH_NOINPUT is desirable for LN-Symmetry, a softfork containing
> both it
> > and OP_Expire could make sense.
> 
> I think there is one obvious issue of pre-signing RBF replacements combined
> with LN-symmetry, namely every state has to pre-commit to fee values
> attached and such states might spend each other in chain. So now you would
> need `max-rbf-replacement` *  `max-theoretical-number-of-states` of
> fee-bumping reserves unless you can pipe fee value with some covenant
> magic, I think.

No, you are missing the point. RBF replacements can use SIGHASH_NOINPUT to sign
HTLC refund transactions, removing the need for a set of different HTLC refund
transactions for each different feerate of the commitment transaction.

I'm making no comment on how to do RBF replacements with LN-Symmetry, which I
consider to be a broken idea in non-trusted situations anyway. Removing justice
from Lightning is always going to be hopelessly insecure when you can't at
least somewhat trust your counterparty. If your usage of LN-Symmetry is
sufficiently secure, you probably don't have to worry about them playing fee
games with you either.
 
-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231114/2d755c3e/attachment-0001.sig>

------------------------------

Message: 3
Date: Tue, 14 Nov 2023 09:32:37 -0600
From: Overthefalls <overthefalls@opengroupware.ch>
To: alicexbt <alicexbt@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID:
	<d8c894f8bafc0070d49b235e8759533903a6c6e1.camel@opengroupware.ch>
Content-Type: text/plain; charset="utf-8"

Hi floppy disk guy, thanks for prompting me to look closer at Nostr,
it's very interesting. 

I hope that whatever solution is chosen doesn't involve handing power
over to a centralized entity that wants collect as much information on
every living person as possible, and lock everyone and everything into
using it's services forever.

On Mon, 2023-11-13 at 18:51 +0000, alicexbt wrote:
> Hi Overthefalls,
> 
> 
> +1
> 
> 
> Using google for bitcoin mailing list is not good. It feels
> embarrassing that some developers that built and maintained the only
> decentralized network used to settle uncensored payments and some of
> them even working on nostr, can't build their own mailing list which
> is better than present mailing list. I have some ideas but it seems
> the influential developers have already decided and wont accept
> anything.
> 
> Nostr can be used to build a mailing list which also allows anyone to
> send emails apart from publishing events from different clients. We
> just need a new NIP so that nostr relays understand its a different
> event. There can be multiple front end with different levels of
> moderation to hide some emails and ultimately one will be used the
> most. It can use multiple relays and relays share some information in
> NIP 11 which can include an email address.
> 
> 
> /dev/fd0
> floppy disk guy
> 
> 
> 
>     
>         
>             
>     
>             
>         Sent with Proton Mail secure email.
>     
> 
> 
> 
> 
>         On Monday, November 13th, 2023 at 8:35 PM, Overthefalls via
> bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> 
>         
> >             On Tue, 2023-11-07 at 09:37 -0600, Bryan Bishop via
> > bitcoin-dev wrote:
> > > Google Groups is another interesting option, 
> > 
> > I don't think I'm the only person on this list that is strongly
> > opposed to using google for anything. They are too big and they
> > have their hand in everything, and their eyes (and analytics) on
> > everything.
> > I remember when there were virtually no gmail email addresses that
> > posted to this list. Suddenly in 2020 or 2021, we had an influx of
> > gmail subscribers and posters. That didn't escape me then and it is
> > not lost on me now. 
> > Email is great for public discussion for many reasons. The fact
> > that everyone gets a copy of the data, there is no single central
> > authority that can edit emails once they have been sent out. Anyone
> > can archive email messages, they can generally store or publish the
> > data anywhere they like. That is not the case with web forum
> > content. 
> > I like the lightning anti-spam fee idea. That would encourage me to
> > finally adopt lightning, and it would, I'm sure, produce some
> > interesting results for the list. 
> > I don't think email should be out of the question. Does anyone
> > besides kanzure@gmail.com think that sticking with email is out of
> > the question?
> > Let's do what's necessary to stick with email. 
> > 
> > 
> > 
> > 
> > 
> >         
> 
>     


-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231114/d2fbce8d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 26
********************************************
