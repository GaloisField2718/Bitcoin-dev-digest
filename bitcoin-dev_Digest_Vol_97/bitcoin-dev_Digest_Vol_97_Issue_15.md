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

   1. Re: Standardisation of an unstructured taproot annex (Joost Jager)
   2. Re: Standardisation of an unstructured taproot annex
      (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Sun, 11 Jun 2023 21:25:42 +0200
From: Joost Jager <joost.jager@gmail.com>
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAJBJmV-eVZONZ-Qd54BLeN-6LCRNUpHOfLp3Ecg3HXT_AJzRLA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Dave,

On Sun, Jun 11, 2023 at 12:10?AM David A. Harding <dave@dtrt.org> wrote:

> 3. When paying the script in #2, Alice chooses the scriptpath spend from
>     #1 and pushes a serialized partial signature for the ephemeral key
>     from #2 onto the stack, where it's immediately dropped by the
>     interpreter (but is permanently stored on the block chain).  She also
>     attaches a regular signature for the OP_CHECKSIG opcode.
>

Isn't it the case that that op-dropped partial signature for the ephemeral
key isn't committed to and thus can be modified by anyone before it is
mined, effectively deleting the keys to the vault? If not, this would be a
great alternative!

Even better, I think you can achieve nearly the same safety without
> putting any data on the chain.  All you need is a widely used
> decentralized protocol that allows anyone who can prove ownership of a
> UTXO to store some data.
>

I appreciate the suggestion, but I am really looking for a bitcoin-native
solution to leverage bitcoin's robustness and security properties.

By comparison, rolling
> out relay of the annex and witness replacement may take months of review
> and years for >90% deployment among nodes, would allow an attacker to
> lower the feerate of coinjoin-style transactions by up to 4.99%, would
> allow an attacker to waste 8 million bytes of bandwidth per relay node
> for the same cost they'd have to pay to today to waste 400 thousand
> bytes, and might limit the flexibility and efficiency of future
> consensus changes that want to use the annex.


That years-long timeline that you sketch for witness replacement (or any
other policy change I presume?) to become effective is perhaps indicative
of the need to have an alternative way to relay transactions to miners
besides the p2p network?

I agree though that it would be ideal if there is a good solution that
doesn't require any protocol changes or upgrade path.

Joost
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230611/bfbf1f51/attachment-0001.html>

------------------------------

Message: 2
Date: Mon, 12 Jun 2023 04:16:44 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Joost Jager <joost.jager@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CALZpt+EXY6EjrC_mtZLe--ZrnycVdARG8eK6qvqaExA4t+EsQA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Joost,

> However, the primary advantage I see in the annex is that its data isn't
included in the calculation of the txid or a potential parent commit
transaction's txid (for inscriptions). I've explained this at [1]. This
> feature makes the annex a powerful tool for applications that would
ideally use covenants.

I share the observation that the annex data not being committed in the
parent txid is very powerful for use-cases that would use covenants. E.g
there could be an alternative design of CoinPool based on Grafroot, where
the signed surrogate scripts authorized withdrawal abilities [0]. Once
consumed the signed surrogate shouldn't be replayable against the clawback
pool output, and the signature of the surrogate added as "toxic" in a
cryptographic accumulator. Efficient set test membership can be realized to
refuse pool output spend attempts with consumed surrogate scripts.

The annex is a perfect emplacement to locate such an accumulator in the
future as the state of the accumulator cannot be predicted as pool setup
time and is a function of the effective order withdrawal.

Note with Taproot-based design, the replay protection is achieved by the
removal from the taproot tree as edited by any contracting primitive during
the withdrawal phase (e.g TLUV).

> When it comes to the trade-offs associated with various encodings, I
fully acknowledge their existence. The primary motivation behind my
proposal to adopt a simple approach to the Taproot annex is to
> avoid a potentially long standardization process. While I am not entirely
familiar with the decision-making process of Bitcoin Core, my experience
with other projects suggests that simpler changes often
> encounter less resistance and can be implemented more swiftly. Perhaps I
am being overly cautious here, though.

I fully understand the motivation to avoid a lengthy standardization
process, which can be a source of frustration for everyone, including the
standard champions themselves. Indeed, no one lacks the bureaucratic-style
of standardization process for their own sake.

Long standardization processes in Bitcoin consensus are better explained by
the number of technical dimensions to weigh in terms of designs (e.g
full-nodes ressources scalability, fee economic costs, confidentiality,
composability with other changes). And due to the asynchronous nature of
FOSS development, every domain expert is constantly jungling between
different engineering contributions priorities (e.g for myself currently
package relay and mempool for L2s).

All that said, to make the conversation of annex standardization more
practical, and aiming to compose with all technical interest expressed, I
can think about a 2 phase process, at least.

Such standardization process reflects only my opinion, and is based on the
experience of recent mempool fullrbf partial deployment experience, the
Core's trends to have tracking issues for substantial changes,
bitcoin-inquisition and the bitcoin contracting primitives WG experiences.

Phase 1:
- a BIP proposal for the TLV records + code (almost done with #9 in
bitcoin-inquisition and #1421 in the bips repository)
- a BIP proposal to reserve "tag 0" for unstructured data + code (let's say
in bitcoin-inquisition)
- anti-DoS mempool/transaction-relay/replacement code (same)
- bonus point: documenting the new mempool/replacement rules like in Core's
`doc/policy`
- preferential peering logic working code (there is already some code with
Core's #25600)
- opt-in activation of the annex validation rules
- engage Bitcoin devs appreciated by the community as domain experts in the
covered areas to collect more relevant technical feedbacks

Phase 2:
- submit the annex branch with all the features on the Bitcoin Core
repository
- communicate to the Bitcoin technical community at large the existence of
the proposal e.g dev mail list, technical newsletters
- communicate to the second-layers and unstructured data application
maintainers the existence of the proposal
- integrate the feedback from Bitcoin Core, Bitcoin users and second-layers
communities in a "staging code branch"
- if there is a deep technical objection, go back to phase 1 (e.g a
competing serializing proposal for the annex)
- otherwise, split the annex reference branch core in logical chunks for
optimal review process

This is what an efficient-yet-decentralized standardization process of the
annex would look like to me, I don't know. About when we can expect a
deployment of new policy rules for the annex, as Dave made me the
(grounded) reprimand on the list a while back, I don't think mentioning a
date or software version release is appropriate. And this to avoid creating
a sense of commitment on all the contributors involved in the projects
above mentioned.

I'm still interested in championing the "base" TLV serialization annex code
and BIP. To move faster, I think it would be better to have another
champion on the "tag 0" and BIP, especially as the unstructured data
use-cases are coming with their own specifics.

> Regarding the potential payload extension attack, I believe that the
changes proposed in the [3] to allow tx replacement by smaller witnesses
would provide a viable solution?

To be honest, in terms of DoS, I wouldn't give a strong opinion before
better formalization or consensus of the use-case requirements. From
experience of Core's mempools PRs, you have few subcomponents that can be
involved (replacement, block template, broadcast backend of L2s, etc).

> That years-long timeline that you sketch for witness replacement (or any
other policy change I presume?) to become effective is perhaps indicative
of the need to have an alternative way to relay
> transactions to miners besides the p2p network?

Assuming an alternative p2p network, I don't think we can avoid some
standardization of fundamental data structures between those p2p network.
Most of L2s are pre-signing transactions/packages and might not be able to
alter the validity of such set of transactions in a unilateral fashion
without re-introducing some ?bad? malleability. And a L2 node has an
interest to use multiple p2p networks to mitigate against things like
time-dilation attacks.

Best,
Antoine

[0]
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-February/015700.html

Le dim. 11 juin 2023 ? 20:26, Joost Jager <joost.jager@gmail.com> a ?crit :

> Hi Dave,
>
> On Sun, Jun 11, 2023 at 12:10?AM David A. Harding <dave@dtrt.org> wrote:
>
>> 3. When paying the script in #2, Alice chooses the scriptpath spend from
>>     #1 and pushes a serialized partial signature for the ephemeral key
>>     from #2 onto the stack, where it's immediately dropped by the
>>     interpreter (but is permanently stored on the block chain).  She also
>>     attaches a regular signature for the OP_CHECKSIG opcode.
>>
>
> Isn't it the case that that op-dropped partial signature for the ephemeral
> key isn't committed to and thus can be modified by anyone before it is
> mined, effectively deleting the keys to the vault? If not, this would be a
> great alternative!
>
> Even better, I think you can achieve nearly the same safety without
>> putting any data on the chain.  All you need is a widely used
>> decentralized protocol that allows anyone who can prove ownership of a
>> UTXO to store some data.
>>
>
> I appreciate the suggestion, but I am really looking for a bitcoin-native
> solution to leverage bitcoin's robustness and security properties.
>
> By comparison, rolling
>> out relay of the annex and witness replacement may take months of review
>> and years for >90% deployment among nodes, would allow an attacker to
>> lower the feerate of coinjoin-style transactions by up to 4.99%, would
>> allow an attacker to waste 8 million bytes of bandwidth per relay node
>> for the same cost they'd have to pay to today to waste 400 thousand
>> bytes, and might limit the flexibility and efficiency of future
>> consensus changes that want to use the annex.
>
>
> That years-long timeline that you sketch for witness replacement (or any
> other policy change I presume?) to become effective is perhaps indicative
> of the need to have an alternative way to relay transactions to miners
> besides the p2p network?
>
> I agree though that it would be ideal if there is a good solution that
> doesn't require any protocol changes or upgrade path.
>
> Joost
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230612/4d095d65/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 15
*******************************************
