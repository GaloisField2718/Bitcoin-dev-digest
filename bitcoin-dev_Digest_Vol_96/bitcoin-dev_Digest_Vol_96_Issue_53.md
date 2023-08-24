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

   1. Re: Ark: An Alternative Privacy-preserving Second	Layer
      Solution (ZmnSCPxj)
   2. Coinjoin with less steps using ALL|ANYONECANPAY (alicexbt)
   3. Re: Responsible disclosures and Bitcoin development (alicexbt)
   4. Re: Coinjoin with less steps using ALL|ANYONECANPAY (Ben Carman)


----------------------------------------------------------------------

Message: 1
Date: Mon, 22 May 2023 13:03:00 +0000
From: ZmnSCPxj <ZmnSCPxj@protonmail.com>
To: Burak Keceli <burak@buraks.blog>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Ark: An Alternative Privacy-preserving
	Second	Layer Solution
Message-ID:
	<94d_XdPjU7_erTbusSTbsSWNNL3Wgx61scF_EknkwXp_ywmCLJ5jc13RVlTF_gpdZG5scUU_4z27qPykXQjLESE1m06CEJbsCha13QdqeFY=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Good morning Burak,

I have not gone through the deep dive fully yet, but I find myself confused about this particular claim:

> A pool transaction can be double-spent by the Ark service provider while it remains in the mempool. However, in the meantime, the recipient can pay a lightning invoice with their incoming zero-conf vTXOs, so it?s a footgun for the service operator to double-spend in this case.?

Given that you make this claim:

> ASPs on Ark are both (1) liquidity providers, (2) blinded coinjoin coordinators, and (3) Lightning service providers. ASPs main job is to create rapid, blinded coinjoin sessions every five seconds, also known as pools.

As the access to Lightning is also by the (same?) ASP, it seems to me that the ASP will simply fail to forward the payment on the broader Lightning network after it has replaced the in-mempool transaction, preventing recipients from actually being able to rely on any received funds existing until the next pool transaction is confirmed.

Even if the Lightning access is somehow different from the ASP you are receiving funds on, one ASP cannot prove that another ASP is not its sockpuppet except via some expensive process (i.e. locking funds or doing proof-of-work).

Regards,
ZmnSCPxj



------------------------------

Message: 2
Date: Mon, 22 May 2023 12:51:22 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Coinjoin with less steps using ALL|ANYONECANPAY
Message-ID:
	<EWAXAmgFlZ8XQJOYO8VTH7Zj0tTAftwy-ylaGvf3Giealz1FFb97CbcxjP0q-Zu85XoAzOG0ivdYIKa_kG77ooHqBvCP7YOZOkb6yHmX75s=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Bitcoin Developers,

I recently experimented with different sighash flags, PSBTs and realized ALL|ANYONECANPAY could be used to reduce some steps in coinjoin.

Steps:

- Register outputs.
- One user creates a signed PSBT with 1 input, all registered outputs and ALL|ANYONECANPAY sighash flag. Other participants keep adding their inputs to PSBT.
- Finalize and broadcast the transaction.

Proof of Concept (Aice and Bob):?https://gitlab.com/-/snippets/2542297

Tx: https://mempool.space/testnet/tx/c6dd626591dca7e25bbd516f01b23171eb0f2b623471fcf8e073c87c1179c492

I plan to use this in joinstr if there are no major drawbacks and it can even be implemented by other coinjoin implementations. 

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.


------------------------------

Message: 3
Date: Mon, 22 May 2023 12:56:13 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Michael Folkson <michaelfolkson@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Responsible disclosures and Bitcoin
	development
Message-ID:
	<yCRGs9ve5782SDi1mdGMA1x1jOeJzBkfsWJxtFD3gcrPHI7WW2Ah3Qn9_Z1f17pGFAfC4DIx8fnLUMggrRdq0kfYRlJxpgLt_qJ7wSVC9t0=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Michael,

> Now that's not to say you may not have a point about better documentation and guidance on what should go through the vulnerability reporting process and what shouldn't.

Yes, this can be improved.

> Or even that this particular issue could ultimately end up being classed a CVE.

It has been assigned CVE-2023-33297


/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Wednesday, May 17th, 2023 at 6:14 PM, Michael Folkson <michaelfolkson@protonmail.com> wrote:


