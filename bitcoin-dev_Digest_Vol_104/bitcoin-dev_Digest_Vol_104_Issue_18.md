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

   1. BIP process friction (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Wed, 17 Jan 2024 12:42:52 +1000
From: Anthony Towns <aj@erisian.com.au>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] BIP process friction
Message-ID: <Zac+rMC/c+qTmSxY@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

Hi all,

Just under three years ago there was some discussion about the BIPs repo,
with the result that Kalle became a BIPs editor in addition to Luke, eg:

 * https://gnusha.org/bitcoin-core-dev/2021-04-22.log
 * https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-April/018859.html

It remains, however, quite hard to get BIPs merged into the repo, eg
the following PRs have been open for quite some time:

 * #1408: Ordinal Numbers; opened 2023-01-21, editors comments:
     Kalle:
       https://github.com/bitcoin/bips/pull/1408#issuecomment-1421641390
       https://github.com/bitcoin/bips/pull/1408#issuecomment-1435389476

     Luke:
       https://github.com/bitcoin/bips/pull/1408#issuecomment-1429146796
       https://github.com/bitcoin/bips/pull/1408#issuecomment-1438831607
       https://github.com/bitcoin/bips/pull/1408#issuecomment-1465016571

 * #1489: Taproot Assets Protocol; opened 2023-09-07, editors comments:
     Kalle: https://github.com/bitcoin/bips/pull/1489#issuecomment-1855079626
     Luke: https://github.com/bitcoin/bips/pull/1489#issuecomment-1869721535j

 * #1500: OP_TXHASH; opened 2023-09-30, editors comments:
     Luke:
       https://github.com/bitcoin/bips/pull/1500#pullrequestreview-1796550166
       https://twitter.com/LukeDashjr/status/1735701932520382839

The range of acceptable BIPs seems to also be becoming more limited,
such that mempool/relay policy is out of scope:

 * https://github.com/bitcoin/bips/pull/1524#issuecomment-1869734387

Despite having two editors, only Luke seems to be able to assign new
numbers to BIPs, eg:

 * https://github.com/bitcoin/bips/pull/1458#issuecomment-1597917780

There's also been some not very productive delays due to the editors
wanting backwards compatibility sections even if authors don't think
that's necessary, eg:

 * https://github.com/bitcoin/bips/pull/1372#issuecomment-1439132867

Even working out whether to go back to allowing markdown as a text format
is a multi-month slog due to process confusion:

 * https://github.com/bitcoin/bips/pull/1504

Anyway, while it's not totally dysfunctional, it's very high friction.

There are a variety of recent proposals that have PRs open against
inquisition; up until now I've been suggesting people write a BIP, and
have been keying off the BIP number to signal activation. But that just
seems to be introducing friction, when all I need is a way of linking
an arbitrary number to a spec.

So I'm switching inquisition over to having a dedicated "IANA"-ish
thing that's independent of BIP process nonsense. It's at:

 * https://github.com/bitcoin-inquisition/binana

If people want to use it for bitcoin-related proposals that don't have
anything to do with inquisition, that's fine; I'm intending to apply the
policies I think the BIPs repo should be using, so feel free to open a PR,
even if you already know I think your idea is BS on its merits. If someone
wants to write an automatic-merge-bot for me, that'd also be great.

If someone wants to reform the BIPs repo itself so it works better,
that'd be even better, but I'm not volunteering for that fight.

Cheers,
aj

(It's called "numbers and names" primarily because that way the acronym
amuses me, but also in case inquisition eventually needs an authoritative
dictionary for what "cat" or "txhash" or similar terms refer to)


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 18
********************************************
