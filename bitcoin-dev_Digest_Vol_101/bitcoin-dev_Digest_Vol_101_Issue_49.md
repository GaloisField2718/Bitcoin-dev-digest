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

   1. Re: Examining ScriptPubkeys in Bitcoin Script (James O'Beirne)


----------------------------------------------------------------------

Message: 1
Date: Mon, 30 Oct 2023 12:20:32 -0400
From: "James O'Beirne" <james.obeirne@gmail.com>
To: Rusty Russell <rusty@rustcorp.com.au>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Examining ScriptPubkeys in Bitcoin Script
Message-ID:
	<CAPfvXfK7a5To=-n+TOY34KZn2T=Dkf5M1S3eFCNmug8xuE9rTw@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

On Sat, Oct 28, 2023 at 12:51?AM Rusty Russell via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> But AFAICT there are multiple perfectly reasonable variants of vaults,
> too.  One would be:
>
> 1. master key can do anything
> 2. OR normal key can send back to vault addr without delay
> 3. OR normal key can do anything else after a delay.
>
> Another would be:
> 1. normal key can send to P2WPKH(master)
> 2. OR normal key can send to P2WPKH(normal key) after a delay.
>

I'm confused by what you mean here. I'm pretty sure that BIP-345 VAULT
handles the cases that you're outlining, though I don't understand your
terminology -- "master" vs. "normal", and why we are caring about P2WPKH
vs. anything else. Using the OP_VAULT* codes can be done in an arbitrary
arrangement of tapleaves, facilitating any number of vaultish spending
conditions, alongside other non-VAULT leaves.

Well, I found the vault BIP really hard to understand.  I think it wants
> to be a new address format, not script opcodes.
>

Again confused here. This is like saying "CHECKLOCKTIMEVERIFY wants to be a
new address format, not a script opcode."

That said, I'm sure some VAULT patterns could be abstracted into the
miniscript/descriptor layer to good effect.
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20231030/4f761a74/attachment-0001.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 101, Issue 49
********************************************
