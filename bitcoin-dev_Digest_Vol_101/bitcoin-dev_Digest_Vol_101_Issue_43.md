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

   1. Re: Ordinals BIP PR (Luke Dashjr)
   2. Re: Ordinals BIP PR (Christopher Allen)


----------------------------------------------------------------------

Message: 1
Date: Tue, 24 Oct 2023 20:15:04 -0400
From: Luke Dashjr <luke@dashjr.org>
To: Olaoluwa Osuntokun <laolu32@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <f6c909b3-6851-f26d-3b30-a65232c1cc61@dashjr.org>
Content-Type: text/plain; charset="utf-8"; Format="flowed"

Seems like a "solution" looking for a problem which doesn't actually 
exist. And not even a good "solution" for that - might as well not have 
BIP number at all, if they're not going to be usefully assigned. What we 
have now is working fine aside from a few trolls once in a while.

On 10/24/23 18:56, Olaoluwa Osuntokun wrote:
> TL;DR: let's just use an automated system to assign BIP numbers, so we can
> spend time on more impactful things.
>
> IIUC, one the primary roles of the dedicated BIP maintainers is just 
> to hand
> out BIP numbers for documents. Supposedly with this privilege, the BIP
> maintainer is able to tastefully assign related BIPs to consecutive 
> numbers,
> and also reserve certain BIP number ranges for broad categories, like 3xx
> for p2p changes (just an example).
>
> To my knowledge, the methodology for such BIP number selection isn't
> published anywhere, and is mostly arbitrary. As motioned in this thread,
> some perceive this manual process as a gatekeeping mechanism, and often
> ascribe favoritism as the reason why PR X got a number immediately, 
> but PR Y
> has waited N months w/o an answer.
>
> Every few years we go through an episode where someone is rightfully upset
> that they haven't been assigned a BIP number after following the requisite
> process.? Most recently, another BIP maintainer was appointed, with 
> the hope
> that the second maintainer would help to alleviate some of the subjective
> load of the position.? Fast forward to this email thread, and it doesn't
> seem like adding more BIP maintainers will actually help with the issue of
> BIP number assignment.
>
> Instead, what if we just removed the subjective human element from the
> process, and switched to using PR numbers to assign BIPs? Now instead of
> attempting to track down a BIP maintainer at the end of a potentially
> involved review+iteration period, PRs are assigned BIP numbers as soon as
> they're opened and we have one less thing to bikeshed and gatekeep.
>
> One down side of this is that assuming the policy is adopted, we'll sorta
> sky rocket the BIP number space. At the time of writing of this email, the
> next PR number looks to be 1508. That doesn't seem like a big deal to me,
> but we could offset that by some value, starting at the highest currently
> manually assigned BIP number. BIP numbers would no longer always be
> contiguous, but that's sort of already the case.
>
> There's also the matter of related BIPs, like the segwit series (BIPs 141,
> 142, 143, 144, and 145). For these, we can use a suffix scheme to indicate
> the BIP lineage. So if BIP 141 was the first PR, then BIP 142 was opened
> later, the OP can declare the BIP 142 is BIP 141.2 or BIP 141-2. I don't
> think it would be too difficult to find a workable scheme.
>
> Thoughts?
>
> -- Laolu
>
>
> On Mon, Oct 23, 2023 at 11:35?AM Luke Dashjr via bitcoin-dev 
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>     Everything standardized between Bitcoin software is eligible to be
>     and
>     should be a BIP. I completely disagree with the claim that it's
>     used for
>     too many things.
>
>     SLIPs exist for altcoin stuff. They shouldn't be used for things
>     related
>     to Bitcoin.
>
>     BOLTs also shouldn't have ever been a separate process and should
>     really
>     just get merged into BIPs. But at this point, that will probably take
>     quite a bit of effort, and obviously cooperation and active
>     involvement
>     from the Lightning development community.
>
>     Maybe we need a 3rd BIP editor. Both Kalle and myself haven't had
>     time
>     to keep up. There are several PRs far more important than Ordinals
>     nonsense that need to be triaged and probably merged.
>
>     The issue with Ordinals is that it is actually unclear if it's
>     eligible
>     to be a BIP at all, since it is an attack on Bitcoin rather than a
>     proposed improvement. There is a debate on the PR whether the
>     "technically unsound, ..., or not in keeping with the Bitcoin
>     philosophy." or "must represent a net improvement." clauses (BIP
>     2) are
>     relevant. Those issues need to be resolved somehow before it could be
>     merged. I have already commented to this effect and given my own
>     opinions on the PR, and simply pretending the issues don't exist
>     won't
>     make them go away. (Nor is it worth the time of honest people to help
>     Casey resolve this just so he can further try to harm/destroy
>     Bitcoin.)
>
>     Luke
>
>
>     On 10/23/23 13:43, Andrew Poelstra via bitcoin-dev wrote:
>     > On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via
>     bitcoin-dev wrote:
>     >> I have _not_ requested a BIP for OpenTimestamps, even though it
>     is of much
>     >> wider relevance to Bitcoin users than Ordinals by virtue of the
>     fact that much
>     >> of the commonly used software, including Bitcoin Core, is
>     timestamped with OTS.
>     >> I have not, because there is no need to document every single
>     little protocol
>     >> that happens to use Bitcoin with a BIP.
>     >>
>     >> Frankly we've been using BIPs for too many things. There is no
>     avoiding the act
>     >> that BIP assignment and acceptance is a mark of approval for a
>     protocol. Thus
>     >> we should limit BIP assignment to the minimum possible:
>     _extremely_ widespread
>     >> standards used by the _entire_ Bitcoin community, for the core
>     mission of
>     >> Bitcoin.
>     >>
>     > This would eliminate most wallet-related protocols e.g. BIP69
>     (sorted
>     > keys), ypubs, zpubs, etc. I don't particularly like any of those
>     but if
>     > they can't be BIPs then they'd need to find another spec repository
>     > where they wouldn't be lost and where updates could be tracked.
>     >
>     > The SLIP repo could serve this purpose, and I think e.g. SLIP39
>     is not a BIP
>     > in part because of perceived friction and exclusivity of the
>     BIPs repo.
>     > But I'm not thrilled with this situation.
>     >
>     > In fact, I would prefer that OpenTimestamps were a BIP :).
>     >
>     >> It's notable that Lightning is _not_ standardized via the BIP
>     process. I think
>     >> that's a good thing. While it's arguably of wide enough use to
>     warrent BIPs,
>     >> Lightning doesn't need the approval of Core maintainers, and
>     using their
>     >> separate BOLT process makes that clear.
>     >>
>     > Well, LN is a bit special because it's so big that it can have
>     its own
>     > spec repo which is actively maintained and used.
>     >
>     > While it's technically true that BIPs need "approval of Core
>     maintainers"
>     > to be merged, the text of BIP2 suggests that this approval
>     should be a
>     > functionary role and be pretty-much automatic. And not require
>     the BIP
>     > be relevant or interesting or desireable to Core developers.
>     >
>     >
>     >
>     > _______________________________________________
>     > bitcoin-dev mailing list
>     > bitcoin-dev@lists.linuxfoundation.org
>     > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>     _______________________________________________
>     bitcoin-dev mailing list
>     bitcoin-dev@lists.linuxfoundation.org
>     https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231024/957eb278/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 24 Oct 2023 16:08:37 -0700
From: Christopher Allen <ChristopherA@lifewithalacrity.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,  Olaoluwa Osuntokun
	<laolu32@gmail.com>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<CACrqygDMmEunc2_Js12ON3_uH2AN7xopFzC2fF9nUsEGNCkRhg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

