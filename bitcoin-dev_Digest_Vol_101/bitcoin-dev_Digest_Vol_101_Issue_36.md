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

   1. Re: OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer
      by Letting Transactions Expire Safely (vjudeu@gazeta.pl)
   2. Re: Proposed BIP for OP_CAT (vjudeu@gazeta.pl)


----------------------------------------------------------------------

Message: 1
Date: Sun, 22 Oct 2023 10:30:01 +0200
From: vjudeu@gazeta.pl
To: "Peter Todd <pete@petertodd.org>, Bitcoin Protocol Discussion"
	<bitcoin-dev@lists.linuxfoundation.org>, Antoine Riard
	<antoine.riard@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: security@ariard.me, "lightning-dev\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] OP_Expire and Coinbase-Like Behavior:
	Making HTLCs Safer by Letting Transactions Expire Safely
Message-ID:
	<193770517-370d11da072c35721a528135516153d7@pmq5v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> By redefining a bit of the nVersion field, eg the most significant bit, we can apply coinbase-like txout handling to arbitrary transactions.
?
We already have that in OP_CHECKSEQUENCEVERIFY. You can have a system with no coinbase transactions at all, and use only OP_CHECKSEQUENCEVERIFY on the first transaction, and set sequence numbers to put a relative locktime of 100 blocks. Also, if you think some soft-fork is needed anyway, then I recommend building it around already existing OP_CHECKSEQUENCEVERIFY, than reinvent the wheel.
?
> Redefining an existing OP_Nop opcode, OP_Expire would terminate script evaluation with an error
?
This one is also already there. We have reserved opcodes, like OP_RESERVED. You can do something like "<condition> OP_IF OP_RESERVED OP_ENDIF", and then, if "<condition>" is triggered in the Script, the whole transaction is marked as invalid. But if that condition is false, then everything is fine, and you can continue executing next opcodes. Again, the situation is the same as in previous case: build it around OP_RESERVED, that is just "OP_EXPIRE" with a different name than you want, and then the only thing you need, is soft-forking a proper condition on the stack.
?
On 2023-10-21 02:09:55 user Peter Todd via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
On Mon, Oct 16, 2023 at 05:57:36PM +0100, Antoine Riard via bitcoin-dev wrote: > Here enter a replacement cycling attack. A malicious channel counterparty > can broadcast its HTLC-preimage transaction with a higher absolute fee and > higher feerate than the honest HTLC-timeout of the victim lightning node > and triggers a replacement. Both for legacy and anchor output channels, a > HTLC-preimage on a counterparty commitment transaction is malleable, i.e > additional inputs or outputs can be added. The HTLC-preimage spends an > unconfirmed and unrelated to the channel parent transaction M and conflicts > its child. The basic problem here is after the HTLC-timeout path becomes spendable, the HTLC-preimage path remains spendable. That's bad, because in this case we want spending the HTLC-preimage - if possible - to have an urgency attached to it to ensure that it happens before the previous HTLC-timeout is mined. So, why can't we make the HTLC-preimage path expire? Traditionally, we've 
 tried to ensure that transactions - once valid - remain valid forever. We do this because we don't want transactions to become impossible to mine in the event of a large reorganization. A notable example of this design philosophy is seen in Bitcoin's rules around coinbase outputs: they only become spendable after 100 more blocks have been found; a 100 block reorg is quite unlikely. Enter the OP_Expire and the Coinbase Bit soft-fork upgrade. # Coinbase Bit By redefining a bit of the nVersion field, eg the most significant bit, we can apply coinbase-like txout handling to arbitrary transactions. Such a transaction's outputs would be treated similarly to a coinbase transaction, and would be spendable only after 100 more blocks had been mined. Due to this requirement, these transactions will pose no greater risk to reorg safety than the existing hazard of coinbase transactions themselves becoming invalid. Note how such a transaction is non-standard right now, ensuring compatibility with
  existing nodes in a soft-fork upgrade. # OP_Expire Redefining an existing OP_Nop opcode, OP_Expire would terminate script evaluation with an error if: 1) the Coinbase Bit was not set; or 2) the stack is empty; or 3) the top item on the stack was >= the block height of the containing block This is conceptually an AntiCheckLockTimeVerify: where CLTV _allows_ a txout to become spendable in a particular way in the future, Expire _prevents_ a txout from being spent in a particular way. Since OP_Expire requires the Coinbase Bit to be set, the reorg security of OP_Expire-using transactions is no worse than transactions spending miner coinbases. # How HTLC's Would Use OP_Expire Whenever revealing the preimage on-chain is necessary to the secure functioning of the HTLC-using protocol, we simply add an appropriate OP_Expire to the pre-image branch of the script along the lines of: If Expire Drop Hash EqualVerify CheckSig ElseIf # HTLC Expiration conditions ... EndIf Now the party receiving t
 he pre-image has a deadline. Either they get a transaction spending the preimage mined, notifying the other party via the blockchain itself, or they fail to get the preimage mined in time, reverting control to the other party who can spend the HTLC output at their leisure, without strict time constraints. Since the HTLC-expired branch does *not* execute OP_Expire, the transaction spending the HTLC-expired branch does *not* need to set the Coinbase Bit. Thus it can be spent in a perfectly normal transaction, without restrictions. # Delta Encoding Expiration Rather than having a specific Coinbase Bit, it may also be feasible to encode the expiration height as a delta against a block-height nLockTime. In this variant, OP_Expire would work similarly to OP_CheckLockTimeVerify, by checking that the absolute expiration height was <= the requested expiration, allowing multiple HTLC preimage outputs to be spent in one transaction. If the top 16-bits were used, the maximum period a transactio
 n could be valid would be: 2^16 blocks / 144 blocks/day = 455 days In this variant, a non-zero expiration delta would enable expiration behavior, as well as the coinbase-like output spending restriction. The remaining 16-bits of nVersion would remain available for other meanings. Similar to how CLTV and CSV verified nLockTime and nSequence respectively, verifying an expiration height encoded in the nVersion has the advantage of making an expiration height easy to detect without validating scripts. While Lightning's HTLC-success transactions currently use nLockTime=0, AFAIK there is no reason why they could not set nLockTime to be valid in the next block, allowing delta encoding to be used. ## Reusing Time-Based nLockTime Reusing time-based nLockTime's prior to some pre-2009 genesis point for expiration is another possibility (similar to how Lightning makes use of time-based nLockTime for signalling). However I believe this is not as desirable as delta encoding or a coinbase bit, as 
 it would prevent transactions from using block nLockTime and expiration at the same time. It would also still require a coinbase bit or nVersion increase to ensure expiration-using transactions are non-standard. # Mempool Behavior Obviously, mempool logic will need to handle transactions that can expire differently than non-expiring transactions. One notable consideration is that nodes should require higher minimum relay fees for transactions close to their expiration height to ensure we don't waste bandwidth on transactions that have no potential to be mined. Considering the primary use-case, it is probably acceptable to always require a fee rate high enough to be mined in the next block. -- https://petertodd.org 'peter'[:-1]@petertodd.org _______________________________________________ bitcoin-dev mailing list bitcoin-dev@lists.linuxfoundation.org https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231022/2acbf029/attachment-0001.html>

