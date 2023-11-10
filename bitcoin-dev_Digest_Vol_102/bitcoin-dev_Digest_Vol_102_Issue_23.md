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

   1. Re: Ordinals BIP PR (Casey Rodarmor)
   2. Re: Future of the bitcoin-dev mailing list (William Casarin)
   3. Re: Ordinals BIP PR (Claus Ehrenberg)


----------------------------------------------------------------------

Message: 1
Date: Wed, 8 Nov 2023 18:15:05 -0800
From: Casey Rodarmor <casey@rodarmor.com>
To: Luke Dashjr <luke@dashjr.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CANLPe+NAd4imuGji7+o+Y3bWtC4aeTMNj0RrJw0Pu4=e6TEdeQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi all,

Luke is definitely entitled to his opinions about ordinals, and I certainly
understand why people may not like ordinals and inscriptions.

I don't think that ordinals are "nonsense", an "attack on Bitcoin", or that
I'm dishonest, as Luke implies, or that my actions are an attempt to
"harm/destroy Bitcoin".

I think that whether or not ordinals are good is something about which
reasonable people do and will disagree, and that an impartial BIP editor
would recognize this above their own personal feelings about the matter.

Also, regarding:

> There is a debate on the PR whether the "technically unsound, ..., or not
in keeping with the Bitcoin philosophy." or "must represent a net
improvement." clauses (BIP 2) are relevant.

As I said in my initial email, I think these standards are being applied in
a way that they have not been to previous BIPs, which include all manner of
things, including changes to bitcoin which are nearly unanimously thought
to be quite harmful if adopted.

Best,
Casey

On Mon, Oct 23, 2023 at 11:35?AM Luke Dashjr via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Everything standardized between Bitcoin software is eligible to be and
> should be a BIP. I completely disagree with the claim that it's used for
> too many things.
>
> SLIPs exist for altcoin stuff. They shouldn't be used for things related
> to Bitcoin.
>
> BOLTs also shouldn't have ever been a separate process and should really
> just get merged into BIPs. But at this point, that will probably take
> quite a bit of effort, and obviously cooperation and active involvement
> from the Lightning development community.
>
> Maybe we need a 3rd BIP editor. Both Kalle and myself haven't had time
> to keep up. There are several PRs far more important than Ordinals
> nonsense that need to be triaged and probably merged.
>
> The issue with Ordinals is that it is actually unclear if it's eligible
> to be a BIP at all, since it is an attack on Bitcoin rather than a
> proposed improvement. There is a debate on the PR whether the
> "technically unsound, ..., or not in keeping with the Bitcoin
> philosophy." or "must represent a net improvement." clauses (BIP 2) are
> relevant. Those issues need to be resolved somehow before it could be
> merged. I have already commented to this effect and given my own
> opinions on the PR, and simply pretending the issues don't exist won't
> make them go away. (Nor is it worth the time of honest people to help
> Casey resolve this just so he can further try to harm/destroy Bitcoin.)
>
> Luke
>
>
> On 10/23/23 13:43, Andrew Poelstra via bitcoin-dev wrote:
> > On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via bitcoin-dev
> wrote:
> >> I have _not_ requested a BIP for OpenTimestamps, even though it is of
> much
> >> wider relevance to Bitcoin users than Ordinals by virtue of the fact
> that much
> >> of the commonly used software, including Bitcoin Core, is timestamped
> with OTS.
> >> I have not, because there is no need to document every single little
> protocol
> >> that happens to use Bitcoin with a BIP.
> >>
> >> Frankly we've been using BIPs for too many things. There is no avoiding
> the act
> >> that BIP assignment and acceptance is a mark of approval for a
> protocol. Thus
> >> we should limit BIP assignment to the minimum possible: _extremely_
> widespread
> >> standards used by the _entire_ Bitcoin community, for the core mission
> of
> >> Bitcoin.
> >>
> > This would eliminate most wallet-related protocols e.g. BIP69 (sorted
> > keys), ypubs, zpubs, etc. I don't particularly like any of those but if
> > they can't be BIPs then they'd need to find another spec repository
> > where they wouldn't be lost and where updates could be tracked.
> >
> > The SLIP repo could serve this purpose, and I think e.g. SLIP39 is not a
> BIP
> > in part because of perceived friction and exclusivity of the BIPs repo.
> > But I'm not thrilled with this situation.
> >
> > In fact, I would prefer that OpenTimestamps were a BIP :).
> >
> >> It's notable that Lightning is _not_ standardized via the BIP process.
> I think
> >> that's a good thing. While it's arguably of wide enough use to warrent
> BIPs,
> >> Lightning doesn't need the approval of Core maintainers, and using their
> >> separate BOLT process makes that clear.
> >>
> > Well, LN is a bit special because it's so big that it can have its own
> > spec repo which is actively maintained and used.
> >
> > While it's technically true that BIPs need "approval of Core maintainers"
> > to be merged, the text of BIP2 suggests that this approval should be a
> > functionary role and be pretty-much automatic. And not require the BIP
> > be relevant or interesting or desireable to Core developers.
> >
> >
> >
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231108/d9c796aa/attachment-0001.html>

