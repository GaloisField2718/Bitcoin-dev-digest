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

   1. MuSig2 derivation, descriptor, and PSBT field BIPs (Ava Chow)
   2. Re: MuSig2 derivation, descriptor, and PSBT field BIPs
      (Christopher Allen)
   3. Re: [BUG]: Bitcoin blockspace price discrimination put simple
      transactions at disadvantage (Greg Tonoski)


----------------------------------------------------------------------

Message: 1
Date: Mon, 15 Jan 2024 23:29:46 +0000
From: Ava Chow <lists@achow101.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>, bitcoindev@groups.io
Subject: [bitcoin-dev] MuSig2 derivation, descriptor, and PSBT field
	BIPs
Message-ID: <5d299fc4-8809-4f32-a9b8-17e353d6ff30@achow101.com>
Content-Type: text/plain; charset=utf-8

Hi All,

In October I sent the MuSig2 descriptor and PSBT field BIPs to the list. 
Since then, I've made a few changes to the BIPs and am looking for 
feedback on these.

The most significant change is the addition of third BIP which describes 
how the synthetic xpubs are constructed and derived. This is split from 
the descriptors BIP as I felt that the PSBT fields BIP needed to 
reference this process too, and referencing the descriptors BIP for that 
seemed a bit odd.

Otherwise, the descriptors BIP is unchanged, although I am open to 
Salvatore's suggestion of dropping the ranged derivation within the 
expression and only allow ranged derivation of the aggregate pubkey itself.

I've also made a change to the PSBT fields BIP where the aggregate 
pubkey is included as a plain pubkey rather than as xonly. I think this 
change is necessary for to make discovering derived keys easier. The 
derivation paths for derived keys contain the fingerprint of the parent 
(i.e. the aggregate pubkey) and the fingerprint requires the evenness 
bit to be serialized. So the aggregate pubkey in the PSBT fields need to 
contain that evenness information in order for something looking at only 
the PSBT to be able to determine whether a key is derived from an 
aggregate pubkey also specified in the PSBT.

The full text of the BIPs can be found at the following:
* Derivation: 
https://github.com/achow101/bips/blob/musig2/bip-musig2-derivation.mediawiki
* Descriptors: 
https://github.com/achow101/bips/blob/musig2/bip-musig2-descriptors.mediawiki
* PSBT: 
https://github.com/achow101/bips/blob/musig2/bip-musig2-psbt.mediawiki

Thanks,
Ava Chow



------------------------------

Message: 2
Date: Tue, 16 Jan 2024 00:18:26 -0800
From: Christopher Allen <ChristopherA@lifewithalacrity.com>
To: Ava Chow <lists@achow101.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: bitcoindev@groups.io
Subject: Re: [bitcoin-dev] MuSig2 derivation, descriptor, and PSBT
	field BIPs
Message-ID:
	<CACrqygDY0p-trbHGyhg0_uyViyryyJqO-CkOS6+tknTUG05Wew@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Mon, Jan 15, 2024 at 4:28?PM Ava Chow via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> I've also made a change to the PSBT fields BIP where the aggregate
> pubkey is included as a plain pubkey rather than as xonly. I think this
> change is necessary for to make discovering derived keys easier. The
> derivation paths for derived keys contain the fingerprint of the parent
> (i.e. the aggregate pubkey) and the fingerprint requires the evenness
> bit to be serialized. So the aggregate pubkey in the PSBT fields need to
> contain that evenness information in order for something looking at only
> the PSBT to be able to determine whether a key is derived from an
> aggregate pubkey also specified in the PSBT.
>

The topic of some challenges in using x-only pubkeys with FROST recently
came up in a conversation that I didn't completely understand. It sounds
like it may be related to this issue with MuSig2.

What are the gotcha's in x-only keys with these multisig protocols? Can you
explain a little more? Any other particular things do we need to be careful
about with x-only pubkeys? I had mistakenly assumed the technique was just
a useful trick, not that it might cause some problems in higher level
protocols.

Thanks!

-- Christopher Allen
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20240116/b87c4d6a/attachment-0001.html>

------------------------------

Message: 3
Date: Tue, 16 Jan 2024 11:40:48 +0100
From: Greg Tonoski <gregtonoski@gmail.com>
To: vjudeu@gazeta.pl
Cc: "bitcoin-dev@lists.linuxfoundation.org"
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] [BUG]: Bitcoin blockspace price
	discrimination put simple transactions at disadvantage
Message-ID:
	<CAMHHROzbQQ1MeegD5_jO8gkyXKLKH+wvgjPKVANYEG=0NT58jQ@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Wed, Dec 27, 2023 at 10:43?PM <vjudeu@gazeta.pl> wrote:
>
> I think it should be fixed. Because now, sending coins into P2WPKH is cheaper than sending them to P2TR, even though finally, when those coins are spent, the blockspace usage is cheaper for Taproot (when you spend by key) than for Segwit, because public key hash is not stored anywhere. But of course, because the cost is splitted between sender and spender, it is more profitable to send to P2WPKH, and spend from P2TR.

The difference between P2WPKH and P2TR is a different topic, I think.
A single bloated transaction would be treated with higher priority
than a number of simple transactions of the same total size and fee -
irrespectively of P2WPKH and P2TR type.


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 16
********************************************
