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

   1. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Peter Todd)
   2. Re: bitcoin-dev Digest, Vol 102, Issue 15
      (Luke Kenneth Casson Leighton)
   3. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Peter Todd)
   4. Re: Future of the bitcoin-dev mailing list (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Wed, 8 Nov 2023 00:51:31 +0000
From: Peter Todd <pete@petertodd.org>
To: Antoine Riard <antoine.riard@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZUrbk9a9jiL87pxd@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Mon, Nov 06, 2023 at 06:45:21PM +0000, Antoine Riard wrote:
> > I think you are misunderstanding a key point to my OP_Expire proposal:
> because
> > the ability to spend the preimage branch of the HTLC goes away when the
> refund
> > branch becomes available, replacing cycling or any similar technique
> becomes
> > entirely irrelevant.
> 
> > The situation where Carol prevents Bob from learning about the preimage
> in time
> > simply can't happen: either Carol collects the HTLC with knowledge of the
> > preimage, by spending it in a transaction mined prior to the expiration
> time
> > and ensuring that Bob learns the preimage from the blockchain itself. Or
> the
> > HTLC expires and Bob can use the refund branch at his leisure.
> 
> I think I understand the semantic of the OP_Expire proposal overall
> correctly, however I'm not sure it prevents replacing cycling or any
> similar adversarial technique, as the forwarding node might be the attacker
> in some scenario.

<snip>

> Assuming this advanced scenario is correct, I'm not sure the OP_Expire
> proposal is substantially fixing all the adversarial replacement cycling
> situations.

What you are describing here is a completely different problem than what
OP_Expire aims to solve.

The problem that OP_Expire aims to solve is the fact that Carol could prevent
Bob from learning about the preimage in time, while still getting a chance to
use the preimage herself. OP_Expire thoroughly solves that problem by ensuring
that the preimage is either broadcast in the blockchain in a timely fashion, or
becomes useless.

The problem you are describing, as Zmm points out below, doesn't actually exist
in Bitcoin right now. But it could exist if we adopted v3 package relay, which
as I've pointed out elsewhere, is inferior to using RBF.


On Tue, Nov 07, 2023 at 03:44:21PM +0000, Antoine Riard wrote:
> Hi Zeeman,
> 
> > Neither can Bob replace-recycle out the commitment transaction itself,
> because the commitment transaction is a single-input transaction, whose
> sole input requires a signature from
> > Bob and a signature from Carol --- obviously Carol will not cooperate on
> an attack on herself.
> 
> The replacement cycling happens on the commitment transaction spend itself,
> not the second stage, which is effectively locked until block 100.
> 
> If the commitment transaction is pre-signed with 0 sat / vb and all the
> feerate / absolute fee is provided by a CPFP on one of the anchor outputs,
> Bob can replace the CPFP itself. After replacement of its child, the
> commitment transaction has a package feerate of 0 sat / vb and it will be
> trimmed out of the mempool.
> 
> This is actually the scenario tested here on the nversion = 3 new mempool
> policy branch  (non-deployed yet):
> https://github.com/ariard/bitcoin/commits/2023-10-test-mempool-2
> 
> As of today commitment transactions might not propagate if dynamic mempool
> min fee is above pre-signed commitment transaction, which is itself unsafe.
> I think this behavior can currently be opportunistically exploited by
> attackers.

Yes, obviously it can be. For starters, you can easily end up in a situation
where the commitment transaction simply can't get mined, an obvious problem.

> In a post-package relay world, I think this is possible. And that
> replacement cycling attacks are breaking future dynamic fee-bumping of
> pre-signed transactions concerns me a lot.

Well the answer here is pretty clear: v3 package relay with anchors is broken.

My suggestion of pre-signing RBF replacements, without anchor outputs, and with
all outputs rendered unspendable with 1 CSV, is clearly superior: there are
zero degrees of freedom to the attacker, other than the possibility of
increasing the fee paid or broadcasting a revoked commitment. The latter of
course risks the other party punishing the fraud.

This does have the practical problem that a set of refund transactions will
also need to be signed for each fee variant. But, eg, signing 10x of each isn't
so burdensome. And in the future that problem could be avoided with
SIGHASH_NOINPUT, or replacing the pre-signed refund transaction mechanism with
a covenant.

Using RBF rather than CPFP with package relay also has the advantage of being
more efficient, as no blockspace needs to be consumed by the anchor outputs or
transactions spending them. Of course, there are special circumstances where
BIP125 rules can cause CPFP to be cheaper. But we can easily fix that, eg by
reducing the replacement relay fee, or by delta-encoding transaction updates.


As SIGHASH_NOINPUT is desirable for LN-Symmetry, a softfork containing both it
and OP_Expire could make sense.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231108/5b2b9c2e/attachment-0001.sig>

------------------------------

Message: 2
Date: Wed, 8 Nov 2023 02:00:00 +0000
From: Luke Kenneth Casson Leighton <lkcl@lkcl.net>
To: James Blacklock <jamesblacklock@protonmail.com>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>, Alain Williams
	<addw@phcomp.co.uk>
Subject: Re: [bitcoin-dev] bitcoin-dev Digest, Vol 102, Issue 15
Message-ID:
	<CAPweEDx7_a6rfat=DeXn3FeYwRZWp8GTu4N9rvRywQuxfNTJMg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Tuesday, November 7, 2023, James Blacklock <jamesblacklock@protonmail.com>
wrote:

> Agreed, email lists are the way. Personally I love reading the email
list; it is a great resource to know what kinds of technical discussions
are going on in the community. I certainly hope we can just migrate to a
different email list.

i have a friend alain williams who runs lists.phcomp.co.uk
and is competent at it. was the UKUUG Chair err 25 years ago?
cc'd.

the other lowest-common-denominator method is of course nntp
newsgroups (eternal-september.org run an excellent spam-free
one) and i do not mean "newsgroups via groups.google.com",
i mean *actual* nntp newsgroups, you know, the ones that have
been running for 40 years and everyone has forgotten even
exist? :)