------------------------------

Message: 2
Date: Thu, 9 Nov 2023 13:03:12 +0900
From: William Casarin <jb55@jb55.com>
To: Andrew Chow <lists@achow101.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Future of the bitcoin-dev mailing list
Message-ID:
	<ntl3yxklpw7z7etqhpvwvh2crjtjk3ys6azes4hompryv5xtux@mlcfro55cls5>
Content-Type: text/plain; charset=us-ascii; format=flowed

On Tue, Nov 07, 2023 at 06:14:23PM +0000, Andrew Chow via bitcoin-dev wrote:
>Hi Dan,
>
>I don't think nostr would be a suitable replacement for the mailing
>list, although this opinion is biased by the fact that I do not use
>nostr and find it to be uninteresting.

email-like functionality over nostr isn't really explored yet, but it is
something I'm interesting in. So I agree nostr isn't a suitable email
replacement *yet*.

>From my limited understanding of how nostr works, it's not clear to me
>how a distributed system that uses message broadcast would work in the
>same way as a mailing list.

My idea was to have a mailing list relay, the only thing missing is To:
and Cc: tags on notes so that the relay can reject notes not destined
for the mailing list

>How would people "subscribe"? How would archives be searched or
>otherwise be available to people who are not on nostr?

You would subscribe by connecting to the relay and pulling down the
notes. your client could cache notes and only pull new ones.

>How do you distinguish and filter between legitimate dev posts
>intended for discussion and random crap and shitposting as shows up on
>social media?

You would need to have metadata on the note that specifies that the note
is destined for that specific mailing list relay (To, Cc, etc). Then the
client sending the message can send it to that specific relay during
note composition. Again, this is different than then current model that
exists with social networking clients designed for blasting your note to
as many people as possible.

>I also don't think that long form text on nostr (or any similar
>platform) can sufficiently replace email. None of these things seem to
>contain a way to have a separate subject line as email does. Subjects
>are immensely important for me as it provides a quick and easy way to
>filter out things I don't care about reading. I don't want to have read
>something in before I can decide that I don't care about reading it.

Subject lines already exist in nostr and are a part of some email-like
clients like https://github.com/unclebob/more-speech . it's just a tag
like every other piece of metadata.

>In general, I strongly prefer email, or a platform that has email as a
>first class user interface, over platforms such as nostr, matrix, or web
>forums. Email is universal - everyone has one and everyone knows how it
>works. It dramatically lowers the barrier of entry. Having to make an
>account somewhere or download some specific client in order to
>participate will simply result in only the most dedicated participating.
>Development in open source must be an open process and the barriers to
>entry should be low.

I definitely prefer email at the moment as well, but it is also a pain
in the ass to run email infra. As someone who runs both email servers
and nostr relays I can say nostr is much more pleasant.

So yeah, it's a bit too early for a nostr replacement, but it's
definitely possible, and you get proper cryptographic identities and
schnorr signed notes which is a bonus. For dealing with spam you could
have a sat entrance fee via lightning. I will start looking into this!

Cheers,

	Will


------------------------------

Message: 3
Date: Thu, 9 Nov 2023 23:32:10 +0100
From: Claus Ehrenberg <aubergemediale@gmail.com>
To: Casey Rodarmor <casey@rodarmor.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CANPykMqq-1Xh5WcHpKPeyfi6YAfjP2gJsO863K=D0yr2McT4aQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hello,

I have developed nodes/wallets for Bitcoin and Bitcoin-derived Altcoins.
3rd-party Bitcoin developers take BIPs very seriously, basically as
must-implement/must-comply features.

Therefore, I think it would be best to restrict BIPs to the minimum
necessary to implement a complying node/wallet.

Cheers!

Claus

