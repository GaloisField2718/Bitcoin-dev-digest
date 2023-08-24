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

   1. Re: Scaling and anonymizing Bitcoin at layer 1 with
      client-side validation (John Tromp)
   2. Re: Standardisation of an unstructured taproot annex (Peter Todd)
   3. Re: Scaling and anonymizing Bitcoin at layer 1 with
      client-side validation (Dr Maxim Orlovsky)
   4. Re: Bitcoin mail list needs an explicit moderation	policy
      (alicexbt)


----------------------------------------------------------------------

Message: 1
Date: Sat, 3 Jun 2023 15:30:53 +0200
From: John Tromp <john.tromp@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Scaling and anonymizing Bitcoin at layer 1
	with client-side validation
Message-ID:
	<CAOU__fykfQiymVJ4oRwOZQPZu8CsYJhSHPJZZxoLDwRa25zu0Q@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

> The white paper describing the proposal can be found here:
> https://github.com/LNP-BP/layer1/

Some questions about the Bitcoin PoW anchoring:

What if a miner spends the current miner single-use-seal while
creating a commitment, but makes the PMT only partially available, or
entirely unavailable ?

How do other miners reach consensus on whether a protocol reset is
required? It seems impossible to agree on something like PMT
availability (much like mempool contents).


------------------------------

Message: 2
Date: Sat, 3 Jun 2023 15:50:27 +0000
From: Peter Todd <pete@petertodd.org>
To: Joost Jager <joost.jager@gmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: Greg Sanders <gsanders87@gmail.com>
Subject: Re: [bitcoin-dev] Standardisation of an unstructured taproot
	annex
Message-ID: <ZHthQ3VsQgPRvV5m@petertodd.org>
Content-Type: text/plain; charset="us-ascii"

On Sat, Jun 03, 2023 at 11:14:27AM +0200, Joost Jager via bitcoin-dev wrote:
> Depending on policy to mitigate this annex malleability vector could
> mislead developers into believing their transactions are immune to
> replacement, when in fact they might not be. This potential misalignment
> could result in developers and businesses constructing systems based on
> assumptions that could be compromised in the future, mirroring the
> situation that unfolded with zero-confirmation payments and rbf.
> 
> It may thus be more prudent to permit the utilization of the annex without
> restrictions, inform developers of its inherent risks, and acknowledge that
> Bitcoin, in its present state, might not be ideally suited for certain
> types of applications?

In the specific case of annex replacement leading to larger transactions, in
almost all cases you only care about the annex malleability causing the
transaction to take longer to get mined, due to it being larger. The fact the
transaction has become larger does not matter if the transaction does in fact
get mined, eg due to an out-of-band payment by the "attacker".

The only exception is the rare cases where some transaction processing
software/hardware has actual limits on transaction size. Eg you could imagine a
hardware wallet that simply *can't* process a transaction larger than a certain
size due to a lack of RAM.

I don't think this is a good rational to make use of the annex standard. Quite
the contrary: we should be thinking about if and how to fix annex malleability
in a future soft fork.

-- 
https://petertodd.org 'peter'[:-1]@petertodd.org
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/b7420b57/attachment-0001.sig>

------------------------------

Message: 3
Date: Sat, 03 Jun 2023 17:17:48 +0000
From: Dr Maxim Orlovsky <orlovsky@lnp-bp.org>
To: john.tromp@gmail.com, bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Scaling and anonymizing Bitcoin at layer 1
	with	client-side validation
Message-ID:
	<BZFrQ76cM2ULPqNTIuhMmyKw8RIGJPRdpkVaC_0VyWrceamVOutVF16m0fFchnl9SmJL_FLuPnYdNlOGh-SOUBoqdsh8MNwAoaVa2W8RGdg=@lnp-bp.org>
	
Content-Type: text/plain; charset="utf-8"

Hi John,

Thank you for the question. We have discussed this case in the paper, second paragraph of the ?Bitcoin PoW Anchoring? Section:

> If a party spends current miner single-use-seal without creating a commitment - or committing to a header without sufficient PoW, such closing is considered invalid; in this case, any party is allowed to create a special bitcoin transaction providing publically-identifiableOP_RETURNinformation ("announcement") about a new miner single-use-seal (protocol reset); only the firstOP_RETURNannouncement which is closed with a proper procedure is considered valid under the consensus rules.

Kind regards,
Maxim Orlovsky

On Sat, Jun 3, 2023 at 4:30 PM, John Tromp via bitcoin-dev <[bitcoin-dev@lists.linuxfoundation.org](mailto:On Sat, Jun 3, 2023 at 4:30 PM, John Tromp via bitcoin-dev <<a href=)> wrote:

