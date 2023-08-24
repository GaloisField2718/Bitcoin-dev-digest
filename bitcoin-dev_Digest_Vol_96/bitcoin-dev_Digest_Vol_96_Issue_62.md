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

   1. Re: Ark: An Alternative Privacy-preserving Second Layer
      Solution (David A. Harding)
   2. Re: Bitcoin Transaction Relay over Nostr (David A. Harding)
   3. Re: Ark: An Alternative Privacy-preserving Second	Layer
      Solution (Ali Sherief)


----------------------------------------------------------------------

Message: 1
Date: Sat, 27 May 2023 10:36:47 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Burak Keceli <burak@buraks.blog>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second Layer Solution
Message-ID: <c78b9e621e994f3cf3500e4480b61b0e@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

Hi Burak,

Thanks for your response!  I found it very helpful.  I'm going to reply
to your email a bit out of order.

> 4. Alice places one input to her one-in, three-out transaction to
>    supply funds to commitment output, connectors output, change
>    output, and transaction fees.

You don't mention it in your reply, but was I correct in my earlier
email in assuming that Alice can claim any funds paid to a commitment
output after four weeks if its commitments haven't been published
onchain?  E.g., that in the best case this allows a ~50 vbyte commitment
output that pays an arbitrary number of users to be spent as a ~100
vbyte input (P2TR scriptpath for pk(A) && older(4 weeks))?

> 1. Mixing coins.
> 2. Paying lightning invoices
> 3. Making internal transfers

If commitment outputs can't normally be spent by Alice for four weeks,
then Alice needs to keep enough capital on hand to pay out all amounts
involved in the activities listed above.  I've seen many people make
this point, but I wanted to run some rough numbers to estimate the
extent of that capital load.

Let's say Alice has a million customers who each receive all of their
income and pay all of their expenses with her.  In my country, the
median income is a bit less than $36,000 USD, or about $3,000 a month.
I imagine spending is not evenly distributed over time, so let's say
Alice needs to hold 3x the average to be prepared for a busy period.
That implies Alice's capital requirements are about $9 billion USD (3 *
3000 * 1e6).

At a hypothetical risk-free interest rate of 1.5% annual, that's about
$135 that will need to be recovered from each user per year (9e9 * 0.015
/ 1e6).

Additionally, if we assume the cost of an onchain transaction is $100
and the service creates one transaction per five seconds, that's $630 in
fee costs that will need to be recovered from each user per year ((60 /
5) * 60 * 24 * 365 * 100 / 1e6).

I'll come back to this financial analysis later.

> If we want to enable Lightning-style instant settlement assurances for
> the internal transfers, we need OP_XOR or OP_CAT on the base layer
> [...] https://eprint.iacr.org/2017/394.pdf

What do you mean by "instant"?  Do you mean "settlement as soon as the
next onchain pool transaction is published"?  For example, within 5
seconds if the coinjoining completes on time?  That's significantly
slower than LN today, at least in the typical case for a well-connected
node.[1]

I think 5 seconds is fine for a lot of purposes (at both point-of-sale
terminals and on websites, I very often need to wait >5 seconds for a
credit card transaction to process), but I think it's worth noting the
speed difference in a technical discussion.

Additionally, I think the idea described significantly predates that
paper's publication, e.g.:

"Well while you can't prevent it you could render it insecure enabling
miners to take funds.  That could work via a one-show signature
[...]"[2]

A problem with the idea of using one-show signatures as double-spend
protection is that miner-claimable fidelity bonds don't work as well
against adversaries that are not just counterparties but also miners
themselves.  This same problem has been described for other ideas[3],
but to summarize:

Bob has something valuable.  Alice offers him the output of an
unconfirmed transaction in exchange for that thing.  She also provides a
bond that will pay its amount to any miner who can prove that Alice
double spent her input to the unconfirmed transaction.

If Alice is miner, she can privately create candidate blocks that double
spend the payment to Bob and which also claim the bond.  If she fails to
find a PoW solution for those candidate blocks, she lets Bob have his
money.  If she does find a PoW solution, she publishes the block, taking
Bob's money, securing her bond, and also receiving all the regular block
rewards (sans the fees from whatever space she used for her
transaction).

