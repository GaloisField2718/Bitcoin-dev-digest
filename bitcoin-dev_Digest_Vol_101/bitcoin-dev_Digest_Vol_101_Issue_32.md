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

   1. Proposed BIP for OP_CAT (Ethan Heilman)
   2. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (David A. Harding)
   3. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Sat, 21 Oct 2023 01:08:03 -0400
From: Ethan Heilman <eth3rs@gmail.com>
To: Bitcoin Dev <bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<CAEM=y+XDB7GGa5BTAWrQHqTqQHBE2VRyd7VWjEb+zCOMzRP+Lg@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi everyone,

We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki

OP_CAT was available in early versions of Bitcoin. It was disabled as
it allowed the construction of a script whose evaluation could create
stack elements exponential in the size of the script. This is no
longer an issue in the current age as tapscript enforces a maximum
stack element size of 520 Bytes.

Thanks,
Ethan

==Abstract==

This BIP defines OP_CAT a new tapscript opcode which allows the
concatenation of two values on the stack. This opcode would be
activated via a soft fork by redefining the opcode OP_SUCCESS80.

When evaluated the OP_CAT instruction:
# Pops the top two values off the stack,
# concatenate the popped values together,
# and then pushes the concatenated value on the top of the stack.

OP_CAT fails if there are less than two values on the stack or if a
concatenated value would have a combined size of greater than the
maximum script element size of 520 Bytes.

==Motivation==
Bitcoin tapscript lacks a general purpose way of combining objects on
the stack restricting the expressiveness and power of tapscript. For
instance this prevents among many other things the ability to
construct and evaluate merkle trees and other hashed data structures
in tapscript. OP_CAT by adding a general purpose way to concatenate
stack values would overcome this limitation and greatly increase the
functionality of tapscript.

OP_CAT aims to expand the toolbox of the tapscript developer with a
simple, modular and useful opcode in the spirit of Unix[1]. To
demonstrate the usefulness of OP_CAT below we provide a non-exhaustive
list of some usecases that OP_CAT would enable:

* Tree Signatures provide a multisignature script whose size can be
logarithmic in the number of public keys and can encode spend
conditions beyond n-of-m. For instance a transaction less than 1KB in
size could support tree signatures with a thousand public keys. This
also enables generalized logical spend conditions. [2]
* Post-Quantum Lamport Signatures in Bitcoin transactions. Lamport
signatures merely requires the ability to hash and concatenate values
on the stack. [3]
* Non-equivocation contracts [4] in tapscript provide a mechanism to
punish equivocation/double spending in Bitcoin payment channels.
OP_CAT enables this by enforcing rules on the spending transaction's
nonce. The capability is a useful building block for payment channels
and other Bitcoin protocols.
* Vaults [5] which are a specialized covenant that allows a user to
block a malicious party who has compromised the user's secret key from
stealing the funds in that output. As shown in <ref>A. Poelstra, "CAT
and Schnorr Tricks II", 2021,
https://www.wpsoftware.net/andrew/blog/cat-and-schnorr-tricks-ii.html</ref>
OP_CAT is sufficent to build vaults in Bitcoin.
* Replicating CheckSigFromStack <ref> A. Poelstra, "CAT and Schnorr
Tricks I", 2021,
https://medium.com/blockstream/cat-and-schnorr-tricks-i-faf1b59bd298
</ref> which would allow the creation of simple covenants and other
advanced contracts without having to presign spending transactions,
possibly reducing complexity and the amount of data that needs to be
stored. Originally shown to work with Schnorr signatures, this result
has been extended to ECDSA signatures. [6]

The opcode OP_CAT was available in early versions of Bitcoin. However
OP_CAT was removed because it enabled the construction of a script for
which an evaluation could have memory usage exponential in the size of
the script.
For instance a script which pushed an 1 Byte value on the stack then
repeated the opcodes OP_DUP, OP_CAT 40 times would result in a stack
value whose size was greater than 1 Terabyte. This is no longer an
issue because tapscript enforces a maximum stack element size of 520
Bytes.

==Specification==

Implementation
<pre>
  if (stack.size() < 2)
    return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
  valtype vch1 = stacktop(-2);
  valtype vch2 = stacktop(-1);

  if (vch1.size() + vch2.size() > MAX_SCRIPT_ELEMENT_SIZE)
      return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);

  valtype vch3;
  vch3.reserve(vch1.size() + vch2.size());
  vch3.insert(vch3.end(), vch1.begin(), vch1.end());
  vch3.insert(vch3.end(), vch2.begin(), vch2.end());

  popstack(stack);
  popstack(stack);
  stack.push_back(vch3);
