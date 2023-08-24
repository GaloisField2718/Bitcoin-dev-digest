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

   1. Re: [Lightning-dev] Bitcoin mail list needs an	explicit
      moderation policy (Bryan Bishop)
   2. Re: Standardisation of an unstructured taproot annex
      (David A. Harding)
   3. Re: Standardisation of an unstructured taproot annex
      (Greg Sanders)


----------------------------------------------------------------------

Message: 1
Date: Fri, 2 Jun 2023 19:06:53 -0500
From: Bryan Bishop <kanzure@gmail.com>
To: Dr Maxim Orlovsky <orlovsky@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org,
	lightning-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] [Lightning-dev] Bitcoin mail list needs an
	explicit moderation policy
Message-ID:
	<CABaSBawHd4C0POxCs5NUA7pAjyz_MR2JmSoCTsC26Kf9H_zEDw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Maxim,

This is exceedingly boring. This is not a good use of your time. There are
thousands of developers subscribed to this mailing list, and we should not
waste their time, including this discussion.

On Fri, Jun 2, 2023 at 6:44?PM Dr Maxim Orlovsky via Lightning-dev <
lightning-dev@lists.linuxfoundation.org> wrote:

> What happened next was very unexpected. I am giving the core of the
> conversation over Twitter after in Annex A - with the purpose to showcase
> the problem I?d like to address in this e-mail. From the discussion, it is
> clear that bitcoin-dev mail list lacks clear explicit moderation (or
> peer-review) policies, which must be applied on a non-selective basis.
> Also, Bryan Bishop, as the current moderator, had abused his powers in
> achieving his agenda based on personal likes or dislikes. The conversation
> went nowhere, and the post got published only after a requirement from
> Peter Todd [9].
>

What exactly is the abuse being alleged here though? Why would it be
surprising that your tweets didn't get the behavior you wanted out of me?
In general mailing list moderators should not be sending items through
based on twitter mobbing, that's a policy you can consider if you want to
think about policies.

Annex A:
>
>    - @kanzure just like to check that our submission to bitcoin-dev
>    hasn?t got to spam <
>    https://twitter.com/lnp_bp/status/1664649328349069320?s=61&t=9A8uvggqKVKV3sT4HPlQyg
>    >
>    - A few mods are reviewing it <
>    https://twitter.com/kanzure/status/1664680893548572677?s=61&t=9A8uvggqKVKV3sT4HPlQyg
>    >
>    - Oh, so a peer review is required to get to bitcoin-dev mail list?
>    Never read about that requirement anywhere <
>    https://twitter.com/lnp_bp/status/1664695061462777858?s=61&t=9A8uvggqKVKV3sT4HPlQyg>.
>    Seems like bitcoin-dev mail list requirements are now specific to the
>    author :) <
>    https://twitter.com/dr_orlovsky/status/1664695668475142144?s=61&t=9A8uvggqKVKV3sT4HPlQyg
>    >
>    - Not the greatest email to pull this over. I'll double check but
>    pretty sure the antagonization is boring me. <
>    https://twitter.com/kanzure/status/1664705038315409420?s=61&t=9A8uvggqKVKV3sT4HPlQyg
>    >
>    - Not sure I understand what you are saying. Can you please clarify? <
>    https://twitter.com/dr_orlovsky/status/1664705280393859103?s=61&t=9A8uvggqKVKV3sT4HPlQyg
>    >
>    - You are boring me and these antics don't make me want to go click
>    approve on your email. <
>    https://twitter.com/kanzure/status/1664705509147004946?s=61&t=9A8uvggqKVKV3sT4HPlQyg
>    >
>
>
Excluding your (and my) other tweets and any other collaborators' tweets
from your report is kind of weird. I think you should include the other
tweets that you were sending me because it provides context. Zooming out,
the entirety of your complaint seems to be about moderation queue latency
and delay. Why would you, or anyone, allege that that moderator latency is
indicative of me specifically not liking you? Wouldn't it be more likely
that the other moderators and I are looking at your email and talking with
each other asynchronously about whether to suggest edits/reject/submit?

I suspect you may be attributing malice to me because I recently asked you
to stop tagging me on quantum woo and you might have taken that negatively
- please keep in mind that not everyone believes in quantum consciousness
or is interested in hearing about it, and it's okay for people like me to
not want to engage on each of your different interests. There is some
overlap in our interests outside of crypto, but that isn't one of them. I
noticed some odd tweets from you to me after that, so that's why that
incident came to my mind as a possible explanation for this.

Thank you.