they were and always have been distributed and distributable
(and spam-free *if* run properly) and i am sure the owner of
eternal-september would be happy to host/distribute bitcoin-dev.

another idea is public-inbox which actually stores
an entire mail archive *in a git repository*
https://github.com/nojb/public-inbox

  public-inbox implements the sharing of an email inbox
  via git to complement or replace traditional mailing lists.
  Readers may read via NNTP, IMAP, Atom feeds or HTML archives.

public-inbox can be "initialised" from a mailman archive
so you can have the entire past history of messages in
the git repo as well.  it's really quite sophisticated.

if anyone doesn't like "email bcuz old", or wants to remain
anonymous, they can always get a protonmail account, use
mail-forwarders, and TOR. and if they are happy to use nntp they can
register
on eternal-september.org, which then allows them to send and
receive... and then use TOR-proxy.

all doable *without* having to install something that will
consume alarmingly high resources and cost a fortune in hosting
every month.

l.

>
>
> On Tuesday, November 7th, 2023 at 3:20 PM, Luke Kenneth Casson Leighton
via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>
>>
>>
>> On Tuesday, November 7, 2023, <
bitcoin-dev-request@lists.linuxfoundation.org> wrote:
>>
>> > Rooms can be E2E encrypted.
>>
>> please, NO.
>>
>> there are people who have such valuable skills that their
>> lives are put in danger if they engage in encrypted conversations.
>>
>> additionally the entire point of an open project IS THAT IT IS OPEN.
>>
>> mailing lists are the lowest OPEN common denominator.
>>
>> l.
>>
>>
>> --
>> ---
>> crowd-funded eco-conscious hardware: https://www.crowdsupply.com/eoma68
>

-- 
---
crowd-funded eco-conscious hardware: https://www.crowdsupply.com/eoma68
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231108/1c6c6030/attachment-0001.html>

------------------------------

Message: 3
Date: Wed, 8 Nov 2023 02:06:23 +0000
From: Peter Todd <pete@petertodd.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZUrtHyQBOEZTM3Bj@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Wed, Nov 08, 2023 at 12:51:31AM +0000, Peter Todd via bitcoin-dev wrote:
> > In a post-package relay world, I think this is possible. And that
> > replacement cycling attacks are breaking future dynamic fee-bumping of
> > pre-signed transactions concerns me a lot.
> 
> Well the answer here is pretty clear: v3 package relay with anchors is broken.

