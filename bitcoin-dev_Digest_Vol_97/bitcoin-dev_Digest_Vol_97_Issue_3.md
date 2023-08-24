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

   1. Scaling and anonymizing Bitcoin at layer 1 with	client-side
      validation (Dr Maxim Orlovsky)
   2. Bitcoin mail list needs an explicit moderation policy
      (Dr Maxim Orlovsky)


----------------------------------------------------------------------

Message: 1
Date: Thu, 01 Jun 2023 17:21:39 +0000
From: Dr Maxim Orlovsky <orlovsky@lnp-bp.org>
To: bitcoin-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Scaling and anonymizing Bitcoin at layer 1 with
	client-side validation
Message-ID:
	<W-qyMFEGyTIpuZXvGiif_9Funkz7LLwtl6Iyv_yxxouiSwygBVOq5MM6CX4Pr2CCenCzginP4cn5csOar3gyYN20I6Izhr_mvOeCzbRYk2w=@lnp-bp.org>
	
Content-Type: text/plain; charset="utf-8"

Dear community,

Some time ago we (LNP/BP Standards Association) announced the release of RGB smart contract system [1]. In the subsequent discussion, we have referenced [2] that the introduction of client-side validation has the potential for upgrading Bitcoin layer 1 - blockchain, which has become an unnecessary limiting factor for the Bitcoin ecosystem, creating both scaling and privacy problems. While client-side validation requires consensus protocol and some layer 1 (for the proof of publication), this layer can be implemented in a more efficient way than the Bitcoin blockchain.

Today we are glad to present Prime: a proposal to upgrade Bitcoin protocol with the new scalable (up to billions of tx per minute) and fully anonymous (opaque) layer 1, moving most validation work into the client-side validation system. It leaves BTC (Bitcoin as money) and the rest of the Bitcoin ecosystem (including PoW) intact. It may be deployed without a softfork and miners upgrade, but can certainly benefit from it. It doesn't affect those users who are not willing to upgrade and doesn't require any consensus or majority for the initial deployment. It also makes Lightning Network and other layer 2 systems redundant. Finally, it will make things like BRC20, inscriptions, ordinals etc. impossible; all proper assets, NFTs etc. will be done with RGB smart contracts, not forcing non-users to store, validate and use their network bandwidth for the unpaid third-party interests.

The white paper describing the proposal can be found here:
https://github.com/LNP-BP/layer1/

As LNP/BP Standards Association we are setting a working group which will be focused on formal specification and reference implementation of this new layer - and will gladly accept everybody who wishes to cooperate on this topic. We also plan educational and workshop activities to make community understand the underlying technology better and take educated decision on its adoption.

We believe that this infrastructural effort must not be managed by a for-profit company - or a commercial group with its interests, and the only proper way of funding such an effort should be through non-profit donations. We do plan a fundraising campaign, so everyone interested in driving the Bitcoin evolution forward please contact us at ukolova [at] lnp-bp.org. For-profit organizations can also become members of the Association [3] and get to the committees defining the shape of the future Bitcoin technologies.

Dr Maxim Orlovsky
on behalf of LNP/BP Standards Association
https://lnp-bp.org/
GitHub: github.com/LNP-BP
Twitter: @lnp_bp
Nostr: npub13mhg7ksq9efna8ullmc5cufa53yuy06k73q4u7v425s8tgpdr5msk5mnym

[1]: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021554.html
[2]: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021577.html
[3]: https://www.lnp-bp.org/membership
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230601/3ede4035/attachment-0001.html>

------------------------------

Message: 2
Date: Fri, 02 Jun 2023 23:43:45 +0000
From: Dr Maxim Orlovsky <orlovsky@protonmail.com>
To: bitcoin-dev@lists.linuxfoundation.org,
	lightning-dev@lists.linuxfoundation.org
Subject: [bitcoin-dev] Bitcoin mail list needs an explicit moderation
	policy
Message-ID:
	<eXXv90Zp7BkXLnld8dDksxrZ7tA0rHngfZ2NLwQ3hrt5tBWGmodmDaT7_JzbcyMukDSVSNtbNoV0wxrkFZt29bXW5WyAT6iyL4lFcvlRDI4=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Dear community,

I am writing this list to bitcoin-dev mail list, but to prevent potential censorship I am sending CC to lightning-dev mail list, in order to leave the current moderator(s) without an option not to publish the letter and not to leave the topic ?under the cover? (sorry Lightning friends for spamming your list with this off-topic).

A day before yesterday I sent a post to bitcoin-dev referencing the publication of the new Bitcoin scalability and privacy protocol, which had already received a broad reaction across the bitcoin community with literally no critical/negative responses after ~25k of reads [1]. I am not the first-time writer to the mail list and had developed things like RGB smart contracts [2], rust lightning implementation named LNP [3], multiple bitcoin libraries and software [4], [5], during three years was a main contributor to rust-bitcoin [6] etc, etc. The post was clearly not spam and received support from known community members like Giacomo Zucco [7]. Bryan Bishop knows me since 2019 when I was presenting Storm protocol on the stage on Scaling Bitcoin in Tel Aviv - and he was writing a transcript of it [8]. Thus, I am not a random unknown guy or a known spammer - and the post can be easily checked for not containing any scam promotion.