>> The white paper describing the proposal can be found here:
>> https://github.com/LNP-BP/layer1/
>
> Some questions about the Bitcoin PoW anchoring:
>
> What if a miner spends the current miner single-use-seal while
> creating a commitment, but makes the PMT only partially available, or
> entirely unavailable ?
>
> How do other miners reach consensus on whether a protocol reset is
> required? It seems impossible to agree on something like PMT
> availability (much like mempool contents).
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230603/283cc020/attachment-0001.html>

------------------------------

Message: 4
Date: Sat, 03 Jun 2023 17:21:27 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Dr Maxim Orlovsky <orlovsky@protonmail.com>
Cc: bitcoin-dev@lists.linuxfoundation.org
Subject: Re: [bitcoin-dev] Bitcoin mail list needs an explicit
	moderation	policy
Message-ID:
	<GTdzPjEl3CPwtXTNPfqssJ5_xBr_Rd0AlI_1V4u7etEmG83LlMz7mR-RNlXSRureAp9_uz2JbQA06Y8grZi1mEC6dAt3w9uv8_tRrA4GQNE=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Maxim,

> In this regard, I?d like to propose the following:
> 
> 1.  The bitcoin-dev mail list must have a clear moderation (or pre-publication peer-review policy). It can be proposed and discussed in this mail list and, upon agreement, must become public and obligatory.
> 2.  Bryan Bishop, who was acting for a long time as moderator, must be appreciated for many years of unpaid work, and replaced with the new moderator who should be selected from a list of potential candidates (again in this mail list) using the criteria ?least votes against?.
> 3.  The role of the moderator(s) must be purely executive of the policies, without any personal preferences.
> 4.  A dedicated mail list should be created (?bitcoin-dev-unmoderated?) which will publish all submissions without moderation. It may contain spam and only people interested in the auditing bitcoin-dev main mal list non-censorship will be reading it. However, if they will notice that some non-spam e-mails were censored, they can announce that publicly. In this case, the failing moderator(s) should be removed and replaced.
> 5.  The incentive to work as a moderator should be reputation-based.

- I doubt moderation policy would change anything as it could be interpreted differently by everyone and misused. We have seen this in [BIPs repository][0] recently.

- We should change moderators regularly since everyone has their bias and mailing list is important part of discussions related to bitcoin development.

- Unmoderated mailing list front end could be created using all the emails from archives and moderated section. Moderated emails have attachments that would need some [EML parser][1].

I don't even know who are the present moderators or people with access to moderation queue. There should be some transparency about it.

[0]: https://github.com/bitcoin/bips/pull/1408
[1]: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020213.html

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Saturday, June 3rd, 2023 at 5:13 AM, Dr Maxim Orlovsky via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:


