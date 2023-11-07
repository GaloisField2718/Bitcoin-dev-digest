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

   1. Re: Future of the bitcoin-dev mailing list (Ademan)


----------------------------------------------------------------------

Message: 1
Date: Tue, 7 Nov 2023 11:03:30 -0600
From: Ademan <ademan555@gmail.com>
To: Bryan Bishop <kanzure@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID:
	<CAKwYL5ERT0zH=kcpPwqWe2Q2Gtn+Lj5nQF14yzAZ2nhn8AdD6A@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Bryan,

I don't really want my first (and last?) devlist message to be a fairly
off-the-cuff post on this topic, but here we go anyway.

At the risk of sounding like a nostr evangelist (I promise I'm not), I want
to suggest nostr as a potential replacement to the mailing list. A decent
chunk of software would need to be written, but none of the alternatives
seem particularly attractive to me. I particularly dislike the idea of
locking into a single siloed forum service like the bitcointalk forums. I
realize I may be in the minority of course.


Nostr enables the ML team to outsource all of its biggest burdens, if it
chooses:

- mail server blocking is N/A to nostr

- Hosting costs are completely outsourced unless the ML team chooses to
host a relay.

- Archives and web portal access can be similarly outsourced because any
nostr archive is self-authenticating.

- The ML team can also choose to completely outsource moderation, as nostr
is (more or less) permissionless by nature.
  I understand if there is a "blessed" communication system, the ML team
would probably prefer to keep it high quality. To that end there are
proposals for proof-of-work, and web of trust based blocklists for nostr
which are optional for end users. There are other options such as the
"moderated communities" proposal which would provide tighter control.


On the user side, the optional moderation is very attractive, allowing
controversial threads to exist and continue, without requiring everyone to
see them.


The following do not currently exist (to my knowledge) and would need to be
implemented to meet the ML's requirements:

- an email gateway to satisfy the bulk of existing ML subscribers
  This reintroduces issues with mail server blocking of course.
- a long-form oriented nostr client (current plain text clients could be
used in the meantime)

That admittedly is quite a lot of work, but the second item can be
deferred, and the first is not particularly technically challenging, the
complications are all on the administration side.

I expect some reflexive NACKs based on the immaturity of the ecosystem but
if we have months to prepare, I believe the core requirements can be
solidly satisfied in time, the rest can be developed over time, and I
believe the advantages are worth careful consideration.

Cheers,
Dan

On Tue, Nov 7, 2023 at 9:38?AM Bryan Bishop via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231107/eaec03be/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 14
********************************************
