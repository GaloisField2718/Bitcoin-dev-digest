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

   1. Re: Standardisation of an unstructured taproot annex
      (Greg Sanders)
   2. Re: postr: p2n payjoin using nostr (alicexbt)
   3. Re: Standardisation of an unstructured taproot annex
      (David A. Harding)


----------------------------------------------------------------------

Message: 1
Date: Mon, 12 Jun 2023 09:03:47 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Joost Jager <joost.jager@gmail.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CAB3F3Ds4aZ7fqqNUBGW3vzvUhsJ7ABvbGaAaEhWimyLosxwVmg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

> Regarding the potential payload extension attack, I believe that the
changes proposed in the [3] to allow tx replacement by smaller witness
would provide a viable solution?

The only plausible case I could see moving forward is replacing the
transaction to a form that has *no* annex or scriptpath spends, ala
https://github.com/bitcoin/bitcoin/pull/24007#issuecomment-1308104119 .
It's much easier to think about one-off replacements from an anti-DoS
perspective.

We would have to think a lot harder if that actually solves the problem and
maintains the prospective use-cases before diving into analysis, regardless.

Cheers,
Greg


On Sat, Jun 10, 2023 at 5:02?AM Joost Jager via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi Antoine,
>
> On Sat, Jun 10, 2023 at 2:23?AM Antoine Riard <antoine.riard@gmail.com>
> wrote:
>
>> From a taproot annex design perspective, I think this could be very
>> valuable if you have a list of unstructured data use-cases you're thinking
>> about ?
>>
>
> The annex's list of unstructured data use-cases includes existing data
> storage uses that utilize OP_RETURN or inscriptions. Consider ordinals,
> timestamps, and any other data already stored on the chain. These
> applications would immediately benefit from the annex's improved space
> efficiency.
>
> However, the primary advantage I see in the annex is that its data isn't
> included in the calculation of the txid or a potential parent commit
> transaction's txid (for inscriptions). I've explained this at [1]. This
> feature makes the annex a powerful tool for applications that would ideally
> use covenants.
>
> The most critical application in this category, for me, involves
> time-locked vaults. Given the positive reception to proposals such as
> OP_VAULT [2], I don't think I'm alone in this belief. OP_VAULT is probably
> a bit further out, but pre-signed transactions signed using an ephemeral
> key can fill the gap and improve the safeguarding of Bitcoin in the short
> term.
>
> Backing up the ephemeral signatures of the pre-signed transactions on the
> blockchain itself is an excellent way to ensure that the vault can always
> be 'opened'. However, without the annex, this is not as safe as it could
> be. Due to the described circular reference problem, the vault creation and
> signature backup can't be executed in one atomic operation. For example,
> you can store the backup in a child commit/reveal transaction set, but the
> vault itself can be confirmed independently and the backup may never
> confirm. If you create a vault and lose the ephemeral signatures, the funds
> will be lost.
>
> This use case for the annex has been labeled 'speculative' elsewhere. To
> me, every use case appears speculative at this point because the annex
> isn't available. However, if you believe that time-locked vaults are
> important for Bitcoin and also acknowledge that soft forks, such as the one
> required for OP_VAULT, aren't easy to implement, I'd argue that the
> intermediate solution described above is very relevant.
>
>
>> As raised on the BIP proposal, those unstructured data use-cases could
>> use annex tags with the benefit to combine multiple "types" of unstructured
>> data in a single annex payload. As you're raising smaller bits of
>> unstructured data might not afford the overhead though my answer with this
>> observation would be to move this traffic towards some L2 systems ? In my
>> mind, the default of adding a version byte for the usage of unstructured
>> data comes with the downside of having future consensus enabled use-cases
>> encumbering by the extended witness economic cost.
>>
>
> When it comes to the trade-offs associated with various encodings, I fully
> acknowledge their existence. The primary motivation behind my proposal to
> adopt a simple approach to the Taproot annex is to avoid a potentially long
> standardization process. While I am not entirely familiar with the
> decision-making process of Bitcoin Core, my experience with other projects
> suggests that simpler changes often encounter less resistance and can be
> implemented more swiftly. Perhaps I am being overly cautious here, though.
>
>
>> About the annex payload extension attack described by Greg. If my
>> understanding of this transaction-relay jamming griefing issue is correct,
>> we can have an annex tag in the future where the signer is committing to
>> the total weight of the transaction, or even the max per-input annex size ?
>> This should prevent a coinjoin or aggregated commitment transaction
>> counterparty to inflate its annex space to downgrade the overall
>> transaction feerate, I guess. And I think this could benefit unstructured
>> data use-cases too.
>>
>
> Regarding the potential payload extension attack, I believe that the
> changes proposed in the [3] to allow tx replacement by smaller witness
> would provide a viable solution?
>
> Joost
>
> [1]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-June/021737.html
> [2] https://github.com/bitcoin/bips/pull/1421
> [3] https://github.com/bitcoin/bitcoin/pull/24007
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230612/2d695cd7/attachment-0001.html>

------------------------------

Message: 2
Date: Mon, 12 Jun 2023 19:28:47 +0000
From: alicexbt <alicexbt@protonmail.com>
To: symphonicbtc <symphonicbtc@proton.me>
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] postr: p2n payjoin using nostr
Message-ID:
	<EQsyuwTpcGBPNNTpCdDzZr4mWC99WoNQLxt5_vSpBCVUZ-dfbGJOrAUh4aLZ7LBkDjpRtEsPTi11xCn4NfY4z18ljbrbsx6GIUgJaK_APxI=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Symphonic,

> I'm a bit confused as to what exactly this is a proof of concept for.

This is a proof of concept for using nostr npub and relays for payjoin.

