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
   2. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Peter Todd)
   3. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Matt Corallo)
   4. Re: [Lightning-dev] Full Disclosure: CVE-2023-40231 /
      CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All your
      mempool are belong to us" (Peter Todd)


----------------------------------------------------------------------

Message: 1
Date: Fri, 20 Oct 2023 21:03:49 -0400
From: Matt Corallo <lf-lists@mattcorallo.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <24a18bdd-eef6-4f96-b8a5-05f64130a5c5@mattcorallo.com>
Content-Type: text/plain; charset=UTF-8; format=flowed



On 10/20/23 8:15 PM, Peter Todd wrote:
> On Fri, Oct 20, 2023 at 05:05:48PM -0400, Matt Corallo wrote:
>> Sadly this only is really viable for pre-anchor channels. With anchor
>> channels the attack can be performed by either side of the closure, as the
>> HTLCs are now, at max, only signed SIGHASH_SINGLE|ANYONECANPAY, allowing you
>> to add more inputs and perform this attack even as the broadcaster.
>>
>> I don't think its really viable to walk that change back to fix this, as it
>> also fixed plenty of other issues with channel usability and important
>> edge-cases.
> 
> What are anchor outputs used for other than increasing fees?
> 
> Because if we've pre-signed the full fee range, there is simply no need for
> anchor outputs. Under any circumstance we can broadcast a transaction with a
> sufficiently high fee to get mined.


Indeed, that is what anchor outputs are for. Removing the pre-set feerate solved a number of issues 
with edge-cases and helped address the fee-inflation attack. Now, just using pre-signed transactions 
doesn't have to re-introduce those issues - as long as the broadcaster gets to pick which of the 
possible transactions they broadcast its just another transaction of theirs.

Still, I'm generally really dubious of the multiple pre-signed transaction thing, (a) it would mean 
more fee overhead (not the end of the world for a force-closure, but it sucks to have all these 
individual transactions rolling around and be unable to batch), but more importantly (b) its a bunch 
of overhead to keep track of a ton of variants across a sufficiently granular set of feerates for it 
to not result in substantially overspending on fees.

Like I mentioned in the previous mail, this is really a policy bug - we're talking about a 
transaction pattern that might well happen where miners aren't getting the optimal value in 
transaction fees (potentially by a good bit). This needs to be fixed at the policy/Bitcoin Core 
layer, not in the lightning world (as much as its pretty resource-intensive to fix in the policy 
domain, I think).

Matt


------------------------------

Message: 2
Date: Sat, 21 Oct 2023 01:25:10 +0000
From: Peter Todd <pete@petertodd.org>
To: Matt Corallo <lf-lists@mattcorallo.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <ZTModpNyIQ3qFFI3@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 09:03:49PM -0400, Matt Corallo wrote:
> > What are anchor outputs used for other than increasing fees?
> > 
> > Because if we've pre-signed the full fee range, there is simply no need for
> > anchor outputs. Under any circumstance we can broadcast a transaction with a
> > sufficiently high fee to get mined.
> 
> 
> Indeed, that is what anchor outputs are for. Removing the pre-set feerate
> solved a number of issues with edge-cases and helped address the
> fee-inflation attack. Now, just using pre-signed transactions doesn't have
> to re-introduce those issues - as long as the broadcaster gets to pick which
> of the possible transactions they broadcast its just another transaction of
> theirs.
> 
> Still, I'm generally really dubious of the multiple pre-signed transaction
> thing, (a) it would mean more fee overhead (not the end of the world for a
> force-closure, but it sucks to have all these individual transactions
> rolling around and be unable to batch), but more importantly (b) its a bunch
> of overhead to keep track of a ton of variants across a sufficiently
> granular set of feerates for it to not result in substantially overspending
> on fees.

Quite the contrary. Schnorr signatures are 64 bytes, so in situations like
lightning where the transaction form is deterministically derived, signing 100
extra transactions requires just 6400 extra bytes. Even a very slow 100KB/s
connection can transfer that in 64ms; latency will still dominate.

RBF has a minimum incremental relay fee of 1sat/vByte by default. So if you use
those 100 pre-signed transaction variants to do nothing more than sign every
possible minimum incremental relay, you've covered a range of 1sat/vByte to
100sat/vByte. I believe that is sufficient to get mined for any block in
Bitcoin's entire modern history.

CPFP meanwhile requires two transactions, and thus extra bytes. Other than edge
cases with very large transactions in low-fee environments, there's no
circumstance where CPFP beats RBF.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/adb5dfe7/attachment-0001.sig>

------------------------------

Message: 3
Date: Fri, 20 Oct 2023 21:55:12 -0400
From: Matt Corallo <lf-lists@mattcorallo.com>
To: Peter Todd <pete@petertodd.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <c7ca9861-0734-4065-851a-8af9cabd7e87@mattcorallo.com>
Content-Type: text/plain; charset=UTF-8; format=flowed



