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

   1. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Greg Tonoski)


----------------------------------------------------------------------

Message: 1
Date: Sun, 14 Jan 2024 14:10:30 +0100
From: Greg Tonoski <gregtonoski@gmail.com>
To: Keagan McClelland <keagan.mcclelland@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAMHHROwP8guVcy3yV09B=PYQscTcnGtNGMheFdvJM4ZYdWTSYw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Wed, Dec 27, 2023 at 11:39?PM Keagan McClelland
<keagan.mcclelland@gmail.com> wrote:
>
> > As a result, there are incentives structure distorted and critical
> inefficiencies/vulnerabilities (e.g. misallocation of block space,
> blockspace value destruction, disincentivized simple transaction,
> centralization around complex transactions originators).
>
> Can you please describe the mechanism here?

Sure. Because of the preferential treatment there is incentive to
bloat the underpriced part of transaction data (so-called Witness) at
the expense of a number of genuine, simple transactions and so a
number of updates in the ledger. Blockspace is allocated to useless,
irrelevant data that don't affect state of Bitcoin, e.g. the
transaction 1c35521798dde4d1621e9aa5a3bacac03100fca40b6fb99be546ec50c1bcbd4a
could have been stripped of bloat and UTXO set wouldn't have changed;
at the same time the freed space could have been allocated to a simple
transaction that updates UTXO set (improving cost effectivness at the
same time).

Additionally, bloated transactions are bigger and so require more time
to be downloaded during Initial Block Download - wasting bandwith
(cost borne by node operators).

>
> > Price of blockspace should be the same for any data (1 byte = 1 byte,
> irrespectively of location inside or outside of witness), e.g. 205/205
> and 767/767 bytes in the examples above.
>
> "Should" ... to what end?

"Should" in order to avoid hazard of centralization. A single bidder
who takes advantage of "buy 1 get 3 megabytes free" may outcompete a
number of individuals whose simple transactions recieve
anti-preferential treatment - "buy 1 get 0.33 megabytes free" in
aggregate. There is the illustration at:
"https://gregtonoski.github.io/bitcoin/segwit-mispricing/Comparison_of_4MB_and_1.33MB_blocks_in_Bitcoin.pdf".


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 15
********************************************