> Your use of SIGHASH_NONE does in fact make it possible for the reciever to do whatever they want with your funds (which I see you acknowledge in your brief description, but still, not very practical).

SIGHASH_NONE can be used when there is no change in the transaction and sender wants to spend whole UTXO for the payment. Recipient is free to decide the outputs and extra input for the transaction.

> However, it is also possible for anyone who sees the final broadcasted transaction to extract the sender's input and use it for any purpose they wish; game theoretically miners would just steal your funds, but it's possible for any user to RBF and send those funds wherever they like.

- Based on my understanding of SIGHASH flags and a [blog post][0] by Raghav Sood, use of SIGHASH_ALL by recipient will secure all outputs. However I have realized it is still vulnerable in a [tweet thread][1] as you mentioned. While writing this email, poll was still 50-50 so I guess its a learning thing. We have less docs about SIGHASH flags, maybe an e-book with all experiments would improve this.
- Since this was just a PoC to use nostr, use of specific SIGHASH flags can be ignored and developers can use other flags or default. I will improve/change it as well. I wanted to use SIGHASH_NONE to improve privacy and less UX issues.
- There are no incentives for sender or recipient to use RBF and double spend in a payjoin transaction.

[0]: https://raghavsood.com/blog/2018/06/10/bitcoin-signature-types-sighash
[1]: https://twitter.com/1440000bytes/status/1668261886884708352

/dev/fd0
flopyy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Sunday, June 11th, 2023 at 8:02 AM, symphonicbtc <symphonicbtc@proton.me> wrote:


> Hey alicexbt,
> I'm a bit confused as to what exactly this is a proof of concept for. Your use of SIGHASH_NONE does in fact make it possible for the reciever to do whatever they want with your funds (which I see you acknowledge in your brief description, but still, not very practical). However, it is also possible for anyone who sees the final broadcasted transaction to extract the sender's input and use it for any purpose they wish; game theoretically miners would just steal your funds, but it's possible for any user to RBF and send those funds wherever they like.
> 
> As is the case with any work-in-progress software, but especially in this instance, I urge you to disable the ability to use mainnet coins directly in your code. This is highly irresponsible to post in this state.
> 
> Moreover, a bit redundantly considering the glaring and severe security issues, this is not a proper implemenation of a payjoin, even in a theoretical scenario, as it is trivial to discern which inputs belong to the sender and reciever respectively in the final transaction.
> 
> Symphonic
> 
> 
> Sent with Proton Mail secure email.


------------------------------

Message: 3
Date: Mon, 12 Jun 2023 22:51:39 -1000
From: "David A. Harding" <dave@dtrt.org>
To: Joost Jager <joost.jager@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID: <211fef60bb46fae7f69e8e5882ff27cb@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

On 2023-06-11 09:25, Joost Jager wrote:
> Isn't it the case that that op-dropped partial signature for the
> ephemeral key isn't committed to and thus can be modified by anyone
> before it is mined

That's correct; I hadn't thought of that, sorry.

> I am really looking for a bitcoin-native solution to leverage
> bitcoin's robustness and security properties.

I understand.  I would briefly point out that there are other advantages
to not storing a signature for an ephemeral key in the annex.  For
example, if you want to generate multiple different potential spending
transactions, you need to store one signature for each potential
transaction.  The more data you store in the annex, the less scalable
the vault protocol becomes; by comparison, it's possible to cheaply
store a very large amount of data offchain with high robustness.

Also, depending on construction of the vault, a possible advantage of a
presigned vault (without using the annex) over a solution like OP_VAULT
is that all actions might be able to use keypath spends.  That would be
highly efficient, increasing the usability of vaults.  It would also be
more private, which may be important to certain classes of vault users.
Even if OP_VAULT was added to Bitcoin, it would be interesting to have
an alternative vault protocol that offered different tradeoffs.

> That years-long timeline that you sketch for witness replacement (or
> any other policy change I presume?) to become effective is perhaps
> indicative of the need to have an alternative way to relay
> transactions to miners besides the p2p network?

The speed depends on the policy change.  In this case, I think there's a
reasonable argument to be made that a mitigation for the problems of
annex relay should be widely deployed before we enable annex relay.

Bitcoin Core's policy is designed to both prevent the abuse of relay
node resources and also serve the transaction selection needs of miners.
Any alternative relay system will need to solve the same general
problems: how to prevent abuse of the relayers and help miners choose
the best transactions.  Ideas for alternative relay like those
previously proposed on this list[1] avoid certain problems but also
(AFAICT) create new problems.

To be specific towards this proposal, if an alternative relay network
naively implemented annex relay, any miners who used that network could
receive a coinjoin-style transaction with a large annex that
significantly reduced the transaction's feerate.  By comparison, any
miners who continued to only receive transactions from the P2P network
of Bitcoin Core (or similar) nodes would have received the transaction
without an annex at its original (higher) feerate, allowing them to to
receive greater revenue if they mined it.  If, instead, the alternative
relay network implemented the witness replacement proposal you've linked
to, those miners could still receive up to 4.99% less revenue than
Bitcoin Core-based miners and the operators of the alternative relay
network might have had to pay extra costs for the replacement relays.
You can tweak the proposal to tweak those ratios, but I'm not sure
there's a case where an alternative relay network comes up as a clear
winner over the existing network for general purpose transactions.
Instead, like many things, it's a matter of tradeoffs.

> I agree though that it would be ideal if there is a good solution that
> doesn't require any protocol changes or upgrade path.

Apologies for the salt, but there is a good solution: don't use the
block chain to store backup data.

-Dave

[1] 
https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-May/021700.html


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 17
*******************************************