On 10/20/23 9:25 PM, Peter Todd wrote:
> On Fri, Oct 20, 2023 at 09:03:49PM -0400, Matt Corallo wrote:
>>> What are anchor outputs used for other than increasing fees?
>>>
>>> Because if we've pre-signed the full fee range, there is simply no need for
>>> anchor outputs. Under any circumstance we can broadcast a transaction with a
>>> sufficiently high fee to get mined.
>>
>>
>> Indeed, that is what anchor outputs are for. Removing the pre-set feerate
>> solved a number of issues with edge-cases and helped address the
>> fee-inflation attack. Now, just using pre-signed transactions doesn't have
>> to re-introduce those issues - as long as the broadcaster gets to pick which
>> of the possible transactions they broadcast its just another transaction of
>> theirs.
>>
>> Still, I'm generally really dubious of the multiple pre-signed transaction
>> thing, (a) it would mean more fee overhead (not the end of the world for a
>> force-closure, but it sucks to have all these individual transactions
>> rolling around and be unable to batch), but more importantly (b) its a bunch
>> of overhead to keep track of a ton of variants across a sufficiently
>> granular set of feerates for it to not result in substantially overspending
>> on fees.
> 
> Quite the contrary. Schnorr signatures are 64 bytes, so in situations like
> lightning where the transaction form is deterministically derived, signing 100
> extra transactions requires just 6400 extra bytes. Even a very slow 100KB/s
> connection can transfer that in 64ms; latency will still dominate.

Lightning today isn't all that much data, but multiply it by 100 and we start racking up data enough 
that people may start to have to store a really material amount of data for larger nodes and dealing 
with that starts to be a much bigger pain then when we're talking about a GiB or twenty.

> RBF has a minimum incremental relay fee of 1sat/vByte by default. So if you use
> those 100 pre-signed transaction variants to do nothing more than sign every
> possible minimum incremental relay, you've covered a range of 1sat/vByte to
> 100sat/vByte. I believe that is sufficient to get mined for any block in
> Bitcoin's entire modern history.
> 
> CPFP meanwhile requires two transactions, and thus extra bytes. Other than edge
> cases with very large transactions in low-fee environments, there's no
> circumstance where CPFP beats RBF.

What I was referring to is that if we have the SIGHASH_SINGLE|ANYONECANPAY we can combine many HTLC 
claims into one transaction, vs pre-signing means we're stuck with a ton of individual transactions.

Matt


------------------------------

Message: 4
Date: Sat, 21 Oct 2023 02:43:31 +0000
From: Peter Todd <pete@petertodd.org>
To: Matt Corallo <lf-lists@mattcorallo.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, security@ariard.me,
	"lightning-dev\\\\\\\\\\\\\\\\@lists.linuxfoundation.org"
	<lightning-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [Lightning-dev] Full Disclosure:
	CVE-2023-40231 / CVE-2023-40232 / CVE-2023-40233 / CVE-2023-40234 "All
	your mempool are belong to us"
Message-ID: <ZTM607UFnxgXPSNp@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Fri, Oct 20, 2023 at 09:55:12PM -0400, Matt Corallo wrote:
> > Quite the contrary. Schnorr signatures are 64 bytes, so in situations like
> > lightning where the transaction form is deterministically derived, signing 100
> > extra transactions requires just 6400 extra bytes. Even a very slow 100KB/s
> > connection can transfer that in 64ms; latency will still dominate.
> 
> Lightning today isn't all that much data, but multiply it by 100 and we
> start racking up data enough that people may start to have to store a really
> material amount of data for larger nodes and dealing with that starts to be
> a much bigger pain then when we're talking about a GiB or twenty.

We are talking about storing ephemeral data here, HTLC transactions and
possibly commitment transactions. Since lightning uses disclosed secrets to
invalidate old state, you do not need to keep every signature from your
counterparty indefinitely.

Per channel, with the above numbers, you'd need <10KB worth of extra signatures
to fee bump the current commitment (with pre-signed txs), and if HTLCs happen
to be in flight, say <10KB of extra signatures per HTLC.

Amazon AWS charges $0.125/GB/month for their most expensive SSD volumes. Let's
round that up to $1/GB/month to account for RAID and backups. Let's say each
channel constantly has 483 HTLC's in flight, and each HTLC is associated with
~10KB of extra data for pre-signed transactions.

That's ~5MB/channel of data you constantly need to store, or $0.005/month.

In what world is that too expensive or too much of a pain to deal with? If
you're node is actually that busy, you're probably making that cost back per
channel every minute, or better.

> > RBF has a minimum incremental relay fee of 1sat/vByte by default. So if you use
> > those 100 pre-signed transaction variants to do nothing more than sign every
> > possible minimum incremental relay, you've covered a range of 1sat/vByte to
> > 100sat/vByte. I believe that is sufficient to get mined for any block in
> > Bitcoin's entire modern history.
> > 
> > CPFP meanwhile requires two transactions, and thus extra bytes. Other than edge
> > cases with very large transactions in low-fee environments, there's no
> > circumstance where CPFP beats RBF.
> 
> What I was referring to is that if we have the SIGHASH_SINGLE|ANYONECANPAY
> we can combine many HTLC claims into one transaction, vs pre-signing means
> we're stuck with a ton of individual transactions.

Since SIGHASH_SINGLE requires one output per input, the savings you get by
combining multiple SIGHASH_SINGLE transactions together aren't very
significant. Just 18 bytes for nVersion, nLockTime, and the txin and txout size
fields. The HTLC-timeout transaction is 166.5 vBytes, so that's a savings of
just 11%

Of course, if you _do_ need to fee bump and add an additional input, that input
takes up space, and you'll probably need a change output. At which point you
again would probably have been better off with a pre-signed transaction.

You are also assuming there's lots of HTLC's in flight that need to be spent.
That's very often not the case.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231021/73c2036a/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 31
********************************************
