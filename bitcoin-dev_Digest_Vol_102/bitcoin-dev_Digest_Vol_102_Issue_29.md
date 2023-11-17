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

   1. Re: Purely off-chain coin colouring (Anthony Towns)


----------------------------------------------------------------------

Message: 1
Date: Fri, 17 Nov 2023 17:58:34 +1000
From: Anthony Towns <aj@erisian.com.au>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Cc: Casey Rodarmor <casey@rodarmor.com>
Subject: Re: [bitcoin-dev] Purely off-chain coin colouring
Message-ID: <ZVcdKupXU+wjawRI@erisian.com.au>
Content-Type: text/plain; charset=us-ascii

On Sat, Feb 04, 2023 at 08:38:54PM +1000, Anthony Towns via bitcoin-dev wrote:
> > AJ Towns writes:
> > > I think, however, that you can move inscriptions entirely off-chain. I
> > > wrote a little on this idea on twitter already [1], but after a bit more
> > > thought, I think pushing things even further off-chain would be plausible.

Oh, you could also do inscriptions minimally on-chain. Rather than
posting the inscription on-chain per se, take a hash of the data you
want to inscribe, and then do a sign-to-contract commitment of that
hash.

That reduces your on-chain overhead for creating an inscription to
approximately zero (you're just signing a transaction), so can be much
cheaper, and also can't be blocked or front run by mempool observers. But
obviously means the inscription must be announced off-chain for anyone to
know about it. Of course, that could be seen as a benefit: you can now
have a private inscription, that's still transferable via the regular
ordinals protocol.

OTOH, there's no way to definitvely say "this tx is the Nth inscription
that matches pattern X", as there may be many earlier sign-to-contract
inscriptions that match that pattern that simply haven't been publicly
revealed yet. So that wouldn't be compatible with "inscription numbers"
or "first X inscripts count as minting token Y".

If you go one step further and allow the sign-to-contract to be the
merkle root of many inscriptions, then you've effectively reinvented
timestamping. (You can't outsource inscriptions to a timestamp server,
because you'd fail to own the ordinal that indicates "ownership" of
the inscription, however you could provide timestamping services as a
value-add while creating inscriptions)

Sign-to-contract looks like:

 * generate a secret random nonce r0
 * calculate the public version R0 = r0*G
 * calculate a derived nonce r = r0 + SHA256(R0, data), where "data"
   is what you want to commit to
 * generate your signature using public nonce R=r*G as usual

To be able to verify sign-to-contract, you reveal R0 and data, and the
verification is just checking that R=R0+SHA256(R0, data)*G. That works
with both ecdsa and schnorr signatures, so doesn't require any advance
preparation.

While it's not widely supported, sign-to-contract is a useful feature
in general for anti-exfil (eg, preventing a malicious hardware wallet
from leaking your secret key when signing txs).

Some references:

 https://www.reddit.com/r/Bitcoin/comments/d3lffo/technical_paytocontract_and_signtocontract/
 https://github.com/BlockstreamResearch/secp256k1-zkp/blob/d22774e248c703a191049b78f8d04f37d6fcfa05/include/secp256k1_ecdsa_s2c.h
 https://github.com/bitcoin-core/secp256k1/pull/1140
 https://wally.readthedocs.io/en/release_0.8.9/anti_exfil_protocol/
 https://github.com/opentimestamps/python-opentimestamps/pull/14

Cheers,
aj


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 102, Issue 29
********************************************
