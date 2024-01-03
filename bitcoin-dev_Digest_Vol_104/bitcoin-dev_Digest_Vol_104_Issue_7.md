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

   1. Re: Swift Activation - CTV (Ryan Breen)
   2. Re: Swift Activation - CTV (alicexbt)
   3. Re: Ordinal Inscription Size Limits (Brad Morrison)
   4. Re: Ordinal Inscription Size Limits (Erik Aronesty)


----------------------------------------------------------------------

Message: 1
Date: Tue, 2 Jan 2024 11:24:06 -0500
From: Ryan Breen <ryan@breen.xyz>
To: Michael Folkson <michaelfolkson@protonmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID: <5E185ABF-9F36-427D-B30D-D1E26D198469@breen.xyz>
Content-Type: text/plain; charset="utf-8"



> On Jan 2, 2024, at 10:50?AM, Michael Folkson via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> Your knowledge is incorrect. As far as I know in the getting on for 2 years since the first CTV activation talk/attempt literally no one has built out a CTV use case and demonstrated it on signet with the possible exception of James O'Beirne's OP_VAULT which requires other new opcodes in addition to CTV. I wish this wasn't the case. It is pitiful that we have these individuals (such as yourself) that are so convinced CTV should be activated but refuse to address any concerns raised by others and refuse to work on any of the speculated use cases, instead choosing to just beat the activation drum over and over again.

James O?Beirne built a CTV-only vault prototype[1], actually. Jeremy Rubin also built vaults and many other prototypes with his Sapio smart contracting language.[2]

So this assertion that CTV has had no use cases or prototypes built out for it is just not true.

[1]: https://github.com/jamesob/simple-ctv-vault
[2]: https://github.com/sapio-lang/sapio
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240102/7c973395/attachment.html>

------------------------------

Message: 2
Date: Tue, 02 Jan 2024 16:43:22 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Michael Folkson <michaelfolkson@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, Anthony Towns
	<aj@erisian.com.au>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<ISvX58I2-K-suhB33yY9A-zeW7xEFpF83jUgYClJH-nu469Gqa4V-YoikUfSb4BPVdFEHJh_JpH7b6OGPZdPQm_HI9_LtKRd_6vno0HdLRI=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

> Your knowledge is incorrect. As far as I know in the getting on for 2 years since the first CTV activation talk/attempt literally no one has built out a CTV use case and demonstrated it on signet with the possible exception of James O'Beirne's OP_VAULT which requires other new opcodes in addition to CTV. 

This is not true.

https://github.com/AdamISZ/pathcoin-poc

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

On Tuesday, January 2nd, 2024 at 1:52 PM, Michael Folkson via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> In the interests of time I'll just pick two to respond to but I don't agree with any of your points.
> 
> > Covenants allow trustless utxos sharing and also are needed for vaulting. The numerous use cases are documented, built out and on signet to my knowledge. Check out?utxos.org?for a good list
> 
> Your knowledge is incorrect. As far as I know in the getting on for 2 years since the first CTV activation talk/attempt literally no one has built out a CTV use case and demonstrated it on signet with the possible exception of James O'Beirne's OP_VAULT which requires other new opcodes in addition to CTV. I wish this wasn't the case. It is pitiful that we have these individuals (such as yourself) that are so convinced CTV should be activated but refuse to address any concerns raised by others and refuse to work on any of the speculated use cases, instead choosing to just beat the activation drum over and over again.
> 
> >?4. "Best tool for the job" is not the bar. "Safe for all" and "useful for some" is the bar. Like any opcodes or tech Bitcoin has deployed in the past. Changing the bar is not up for discussion.
> 
> If you want to avoid a chain split with an activation attempt (it is possible you don't care but if you do) you have to address concerns others have with a particular proposal. Just because Satoshi was able to make whatever changes he liked in the early days of Bitcoin's history and smaller groups of contributors then were able to activate changes without much scrutiny (Bitcoin was worth a fraction of what it is today and was only supporting a tiny ecosystem back then) doesn't mean we can do the same today. Appointing Erik as the new Satoshi who can make whatever changes he likes, who defines the bar with ultimate certainty and decides what is and what isn't up for discussion also isn't a viable option.
> 
> Thanks
> Michael
> 
> --
> Michael Folkson
> Email: michaelfolkson at protonmail.com
> GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
> 
> 
> Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
> 
> 
> On Monday, 1 January 2024 at 17:11, Erik Aronesty <erik@q32.com> wrote:
> 
> 
> > 1. Claiming that something that isn't activated (unusable) isn't used as a non-argument
> > 2. Talking about activation methods is orthogonal. Bip8 is fine.
> > 
> > 3. Covenants allow trustless utxos sharing and also are needed for vaulting. The numerous use cases are documented, built out and on signet to my knowledge. Check out utxos.org for a good list
> > 
> > 3. No need to discuss wild extremes that are unrelated to ctvs well documented utility. Plus multi-sig allows governments to encumber (or accidentally ruin) destination addresses just like covenants.
> > 
> > 4. "Best tool for the job" is not the bar. "Safe for all" and "useful for some" is the bar. Like any opcodes or tech Bitcoin has deployed in the past. Changing the bar is not up for discussion.
> > 
> > 
> > CTV has already been demonstrated "useful for some". The question that needs to be answered is whether there are any specific objections to safety.
> > 
> > 
> > 
> > 
> > 
> > 
> > 
> > 
> > 
> > On Mon, Jan 1, 2024, 11:37 AM Michael Folkson <michaelfolkson@protonmail.com> wrote:
> > 
> > > Hi Erik
> > > 
> > > 
> > > > So what exactly are the risks of CTV over multi-sig?
> > > 
> > > 
> > > It is a strange comparison. Multisig is active onchain and is being used today for all sorts of things including Lightning and setups that address risk of single key loss or malicious signing. When discussing risks of CTV there are all sorts of risks that don't apply to multisig. These include that it is never used for any of its speculated use cases (multisig is being used today), other proposals end up being used instead of it (I'm not sure there were or are competing proposals so that multisig stops being used, MuSig2 maybe?), chain split risks with activation if there isn't consensus to activate it etc. Plus usage of complex (non covenant) scripts that fully utilize Taproot trees is still low today. Going straight to covenants (imposing restrictions on where funds can be sent) and not bothering with imposing all the restrictions you'd like on how funds can be spent in the first place seems to me to be putting the cart before the horse. Covenants don't ultimately solve the k
 ey management issue, they just move it from the pre spending phase to the post spending phase. So the benefits (although non-zero) aren't as obvious as some of the covenant advocates are suggesting. And although CTV is a limited covenant (some argue too limited) covenants taken to wild extremes could create all sorts of second order effects where funds can't be spent because of complex combinations of covenants. Even the strongest CTV proponent seems to suggest that the introduction of covenants wouldn't end with CTV.
