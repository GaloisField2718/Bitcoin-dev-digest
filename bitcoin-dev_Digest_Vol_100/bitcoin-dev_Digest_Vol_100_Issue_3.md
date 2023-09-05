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

   1. Re: Concern about "Inscriptions" (vjudeu@gazeta.pl)


----------------------------------------------------------------------

Message: 1
Date: Sun, 03 Sep 2023 18:01:02 +0200
From: vjudeu@gazeta.pl
To: GamedevAlice <gamedevalice256@gmail.com>, Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>,
	"bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Concern about "Inscriptions"
Message-ID:
	<98009035-ac19029087479e992d1f7eccdc9eb0ab@pmq6v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> Given the current concerns with blockchain size increases due to inscriptions, and now that the lightning network is starting to gain more traction, perhaps people are now more willing to consider a smaller blocksize in favor of pushing more activity to lightning?
?
People will not agree to shrink the maximum block size. However, if you want to kill inscriptions, there is another approach, that could be used to force them into second layers: it is called cut-through, and was described in this topic: https://bitcointalk.org/index.php?topic=281848.0
?
Then, if you have "Alice -> Bob -> ... -> Zack" transaction chain, and for example some inscriptions were created in "Alice -> Bob" transaction, then cut-through could remove those inscriptions, while leaving the payment unaffected, because the proper amount of coins will be received by Zack, as it should be.
?
On 2023-08-25 10:44:41 user GamedevAlice via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
As I understand it, protecting against this is exactly the reason why a blocksize limit exists. Perhaps it should never have been increased in the first place.
Given the current concerns with blockchain size increases due to inscriptions, and now that the lightning network is starting to gain more traction, perhaps people are now more willing to consider a smaller blocksize in favor of pushing more activity to lightning?
?
?
?
On Tue, Aug 22, 2023, 8:00 AM , <bitcoin-dev-request@lists.linuxfoundation.org> wrote:
Send bitcoin-dev mailing list submissions to
? ? ? ? bitcoin-dev@lists.linuxfoundation.org
To subscribe or unsubscribe via the World Wide Web, visit
? ? ? ? https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
or, via email, send a message with subject or body 'help' to
? ? ? ? bitcoin-dev-request@lists.linuxfoundation.org
You can reach the person managing the list at
? ? ? ? bitcoin-dev-owner@lists.linuxfoundation.org
When replying, please edit your Subject line so it is more specific
than "Re: Contents of bitcoin-dev digest..."
Today's Topics:
? ?1. Re: Concern about "Inscriptions" (symphonicbtc)
----------------------------------------------------------------------
Message: 1
Date: Mon, 21 Aug 2023 22:34:03 +0000
From: symphonicbtc <symphonicbtc@proton.me>
To: John Tromp <john.tromp@gmail.com>
Cc: Bitcoin Protocol Discussion
? ? ? ? <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Concern about "Inscriptions"
Message-ID:
? ? ? ? <UMOgM6dqQHqgxIoeyCE1ZzBDbU1c2H6oyUCVs4eTgUwozDphZwFdfO4qvnXUMZwYhfShzcaYqmLGN-XrfzyhYKWD8Q8IOD7EJAtdgbqMLe8=@proton.me>
Content-Type: text/plain; charset=utf-8
It is important to also note that proof of secret key schemes are highly data inefficient and likely would have a higher cost for users than simply allowing arbitrary data to continue. In ECDSA, purposely re-using k values allows you to encode data in both k and the entire secret key, as both become computable. Or, one could bruteforce a k value to encode data in a sig, as is done in some compromised hardware key exfiltration attacks. Additionally, one can bruteforce keys in order to encode data in the public key.
It is very difficult and expensive to attempt to limit the storage of arbitrary data in a system where the security comes from secret keys being arbitrary data.
Symphonic
------- Original Message -------
On Monday, August 21st, 2023 at 4:28 PM, John Tromp via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> > If we ban "arbitrary data", however you want to define it, then actors will
> > simply respond by encoding their data within sets of public keys. Public
> > key data is indistinguishable from random data, and, unless we are willing
> > to pad the blockchain with proof of knowledge of secret keys, there will be
> > no way to tell a priori whether a given public key is really a public key
> > or whether it is encoding an inscription or some other data.
>
>
> Note that in the Mimblewimble protocol, range proofs already prove
> knowledge of blinding factor in Pedersen commitments, and thus no
> additional padding is needed there to prevent the encoding of spam
> into cryptographic material. This makes pure MW blockchains the most
> inscription/spam resistant [1].
>
> [1] https://bitcointalk.org/index.php?topic=5437464.msg61980991#msg61980991
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
------------------------------
Subject: Digest Footer
_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
------------------------------
End of bitcoin-dev Digest, Vol 99, Issue 43
*******************************************
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230903/26efb381/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 3
*******************************************
