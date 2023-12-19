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
      (Nagaev Boris)


----------------------------------------------------------------------

Message: 1
Date: Mon, 18 Dec 2023 21:45:45 -0300
From: Nagaev Boris <bnagaev@gmail.com>
To: yurisvb@pm.me
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID:
	<CAFC_Vt644Wqn7EcvoZwFscPMov8T5kO9ss_QRgNgVNir-bBA0Q@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

On Mon, Dec 18, 2023 at 7:44?PM <yurisvb@pm.me> wrote:
>
> I beg to disagree: key owner broadcasts first bundle (let's call it this way) so that it is on any miner's best interest to include said bundle on their's attempted coinbase because they know if they don't any other competing miner will in the next block.

What if an attacker broadcasts the first bundle? He spent a lot of
time cracking the hash which is the part of the address in the
proposed scheme. Then he cracked the second layer of hashing to have
both hashes ready. If the utxo has enough sats, the attack is
economically viable.


-- 
Best regards,
Boris Nagaev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 103, Issue 15
********************************************
