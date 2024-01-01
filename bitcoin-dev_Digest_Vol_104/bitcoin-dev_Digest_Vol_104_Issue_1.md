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
      (David A. Harding)


----------------------------------------------------------------------

Message: 1
Date: Sun, 31 Dec 2023 09:33:24 -1000
From: "David A. Harding" <dave@dtrt.org>
To: yurisvb@pm.me, Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Lamport scheme (not signature) to economize
	on L1
Message-ID: <6068d3536339704f3621894b2ba0daa8@dtrt.org>
Content-Type: text/plain; charset=US-ASCII; format=flowed

Hi Yuri,

I think it's worth noting that for transactions with an equal number of 
P2TR keypath spends (inputs) and P2TR outputs, the amount of space used 
in a transaction by the serialization of the signature itself (16 vbytes 
per input) ranges from a bit over 14% of transaction size (1-input, 
1-output) to a bit less than 16% (10,000-in, 10,000-out; a ~1 MvB tx).  
I infer that to mean that the absolute best a signature replacement 
scheme can do is free up 16% of block space.

An extra 16% of block space is significant, but the advantage of that 
savings needs to be compared to the challenge of creating a highly peer 
reviewed implementation of the new signature scheme and then convincing 
a very large number of Bitcoin users to accept it.  A soft fork proposal 
that introduces new-to-Bitcoin cryptography (such as a different hash 
function) will likely need to be studied for a prolonged period by many 
experts before Bitcoin users become confident enough in it to trust 
their bitcoins to it.  A hard fork proposal has the same challenges as a 
soft fork, plus likely a large delay before it can go into effect, and 
it also needs to be weighed against the much easier process it would be 
for experts and users to review a hard fork that increased block 
capacity by 16% directly.

I haven't fully studied your proposal (as I understand you're working on 
an improved version), but I wanted to put my gut feeling about it into 
words to offer feedback (hopefully of the constructive kind): I think 
the savings in block space might not be worth the cost in expert review 
and user consensus building.

That said, I love innovative ideas about Bitcoin and this is one I will 
remember.  If you continue working on it, I very much look forward to 
seeing what you come up with.  If you don't continue working on it, I 
believe you're likely to think of something else that will be just as 
exciting, if not more so.

Thanks for innovating!,

-Dave


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 104, Issue 1
*******************************************
