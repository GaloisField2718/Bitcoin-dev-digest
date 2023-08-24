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
   2. Re: Standardisation of an unstructured taproot annex
      (Greg Sanders)


----------------------------------------------------------------------

Message: 1
Date: Fri, 16 Jun 2023 13:26:34 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV_vPW1vBSfTeDOU_FecHk1sX2=uGUFYS9enC=hwvLpVQA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Greg,

On Thu, Jun 15, 2023 at 12:39?PM Greg Sanders <gsanders87@gmail.com> wrote:

> > Would it then still be necessary to restrict the annex to a maximum size?
>
> I think it's worth thinking about to protect the opt-in users, and can
> also be used for other anti-pinning efforts(though clearly not sufficient
> by itself for the many many pinning vectors we have :) )
>

Thinking about the most restrictive policy that would still enable
annex-vaults (which I believe has great potential for improving bitcoin
custody) and is in line with work already done, I get to:

* Opt-in annex (every input must commit to an annex even if its is empty)
-> make sure existing multi-party protocols remain unaffected
* Tlv format as defined in https://github.com/bitcoin/bips/pull/1381 ->
future extensibility
* Only allow tlv record 0 - unstructured data -> future extensibility
* Limit maximum size of the value to 256 bytes -> protect opt-in users

Unfortunately the limit of 126 bytes in
https://github.com/bitcoin-inquisition/bitcoin/pull/22 isn't sufficient for
these types of vaults. If there are two presigned txes (unvault and
emergency), those signatures would already take up 2*64=128 bytes. Then you
also want to store 32 bytes for the ephemeral key itself as the key can't
be reconstructed from the schnorr signature. The remaining bytes could be
used for a third presigned tx and/or additional vault parameters.

Can you think of remaining practical objections to making the annex
standard under the conditions listed above?

Joost

>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230616/4e1a529e/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 16 Jun 2023 09:30:46 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Joost Jager <joost.jager@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAB3F3DszC3ZDDYrN_jzoU+hZ021TfmCRoVTZWCpzOmH4F_anwg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Joost,

I haven't thought a ton about the specific TLV format, but that seems like
a reasonable place to start as it shouldn't unduly
impact current users, and is pretty simple from an accounting perspective.
It also can be further relaxed in the future if we so decide by using max
tx size policy "hints" in an annex field.

I'll let others chime in at this point!

Cheers,
Greg

On Fri, Jun 16, 2023 at 7:27?AM Joost Jager <joost.jager@gmail.com> wrote:

> Hi Greg,
>
> On Thu, Jun 15, 2023 at 12:39?PM Greg Sanders <gsanders87@gmail.com>
> wrote:
>
>> > Would it then still be necessary to restrict the annex to a maximum
>> size?
>>
>> I think it's worth thinking about to protect the opt-in users, and can
>> also be used for other anti-pinning efforts(though clearly not sufficient
>> by itself for the many many pinning vectors we have :) )
>>
>
> Thinking about the most restrictive policy that would still enable
> annex-vaults (which I believe has great potential for improving bitcoin
> custody) and is in line with work already done, I get to:
>
> * Opt-in annex (every input must commit to an annex even if its is empty)
> -> make sure existing multi-party protocols remain unaffected
> * Tlv format as defined in https://github.com/bitcoin/bips/pull/1381 ->
> future extensibility
> * Only allow tlv record 0 - unstructured data -> future extensibility
> * Limit maximum size of the value to 256 bytes -> protect opt-in users
>
> Unfortunately the limit of 126 bytes in
> https://github.com/bitcoin-inquisition/bitcoin/pull/22 isn't sufficient
> for these types of vaults. If there are two presigned txes (unvault and
> emergency), those signatures would already take up 2*64=128 bytes. Then you
> also want to store 32 bytes for the ephemeral key itself as the key can't
> be reconstructed from the schnorr signature. The remaining bytes could be
> used for a third presigned tx and/or additional vault parameters.
>
> Can you think of remaining practical objections to making the annex
> standard under the conditions listed above?
>
> Joost
>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230616/e427c0b7/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 20
*******************************************
