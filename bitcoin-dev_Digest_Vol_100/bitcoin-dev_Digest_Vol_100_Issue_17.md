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

   1. Re: Concrete MATT opcodes (Antoine Riard)
   2. Re: Trustless 2-way-peg without softfork (Dr Maxim Orlovsky)


----------------------------------------------------------------------

Message: 1
Date: Fri, 15 Sep 2023 01:23:31 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Salvatore Ingala <salvatore.ingala@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Concrete MATT opcodes
Message-ID:
	<CALZpt+G_tntsKxui9UOeF2SzEfYHL5avUe=WzhBt9C3ZnuCzpw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Salvatore,

Thanks for the additional insights.

> At this time, my goal is to facilitate maximum experimentation; it's safe
to open Pandora's box in a sandbox, as that's the only way to know if it's
empty.
> Concerns will of course need to be answered when a soft-fork proposal is
made, and restrictions can be added if necessary.

Thinking more, I wonder if the following conjecture could be sketched out
e.g "any utxo-inspecting based miners bribing contracts know a
`counter-bribing` contract that can be offered by a honest Lightning
channel counterparty".

UTXO-inspection can be leveraged to offer "fee bounties" if a Lightning
funding UTXO is unspent after X and there is some ongoing anomaly suspected
(e.g miner-censorship)

> Cross-input introspection seems very likely to have use cases; for
example, I drafted some notes on how it could be used to implement
eltoo-style replacement for lightning
> (or arbitrary state channels) when combined with ANYONECANPAY:
 https://gist.github.com/bigspider/041ebd0842c0dcc74d8af087c1783b63
<https://gist.github.com/bigspider/041ebd0842c0dcc74d8af087c1783b63>.
Although, it would be much ?
> easier with CCV+CHECKSIGFROMSTACK, and in that case cross-input
introspection is not needed.

I looked at the gist and the sequence of transactions is still a bit
unclear to me. From my understanding:
- Alice and Bob both creates virtual UTXOs
- the asymmetric update transactions are valid at the condition of spending
a lower-state number virtual UTXO
- any new update transaction is committing to an on-chain virtual UTXO of a
higher state number

If I'm correct the construction sounds work to me, however I think it
sounds slightly less economically efficient than OG Eltoo (as presented in
2018 paper).

> Similarly, some people raised concerns with recursivity of covenant
opcodes; that also could be artificially limited in CCV if desired, but it
would prevent some use cases.

I think this is still a good design question if we could prevent recursive
covenants that could be hijacked by censorship adversaries. Maybe
recursivity-enablement could be safeguarded on a timelock allowing escape
out of the recursivity after X blocks.

> The flags alter the semantic behavior of the opcode; perhaps you rather
refer to generalizing the index parameter so that it can refer to a group
of inputs/outputs, instead?

Yes, the link about sighash_group-like talk about the use-case of
(non-interactive) aggregation of pre-signed LN commitment transactions with
a single pair of input / output iirc. Witness space efficiency benefit for
LSP and Lightning nodes with hundreds of channels to be closed.

> How would these "tags" interact with CHECKCONTRACTVERIFY? I don't quite
understand the use case.

https://github.com/bitcoin/bips/pull/1381 and let's say you have
`OP_PUSH_ANNEX_TAG(t)` where `t` is the type of tag queried. I wonder if
you could re-build a more powerful CHECKSIGFROMSTACK combined with
CHECKCONTRACTVERIFY.

> More generic introspection might not fit well within the semantics of
CCV, but it could (and probably should) be added with separate opcodes.

I think more witness space efficiency could be obtained by casting the CCV
hash as a merkle tree and traverse it a la g'root
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-July/016249.html

> I personally find OP_CHECKSIGFROMSTACK more natural when thinking about
constructions with CCV; but most likely either would work here.

I agree it's more natural to leverage OP_CHECKSIGFROMSTACK to enable amount
transfer validation, however far less efficient in terms of witness space.

