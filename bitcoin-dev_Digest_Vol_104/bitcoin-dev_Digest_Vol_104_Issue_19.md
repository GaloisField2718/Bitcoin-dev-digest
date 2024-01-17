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

   1. Re: BIP process friction (Christopher Allen)
   2. Re: BIP process friction (Luke Dashjr)


----------------------------------------------------------------------

Message: 1
Date: Tue, 16 Jan 2024 22:55:03 -0800
From: Christopher Allen <ChristopherA@lifewithalacrity.com>
To: Anthony Towns <aj@erisian.com.au>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID:
	<CACrqygDJRtZN4Oo30=DaFO2KYkn1H+Daxh5cinHKz66Uvn9BVg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Tue, Jan 16, 2024 at 6:43?PM Anthony Towns via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> If people want to use it for bitcoin-related proposals that don't have
> anything to do with inquisition, that's fine; I'm intending to apply the
> policies I think the BIPs repo should be using, so feel free to open a PR,
> even if you already know I think your idea is BS on its merits. If someone
> wants to write an automatic-merge-bot for me, that'd also be great.
>
> If someone wants to reform the BIPs repo itself so it works better,
> that'd be even better, but I'm not volunteering for that fight.
>

I've no idea how to reform BIPs, but we have a similar problem with the
Blockchain Commons Research (BCR) vs Proposals (BCP), vs. specifications
that are emerging in various other standards groups (IETF, W3C, and we have
desire to submit some of these as BIPs as well).

We do a few things differently, one of which in particular might be useful
for the future of BIPs: we reset the numbers every year. So the first new
BCR (research proposal) for 2024 would be 2024-01. Also, when there is a
major change in an old BCR, we create a new number for it in the new year
it is update.

We also have a concept called "Status", which is a progression that only
moves forward if BCRs are actually implemented with a reference
implementation, and advances further when they have multiple
implementations (and thus are qualified moved over to BCP repo as it is
somewhat stable and no longer "research".). A last form is when a
specification has moved to be controlled by another standards group (such
as a BIP). If only one organization implements a BCR, it will never advance
to BCP.

Some form of Status for BIPs inspired by this concept could track if a BIP
was ever actually implemented by someone, or more ideally, implemented by
multiple people in multiple organizations, ideally in multiple languages.

Here is how we currently do status, and the status of our current
specifications:
https://github.com/BlockchainCommons/Research/blob/master/README.md#status

Each BCR has a status which is indicated by a symbol.
SymbolTitleDescription
?? Withdrawn Of historic interest only. Withdrawn either because never came
into use or proved sufficiently problematic that we do not recommend its
usage in any way.
? Superseded Superseded by a newer BCR. We do not suggest implementing as
an output format, but you may still wish to implement as an input format to
maintain backward compatibility.
? Research Contains original research or proposes specifications that have
not yet been implemented by us. Offered to the community for consideration.
?? Reference Implementation At least one reference implementation has been
released, usually as a library, and may include demos or other supporting
tools. This specification still remains very open to change because it has
not yet (to our knowledge) been implemented by additional parties.
???? Multiple Implementations At least two (known) implementations exist,
at least one not by the owner of the reference implementation. Has
demonstrable community support. May still change due to the needs of the
community, but community feedback will be sought.
?????? Standards Track Typically at least two implementations, and is
considered stable and ready for standardization. Being proposed as a BIP,
IETF Internet Draft, or some other standardization draft format. Will
typically be moved to the BCP repo
<https://github.com/BlockchainCommons/bcps>. Though changes may still be
made to the specification, these changes will exclusively be to allow for
standardization, and will be conducted with community feedback.
???????? Standardized A specification has been standardized as a an IETF
RFC, BIP, or approved by some other standards body.

?? after another status symbol is read, "...but withdrawn" and ? is read,
"...but superseded".

-- Christopher Allen
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240116/b04a48a8/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 17 Jan 2024 11:45:59 -0500
From: Luke Dashjr <luke@dashjr.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID: <030e09b8-3831-45ff-92ad-9531ae277f80@dashjr.org>
Content-Type: text/plain; charset="utf-8"; Format="flowed"

