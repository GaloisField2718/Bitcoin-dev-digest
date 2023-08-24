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

   1. Re: Vaults in the MATT framework (Johan Tor?s Halseth)
   2. Standardisation of an unstructured taproot annex (Joost Jager)


----------------------------------------------------------------------

Message: 1
Date: Fri, 2 Jun 2023 15:25:39 +0200
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Salvatore Ingala <salvatore.ingala@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Vaults in the MATT framework
Message-ID:
	<CAD3i26CLwLsgUcyDFBerACg_MMGG0Zz4n5dFG75AUS02rxnucg@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi,

It was briefly mentioned in the original post, but wanted to show how
simple it is to use COCV as an alternative to CTV, removing that
dependency.

> In particular, it also inherits the choice of using OP_CTV as a primitive,
> building on top of the bitcoin-inquisition's current branch that has already
> merged OP_CTV. Reasonable vaults would be possible without CTV, but they
> would be less efficient, particularly in the case of sending to many addresses
> in a single unvaulting flow.

Instead of specifying a CTV hash as embedded data, one could embed the
(commitment to the) outputs of the withdrawal transaction. Then
instead of a single OP_CTV, one OP_COCV per output to match against
the embedded data. Less efficient in case of many outputs as you
mention, but simple enough to be interesting.

Here's an example how to use MATT as a CTV replacement:
https://github.com/halseth/tapsim/blob/b07f29804cf32dce0168ab5bb40558cbb18f2e76/examples/matt/ctv2/README.md

Cheers,
Johan



