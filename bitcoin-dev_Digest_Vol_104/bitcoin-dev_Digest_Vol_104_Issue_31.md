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

   1. Re: One-Shot Replace-By-Fee-Rate (Murch)


----------------------------------------------------------------------

Message: 1
Date: Sun, 28 Jan 2024 12:27:06 -0500
From: Murch <murch@murch.one>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] One-Shot Replace-By-Fee-Rate
Message-ID: <42006209-4ea4-4008-b3b3-556a8461323c@murch.one>
Content-Type: text/plain; charset=UTF-8; format=flowed

Hi Peter,

Thanks you for investigate my concern and replicate the scenario I drafted.

On 27.01.24 02:19, Peter Todd wrote:
> I actually tried this attack out, and it fails at step #4 due to the Rule #6,
> PaysMoreThanConflicts, check.
> 
> While on stacker.news you stated that:
> 
>      tx_HS has 5000 vB and pays 21 s/vB, but since it spends an output from a
>      low-feerate parent, it?s mining score is only 1.95?s/vB.
> 
> and
> 
>      You RBF tx_LL and tx_HS with tx_LM that has 100,000 vB and pays 3.05?s/vB (fee:
>      305,000 s) by spending the outputs C1 and C2. This is permitted, since only
>      tx_LL is a direct conflict, so the feerate of tx_HS does not have to be beat
>      directly.
> 
> tx_HS _is_ considered to be a direct conflict, and its raw fee-rate _does_ have
> to be beat directly. While ts_HS does spend an unconfirmed output, it appears
> that the fee-rate PaysMoreThanConflicts uses to calculate if ts_HS can be
> beaten is ts_HS's raw fee-rate. So looks like your understanding was incorrect
> on these two points.

I agree in the detail, but not about the big picture. You are right that 
it?s a problem that `tx_LM` and `tx_HS` spend the same input and 
therefore are direct conflicts.

Luckily, it is unnecessary for my scenario that `tx_LM` and `tx_HS` 
conflict. The scenario only requires that `tx_LM` conflicts with `tx_LL` 
and `tx_RBFr`. `tx_HS` is supposed to get dropped indirectly per the 
conflict with `tx_LL`.

It seems to me that my example attack should work when a third confirmed 
input `c3` is introduced as follows:
`tx_LM` spends `c3` instead of `c2`, and `tx_RBFr` spends both `c2` and 
`c3`, which allows the following four conflicts:

- `tx_HS` and `tx_RBFr` conflict on spending `c2`
- `tx_HS` and `tx_LS` conflict on spending `tx_LL:0`
- `tx_LL` and `tx_LM` conflict on spending `c1`
- `tx_LM` and `tx_RBFr` conflict on spending `c3`

`tx_RBFr` would end up slightly bigger and therefore have a bigger fee, 
but otherwise the number should work out fine as they are.
I have not verified this yet (thanks for sharing your code), but I might 
be able to take another look in the coming week if you haven?t by then.

It seems to me that my main point stands, though: the proposed RBFr 
rules would enable infinite replacement cycles in combination with the 
existing RBF rules.

Murch


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 31
********************************************