</pre>

The value of MAX_SCRIPT_ELEMENT_SIZE is 520 Bytes

== Reference Implementation ==
[Elements](https://github.com/ElementsProject/elements/blob/master/src/script/interpreter.cpp#L1043)

==References==

[1]: R. Pike and B. Kernighan, "Program design in the UNIX
environment", 1983,
https://harmful.cat-v.org/cat-v/unix_prog_design.pdf
[2]: P. Wuille, "Multisig on steroids using tree signatures", 2015,
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html
[3]: J. Rubin, "[bitcoin-dev] OP_CAT Makes Bitcoin Quantum Secure [was
CheckSigFromStack for Arithmetic Values]", 2021,
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html
[4]: T. Ruffing, A. Kate, D. Schr?der, "Liar, Liar, Coins on Fire:
Penalizing Equivocation by Loss of Bitcoins", 2015,
https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.727.6262&rep=rep1&type=pdf
[5]: M. Moser, I. Eyal, and E. G. Sirer, Bitcoin Covenants,
http://fc16.ifca.ai/bitcoin/papers/MES16.pdf
[6]: R. Linus, "Covenants with CAT and ECDSA", 2023,
https://gist.github.com/RobinLinus/9a69f5552be94d13170ec79bf34d5e85#file-covenants_cat_ecdsa-md


------------------------------

Message: 2
Date: Fri, 20 Oct 2023 22:58:32 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Peter Todd <pete@petertodd.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: "lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <d8227003b4a6065414d32a31a7020a93@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-10-20 14:09, Peter Todd via bitcoin-dev wrote:
> The basic problem here is after the HTLC-timeout path becomes 
> spendable, the
> HTLC-preimage path remains spendable. That's bad, because in this case 
> we want
> spending the HTLC-preimage - if possible - to have an urgency attached 
> to it to
> ensure that it happens before the previous HTLC-timeout is mined.
> 
> So, why can't we make the HTLC-preimage path expire?

If the goal is to ensure the HTLC-preimage should be mined before an 
upstream HTLC-timeout becomes mineable, then I don't think a consensus 
change is required.  We can just make the HTLC-preimage claimable by 
anyone some time after the HTLC-timeout becomes mineable.

For example, imagine that Alice offers Bob an HTLC with a timeout at 
block t+200.  Bob offers Carol an HTLC with a timeout at block t+100.  
The Bob-Carol HTLC script looks like this:

If
   # Does someone have the preimage?
   Hash <digest> EqualVerify
   If
     # Carol has the preimage at any time
     <Carol key> CheckSig
   Else
     # Anyone else has the preimage after t+150
     <t+150> CLTV
   EndIf
Else
   # Bob is allowed a refund after t+100
   <Bob key> CheckSigVerify
   <t+100> CLTV
EndIf

In English:

- At any time, Carol can spend the output by releasing the preimage
- After t+100, Bob can spend the output
- After t+150, anyone with the preimage can spend the output



Let's consider this in the wider context of the forwarded payment 
Alice->Bob->Carol:

- If Carol attempts to spend the output by releasing the preimage but 
pays too low of a feerate to get it confirmed by block t+100, Bob can 
spend the output in block t+101.  He then has 99 blocks to settle 
(revoke) the Alice-Bob HTLC offchain.

- If Carol releases the preimage to the network in general but prevents 
Bob from using it (e.g. using a replacement cycling attack), anyone who 
saw the preimage can take Carol's output at t+150 and, by doing so, will 
put the preimage in the block chain where Bob will learn about it.  
He'll then have 49 blocks to settle (revoke) the Alice-Bob HTLC 
offchain.

- (All the normal cases when the HTLC is settled offchain, or where 
onchain operations occur in a timely manner)



I think that adequately satisfies the concern about the effect on LN 
from replacement cycling.  Looking at potential complications:

- If all miners acted together[1], they are incentivized to not mine 
Carol's preimage transaction before t+150 because its fees are less than 
the HTLC value they can receive at t+150.  I think this level of miner 
centralization would result in a general failure for LN given that 
miners could be any LN user's counterparty (or bribed by a user's 
counterparty).  E.g., stuff like this: 
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-June/017997.html

- To allow anyone with the preimage to spend the output after t+150, 
they need to know the script.  For taproot, that means the t+150 tapleaf 
script needs to follow a standard (e.g. a BOLT) and that any internal 
merkle nodes needed to connect it to the taproot commitment need to be 
shown in Carol's preimage transaction (or inferable from it or other 
data).

- Classic RBF pinning of the t+150 transaction to prevent it from 
confirming by block t+200 might be an issue.  E.g., including it in a 
400,000 weight low-feerate transaction.

