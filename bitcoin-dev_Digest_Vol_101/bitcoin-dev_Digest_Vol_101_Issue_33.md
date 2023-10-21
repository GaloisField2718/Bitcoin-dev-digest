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

   1. Re: Breaking change in calculation of	hash_serialized_2 (Fabian)
   2. Re: Proposed BIP for OP_CAT (alicexbt)
   3. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Nagaev Boris)
   4. Re: Proposed BIP for OP_CAT (Andrew Poelstra)
   5. Re: Proposed BIP for OP_CAT (Greg Sanders)


----------------------------------------------------------------------

Message: 1
Date: Fri, 20 Oct 2023 22:01:40 +0000
From: Fabian <fjahr@protonmail.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Breaking change in calculation of
	hash_serialized_2
Message-ID:
	<aAzprT3_Jlpgb6Z_sFOiC1q9KMmB9mCTaCk19hO8oe0vA1Z__kQhzprdDZblXGvR2_xTaUYk67RNFGxJcnm5QkAmi_PE8d51E80z077FpoM=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Peter,

to my knowledge, this was never considered as an option previously (James correct me if I am wrong). At least I couldn't find any reference to that in the original proposal [1] and I can not remember it being discussed since I have followed the project more closely (ca. 2020).

Here are the reasons that I can think of why that might be the case:

- If the serialization and hashing of the UTXO set works as intended, that hash should be working just as well as the flat file hash and hash_serialized_2 certainly was assumed to be robust since it has been around for a very long time. So it may simply have been viewed as additional overhead.
- We may want to optimize the serialization of data to file further, adding compression, etc. to have smaller files that result in the same UTXO set without having to change the chainparams committing to that UTXO set or potentially having multiple file hashes for the same block.
- We may want to introduce other file hashing strategies instead that are more optimized for P2P sharing of the UTXO snapshots. P2P sharing the UTXO set has always been part of the idea of assumeutxo but so far it hasn't been explored very deeply. For more on this see the conversation on IRC that started in the meeting yesterday between sipa, aj et al [2][3].

Cheers,
Fabian

[1] https://github.com/jamesob/assumeutxo-docs/tree/2019-04-proposal/proposal
[2] https://bitcoin-irc.chaincode.com/bitcoin-core-dev/2023-10-19#976439;
[3] https://bitcoin-irc.chaincode.com/bitcoin-core-dev/2023-10-20#976636;

------- Original Message -------
On Friday, October 20th, 2023 at 7:34 PM, Peter Todd <pete@petertodd.org> wrote:


> On Fri, Oct 20, 2023 at 05:19:19PM +0000, Fabian via bitcoin-dev wrote:
> 
> > Hello list,
> > 
> > on Wednesday I found a potential malleability issue in the UTXO set dump files
> > generated for and used by assumeutxo [1]. On Thursday morning theStack had
> > found the cause of the issue [2]: A bug in the serialization of UTXOs for the
> > calculation of hash_serialized_2. This is the value used by Bitcoin Core to
> > check if the UTXO set loaded from a dump file matches what is expected. The
> > value of hash_serialized_2 expected for a particular block is hardcoded into
> > the chainparams of each chain.
> 
> 
> <snip>
> 
> > [1] https://github.com/bitcoin/bitcoin/issues/28675
> > [2] https://github.com/bitcoin/bitcoin/issues/28675#issuecomment-1770389468[3] https://github.com/bitcoin/bitcoin/pull/28685
> 
> 
> James made the following comment on the above issue:
> 
> > Wow, good find @fjahr et al. I wonder if there's any value in committing to a
> > sha256sum of the snapshot file itself in the source code as a
> > belt-and-suspenders remediation for issues like this.
> 
> 
> Why isn't the sha256 hash of the snapshot file itself the canonical hash?
> That would obviously eliminate any malleability issues. gettxoutsetinfo already
> has to walk the entire UTXO set to calculate the hash. Making it simply
> generate the actual contents of the dump file and calculate the hash of it is
> the obvious way to implement this.
> 
> --
> https://petertodd.org 'peter'[:-1]@petertodd.org


------------------------------

Message: 2
Date: Sat, 21 Oct 2023 05:49:59 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Ethan Heilman <eth3rs@gmail.com>
Cc: Bitcoin Dev <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<FyACu9CRVXwjOFUA4w_4I884yIFerThlYDDiXYVKfBbAyF5H8DQP6ZzqbNpaMpDt9RZN2fQqaJfk20Zp-R660l6cQZ6l8ZdylTDI8X40H50=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Ethan,

