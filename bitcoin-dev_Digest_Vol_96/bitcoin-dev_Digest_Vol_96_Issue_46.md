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

   1. Re: Responsible disclosures and Bitcoin development (alicexbt)


----------------------------------------------------------------------

Message: 1
Date: Tue, 16 May 2023 22:39:53 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Michael Folkson <michaelfolkson@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Responsible disclosures and Bitcoin
	development
Message-ID:
	<k95MsgwJmus2shEQ3XcON4sPN2jpvN0NOiVuIUk27H-gQno3iH4XEMH_nyaKzUuCM8KKt63qM8cph6Eai7fCgWRxfTdYnKdfVw0i2NZTTf0=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Hi Michael,

A disagreement and some thoughts already shared in an email although its not clear to some "open source" devs:

Impact of this vulnerability:

- Denial of Service
- Stale blocks affecting mining pool revenue
Why it should have been reported privately to security@bitcoincore.org, even if initially found affecting only debug build?

Example: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3129

CVE is a different process and I am aware of it. It would be good for certain developers in the core team to reflect on their own approach to security, regardless of whether their work receives CVE recognition or not.

/dev/fd0
floppy disk guy

Sent with [Proton Mail](https://proton.me/) secure email.

------- Original Message -------
On Friday, May 12th, 2023 at 1:14 AM, Michael Folkson <michaelfolkson@protonmail.com> wrote:

> Hi alicexbt
>
> The vulnerability reporting process requires communication and resolution via a small group of individuals [0] rather than through open collaboration between any contributors on the repo. There are clearly examples where the process is critically needed, the most obvious past example being the 2018 inflation bug [1]. However, it doesn't scale for all bug reports and investigations to go through this tiny funnel. For an issue that isn't going to result in loss of onchain funds and doesn't seem to present a systemic issue (e.g. network DoS attack, inflation bug) I'm of the view that opening a public issue was appropriate in this case especially as the issue initially assumed it was only impacting nodes running in debug mode (not a mode a node in production is likely to be running in).
>
> An interesting question though and I'm certainly happy to be corrected by those who have been investigating the issue. Some delicate trade-offs involved including understanding and resolving the issue faster through wider collaboration versus keeping knowledge of the issue within a smaller group.
>
> Thanks
> Michael
>
> [0]: https://github.com/bitcoin/bitcoin/blob/master/SECURITY.md
> [1]: https://bitcoincore.org/en/2018/09/20/notice/
>
> --
> Michael Folkson
> Email: michaelfolkson at [protonmail.com](http://protonmail.com/)
> GPG: A2CF5D71603C92010659818D2A75D601B23FEE0F
>
> Learn about Bitcoin: https://www.youtube.com/@portofbitcoin
>
> ------- Original Message -------
> On Tuesday, May 9th, 2023 at 03:47, alicexbt via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> Hi Bitcoin Developers,
>>
>> There is an open issue in bitcoin core repository which was created last week: https://github.com/bitcoin/bitcoin/issues/27586
>>
>> I think this should have been reported privately as vulnerability instead of creating a GitHub issue even if it worked only in debug mode. Some users in the comments have also experienced similar issues without debug build used for bitcoind. I have not noticed any decline in the number of listening nodes on bitnodes.io in last 24 hours so I am assuming this is not an issue with majority of bitcoin core nodes. However, things could have been worse and there is nothing wrong in reporting something privately if there is even 1% possibility of it being a vulnerability. I had recently reported something to LND security team based on a closed issue on GitHub which eventually was not considered a vulnerability: https://github.com/lightningnetwork/lnd/issues/7449
>>
>> In the CPU usage issue, maybe the users can run bitcoind with bigger mempool or try other things shared in the issue by everyone.
>>
>> This isn't the first time either when vulnerability was reported publicly: https://gist.github.com/chjj/4ff628f3a0d42823a90edf47340f0db9 and this was even exploited on mainnet which affected some projects.
>>
>> This email is just a request to consider the impact of any vulnerability if gets exploited could affect lot of things. Even the projects with no financial activity involved follow better practices.
>>
>> /dev/fd0
>> floppy disk guy
>>
>> Sent with [Proton Mail](https://proton.me/) secure email.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230516/f9af5f1d/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 46
*******************************************
