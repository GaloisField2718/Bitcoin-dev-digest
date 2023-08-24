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

   1. Denial of Service using Package Relay (alicexbt)
   2. Re: Denial of Service using Package Relay (Andrew Chow)


----------------------------------------------------------------------

Message: 1
Date: Thu, 06 Jul 2023 16:22:44 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Denial of Service using Package Relay
Message-ID:
	<Ga2AELVMhRn2JlAC1-85LivVhcBhXzsf5ypHXMt_lg9RpwKTxeRxIRr8g8UHUihvxIVNKua6FIGRCjkt4CuNcDtZy2MetpOucpZYoKPW5sw=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Bitcoin Developers,

I think its possible to use [package relay][0] for DoS attack in coinjoin. A few other projects could also be affected by packages. Since its a proposal that adds new P2P messages, transaction relay etc. its as important as any soft fork. Let me know if I am missing something.

Consider there are 2 coinjoin implementations: A and B

1) Register input in A
2) Double spend same input with zero fee to your own address
3) Register unconfirmed UTXO from 2 in B
4) B relays a package in which coinjoin transaction (child) pays for 2 (parent)

Users and coinjoin implementation B, both are incentivized to attack in this case.

Attacker could also use a different approach and register same input in A, B although there are some tradeoffs:

- If input gets included in a coinjoin transaction broadcasted by A, there is nothing much B can do about it. RBF with multiple users isn't easy and costly.
- Implementation with less users participating in a round would have an advantage.

[0]: https://gist.github.com/sdaftuar/8756699bfcad4d3806ba9f3396d4e66a


/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.


------------------------------

Message: 2
Date: Thu, 06 Jul 2023 17:24:47 +0000
From: Andrew Chow <lists@achow101.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Denial of Service using Package Relay
Message-ID: <67c37967-ba7d-eabe-01e7-c5a0f9ca7da8@achow101.com>
Content-Type: text/plain; charset=utf-8

On 07/06/2023 12:22 PM, alicexbt via bitcoin-dev wrote:
 > 1) Register input in A
 > 2) Double spend same input with zero fee to your own address
 > 3) Register unconfirmed UTXO from 2 in B

Why would unconfirmed inputs be accepted in a coinjoin? That seems 
unsafe, regardless of package relay. The sender of the unconfirmed 
transaction can already replace it thereby pinning or otherwise 
invalidating the coinjoin, it doesn't need package relay.

Furthermore, the coordinator B shouldn't accept the unconfirmed UTXO 
from 2 because it doesn't even know about that unconfirmed transaction. 
It has zero fee, so it's not going to be relayed.

Conceivably a similar attack can already be done by simply registering 
the same UTXO with multiple coordinators anyways. This doesn't require 
package relay either.

***

Package relay should help coinjoins since any one of the participants 
can rebroadcast the coinjoin with a further CPFP if the coinjoin is 
below the minimum relay fee. Some of the upcoming package RBF proposals 
should also help by allowing other child transactions in the package to 
RBF the entire thing, thereby resolving the need to have everyone 
re-sign the coinjoin in order to RBF.


Andrew



------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 98, Issue 2
******************************************
