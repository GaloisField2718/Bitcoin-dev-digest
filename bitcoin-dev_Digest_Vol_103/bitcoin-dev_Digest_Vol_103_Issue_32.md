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

   1. Re: Ordinal Inscription Size Limits (Nagaev Boris)
   2. Re: Scaling Lightning Safely With Feerate-Dependent	Timelocks
      (Nagaev Boris)
   3. Re: Scaling Lightning Safely With Feerate-Dependent	Timelocks
      (Nagaev Boris)
   4. Re: Swift Activation - CTV (Erik Aronesty)
   5. Re: Ordinal Inscription Size Limits (Erik Aronesty)


----------------------------------------------------------------------

Message: 1
Date: Fri, 29 Dec 2023 16:01:52 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: Greg Tonoski <gregtonoski@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID:
	<CAFC_Vt7r_HA73UBmDdYsjxMirLfPb3K+3do_NwS-2o=Jsmw0gA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Fri, Dec 29, 2023 at 1:34?PM Greg Tonoski via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> There is significant difference when storing data as dummy signatures
> (or OP_RETURN) which is much more expensive than (discounted) witness.
> Witness would not have been chosen as the storage of arbitrary data if
> it cost as much as alternatives, e.g. OP_RETURN.

Hi Greg!

How about storing data in multisig signatures? Make a 1/n multisig and
store the data in (n-1) dummy public keys. It is stored in witness and
is quite efficient and hard to filter out only if together with
legitimate multisigs.

Another smart place for hidden data is Merkle proof in Taproot. The
depth is limited to 128 levels, so put 1 valid leaf and add data to
127 fake elements to calculate the Merkle root.

I think there are more ways like this. If the current place is banned,
they can always waste money in other parts of bitcoin transactions. It
is impossible to stop someone who can afford to waste money from doing
it. (Well, it is, but not in a decentralized voluntary way of
Bitcoin.) My approach is just to wait for them to run out of money and
use Lightning Network for payments meanwhile.

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 2
Date: Fri, 29 Dec 2023 22:17:01 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: "David A. Harding" <dave@dtrt.org>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent	Timelocks
Message-ID:
	<CAFC_Vt6yk2MwkUhiBKyGmOArVrU9VCdf27qR8wDMMOz_ONjt=A@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hey David!

On Fri, Dec 29, 2023 at 9:37?PM David A. Harding via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> We can't prevent people from paying out of band, but we can ensure that
> the easiest and most effective way to pay for a transaction is through
> in-band fees and transactions that are relayed to every miner who is
> interested in them.  If we fail at that, I think Bitcoin losing its
> censorship resistance will be inevitable.  LN, coinpools, and channel
> factories all strongly depend on Bitcoin transactions not being
> censored, so I don't think any security is lost by redesigning them to
> additionally depend on reasonably accurate in-band fee statistics.

Feerate-Dependent Timelocks do create incentives to accept out-of-band
fees to decrease in-band fees and speed up mining of transactions
using FDT! Miners can make a 5% discount on fees paid out-of-band and
many people will use it. Observed fees decrease and FDT transactions
mature faster. It is beneficial for both parties involved: senders of
transactions save 5% on fees, miners get FDT transactions mined faster
and get more profits (for the sake of example more than 5%).

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 3
Date: Sat, 30 Dec 2023 00:20:37 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning Safely With
	Feerate-Dependent	Timelocks
Message-ID:
	<CAFC_Vt5iEvCMgUGAEgSYdd2CByR3Q3M=9tf8Uz7TK1oCPHXRvA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Sat, Dec 30, 2023 at 12:11?AM David A. Harding <dave@dtrt.org> wrote:
