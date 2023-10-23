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

   1. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Matt Corallo)
   2. Re: Ordinals BIP PR (L?o Haf)
   3. Re: Ordinals BIP PR (Tim Ruffing)
   4. Re: Ordinals BIP PR (Andrew Poelstra)
   5. Re: Ordinals BIP PR (Luke Dashjr)


----------------------------------------------------------------------

Message: 1
Date: Mon, 23 Oct 2023 09:09:50 -0700
From: Matt Corallo <lf-lists@mattcorallo.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <82353ef0-71c3-4c18-8e2b-80c69a391212@mattcorallo.com>
Content-Type: text/plain; charset=UTF-8; format=flowed



On 10/20/23 7:43 PM, Peter Todd wrote:
> On Fri, Oct 20, 2023 at 09:55:12PM -0400, Matt Corallo wrote:
>>> Quite the contrary. Schnorr signatures are 64 bytes, so in situations like
>>> lightning where the transaction form is deterministically derived, signing 100
>>> extra transactions requires just 6400 extra bytes. Even a very slow 100KB/s
>>> connection can transfer that in 64ms; latency will still dominate.
>>
>> Lightning today isn't all that much data, but multiply it by 100 and we
>> start racking up data enough that people may start to have to store a really
>> material amount of data for larger nodes and dealing with that starts to be
>> a much bigger pain then when we're talking about a GiB or twenty.
> 
> We are talking about storing ephemeral data here, HTLC transactions and
> possibly commitment transactions. Since lightning uses disclosed secrets to
> invalidate old state, you do not need to keep every signature from your
> counterparty indefinitely.

Mmm, fair point, yes.

>>> RBF has a minimum incremental relay fee of 1sat/vByte by default. So if you use
>>> those 100 pre-signed transaction variants to do nothing more than sign every
>>> possible minimum incremental relay, you've covered a range of 1sat/vByte to
>>> 100sat/vByte. I believe that is sufficient to get mined for any block in
>>> Bitcoin's entire modern history.
>>>
>>> CPFP meanwhile requires two transactions, and thus extra bytes. Other than edge
>>> cases with very large transactions in low-fee environments, there's no
>>> circumstance where CPFP beats RBF.
>>
>> What I was referring to is that if we have the SIGHASH_SINGLE|ANYONECANPAY
>> we can combine many HTLC claims into one transaction, vs pre-signing means
>> we're stuck with a ton of individual transactions.
> 
> Since SIGHASH_SINGLE requires one output per input, the savings you get by
> combining multiple SIGHASH_SINGLE transactions together aren't very
> significant. Just 18 bytes for nVersion, nLockTime, and the txin and txout size
> fields. The HTLC-timeout transaction is 166.5 vBytes, so that's a savings of
> just 11%

Yep, its not a lot, but for a thing that's inherently super chain-spammy, its still quite nice.

> Of course, if you _do_ need to fee bump and add an additional input, that input
> takes up space, and you'll probably need a change output. At which point you
> again would probably have been better off with a pre-signed transaction.
> 
> You are also assuming there's lots of HTLC's in flight that need to be spent.
> That's very often not the case.

In general, yes, in force-close cases often there's been some failure which is repeated in several 
HTLCs :).

More generally, I think we're getting lost here - this isn't really a material change for 
lightning's trust model - its already the case that a peer that is willing to put a lot of work in 
can probably steal your money, and there's now just one more way they can do that. We really don't 
need to rush to "fix lightning" here, we can do it right and fix it at the ecosystem level. It 
shouldn't be the case that a policy restriction results in both screwing up a L2 network *and* 
results in miners getting paid less. That's a policy bug.

Matt


------------------------------

Message: 2
Date: Mon, 23 Oct 2023 16:57:32 +0200
From: L?o Haf <leohaf@orangepill.ovh>
To: Casey Rodarmor <casey@rodarmor.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <C61E710C-772F-4473-8FF2-38A47AC0D333@orangepill.ovh>
Content-Type: text/plain; charset="utf-8"

? BIPs such as the increase in block size, drives-chains, colored coins, etc... were proposals for Bitcoin improvements. On the other hand, your BIP brings absolutely no improvement, on the contrary it is a regression, but you already know that.

