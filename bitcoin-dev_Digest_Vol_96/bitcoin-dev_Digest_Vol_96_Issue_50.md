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

   1. Re: Bitcoin Core 24.1 released (Sjors Provoost)
   2. Re: Formosa --- proposed improvement upon BIP39
      (Keagan McClelland)
   3. Re: Formosa --- proposed improvement upon BIP39 (yurisvb@pm.me)


----------------------------------------------------------------------

Message: 1
Date: Fri, 19 May 2023 13:20:26 +0200
From: Sjors Provoost <sjors@sprovoost.nl>
To: Michael Ford <fanquake@gmail.com>, Bitcoin Dev
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Bitcoin Core 24.1 released
Message-ID: <D8B548F5-9330-47EE-82E1-EAD1CFE8D835@sprovoost.nl>
Content-Type: text/plain; charset="us-ascii"

There's a typo in the tracker subdomain: trakcer.bitcoin.sprovoost.nl <http://trakcer.bitcoin.sprovoost.nl/> should be tracker.bitcoin.sprovoost.nl <http://tracker.bitcoin.sprovoost.nl/>, but I'll just add that subdomain now.

- Sjors

> Op 19 mei 2023, om 12:56 heeft Michael Ford via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> het volgende geschreven:
> 
> Bitcoin Core version 24.1 is now available from:
> 
>  <https://bitcoincore.org/bin/bitcoin-core-24.1/>
> 
> Or through BitTorrent:
> 
>  magnet:?xt=urn:btih:ebb58d7495a8aaed2f20ec4ce3e5ae27aff69529&dn=bitcoin-core-24.1&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftrakcer.bitcoin.sprovoost.nl%3A6969


-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 833 bytes
Desc: Message signed with OpenPGP
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230519/b1700b61/attachment-0001.sig>

------------------------------

Message: 2
Date: Fri, 19 May 2023 15:24:45 -0600
From: Keagan McClelland <keagan.mcclelland@gmail.com>
To: yurisvb@pm.me,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Formosa --- proposed improvement upon BIP39
Message-ID:
	<CALeFGL3ywc3YiZ-JnaShGPyaKRjDyG4gs7N3SiV4OJudFAwYcg@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Good day Yuri,

This is a very cool idea. After reviewing the repository it seems that
there lacks a BIP style specification for this, so it is possible that some
of my takeaways may not be correct but I figured I'd comment with some
observations anyway. Feel free to correct me where I've made a mistake.

I think to make an idea like this work it would be necessary for it to
"extend" BIP39 rather than "replace" it. What I mean by this is that BIP39
is heavily entrenched in the ecosystem and so in order for you to sidestep
the need to get everyone in the ecosystem to adopt a new standard, you'd
want this process to be able to output a standard BIP39 seed sequence. This
becomes even more important when you allow these different "themes" that
are mentioned later in the document. The notion of themes practically
precludes the standardization of the technique since customization really
is the antithesis of standardization.

The largest value proposition of these schemes is that it allows
significant wallet interoperability. This is achieved if process for
translating these phrases to the underlying wallet seed is deterministic.
Themes may prove to make this harder to solve. I also do not believe that
themes meaningfully increase the ability to remember the phrase: the fact
that the phrase has a valid semantic at all is a massive step up from an
undifferentiated sequence of words that is the current state of BIP39. The
benefits afforded by the themes here are little by comparison.

Overall, I think exploring this idea further is a good idea. However, there
may be concerns about whether the increased memorability is a good thing.
It would certainly make $5 wrench attacks more viable, not less. I can't
help but ask myself the question whether more Bitcoin is lost because of
seed phrases not being memorized, or because of social engineering
exercises used to scrape these phrases from the brains of users. I have a
hunch that loss is a larger problem than theft, but it is a very real
possibility that a wide deployment of this type of tech could change that.

Stay Inspired,
Keags

On Tue, May 2, 2023 at 6:05?AM Yuri S VB via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Dear colleagues,
>
> The following is a password format that improves upon BIP39 by allowing
> meaningful, themed sentences with a regular grammatical structure instead
> of semantically disconnected words, while keeping the same entropy/checksum
> and total bits/non-repeating leading digits ratios (of 32/1 and 11/4
> respectively).
>
> https://github.com/Yuri-SVB/formosa
>
> Anecdotal experiments suggest that less than one hour of moderate
> concentration is enough for long term memorization of 128 + 4 bits
> (equivalent to the 12 words standard of BIP39) if a theme of interest is
> employed.
>
> I hereby offer it to your scrutiny as a Bitcoin Improvement Proposal.
> Please don't hesitate to ask whatever issue about the project there might
> be.
>
> Faithfully yours, Yuri S VB.
>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230519/398213db/attachment.html>

------------------------------

Message: 3
Date: Fri, 19 May 2023 23:08:36 +0000
From: yurisvb@pm.me
To: Keagan McClelland <keagan.mcclelland@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Formosa --- proposed improvement upon BIP39
Message-ID:
	<MDR9A5T9YZOJI2x9N6eKk9JUmeX_bIyNf_6cqmSjWm4GOYFosnr0it3c-wBl_GbRtf4b-xTZsSuMV-xaAv2rNKVLjlkOWjNCakTwGrfu3TY=@pm.me>
	
Content-Type: text/plain; charset="utf-8"

Good day, Keagan and all!

First of all, thank you for your feedback! Yes, I made it so that Formosa does accomplish that: BIP39 is a particular case; a degenerate 'theme' in which you have sentences of just 11 bits (instead of 33 in a typical Formosa sentence), and they are made up of just one (11 bits) word with no syntactic structure. The sublist of possibilities for this one field does not impact and is not impacted by any other (because there is no other). Therefore it is rather a list (without 'sub') and it consists of the original BIP39 word list.