I haven't exactly[4] seen this mentioned before, but I think it's
possible to weaken Alice's position by putting a timelock on the
spending of the bond, preventing it from being spent in the same block
as the double-spend.  For example, a one-block timelock (AKA: 1 CSV)
would mean that she would need to mine both the block containing her
unconfirmed transactions (to double spend them) and the next block (to
pay the fidelity bonds back to herself).

Ignoring fee-sniping (bond-sniping in this case), selfish mining, and
51% attacks, her chance of success at claiming the fidelity bond is
equal to her portion of the network hashrate, e.g. if she has 33%, she's
33% likely to succeed at double spending without paying a penalty.  The
value of the fidelity bond can be scaled to compensate for that, e.g. if
you're worried about Alice controlling up to 50% of hashrate, you make
the fidelity bond at least 2x the base amount (1 / 50%).  Let's again
assume that Alice has a million users making $3,000 USD of payments per
month (28 days), or about on average $75,000 per minute (1e6 * 3000 / 28
/ 24 / 60).  If Alice bonds 2x the payment value and her bonds don't
expire for 6 blocks (which might take 3 hours), she needs an additional
$27 million worth of BTC on hand (75000 * 2 * (3 * 60)), which I admit
is trivial compared to the other capital requirements mentioned above.

* * *

Taken all together, it seems to me that Alice might need to keep several
billion dollars worth of BTC in a hot wallet in order to serve a million
users.  The per-user cost in fees and capital service would be around
$1,000 per year.  If we assume onchain transaction costs are about $100,
that would be equal to 10 channels that could be opened or closed by
each user for the same amount (i.e. an average of 5 channel rotations
per year).

Did I miss something in my analysis that would indicate the capital
costs would be significantly lower or that there wouldn't be other
tradeoffs (slower settlement than LN and a need to use a timelocked
fidelity bond)?

Thanks!,

-Dave

[1] https://twitter.com/Leishman/status/1661138737009442818

[2] 
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2014-December/007038.html

[3] 
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/018010.html

[4] Years ago, I think I saw a reply by Peter Todd to some idea about
     paying money to miners in a fair way and he noted that it was
     critical to pay miners far enough in the future that the current set
     of miners wouldn't be incentivized to manipulate who got the money
     by choosing which block to include the transaction in now.  I wasn't
     able to quickly find that post, but it definitely influenced my
     thinking here.


------------------------------

Message: 2
Date: Sat, 27 May 2023 16:37:12 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Joost Jager <joost.jager@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Bitcoin Transaction Relay over Nostr
Message-ID: <020c50422fb4bc03fe1d6f06c2ae751f@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-05-22 21:19, Joost Jager via bitcoin-dev wrote:
> A notable advantage of this approach is that it delegates the
> responsibility of dealing with Denial-of-Service (DoS) threats to the
> relays themselves. They could, for example, require a payment to
> mitigate such concerns.

Hi Joost,

Thanks for working on this!  One quick thought I had was that a possibly
interesting avenue for exploration would be that, in addition to
relaying individual transactions or packages, it might be worth relaying
block templates and weak blocks as both of those provide inherent DoS
resistance and can offer useful features.

A block template is an ordered list of raw transactions that can all be
included in the next block (with some space reserved for a coinbase
transaction).  A full node can validate those transactions and calculate
how much fee they pay.  A Nostr relay can simply relay almost[1] any
template that pays more fees than the previous best template it saw for
the next block.  That can be more flexible than the current
implementation of submitblock with package relay which still enforces a
lot of the rules that helps keep a regular relay node safe from DoS and
a miner node able to select mineable transactions quickly.

A weak block is a block whose header doesn't quite hash to low enough of
a value to be included on the chain.  It still takes an extraordinary
amount of hashrate to produce, so it's inherently DoS resistant.  If
miners are producing block that include transactions not seen by typical
relay nodes, that can reduce the efficiency and effectiveness of BIP152
compact block relay, which hurts the profitability of miners of custom
blocks.  To compensate, miners could relay weak blocks through Nostr to
full nodes and other miners so that they could quickly relay and accept
complete blocks that later included the same custom transactions.  This
would also help fee estimation and provide valuable insights to those
trying to get their transactions included into the next block.

