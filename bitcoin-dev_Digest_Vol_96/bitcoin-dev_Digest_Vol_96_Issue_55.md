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

   1. Re: Coinjoin with less steps using ALL|ANYONECANPAY
      (Lucas Ontivero)
   2. Re: Coinjoin with less steps using ALL|ANYONECANPAY (alicexbt)
   3. Re: Coinjoin with less steps using ALL|ANYONECANPAY (alicexbt)


----------------------------------------------------------------------

Message: 1
Date: Tue, 23 May 2023 09:17:23 -0300
From: Lucas Ontivero <lucasontivero@gmail.com>
To: Ben Carman <benthecarman@live.com>,  Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Coinjoin with less steps using
	ALL|ANYONECANPAY
Message-ID:
	<CALHvQn29S2T=ehqGD1vCJQQuC0aD6rjUUPsb+n80EBPgc_G4JA@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi all,

In some coinjoin implementations inputs are registered first because in
that way, if the user fails or refuses to sign the transaction the input is
banned and denial of service is made a bit more expensive, in the sense
that an attacker needs more and more utxos to keep the attack going.

Your proposal can work if you find an alternative mechanism for mitigating
the DoS attacks or when DoS attacks are not a problem (I can imagine there
are scenarios where it is not really important).

Best

- Lucas


On Mon, May 22, 2023 at 7:53?PM Ben Carman via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> The problem with using ALL|ANYONECANPAY is that you cannot verify
> beforehand that the other inputs are the inputs you want added to the
> transaction.
>
> Some examples of bad things that could happen:
>
>
>    - Coordinator adds its own inputs, you still get your outputs but
>    effectively paid fees for no privacy gain
>    - The inputs added could be paying at a lower fee rate than expected,
>    causing the tx to take longer than what you paid for
>    - Different input types or amount are added so you no longer have the
>    same uniformity across the inputs
>    - (if you care) An input from a sanctioned address is added, causing
>    you to get "tainted" coins.
>
> This is the code in ln-vortex that verifies the psbt on the client side if
> you are curious
>
>
> https://github.com/ln-vortex/ln-vortex/blob/master/client/src/main/scala/com/lnvortex/client/VortexClient.scala#L616
>
>
> Best,
>
> benthecarman
>
> ------------------------------
> *From:* bitcoin-dev <bitcoin-dev-bounces@lists.linuxfoundation.org> on
> behalf of alicexbt via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>
> *Sent:* Monday, May 22, 2023 7:51 AM
> *To:* Bitcoin Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
> *Subject:* [bitcoin-dev] Coinjoin with less steps using ALL|ANYONECANPAY
>
> Hi Bitcoin Developers,
>
> I recently experimented with different sighash flags, PSBTs and realized
> ALL|ANYONECANPAY could be used to reduce some steps in coinjoin.
>
> Steps:
>
> - Register outputs.
> - One user creates a signed PSBT with 1 input, all registered outputs and
> ALL|ANYONECANPAY sighash flag. Other participants keep adding their inputs
> to PSBT.
> - Finalize and broadcast the transaction.
>
> Proof of Concept (Aice and Bob): https://gitlab.com/-/snippets/2542297
>
> Tx:
> https://mempool.space/testnet/tx/c6dd626591dca7e25bbd516f01b23171eb0f2b623471fcf8e073c87c1179c492
>
> I plan to use this in joinstr if there are no major drawbacks and it can
> even be implemented by other coinjoin implementations.
>
> /dev/fd0
> floppy disk guy
>
> Sent with Proton Mail secure email.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230523/4bc0294c/attachment.html>

------------------------------

Message: 2
Date: Tue, 23 May 2023 12:34:03 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Ben Carman <benthecarman@live.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Coinjoin with less steps using
	ALL|ANYONECANPAY
Message-ID:
	<WEKSZ7Q3Eloj2wIrMIjdLPpvmhKq9nvcZz5Agb6CvnpOAGrkRXatFogui9N7XnSorQ4BymhISqAHjss90M1F-H-HIaGKvbfaCTXDCVHQsqM=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Ben,

