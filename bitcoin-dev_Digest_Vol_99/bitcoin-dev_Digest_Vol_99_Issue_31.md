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

   1. Re: BIP for Serverless Payjoin (Dan Gould)
   2. Re: Concrete MATT opcodes (Antoine Riard)
   3. Re: Blinded 2-party Musig2 (Lloyd Fournier)


----------------------------------------------------------------------

Message: 1
Date: Sun, 13 Aug 2023 12:50:32 +0000
From: Dan Gould <d@ngould.dev>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, dave@dtrt.org
Subject: Re: [bitcoin-dev] BIP for Serverless Payjoin
Message-ID: <92588478-9239-4D85-89E5-B6EDE3068FCF@ngould.dev>
Content-Type: text/plain; charset=utf-8

Thanks for weighing in Dave,

> On Aug 13, 2023, at 8:00 AM, bitcoin-dev-request@lists.linuxfoundation.org wrote:
> 
> 

> The way BItcoin users currently use BIP21 URIs and QR-encoded BIP21 URIs, posting them where evesdroppers can see
> 
> ?
> 
> I don't think it would be practical to change that expectation, and I think a protocol where evesdropping didn't create a risk of funds loss would be much better than one where that risk was created.
> 
> dave@dtrt.org

The BIP has changed to adopt a DH cryptosystem where the receiver only shares a public key in the BIP 21 as part of the pj= endpoint since Adam posted comments. I agree enabling the simplest asynchronous experience while, as I gather you?re thinking, keeping the UX expectation that leaked BIP 21 URIs pose no risk for loss of funds is the right set of tradeoffs.

Dan




------------------------------

Message: 2
Date: Mon, 14 Aug 2023 04:00:57 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Salvatore Ingala <salvatore.ingala@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Concrete MATT opcodes
Message-ID:
	<CALZpt+F251k7gSpogwFYHxFtGxc_tZjB4UU4SVEr=WvrsyMVMQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Salvatore,

> This also allows inspection of other inputs, that was not possible with
the original opcodes.

I think cross-input inspection (not cross-input signature aggregation which
is different) is opening a pandora box in terms of "malicious" off-chain
contracts than one could design. E.g miners bribing contracts to censor the
confirmation of time-sensitive lightning channel transactions, where the
bribes are paid on the hashrate distribution of miners during the previous
difficulty period, thanks to the coinbase pubkey.

See https://blog.bitmex.com/txwithhold-smart-contracts/ and
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-February/021395.html

I wonder if we might face the dilemma of miners censorship attacks, if we
wish to have more advanced bitcoin contracts, though I think it would be
safe design practice to rule out those types of concerns thanks to smart
bitcoin contracting primitives.

I think this is a common risk to all second-layers vaults, lightning
channels and payment pools.

> A flag can disable this behavior"

More than a binary flag like a matrix could be introduced to encode subset
of introspected inputs /outputs to enable sighash_group-like semantic:
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019243.html

> There are two defined flags:
> - CCV_FLAG_CHECK_INPUT = 1: if present, <index> refers to an input;
>  otherwise, it refers to an output.
> - CCV_FLAG_IGNORE_OUTPUT_AMOUNT = 2: only defined when _CHECK_INPUT
>  is absent, it disables the deferred checks logic for amounts.

Or even beyond a matrix, it could be a set of "tags". There could be a
generalized tag for unstructured data, and another one for bitcoin
transaction / script data types (e.g scriptpubkey, amount, nsequence,
merkle branch) that could be fetched from the taproot annex.

> After the evaluation of all inputs, it is verified that each output's
> amount is greater than or equal to the total amount in the bucket
> if that output (validation of the deferred checks).

At the very least, I think for the payment pool, where you're fanning-out
satoshis value from a subset of inputs to another subset of outputs, I
think you would need more malleability here.

> It is unclear if all the special values above will be useful in
> applications; however, as each special case requires very little added
> code, I tried to make the specs as flexible as possible at this time.

I think this generic framework is interesting for joinpool / coinpool /
payment pool, as you can check that any withdrawal output can be committed
as part of the input scriptpubkey, and spend it on
blessed-with-one-participant-sig script. There is still a big open question
if it's efficient in terms of witness space consumed.