------------------------------

Message: 2
Date: Sun, 22 Oct 2023 10:58:07 +0200
From: vjudeu@gazeta.pl
To: "Ethan Heilman <eth3rs@gmail.com>, Bitcoin Protocol Discussion"
	<bitcoin-dev@lists.linuxfoundation.org>, Bitcoin Dev
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<194372901-852eeb9299035adb7fdfc7fe5aa21080@pmq3v.m5r2.onet>
Content-Type: text/plain; charset="utf-8"

> This opcode would be activated via a soft fork by redefining the opcode OP_SUCCESS80.
?
Why OP_SUCCESS80, and not OP_SUCCESS126? When there is some existing opcode, it should be reused. And if OP_RESERVED will ever be re-enabled, I think it should behave in the same way, as in pre-Taproot, so it should "Mark transaction as invalid unless occuring in an unexecuted OP_IF branch". Which means, "<condition> OP_VERIFY" should be equivalent to "<condition> OP_NOTIF OP_RESERVED OP_ENDIF".
?
On 2023-10-21 07:09:13 user Ethan Heilman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
Hi everyone, We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode. https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki OP_CAT was available in early versions of Bitcoin. It was disabled as it allowed the construction of a script whose evaluation could create stack elements exponential in the size of the script. This is no longer an issue in the current age as tapscript enforces a maximum stack element size of 520 Bytes. Thanks, Ethan ==Abstract== This BIP defines OP_CAT a new tapscript opcode which allows the concatenation of two values on the stack. This opcode would be activated via a soft fork by redefining the opcode OP_SUCCESS80. When evaluated the OP_CAT instruction: # Pops the top two values off the stack, # concatenate the popped values together, # and then pushes the concatenated value on the top of the stack. OP_CAT fails if there are less than two values on the stack or if a concatenated value would have a combined size of greater than t
 he maximum script element size of 520 Bytes. ==Motivation== Bitcoin tapscript lacks a general purpose way of combining objects on the stack restricting the expressiveness and power of tapscript. For instance this prevents among many other things the ability to construct and evaluate merkle trees and other hashed data structures in tapscript. OP_CAT by adding a general purpose way to concatenate stack values would overcome this limitation and greatly increase the functionality of tapscript. OP_CAT aims to expand the toolbox of the tapscript developer with a simple, modular and useful opcode in the spirit of Unix[1]. To demonstrate the usefulness of OP_CAT below we provide a non-exhaustive list of some usecases that OP_CAT would enable: * Tree Signatures provide a multisignature script whose size can be logarithmic in the number of public keys and can encode spend conditions beyond n-of-m. For instance a transaction less than 1KB in size could support tree signatures with a thousand p
 ublic keys. This also enables generalized logical spend conditions. [2] * Post-Quantum Lamport Signatures in Bitcoin transactions. Lamport signatures merely requires the ability to hash and concatenate values on the stack. [3] * Non-equivocation contracts [4] in tapscript provide a mechanism to punish equivocation/double spending in Bitcoin payment channels. OP_CAT enables this by enforcing rules on the spending transaction's nonce. The capability is a useful building block for payment channels and other Bitcoin protocols. * Vaults [5] which are a specialized covenant that allows a user to block a malicious party who has compromised the user's secret key from stealing the funds in that output. As shown in A. Poelstra, "CAT and Schnorr Tricks II", 2021, https://www.wpsoftware.net/andrew/blog/cat-and-schnorr-tricks-ii.html OP_CAT is sufficent to build vaults in Bitcoin. * Replicating CheckSigFromStack A. Poelstra, "CAT and Schnorr Tricks I", 2021, https://medium.com/blockstream/cat-an
 d-schnorr-tricks-i-faf1b59bd298 which would allow the creation of simple covenants and other advanced contracts without having to presign spending transactions, possibly reducing complexity and the amount of data that needs to be stored. Originally shown to work with Schnorr signatures, this result has been extended to ECDSA signatures. [6] The opcode OP_CAT was available in early versions of Bitcoin. However OP_CAT was removed because it enabled the construction of a script for which an evaluation could have memory usage exponential in the size of the script. For instance a script which pushed an 1 Byte value on the stack then repeated the opcodes OP_DUP, OP_CAT 40 times would result in a stack value whose size was greater than 1 Terabyte. This is no longer an issue because tapscript enforces a maximum stack element size of 520 Bytes. ==Specification== Implementation if (stack.size() < 2) return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION); valtype vch1 = stacktop(-2); val
 type vch2 = stacktop(-1); if (vch1.size() + vch2.size() > MAX_SCRIPT_ELEMENT_SIZE) return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION); valtype vch3; vch3.reserve(vch1.size() + vch2.size()); vch3.insert(vch3.end(), vch1.begin(), vch1.end()); vch3.insert(vch3.end(), vch2.begin(), vch2.end()); popstack(stack); popstack(stack); stack.push_back(vch3); The value of MAX_SCRIPT_ELEMENT_SIZE is 520 Bytes == Reference Implementation == [Elements](https://github.com/ElementsProject/elements/blob/master/src/script/interpreter.cpp#L1043) ==References== [1]: R. Pike and B. Kernighan, "Program design in the UNIX environment", 1983, https://harmful.cat-v.org/cat-v/unix_prog_design.pdf [2]: P. Wuille, "Multisig on steroids using tree signatures", 2015, https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html [3]: J. Rubin, "[bitcoin-dev] OP_CAT Makes Bitcoin Quantum Secure [was CheckSigFromStack for Arithmetic Values]", 2021, https://lists.linuxfoundation.org/pipermail
 /bitcoin-dev/2021-July/019233.html [4]: T. Ruffing, A. Kate, D. Schr?der, "Liar, Liar, Coins on Fire: Penalizing Equivocation by Loss of Bitcoins", 2015, https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.727.6262&rep=rep1&type=pdf [5]: M. Moser, I. Eyal, and E. G. Sirer, Bitcoin Covenants, http://fc16.ifca.ai/bitcoin/papers/MES16.pdf [6]: R. Linus, "Covenants with CAT and ECDSA", 2023, https://gist.github.com/RobinLinus/9a69f5552be94d13170ec79bf34d5e85#file-covenants_cat_ecdsa-md _______________________________________________ bitcoin-dev mailing list bitcoin-dev@lists.linuxfoundation.org https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231022/bc577761/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 36
********************************************