Perhaps a BIP 3 is in order, but most of the real issue is simply a 
matter of volunteer time.

AJ's attempt to conflate that with his own personal disagreements with 
how BIPs have always worked, is unrelated.

Luke


On 1/17/24 01:55, Christopher Allen via bitcoin-dev wrote:
>
>
> On Tue, Jan 16, 2024 at 6:43?PM Anthony Towns via bitcoin-dev 
> <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>     If people want to use it for bitcoin-related proposals that don't have
>     anything to do with inquisition, that's fine; I'm intending to
>     apply the
>     policies I think the BIPs repo should be using, so feel free to
>     open a PR,
>     even if you already know I think your idea is BS on its merits. If
>     someone
>     wants to write an automatic-merge-bot for me, that'd also be great.
>
>     If someone wants to reform the BIPs repo itself so it works better,
>     that'd be even better, but I'm not volunteering for that fight.
>
>
> I've no idea how to reform BIPs, but we have a similar problem with 
> the Blockchain Commons Research (BCR) vs Proposals (BCP), vs. 
> specifications that are emerging in various other standards groups 
> (IETF, W3C, and we have desire to submit some of these as BIPs as well).
>
> We do a few things differently, one of which in particular might be 
> useful for the future of BIPs: we reset the numbers every year. So the 
> first new BCR (research proposal) for 2024 would be 2024-01. Also, 
> when there is a major change in an old BCR, we create a new number for 
> it in the new year it is update.
>
> We also have a concept called "Status", which is a progression that 
> only moves forward if BCRs are actually implemented with a reference 
> implementation, and advances further when they have multiple 
> implementations (and thus are qualified moved over to BCP repo as it 
> is somewhat stable and no longer "research".). A last form is when a 
> specification has moved to be controlled by another standards group 
> (such as a BIP). If only one organization implements a BCR, it will 
> never advance to BCP.
>
> Some form of Status for BIPs inspired by this concept could track if a 
> BIP was ever actually implemented by someone, or more ideally, 
> implemented by multiple people in multiple organizations, ideally in 
> multiple languages.
>
> Here is how we currently do status, and the status of our current 
> specifications: 
> https://github.com/BlockchainCommons/Research/blob/master/README.md#status
>
> Each BCR has a status which is indicated by a symbol.
>
> Symbol 	Title 	Description
> ?? 	Withdrawn 	Of historic interest only. Withdrawn either because 
> never came into use or proved sufficiently problematic that we do not 
> recommend its usage in any way.
> ? 	Superseded 	Superseded by a newer BCR. We do not suggest 
> implementing as an output format, but you may still wish to implement 
> as an input format to maintain backward compatibility.
> ? 	Research 	Contains original research or proposes specifications 
> that have not yet been implemented by us. Offered to the community for 
> consideration.
> ?? 	Reference Implementation 	At least one reference implementation 
> has been released, usually as a library, and may include demos or 
> other supporting tools. This specification still remains very open to 
> change because it has not yet (to our knowledge) been implemented by 
> additional parties.
> ???? 	Multiple Implementations 	At least two (known) implementations 
> exist, at least one not by the owner of the reference implementation. 
> Has demonstrable community support. May still change due to the needs 
> of the community, but community feedback will be sought.
> ?????? 	Standards Track 	Typically at least two implementations, and 
> is considered stable and ready for standardization. Being proposed as 
> a BIP, IETF Internet Draft, or some other standardization draft 
> format. Will typically be moved to theBCP repo 
> <https://github.com/BlockchainCommons/bcps>. Though changes may still 
> be made to the specification, these changes will exclusively be to 
> allow for standardization, and will be conducted with community feedback.
> ???????? 	Standardized 	A specification has been standardized as a an 
> IETF RFC, BIP, or approved by some other standards body.
>
> ?? after another status symbol is read, "...but withdrawn" and ? is 
> read, "...but superseded".
>
> -- Christopher Allen
>
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240117/e31a7a57/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 19
********************************************