> Dear community,
> 
> 
> I am writing this list to bitcoin-dev mail list, but to prevent potential censorship I am sending CC to lightning-dev mail list, in order to leave the current moderator(s) without an option not to publish the letter and not to?leave the topic ?under the cover? (sorry Lightning friends for spamming your list with this off-topic).
> 
> 
> 
> A day before yesterday I sent a post to bitcoin-dev referencing the publication of the new Bitcoin scalability and privacy protocol, which had already received a broad reaction across the bitcoin community with literally no critical/negative responses after ~25k of reads [1]. I am not the first-time writer to the mail list and had developed things like RGB smart contracts [2], rust lightning implementation named LNP [3], multiple bitcoin libraries and software [4], [5], during three years was a main contributor to rust-bitcoin [6] etc, etc. The post was clearly not spam and received support from known community members like Giacomo Zucco [7]. Bryan Bishop knows me since 2019 when I was presenting Storm protocol on the stage on Scaling Bitcoin in Tel Aviv - and he was writing a transcript of it [8]. Thus, I am not a random unknown guy or a known spammer - and the post can be easily checked for not containing any scam promotion.
> 
> 
> 
> Nevertheless, I next day I see other e-mails getting released to bitcoin-dev, while mine - was not. It is not a problem, but since we already had an incident in the past where Bryan reported the failure of his software, me and my colleagues from LNP/BP Standards Association started asking questions about whether this post ever got to Bryan.
> 
> 
> 
> What happened next was very unexpected. I am giving the core of the conversation over Twitter after in Annex A - with the purpose to showcase the problem I?d like to address in this e-mail. From the discussion, it is clear that bitcoin-dev mail list lacks clear explicit moderation (or peer-review) policies, which must be applied on a non-selective basis. Also, Bryan Bishop, as the current moderator, had abused his powers in achieving his agenda based on personal likes or dislikes. The conversation went nowhere, and the post got published only after a requirement from Peter Todd [9].
> 
> 
> 
> In this regard, I?d like to propose the following:
> 
> 1.  The bitcoin-dev mail list must have a clear moderation (or pre-publication peer-review policy). It can be proposed and discussed in this mail list and, upon agreement, must become public and obligatory.
> 2.  Bryan Bishop, who was acting for a long time as moderator, must be appreciated for many years of unpaid work, and replaced with the new moderator who should be selected from a list of potential candidates (again in this mail list) using the criteria ?least votes against?.
> 3.  The role of the moderator(s) must be purely executive of the policies, without any personal preferences.
> 4.  A dedicated mail list should be created (?bitcoin-dev-unmoderated?) which will publish all submissions without moderation. It may contain spam and only people interested in the auditing bitcoin-dev main mal list non-censorship will be reading it. However, if they will notice that some non-spam e-mails were censored, they can announce that publicly. In this case, the failing moderator(s) should be removed and replaced.
> 5.  The incentive to work as a moderator should be reputation-based.
> 
> 
> 
> With that, I rest my case.
> 
> 
> 
> Kind regards,
> 
> Maxim Orlovsky
> 
> 
> 
> [1]:?https://twitter.com/lnp_bp/status/1664329393131364353?s=61&t=9A8uvggqKVKV3sT4HPlQyg
> 
> [2]:?https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021554.html
> 
> [3]:?https://github.com/LNP-WG
> 
> [4]:?https://github.com/BP-WG
> 
> [5]:?https://github.com/mycitadel
> 
> [6]:?https://github.com/rust-bitcoin/rust-bitcoin/graphs/contributors?from=2018-12-31&to=2022-04-12&type=c
> 
> [7]:?https://twitter.com/giacomozucco/status/1664515543154544645?s=61&t=9A8uvggqKVKV3sT4HPlQyg?and?https://twitter.com/giacomozucco/status/1664731504923095041?s=61&t=9A8uvggqKVKV3sT4HPlQyg
> 
> [8]:?https://scalingbitcoin.org/transcript/telaviv2019/wip-storm-layer-2-3-storage-and-messaging
> 
> [9]:?https://twitter.com/peterktodd/status/1664742651835367424?s=61&t=9A8uvggqKVKV3sT4HPlQyg
> 
> 
> 
> 
> 
> Annex A:
> 
> 
> 
> -   @kanzure just like to check that our submission to bitcoin-dev hasn?t got to spam <https://twitter.com/lnp_bp/status/1664649328349069320?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   A few mods are reviewing it <https://twitter.com/kanzure/status/1664680893548572677?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Oh, so a peer review is required to get to bitcoin-dev mail list? Never read about that requirement anywhere <https://twitter.com/lnp_bp/status/1664695061462777858?s=61&t=9A8uvggqKVKV3sT4HPlQyg>. Seems like bitcoin-dev mail list requirements are now specific to the author :) <https://twitter.com/dr_orlovsky/status/1664695668475142144?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Not the greatest email to pull this over. I'll double check but pretty sure the antagonization is boring me. <https://twitter.com/kanzure/status/1664705038315409420?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Not sure I understand what you are saying. Can you please clarify? <https://twitter.com/dr_orlovsky/status/1664705280393859103?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   You are boring me and these antics don't make me want to go click approve on your email. <https://twitter.com/kanzure/status/1664705509147004946?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Are you the person to approve emails for it? <https://twitter.com/phyrooo/status/1664732932068589568?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Yes <https://twitter.com/kanzure/status/1664733107096899585?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   It appears that people boring @kanzure is going through a dedicated review procedure on bitcoin-dev mail list. Good moderation! Very clear policy! <https://twitter.com/dr_orlovsky/status/1664706165790461959?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   What are you even doing. How does this behavior suppose to get people to help you? <https://twitter.com/kanzure/status/1664706931083329536?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   I am not expecting you to help me - and never asked. I expect you to openly declare moderation (or peer review) policy and follow it. <https://twitter.com/dr_orlovsky/status/1664719295123685381?s=61&t=9A8uvggqKVKV3sT4HPlQyg> Since ?if you get me bored I will not click an accept button? is not a moderation policy which I expect from bitcoin-dev mail list. Probably not just me. <https://twitter.com/dr_orlovsky/status/1664719786633310209?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Yeah I mean I don't think these tweets are likely to get me to enthusiastically resolve your problem... I dunno man. What's even going on here. <https://twitter.com/kanzure/status/1664735139065208833?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> -   Bitcoin mail list clearly lacks explicit moderation policy. The same mistake like with rust-bitcoin 1+ yrs ago. I am fine with peer review. Moderation. But only explicit - not just ?the way I (dis)like this guy? <https://twitter.com/dr_orlovsky/status/1664736404931321859?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
> 
> 
> 
> 


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 7
******************************************