> > > 
> > > 
> > > The way to reduce implementation risk for a use case of a particular proposal is to build out that use case and see if CTV is the best tool for the job. Repeatedly trying to activate CTV when there isn't consensus for it to be activated does not reduce that implementation risk in any way, shape or form.
> > > 
> > > 
> > > Thanks
> > > Michael
> > > 
> > > 
> > > --
> > > Michael Folkson
> > > Email: michaelfolkson at protonmail.com
> > > GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
> > > 
> > > 
> > > Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
> > > 
> > > 
> > > On Saturday, 30 December 2023 at 08:59, Erik Aronesty via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> > > 
> > > 
> > > > So what exactly are the risks of CTV over multi-sig?
> > > > 
> > > > 
> > > > > 
> > > > > 


------------------------------

Message: 3
Date: Wed, 03 Jan 2024 01:11:58 -0800
From: Brad Morrison <bradmorrison@sonic.net>
To: Erik Aronesty <erik@q32.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID: <fea6d7f6cbd7b58c052fb993e443a751@sonic.net>
Content-Type: text/plain; charset="us-ascii"

Erik/all, 

Are you saying that node capacity is the primary technical limiting
factor to increasing adoption of bitcoin payments? 

UBER & Lyft payments are actually poor examples because they are not
regular/monthly and I should not have used them (unless refilling
existing accounts, like gift cards). But utility bills would be a much
better example of an opportunity for bitcoin payments to compete with
existing credit card payment systems because processing timing has the
potential to be less urgent. 

Sharing UTXOs seems pretty minor compared to lowering transaction costs.


Brad

On 2024-01-01 08:08, Erik Aronesty wrote:

>> . 
>> 
>> In the USA, where I am, large businesses like UBER, Lyft, and many major telecom, cable, & electric utilities process huge volumes of regular and irregular credit card payments on a monthly basis. Almost none oft hose transactions are completed in bitcoin.
> 
> Unfortunately block size is not the limiting factor 
> 
> Main chain transactions have to be broadcast and stored on every node in the network which, as you know, cannot scale to the level of Uber payments 
> 
> Lighting and possibly ark are solutions to this problem 
> 
> Both require covenant tech of some kind to scale properly (nonrecursive is fine) 
> 
> Covenant tech (any will do, arguing about which is bike shedding at this point) allows people to share utxos and yet still maintain sovereignty over their assets 
> 
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240103/273cd189/attachment.html>

------------------------------

Message: 4
Date: Wed, 3 Jan 2024 08:05:42 -0500
From: Erik Aronesty <erik@q32.com>
To: Brad Morrison <bradmorrison@sonic.net>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID:
	<CAJowKg+Sq+VK-K6gdHFLFt3zM8XL0xGDc=PF-jG88neadTiDqg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Onchain capacity is a red herring.  There are so many problems with it and
we don't need to go into it here if it's already been beaten to death.


 What we need are the op codes necessary to create a trustless,
disconnected graph of layer two solution.

We all know that some form of covenant technology is the right way to do
this

Some way of revokably sharing UTXOs, such that the incentives keep
coordinators in line

That can get us to global scale on a layer two that isn't custodial







On Wed, Jan 3, 2024, 4:12 AM Brad Morrison <bradmorrison@sonic.net> wrote:

> Erik/all,
>
> Are you saying that node capacity is the primary technical limiting factor
> to increasing adoption of bitcoin payments?
>
> UBER & Lyft payments are actually poor examples because they are not
> regular/monthly and I should not have used them (unless refilling existing
> accounts, like gift cards). But utility bills would be a much better
> example of an opportunity for bitcoin payments to compete with existing
> credit card payment systems because processing timing has the potential to
> be less urgent.
>
> Sharing UTXOs seems pretty minor compared to lowering transaction costs.
>
> Brad
>
>
>
> On 2024-01-01 08:08, Erik Aronesty wrote:
>
> .
>>
>> In the USA, where I am, large businesses like UBER, Lyft, and many major
>> telecom, cable, & electric utilities process huge volumes of regular and
>> irregular credit card payments on a monthly basis. Almost none oft hose
>> transactions are completed in bitcoin.
>>
>
>
> Unfortunately block size is not the limiting factor
>
> Main chain transactions have to be broadcast and stored on every node in
> the network which, as you know, cannot scale to the level of Uber payments
>
> Lighting and possibly ark are solutions to this problem
>
> Both require covenant tech of some kind to scale properly (nonrecursive is
> fine)
>
> Covenant tech (any will do, arguing about which is bike shedding at this
> point) allows people to share utxos and yet still maintain sovereignty over
> their assets
>
>
>
>
>
>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240103/0a4d4b7e/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 7
*******************************************