I think this is a good idea, but suggest that the numbers include year and
number in the year. We do that for all the research and ?wallet improvement
proposals? at Blockchain Commons. This way numbers don?t grow huge like
EIPs currently do.

I might also suggest that the numbers are only automatically offered when a
maintainer does not reject it for three days. That way they can focus on
just responding to obvious spam, and if rejected the moderator name is on
it, rather than the current anonymous pocket veto.

? Christopher Allen [via iPhone]

On Tue, Oct 24, 2023 at 3:57?PM Olaoluwa Osuntokun via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> TL;DR: let's just use an automated system to assign BIP numbers, so we can
> spend time on more impactful things.
>
> IIUC, one the primary roles of the dedicated BIP maintainers is just to
> hand
> out BIP numbers for documents. Supposedly with this privilege, the BIP
> maintainer is able to tastefully assign related BIPs to consecutive
> numbers,
> and also reserve certain BIP number ranges for broad categories, like 3xx
> for p2p changes (just an example).
>
> To my knowledge, the methodology for such BIP number selection isn't
> published anywhere, and is mostly arbitrary. As motioned in this thread,
> some perceive this manual process as a gatekeeping mechanism, and often
> ascribe favoritism as the reason why PR X got a number immediately, but PR
> Y
> has waited N months w/o an answer.
>
> Every few years we go through an episode where someone is rightfully upset
> that they haven't been assigned a BIP number after following the requisite
> process.  Most recently, another BIP maintainer was appointed, with the
> hope
> that the second maintainer would help to alleviate some of the subjective
> load of the position.  Fast forward to this email thread, and it doesn't
> seem like adding more BIP maintainers will actually help with the issue of
> BIP number assignment.
>
> Instead, what if we just removed the subjective human element from the
> process, and switched to using PR numbers to assign BIPs? Now instead of
> attempting to track down a BIP maintainer at the end of a potentially
> involved review+iteration period, PRs are assigned BIP numbers as soon as
> they're opened and we have one less thing to bikeshed and gatekeep.
>
> One down side of this is that assuming the policy is adopted, we'll sorta
> sky rocket the BIP number space. At the time of writing of this email, the
> next PR number looks to be 1508. That doesn't seem like a big deal to me,
> but we could offset that by some value, starting at the highest currently
> manually assigned BIP number. BIP numbers would no longer always be
> contiguous, but that's sort of already the case.
>
> There's also the matter of related BIPs, like the segwit series (BIPs 141,
> 142, 143, 144, and 145). For these, we can use a suffix scheme to indicate
> the BIP lineage. So if BIP 141 was the first PR, then BIP 142 was opened
> later, the OP can declare the BIP 142 is BIP 141.2 or BIP 141-2. I don't
> think it would be too difficult to find a workable scheme.
>
> Thoughts?
>
> -- Laolu
>
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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231024/610c8d60/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 43
********************************************
