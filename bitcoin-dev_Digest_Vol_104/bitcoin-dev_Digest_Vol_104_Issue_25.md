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

   1. Re: One-Shot Replace-By-Fee-Rate (Murch)
   2. Re: One-Shot Replace-By-Fee-Rate (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Mon, 22 Jan 2024 13:12:45 -0500
From: Murch <murch@murch.one>
To: Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <9a89eca8-61fd-4156-825d-c9b718dc3034@murch.one>
Content-Type: text/plain; charset=UTF-8; format=flowed

Hi Peter,

On 1/18/24 13:23, Peter Todd via bitcoin-dev wrote:
 > Reposting this blog post here for discussion:
 >
 > https://petertodd.org/2024/one-shot-replace-by-fee-rate

I saw your proposal mentioned on Stacker News and read it with interest. 
In response, I described a replacement cycle that can be used to 
broadcast the same five transactions repeatedly:

https://stacker.news/items/393182

The gist is that by using two confirmed inputs and five transactions, 
you can use RBFr to reduce the absolute fee while raising the feerate to 
top block levels, then immediately use the current RBF rules to 
introduce a high-feerate transaction that beats the RBFr transaction but 
is hampered by a low-feerate parent and not attractive for mining, then 
use RBF to replace its low-feerate parent, then use the RBFr transaction 
again to reduce the absolute feerate. Due to the asymmetric 
replacements, the same transactions can replace each other in that order 
in every cycle. Please refer to the linked write-up for details, I?ve 
included weights, fees, and a transaction graph to make my example 
comprehensible.

Among those five transactions, the only transaction attractive for block 
inclusion would be the small RBFr transaction with a 
bottom-of-the-next-block feerate. Today, if it were mined it would 
amount to fees of around 4000 sats every few blocks to make the entire 
network relay transactions of more than 205,000?vB every few seconds. 
Given that my example is minimal, it should be possible to further 
increase bandwidth cost.

Assuming that I did not make a mistake, i.e. all the replacements are 
viable and my scenario is compatible with your proposal, the described 
One-Shot Replace-By-Fee-Rate proposal would not be safe for deployment 
on the network.

Best,
Murch


------------------------------

Message: 2
Date: Mon, 22 Jan 2024 22:52:01 +0000
From: Peter Todd <pete@petertodd.org>
To: Murch <murch@murch.one>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <Za7xkUsoeACMv6Fw@petertodd.org>
Content-Type: text/plain; charset="utf-8"

On Mon, Jan 22, 2024 at 01:12:45PM -0500, Murch via bitcoin-dev wrote:
> Hi Peter,
> 
> On 1/18/24 13:23, Peter Todd via bitcoin-dev wrote:
> > Reposting this blog post here for discussion:
> >
> > https://petertodd.org/2024/one-shot-replace-by-fee-rate
> 
> I saw your proposal mentioned on Stacker News and read it with interest. In
> response, I described a replacement cycle that can be used to broadcast the
> same five transactions repeatedly:
> 
> https://stacker.news/items/393182

So if this does in fact work - I haven't actually tested it - the root problem
here is not replace-by-fee-rate, but rather our current replace-by-fee rules:
in step 7 you've clearly replaced a more desirable, high fee-rate, transaction
that will be mined soon with a low fee-rate transaction that will not be.
That's obviously not incentive compatible for miners, for the same reason that
replace-by-fee-rate generally is incentive compatible.

I had incorrectly thought we had gotten rid of those cases... But looks like
the definition of BIP-125 Rule #2, "The replacement transaction may only
include an unconfirmed input if that input was included in one of the original
transactions.", is not sufficient because you can combine unconfirmed inputs
from two different replaced transactions, making a resulting transaction that
is less valuable to miners than one of the replaced transactions.

IIUC Suhas has a draft fix here that would solve this issue: https://github.com/bitcoin/bitcoin/pull/26451

An even simpler fix would be to just require that all unconfirmed inputs in a
replacement come from the *same* replaced transaction. That would make certain
rare, but economically viable, replacements infeasible. But it would definitely
fix the issue.

> The gist is that by using two confirmed inputs and five transactions, you
> can use RBFr to reduce the absolute fee while raising the feerate to top
> block levels, then immediately use the current RBF rules to introduce a
> high-feerate transaction that beats the RBFr transaction but is hampered by
> a low-feerate parent and not attractive for mining, then use RBF to replace
> its low-feerate parent, then use the RBFr transaction again to reduce the
> absolute feerate. Due to the asymmetric replacements, the same transactions
> can replace each other in that order in every cycle. Please refer to the
> linked write-up for details, I?ve included weights, fees, and a transaction
> graph to make my example comprehensible.

BTW do you mind if I reproduce those graphics, with credit, to explain the
issue? I have a few places where I could make use of it, eg the
replace-by-fee-rate post itself.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240122/11bae57e/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 25
********************************************