> Hi alicexbt
> 
> "Open source" has the word "open" in it. Pushing everything into closed, private channels of communication and select groups of individuals is what I've been trying to push back upon. As I said in my initial response "it doesn't scale for all bug reports and investigations to go through this tiny funnel" though "there are clearly examples where the process is critically needed".
> 
> 
> Now that's not to say you may not have a point about better documentation and guidance on what should go through the vulnerability reporting process and what shouldn't. Or even that this particular issue could ultimately end up being classed a CVE. But rather than merely complaining and putting "open source" into quote marks perhaps suggest what class of bug reports should go through the tiny funnel and what shouldn't. Unless you think everything should go through the funnel in which case you are advocating for less openness whilst simultaneously complaining it isn't "open source". Square that circle.
> 
> 
> Thanks
> Michael
> 
> --
> Michael Folkson
> Email: michaelfolkson at protonmail.com
> GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
> 
> 
> Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
> 
> 
> ------- Original Message -------
> On Tuesday, May 16th, 2023 at 23:39, alicexbt <alicexbt@protonmail.com> wrote:
> 
> 
> > Hi Michael,
> > 
> > A disagreement and some thoughts already shared in an email although its not clear to some "open source" devs:
> > 
> > Impact of this vulnerability:
> > 
> > - Denial of Service
> > - Stale blocks affecting mining pool revenue
> > 
> > Why it should have been reported privately to security@bitcoincore.org, even if initially found affecting only debug build?
> > 
> > 
> > Example:?https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3129
> > 
> > 
> > CVE is a different process?and I am aware of it.?It would be good for certain developers in the core team to reflect on their own approach to security, regardless of whether their work receives CVE recognition or not.
> > 
> > /dev/fd0
> > floppy disk guy
> > 
> > 
> > Sent with Proton Mail secure email.
> > 
> > ------- Original Message -------
> > On Friday, May 12th, 2023 at 1:14 AM, Michael Folkson <michaelfolkson@protonmail.com> wrote:
> > 
> > 
> > > Hi alicexbt
> > > 
> > > The vulnerability reporting process requires communication and resolution via a small group of individuals [0] rather than through open collaboration between any contributors on the repo. There are clearly examples where the process is critically needed, the most obvious past example being the 2018 inflation bug [1]. However, it doesn't scale for all bug reports and investigations to go through this tiny funnel. For an issue that isn't going to result in loss of onchain funds and doesn't seem to present a systemic issue (e.g. network DoS attack, inflation bug) I'm of the view that opening a public issue was appropriate in this case especially as the issue initially assumed it was only impacting nodes running in debug mode (not a mode a node in production is likely to be running in).
> > > 
> > > An interesting question though and I'm certainly happy to be corrected by those who have been investigating the issue. Some delicate trade-offs involved including understanding and resolving the issue faster through wider collaboration versus keeping knowledge of the issue within a smaller group.
> > > 
> > > Thanks
> > > Michael
> > > 
> > > [0]:?https://github.com/bitcoin/bitcoin/blob/master/SECURITY.md
> > > [1]:?https://bitcoincore.org/en/2018/09/20/notice/
> > > 
> > > --
> > > Michael Folkson
> > > Email: michaelfolkson at protonmail.com
> > > GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
> > > 
> > > 
> > > Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
> > > 
> > > 
> > > ------- Original Message -------
> > > On Tuesday, May 9th, 2023 at 03:47, alicexbt via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> > > 
> > > 
> > > > Hi Bitcoin Developers,
> > > > 
> > > > There is an open issue in bitcoin core repository which was created last week:?https://github.com/bitcoin/bitcoin/issues/27586
> > > > 
> > > > I think this should have been reported privately as vulnerability instead of creating a GitHub issue even if it worked only in debug mode. Some users in the comments have also experienced similar issues without debug build used for bitcoind. I have not noticed any decline in the number of listening nodes on bitnodes.io in last 24 hours so I am assuming this is not an issue with majority of bitcoin core nodes. However, things could have been worse and there is nothing wrong in reporting something privately if there is even 1% possibility of it being a vulnerability. I had recently reported something to LND security team based on a closed issue on GitHub which eventually was not considered a vulnerability:?https://github.com/lightningnetwork/lnd/issues/7449?
> > > > 
> > > > In the CPU usage issue, maybe the users can run bitcoind with bigger mempool or try other things shared in the issue by everyone.
> > > > 
> > > > This isn't the first time either when vulnerability was reported publicly:?https://gist.github.com/chjj/4ff628f3a0d42823a90edf47340f0db9?and this was even exploited on mainnet which affected some projects.
> > > > 
> > > > 
> > > > This email is just a request to consider the impact of any vulnerability if gets exploited could affect lot of things. Even the projects with no financial activity involved follow better practices.
> > > > 
> > > > /dev/fd0
> > > > floppy disk guy?
> > > > 
> > > > 
> > > > Sent with Proton Mail secure email.


------------------------------

Message: 4
Date: Mon, 22 May 2023 22:51:49 +0000
From: Ben Carman <benthecarman@live.com>
To: alicexbt <alicexbt@protonmail.com>, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Coinjoin with less steps using
	ALL|ANYONECANPAY
Message-ID:
	<SJ1P223MB0531D7D62140F0516A25897AA1439@SJ1P223MB0531.NAMP223.PROD.OUTLOOK.COM>
	
Content-Type: text/plain; charset="iso-8859-1"

The problem with using ALL|ANYONECANPAY is that you cannot verify beforehand that the other inputs are the inputs you want added to the transaction.

Some examples of bad things that could happen:


  *   Coordinator adds its own inputs, you still get your outputs but effectively paid fees for no privacy gain
  *   The inputs added could be paying at a lower fee rate than expected, causing the tx to take longer than what you paid for
  *   Different input types or amount are added so you no longer have the same uniformity across the inputs
  *   (if you care) An input from a sanctioned address is added, causing you to get "tainted" coins.

This is the code in ln-vortex that verifies the psbt on the client side if you are curious

https://github.com/ln-vortex/ln-vortex/blob/master/client/src/main/scala/com/lnvortex/client/VortexClient.scala#L616


Best,

benthecarman

________________________________
From: bitcoin-dev <bitcoin-dev-bounces@lists.linuxfoundation.org> on behalf of alicexbt via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>
Sent: Monday, May 22, 2023 7:51 AM
To: Bitcoin Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] Coinjoin with less steps using ALL|ANYONECANPAY

Hi Bitcoin Developers,

I recently experimented with different sighash flags, PSBTs and realized ALL|ANYONECANPAY could be used to reduce some steps in coinjoin.

Steps:

- Register outputs.
- One user creates a signed PSBT with 1 input, all registered outputs and ALL|ANYONECANPAY sighash flag. Other participants keep adding their inputs to PSBT.
- Finalize and broadcast the transaction.

Proof of Concept (Aice and Bob): https://gitlab.com/-/snippets/2542297

Tx: https://mempool.space/testnet/tx/c6dd626591dca7e25bbd516f01b23171eb0f2b623471fcf8e073c87c1179c492

I plan to use this in joinstr if there are no major drawbacks and it can even be implemented by other coinjoin implementations.

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.
_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230522/9d45d394/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 53
*******************************************