BTW a subtlety of this that may not be obvious is that in v3 package relay,
with zero value outputs, the outputs must be spent in the same package. Thus
_unlike_ existing anchor-using transactions, there would be only one anchor
output on the commitment transaction.

In existing anchor output transactions, this type of attack wouldn't work as
when broadcasting the transaction, Alice would be spending her anchor output,
which Bob can't double spend. But that doesn't work in v3, which intends to
limit UTXO growth by requiring that anchors be spent in the same package. Thus
unlike existing anchor outputs, an anchor would be truly a OP_1 output without
a signature, and thus belong to either Alice nor Bob uniquely.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231108/524271a8/attachment-0001.sig>

------------------------------

Message: 4
Date: Wed, 8 Nov 2023 13:56:17 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID: <ZUsG4fxgrdCIulef@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Tue, Nov 07, 2023 at 09:37:22AM -0600, Bryan Bishop via bitcoin-dev wrote:
> Web forums are an interesting option, but often don't have good email user
> integration.

> What about bitcointalk.org or delvingbitcoin.org?

delvingbitcoin.org is something I setup; it's a self-hosted discourse
instance. (You don't have to self-host discourse, but not doing so limits
the number of admins/moderators, the plugins you can use, and the APIs you
can access)

For what it's worth, I think (discourse) forums have significant
advantages over email for technical discussion:

 * much better markup: you can write LaTeX for doing maths, you
   can have graphviz or mermaid diagrams generated directly from text,
   you can do formatting without having to worry about HTML email.
   because that's done direct from markup, you can also quote such
   things in replies, or easily create a modified equation/diagram
   if desired, things that are much harder if equations/diagrams are
   image/pdf attachments.

 * consistent threading/quoting: you don't have to rely on email clients
   to get threading/quoting correct in order to link replies with the
   original message

 * having topics/replies, rather than everything being an individual
   email, tends to make it easier to avoid being distracted by followups
   to a topic you're not interested in.

 * you can do reactions (heart / thumbs up / etc) instead of "me too"
   posts, minimising the impact of low-content responses on readers,
   without doing away with those responses entirely.

 * after the fact moderation: with mailing lists, moderation can only
   be a choice between "send this post to every subscriber" or not,
   and the choice obviously has to be made before anyone sees the posts;
   forums allow off-topic/unconstructive posts to be removed or edited.

Compared to mailing-lists-as-a-service, a self-hosted forum has a few
other possible benefits:

 * it's easier to setup areas for additional topics, without worrying
   you're going to be forced into an arbitrarily higher pricing tier

 * you can setup spaces for private working groups. (and those groups can
   make their internal discussions public after the fact, if desired)

 * you can use plugin interfaces/APIs to link up with external resources

There are a few disadvantages too:

 * discourse isn't lightweight -- you need a whole bunch of infrastructure
   to go from the markdown posts to the actual rendered posts/comments;
   so backups of just the markdown text isn't really "complete"

 * discourse is quite actively developed -- so it could be possible
   that posts that use particular features/plugins (eg to generate
   diagrams) will go stale eventually as the software changes, and stop
   being rendered correctly

 * discourse gathers a moderate amount of non-public/potentially private
   data (eg email addresses, passwords, IP addresses, login times) that
   may make backups and admin access sensitive (which is why there's a
   git archive generated by a bot for delvingbitcoin, rather than raw
   database dumps)

There are quite a few open source projects using discourse instances, eg:

  Python: https://discuss.python.org/
  Ruby on Rails: https://discuss.rubyonrails.org/
  LLVM: https://discourse.llvm.org/
  Jupyter: https://discourse.jupyter.org/
  Fedora: https://discussion.fedoraproject.org/
  Ubuntu: https://discourse.ubuntu.com/
  Haskell: https://discourse.haskell.org/

There's also various crypto projects using it:

  Eth research: https://ethresear.ch/
  Chia: https://developers.chia.net/

There's a couple of LWN articles on Python's adoption of discourse
that I found interesting, fwiw:

  https://lwn.net/Articles/901744/  [2022-07-20]
  https://lwn.net/Articles/674271/  [2016-02-03]

I don't think this needs to be an "either-or" question -- better to
have technical discussions about bitcoin in many places and in many
formats, rather than just one -- but I thought I'd take the opportunity
to write out why I thought discourse was worth spending some time on in
this context.

Cheers,
aj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 20
********************************************