That said, I still think you would need at least ANYPREVOUT and more
malleability for the amount transfer validation as laid out above.

Looking on the `DeferredCheck` framework commit, one obvious low-level
concern is the DoS risk for full-nodes participating in transaction-relay,
and that maybe policy rules should be introduced to keep the worst-CPU
input in the ranges of current transaction spend allowed to propagate on
the network today.

Thanks for the proposal,

Best,
Antoine



Le dim. 30 juil. 2023 ? 22:52, Salvatore Ingala via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> a ?crit :

> Hi all,
>
> I have put together a first complete proposal for the core opcodes of
> MATT [1][2].
> The changes make the opcode functionally complete, and the
> implementation is revised and improved.
>
> The code is implemented in the following fork of the
> bitcoin-inquisition repo:
>
> https://github.com/Merkleize/bitcoin/tree/checkcontractverify
>
> Therefore, it also includes OP_CHECKTEMPLATEVERIFY, as in a
> previous early demo for vaults [3].
>
> Please check out the diff [4] if you are interested in the
> implementation details. It includes some basic functional tests for
> the main cases of the opcode.
>
> ## Changes vs the previous draft
>
> These are the changes compared to the initial incomplete proposal:
> - OP_CHECK{IN,OUT}CONTRACTVERIFY are replaced by a single opcode
>   OP_CHECKCONTRACTVERIFY (CCV). An additional `flags` parameter allows
>   to specify if the opcode operates on an input or an output.
>   This also allows inspection of other inputs, that was not possible
>   with the original opcodes.
> - For outputs, the default behavior is to have the following deferred
>   checks mechanism for amounts: all the inputs that have a CCV towards
>   the same output, have their input amounts summed, and that act as a
>   lower bound for that output's amount.
>   A flag can disable this behavior. [*]
> - A number of special values of the parameters were defined in order
>   to optimize for common cases, and add some implicit introspection.
> - The order of parameters is modified (particularly, <data> is at the
>   bottom of the arguments, as so is more natural when writing Scripts).
>
> ## Semantics
>
> The new OP_CHECKCONTRACTVERIFY takes 5 parameters from the stack:
>
>   <data>, <index>, <pk>, <taptree>, <flags>
>
> The core logic of the opcode is as follows:
>
> "Check if the <index>-th input/output's scriptPubKey is a P2TR
> whose public key is obtained from <pk>, (optionally) tweaked with
> <data>, (optionally) tap-tweaked with <taptree>".
>
> The following are special values of the parameters:
>
> - if <pk> is empty, it is replaced with a fixed NUMS point. [**]
> - if <pk> is -1, it is replaced with the current input's taproot
>   internal key.
> - if <index> is -1, it is replaced with the current input's index.
> - if <data> is empty, the data tweak is skipped.
> - if <taptree> is empty, the taptweak is skipped.
> - if <taptree> is -1, it is replaced with the current input's root
>   of the taproot merkle tree.
>
> There are two defined flags:
> - CCV_FLAG_CHECK_INPUT = 1: if present, <index> refers to an input;
>   otherwise, it refers to an output.
> - CCV_FLAG_IGNORE_OUTPUT_AMOUNT = 2: only defined when _CHECK_INPUT
>   is absent, it disables the deferred checks logic for amounts.
>
> Finally, if both the flags CCV_FLAG_CHECK_INPUT and
> CCV_FLAG_IGNORE_OUTPUT_AMOUNT are absent:
>   - Add the current input's amount to the <index>-th output's bucket.
>
> After the evaluation of all inputs, it is verified that each output's
> amount is greater than or equal to the total amount in the bucket
> if that output (validation of the deferred checks).
>
> ## Comment
>
> It is unclear if all the special values above will be useful in
> applications; however, as each special case requires very little added
> code, I tried to make the specs as flexible as possible at this time.
>
> With this new opcode, the full generality of MATT (including the fraud
> proofs) can be obtained with just two opcodes: OP_CHECKCONTRACTVERIFY
> and OP_CAT.
> However, additional opcodes (and additional introspection) would
> surely benefit some applications.
>
> I look forward to your comments, and to start drafting a BIP proposal.
>
> Best,
> Salvatore Ingala
>
>
> [*] - Credits go to James O'Beirne for this approach, taken from his
>       OP_VAULT proposal. I cherry-picked the commit containing the
>       Deferred Checks framework.
> [**] - The same NUMS point suggested in BIP-0341 was used.
>
>
> References:
>
> [1] - https://merkle.fun/
> [2] -
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021182.html
> [3] -
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021588.html
> [4] -
> https://github.com/bitcoin-inquisition/bitcoin/compare/24.0...Merkleize:bitcoin:checkcontractverify
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230814/cef35006/attachment.html>