- Bryan
https://twitter.com/kanzure
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230602/b8b5b953/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 02 Jun 2023 15:08:01 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Joost Jager <joost.jager@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID: <29ff546a6007cec1a0f85b91541f8e4d@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-06-02 05:00, Joost Jager via bitcoin-dev wrote:
> the benefits of making the annex available in a
> non-structured form are both evident and immediate. By allowing
> developers to utilize the taproot annex without delay, we can take
> advantage of its features today,

Hi Joost,

Out of curiosity, what features and benefits are available today?  I 
know Greg Sanders wants to use annex data with LN-Symmetry[1], but 
that's dependent on a soft fork of SIGHASH_ANYPREVOUT.  I also heard you 
mention that it could allow putting arbitrary data into a witness 
without having to commit to that data beforehand, but that would only 
increase the efficiency of witness stuffing like ordinal inscriptions by 
only 0.4% (~2 bytes saved per 520 bytes pushed) and it'd still be 
required to create an output in order to spend it.

Is there some other way to use the annex today that would be beneficial 
to users of Bitcoin?

-Dave

[1] 
https://github.com/lightning/bolts/compare/master...instagibbs:bolts:eltoo_draft#diff-156a655274046c49e6b1c2a22546ed66366d3b8d97b8e9b34b45fe5bd8800ae2R119


------------------------------

Message: 3
Date: Fri, 2 Jun 2023 21:14:40 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: "David A. Harding" <dave@dtrt.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAB3F3Dtad8Fqb4R1phFU33SQPoL66nRz3rSHNbAaDSF=RN1NOA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hello Joost, David,

Thanks for the link to my ln-symmetry draft David. I'd also be curious as
to the usage you have in
mind Joost.

It's probably helpful to cite the most recent discussions on the topic,
which is probably
https://github.com/bitcoin-inquisition/bitcoin/pull/22 , where
bitcoin-inquisition has included
the `annexcarrier` option. I have a particular use for APO-enabled payment
channel designs
that doesn't require consensus meaning, so some effort was put in to try
something out there.

Attempting to summarize the linked PR:

I think the biggest remaining issue to this kind of idea, which is why I
didn't propose it for mainnet,
is the fact that BIP341/342 signature hashes do not cover *other* inputs'
annex fields, which we
briefly discussed here
https://github.com/bitcoin-inquisition/bitcoin/pull/22#discussion_r1143382264
.

This means that in a coinjoin like scenario, even if the other joining
parties prove they don't have any
crazy script paths, a malicious party can make the signed transaction into
a maximum sized transaction
package, causing griefing. The mitigation in the PR I linked was to limit
it to 126 bytes, basically punting
on the problem by making the grief vector small. Another solution could be
to make annex usage "opt-in"
by requiring all inputs to commit to an annex to be relay-standard. In this
case, you've opted into a possible
vector, but at least current usage patterns wouldn't be unduly affected.
For those who opt-in, perhaps the first
order of business would be to have a field that limits the total
transaction weight, by policy only?

Some logs related to that here:
https://gist.github.com/instagibbs/7406931d953fd96fea28f85be50fc7bb

Related discussion on possible BIP118 modifications to mitigate this in
tapscript-spending circumstances:
https://github.com/bitcoin-inquisition/bitcoin/issues/19

Anyways, curious to hear what people think and want to make sure everyone
is on the same page.

Best,
Greg

On Fri, Jun 2, 2023 at 9:08?PM David A. Harding via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> On 2023-06-02 05:00, Joost Jager via bitcoin-dev wrote:
> > the benefits of making the annex available in a
> > non-structured form are both evident and immediate. By allowing
> > developers to utilize the taproot annex without delay, we can take
> > advantage of its features today,
>
> Hi Joost,
>
> Out of curiosity, what features and benefits are available today?  I
> know Greg Sanders wants to use annex data with LN-Symmetry[1], but
> that's dependent on a soft fork of SIGHASH_ANYPREVOUT.  I also heard you
> mention that it could allow putting arbitrary data into a witness
> without having to commit to that data beforehand, but that would only
> increase the efficiency of witness stuffing like ordinal inscriptions by
> only 0.4% (~2 bytes saved per 520 bytes pushed) and it'd still be
> required to create an output in order to spend it.
>
> Is there some other way to use the annex today that would be beneficial
> to users of Bitcoin?
>
> -Dave
>
> [1]
>
> https://github.com/lightning/bolts/compare/master...instagibbs:bolts:eltoo_draft#diff-156a655274046c49e6b1c2a22546ed66366d3b8d97b8e9b34b45fe5bd8800ae2R119
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230602/7ff6b96e/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 4
******************************************
