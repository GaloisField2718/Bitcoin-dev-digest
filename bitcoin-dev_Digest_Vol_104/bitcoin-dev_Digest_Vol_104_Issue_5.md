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

   1. Re: Swift Activation - CTV (Michael Folkson)


----------------------------------------------------------------------

Message: 1
Date: Tue, 02 Jan 2024 13:52:20 +0000
From: Michael Folkson <michaelfolkson@protonmail.com>
To: Erik Aronesty <erik@q32.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Anthony Towns
	<aj@erisian.com.au>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<Zzpp9sp69_QmkUre4YUawBxOLECIfHHUf_OoD8UXXZ8Xwtmr5R62_rlGV2iwLivkST-vWusc0X9horY9qHEHKP2g4GR2ppCAuIE57VANUP0=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

In the interests of time I'll just pick two to respond to but I don't agree with any of your points.

> Covenants allow trustless utxos sharing and also are needed for vaulting. The numerous use cases are documented, built out and on signet to my knowledge. Check out[utxos.org](http://utxos.org/)for a good list

Your knowledge is incorrect. As far as I know in the getting on for 2 years since the first CTV activation talk/attempt literally no one has built out a CTV use case and demonstrated it on signet with the possible exception of James O'Beirne's OP_VAULT which requires other new opcodes in addition to CTV. I wish this wasn't the case. It is pitiful that we have these individuals (such as yourself) that are so convinced CTV should be activated but refuse to address any concerns raised by others and refuse to work on any of the speculated use cases, instead choosing to just beat the activation drum over and over again.

> 4. "Best tool for the job" is not the bar. "Safe for all" and "useful for some" is the bar. Like any opcodes or tech Bitcoin has deployed in the past. Changing the bar is not up for discussion.

If you want to avoid a chain split with an activation attempt (it is possible you don't care but if you do) you have to address concerns others have with a particular proposal. Just because Satoshi was able to make whatever changes he liked in the early days of Bitcoin's history and smaller groups of contributors then were able to activate changes without much scrutiny (Bitcoin was worth a fraction of what it is today and was only supporting a tiny ecosystem back then) doesn't mean we can do the same today. Appointing Erik as the new Satoshi who can make whatever changes he likes, who defines the bar with ultimate certainty and decides what is and what isn't up for discussion also isn't a viable option.

Thanks
Michael

--
Michael Folkson
Email: michaelfolkson at [protonmail.com](http://protonmail.com/)
GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F

Learn about Bitcoin: https://www.youtube.com/@portofbitcoin

On Monday, 1 January 2024 at 17:11, Erik Aronesty <erik@q32.com> wrote:

> 1. Claiming that something that isn't activated (unusable) isn't used as a non-argument
>
> 2. Talking about activation methods is orthogonal. Bip8 is fine.
>
> 3. Covenants allow trustless utxos sharing and also are needed for vaulting. The numerous use cases are documented, built out and on signet to my knowledge. Check out utxos.org for a good list
>
> 3. No need to discuss wild extremes that are unrelated to ctvs well documented utility. Plus multi-sig allows governments to encumber (or accidentally ruin) destination addresses just like covenants.
>
> 4. "Best tool for the job" is not the bar. "Safe for all" and "useful for some" is the bar. Like any opcodes or tech Bitcoin has deployed in the past. Changing the bar is not up for discussion.
>
> CTV has already been demonstrated "useful for some". The question that needs to be answered is whether there are any specific objections to safety.
>
> On Mon, Jan 1, 2024, 11:37 AM Michael Folkson <michaelfolkson@protonmail.com> wrote:
>
>> Hi Erik
>>
>>> So what exactly are the risks of CTV over multi-sig?
>>
>> It is a strange comparison. Multisig is active onchain and is being used today for all sorts of things including Lightning and setups that address risk of single key loss or malicious signing. When discussing risks of CTV there are all sorts of risks that don't apply to multisig. These include that it is never used for any of its speculated use cases (multisig is being used today), other proposals end up being used instead of it (I'm not sure there were or are competing proposals so that multisig stops being used, MuSig2 maybe?), chain split risks with activation if there isn't consensus to activate it etc. Plus usage of complex (non covenant) scripts that fully utilize Taproot trees is still low today. Going straight to covenants (imposing restrictions on where? funds can be sent) and not bothering with imposing all the restrictions you'd like on how? funds can be spent in the first place seems to me to be putting the cart before the horse. Covenants don't ultimately solve the ke
 y management issue, they just move it from the pre spending phase to the post spending phase. So the benefits (although non-zero) aren't as obvious as some of the covenant advocates are suggesting. And although CTV is a limited covenant (some argue too limited) covenants taken to wild extremes could create all sorts of second order effects where funds can't be spent because of complex combinations of covenants. Even the strongest CTV proponent seems to suggest that the introduction of covenants wouldn't end with CTV.
>>
>> The way to reduce implementation risk for a use case of a particular proposal is to build out that use case and see if CTV is the best tool for the job. Repeatedly trying to activate CTV when there isn't consensus for it to be activated does not reduce that implementation risk in any way, shape or form.
>>
>> Thanks
>> Michael
>>
>> --
>> Michael Folkson
>> Email: michaelfolkson at [protonmail.com](http://protonmail.com/)
>> GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
>>
>> Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
>>
>> On Saturday, 30 December 2023 at 08:59, Erik Aronesty via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>>
>>> So what exactly are the risks of CTV over multi-sig?
>>>
>>>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240102/e0d6d57d/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 5
*******************************************