>
> On 2023-12-29 15:17, Nagaev Boris wrote:
> > Feerate-Dependent Timelocks do create incentives to accept out-of-band
> > fees to decrease in-band fees and speed up mining of transactions
> > using FDT! Miners can make a 5% discount on fees paid out-of-band and
> > many people will use it. Observed fees decrease and FDT transactions
> > mature faster. It is beneficial for both parties involved: senders of
> > transactions save 5% on fees, miners get FDT transactions mined faster
> > and get more profits (for the sake of example more than 5%).
>
> Hi Nagaev,
>
> That's an interesting idea, but I don't think that it works due to the
> free rider problem: miner Alice offers a 5% discount on fees paid out of
> band now in the hopes of collecting more than 5% in extra fees later due
> to increased urgency from users that depended on FDTs.  However,
> sometimes the person who actually collects extra fees is miner Bob who
> never offered a 5% discount.  By not offering a discount, Bob earns more
> money on average per block than Alice (all other things being equal),
> eventually forcing her to stop offering the discount or to leave the
> market.
>
> Additionally, if nearly everyone was paying discounted fees out of band,
> participants in contract protocols using FDTs would know to use
> proportionally higher FDT amounts (e.g. 5% over their actual desired
> fee), negating the benefit to miners of offering discounted fees.
>
> -Dave

Good points. It makes sense!

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 4
Date: Sat, 30 Dec 2023 01:59:45 -0700
From: Erik Aronesty <erik@q32.com>
To: Anthony Towns <aj@erisian.com.au>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Swift Activation - CTV
Message-ID:
	<CAJowKg+VR5sYkxOtfeMeaW_ZiU8=6YC_T-21jSBk9VuFO1739g@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

So what exactly are the risks of CTV over multi-sig?


>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231230/9b21d98f/attachment.html>

------------------------------

Message: 5
Date: Sat, 30 Dec 2023 02:58:41 -0700
From: Erik Aronesty <erik@q32.com>
To: Greg Tonoski <gregtonoski@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinal Inscription Size Limits
Message-ID:
	<CAJowKgJ8n0GFj3S88qW+rk2RcLg-1JH9aL22YtTB-55EEQzsYw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Bitcoin already has a spam prevention system called "fees".   I don't
believe it's insufficient.  The only issue is the stochastic nature of its
effectiveness

Which can be resolved with things like payment pools, tree payments (
https://utxos.org/uses/scaling/), etc.



On Fri, Dec 29, 2023, 9:33 AM Greg Tonoski via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> > Unfortunately, as near as I can tell there is no sensible way to
> > prevent people from storing arbitrary data in witnesses ...
>
> To prevent "from storing arbitrary data in witnesses" is the extreme
> case of the size limit discussed in this thread. Let's consider it along
> with other (less radical) options in order not to lose perspective,
> perhaps.
>
> > ...without incentivizing even worse behavior and/or breaking
> > legitimate use cases.
>
> I can't find evidence that would support the hypothesis. There had not
> been "even worse behavior and/or breaking legitimate use cases" observed
> before witnesses inception. The measure would probably restore
> incentives structure from the past.
>
> As a matter of fact, it is the current incentive structure that poses
> the problem - incentivizes worse behavior ("this sort of data is toxic
> to the network") and breaks legitimate use cases like a simple transfer
> of BTC.
>
> > If we ban "useless data" then it would be easy for would-be data
> > storers to instead embed their data inside "useful" data such as dummy
> > signatures or public keys.
>
> There is significant difference when storing data as dummy signatures
> (or OP_RETURN) which is much more expensive than (discounted) witness.
> Witness would not have been chosen as the storage of arbitrary data if
> it cost as much as alternatives, e.g. OP_RETURN.
>
> Also, banning "useless data" seems to be not the only option suggested
> by the author who asked about imposing "a size limit similar to OP_RETURN".
>
> > But from a technical point of view, I don't see any principled way to
> > stop this.
>
> Let's discuss ways that bring improvement rather than inexistence of a
> perfect technical solution that would have stopped "toxic data"/"crap on
> the chain". There are at least a few:
> - https://github.com/bitcoin/bitcoin/pull/28408
> - https://github.com/bitcoin/bitcoin/issues/29146
> - deprecate OP_IF opcode.
>
> I feel like the elephant in the room has been brought up. Do you want to
> maintain Bitcoin without spam or a can't-stop-crap alternative, everybody?
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231230/01f04983/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 32
********************************************