On Thu, Nov 9, 2023 at 1:43?PM Casey Rodarmor via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi all,
>
> Luke is definitely entitled to his opinions about ordinals, and I
> certainly understand why people may not like ordinals and inscriptions.
>
> I don't think that ordinals are "nonsense", an "attack on Bitcoin", or
> that I'm dishonest, as Luke implies, or that my actions are an attempt to
> "harm/destroy Bitcoin".
>
> I think that whether or not ordinals are good is something about which
> reasonable people do and will disagree, and that an impartial BIP editor
> would recognize this above their own personal feelings about the matter.
>
> Also, regarding:
>
> > There is a debate on the PR whether the "technically unsound, ..., or
> not in keeping with the Bitcoin philosophy." or "must represent a net
> improvement." clauses (BIP 2) are relevant.
>
> As I said in my initial email, I think these standards are being applied
> in a way that they have not been to previous BIPs, which include all manner
> of things, including changes to bitcoin which are nearly unanimously
> thought to be quite harmful if adopted.
>
> Best,
> Casey
>
> On Mon, Oct 23, 2023 at 11:35?AM Luke Dashjr via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> Everything standardized between Bitcoin software is eligible to be and
>> should be a BIP. I completely disagree with the claim that it's used for
>> too many things.
>>
>> SLIPs exist for altcoin stuff. They shouldn't be used for things related
>> to Bitcoin.
>>
>> BOLTs also shouldn't have ever been a separate process and should really
>> just get merged into BIPs. But at this point, that will probably take
>> quite a bit of effort, and obviously cooperation and active involvement
>> from the Lightning development community.
>>
>> Maybe we need a 3rd BIP editor. Both Kalle and myself haven't had time
>> to keep up. There are several PRs far more important than Ordinals
>> nonsense that need to be triaged and probably merged.
>>
>> The issue with Ordinals is that it is actually unclear if it's eligible
>> to be a BIP at all, since it is an attack on Bitcoin rather than a
>> proposed improvement. There is a debate on the PR whether the
>> "technically unsound, ..., or not in keeping with the Bitcoin
>> philosophy." or "must represent a net improvement." clauses (BIP 2) are
>> relevant. Those issues need to be resolved somehow before it could be
>> merged. I have already commented to this effect and given my own
>> opinions on the PR, and simply pretending the issues don't exist won't
>> make them go away. (Nor is it worth the time of honest people to help
>> Casey resolve this just so he can further try to harm/destroy Bitcoin.)
>>
>> Luke
>>
>>
>> On 10/23/23 13:43, Andrew Poelstra via bitcoin-dev wrote:
>> > On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via bitcoin-dev
>> wrote:
>> >> I have _not_ requested a BIP for OpenTimestamps, even though it is of
>> much
>> >> wider relevance to Bitcoin users than Ordinals by virtue of the fact
>> that much
>> >> of the commonly used software, including Bitcoin Core, is timestamped
>> with OTS.
>> >> I have not, because there is no need to document every single little
>> protocol
>> >> that happens to use Bitcoin with a BIP.
>> >>
>> >> Frankly we've been using BIPs for too many things. There is no
>> avoiding the act
>> >> that BIP assignment and acceptance is a mark of approval for a
>> protocol. Thus
>> >> we should limit BIP assignment to the minimum possible: _extremely_
>> widespread
>> >> standards used by the _entire_ Bitcoin community, for the core mission
>> of
>> >> Bitcoin.
>> >>
>> > This would eliminate most wallet-related protocols e.g. BIP69 (sorted
>> > keys), ypubs, zpubs, etc. I don't particularly like any of those but if
>> > they can't be BIPs then they'd need to find another spec repository
>> > where they wouldn't be lost and where updates could be tracked.
>> >
>> > The SLIP repo could serve this purpose, and I think e.g. SLIP39 is not
>> a BIP
>> > in part because of perceived friction and exclusivity of the BIPs repo.
>> > But I'm not thrilled with this situation.
>> >
>> > In fact, I would prefer that OpenTimestamps were a BIP :).
>> >
>> >> It's notable that Lightning is _not_ standardized via the BIP process.
>> I think
>> >> that's a good thing. While it's arguably of wide enough use to warrent
>> BIPs,
>> >> Lightning doesn't need the approval of Core maintainers, and using
>> their
>> >> separate BOLT process makes that clear.
>> >>
>> > Well, LN is a bit special because it's so big that it can have its own
>> > spec repo which is actively maintained and used.
>> >
>> > While it's technically true that BIPs need "approval of Core
>> maintainers"
>> > to be merged, the text of BIP2 suggests that this approval should be a
>> > functionary role and be pretty-much automatic. And not require the BIP
>> > be relevant or interesting or desireable to Core developers.
>> >
>> >
>> >
>> > _______________________________________________
>> > bitcoin-dev mailing list
>> > bitcoin-dev@lists.linuxfoundation.org
>> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231109/6dd6a8b5/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 23
********************************************
