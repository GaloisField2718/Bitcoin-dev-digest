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
      (Antoine Riard)


----------------------------------------------------------------------

Message: 1
Date: Tue, 4 Jul 2023 21:18:23 +0100
From: Antoine Riard <antoine.riard@gmail.com>
To: Joost Jager <joost.jager@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID:
	<CALZpt+GZd8kv4Nq-ANR26GPeT_6+0U8zRnsQM1_OLOuhxD7QFg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Joost,

> Hopefully this further raises awareness of the on-chain ephemeral
signature backup functionality that the annex uniquely enables.

>From my perspective, if vault applications can be made more robust by
on-chain backing up of ephemeral signatures, this can be rational to make
the annex standard.

There is the observation that other critical elements of vault's
application state could be backed up in this way (e.g pubkeys and amounts
of the destination output) to rebuild from scratch a pre-signed withdrawal.
The unstructured data could be even marked by an application-level "tag" or
"signaling" to identify all the backup annexes composing your vault
application state.

Of course, such backing up of more critical elements comes with its own
drawbacks in terms of confidentiality, as you would leak your vault policy
on-chain, so they would need to be ciphered first, I think.

It sounds to me another economically rational set of use-cases can be to
simplify protocols using the chain as a publication space for collectibles.
Using the annex as a publication space enables a clear chain of collectible
ownership thanks to the key signing the annex, which is not permissible
with op_return outputs today.

Best,
Antoine


Le mar. 20 juin 2023 ? 13:30, Joost Jager <joost.jager@gmail.com> a ?crit :

> Hi all,
>
> On Sat, Jun 10, 2023 at 9:43?AM Joost Jager <joost.jager@gmail.com> wrote:
>
>> However, the primary advantage I see in the annex is that its data isn't
>> included in the calculation of the txid or a potential parent commit
>> transaction's txid (for inscriptions). I've explained this at [1]. This
>> feature makes the annex a powerful tool for applications that would ideally
>> use covenants.
>>
>> The most critical application in this category, for me, involves
>> time-locked vaults. Given the positive reception to proposals such as
>> OP_VAULT [2], I don't think I'm alone in this belief. OP_VAULT is probably
>> a bit further out, but pre-signed transactions signed using an ephemeral
>> key can fill the gap and improve the safeguarding of Bitcoin in the short
>> term.
>>
>> Backing up the ephemeral signatures of the pre-signed transactions on the
>> blockchain itself is an excellent way to ensure that the vault can always
>> be 'opened'. However, without the annex, this is not as safe as it could
>> be. Due to the described circular reference problem, the vault creation and
>> signature backup can't be executed in one atomic operation. For example,
>> you can store the backup in a child commit/reveal transaction set, but the
>> vault itself can be confirmed independently and the backup may never
>> confirm. If you create a vault and lose the ephemeral signatures, the funds
>> will be lost.
>>
>> This use case for the annex has been labeled 'speculative' elsewhere. To
>> me, every use case appears speculative at this point because the annex
>> isn't available. However, if you believe that time-locked vaults are
>> important for Bitcoin and also acknowledge that soft forks, such as the one
>> required for OP_VAULT, aren't easy to implement, I'd argue that the
>> intermediate solution described above is very relevant.
>>
>
> To support this use case of the taproot annex, I've create a simple demo
> application here: https://github.com/joostjager/annex-covenants
>
> This demo shows how a coin can be spent to a special address from which it
> can - at a later stage - only move to a pre-defined final destination. It
> makes use of the annex to store the ephemeral signature for the presigned
> transaction so that the coin cannot get lost. This is assuming that nodes
> do not prune witness data en masse and also that the destination address
> itself is known.
>
> The application may not be the most practically useful, but more advanced
> covenants such as time-locked vaults can be implemented similarly.
>
> Hopefully this further raises awareness of the on-chain ephemeral
> signature backup functionality that the annex uniquely enables.
>
> Joost
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230704/ecfe6628/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 98, Issue 1
******************************************
