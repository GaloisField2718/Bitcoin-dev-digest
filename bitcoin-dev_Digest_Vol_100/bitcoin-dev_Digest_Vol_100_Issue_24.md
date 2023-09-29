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

   1. Re: Scaling Lightning With Simple Covenants (jlspc)


----------------------------------------------------------------------

Message: 1
Date: Thu, 28 Sep 2023 15:56:11 +0000
From: jlspc <jlspc@protonmail.com>
To: ZmnSCPxj <ZmnSCPxj@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling Lightning With Simple Covenants
Message-ID:
	<i-ch8ZncRDzXhqcYckpOLshpG0RwI3x1UQLPGT6bZD9qRHjBro79AqCwDpTd8BbaYxRKHEihvgdvU9gg-mxDV7rIsNlgC1xt0fOpYjxMoio=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8


Hi ZmnSCPxj,

> Good morning John,

> &gt;<i> On the other hand, if the consensus rules are changed to allow even simple covenants, this scaling bottleneck is eliminated.
> </i>&gt;<i> The key observation is that with covenants, a casual user can co-own an off-chain Lightning channel without having to sign all (or any) of the transactions on which it depends.
> </i>&gt;<i> Instead, a UTXO can have a covenant that guarantees the creation of the casual user's channel.
> </i>&gt;<i> The simplest way to have a single UTXO create channels for a large number of casual users is to put a covenant on the UTXO that forces the creation of a tree of transactions, the leaves of which are the casual users' channels.
> </i>&gt;<i> 
> </i>&gt;<i> While such a covenant tree can create channels for millions of casual users without requiring signatures or solving a difficult group coordination problem, it's not sufficient for scaling.
> </i>&gt;<i> The problem is that each channel created by a covenant tree has a fixed set of owners, and changing the ownership of a channel created by a covenant tree requires putting the channel on-chain.
> </i>&gt;<i> Therefore, assuming that all casual users will eventually want to pair with different dedicated users (and vice-versa), the covenant tree doesn't actually provide any long-term scaling benefit.
> </i>&gt;<i> 
> </i>&gt;<i> Fortunately, real long-term scaling can be achieved by adding a deadline after which all non-leaf outputs in the covenant tree can be spent without having to meet the conditions of the covenant.
> </i>&gt;<i> The resulting covenant tree is called a "timeout-tree" [9, Section 5.3].
> </i>&gt;<i> 
> </i>&gt;<i> Let A_1 ... A_n denote a large number of casual users, let B be a dedicated user, and let E denote some fixed time in the future.
> </i>&gt;<i> User B creates a timeout-tree with expiry E where:
> </i>&gt;<i> &nbsp;* leaf i has an output that funds a Lightning channel owned by A_i and B, and
> </i>&gt;<i> &nbsp;* after time E, each non-leaf output in the covenant tree can also be spent by user B without having to meet the conditions of the covenant.
> </i>
> I think, based solely on the description above, that it is not safe for dedicated user `B` to create this, unless it gets a signature from `A_i`.

You're right!

> The alternative is to also infect the leaf itself with a lifetime `(A_i &amp;&amp; B) || (B &amp;&amp; CLTV)`.

Yes, exactly.

This is the design given in the figures in the paper, as well as in the detailed descriptions that accompany those figures.
However, the text that you quoted above was incorrect and requires the change you described.

I've created a new version of the paper that includes this fix [1].
It also includes more detail (at the end of Section 4.9) on the use of hierarchical channels while performing passive rollovers.

Thanks for making this correction.

Regards,
John

[1] Law, "Scaling Lightning With Simple Covenants, version 1.1", https://github.com/JohnLaw2/ln-scaling-covenants




Sent with Proton Mail secure email.




------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 24
********************************************
