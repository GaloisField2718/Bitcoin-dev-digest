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

   1. Re: Proposed BIP for OP_CAT (Ethan Heilman)


----------------------------------------------------------------------

Message: 1
Date: Wed, 25 Oct 2023 21:53:44 -0400
From: Ethan Heilman <eth3rs@gmail.com>
To: Steven Roose <steven@roose.io>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<CAEM=y+X_VL8ZRsVhrcG6ymK=k75MUteZ5c8qxA+LPyCf7LxHpA@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

If there is sufficient interest in enabling OP_CAT on Bitcoin and
there is a strong desire in the community for using OP_SUCCESS126
rather than OP_SUCCESS80 then I'd be happy to switch to OP_SUCCESS126.
I don't have any particular affinity for OP_SUCCESS80.

Is there anyone who objects to using OP_SUCCESS126 rather than OP_SUCCESS80?

On Tue, Oct 24, 2023 at 4:12?PM Steven Roose via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> I agree that there is no reason not to use OP_SUCCESS126, i.e. the original OP_CAT opcode 0x7e. In many codebases, for example in Core, there might be two OP_CAT constants than which might be confusing.
>
> On 10/22/23 09:58, vjudeu via bitcoin-dev wrote:
>
> > This opcode would be activated via a soft fork by redefining the opcode OP_SUCCESS80.
>
> Why OP_SUCCESS80, and not OP_SUCCESS126? When there is some existing opcode, it should be reused. And if OP_RESERVED will ever be re-enabled, I think it should behave in the same way, as in pre-Taproot, so it should "Mark transaction as invalid unless occuring in an unexecuted OP_IF branch". Which means, "<condition> OP_VERIFY" should be equivalent to "<condition> OP_NOTIF OP_RESERVED OP_ENDIF".
>
>
>
> On 2023-10-21 07:09:13 user Ethan Heilman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> Hi everyone,
>
> We've posted a draft BIP to propose enabling OP_CAT as Tapscript opcode.
> https://github.com/EthanHeilman/op_cat_draft/blob/main/cat.mediawiki
>
> OP_CAT was available in early versions of Bitcoin. It was disabled as
> it allowed the construction of a script whose evaluation could create
> stack elements exponential in the size of the script. This is no
> longer an issue in the current age as tapscript enforces a maximum
> stack element size of 520 Bytes.
>
> Thanks,
> Ethan
>
> ==Abstract==
>
> This BIP defines OP_CAT a new tapscript opcode which allows the
> concatenation of two values on the stack. This opcode would be
> activated via a soft fork by redefining the opcode OP_SUCCESS80.
>
> When evaluated the OP_CAT instruction:
> # Pops the top two values off the stack,
> # concatenate the popped values together,
> # and then pushes the concatenated value on the top of the stack.
>
> OP_CAT fails if there are less than two values on the stack or if a
> concatenated value would have a combined size of greater than the
> maximum script element size of 520 Bytes.
>
> ==Motivation==
> Bitcoin tapscript lacks a general purpose way of combining objects on
> the stack restricting the expressiveness and power of tapscript. For
> instance this prevents among many other things the ability to
> construct and evaluate merkle trees and other hashed data structures
> in tapscript. OP_CAT by adding a general purpose way to concatenate
> stack values would overcome this limitation and greatly increase the
> functionality of tapscript.
>
> OP_CAT aims to expand the toolbox of the tapscript developer with a
> simple, modular and useful opcode in the spirit of Unix[1]. To
> demonstrate the usefulness of OP_CAT below we provide a non-exhaustive
> list of some usecases that OP_CAT would enable:
>
> * Tree Signatures provide a multisignature script whose size can be
> logarithmic in the number of public keys and can encode spend
> conditions beyond n-of-m. For instance a transaction less than 1KB in
> size could support tree signatures with a thousand public keys. This
> also enables generalized logical spend conditions. [2]
> * Post-Quantum Lamport Signatures in Bitcoin transactions. Lamport
> signatures merely requires the ability to hash and concatenate values
> on the stack. [3]
> * Non-equivocation contracts [4] in tapscript provide a mechanism to
> punish equivocation/double spending in Bitcoin payment channels.
> OP_CAT enables this by enforcing rules on the spending transaction's
> nonce. The capability is a useful building block for payment channels
> and other Bitcoin protocols.
> * Vaults [5] which are a specialized covenant that allows a user to
> block a malicious party who has compromised the user's secret key from
> stealing the funds in that output. As shown in A. Poelstra, "CAT
> and Schnorr Tricks II", 2021,
> https://www.wpsoftware.net/andrew/blog/cat-and-schnorr-tricks-ii.html
> OP_CAT is sufficent to build vaults in Bitcoin.
> * Replicating CheckSigFromStack  A. Poelstra, "CAT and Schnorr
> Tricks I", 2021,
> https://medium.com/blockstream/cat-and-schnorr-tricks-i-faf1b59bd298
>  which would allow the creation of simple covenants and other
> advanced contracts without having to presign spending transactions,
> possibly reducing complexity and the amount of data that needs to be
> stored. Originally shown to work with Schnorr signatures, this result
> has been extended to ECDSA signatures. [6]
>
> The opcode OP_CAT was available in early versions of Bitcoin. However
> OP_CAT was removed because it enabled the construction of a script for
> which an evaluation could have memory usage exponential in the size of
> the script.
> For instance a script which pushed an 1 Byte value on the stack then
> repeated the opcodes OP_DUP, OP_CAT 40 times would result in a stack
> value whose size was greater than 1 Terabyte. This is no longer an
> issue because tapscript enforces a maximum stack element size of 520
> Bytes.
>
> ==Specification==
>
> Implementation
>
>   if (stack.size() < 2)
>     return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>   valtype vch1 = stacktop(-2);
>   valtype vch2 = stacktop(-1);
>
>   if (vch1.size() + vch2.size() > MAX_SCRIPT_ELEMENT_SIZE)
>       return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>
>   valtype vch3;
>   vch3.reserve(vch1.size() + vch2.size());
>   vch3.insert(vch3.end(), vch1.begin(), vch1.end());
>   vch3.insert(vch3.end(), vch2.begin(), vch2.end());
>
>   popstack(stack);
>   popstack(stack);
>   stack.push_back(vch3);
>
> The value of MAX_SCRIPT_ELEMENT_SIZE is 520 Bytes == Reference Implementation == [Elements](https://github.com/ElementsProject/elements/blob/master/src/script/interpreter.cpp#L1043) ==References== [1]: R. Pike and B. Kernighan, "Program design in the UNIX environment", 1983, https://harmful.cat-v.org/cat-v/unix_prog_design.pdf [2]: P. Wuille, "Multisig on steroids using tree signatures", 2015, https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html [3]: J. Rubin, "[bitcoin-dev] OP_CAT Makes Bitcoin Quantum Secure [was CheckSigFromStack for Arithmetic Values]", 2021, https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html [4]: T. Ruffing, A. Kate, D. Schr?der, "Liar, Liar, Coins on Fire: Penalizing Equivocation by Loss of Bitcoins", 2015, https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.727.6262&rep=rep1&type=pdf [5]: M. Moser, I. Eyal, and E. G. Sirer, Bitcoin Covenants, http://fc16.ifca.ai/bitcoin/papers/MES16.pdf [6]: R. Linus,
  "Covenants with CAT and ECDSA", 2023, https://gist.github.com/RobinLinus/9a69f5552be94d13170ec79bf34d5e85#file-covenants_cat_ecdsa-md _______________________________________________ bitcoin-dev mailing list bitcoin-dev@lists.linuxfoundation.org https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
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

End of bitcoin-dev Digest, Vol 101, Issue 44
********************************************
