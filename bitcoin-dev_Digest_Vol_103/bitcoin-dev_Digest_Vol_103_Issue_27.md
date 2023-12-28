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

   1. [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Greg Tonoski)
   2. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Nagaev Boris)
   3. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (vjudeu@gazeta.pl)
   4. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Keagan McClelland)


----------------------------------------------------------------------

Message: 1
Date: Wed, 27 Dec 2023 17:44:51 +0100
From: Greg Tonoski <gregtonoski@gmail.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] [BUG]: Bitcoin blockspace price discrimination
	put simple transactions at disadvantage
Message-ID:
	<CAMHHROxsKuqzVsU90srQBNDj4redB11uqB2JxmDK=G1LDw9_HA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Blockspace price for data of a simple transaction is higher than the
one for data of other ("complex") transactions: 3 vs 1.49
"weight"/byte in the examples below:
- 3=616 "weight" / 205 bytes (txid:
aabbcce67f2aa71932f789cac5468d39e3d2224d8bebb7ca2c3bf8c41d567cdd)
- 1.49=1140 "weight" / 767 bytes (txid:
1c35521798dde4d1621e9aa5a3bacac03100fca40b6fb99be546ec50c1bcbd4a).

As a result, there are incentives structure distorted and critical
inefficiencies/vulnerabilities (e.g. misallocation of block space,
blockspace value destruction, disincentivized simple transaction,
centralization around complex transactions originators).

Price of blockspace should be the same for any data (1 byte = 1 byte,
irrespectively of location inside or outside of witness), e.g. 205/205
and 767/767 bytes in the examples above.

Perhaps, the solution (the same price, "weight" of each bit of a
transaction) could be introduced as part of the next version of Segwit
transactions.

Let's fix it. What do you think?


------------------------------

Message: 2
Date: Wed, 27 Dec 2023 16:06:13 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: Greg Tonoski <gregtonoski@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAFC_Vt4pjZCMAZSi32Y3z-F3rrnnXVR4pvF5T4Ojrdb=Lsu97A@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Wed, Dec 27, 2023 at 2:26?PM Greg Tonoski via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
> As a result, there are incentives structure distorted and critical
> inefficiencies/vulnerabilities (e.g. misallocation of block space,
> blockspace value destruction, disincentivized simple transaction,
> centralization around complex transactions originators).
>
> Price of blockspace should be the same for any data (1 byte = 1 byte,
> irrespectively of location inside or outside of witness), e.g. 205/205
> and 767/767 bytes in the examples above.

Witness data does not contribute to utxo set. The discount on storing
data in witness creates an incentive to store data exactly in the
witness and not in the parts contributing to utxo set.

$ du -sh blocks/ chainstate/
569G    blocks/
9.3G    chainstate/

Witness data is part of the "blocks" directory which is not
latency-critical and can be stored on a slow and cheap storage device.
Directory "chainstate" contains the data needed to validate new
transactions and should fit into a fast storage device otherwise
initial block download takes weeks. It is important to maintain the
incentives structure, resulting in a small chainstate.

-- 
Best regards,
Boris Nagaev


------------------------------

Message: 3
Date: Wed, 27 Dec 2023 22:43:34 +0100
From: vjudeu@gazeta.pl
To: Greg Tonoski <gregtonoski@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<173813261-12d93c171dc593da018492a4fc8f3f2b@pmq8v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

I think it should be fixed. Because now, sending coins into P2WPKH is cheaper than sending them to P2TR, even though finally, when those coins are spent, the blockspace usage is cheaper for Taproot (when you spend by key) than for Segwit, because public key hash is not stored anywhere. But of course, because the cost is splitted between sender and spender, it is more profitable to send to P2WPKH, and spend from P2TR.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231227/377ed324/attachment-0001.html>

------------------------------

Message: 4
Date: Wed, 27 Dec 2023 15:39:38 -0700
From: Keagan McClelland <keagan.mcclelland@gmail.com>
To: Greg Tonoski <gregtonoski@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CALeFGL2AZfVqchy=GWTDyehKXJkjYtCaonYFigv7ctHUnsxPfg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> As a result, there are incentives structure distorted and critical
inefficiencies/vulnerabilities (e.g. misallocation of block space,
blockspace value destruction, disincentivized simple transaction,
centralization around complex transactions originators).

Can you please describe the mechanism here?

> Price of blockspace should be the same for any data (1 byte = 1 byte,
irrespectively of location inside or outside of witness), e.g. 205/205
and 767/767 bytes in the examples above.

"Should" ... to what end?

Keags

On Wed, Dec 27, 2023 at 10:26?AM Greg Tonoski via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Blockspace price for data of a simple transaction is higher than the
> one for data of other ("complex") transactions: 3 vs 1.49
> "weight"/byte in the examples below:
> - 3=616 "weight" / 205 bytes (txid:
> aabbcce67f2aa71932f789cac5468d39e3d2224d8bebb7ca2c3bf8c41d567cdd)
> - 1.49=1140 "weight" / 767 bytes (txid:
> 1c35521798dde4d1621e9aa5a3bacac03100fca40b6fb99be546ec50c1bcbd4a).
>
> As a result, there are incentives structure distorted and critical
> inefficiencies/vulnerabilities (e.g. misallocation of block space,
> blockspace value destruction, disincentivized simple transaction,
> centralization around complex transactions originators).
>
> Price of blockspace should be the same for any data (1 byte = 1 byte,
> irrespectively of location inside or outside of witness), e.g. 205/205
> and 767/767 bytes in the examples above.
>
> Perhaps, the solution (the same price, "weight" of each bit of a
> transaction) could be introduced as part of the next version of Segwit
> transactions.
>
> Let's fix it. What do you think?
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231227/c5df2ab2/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 27
********************************************