> The DeferredChecks added specifically for CCV has negligible cost, as
it's just O(n_outputs + n_ccv_out) where n_ccv_out is the number of executed
> OP_CHECKCONTRACTVERIFY opcodes (transaction-wide) that check the output
amount.

At first sight, n_outputs + n_ccv_out sounds indeed cheap. Though I think
this is yet to see how it interferes with spending script max opcode limits
and max transaction size.

Best,
Antoine

Le ven. 18 ao?t 2023 ? 16:08, Salvatore Ingala <salvatore.ingala@gmail.com>
a ?crit :

> Hi Antoine,
>
> Thanks for your comments and insights.
>
> On Mon, 14 Aug 2023 at 05:01, Antoine Riard <antoine.riard@gmail.com>
> wrote:
>
>> I think cross-input inspection (not cross-input signature
>> aggregation which is different) is opening a pandora box in terms of
>> "malicious" off-chain contracts than one could design. E.g miners bribing
>> contracts to censor the confirmation of time-sensitive lightning channel
>> transactions, where the bribes are paid on the hashrate distribution of
>> miners during the previous difficulty period, thanks to the coinbase pubkey.
>>
>
> At this time, my goal is to facilitate maximum experimentation; it's safe
> to open Pandora's box in a sandbox, as that's the only way to know if it's
> empty.
> Concerns will of course need to be answered when a soft-fork proposal is
> made, and restrictions can be added if necessary.
>
> Cross-input introspection seems very likely to have use cases; for
> example, I drafted some notes on how it could be used to implement
> eltoo-style replacement for lightning (or arbitrary state channels) when
> combined with ANYONECANPAY:
>  https://gist.github.com/bigspider/041ebd0842c0dcc74d8af087c1783b63
> <https://gist.github.com/bigspider/041ebd0842c0dcc74d8af087c1783b63>.
> Although, it would be much easier with CCV+CHECKSIGFROMSTACK, and in that
> case cross-input introspection is not needed.
>
> Similarly, some people raised concerns with recursivity of covenant
> opcodes; that also could be artificially limited in CCV if desired, but it
> would prevent some use cases.
>
> I have some thoughts on why the fear of covenants might generally be
> unjustified, which I hope to write in long form at some point.
>
> More than a binary flag like a matrix could be introduced to encode subset
>> of introspected inputs /outputs to enable sighash_group-like semantic:
>>
>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-July/019243.html
>>
>
> The flags alter the semantic behavior of the opcode; perhaps you rather
> refer to generalizing the index parameter so that it can refer to a group
> of inputs/outputs, instead?
> I'm not aware of the use cases at this time, feel free to expand further.
>
>
>> Or even beyond a matrix, it could be a set of "tags". There could be a
>> generalized tag for unstructured data, and another one for bitcoin
>> transaction / script data types (e.g scriptpubkey, amount, nsequence,
>> merkle branch) that could be fetched from the taproot annex.
>>
>
> How would these "tags" interact with CHECKCONTRACTVERIFY? I don't quite
> understand the use case.
>
> I think this generic framework is interesting for joinpool / coinpool /
>> payment pool, as you can check that any withdrawal output can be committed
>> as part of the input scriptpubkey, and spend it on
>> blessed-with-one-participant-sig script. There is still a big open question
>> if it's efficient in terms of witness space consumed.
>>
>
> More generic introspection might not fit well within the semantics of CCV,
> but it could (and probably should) be added with separate opcodes.
>
> That said, I still think you would need at least ANYPREVOUT and more
>> malleability for the amount transfer validation as laid out above.
>>
>
> I personally find OP_CHECKSIGFROMSTACK more natural when thinking about
> constructions with CCV; but most likely either would work here.
>
> Looking on the `DeferredCheck` framework commit, one obvious low-level
>> concern is the DoS risk for full-nodes participating in transaction-relay,
>> and that maybe policy rules should be introduced to keep the worst-CPU
>> input in the ranges of current transaction spend allowed to propagate on
>> the network today.
>>
>
> Of course, care needs to be taken in general when designing new deferred
> checks, to avoid any sort of quadratic validation cost.
> The DeferredChecks added specifically for CCV has negligible cost, as it's
> just O(n_outputs + n_ccv_out) where n_ccv_out is the number of executed
> OP_CHECKCONTRACTVERIFY opcodes (transaction-wide) that check the output
> amount.
>
> Best,
> Salvatore
>
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230915/54c1c117/attachment.html>