------------------------------

Message: 3
Date: Mon, 14 Aug 2023 14:31:42 +0800
From: Lloyd Fournier <lloyd.fourn@gmail.com>
To: Tom Trevethan <tom@commerceblock.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Blinded 2-party Musig2
Message-ID:
	<CAH5Bsr07j38wyUnteuofGiBCWEyrtvnc=yArr1G=6Rg-ji2Cag@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Tom,

Thanks for the explanation. There's one remaining thing that isn't clear:
do you actually require parallel signing requests under the same key. It
seems to me that the protocol is very sequential in that you are passing a
utxo from one point to another in sequence. If so then the Schnorr blind
sigs problem doesn't apply.

LL

On Thu, 10 Aug 2023 at 20:00, Tom Trevethan <tom@commerceblock.com> wrote:

> HI Lloyd,
>
> Yes, the blind signatures are for bitcoin transactions (these are
> timelocked 'backup txs' if the server disappears). This is not standard
> 'Schnorr blind signature' (like
> https://suredbits.com/schnorr-applications-blind-signatures/) but a
> 2-of-2 MuSig where two keys are required to generate the full signature,
> but one of them (the server) does not learn of either the full key, message
> (tx) or final signature.
>
> The server is explicitly trusted to report the total number of partial
> signatures it has generated for a specific key. If you can verify that ALL
> the signatures generated for a specific key were generated correctly, and
> the total number of them matches the number reported by the server, then
> there can be no other malicious valid signatures in existence. In this
> statechain protocol, the receiver of a coin must check all previous backup
> txs are valid, and that the total number of them matches the server
> reported signature count before accepting it.
>
> On Thu, Aug 10, 2023 at 4:30?AM Lloyd Fournier <lloyd.fourn@gmail.com>
> wrote:
>
>> Hi Tom,
>>
>> These questions might be wrongheaded since I'm not familiar enough with
>> the statechain protocol. Here goes:
>>
>> Why do you need to use schnorr blind signatures for this? Are the blind
>> signatures being used to produce on-chain tx signatures or are they just
>> for credentials for transferring ownership (or are they for both). If they
>> are for on-chain txs then you won't be able to enforce that the signature
>> used was not generated maliciously so it doesn't seem to me like your trick
>> above would help you here. I can fully verify that the state chain
>> signatures were all produced non-maliciously but then there may be another
>> hidden forged signature that can take the on-chain funds that were produced
>> by malicious signing sessions I was never aware of (or how can you be sure
>> this isn't the case).
>>
>> Following on from that point, is it not possible to enforce sequential
>> blind signing in the statechain protocol under each key. With that you
>> don't have the problem of wagner's attack.
>>
>> LL
>>
>> On Wed, 9 Aug 2023 at 23:34, Tom Trevethan via bitcoin-dev <
>> bitcoin-dev@lists.linuxfoundation.org> wrote:
>>
>>> @moonsettler
>>>
>>> When anyone receives a coin (either as payment or as part of a swap)
>>> they need to perform a verification of all previous signatures and
>>> corresponding backup txs. If anything is missing, then the verification
>>> will fail. So anyone 'breaking the chain' by signing something
>>> incorrectly simply cannot then send that coin on.
>>>
>>> The second point is important. All the 'transfer data' (i.e. new and all
>>> previous backup txs, signatures and values) is encrypted with the new owner
>>> public key. But the server cannot know this pubkey as this would enable it
>>> to compute the full coin pubkey and identify it on-chain. Currently, the
>>> server identifies individual coins (shared keys) with a statechain_id
>>> identifier (unrelated to the coin outpoint), which is used by the coin
>>> receiver to retrieve the transfer data via the API. But this means the
>>> receiver must be sent this identifier out-of-band by the sender, and also
>>> that if anyone else learns it they can corrupt the server key
>>> share/signature chain via the API. One solution to this is to have a second
>>> non-identifying key used only for authenticating with the server. This
>>> would mean a 'statchain address' would then be composed of 2 separate
>>> pubkeys 1) for the shared taproot address and 2) for server authentication.
>>>
>>> Thanks,
>>>
>>> Tom
>>>
>>> On Tue, Aug 8, 2023 at 6:44?PM moonsettler <moonsettler@protonmail.com>
>>> wrote:
>>>
>>>> Very nice! Is there an authentication mechanism to avoid 'breaking the
>>>> chain' with an unverifiable new state by a previous owner? Can the current
>>>> owner prove the knowledge of a non-identifying secret he learned as
>>>> recipient to the server that is related to the statechain tip?
>>>>
>>>> BR,
>>>> moonsettler
>>>>
>>>> ------- Original Message -------
>>>> On Monday, August 7th, 2023 at 2:55 AM, Tom Trevethan via bitcoin-dev <
>>>> bitcoin-dev@lists.linuxfoundation.org> wrote:
>>>>
>>>> A follow up to this, I have updated the blinded statechain protocol
>>>> description to include the mitigation to the Wagner attack by requiring the
>>>> server to send R1 values only after commitments made to the server of the
>>>> R2 values used by the user, and that all the previous computed c values are
>>>> verified by each new statecoin owner.
>>>> https://github.com/commerceblock/mercury/blob/master/layer/protocol.md
>>>>
>>>> Essentially, the attack is possible because the server cannot verify
>>>> that the blinded challenge (c) value it has been sent by the user has been
>>>> computed honestly (i.e. c = SHA256(X1 + X2, R1 + R2, m) ), however this CAN
>>>> be verified by each new owner of a statecoin for all the previous
>>>> signatures.
>>>>
>>>> Each time an owner cooperates with the server to generate a signature
>>>> on a backup tx, the server will require that the owner send a commitment to
>>>> their R2 value: e.g. SHA256(R2). The server will store this value before
>>>> responding with it's R1 value. This way, the owner cannot choose the value
>>>> of R2 (and hence c).
>>>>
>>>> When the statecoin is received by a new owner, they will receive ALL
>>>> previous signed backup txs for that coin from the sender, and all the
>>>> corresponding R2 values used for each signature. They will then ask the
>>>> server (for each previous signature), the commitments SHA256(R2) and the
>>>> corresponding server generated R1 value and c value used. The new owner
>>>> will then verify that each backup tx is valid, and that each c value was
>>>> computed c = SHA256(X1 + X2, R1 + R2, m) and each commitment equals
>>>> SHA256(R2). This ensures that a previous owner could not have generated
>>>> more valid signatures than the server has partially signed.
>>>>
>>>> On Thu, Jul 27, 2023 at 2:25?PM Tom Trevethan <tom@commerceblock.com>
>>>> wrote:
>>>>
>>>>>
>>>>> On Thu, Jul 27, 2023 at 9:08?AM Jonas Nick <jonasdnick@gmail.com>
>>>>> wrote:
>>>>>
>>>>>> No, proof of knowledge of the r values used to generate each R does
>>>>>> not prevent
>>>>>> Wagner's attack. I wrote
>>>>>>
>>>>>> > Using Wagner's algorithm, choose R2[0], ..., R2[K-1] such that
>>>>>> > c[0] + ... + c[K-1] = c[K].
>>>>>>
>>>>>> You can think of this as actually choosing scalars r2[0], ...,
>>>>>> r2[K-1] and
>>>>>> define R2[i] = r2[i]*G. The attacker chooses r2[i]. The attack
>>>>>> wouldn't make
>>>>>> sense if he didn't.
>>>>>>
>>>>>
>>>> _______________________________________________
>>> bitcoin-dev mailing list
>>> bitcoin-dev@lists.linuxfoundation.org
>>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>>>
>>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230814/56725037/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 99, Issue 31
*******************************************