- Full RBF might be required to ensure the t+150 transaction isn't sent 
with a low feerate and no opt-in signal.



Deployment considerations:

- No changes are required to full nodes (no consensus change required)

- No changes are required to mining Bitcoin nodes[2]

- At least one well-connected Bitcoin relay node will need to be updated 
to store preimages and related data, and to send the preimage claim 
transactions.  Data only needs to be kept for a rolling window of a few 
thousand blocks for the LN case, bounding storage requirements.  No 
changes are required to other relaying Bitcoin nodes

- LN nodes will need to update to new HTLC scripts, but this should be 
doable without closing/re-opening channels.  Both anchor and non-anchor 
channels can continue to be used



Compared to OP_EXPIRE:

- OP_EXPIRE requires consensus and policy changes; this does not

- OP_EXPIRE does not depend on special software; this depends on at 
least one person running special software



Although this proposal is an alternative to Peter's proposal and is 
primarily inspired by his idea, it's also a variation on a previous 
suggestion of mine: 
https://lists.linuxfoundation.org/pipermail/lightning-dev/2020-April/002664.html

-Dave

[1] Perhaps under block censorship threat from a mining majority or a 
sub-majority performing selfish mining.

[2] Although miners may want to consider running code that allows them 
to rewrite any malleable transactions to pay themselve


------------------------------

Message: 3
Date: Sat, 21 Oct 2023 10:31:05 +0000
From: Peter Todd <pete@petertodd.org>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>,
	"lightning-dev@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID: <ZTOoadyBiuKnzsgJ@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 10:58:32PM -1000, David A. Harding wrote:
> On 2023-10-20 14:09, Peter Todd via bitcoin-dev wrote:
> > The basic problem here is after the HTLC-timeout path becomes spendable,
> > the
> > HTLC-preimage path remains spendable. That's bad, because in this case
> > we want
> > spending the HTLC-preimage - if possible - to have an urgency attached
> > to it to
> > ensure that it happens before the previous HTLC-timeout is mined.
> > 
> > So, why can't we make the HTLC-preimage path expire?
> 
> If the goal is to ensure the HTLC-preimage should be mined before an
> upstream HTLC-timeout becomes mineable, then I don't think a consensus
> change is required.  We can just make the HTLC-preimage claimable by anyone
> some time after the HTLC-timeout becomes mineable.
> 
> For example, imagine that Alice offers Bob an HTLC with a timeout at block
> t+200.  Bob offers Carol an HTLC with a timeout at block t+100.  The
> Bob-Carol HTLC script looks like this:
> 
> If
>   # Does someone have the preimage?
>   Hash <digest> EqualVerify
>   If
>     # Carol has the preimage at any time
>     <Carol key> CheckSig
>   Else
>     # Anyone else has the preimage after t+150
>     <t+150> CLTV
>   EndIf
> Else
>   # Bob is allowed a refund after t+100
>   <Bob key> CheckSigVerify
>   <t+100> CLTV
> EndIf
> 
> In English:
> 
> - At any time, Carol can spend the output by releasing the preimage
> - After t+100, Bob can spend the output
> - After t+150, anyone with the preimage can spend the output

This is a clever idea. But it doesn't prevent this attack.

Think about it this way: where previously there was one Carol who could perform
the replacement cycling attack, with the anyone-can-spend branch the situation
eventually transforms into a situation where there is an unlimited set of
Carols who can perform the attack and, if they are a miner, benefit from it.

Either way Bob is in a position where they might not learn about the preimage
in time, and thus fail to redeem the received HTLC output.

From Carol's point of view the situation didn't significantly change. Either
they manage to succesfully spend the offered HTLC output after the redeemed
HTLC output times out. Or they fail. Whether or not that failure happens
because Bob got their refund, or someone else spent the offered HTLC output via
the anyone-can-spend path is not relevant to Carol.


Finally, this solution is inferior to OP_Expire in another important way: the
anyone-can-spend branch represents a strict deadline for Bob too. With
OP_Expire, once HTLC preimage branch has expired, Bob can spend the offered
HTLC output at their leisure, as they are the only party with the ability to do
that (assuming of course that we're talking about a valid commitment
transaction, not an illegitmate revoked once).

> [2] Although miners may want to consider running code that allows them to
> rewrite any malleable transactions to pay themselve

With full-RBF _anyone_ can run that code on behalf of miners, modulo edge cases
where the replacement isn't possible due to the RBF anti-DoS rules. Indeed,
people are apparently already doing this to screw over signature-less ordinal
transactions.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/c5a04bb9/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 32
********************************************
