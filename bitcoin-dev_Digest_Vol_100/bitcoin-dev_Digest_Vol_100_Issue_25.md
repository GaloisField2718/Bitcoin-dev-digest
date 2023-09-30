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

   1. MATT: [demo] Optimistic execution of arbitrary	programs
      (Johan Tor?s Halseth)


----------------------------------------------------------------------

Message: 1
Date: Fri, 29 Sep 2023 15:14:25 +0200
From: Johan Tor?s Halseth <johanth@gmail.com>
To: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: [bitcoin-dev] MATT: [demo] Optimistic execution of arbitrary
	programs
Message-ID:
	<CAD3i26BAoN06rR=BnvNDDBCyMkKTcROGK7zaC784XV5FWYM+5w@mail.gmail.com>
Content-Type: text/plain; charset="UTF-8"

Hi, all!

I've been working on an implementation of the original MATT challenge
protocol[0], with a detailed description of how we go from a
"high-level arbitrary program" to something that can be verified
on-chain in Bitcoin Script.

You can find the write-up here, which also includes instructions of
how to run the code and inspect the transactions using a local block
explorer: https://github.com/halseth/mattlab/blob/main/docs/challenge.md

TLDR; Using the proposed opcode OP_CHECKCONTRACTVERIFY and OP_CAT, we
show to trace execution of the program `multiply` [1] and challenge
this computation in O(n logn) on-chain transactions:

func multiply(x int) int {
    i := 0
    while {
        if i < 8 {
            x = x + x
            i = i + 1
        } else {
            break
        }
    }
    return x
}

Next steps would be to make this a generic framework with tools to
automatically compile arbitrary high-level programs down to
MATT-compatible Bitcoin Scripts.

All feedback appreciated!

- Johan

[0] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021182.html
[1] https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-November/021205.html


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 100, Issue 25
********************************************