In addition to that, we make it so that themes (including BIP39) are convertible into one another. The conversion is straightforward: just map the words back into the array of bits that originated it and derive the new seed from it using the new theme. This is why I made sure to have sentences have a number of bits multiple of 11. Moreover, in order to enable forwards and backwards compatibility and facilitate adoption, we set the original BIP39 as standard for key derivation. Meaning: in order to derive keys from a seed, we first convert back to BIP39 and then proceed the KDF step as originally specified in BIP39. This way legacy addresses can be kept even if a user wants to choose a theme. Finally, as a bonus, one could argue that a hyper customization would allow for a(n additional, dispensable, non-critical) layer of obscurity (which, therefore, wouldn't violate Kerckhoff's principle). Example: consider, for example, that a one hyper-customized seed could be (just an extra tool) 
 more easily stenographed in human speech or written text.

I hope this answers your objections concerning loss of standardization. Thank you for bringing about the issue of coercion resistance! Here is my response to that: a user willing to avoid the additional vulnerability to coercion that an effective brain wallet would ensue could just not put up the effort to memorize the seed for long term, and just take advantage of the easier transcription and checking (ie: short-term memorization). Right now I could anticipate a response in the lines of "Such a format might as well be so much easier to long-term memorize that a user either ends up doing that accidentally, and/or the denial of that becomes less plausible.". If that is the objection, well, thank you, and, however self-serving it is my saying it, I tend to agree that that would,?in fact,?be the case. My response to it is that:

1.  knowledge-based authentication, whether or not for Bitcoin, still have some properties that possession-based authentication doesn't. Whatever master password you memorize, in whatever context, you'd better have an efficient format, with uniformly high entropy density (and even possibly checksum), and not having to resort to a silly meme about a staple, a battery and a horse.
2.  Mitigating the shortcomings of KBA can arguably be done better with 2FA, instead of PBA. Having a superior format just as beneficial as before.
3.  Once again, thank you for bringing up coercion resistance! I'd like to point out to an elephant in the room: To this day, and to the best of my knowledge there is no scheme, protocol or ceremony that simultaneously achieves self-custody and coercion resistance with?non-obscurity. IMHO this is an critical problem for various reasons and I'll be making a thread about it shortly.


Thank you again for your inputs and be my guest to further debate your points! I hope this could have been of help!

Faithfully yours, Yuri S VB.
------- Original Message -------
On Friday, May 19th, 2023 at 11:24 PM, Keagan McClelland <keagan.mcclelland@gmail.com> wrote:


> Good day Yuri,
> 

> This is a very cool idea. After reviewing the repository it seems that there lacks a BIP style specification for this, so it is possible that some of my takeaways may not be correct but I figured I'd comment with some observations anyway. Feel free to correct me where I've made a mistake.
> I think to make an idea like this work it would be necessary for it to "extend" BIP39 rather than "replace" it. What I mean by this is that BIP39 is heavily entrenched in the ecosystem and so in order for you to sidestep the need to get everyone in the ecosystem to adopt a new standard, you'd want this process to be able to output a standard BIP39 seed sequence. This becomes even more important when you allow these different "themes" that are mentioned later in the document. The notion of themes practically precludes the standardization of the technique since customization really is the antithesis of standardization.
> 

> The largest value proposition of these schemes is that it allows significant wallet interoperability. This is achieved if process for translating these phrases to the underlying wallet seed is deterministic. Themes may prove to make this harder to solve. I also do not believe that themes meaningfully increase the ability to remember the phrase: the fact that the phrase has a valid semantic at all is a massive step up from an undifferentiated sequence of words that is the current state of BIP39. The benefits afforded by the themes here are little by comparison.
> 

> Overall, I think exploring this idea further is a good idea. However, there may be concerns about whether the increased memorability is a good thing. It would certainly make $5 wrench attacks more viable, not less. I can't help but ask myself the question whether more Bitcoin is lost because of seed phrases not being memorized, or because of social engineering exercises used to scrape these phrases from the brains of users. I have a hunch that loss is a larger problem than theft, but it is a very real possibility that a wide deployment of this type of tech could change that.
> 

> Stay Inspired,
> Keags
> 

> On Tue, May 2, 2023 at 6:05?AM Yuri S VB via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 

> > Dear colleagues,
> > The following is a password format that improves upon BIP39 by allowing meaningful, themed sentences with a regular grammatical structure instead of semantically disconnected words, while keeping the same entropy/checksum and total bits/non-repeating leading digits ratios (of 32/1 and 11/4 respectively).
> > 

> > https://github.com/Yuri-SVB/formosa
> > 

> > Anecdotal experiments suggest that less than one hour of moderate concentration is enough for long term memorization of 128 + 4 bits (equivalent to the 12 words standard of BIP39) if a theme of interest is employed.
> > 

> > I hereby offer it to your scrutiny as a Bitcoin Improvement Proposal. Please don't hesitate to ask whatever issue about the project there might be.
> > 

> > Faithfully yours, Yuri S VB.
> > 

> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230519/195f8cf8/attachment.html>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: publickey - yurisvb@pm.me - 0x535F445D.asc
Type: application/pgp-keys
Size: 1678 bytes
Desc: not available
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230519/195f8cf8/attachment.bin>
-------------- next part --------------
A non-text attachment was scrubbed...
Name: signature.asc
Type: application/pgp-signature
Size: 509 bytes
Desc: OpenPGP digital signature
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230519/195f8cf8/attachment.sig>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 50
*******************************************
