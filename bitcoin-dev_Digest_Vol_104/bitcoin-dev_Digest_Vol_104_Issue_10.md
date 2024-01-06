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

   1. Re: Lamport scheme (not signature) to economize on L1
      (yurisvb@pm.me)


----------------------------------------------------------------------

Message: 1
Date: Fri, 05 Jan 2024 18:22:44 +0000
From: yurisvb@pm.me
To: "David A. Harding" <dave@dtrt.org>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<ek_yawNCaDmqpsW5IjJXdxR8w1UOnydBnT3XIi_WtIjPXdN7Ag_gdDV4bDQ66--rwPmdgtE_ZiU2ahS_tAaGJkDwt25Yd12o_OulAwOubDI=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Addendum:

Tomorrow I'll host a Twitter Spaces on this topic:
https://twitter.com/yurivillasboas/status/1743305920937963696
You are all welcome to join!

YSVB

Sent with Proton Mail secure email.

On Friday, January 5th, 2024 at 7:02 PM, yurisvb@pm.me <yurisvb@pm.me> wrote:


> Dear friends and colleagues,
> 

> I believe this current version of the protocol and its documentation, now including a diagram answers the questions raised so far:
> 

> https://github.com/Yuri-SVB/LVBsig/blob/main/docs/white_paper.md
> 

> All in all, in addition to the plain transaction TXi, only 36 bytes are needed to authenticate it. The number falls to 16 in case of address (address chain) is reused, because change address coincides with Lamport-scheme pre-image.
> 

> YSVB.
> 

> Sent with Proton Mail secure email.
> 

> 

> On Monday, January 1st, 2024 at 11:17 AM, yurisvb@pm.me yurisvb@pm.me wrote:
> 

> 

> 

> > Hello, Dave,
> > 

> > I'm afraid I didn't understand your objection. It would be great to have a direct, real-time conversation with you, if you have the availability. Be my guest to DM me for that.
> > 

> > Though this is to be confirmed, I suspect my proposed scheme can be implemented with available, existing Bitcoin infrastructure. As far as my limited knowledge goes, the trickiest part would be to have miners agree that pre-image of hash of a transaction, in a subsequent block is acceptable authentication. As for the commitment, it could be implemented as ordinary smart contracts are, and its size doesn't matter because in the normal use case, it is not mined.
> > 

> > To be clear: The only component that is mined other than addresses and the plaintext transactions would be one hash, between 16 and 20 bytes. From the No-Free-Lunch Principle, the cost for it is that transaction takes a few blocks, instead of just one to be validated.
> > 

> > YSVB
> > 

> > Sent with Proton Mail secure email.
> > 

> > On Sunday, December 31st, 2023 at 8:33 PM, David A. Harding dave@dtrt.org wrote:
> > 

> > > Hi Yuri,
> > > 

> > > I think it's worth noting that for transactions with an equal number of
> > > P2TR keypath spends (inputs) and P2TR outputs, the amount of space used
> > > in a transaction by the serialization of the signature itself (16 vbytes
> > > per input) ranges from a bit over 14% of transaction size (1-input,
> > > 1-output) to a bit less than 16% (10,000-in, 10,000-out; a ~1 MvB tx).
> > > I infer that to mean that the absolute best a signature replacement
> > > scheme can do is free up 16% of block space.
> > > 

> > > An extra 16% of block space is significant, but the advantage of that
> > > savings needs to be compared to the challenge of creating a highly peer
> > > reviewed implementation of the new signature scheme and then convincing
> > > a very large number of Bitcoin users to accept it. A soft fork proposal
> > > that introduces new-to-Bitcoin cryptography (such as a different hash
> > > function) will likely need to be studied for a prolonged period by many
> > > experts before Bitcoin users become confident enough in it to trust
> > > their bitcoins to it. A hard fork proposal has the same challenges as a
> > > soft fork, plus likely a large delay before it can go into effect, and
> > > it also needs to be weighed against the much easier process it would be
> > > for experts and users to review a hard fork that increased block
> > > capacity by 16% directly.
> > > 

> > > I haven't fully studied your proposal (as I understand you're working on
> > > an improved version), but I wanted to put my gut feeling about it into
> > > words to offer feedback (hopefully of the constructive kind): I think
> > > the savings in block space might not be worth the cost in expert review
> > > and user consensus building.
> > > 

> > > That said, I love innovative ideas about Bitcoin and this is one I will
> > > remember. If you continue working on it, I very much look forward to
> > > seeing what you come up with. If you don't continue working on it, I
> > > believe you're likely to think of something else that will be just as
> > > exciting, if not more so.
> > > 

> > > Thanks for innovating!,
> > > 

> > > -Dave
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240105/012dba87/attachment-0001.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240105/012dba87/attachment-0001.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 10
********************************************