> [2]: P. Wuille, "Multisig on steroids using tree signatures", 2015,
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html

Correct link for "Multisig on steroids using tree signatures": https://blog.blockstream.com/en-treesignatures/

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Saturday, October 21st, 2023 at 10:38 AM, Ethan Heilman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


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
> stealing the funds in that output. As shown in <ref>A. Poelstra, "CAT
> 
> and Schnorr Tricks II", 2021,
> https://www.wpsoftware.net/andrew/blog/cat-and-schnorr-tricks-ii.html</ref>
> 
> OP_CAT is sufficent to build vaults in Bitcoin.
> * Replicating CheckSigFromStack <ref> A. Poelstra, "CAT and Schnorr
> 
> Tricks I", 2021,
> https://medium.com/blockstream/cat-and-schnorr-tricks-i-faf1b59bd298
> </ref> which would allow the creation of simple covenants and other
> 
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
> <pre>
> 
> if (stack.size() < 2)
> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
> valtype vch1 = stacktop(-2);
> valtype vch2 = stacktop(-1);
> 
> if (vch1.size() + vch2.size() > MAX_SCRIPT_ELEMENT_SIZE)
> 
> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
> 
> valtype vch3;
> vch3.reserve(vch1.size() + vch2.size());
> vch3.insert(vch3.end(), vch1.begin(), vch1.end());
> vch3.insert(vch3.end(), vch2.begin(), vch2.end());
> 
> popstack(stack);
> popstack(stack);
> stack.push_back(vch3);
> </pre>
> 
> 
> The value of MAX_SCRIPT_ELEMENT_SIZE is 520 Bytes
> 
> == Reference Implementation ==
> Elements
> 
> ==References==
> 
> [1]: R. Pike and B. Kernighan, "Program design in the UNIX
> environment", 1983,
> https://harmful.cat-v.org/cat-v/unix_prog_design.pdf
> [2]: P. Wuille, "Multisig on steroids using tree signatures", 2015,
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html
> [3]: J. Rubin, "[bitcoin-dev] OP_CAT Makes Bitcoin Quantum Secure [was
> CheckSigFromStack for Arithmetic Values]", 2021,
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html
> [4]: T. Ruffing, A. Kate, D. Schr?der, "Liar, Liar, Coins on Fire:
> Penalizing Equivocation by Loss of Bitcoins", 2015,
> https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.727.6262&rep=rep1&type=pdf
> [5]: M. Moser, I. Eyal, and E. G. Sirer, Bitcoin Covenants,
> http://fc16.ifca.ai/bitcoin/papers/MES16.pdf
> [6]: R. Linus, "Covenants with CAT and ECDSA", 2023,
> https://gist.github.com/RobinLinus/9a69f5552be94d13170ec79bf34d5e85#file-covenants_cat_ecdsa-md
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 3
Date: Sat, 21 Oct 2023 11:21:48 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID:
	<CAFC_Vt4-DXkEPZEfXzZQET7P9KSyOrgojGqr8w-xvTECeRn7Zw@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

I think the presigned transactions should be interleaved fee-wise:
1.1 to Alice
1.2 to Bob
1.3 to Alice
1.4 to Bob
...

Then any such transaction evicts all previous transactions in the
chain. It reduces risks of mempool split.

If there are two transactions to Alice and to Bob both with fee 1.1,
then it is possible that half of nodes have the transaction to Alice
in their mempools and another half of nodes has the transaction to
Bob. Though I don't see how exactly this can be used in replacement
cycling attacks, I think it is safer to prevent this scenario.

On Fri Oct 20 18:35:26 UTC 2023, Matt Morehouse via bitcoin-dev wrote:
> I think if we apply this presigned fee multiplier idea to HTLC spends,
> we can prevent replacement cycles from happening.

> We could modify HTLC scripts so that *both* parties can only spend the
> HTLC via presigned second-stage transactions, and we can always sign
> those with SIGHASH_ALL.  This will prevent the attacker from adding
> inputs to their presigned transaction, so (AFAICT) a replacement
> cycling attack becomes impossible.

> The tradeoff is more bookkeeping and less fee granularity when
> claiming HTLCs on chain.


-- 
Best regards,
Boris Nagaev


------------------------------

Message: 4
Date: Sat, 21 Oct 2023 15:03:07 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Ethan Heilman <eth3rs@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID: <ZTPoK3aD8kFyhy3T@camus>
Content-Type: text/plain; charset="us-ascii"

