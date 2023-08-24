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

   1. Re: Standardisation of an unstructured taproot annex
      (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Mon, 19 Jun 2023 02:14:10 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Greg Sanders <gsanders87@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CALZpt+EKC840oQkL_Jd_BaKTJRsZzsZkPKHA32E+7i=gbwOmSQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Greg,

> Going to need a citation for this.

Sorry for the confusion, this was in reply to Joost's point on "Opt-in
annex (every input must commit to an annex even if its is empty) -> make
sure existing multi-party protocols remain unaffected"

What is unclear to me is if we're talking about opt-in of non-deployed-yet
protocols like the pre-signed vaults or deployed protocols like
coinjoin/lightning spending P2TR outputs, where a counterparty script spend
path can inflate the witness, and we would like to commit *now* to avoid
future interferences. E.g 0-conf dual-funding and we loosened the limit
from 126 bytes to 256, the worst-case liquidity griefing is not the same
anymore.

If the opt-in mechanism we're talking about is just adding an annex for
non-deployed-yet protocols as a script spend path of a currently deployed
protocol could always be opted-in to the new annex policy through script
spend path in the context of collaborative added inputs, no ?

> People should really not be building protocols that are meant to go into
production on top of undeveloped upgrade hooks,
and we should not be encumbered by these premature choices if so.

> People should really not be building protocols that are meant to go into
production on top of undeveloped upgrade hooks,
> and we should not be encumbered by these premature choices if so. Maybe
I'm misunderstanding, which is why a citation
> would be handy.

Yes ideally we should not be encumbered by these premature choices. Still
if those use-cases catched up in terms of economic weight, the coordination
cost of deploying a new policy might be prohibitive, or require very long
periods, somehow like we're seeing with mempoolfullrbf. And I don't think
we can say the use-cases would be illegitimate, or that base-layer policy
should always have the last word. In the example of lightning, we're doing
major re-work of the mempool, partially to improve lightning operations.
Personally, I think we should care more about sound and "firewalled"
signaling and upgrading mechanisms that let us deploy new policy rules for
new use-cases more smoothly.

Best,
Antoine

Le dim. 18 juin 2023 ? 21:41, Greg Sanders <gsanders87@gmail.com> a ?crit :

> Hi Antoine,
>
> > If I understand correctly, this would require modifying current Taproot
> support on the Lightning-side, where all P2TR spends must add an annex and
> commit to it in the BIP341 signature digest.
>
> huh?
>
> Going to need a citation for this.
>
> People should really not be building protocols that are meant to go into
> production on top of undeveloped upgrade hooks,
> and we should not be encumbered by these premature choices if so. Maybe
> I'm misunderstanding, which is why a citation
> would be handy.
>
> Best,
> Greg
>
> On Sun, Jun 18, 2023 at 4:32?PM Antoine Riard <antoine.riard@gmail.com>
> wrote:
>
>> Hi all,
>>
>> > * Opt-in annex (every input must commit to an annex even if its is
>> empty) -> make sure existing multi-party protocols remain unaffected
>>
>> By requiring every input to commit to an annex even if it is empty, do
>> you mean rejecting a transaction where the minimal annex with its 0x50 tag
>> is absent ?
>>
>> If I understand correctly, this would require modifying current Taproot
>> support on the Lightning-side, where all P2TR spends must add an annex and
>> commit to it in the BIP341 signature digest. This would be quite a
>> mandatory upgrade for Lightning nodes, as failure to do so would break
>> propagations of their `option_taproot` channel transactions.
>>
>> > * Limit maximum size of the value to 256 bytes -> protect opt-in users
>>
>> There is another approach where the maximum size/weight of the
>> witness/transaction is introduced as a TLV record itself:
>> https://github.com/bitcoin-inquisition/bitcoin/pull/28
>>
>> Note this branch also implements the "only allow tlv record 0" with the
>> TLV format from bips #1381.
>>
>> Best,
>> Antoine
>>
>> Le ven. 16 juin 2023 ? 14:31, Greg Sanders via bitcoin-dev <
>> bitcoin-dev@lists.linuxfoundation.org> a ?crit :
>>
>>> Hi Joost,
>>>
>>> I haven't thought a ton about the specific TLV format, but that seems
>>> like a reasonable place to start as it shouldn't unduly
>>> impact current users, and is pretty simple from an accounting
>>> perspective.
>>> It also can be further relaxed in the future if we so decide by using
>>> max tx size policy "hints" in an annex field.
>>>
>>> I'll let others chime in at this point!
>>>
>>> Cheers,
>>> Greg
>>>
>>> On Fri, Jun 16, 2023 at 7:27?AM Joost Jager <joost.jager@gmail.com>
>>> wrote:
>>>
>>>> Hi Greg,
>>>>
>>>> On Thu, Jun 15, 2023 at 12:39?PM Greg Sanders <gsanders87@gmail.com>
>>>> wrote:
>>>>
>>>>> > Would it then still be necessary to restrict the annex to a maximum
>>>>> size?
>>>>>
>>>>> I think it's worth thinking about to protect the opt-in users, and can
>>>>> also be used for other anti-pinning efforts(though clearly not sufficient
>>>>> by itself for the many many pinning vectors we have :) )
>>>>>
>>>>
>>>> Thinking about the most restrictive policy that would still enable
>>>> annex-vaults (which I believe has great potential for improving bitcoin
>>>> custody) and is in line with work already done, I get to:
>>>>
>>>> * Opt-in annex (every input must commit to an annex even if its is
>>>> empty) -> make sure existing multi-party protocols remain unaffected
>>>> * Tlv format as defined in https://github.com/bitcoin/bips/pull/1381
>>>> -> future extensibility
>>>> * Only allow tlv record 0 - unstructured data -> future extensibility
>>>> * Limit maximum size of the value to 256 bytes -> protect opt-in users
>>>>
>>>> Unfortunately the limit of 126 bytes in
>>>> https://github.com/bitcoin-inquisition/bitcoin/pull/22 isn't
>>>> sufficient for these types of vaults. If there are two presigned txes
>>>> (unvault and emergency), those signatures would already take up 2*64=128
>>>> bytes. Then you also want to store 32 bytes for the ephemeral key itself as
>>>> the key can't be reconstructed from the schnorr signature. The remaining
>>>> bytes could be used for a third presigned tx and/or additional vault
>>>> parameters.
>>>>
>>>> Can you think of remaining practical objections to making the annex
>>>> standard under the conditions listed above?
>>>>
>>>> Joost
>>>>
>>>>> _______________________________________________
>>> bitcoin-dev mailing list
>>> bitcoin-dev@lists.linuxfoundation.org
>>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230619/adfbce5a/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 22
*******************************************