On Tue, May 2, 2023 at 10:22?AM Salvatore Ingala via bitcoin-dev
<bitcoin-dev@lists.linuxfoundation.org> wrote:
>
> Hi Michael,
>
> I can't make any claim of expertise on the field (especially on the
> other proposals that you mentioned), so this post necessarily includes
> my opinions ? and possibly my biases.
>
> The core functionality of MATT is quite simple, and could be adapted
> to any version of the scripting system: basically, COCV allows to
> "embed" some data in the next output, and decide its script; CICV
> allows "reading" this data.
> The design I proposed on taproot is surely not the only possible way,
> but it's the most simple/elegant I could come up with. Moreover, it
> doesn't seem very useful to spend time trying to get it to work on
> pre-taproot Script, due to the obvious advantages of those ideas when
> deployed on taproot (like having taptrees, and all the nice properties
> of Schnorr signatures).
>
> CICV/COCV can certainly be considered an additional form of
> introspection: you're checking that the script of an input/output
> equals a certain value, which is not possible in today's Script.
> I think that's generally true for all covenant proposals.
>
> Unlike some other proposals, MATT is not yet fully formalized, so I
> generally call "MATT" the combination of CICV+COCV, plus some other
> small set of opcodes that is yet to be defined exactly. I would say it
> fits in the same family as APO/OP_CTV/OP_VAULT, per your bucketization.
>
> The previous posts about MATT, fraud proofs, etc. are an exploration of
> the deeper things that are enabled by the MATT opcodes. The claim is
> that a set of changes that is (arguably) quite small and easy to analyze
> is enough to express general smart contracts ? thanks to fraud proofs.
> However, fraud proofs themselves are a quite advanced application of
> the new opcodes, and are not needed for most/all of the things that
> people are trying to build today with the other covenant proposals.
>
>
> Since you mention Simplicity: my current understanding is that its
> endeavour of replacing Script with a better language is orthogonal to
> the discussion about what features (e.g.: introspection, covenants)
> should be in the language.
>
> All the covenant proposals listed above are technically a lot smaller
> and easier to audit than both the SegWit and the Taproot soft forks,
> both in terms of code and conceptual complexity.
>
> Therefore, if we _do_ want the features that they enable, the required
> engineering for a soft-fork is relatively straightforward, and there is
> not much of a reason to wait for Simplicity. It will be trivial to "port" any
> constructions we might create today with covenants to Simplicity scripts.
>
> If we _do not_ want those features, then the decision would rather be
> guided by other considerations, like potential risks to bitcoin caused
> by the effect of those features on miners' incentives. These
> concerns are not answered by Simplicity, as far as I understand:
> you would then want to implement Simplicity _without_ those features.
>
> Best,
> Salvatore
>
> On Mon, 1 May 2023 at 16:18, Michael Folkson <michaelfolkson@protonmail.com> wrote:
>>
>> Hi Salvatore
>>
>> Can you clarify for me which bucket this proposal sits? We have APO, CTV, OP_VAULT etc that are proposals to add additional functionality to SegWit version 1, Tapleaf version 0 scripts. We have Simplicity that would need a new Tapleaf version (e.g. Tapleaf version 1). And then there are CISA like proposals that would need a new SegWit version (e.g. SegWit version 2). It looks to me like your proposal is in the first bucket (same as APO, CTV etc) as it is just introducing new opcode functionality to existing script with no deeper introspection needed but previous and current discussion of fraud proofs, MATT frameworks etc made me initially think it was going to require more than that.
>>
>> Thanks
>> Michael
>>
>> --
>> Michael Folkson
>> Email: michaelfolkson at protonmail.com
>> GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
>>
>> Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
>>
>> ------- Original Message -------
>> On Monday, April 24th, 2023 at 20:37, Salvatore Ingala via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>>
>> Hello list,
>>
>> TL;DR: the core opcodes of MATT can build vaults with a very similar design
>> to OP_VAULT. Code example here:
>>
>> https://github.com/bitcoin-inquisition/bitcoin/compare/24.0...bigspider:bitcoin-inquisition:matt-vault
>>
>>
>> In my previous emails about the MATT proposal for smart contracts in
>> bitcoin [1], I mostly focused on proving its generality; that is, it
>> allows arbitrary smart contracts thanks to fraud proofs.
>>
>> While I still find this "completeness" result compelling, I spent more time
>> thinking about the framework itself; the construction is not very interesting
>> if it turns simple things into complicated ones. Luckily, this is not the case.
>> In particular, in this email we will not merkleize anything (other than taptrees).
>>
>> This post describes some progress into formalizing the semantics of the core
>> opcodes, and demonstrates how they could be used to create vaults that seem
>> comparable to the ones built with OP_VAULT [2], despite using general purpose
>> opcodes.
>>
>> An implementation and some minimal tests matching the content of this
>> e-mail can be found in the link above, using the bitcoin-inquisition as the
>> base branch.
>>
>> Note that the linked code is not well tested and is only intended for
>> exploratory and demonstrative purposes; therefore, bugs are likely at this
>> stage.
>>
>>
>> ##########################
>> # PART 1: MATT's core
>> ##########################
>>
>> In this section, I will discuss plausible semantics for the core opcodes for MATT.
>>
>> The two core opcodes are defined below as OP_CHECKINPUTCONTRACTVERIFY and
>> OP_CHECKOUTPUTCONTRACTVERIFY.
>>
>> (the initial posts named them OP_CHECK{INPUT,OUTPUT}COVENANTVERIFY)
>>
>> They enhance Script with the following capabilities:
>> - decide the taptree of the output
>> - embed some (dynamically computed) data in the output
>> - access the embedded data in the current UTXO (if any)
>>
>> The opcodes below are incomplete, as they only control the output's Script and
>> not the amounts; more on that below.
>>
>> Other than that, the semantics should be quite close to the "right" one for
>> the MATT framework.
>>
>>
>> ### The opcodes
>>
>> case OP_CHECKINPUTCONTRACTVERIFY:
>> {
>> // OP_CHECKINPUTCONTRACTVERIFY is only available in Tapscript
>> if (sigversion == SigVersion::BASE || sigversion == SigVersion::WITNESS_V0) return set_error(serror, SCRIPT_ERR_BAD_OPCODE);
>> // (x d -- )
>> if (stack.size() < 2)
>> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>> valtype& x = stacktop(-2);
>> valtype& d = stacktop(-1);
>> if (x.size() != 32 || d.size() != 32)
>> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>> const XOnlyPubKey nakedXOnlyKey{Span<const unsigned char>{x.data(), x.data() + 32}};
>> const uint256 data(d);
>> if (!execdata.m_internal_key.has_value())
>> return set_error(serror, SCRIPT_ERR_UNKNOWN_ERROR); // TODO
>> // Verify that tweak(lift_x(x), d) equals the internal pubkey
>> if (!execdata.m_internal_key.value().CheckDoubleTweak(nakedXOnlyKey, &data, nullptr))
>> return set_error(serror, SCRIPT_ERR_WRONGCONTRACTDATA);
>> popstack(stack);
>> popstack(stack);
>> }
>> break;
>> case OP_CHECKOUTPUTCONTRACTVERIFY:
>> {
>> // OP_CHECKOUTPUTCONTRACTVERIFY is only available in Tapscript
>> if (sigversion == SigVersion::BASE || sigversion == SigVersion::WITNESS_V0) return set_error(serror, SCRIPT_ERR_BAD_OPCODE);
>> // (out_i x taptree d -- )
>> if (stack.size() < 4)
>> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>> int out_i = CScriptNum(stacktop(-4), fRequireMinimal).getint();
>> valtype& x = stacktop(-3);
>> valtype& taptree = stacktop(-2);
>> valtype& d = stacktop(-1);
>> auto outps = checker.GetTxvOut();
>> // Return error if the evaluation context is unavailable
>> if (!outps)
>> return set_error(serror, SCRIPT_ERR_UNKNOWN_ERROR); // TODO
>> if (x.size() != 32 || taptree.size() != 32 || (d.size() != 0 && d.size() != 32))
>> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>> if (out_i < 0 || out_i >= (int)outps->size())
>> return set_error(serror, SCRIPT_ERR_INVALID_STACK_OPERATION);
>> const XOnlyPubKey nakedXOnlyKey{Span<const unsigned char>{x.data(), x.data() + 32}};
>> const uint256 data(d);
>> const uint256 *data_ptr = (d.size() == 0 ? nullptr : &data);
>> const uint256 merkle_tree(taptree);
>> CScript scriptPubKey = outps->at(out_i).scriptPubKey;
>> if (scriptPubKey.size() != 1 + 1 + 32 || scriptPubKey[0] != OP_1 || scriptPubKey[1] != 32)
>> return set_error(serror, SCRIPT_ERR_WRONGCONTRACTDATA);
>> const XOnlyPubKey outputXOnlyKey{Span<const unsigned char>{scriptPubKey.data() + 2, scriptPubKey.data() + 34}};
>> // Verify that taptweak(tweak(lift_x(x), d), taptree) equals the internal pubkey
>> if (!outputXOnlyKey.CheckDoubleTweak(nakedXOnlyKey, data_ptr, &merkle_tree))
>> return set_error(serror, SCRIPT_ERR_WRONGCONTRACTDATA);
>> popstack(stack);
>> popstack(stack);
>> popstack(stack);
>> popstack(stack);
>> }
>> break;
>>
>> ### Commentary
>>
>> CheckDoubleTweak function (implemented in the branch) gets an x-only pubkey,
>> optionally some data, and optionally taptree's merkle root.
>> It verifies that the x-only pubkey being tested equals the given naked pubkey,
>> optionally tweaked with the embedded data, optionally tweaked with the tagged
>> hash of the merkle tree per BIP-0341 [3].
>> Making both the tweaks optional allows to simplify the code, and also to obtain
>> more compact scripts in some spending paths.
>>
>> In words:
>>
>> - OP_CHECKINPUTCONTRACTVERIFY: verify that the current input's internal key
>> contains some embedded data (which would typically be passed through the
>> witness stack)
>> - OP_CHECKOUTPUTCONTRACTVERIFY: verify that a given output is a certain P2TR
>> output script containing the desired embedded data.
>>
>> TBD if the tweaking used for the embedded data tweak should use a tagged hash;
>> omitted for simplicity in this demo implementation.
>>
>> ### Amount preservation
>>
>> In the code above and in the linked demo implementation, the opcodes only
>> operate on the scriptPubkey; a complete implementation would want to make sure
>> that amounts are correctly preserved.
>>
>> The most direct and general way to address this would be to allow direct
>> introspection on the output amounts. This has the complication that output
>> amounts require 64-bits arithmetics, as discussed in the context of other
>> proposals, for example: [4].
>>
>> One more limited approach that works well for many interesting contracts
>> is that of the deferred checks, implemented in OP_VAULT [2].
>> The idea is that all the amounts of the inputs that commit to the same output
>> script with OP_CHECKOUTPUTCONTRACTVERIFY are added together, and the script
>> interpreter requires that the amount of that output is not smaller than the
>> total amount of those inputs. This check is therefore transaction-wide rather
>> than being tested during the input's script evaluation.
>>
>> This behaviour is adequate for vaults and likely suitable for many other
>> applications; however, it's not the most general approach. I didn't try to
>> implement it yet, and defer the decision on the best approach to a later time.
>>
>> ### Extensions
>>
>> The opcodes above are not enough for the full generality of MATT: one would
>> need to add an opcode like OP_SHA256CAT to allow the data embedding to commit
>> to multiple pieces of data.
>> This is not used in today's post, therefore I left it out of these code examples.
>>
>> It would be easy to extend OP_CHECKOUTPUTCONTRACTVERIFY to also apply for
>> an arbitrary input (typically, different from the currently executed one); there
>> are likely use cases for that, allowing to define contracts with more complex
>> cross-input semantics, but I preferred to keep things simple.
>>
>> Of course, one could also entirely replace CICV/COCV with generic full
>> introspection on inputs/output's program, plus opcodes for elliptic curve math
>> and tagged hashes.
>>
>>
>> ##########################
>> # PART 2: Vaults with MATT
>> ##########################
>>
>> In the rest of this post, I will document the first attempt at creating a vault
>> using the opcodes described.
>>
>> While not an attempt at cloning exactly the functionality of OP_VAULT [2],
>> it borrows heavily from the excellent work that was done there.
>>
>> In particular, it also inherits the choice of using OP_CTV as a primitive,
>> building on top of the bitcoin-inquisition's current branch that has already
>> merged OP_CTV. Reasonable vaults would be possible without CTV, but they
>> would be less efficient, particularly in the case of sending to many addresses
>> in a single unvaulting flow.
>>
>> ### Distilling OP_VAULT
>>
>> Abstracting from the implementation details, I mentally model a vault as a
>> simple state machine with 2 states: [V] and [U]:
>>
>> [V]: the initial vault UTXO(s);
>> [U]: the utxo produced by the "trigger transaction" during unvaulting.
>>
>> On the typical path: one or more [V] UTXOs are sent to the [U] state, and after
>> a timelock set on [U] expires, [U] is spent to one or several destinations.
>> Crucially, the destination outputs and amounts are already decided when [V] is
>> spent into [U].
>>
>> At any time before the funds are spent from [U], they can always be spent by
>> sending them to some specified recovery path.
>>
>> There are two key elements that are part of OP_VAULT's semantics, and could be
>> generalized:
>>
>> ? Forcing the script/amount of the next stepon
>> ? Storing some data for future Script's access (in the vault's case, a hash
>> that commits to the final withdrawal transaction).
>>
>> CICV/COCV generalize both to arbitrary scripts (taptrees) and state machines,
>> and to dynamical and witness-dependent data embedded in the pubkey of a P2TR
>> output.
>>
>> ### Vault parameters
>>
>> A contract that represents a vault has the following parameters (hardcoded in
>> the script when the vault is created):
>>
>> - alternate_pk: a key that can be used any time.
>> - spend_delay: the relative timelock before the withdrawal can be finalized;
>> - recover_pk: a pubkey for a P2TR output where funds can be sent at any time.
>>
>> The alternate_pk is a pubkey that can optionally be used as the key-path
>> spending condition for both states [V] and [U]. If such a spending condition is not
>> desired, it can be replaced with a NUMS point, making the key-path unspendable.
>>
>> The spend_delay is the number of blocks that must be mined before the final
>> withdrawal transaction
>>
>> In this example we also use an unvault_pk needed to authorize the unvaulting
>> process (that is, spend [V] into [U]); this could be replaced with any miniscript
>> or other conditions expressible in Script.
>>
>> ### P2TR structure for [V] (vault)
>>
>> internal key: alternate_pk
>>
>> Script 1: "trigger"
>> # witness: <out_i> <ctv-hash>
>> {
>> <alternate_pk>,
>> <merkle root of U's taptree>,
>> 2, OP_ROLL,
>> OP_CHECKOUTPUTCONTRACTVERIFY,
>>
>> <unvault_pk>
>> OP_CHECKSIG
>> }
>>
>> Script 2: "recover"
>> # witness: <out_i>
>> {
>> recover_pk,
>> OP_0, # no data tweak
>> OP_0, # no taptweak
>> OP_CHECKOUTPUTCONTRACTVERIFY,
>> OP_TRUE
>> }
>>
>> The "trigger" script requires in the witness an output index and the ctv-hash
>> that describes the withdrawal transaction.
>> COCV forces the output to contain the ctv-hash as embedded data.
>> That's followed by the unvaulting condition ? in this example, a simple
>> signature check.
>>
>> The "recover" script doesn't require any signature, and it simply forces
>> the output specified in the witness to be a P2TR output with recover_pk as its
>> pubkey.
>>
>> (Omitting the "recover" script in [V] would reduce the size of the witness by
>> 32 bytes in the expected case, and might be preferred for some users)
>>
>> ### P2TR structure for [U] (unvaulting state)
>>
>> internal key: alternate_pk (tweaked with ctv_hash)
>>
>> Script 1: "withdrawal"
>> # witness: <ctv_hash>
>> {
>> OP_DUP,
>>
>> # check that the top of the stack is the
>> # embedded data in the current input
>> <alternate_pk>, OP_SWAP,
>> OP_CHECKINPUTCONTRACTVERIFY,
>>
>> # Check timelock
>> <spend_delay>,
>> OP_CHECKSEQUENCEVERIFY,
>> OP_DROP,
>>
>> # Check that the transaction output is as expected
>> OP_CHECKTEMPLATEVERIFY
>> }
>>
>> Script 2: "recover"
>> # witness: <out_i>
>> {
>> <recover_pk>,
>> OP_0,
>> OP_0,
>> OP_CHECKOUTPUTCONTRACTVERIFY,
>> OP_TRUE
>> }
>>
>> The "withdrawal" finalizes the transaction, by checking that the timelock expired and
>> the outputs satisfy the CTV hash that was committed to in the previous transaction.
>>
>> The "recover" script is identical as before.
>>
>>
>> ### Differences with OP_VAULT vaults
>>
>> Here I refer to the latest version of OP_VAULT at the time of writing. [5]
>> It is not a thorough analysis.
>>
>> Unlike the implementation based on OP_VAULT, the [V] utxos don't have an option
>> to add an additional output that is sent back to the same exact vault.
>> Supporting this use case seems to require a more general way of handling the
>> distribution of amounts than what I discussed in the section above: that would
>> in fact need to be generalized to the case of multiple
>> OP_CHECKOUTPUTCONTRACTVERIFY opcodes executed for the same input.
>>
>> By separating the ctv-hash (which is considered "data") from the scripts in the
>> taptree, one entirely avoids the need to dynamically create taptrees and
>> replace leaves in the covenant-encumbered UTXOs; in fact, the taptrees of [V]
>> and [U] are already set in stone when [V] utxos are created, and only the
>> "data" portion of [U]'s scriptPubKey is dynamically computed. In my opinion,
>> this makes it substantially easier to program "state machines" that control the
>> behavior of coins, of which vaults are a special case.
>>
>> I hope you'll find this interesting, and look forward to your comments.
>>
>> Salvatore Ingala
>>
>>
>> [1] - https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021223.html
>> [2] - https://github.com/bitcoin/bips/pull/1421
>> [3] - https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
>> [4] - https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-September/019420.html
>> [5] - https://github.com/bitcoin/bips/blob/7112f308b356cdf0c51d917dbdc1b98e30621f80/bip-0345.mediawiki
>>
>>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 2
Date: Fri, 2 Jun 2023 17:00:37 +0200
From: Joost Jager <joost.jager@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV-L4FusaMNV=_7L39QFDKnPKK_Z1QE6YU-wp2ZLjc=RrQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi,