------------------------------

Message: 2
Date: Fri, 15 Sep 2023 09:31:10 +0000
From: Dr Maxim Orlovsky <orlovsky@lnp-bp.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Trustless 2-way-peg without softfork
Message-ID:
	<fZ1TE57Cb_fD-VmcjtDO8qp9qWEC98m9weorLFkxWjB32H2_C9w5HMNlzHW4TS6SgiKzNN9ScBaiQ6A7SJkJEWQ4CLjzTcwhSysEzqdSCkM=@lnp-bp.org>
	
Content-Type: text/plain; charset=utf-8

Hi,

I got a lot of feedback on my proposal -- and it appears that I have to work on a simpler paper explaining how the proposed generic model ("Prometheus") can be applied to a specific case of two-way peg. I have planned this work for the next several weeks and will post it to this mailing list once ready.

Kind regards,
Maxim


------- Original Message -------
On Monday, September 11th, 2023 at 5:26 PM, G. Andrew Stone via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Any chance of a quick tldr to pique our interest by explaining how exactly this works "and the protocol will reach consensus on whether the state reported by the oracle is correct" in presumably a permissionless, anonymous, decentralized fashion, and what caveats there are?
> 
> Regards,
> Andrew
> 
> On Sun, Sep 10, 2023 at 4:06?PM Dr Maxim Orlovsky via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> > Hi,
> > 
> > Several years ago my team from Pandora Project working on censorship-resistant distributed machine learning proposed Prometheus: a protocol for high-load computing on top of Bitcoin. The protocol operates as a multi-party game setting where an oracle ("worker") is provided with an arbitrary computationally complex task (any Turing-complete computing, machine learning training or inference etc) and the network is able to reach a consensus on whether a result reported by the worker is true. The consensus is reached via optional rounds of verification and arbitrage. The protocol is cryptoeconomically-safe, i.e. has a proven Nash equilibrium. The protocol was later transferred to LNP/BP Standards Association (https://lnp-bp.org) and was kept in a backlog of what can be done in a future as a layer on top of Bitcoin.
> > 
> > I'd like to emphasize that Prometheus works on Bitcoin, requires just several Bitcoin tx per task, and _doesn't require any soft fork_. All economic setting is done with Bitcoin as a means of payment, and using existing Bitcoin script capabilities.
> > 
> > Link to the paper describing the protocol: <https://github.com/Prometheus-WG/prometheus-spec/blob/master/prometheus.pdf>
> > 
> > Only today I have realized that Prometheus protocol can be used to build cryptoeconomically-safe (i.e. trustless) 2-way-peg on the Bitcoin blockchain without any soft-forks: a "worker" in such a case acts as an oracle for some extra-bitcoin system (sidechain, client-side-validated protocol, zk rollup etc) validating it, and the protocol will reach consensus on whether the state reported by the oracle is correct.
> > 
> > In other words, this is an alternative to BIP-300 and other similar soft-forks having the only purpose of doing 2-way pegs. It also enables the two-way trustless transfer of Bitcoins between Bitcoin blockchain, RGB and, in a future, potential new layer 1 called "prime" (to learn more about prime you can check my Baltic Honeybadger talk <https://www.youtube.com/live/V3vvybsc1A4?feature=shared&t=23631>).
> > 
> > 
> > Kind regards,
> > Dr Maxim Orlovsky
> > Twitter: @dr_orlovsky
> > Nostr: npub13mhg7ksq9efna8ullmc5cufa53yuy06k73q4u7v425s8tgpdr5msk5mnym
> > 
> > LNP/BP Standards Association
> > Twitter: @lnp_bp
> > 
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev




------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 17
********************************************