Regarding size, the block template and weak block could both be sent in
BIP152 compact block format as a diff against the expected contents of a
typical node, allowing Alice to send just a small amount of additional
data for relay over what she'd have to send anyway for each transaction
in a package.  (Although it's quite possible that BetterHash or Stratum
v2 have even better solutions, possibly already implemented.)

If nothing else, I think Nostr could provide an interesting playground
for experimenting with various relay and mining ideas we've talked about
for years, so thanks again for working on this!

-Dave

[1] In addition to validating transactions, a relay would probably want
     to reject templates that contained transactions that took
     excessively long to validate (which could cause a block including
     them to become stale) or that included features reserved for
     upgrades (as a soft fork that happened before the relay's node was
     upgraded might make that block invalid).


------------------------------

Message: 3
Date: Sun, 28 May 2023 06:02:58 +0000
From: Ali Sherief <ali@notatether.com>
To: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>, "burak@buraks.blog"
	<burak@buraks.blog>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second	Layer Solution
Message-ID:
	<-N2f7ihsZ8VYuCRU0KMXQLlw5vwbZ50lAw-MKEFz8838YBuf39SKlf4lNePJUSYQanOuKzFfmZeLFpzeOnbfss7mlhoCvYPwG6a2tt6kfVY=@notatether.com>
	
Content-Type: text/plain; charset="utf-8"

Burak, I don't remember if this has been mentioned previously in the conversation about Ark, but a disadvantage in the protocol as it is currently is that "Ark require users to come online and "refresh" their coins every few weeks, otherwise the ASP can sweep the funds." (putting that in quotes because although I copied this from a forum, it may have originally been said on this list.)

However, yesterday I have come up with a scheme to mitigate this disadvantage, in a way that works similar to LN watchtowers.

This watchtower program for Ark would be made that runs on an internet-connected server and inputs your wallet password and the date in the future to perform the refreshing. A child process can then be spawned that acts similar to a cronjob, and stores the wallet password with AES encryption in memory.

The key to this cipher is the time stored in ISO 8601 format as a byte string. It is promptly discarded from memory.

Every second, the watchtower child process will attempt to decrypt the cipher using the current ISO 8601 time looking like "YYYY-mm-ddTHH:MM:SSZ" as the key.

Naturally this will only succeed at the requisite time at which the wallet is to be unlocked by the watchtower child process - following which the coins inside the ASP are refreshed, and the watchtower child process is terminated and the encrypted wallet password destroyed.

Of course, memory scrubbing should be applied to the region that has the decrypted wallet password.
If at any point the user comes online by themselves, they can simply cancel the watchtower refreshing task, which will terminate the watchtower child process without opening your wallet and refreshing coins.

The key feature is that nobody will be able to decrypt the wallet password unless they know the exact time it is to be unlocked as an ISO 8601 string. It cannot be unlocked at any time in the future, just at that particular instant, as long as the key is discarded and the software randomly guesses the decryption by attempting each second the new time as the encryption key. Even if the watchtower is hacked after the task has been made, the hacker still won't be able to decrypt the wallet password unless they brute-force the encryption key by exhaustively trying all timestamps in the future.

Alternatively, instead of encrypting the wallet password, it can encrypt a signed transaction which is used by Ark to refresh the coins. In this case, the wallet password would still need to be collected, but only for the purpose of signing the transaction, after which the password is promptly erased from memory.

How this can be extended to repeatedly arming the watchtower program with refreshes remains to be seen, but using the wallet password as the encryption directly is one option albeit not a secure one A better and more secure option would be to take note of the UTXOs created by the coin refreshing transaction, use those as inputs to a second refreshing transaction that is created immediately after the first one, sign it, and similarly create a third, fourth, etc. as many as are desirable for the user. Then every 4 weeks, one of these transactions can be broadcasted, in the order that they were created obviously.

Looking forward to your feedback on this.
-Ali
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230528/451dd264/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 62
*******************************************