On Sat, Oct 21, 2023 at 01:08:03AM -0400, Ethan Heilman via bitcoin-dev wrote:
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

Thanks, Ethan! This is really great, thank you for pushing forward and
writing up the BIP text.

In addition to the usecases listed in the text, I think CAT would open
up a wide range of Bitcoin script research and let us test nontrivial
things, in perhaps inefficient ways, in real life, befoer proposing
dedicated opcodes. When spitballing about ways to do cool stuff with
Bitcoin Script, I'd say about 90% of the time it ends with "we could do
this if only we had CAT". And the remaining 10% usually don't need much
more.

As evidenced by the short text and short implementation code, CAT is
very simple but provides a ton of value. There is a temptation to try
to bundle other opcodes in with this (for example, rolling SHA256
opcodes to allow hashing more than 520 bytes of data) but I think:

* There is no logical end to the list of opcodes we'd like to add, so
  this will invite an interminable amount of bikeshedding.

* No single opcode comes close to the power of CAT (except super
  general-purpose opcodes like OP_ZKP_VERIFY :))

* Most everything is more controversial than we expect. You can find
  Matt's "consensus cleanup" BIP from a couple years ago which did 4
  small things and I think that all 4 got a bunch of pushback.

So I think we should stick with "just CAT" :).

-- 
Andrew Poelstra
Director of Research, Blockstream
Email: apoelstra at wpsoftware.net
Web:   https://www.wpsoftware.net/andrew

The sun is always shining in space
    -Justin Lewis-Webster

-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 488 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/e71f4941/attachment-0001.sig>

------------------------------

Message: 5
Date: Sat, 21 Oct 2023 12:10:00 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Ethan Heilman <eth3rs@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Proposed BIP for OP_CAT
Message-ID:
	<CAB3F3DuV8SHc+fKVEpvWBBE0+=tqJX7pr0Xzhmtj=bQfKbx0eg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> This is no
longer an issue in the current age as tapscript enforces a maximum
stack element size of 520 Bytes.

I don't think there's a new limit related to tapscript? In the very
beginning there was no limit, but a 5k limit was put into place, then 520
the same commit that OP_CAT was
disabled: 4bd188c4383d6e614e18f79dc337fbabe8464c82

On Sat, Oct 21, 2023 at 1:09?AM Ethan Heilman via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

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
> stealing the funds in that output. As shown in <ref>A. Poelstra, "CAT
> and Schnorr Tricks II", 2021,
> https://www.wpsoftware.net/andrew/blog/cat-and-schnorr-tricks-ii.html
> </ref>
> OP_CAT is sufficent to build vaults in Bitcoin.
> * Replicating CheckSigFromStack <ref> A. Poelstra, "CAT and Schnorr
> Tricks I", 2021,
> https://medium.com/blockstream/cat-and-schnorr-tricks-i-faf1b59bd298
> </ref> which would allow the creation of simple covenants and other
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
> <pre>
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
> </pre>
>
> The value of MAX_SCRIPT_ELEMENT_SIZE is 520 Bytes
>
> == Reference Implementation ==
> [Elements](
> https://github.com/ElementsProject/elements/blob/master/src/script/interpreter.cpp#L1043
> )
>
> ==References==
>
> [1]: R. Pike and B. Kernighan, "Program design in the UNIX
> environment", 1983,
> https://harmful.cat-v.org/cat-v/unix_prog_design.pdf
> [2]: P. Wuille, "Multisig on steroids using tree signatures", 2015,
>
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html
> [3]: J. Rubin, "[bitcoin-dev] OP_CAT Makes Bitcoin Quantum Secure [was
> CheckSigFromStack for Arithmetic Values]", 2021,
>
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019233.html
> [4]: T. Ruffing, A. Kate, D. Schr?der, "Liar, Liar, Coins on Fire:
> Penalizing Equivocation by Loss of Bitcoins", 2015,
>
> https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.727.6262&rep=rep1&type=pdf
> [5]: M. Moser, I. Eyal, and E. G. Sirer, Bitcoin Covenants,
> http://fc16.ifca.ai/bitcoin/papers/MES16.pdf
> [6]: R. Linus, "Covenants with CAT and ECDSA", 2023,
>
> https://gist.github.com/RobinLinus/9a69f5552be94d13170ec79bf34d5e85#file-covenants_cat_ecdsa-md
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/8443b2a8/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 33
********************************************
