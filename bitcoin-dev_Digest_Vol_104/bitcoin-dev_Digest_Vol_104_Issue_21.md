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

   1. Re: BIP process friction (David A. Harding)
   2. Re: BIP process friction (alicexbt)
   3. Re: BIP process friction (Peter Todd)
   4. Re: BIP process friction (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Thu, 18 Jan 2024 05:41:14 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Anthony Towns <aj@erisian.com.au>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID: <6f3ce219d7df09c80e8063579555de06@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2024-01-16 16:42, Anthony Towns via bitcoin-dev wrote:
> I'm switching inquisition over to having a dedicated "IANA"-ish
> thing that's independent of BIP process nonsense. It's at:
> 
>  * https://github.com/bitcoin-inquisition/binana
> 
> If people want to use it for bitcoin-related proposals that don't have
> anything to do with inquisition, that's fine

Thank you for doing this!

Question: is there a recommended way to produce a shorter identifier for 
inline use in reading material?  For example, for proposal 
BIN-2024-0001-000, I'm thinking:

- BIN24-1 (references whatever the current version of the proposal is)
- BIN24-1.0 (references revision 0)

I think that doesn't look too bad even if there are over 100 proposals a 
year, with some of them getting into over a hundred revisions:

- BIN24-123
- BIN24-123.123

Rationale:

- Using "BIN" for both full-length and shortened versions makes it 
explicit which document set we're talking about

- Eliminating the first dash losslessly saves space and reduces visual 
clutter

- Shortening a four-digit year to two digits works for the next 75 
years.  Adding more digits as necessary after that won't produce any 
ambiguity

- Although I'd like to eliminate the second dash, and it wouldn't 
introduce any ambiguity in machine parsing for the next 175 years, I 
think it would lead to people interpreting numbers incorrectly.  E.g., 
"BIN241" would be read "BIN two-hundred fourty-one" instead of a more 
desirable "BIN twenty-four dash one"

- Eliminating prefix zeroes in the proposal and revision numbers 
losslessly saves space and reduces visual clutter

- A decimal point between the proposal number and revision number 
creates less visual clutter than the third dash and still conveys the 
intended meaning

- Overall, for the typical case I'd expect---BIN proposals numbered 1-99 
with no mention of revision---this produces strings only one or two or 
characters longer than a typical modern BIP number in shortened format, 
e.g. BIN24-12 versus BIP123.

Thoughts?

-Dave


------------------------------

Message: 2
Date: Thu, 18 Jan 2024 16:47:33 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Anthony Towns <aj@erisian.com.au>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID:
	<jukOxw5FcU6syw4uF2sbFIMPK0RN1nUbUmu5G4zG4w5ZoU2gLOB2vGwHZ3_vEYyJQUQQDIc3w-C0t1anDDAz1tTry6-nCjG5a3nttuoARQc=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi AJ,

I like the idea and agree with everything you shared in the email except one thing:

> So I'm switching inquisition over to having a dedicated "IANA"-ish
> thing that's independent of BIP process nonsense. It's at:
> 
> * https://github.com/bitcoin-inquisition/binana

I think "authority" is a strong word especially in bitcoin and this process could even work with BINN (Bitcoin Inquisition Numbers And Names). IANA (a function of ICANN) is different thing altogether which was founded by US government.

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

On Wednesday, January 17th, 2024 at 2:42 AM, Anthony Towns via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Hi all,
> 
> Just under three years ago there was some discussion about the BIPs repo,
> with the result that Kalle became a BIPs editor in addition to Luke, eg:
> 
> * https://gnusha.org/bitcoin-core-dev/2021-04-22.log
> * https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-April/018859.html
> 
> It remains, however, quite hard to get BIPs merged into the repo, eg
> the following PRs have been open for quite some time:
> 
> * #1408: Ordinal Numbers; opened 2023-01-21, editors comments:
> Kalle:
> https://github.com/bitcoin/bips/pull/1408#issuecomment-1421641390
> https://github.com/bitcoin/bips/pull/1408#issuecomment-1435389476
> 
> Luke:
> https://github.com/bitcoin/bips/pull/1408#issuecomment-1429146796
> https://github.com/bitcoin/bips/pull/1408#issuecomment-1438831607
> https://github.com/bitcoin/bips/pull/1408#issuecomment-1465016571
> 
> * #1489: Taproot Assets Protocol; opened 2023-09-07, editors comments:
> Kalle: https://github.com/bitcoin/bips/pull/1489#issuecomment-1855079626
> Luke: https://github.com/bitcoin/bips/pull/1489#issuecomment-1869721535j
> 
> * #1500: OP_TXHASH; opened 2023-09-30, editors comments:
> Luke:
> https://github.com/bitcoin/bips/pull/1500#pullrequestreview-1796550166
> https://twitter.com/LukeDashjr/status/1735701932520382839
> 
> The range of acceptable BIPs seems to also be becoming more limited,
> such that mempool/relay policy is out of scope:
> 
> * https://github.com/bitcoin/bips/pull/1524#issuecomment-1869734387
> 
> Despite having two editors, only Luke seems to be able to assign new
> numbers to BIPs, eg:
> 
> * https://github.com/bitcoin/bips/pull/1458#issuecomment-1597917780
> 
> There's also been some not very productive delays due to the editors
> wanting backwards compatibility sections even if authors don't think
> that's necessary, eg:
> 
> * https://github.com/bitcoin/bips/pull/1372#issuecomment-1439132867
> 
> Even working out whether to go back to allowing markdown as a text format
> is a multi-month slog due to process confusion:
> 
> * https://github.com/bitcoin/bips/pull/1504
> 
> Anyway, while it's not totally dysfunctional, it's very high friction.
> 
> There are a variety of recent proposals that have PRs open against
> inquisition; up until now I've been suggesting people write a BIP, and
> have been keying off the BIP number to signal activation. But that just
> seems to be introducing friction, when all I need is a way of linking
> an arbitrary number to a spec.
> 
> So I'm switching inquisition over to having a dedicated "IANA"-ish
> thing that's independent of BIP process nonsense. It's at:
> 
> * https://github.com/bitcoin-inquisition/binana
> 
> If people want to use it for bitcoin-related proposals that don't have
> anything to do with inquisition, that's fine; I'm intending to apply the
> policies I think the BIPs repo should be using, so feel free to open a PR,
> even if you already know I think your idea is BS on its merits. If someone
> wants to write an automatic-merge-bot for me, that'd also be great.
> 
> If someone wants to reform the BIPs repo itself so it works better,
> that'd be even better, but I'm not volunteering for that fight.
> 
> Cheers,
> aj
> 
> (It's called "numbers and names" primarily because that way the acronym
> amuses me, but also in case inquisition eventually needs an authoritative
> dictionary for what "cat" or "txhash" or similar terms refer to)
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 3
Date: Thu, 18 Jan 2024 17:42:03 +0000
From: Peter Todd <pete@petertodd.org>
To: alicexbt <alicexbt@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: Anthony Towns <aj@erisian.com.au>
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID: <Zali61MYQBz/cLbY@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Thu, Jan 18, 2024 at 04:47:33PM +0000, alicexbt via bitcoin-dev wrote:
> Hi AJ,
> 
> I like the idea and agree with everything you shared in the email except one thing:
> 
> > So I'm switching inquisition over to having a dedicated "IANA"-ish
> > thing that's independent of BIP process nonsense. It's at:
> > 
> > * https://github.com/bitcoin-inquisition/binana
> 
> I think "authority" is a strong word especially in bitcoin and this process could even work with BINN (Bitcoin Inquisition Numbers And Names). IANA (a function of ICANN) is different thing altogether which was founded by US government.

Bitcoin Inquisition is based on signet, which is a centralized blockchain for
testing run by a central authority whose consensus is based on signatures from
that authority. Using the term "authority" in this context is fine.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240118/b49dd5f2/attachment-0001.sig>

------------------------------

Message: 4
Date: Thu, 18 Jan 2024 18:00:34 +0000
From: Peter Todd <pete@petertodd.org>
To: Michael Folkson <michaelfolkson@protonmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] BIP process friction
Message-ID: <ZalnQqvbxhxm8UG2@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Wed, Jan 17, 2024 at 05:29:48PM +0000, Michael Folkson via bitcoin-dev wrote:
> Hey Luke
> 
> I'd be happy to pick up working on BIP 3 again ([0], [1]) in light of this issue and others that are repeatedly cropping up (e.g. confusion on the recommended flow for working on proposed consensus changes, when to open a pull request to bitcoin-inquisition, when to open a pull request to Core, when to include/exclude activation params etc).
> 
> I don't think there is much I personally disagree with you on with regards to BIPs but one issue where I do think there is disagreement is on whether proposed default policy changes can/should be BIPed.
> 
> I previously drafted this on proposed default policy changes [2]:
> 
> "To address problems such as pinning attacks on Lightning and multiparty protocols (e.g. vaults) there are and will continue to be draft proposals on changing the default policy rules in Bitcoin Core and/or alternative implementations. As these proposals are for default policy rules and **not** consensus rules there is absolutely no obligation for Bitcoin Core and/or alternative implementations to change their default policy rules nor users to run any particular policy rules (default or otherwise). The authors of these draft proposals are clearly recommending what they think the default policy rules should be and what policy rules users should run but it is merely a recommendation. There are a lot of moving parts, subtleties and complexities involved in designing default policy rules so any recommendation(s) to significantly upgrade default policy rules would benefit from being subject to a spec process. This would also aid the review of any policy related pull requests in Bitcoin 
 Core and/or alternative implementations. An interesting recent case study washttps://github.com/bitcoin/bitcoin/pull/22665and Bitcoin Core not implementing the exact wording of BIP 125 RBF. In this case (for various reasons) as a response Bitcoin Core just removed references to BIP 125 and started documenting the replacement to BIP 125 rules in the Bitcoin Core repo instead. However, it is my view that recommendations for default policy rules should be recommendations to all implementations, reviewed by Lightning and multiparty protocol developers (not just Bitcoin Core) and hence they would benefit from being standardized and being subject to a specification process. I will reiterate once again though that policy rules are **not** consensus rules. Consensus rules are much closer to an obligation as divergences from consensus rules risk the user being forked off the blockchain and could ultimately end up in network splits. This does not apply to policy rules."