Thanks for the feedback.

> -   Coordinator adds its own inputs, you still get your outputs but effectively paid fees for no privacy gain

What will be the incentive for a coordinator to add its inputs in coinjoin? Is this possible without ALL|ANYONECANPAY as well? Even if there is an incentive its unlikely to work in joinstr as there is no centralized coordinator. Multiple common relays are used to coordinate a coinjoin round.

> -   The inputs added could be paying at a lower fee rate than expected, causing the tx to take longer than what you paid for
> -   Different input types or amount are added so you no longer have the same uniformity across the inputs

> This is the code in ln-vortex that verifies the psbt on the client side if you are curious
> 
> https://github.com/ln-vortex/ln-vortex/blob/master/client/src/main/scala/com/lnvortex/client/VortexClient.scala#L616

These 2 are important things and could be managed with client side validation by keeping min-max amounts for inputs in a round and disallow different types of inputs. Thanks for sharing the code that validates PSBT.

Joinstr will also use NIP38/48 channels for coinjoin rounds so that only participants in a coinjoin round are aware of details.

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Tuesday, May 23rd, 2023 at 4:21 AM, Ben Carman <benthecarman@live.com> wrote:


> The problem with using ALL|ANYONECANPAY is that you cannot verify beforehand that the other inputs are the inputs you want added to the transaction.
> 
> Some examples of bad things that could happen:
> 
> 
> -   Coordinator adds its own inputs, you still get your outputs but effectively paid fees for no privacy gain
> -   The inputs added could be paying at a lower fee rate than expected, causing the tx to take longer than what you paid for
> -   Different input types or amount are added so you no longer have the same uniformity across the inputs
> -   (if you care) An input from a sanctioned address is added, causing you to get "tainted" coins.
>     
> 
> This is the code in ln-vortex that verifies the psbt on the client side if you are curious
> 
> https://github.com/ln-vortex/ln-vortex/blob/master/client/src/main/scala/com/lnvortex/client/VortexClient.scala#L616
> 
> 
> Best,
> 
> benthecarman
> 
> 
> 
> From: bitcoin-dev <bitcoin-dev-bounces@lists.linuxfoundation.org> on behalf of alicexbt via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>
> Sent: Monday, May 22, 2023 7:51 AM
> To: Bitcoin Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
> Subject: [bitcoin-dev] Coinjoin with less steps using ALL|ANYONECANPAY
> 
> Hi Bitcoin Developers,
> 
> I recently experimented with different sighash flags, PSBTs and realized ALL|ANYONECANPAY could be used to reduce some steps in coinjoin.
> 
> Steps:
> 
> - Register outputs.
> - One user creates a signed PSBT with 1 input, all registered outputs and ALL|ANYONECANPAY sighash flag. Other participants keep adding their inputs to PSBT.
> - Finalize and broadcast the transaction.
> 
> Proof of Concept (Aice and Bob):?https://gitlab.com/-/snippets/2542297
> 
> Tx: https://mempool.space/testnet/tx/c6dd626591dca7e25bbd516f01b23171eb0f2b623471fcf8e073c87c1179c492
> 
> I plan to use this in joinstr if there are no major drawbacks and it can even be implemented by other coinjoin implementations.
> 
> /dev/fd0
> floppy disk guy
> 
> Sent with Proton Mail secure email.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Message: 3
Date: Tue, 23 May 2023 12:48:02 +0000
From: alicexbt <alicexbt@protonmail.com>
To: Lucas Ontivero <lucasontivero@gmail.com>
Cc: Bitcoin Protocol Discussion
	<bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] Coinjoin with less steps using
	ALL|ANYONECANPAY
Message-ID:
	<oLOjKr_MJ2WHkg0KSM5sw5B9RQNFDWpM3RHjea_Q_lRM3rBzwyRELllZzc2hxuGjFTkykJDAP1p-p3QbXTqYMl3U_EnuDxq_3a5ZfcB7aPw=@protonmail.com>
	