Nevertheless, I next day I see other e-mails getting released to bitcoin-dev, while mine - was not. It is not a problem, but since we already had an incident in the past where Bryan reported the failure of his software, me and my colleagues from LNP/BP Standards Association started asking questions about whether this post ever got to Bryan.

What happened next was very unexpected. I am giving the core of the conversation over Twitter after in Annex A - with the purpose to showcase the problem I?d like to address in this e-mail. From the discussion, it is clear that bitcoin-dev mail list lacks clear explicit moderation (or peer-review) policies, which must be applied on a non-selective basis. Also, Bryan Bishop, as the current moderator, had abused his powers in achieving his agenda based on personal likes or dislikes. The conversation went nowhere, and the post got published only after a requirement from Peter Todd [9].

In this regard, I?d like to propose the following:

- The bitcoin-dev mail list must have a clear moderation (or pre-publication peer-review policy). It can be proposed and discussed in this mail list and, upon agreement, must become public and obligatory.
- Bryan Bishop, who was acting for a long time as moderator, must be appreciated for many years of unpaid work, and replaced with the new moderator who should be selected from a list of potential candidates (again in this mail list) using the criteria ?least votes against?.
- The role of the moderator(s) must be purely executive of the policies, without any personal preferences.
- A dedicated mail list should be created (?bitcoin-dev-unmoderated?) which will publish all submissions without moderation. It may contain spam and only people interested in the auditing bitcoin-dev main mal list non-censorship will be reading it. However, if they will notice that some non-spam e-mails were censored, they can announce that publicly. In this case, the failing moderator(s) should be removed and replaced.
- The incentive to work as a moderator should be reputation-based.

With that, I rest my case.

Kind regards,

Maxim Orlovsky

[1]:https://twitter.com/lnp_bp/status/1664329393131364353?s=61&t=9A8uvggqKVKV3sT4HPlQyg

[2]:https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2023-April/021554.html

[3]:https://github.com/LNP-WG

[4]:https://github.com/BP-WG

[5]:https://github.com/mycitadel

[6]:https://github.com/rust-bitcoin/rust-bitcoin/graphs/contributors?from=2018-12-31&to=2022-04-12&type=c

[7]:https://twitter.com/giacomozucco/status/1664515543154544645?s=61&t=9A8uvggqKVKV3sT4HPlQygandhttps://twitter.com/giacomozucco/status/1664731504923095041?s=61&t=9A8uvggqKVKV3sT4HPlQyg

[8]:https://scalingbitcoin.org/transcript/telaviv2019/wip-storm-layer-2-3-storage-and-messaging

[9]:https://twitter.com/peterktodd/status/1664742651835367424?s=61&t=9A8uvggqKVKV3sT4HPlQyg

Annex A:

- @kanzure just like to check that our submission to bitcoin-dev hasn?t got to spam <https://twitter.com/lnp_bp/status/1664649328349069320?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- A few mods are reviewing it <https://twitter.com/kanzure/status/1664680893548572677?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Oh, so a peer review is required to get to bitcoin-dev mail list? Never read about that requirement anywhere <https://twitter.com/lnp_bp/status/1664695061462777858?s=61&t=9A8uvggqKVKV3sT4HPlQyg>. Seems like bitcoin-dev mail list requirements are now specific to the author :) <https://twitter.com/dr_orlovsky/status/1664695668475142144?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Not the greatest email to pull this over. I'll double check but pretty sure the antagonization is boring me. <https://twitter.com/kanzure/status/1664705038315409420?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Not sure I understand what you are saying. Can you please clarify? <https://twitter.com/dr_orlovsky/status/1664705280393859103?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- You are boring me and these antics don't make me want to go click approve on your email. <https://twitter.com/kanzure/status/1664705509147004946?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Are you the person to approve emails for it? <https://twitter.com/phyrooo/status/1664732932068589568?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Yes <https://twitter.com/kanzure/status/1664733107096899585?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- It appears that people boring @kanzure is going through a dedicated review procedure on bitcoin-dev mail list. Good moderation! Very clear policy! <https://twitter.com/dr_orlovsky/status/1664706165790461959?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- What are you even doing. How does this behavior suppose to get people to help you? <https://twitter.com/kanzure/status/1664706931083329536?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- I am not expecting you to help me - and never asked. I expect you to openly declare moderation (or peer review) policy and follow it. <https://twitter.com/dr_orlovsky/status/1664719295123685381?s=61&t=9A8uvggqKVKV3sT4HPlQyg> Since ?if you get me bored I will not click an accept button? is not a moderation policy which I expect from bitcoin-dev mail list. Probably not just me. <https://twitter.com/dr_orlovsky/status/1664719786633310209?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Yeah I mean I don't think these tweets are likely to get me to enthusiastically resolve your problem... I dunno man. What's even going on here. <https://twitter.com/kanzure/status/1664735139065208833?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
- Bitcoin mail list clearly lacks explicit moderation policy. The same mistake like with rust-bitcoin 1+ yrs ago. I am fine with peer review. Moderation. But only explicit - not just ?the way I (dis)like this guy? <https://twitter.com/dr_orlovsky/status/1664736404931321859?s=61&t=9A8uvggqKVKV3sT4HPlQyg>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230602/f0fd6794/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 97, Issue 3
******************************************