I strongly invite you to retract or if the desire continues to push you to negatively affect the chain, to create OIPs or anything similar, as far as possible from the development of Bitcoin and real BIPs that improve Bitcoin.

L?o Haf. 

> Le 23 oct. 2023 ? 10:23, Casey Rodarmor via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> a ?crit :
> ?
> Dear List,
> 
> The Ordinals BIP PR has been sitting open for nine months now[0]. I've commented a few times asking the BIP editors to let me know what is needed for the BIP to either be merged or rejected. I've also reached out to the BIP editors via DM and email, but haven't received a response.
> 
> There has been much misunderstanding of the nature of the BIP process. BIPS, in particular informational BIPs, are a form of technical documentation, and their acceptance does not indicate that they will be included in any implementation, including Bitcoin Core, nor that they they have consensus among the community.
> 
> Preexisting BIPs include hard-fork block size increases, hard-fork proof-of-work changes, colored coin voting protocols, rejected soft fork proposals, encouragement of address reuse, and drivechain.
> 
> I believe ordinals is in-scope for a BIP, and am hoping to get the PR unstuck. I would appreciate feedback from the BIP editors on whether it is in-scope for a BIP, if not, why not, and if so, what changes need to be made for it to be accepted.
> 
> Best regards,
> Casey Rodarmor
> 
> [0] https://github.com/bitcoin/bips/pull/1408
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/a70a3daa/attachment-0001.html>

------------------------------

Message: 3
Date: Mon, 23 Oct 2023 18:32:47 +0200
From: Tim Ruffing <crypto@timruffing.de>
To: Peter Todd <pete@petertodd.org>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID:
	<5f1ba40e6b853851112652b0da8eb7d35369af82.camel@timruffing.de>
Content-Type: text/plain; charset="UTF-8"

On Mon, 2023-10-23 at 15:35 +0000, Peter Todd via bitcoin-dev wrote:
> Thus
> we should limit BIP assignment to the minimum possible: _extremely_
> widespread
> standards used by the _entire_ Bitcoin community, for the core
> mission of
> Bitcoin.

BIPs are Bitcoin Improvement *Proposals*. What you suggest would imply
that someone needs to evaluate them even before they become proposals.
And this raises plenty of notoriously hard to answers questions:
 * Who is in charge?
 * How to predict if a proposal will be a widespread standard?
 * What is the core mission of Bitcoin?
 * How to measure if something is for the core mission?
 * Who and what is the _entire_ Bitcoin community?

Best,
Tim


------------------------------

Message: 4
Date: Mon, 23 Oct 2023 17:43:29 +0000
From: Andrew Poelstra <apoelstra@wpsoftware.net>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <ZTawwRqGN4XUUu8C@camus>
Content-Type: text/plain; charset="us-ascii"

On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via bitcoin-dev wrote:
> 
> I have _not_ requested a BIP for OpenTimestamps, even though it is of much
> wider relevance to Bitcoin users than Ordinals by virtue of the fact that much
> of the commonly used software, including Bitcoin Core, is timestamped with OTS.
> I have not, because there is no need to document every single little protocol
> that happens to use Bitcoin with a BIP.
> 
> Frankly we've been using BIPs for too many things. There is no avoiding the act
> that BIP assignment and acceptance is a mark of approval for a protocol. Thus
> we should limit BIP assignment to the minimum possible: _extremely_ widespread
> standards used by the _entire_ Bitcoin community, for the core mission of
> Bitcoin.
>

This would eliminate most wallet-related protocols e.g. BIP69 (sorted
keys), ypubs, zpubs, etc. I don't particularly like any of those but if
they can't be BIPs then they'd need to find another spec repository
where they wouldn't be lost and where updates could be tracked.

The SLIP repo could serve this purpose, and I think e.g. SLIP39 is not a BIP
in part because of perceived friction and exclusivity of the BIPs repo.
But I'm not thrilled with this situation.

In fact, I would prefer that OpenTimestamps were a BIP :).

> It's notable that Lightning is _not_ standardized via the BIP process. I think
> that's a good thing. While it's arguably of wide enough use to warrent BIPs,
> Lightning doesn't need the approval of Core maintainers, and using their
> separate BOLT process makes that clear.
> 