Content-Type: text/plain; charset=utf-8

Hi Lucas,

> In some coinjoin implementations inputs are registered first because in that way, if the user fails or refuses to sign the transaction the input is banned and denial of service is made a bit more expensive, in the sense that an attacker needs more and more utxos to keep the attack going.

DoS attacks are even possible in later stages of a coinjoin round. Example: Double spend inputs after signing

Inputs could be banned in second step if ALL|ANYONECANPAY sighash flag is used and outputs are registered initially.

/dev/fd0
floppy disk guy

Sent with Proton Mail secure email.

------- Original Message -------
On Tuesday, May 23rd, 2023 at 5:47 PM, Lucas Ontivero <lucasontivero@gmail.com> wrote:


> Hi all,
> In some coinjoin implementations inputs are registered first because in that way, if the user fails or refuses to sign the transaction the input is banned and denial of service is made a bit more expensive, in the sense that an attacker needs more and more utxos to keep the attack going.
> 
> Your proposal can work if you find an alternative mechanism for mitigating the DoS attacks or when DoS attacks are not a problem (I can imagine there are scenarios where it is not really important).
> Best
> - Lucas
> 
> 
> 
> On Mon, May 22, 2023 at 7:53?PM Ben Carman via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org> wrote:
> 
> > The problem with using ALL|ANYONECANPAY is that you cannot verify beforehand that the other inputs are the inputs you want added to the transaction.
> > 
> > Some examples of bad things that could happen:
> > 
> > 
> > -   Coordinator adds its own inputs, you still get your outputs but effectively paid fees for no privacy gain
> > -   The inputs added could be paying at a lower fee rate than expected, causing the tx to take longer than what you paid for
> > -   Different input types or amount are added so you no longer have the same uniformity across the inputs
> > -   (if you care) An input from a sanctioned address is added, causing you to get "tainted" coins.
> >     
> > 
> > This is the code in ln-vortex that verifies the psbt on the client side if you are curious
> > 
> > https://github.com/ln-vortex/ln-vortex/blob/master/client/src/main/scala/com/lnvortex/client/VortexClient.scala#L616
> > 
> > 
> > Best,
> > 
> > benthecarman
> > 
> > 
> > 
> > From: bitcoin-dev <bitcoin-dev-bounces@lists.linuxfoundation.org> on behalf of alicexbt via bitcoin-dev <bitcoin-dev@lists.linuxfoundation.org>
> > Sent: Monday, May 22, 2023 7:51 AM
> > To: Bitcoin Protocol Discussion <bitcoin-dev@lists.linuxfoundation.org>
> > Subject: [bitcoin-dev] Coinjoin with less steps using ALL|ANYONECANPAY
> > 
> > Hi Bitcoin Developers,
> > 
> > I recently experimented with different sighash flags, PSBTs and realized ALL|ANYONECANPAY could be used to reduce some steps in coinjoin.
> > 
> > Steps:
> > 
> > - Register outputs.
> > - One user creates a signed PSBT with 1 input, all registered outputs and ALL|ANYONECANPAY sighash flag. Other participants keep adding their inputs to PSBT.
> > - Finalize and broadcast the transaction.
> > 
> > Proof of Concept (Aice and Bob): https://gitlab.com/-/snippets/2542297
> > 
> > Tx: https://mempool.space/testnet/tx/c6dd626591dca7e25bbd516f01b23171eb0f2b623471fcf8e073c87c1179c492
> > 
> > I plan to use this in joinstr if there are no major drawbacks and it can even be implemented by other coinjoin implementations.
> > 
> > /dev/fd0
> > floppy disk guy
> > 
> > Sent with Proton Mail secure email.
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
> > 
> > _______________________________________________
> > bitcoin-dev mailing list
> > bitcoin-dev@lists.linuxfoundation.org
> > https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 96, Issue 55
*******************************************
