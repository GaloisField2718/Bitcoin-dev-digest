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

   1. Re: One-Shot Replace-By-Fee-Rate (Peter Todd)
   2. Re: CheckTemplateVerify Does Not Scale Due to UTXO's Required
      For Fee Payment (Brandon Black)


----------------------------------------------------------------------

Message: 1
Date: Sat, 27 Jan 2024 07:19:22 +0000
From: Peter Todd <pete@petertodd.org>
To: Murch <murch@murch.one>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <ZbSueoReTvEmm1s9@petertodd.org>
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
> 
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
> 
> Among those five transactions, the only transaction attractive for block
> inclusion would be the small RBFr transaction with a
> bottom-of-the-next-block feerate. Today, if it were mined it would amount to
> fees of around 4000 sats every few blocks to make the entire network relay
> transactions of more than 205,000?vB every few seconds. Given that my
> example is minimal, it should be possible to further increase bandwidth
> cost.
> 
> Assuming that I did not make a mistake, i.e. all the replacements are viable
> and my scenario is compatible with your proposal, the described One-Shot
> Replace-By-Fee-Rate proposal would not be safe for deployment on the
> network.

I actually tried this attack out, and it fails at step #4 due to the Rule #6,
PaysMoreThanConflicts, check.

While on stacker.news you stated that:

    tx_HS has 5000 vB and pays 21 s/vB, but since it spends an output from a
    low-feerate parent, it?s mining score is only 1.95?s/vB.

and

    You RBF tx_LL and tx_HS with tx_LM that has 100,000 vB and pays 3.05?s/vB (fee:
    305,000 s) by spending the outputs C1 and C2. This is permitted, since only
    tx_LL is a direct conflict, so the feerate of tx_HS does not have to be beat
    directly.

tx_HS _is_ considered to be a direct conflict, and its raw fee-rate _does_ have
to be beat directly. While ts_HS does spend an unconfirmed output, it appears
that the fee-rate PaysMoreThanConflicts uses to calculate if ts_HS can be
beaten is ts_HS's raw fee-rate. So looks like your understanding was incorrect
on these two points.

FYI here is the actual test script I used to test this attack. You can run it
using Bitcoin v26.0 with the -acceptnonstdtxn -mempoolfullrbf=1 command line
arguments, with python-bitcoinlib v0.12.2 installed.

#!/usr/bin/env python3

import bitcoin
bitcoin.SelectParams('regtest')

import bitcoin.rpc
import sys

from bitcoin.core import *
from bitcoin.core.script import *
from bitcoin.wallet import *

proxy = bitcoin.rpc.Proxy()

my_addr = proxy.getnewaddress().to_scriptPubKey()

coins = proxy.listunspent(1)

print(coins[0:2])

txo1 = coins[0]['outpoint']
txo1_amount = coins[0]['amount']
txo2 = coins[1]['outpoint']
txo2_amount = coins[1]['amount']

print(txo1)
print(txo2)

for i in range(0, 1):
    # Step 2
    tx_ll = CTransaction(
        [CTxIn(txo1)],
        [CTxOut(txo1_amount - 100000, my_addr),
         CTxOut(0, CScript([OP_RETURN, b'x' * 90000]))])

    r = proxy.signrawtransactionwithwallet(tx_ll)
    assert(r['complete'])
    tx_ll_signed = r['tx']

    print('tx_ll = %s' % b2lx(proxy.sendrawtransaction(tx_ll_signed)))

    tx_ls = CTransaction(
        [CTxIn(COutPoint(tx_ll.GetTxid(), 0))],
        [CTxOut(txo1_amount - 100000 - 300, my_addr)])
    r = proxy.signrawtransactionwithwallet(tx_ls)
    assert(r['complete'])
    tx_ls_signed = r['tx']

    print('tx_ls = %s' % b2lx(proxy.sendrawtransaction(tx_ls_signed)))

    # Step 3
    tx_hs = CTransaction(
        [CTxIn(COutPoint(tx_ll.GetTxid(), 0)),
         CTxIn(txo2)],
        [CTxOut((txo1_amount - 100000) + txo2_amount - 4000, my_addr)])

    r = proxy.signrawtransactionwithwallet(tx_hs)
    assert(r['complete'])
    tx_hs_signed = r['tx']

    print('tx_hs = %s ' % b2lx(proxy.sendrawtransaction(tx_hs_signed)))


    # Step 4
    tx_lm = CTransaction(
        [CTxIn(txo1),
         CTxIn(txo2)],
        [CTxOut(txo1_amount + txo2_amount - 300000, my_addr),
         CTxOut(0, CScript([OP_RETURN, b'x' * 90000]))])

    r = proxy.signrawtransactionwithwallet(tx_lm)
    assert(r['complete'])
    tx_lm_signed = r['tx']

    print('tx_lm = %s' % b2lx(proxy.sendrawtransaction(tx_lm_signed)))
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240127/0b9f65bb/attachment-0001.sig>

------------------------------

Message: 2
Date: Fri, 26 Jan 2024 22:28:54 -0800
From: Brandon Black <freedom@reardencode.com>
To: Peter Todd <pete@petertodd.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] CheckTemplateVerify Does Not Scale Due to
	UTXO's Required For Fee Payment
Message-ID: <ZbSipq2QQx904Ofo@console>
Content-Type: text/plain; charset=us-ascii

Hi Peter,

On 2024-01-24 (Wed) at 19:31:07 +0000, Peter Todd via bitcoin-dev wrote:
> It is
> expected that CTV would be usually used with anchor outputs to pay fees; by
> creating an input of the correct size in a separate transaction and including
> it in the CTV-committed transaction; or possibly, via a transaction sponsor
> soft-fork.
> 
> This poses a scalability problem: to be genuinely self-sovereign in a protocol
> with reactive security, such as Lightning, you must be able to get transactions
> mined within certain deadlines. To do that, you must pay fees. All of the
> intended exogenous fee-payment mechanisms for CTV require users to have at
> least one UTXO of suitable size to pay for those fees.

I understand your reservations with regard to CTV-based protocols for
scaling bitcoin and lightning. Fortunately, the "user gotta have a UTXO"
concern is readily answered (and you actually gave one answer to
approximately the same concern from me when we discussed lightning
fees): If the user's balance inside the protocol is not sufficient to
pay exit fees then they aren't going to try to exit; so their
in-protocol balance can be used to pay fees. With ephemeral anchors
throughout the tree, an exiting user would spend their leaf UTXO, and
the ephemeral anchors along the path to their leaf to create a package
of the necessary fee rate to facilitate their timely exit.

Alternatively, users entering into a channel tree protocol (e.g. Timeout
Trees) can have their leaf include a second UTXO commitment which would
create a fee-paying output exactly when they need it; without causing a
scaling problem.

Finally, the reality of these protocol proposals is that they are
intended to enable users who may never have sufficient funds to pay the
full cost to exit the protocol in on chain fees to use bitcoin in a
trust-minimized way. To facilitate this, such a protocol could employ
fee insurance which would accept claims for fees to pull a specific exit
series on chain via any of the mechanisms you describe. This, by the
way, would bring more than one user out of the protocol, so even in the
worst case it does scale bitcoin by requiring only 1 fee paying UTXO for
log_r(n)*(r-1) users to exit.

Hope this helps,

--Brandon


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 30
********************************************
