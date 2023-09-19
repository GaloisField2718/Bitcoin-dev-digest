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

   1. Re: Scaling Lightning With Simple Covenants (Erik Aronesty)
   2. Re: Scaling Lightning With Simple Covenants (ZmnSCPxj)
   3. Re: Parameters in BIP21 URIs (Vincenzo Palazzo)


----------------------------------------------------------------------

Message: 1
Date: Sun, 17 Sep 2023 07:32:52 -0400
From: Erik Aronesty <erik@q32.com>
To: Antoine Riard <antoine.riard@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Cc: lightning-dev <lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<CAJowKgL+sW_rtO+zaoe=ztia9SfQXCeZ0YnAsmox1O3r3kAAwQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

>
> replacing CTV usage with Musig2
>
>
this changes the trust model to a federated one vs trustless and also
increases the on-chain footprint of failure, correct?

>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230917/ca09d7c4/attachment-0001.html>

------------------------------

Message: 2
Date: Tue, 19 Sep 2023 07:44:48 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Erik Aronesty <erik@q32.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, lightning-dev
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<An4gUD9oSgMzt9dGWj7ZhCZ73fWNcQ_c9dya0X0OILJFGijykRNtWc4HClKJ0QGsQjKiL2-Oak7syh_4XngCNFJEVJDhKeEy11nedSpXbpI=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


Good morning Erik,

> > replacing CTV usage with Musig2
> 
> 
> this changes the trust model to a federated one vs trustless and also increases the on-chain footprint of failure, correct?


As I understand it, no.

MuSig and MuSig2 are n-of-n signing algorithms.

The implied usage is that all entities `A_i` for all `i` and `B` dedicated LN node are in the n-of-n set.

The argument that 2-of-2 channels are non-custodial and trust-minimized extends to n-of-n for all n.

Regards,
ZmnSCPxj


------------------------------

Message: 3
Date: Tue, 19 Sep 2023 11:58:33 +0200
From: "Vincenzo Palazzo" <vincenzopalazzodev@gmail.com>
To: "Lucas Ontivero" <lucasontivero@gmail.com>, "Bitcoin Protocol
	Discussion" <bitcoin-dev@lists.linuxfoundation.org>, "kiminuo"
	<kiminuo@protonmail.com>
Subject: Re: [bitcoin-dev] Parameters in BIP21 URIs
Message-ID: <CVMT0B6XUMRE.2OL4Q00QGBSOY@vincent-arch>
Content-Type: text/plain; charset=UTF-8

> Kiminuo, this was discussed here: https://github.com/bitcoin/bips/pull/49

What was the conclusion? the discussion point to another discussion 
happens on here. It is kind confusing.

I do think that the grammar of the BIP 21 is under specified, in the sense
that each parameter need to specify also how many times can be repeted.

In lightning, people start to ask the possibility to have multiple
invoices, that make kind of sense due that we encode everythink inside 
a invoice. So a person need only to know the invoice. See more here [1]

I am more in favor to work on improving the BIP21 maybe with a new
version? where we change just the grammar a little bit.

[1] https://github.com/lightning/bolts/issues/1111#issuecomment-1725177738

Cheers,

Vincent.


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 21
********************************************