As it stands, the taproot annex is consensus valid but non-standard. The
conversations around standardization seem to be leaning towards the
adoption of a flexible Type-Length-Value (TLV) format [1]. There's no doubt
that this approach has considerable potential. However, settling on an
exact format may require a significant amount of time.

In the interim, the benefits of making the annex available in a
non-structured form are both evident and immediate. By allowing developers
to utilize the taproot annex without delay, we can take advantage of its
features today, without the need to wait for the finalization of a more
lengthy standardization process.

With this in view, I am proposing that we define any annex that begins with
'0' as free-form, without any additional constraints. This strategy offers
several distinct benefits:

Immediate utilization: This opens the door for developers to make use of
the taproot annex for a variety of applications straight away, thus
eliminating the need to wait for the implementation of TLV or any other
structured format.

Future flexibility: Assigning '0'-beginning annexes as free-form keeps our
options open for future developments and structure improvements. As we
forge ahead in determining the best way to standardize the annex, this
strategy ensures we do not limit ourselves by setting its structure in
stone prematurely.

Chainspace efficiency: Non-structured data may require fewer bytes compared
to a probable TLV format, which would necessitate the encoding of length
even when there's only a single field.

In conclusion, adopting this approach will immediately broaden the
utilization scope of the taproot annex while preserving the possibility of
transitioning to a more structured format in the future. I believe this is
a pragmatic and efficient route, one that can yield substantial benefits in
both the short and long term.

Joost

[1] https://github.com/bitcoin/bips/pull/1381
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230602/4411b85b/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 2
******************************************
