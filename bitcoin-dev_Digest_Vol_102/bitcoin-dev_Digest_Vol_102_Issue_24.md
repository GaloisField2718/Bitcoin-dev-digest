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

   1. Re: Future of the bitcoin-dev mailing list (vjudeu@gazeta.pl)
   2. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Antoine Riard)
   3. Re: Future of the bitcoin-dev mailing list (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Sat, 11 Nov 2023 11:54:56 +0100
From: vjudeu@gazeta.pl
To: Bryan Bishop <kanzure@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Bitcoin Dev
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID:
	<102858647-4a24d51eb95c76b443567edd0852c411@pmq6v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

What about using Signet, or some separate P2P network, to handle all of that?
?
1. All e-mails could be sent in a pure P2P way, just each "mailing list node" would receive it, and include to its mempool.
2. The inclusion of some message would be decided by signing a block. Moderators would pick the proper messages, and publish them by broadcasting a new block to all nodes.
3. Each message will be signed by some public key. It could be changed each time, or even derived from some HD wallet. Only those owning "master public keys" would know, which messages were sent by the same person.
4. The time of the block could be much longer than 10 minutes. It could be for example one hour, one day, or even longer. Or, the commitment to all of that could be just included "every sometimes" to the existing Signet chain, because it would take no additional on-chain bytes, and can be easily done in the coinbase transaction.
5. If there will be too much spam in the mempool, then hashcash-based Proof of Work can be used to filter messages. Instead of fee-based filtering, it could be Proof-of-Work-based filtering. Even better: because of "master public keys", the regular participants could be allowed anyway, without providing additional Proof of Work. Their signature would be sufficient in that case.
6. The code is almost there. Maybe there are even altcoins, designed specifically for storing data, and we could just use them?
7. This kind of decision would push things like Silent Payments forward. Because then, you could develop scanners, to know, who wrote which message. You could enter some "master public key", scan the whole chain, and find out all messages written by that particular participant.
8. It would push commitments forward. Because then, it would be possible to send some message to the "P2P mailing list network", and reveal it later. Of course, it is not mandatory to accept commitments at all, which means, they could be easily disabled, if they would be misused. Or we could start with no commitments, and introduce them later if needed.
9. Because Signet challenge can contain some multisig, or even some Taproot address, there will be no issue with using the same password to access the moderation panel. Also, in that case, it is possible to prove later, which moderator accepted which message. And also, it is still possible to use some shared key, if revealing that is not desirable, or even it is possible to easily reach "approved by all moderators" messages, because their Schnorr signatures could be combined. Also, any K-of-N multisig can be battle-tested in that way.
?
So, I can see two options: reusing some existing P2P network, or making a new one, designed specifically for handling mailing list messages in a pure P2P way. I guess we can try some existing chains first, and if there is no promising altcoin, or if we don't want to be associated with any altcoin, then our own Signet-like network could solve it.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231111/581cd60c/attachment-0001.html>

------------------------------

Message: 2
Date: Mon, 13 Nov 2023 02:18:16 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<CALZpt+FEwjwQQWY6TBFuWeZbqC6Ywa7eSTcpqYuQPZ6+6QBzaw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Your two latest mails.

> The problem that OP_Expire aims to solve is the fact that Carol could
prevent
> Bob from learning about the preimage in time, while still getting a
chance to
> use the preimage herself. OP_Expire thoroughly solves that problem by
ensuring
> that the preimage is either broadcast in the blockchain in a timely
fashion, or
> becomes useless.

I respectfully disagree - There is a more general underlying issue for
outdated states in multi-party off-chain constructions, where any "revoked"
or "updated" consensus-valid state can be used to jam the latest off-chain
agreed-on, through techniques like replacement cycling or pinning.

> My suggestion of pre-signing RBF replacements, without anchor outputs,
and with
> all outputs rendered unspendable with 1 CSV, is clearly superior: there
are
> zero degrees of freedom to the attacker, other than the possibility of
> increasing the fee paid or broadcasting a revoked commitment. The latter
of
> course risks the other party punishing the fraud.

Assuming the max RBF replacement is pre-signed at 200 sats / vb, with
commitment transaction of ~268 vbytes and at least one second-stage HTLC
transaction of ~175 vbytes including witness size, a channel counterparty
must keep at worst a fee-bumping reserve of 35 268 sats, whatever payment
value. As of today, any payment under $13 has to become trimmed HTLCs.
Trimmed HTLCs are coming with their own wormhole of issues, notably making
them a target to be stolen by low-hashrate capabilities attackers [0].

[0]
https://lists.linuxfoundation.org/pipermail/lightning-dev/2020-May/002714.html

> This does have the practical problem that a set of refund transactions
will
> also need to be signed for each fee variant. But, eg, signing 10x of each
isn't
> so burdensome. And in the future that problem could be avoided with
> SIGHASH_NOINPUT, or replacing the pre-signed refund transaction mechanism
with
> a covenant.

I think if you wish to be safe against fees griefing games between
counterparties, both counterparties have to maintain their own fee-bumping
reserves, which make channel usage less capital efficient, rather than
being drawn from a common reserve.

> Using RBF rather than CPFP with package relay also has the advantage of
being
> more efficient, as no blockspace needs to be consumed by the anchor
outputs or
> transactions spending them. Of course, there are special circumstances
where
> BIP125 rules can cause CPFP to be cheaper. But we can easily fix that, eg
by
> reducing the replacement relay fee, or by delta-encoding transaction
updates.

It is left as an exercise to the reader how to break the RBF approach for
LN channels as proposed.

> As SIGHASH_NOINPUT is desirable for LN-Symmetry, a softfork containing
both it
> and OP_Expire could make sense.

I think there is one obvious issue of pre-signing RBF replacements combined
with LN-symmetry, namely every state has to pre-commit to fee values
attached and such states might spend each other in chain. So now you would
need `max-rbf-replacement` *  `max-theoretical-number-of-states` of
fee-bumping reserves unless you can pipe fee value with some covenant
magic, I think.

> In existing anchor output transactions, this type of attack wouldn't work
as
> when broadcasting the transaction, Alice would be spending her anchor
output,
> which Bob can't double spend.

However Bob can double-spend Alice's commitment transaction with his own
commitment transaction and a CPFP, as long as it's a better ancestor
feerate and absolute fee package, then double-spend his own CPFP. Which is
exactly what my test is doing so I don't think your statement of saying
this type of advanced replacement cycling attack wouldn't work isn't
correct.

Best,
Antoine

Le mer. 8 nov. 2023 ? 02:06, Peter Todd <pete@petertodd.org> a ?crit :

> On Wed, Nov 08, 2023 at 12:51:31AM +0000, Peter Todd via bitcoin-dev wrote:
> > > In a post-package relay world, I think this is possible. And that
> > > replacement cycling attacks are breaking future dynamic fee-bumping of
> > > pre-signed transactions concerns me a lot.
> >
> > Well the answer here is pretty clear: v3 package relay with anchors is
> broken.
>
> BTW a subtlety of this that may not be obvious is that in v3 package relay,
> with zero value outputs, the outputs must be spent in the same package.
> Thus
> _unlike_ existing anchor-using transactions, there would be only one anchor
> output on the commitment transaction.
>
> In existing anchor output transactions, this type of attack wouldn't work
> as
> when broadcasting the transaction, Alice would be spending her anchor
> output,
> which Bob can't double spend. But that doesn't work in v3, which intends to
> limit UTXO growth by requiring that anchors be spent in the same package.
> Thus
> unlike existing anchor outputs, an anchor would be truly a OP_1 output
> without
> a signature, and thus belong to either Alice nor Bob uniquely.
>
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231113/548a1be6/attachment-0001.html>

------------------------------

Message: 3
Date: Mon, 13 Nov 2023 02:58:04 +0000
From: Antoine Riard <antoine.riard@gmail.com>
To: Bryan Bishop <kanzure@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID:
	<CALZpt+F6Hovy2XKNuMgb5KJvEKCeQRkvWXDGTaAvfYsoQr+BbQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Thanks for the write up and thanks to the bitcoin-dev mailing list
moderation team for their work along the years.

If we can pick up a communication platform where platform moderators /
infra maintainers have low-risk of being targeted by subpoena + gag order
or "injonction administrative" (the equivalent in some civil law systems)
due to lack of moderators discretionary decisions, I think this is a good
outcome.

I don't know of such a communication platform or set of protocols as of
today. Nostr is promising though realistically weak until half a decade of
work is poured in.

Personally, I'll be more present on the Delving Bitcoin forum, though it
sounds more a temporary solution than a long-term ideal. Being hosted by
kernels or other old open-sources project mailing list infra sounds like a
good idea.

Best,
Antoine

Le mar. 7 nov. 2023 ? 15:37, Bryan Bishop via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

> Hello,
>
> We would like to request community feedback and proposals on the future of
> the mailing list.
>
> Our current mailing list host, Linux Foundation, has indicated for years
> that they have wanted to stop hosting mailing lists, which would mean the
> bitcoin-dev mailing list would need to move somewhere else. We temporarily
> avoided that, but recently LF has informed a moderator that they will cease
> hosting any mailing lists later this year.
>
> In this email, we will go over some of the history, options, and invite
> discussion ahead of the cutoff. We have some ideas but want to solicit
> feedback and proposals.
>
> Background
> ==========
>
> The bitcoin-dev mailing list was originally hosted on Sourceforge.net. The
> bitcoin development mailing list has been a source of proposals, analysis,
> and developer discussion for many years in the bitcoin community, with many
> thousands of participants. Later, the mailing list was migrated to the
> Linux Foundation, and after that OSUOSL began to help.
>
> Linux Foundation first asked us to move the mailing list in 2017. They
> internally attempted to migrate all LF mailing lists from mailman2 to
> mailman3, but ultimately gave up. There were reports of scalability issues
> with mailman3 for large email communities. Ours definitely qualifies as..
> large.
>
> 2019 migration plan: LF was to turn off mailman and all lists would
> migrate to the paid service provider groups.io. Back then we were given
> accounts to try the groups.io interface and administration features.
> Apparently we were not the only dev community who resisted change. To our
> surprise LF gave us several years of reprieve by instead handing the
> subdomain and server-side data to the non-profit OSUOSL lab who instead
> operated mailman2 for the past ~4 years.
>
> OSUOSL has for decades been well known for providing server infrastructure
> for Linux and Open Source development so they were a good fit. This however
> became an added maintenance burden for the small non-profit with limited
> resources. Several members of the Bitcoin dev community contributed funding
> to the lab in support of their Open Source development infrastructure
> goals. But throwing money at the problem isn?t going to fix the ongoing
> maintenance burden created by antiquated limitations of mailman2.
>
> Permalinks
> ==========
>
> Linux Foundation has either offered or agreed to maintain archive
> permalinks so that content of historic importance is not lost. Fortunately
> for us while lists.linuxfoundation.org mailman will go down, they have
> agreed the read-only pipermail archives will remain online. So all old URLs
> will continue to remain valid. However, the moderators strongly advise that
> the community supplements with public-inbox instances to have canonical
> archive urls that are separate from any particular email software host.
>
> Public-Inbox
> ============
>
> https://public-inbox.org/README.html
>
> ?Public Inbox? decentralized archiving - no matter what mailing list
> server solution is used, anyone can use git to maintain their own mailing
> list archive and make it available to read on the web.
>
> Public Inbox is a tool that you can run yourself. You can transform your
> mbox file and it makes it browsable and viewable online. It commits every
> post to a git repository. It's kind of like a decentralized mail archiving
> tool. Anyone can publish the mail archive to any web server they wish.
>
> We should try to have one or more canonical archives that are served using
> public-inbox. But it doesn't matter if these are lost because anyone else
> can archive the mailing list in the same way and re-publish the archives.
>
> These git commits can also be stamped using opentimestamps, inserting
> their hashes into the bitcoin blockchain.
>
> LKML mailing list readers often use public-inbox's web interface, and they
> use the reply-to headers to populate their mail client and reply to threads
> of interest. This allows their reply to be properly threaded even if they
> were not a previous subscriber to that mailing list to receive the headers.
>
> public-inbox makes it so that it doesn't really matter where the list is
> hosted, as pertaining to reading the mailing list. There is still a
> disruption if the mailing list goes away, but the archives live on and then
> people can post elsewhere. The archive gets disconnected from the mailing
> list host in terms of posting. We could have a few canonical URLs for the
> hosts, separate from the mailing list server.
>
> mailman problems
> ================
>
> Over the years we have identified a number of problems with mailman2
> especially as it pertains to content moderation. There are presently a
> handful of different moderators, but mailman2 only has a single password
> for logging into the email management interface. There are no moderator
> audit logs to see which user (there is no concept of different users) acted
> on an email. There is no way to mark an email as being investigated by one
> or more of the moderators. Sometimes, while investigating the veracity of
> an email, another moderator would come in and approve a suspect email by
> accident.
>
> Anti spam has been an issue for the moderators. It's relentless. Without
> access to the underlying server, it has been difficult to fight spam. There
> is some support for filters in mailman2 but it's not great.
>
> 100% active moderation and approval of every email is unsustainable for
> volunteer moderators. A system that requires moderation is a heavy burden
> on the moderators and it slows down overall communication and productivity.
> There's lots of problems with this. Also, moderators can be blamed when
> they are merely slow while they are not actually censoring.
>
> Rejection emails can optionally be sent to
> bitcoin-dev-moderation@lists.ozlabs.org but this is an option that a
> moderator has to remember to type in each time.
>
> Not to mention numerous bugs and vulnerabilities that have accumulated
> over the years for relatively unmaintained software. (Not disclosed here)
>
> Requirements and considerations
> ===============================
>
> Looking towards the future, there are a number of properties that seem to
> be important for the bitcoin-dev mailing list community. First, it is
> important that backups of the entire archive should be easy for the public
> to copy or verify so that the system can be brought up elsewhere if
> necessary.
>
> Second, there seems to be demand for both an email threading interface
> (using mailing list software) as well as web-accessible interfaces (such as
> forum software). There seems to be very few options that cater to both
> email and web. Often, in forum software, email support is limited to email
> notifications and there is limited if any support for email user
> participation.
>
> Third, there should be better support for moderator tools and management
> of the mailing list. See above for complaints about problems with the
> mailman2 system.
>
> Burdens of running your own mailing list and email server
> =========================================================
>
> If you have never operated your own MTA you have no idea how difficult it
> is to keep secure and functional in the face of numerous challenges to
> deliverability. Anti-spam filtering is essential to prevent forwarding
> spam. The moment you forward even a single spam message you run the risk of
> the server IP address being added to blacklists.
>
> The problem of spam filtering is so bad that most IP addresses are
> presumed guilty even if they have no prior spam history, such as if their
> network or subnetwork had spam issues in the past.
>
> Even if you put unlimited time into managing your own email server, other
> people may not accept your email. Or you make one mistake, and then you get
> into permanent blacklists and it's hard to remove. The spam problem is so
> bad that most IPs are automatically on a guilty-until-proven-innocent
> blacklist.
>
> Often there is nothing you can do to get server IP addresses removed from
> spam blacklists or from "bad reputation" lists.
>
> Ironically, hashcash-style proof-of-work stamps to prevent spam are an
> appealing solution but not widely used in this community. Or anywhere.
>
> Infinite rejection or forwarding loops happen. They often need to be
> detected through vigilance and require manual sysadmin intervention to
> solve.
>
> Bitcoin's dev lists being hosted alongside other Open Source projects was
> previously protective. If that mailing list server became blacklisted there
> were a lot of other people who would notice and complain. If we run a
> Bitcoin-specific mail server we are on our own. 100% of the administrative
> burden falls upon our own people. There is also nothing we can do if some
> unknown admin decides they don't like us.
>
> Options
> =======
>
> Web forums are an interesting option, but often don't have good email user
> integration. At most you can usually hope for email notifications and an
> ability to reply by email. It changes the model of the community from push
> (email) to pull (logging into a forum to read). RSS feeds can help a little
> bit.
>
> Many other projects have moved from mailing lists to forums (eg
> https://discuss.python.org/ ? see https://lwn.net/Articles/901744/ ; or
> https://ethresear.ch/), which seem easier to maintain and moderate, and
> can have lots of advanced features beyond plaintext, maybe-threading and
> maybe-HTML-markup.
>
> Who would host the forum? Would there be agreement around which forum
> software to use or which forum host? What about bitcointalk.org or
> delvingbitcoin.org? There are many options available. Maybe what we
> actually want isn?t so much a discussion forum, as an 'arxiv of our own'
> where anons can post BIP drafts and the like?
>
> Given the problems with mailman2, and the decline of email communities in
> general, it seems that moving to mailman3 would not be a viable long-term
> option. This leaves us with Google Groups or groups.io as two remaining
> options.
>
> groups.io is an interesting option: they are a paid service that
> implements email communities along with online web forum support. However,
> their public changelog indicates it has been a few years since their last
> public change. They might be a smaller company and it is unclear how long
> they will be around or if this would be the right fit for hosting sometimes
> contentious bitcoin development discussions...
>
> Google Groups is another interesting option, and comes with different
> tradeoffs. It's the lowest effort to maintain option, and has both an email
> interface and web forum interface. Users can choose which mode they want to
> interact with.
>
> For the Google Groups web interface, you can use it with a non-gmail
> account, but you must create a Google Account which is free to do. it does
> not require any personal information to do so. This also allows you to add
> 2FA. Non-gmail non-google users are able to subscribe and post email from
> their non-gmail non-google email accounts. Tor seems to work for the web
> interface.
>
> Will Google shut it down, will they cut us off, will they shut down
> non-google users? The same problem exists with other third-party hosts.
>
> The moderation capabilities for Google Groups and groups.io seem to be
> comparable. It seems more likely that Google Groups will be able to handle
> email delivery issues far better than a small resource-constrained
> operation like groups.io. ((During feedback for this draft, luke-jr
> indicates that Google Workspaces has been known to use blacklisted IPs for
> business email!))
>
> On the other hand, groups.io is a paid service and you get what you pay
> for... hopefully?
>
> Finally, another option is to do literally nothing. It's less work
> overall. Users can switch to forums or other websites, or private
> one-on-one communication. It would remove a point of semi-centralization
> from the bitcoin ecosystem. It would hasten ossification, but on the other
> hand it would hasten ossification and this could be a negative too.
> Moderators would be less of a target.
>
> Unfortunately, by doing nothing, there would be no more widely used group
> email communication system between bitcoin developers. Developers become
> less coordinated, mayhem and chaos as people go to different communication
> platforms, a divided community is more vulnerable, etc. BIP1 and BIP2 would
> need to be revised for other venues.
>
> The main categories of what to move to are: web forums, mailing lists, and
> hybrids of those two options. Most everything is either self-hosted or you
> pay someone else to host it. It's kind of the same problem though. It
> largely depends on how good is the software and unfortunately running your
> own MTA that forwards mail is not a good option.
>
> Going forward
> ===========
>
> We'd like to invite feedback and proposals from the community, and see
> what options are available. One potential option is a migration to Google
> Groups, but we're open to ideas at this point. We apologize for any
> inconvenience this disruption has caused.
>
>
> Bitcoin-dev mailing list moderation team
>
> Bryan Bishop
> Ruben Somsen
> Warren Togami
> various others.
>
> --
> - Bryan
> https://twitter.com/kanzure
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231113/b741068f/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 24
********************************************