> 
> Are you open to adjusting your stance on proposed policy changes being BIPed? I do think it really stunts work on proposed default policy changes and people's ability to follow work on these proposals when the specifications for them are littered all over the place. I've certainly struggled to follow the latest state of V3 policy proposals without clear reference points for the latest state of these proposals e.g. [3]. In addition some proposed consensus change BIPs are starting to want to include sections on policy (e.g. BIP345, OP_VAULT [4]) where it would be much better if they could just refer to a separate policy BIP rather than including proposals for both policy and consensus in the same BIP.

BIP-125 is I think an interesting case study. It is a much more fundamental
standard than Ordinals or Taproot Assets, in the sense that transaction
replacement is expected to be used by essentially all wallets as all wallets
have to deal with fee-rate fluctuations; I do not think that Ordinals or
Taproot assets are appropriate BIP material due to their niche use-case.

The V3 proposal, and ephemeral anchors, would be expected to be used by a wide
range of contracting protocols, most notably lightning. This isn't quite as
broad usage as BIP-124 RBF. But it is close. And yes, Core making changes to
what is essentially BIP125 has an impact: just the other day I ran into someone
that didn't know RBF Rule #6 existed, which Core added on top of BIP-125, and
had made a mistake in their safety analysis of a protocol due to that.

Meanwhile, engineering documentation on V3 is extremely lacking, with basics
like worked through use-case examples not being available. We don't even have
solid agreement let alone documentation on how Lightning channels are meant to
use V3 transactions and what the trade-offs are. And that has lead to mistaken
claims, such as overstating(1) the benefit V3 transactions in their current
form have for transaction pinning.

I don't think V3 necessarily needs a formal BIP. But it would benefit from a
proper engineering process where use-cases are actually worked out and analyzed
properly.

Finally, I think the lesson to be learned here is that mempool policy is better
served by *living* documentation that gets updated to reflect the real world.
There's no easy way for someone to get up to speed on what mempool policy is
actually implemented, and more importantly, *why* it is implemented and what
trade-offs were made to get there. It's quite possible that this "living
documentation" requirement rules out the BIP process.

1) https://petertodd.org/2023/v3-txs-pinning-vulnerability

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240118/16974c52/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 21
********************************************