Well, LN is a bit special because it's so big that it can have its own
spec repo which is actively maintained and used.

While it's technically true that BIPs need "approval of Core maintainers" 
to be merged, the text of BIP2 suggests that this approval should be a
functionary role and be pretty-much automatic. And not require the BIP
be relevant or interesting or desireable to Core developers.


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
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231023/0e346ea4/attachment-0001.sig>

------------------------------

Message: 5
Date: Mon, 23 Oct 2023 14:29:50 -0400
From: Luke Dashjr <luke@dashjr.org>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ordinals BIP PR
Message-ID: <5b641ddc-a30b-4dd7-2481-6d9cdb459359@dashjr.org>
Content-Type: text/plain; charset=UTF-8; format=flowed

Everything standardized between Bitcoin software is eligible to be and 
should be a BIP. I completely disagree with the claim that it's used for 
too many things.

SLIPs exist for altcoin stuff. They shouldn't be used for things related 
to Bitcoin.

BOLTs also shouldn't have ever been a separate process and should really 
just get merged into BIPs. But at this point, that will probably take 
quite a bit of effort, and obviously cooperation and active involvement 
from the Lightning development community.

Maybe we need a 3rd BIP editor. Both Kalle and myself haven't had time 
to keep up. There are several PRs far more important than Ordinals 
nonsense that need to be triaged and probably merged.

The issue with Ordinals is that it is actually unclear if it's eligible 
to be a BIP at all, since it is an attack on Bitcoin rather than a 
proposed improvement. There is a debate on the PR whether the 
"technically unsound, ..., or not in keeping with the Bitcoin 
philosophy." or "must represent a net improvement." clauses (BIP 2) are 
relevant. Those issues need to be resolved somehow before it could be 
merged. I have already commented to this effect and given my own 
opinions on the PR, and simply pretending the issues don't exist won't 
make them go away. (Nor is it worth the time of honest people to help 
Casey resolve this just so he can further try to harm/destroy Bitcoin.)

Luke


On 10/23/23 13:43, Andrew Poelstra via bitcoin-dev wrote:
> On Mon, Oct 23, 2023 at 03:35:30PM +0000, Peter Todd via bitcoin-dev wrote:
>> I have _not_ requested a BIP for OpenTimestamps, even though it is of much
>> wider relevance to Bitcoin users than Ordinals by virtue of the fact that much
>> of the commonly used software, including Bitcoin Core, is timestamped with OTS.
>> I have not, because there is no need to document every single little protocol
>> that happens to use Bitcoin with a BIP.
>>
>> Frankly we've been using BIPs for too many things. There is no avoiding the act
>> that BIP assignment and acceptance is a mark of approval for a protocol. Thus
>> we should limit BIP assignment to the minimum possible: _extremely_ widespread
>> standards used by the _entire_ Bitcoin community, for the core mission of
>> Bitcoin.
>>
> This would eliminate most wallet-related protocols e.g. BIP69 (sorted
> keys), ypubs, zpubs, etc. I don't particularly like any of those but if
> they can't be BIPs then they'd need to find another spec repository
> where they wouldn't be lost and where updates could be tracked.
>
> The SLIP repo could serve this purpose, and I think e.g. SLIP39 is not a BIP
> in part because of perceived friction and exclusivity of the BIPs repo.
> But I'm not thrilled with this situation.
>
> In fact, I would prefer that OpenTimestamps were a BIP :).
>
>> It's notable that Lightning is _not_ standardized via the BIP process. I think
>> that's a good thing. While it's arguably of wide enough use to warrent BIPs,
>> Lightning doesn't need the approval of Core maintainers, and using their
>> separate BOLT process makes that clear.
>>
> Well, LN is a bit special because it's so big that it can have its own
> spec repo which is actively maintained and used.
>
> While it's technically true that BIPs need "approval of Core maintainers"
> to be merged, the text of BIP2 suggests that this approval should be a
> functionary role and be pretty-much automatic. And not require the BIP
> be relevant or interesting or desireable to Core developers.
>
>
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

End of bitcoin-dev Digest, Vol 101, Issue 40
********************************************
