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

   1. Re: Introducing a version field to BIP39 mnemonic	phrases
      (Pavol Rusnak)
   2. Re: Introducing a version field to BIP39 mnemonic	phrases (Leslie)


----------------------------------------------------------------------

Message: 1
Date: Sat, 13 Jan 2024 11:31:35 -0500
From: Pavol Rusnak <stick@satoshilabs.com>
To: Leslie <0300dbdd1b@protonmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Introducing a version field to BIP39
	mnemonic	phrases
Message-ID:
	<CAF90Av=HqhdOfLpY1Pz8J2N7f_A+L_LDcni2Rx59Z5rNpsLksQ@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Sat, 13 Jan 2024 at 10:53, Leslie <0300dbdd1b@protonmail.com> wrote:

> Developments like aezeed[1] or Electrum V2[2] also demonstrate that the
> standard BIP39 entropy might not always suffice for specific applications,
> leading to alternative standards being developed.
> This reality underscores the need to consider ways to enhance the existing
> system to more effectively accommodate these evolving requirements.
>

It is a very unrealistic that any kind of seed standard with extra metadata
will cover all possible future usecases.
Therefore new standards will always keep emerging.

LND coming up with a new aezeed standard and not using Electrum v2 are good
example of this.

For LND, the documentation[1] tells you to convert the seed using a website
(not great) AND on top of that you also need to provide the derivation path
for the funds(!) because the aezeed version is not used to encode the
derivation path used.
Probably the LND folks also realized it is not feasible to regenerate the
seed (and bother user with the backup)
every time wallet starts to use the new address format.

On the other side, CLN is perfectly fine with using BIP39, making it very
easy to recover CLN funds in any BIP39 compatible wallet.

[1]
https://www.lightningnode.info/technicals/restorelndonchainfundsinelectrum

In summary, while I hold deep respect for the fundamental principles of
> BIP39, I firmly believe that exploring the potential of versioned mnemonics
> can effectively address the dynamic nature of user practices and
> application demands, all while preserving the core strengths of the BIP39
> standard.
>

>From where I stand, adding metadata to seed is a fool's errand.
Every year, new people coming to Bitcoin try it and fail.

Everything said, feel free to experiment, but your experiments should be
different standard than BIP39.
I would like to keep the BIP39 base entropy layer "ossified".
Moreover, it would be best if your experiments do not interfere with BIP39
to avoid confusion.
That is, your seeds should not be of lengths 12, 15, 18, 21 or 24 words.

-- 
Best Regards / S pozdravom,

Pavol "Stick" Rusnak
Co-Founder, SatoshiLabs
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240113/0f18e06c/attachment-0001.html>

------------------------------

Message: 2
Date: Sat, 13 Jan 2024 17:06:31 +0000
From: Leslie <0300dbdd1b@protonmail.com>
To: Pavol Rusnak <stick@satoshilabs.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Introducing a version field to BIP39
	mnemonic	phrases
Message-ID:
	<7jxjf0EXqj5cicpawdiNNdEvwlvS9L_beURqIICH64qOB57MP3NJsryIXg2FLV1hBREa2IbEZB1sKV_aWg97QHfEG_hM54dXeQ_FwTOShjY=@protonmail.com>
	
Content-Type: text/plain; charset="utf-8"

Dear Pavol,

>It is a very unrealistic that any kind of seed standard with extra metadata
>will cover all possible future usecases.
>Therefore new standards will always keep emerging.
>

Indeed, this proposal does not aim to cover *all* usecases, but rather to provide a backward-compatible way to introduce new features (such as wallet birthdate, for example).

>From where I stand, adding metadata to seed is a fool's errand.
>Every year, new people coming to Bitcoin try it and fail.
>

Could you provide references to such attempts?
I'd like to take a look at these proposal and find out why it did fail.

>Everything said, feel free to experiment, but your experiments should be
>different standard than BIP39.
>I would like to keep the BIP39 base entropy layer "ossified".
>Moreover, it would be best if your experiments do not interfere with BIP39
>to avoid confusion.
>That is, your seeds should not be of lengths 12, 15, 18, 21 or 24 words.
>

Considering the fact that my proposal aims to be compatible with BIP39, I'm afraid that this wont be possible for obvious reasons.
Fortunately, the 24-bit general purpose field provide space to prevent false positive[1], so it wont interfere with existing BIP39 mnemonics.
As for the mnemonic phrase length, to ensure compatibility with BIP39 (which is the primary goal), the mnemonic phrases will likely remain within the range of 12 to 24 words.

References:
[1] (https://github.com/lukechilds/bip39-versioned?tab=readme-ov-file#false-positives)

Best Regards,
Leslie
On Saturday, January 13th, 2024 at 17:31, Pavol Rusnak <stick@satoshilabs.com> wrote:

> On Sat, 13 Jan 2024 at 10:53, Leslie <0300dbdd1b@protonmail.com> wrote:
>
>> Developments like aezeed[1] or Electrum V2[2] also demonstrate that the standard BIP39 entropy might not always suffice for specific applications, leading to alternative standards being developed.
>> This reality underscores the need to consider ways to enhance the existing system to more effectively accommodate these evolving requirements.
>
> It is a very unrealistic that any kind of seed standard with extra metadata will cover all possible future usecases.
> Therefore new standards will always keep emerging.
>
> LND coming up with a new aezeed standard and not using Electrum v2 are good example of this.
>
> For LND, the documentation[1] tells you to convert the seed using a website (not great) AND on top of that you also need to provide the derivation path for the funds(!) because the aezeed version is not used to encode the derivation path used.
> Probably the LND folks also realized it is not feasible to regenerate the seed (and bother user with the backup)
> every time wallet starts to use the new address format.
>
> On the other side, CLN is perfectly fine with using BIP39, making it very easy to recover CLN funds in any BIP39 compatible wallet.
>
> [1] https://www.lightningnode.info/technicals/restorelndonchainfundsinelectrum
>
>> In summary, while I hold deep respect for the fundamental principles of BIP39, I firmly believe that exploring the potential of versioned mnemonics can effectively address the dynamic nature of user practices and application demands, all while preserving the core strengths of the BIP39 standard.
>
> From where I stand, adding metadata to seed is a fool's errand.
> Every year, new people coming to Bitcoin try it and fail.
>
> Everything said, feel free to experiment, but your experiments should be different standard than BIP39.
> I would like to keep the BIP39 base entropy layer "ossified".
> Moreover, it would be best if your experiments do not interfere with BIP39 to avoid confusion.
> That is, your seeds should not be of lengths 12, 15, 18, 21 or 24 words.
> --
>
> Best Regards / S pozdravom,
>
> Pavol "Stick" Rusnak
> Co-Founder, SatoshiLabs
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240113/10e6a1ec/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 14
********************************************
