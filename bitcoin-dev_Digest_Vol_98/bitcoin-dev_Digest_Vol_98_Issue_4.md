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

   1. Re: On the experiment of the Bitcoin Contracting Primitives
      WG and marking this community process "up for grabs"
      (Keagan McClelland)
   2. Re: On the experiment of the Bitcoin Contracting Primitives
      WG and marking this community process "up for grabs" (Greg Sanders)


----------------------------------------------------------------------

Message: 1
Date: Wed, 19 Jul 2023 12:29:24 -0600
From: Keagan McClelland <keagan.mcclelland@gmail.com>
To: Antoine Riard <antoine.riard@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] On the experiment of the Bitcoin
	Contracting Primitives WG and marking this community process "up for
	grabs"
Message-ID:
	<CALeFGL0wzi0z13-H_t13fyrvy5cTo2j0f6qOL0-_zt8suMZU4A@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hi Antoine,

Thank you for the effort you've put towards this. I generally agree that a
smooth functioning Lightning Network is of greater importance than advanced
contracting capabilities. However, as I dive deeper into some of the more
ambitious goals for LN development I am learning that a great deal of
complexity of some current lightning (LN) proposals can be handily
discharged with CTV. While I am not intimately familiar with all of the
other covenant schemes to the same level of technical proficiency, I have a
suspicion that a number of them, if not all of them, are capable of
discharging the same flavor and amount of complexity as well. Others should
chime in if they can confirm this claim.

I have been publicly on the record as supporting the addition of some
covenant scheme into Bitcoin for some time and have long held on
theoretical grounds that the addition of such a mechanism is both necessary
and inevitable if Bitcoin is to survive in the long term. However, as I've
started to work more directly with the Lightning protocol, these
theoretical and purely logical arguments became far more concrete and
immediately beneficial.

I say this primarily to challenge the idea that covenants are a distraction
from lightning development. It may very well be that your areas of focus on
LN preclude you from splitting your attention and none of this email should
be interpreted as a criticism of you applying your efforts in the highest
leverage manner you can manage. That said, I don't want observers of this
thread to walk away with the impression that they are two independent
efforts as covenants can significantly contribute to LN's maturity. When
and how should they be prioritized? Unfortunately I don't feel able to
comment on that at this time. All I know is that Lightning would almost
certainly benefit substantially from having a covenant primitive.

Cheers,
Keags

On Tue, Jul 18, 2023 at 3:40?PM Antoine Riard via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi list,
>
> Last year amid the failure of the CTV speedy trial activation and intense
> conversations about a rainbow of covenant proposals, I introduced the idea
> of a new community process to specify covenants [0]. This post is to resume
> the experiment so far and officially mark the process maintenance as "up
> for grabs", as I won't actively pursue it further (after wavering on such a
> decision a bit during May / June).
>
> Few of the goals announced at that time were to build a consistent
> framework to evaluate covenant proposals, see the common grounds between
> proposals if they could be composed or combined by their authors, open the
> consensus  changes development process beyond the historical boundaries of
> Bitcoin Core and maintain high-quality technical archive as a consensus
> discussions have spawned half a decade from intellectual conception to
> activation in average (at least for segwit, schnorr, taproot).
>
> Such effort was a speak-by-the-act answer to the issues in
> consensus development changes pointed out by Jeremy Rubin in April of last
> year [1]: namely the lack of a "codified checklist" for consensus changes,
> that "consensus is memoryless" and "bitcoin core is not bitcoin"
> (independently of the technical concerns as I have as limited or
> non-adequate primitive for vaults / payment pools I expressed during the
> same time). Other complementary initiatives have been undertaken during the
> same period, AJ with the bitcoin-inquisition fork where the community of
> developers and contracting primitives of researchers on a consensus-enabled
> fork of core [2]. And Dave Harding with the careful archiving of all
> covenant proposals under the Optech umbrella [3].
>
> About the Bitcoin Contracting Primitives WG, a Github repository was
> started and maintained to archive and document all the primitives (apo,
> tluv, ctv, the taproot annex, sighash_group, CSFS, cat, txhash, evict,
> check_output_covenant_verify, inherited ids, anyamount, singletons,
> op_vault) and the corresponding protocols (payment pools, vaults,
> drivechains, trust-minimized mining pools payouts). We had a total of 6
> monthly meetings on the Libera chat #bitcoin-contracting-primitives-wg for
> a number of more than 20 individual attendees representing most of the
> parts of the community. I think (missing march logs). Numerous in-depth
> discussions did happen on the repository and on the channel on things like
> "merkelized all the things" or "payment pools for miners payoffs".
>
> As I've been busy on the Lightning-side and other Bitcoin projects, I've
> not run an online meeting since the month of April, while still having a
> bunch of fruitful technical discussions with folks involved in the effort
> at conferences and elsewhere. I launched the effort as an experiment with
> the soft commitment to dedicate 20% of my time on it, after few successful
> sessions I think such a process has an interest of its own, however it
> comes with direct competition of my time to work on Lightning robustness.
> Getting my hands dirty on low-level LDK development recently made me
> realize we still have years of titan work to get a secure and reliable
> Lightning Network.
>
> As such, between extended covenant capabilities for advanced contracts
> coming as a reality for Bitcoin _or_ LN working smoothly at scale with
> 50-100M UTXO-sharing users on it during the next 5-7 years cycle, I think
> the latter goal is more critical for Bitcoin existential survival, and
> where on a personal title I'll allocate the best of my time and energy (and
> somehow it match the "slow" technical activity on bitcoin-inquisition
> mostly done by Lightning hands).
>
> This is my personal conclusion only on the state of Bitcoin technological
> momentum, and this is quite tainted by my deep background in Lightning
> development. If you've been working on covenant changes proposals, please
> don't take it as a discouragement, I think Taproot (privacy-preserving
> script policies behind the taproot tree branches) and Schnorr (for native
> multi-sig) soft forks have shown how it can improve the building of
> self-custody solutions by one or two order of magnitude, and small
> incremental changes might be good enough to have a lower technical
> consensus bar.
>
> On my side, I'll pursue pure R&D works on CoinPool, notably coming with
> better solutions with the interactivity issue and mass-compression of
> withdrawal and design exotic advanced Bitcoin contracts based on the
> taproot annex, though more in a "l'art pour l'art" approach for the time
> being [4]. Additionally, I might start to submit an in-depth security
> review of consensus changes under pseudonyms, it has already been done in
> the past and somehow it's good practice in terms of "message neutrality"
> [5]. If folks wanna experiment in terms of payment pools deployment, Greg
> Maxwell's old joinpool can be used today (and somehow it's worthy of its
> own as a net advance for coinjoins).
>
> I'll honestly acknowledge towards the community, I might have overpromised
> with the kickstart of this new process aiming to move the frontlines in
> matters of Bitcoin consensus changes development process. On the other
> hand, I think enough sessions of the working group have been runned and
> enough marks of technical interests have been collected to demonstrate the
> minimal value of such a process, so I would estimate my open-source balance
> sheet towards the community to be in good standing ? (open-minded question).
>
> I don't think Bitcoin fundamentally lacks compelling technical proposals
> to advance the capabilities of Bitcoin Script today, nor the crowd of
> seasoned and smart protocol developers to evaluate mature proposals
> end-to-end and on multiple dimensions with a spirit of independence.
> Rather, I believe what Bitcoin is lacking is a small crowd of technical
> historians and archivist doing the work of assessing, collecting and
> preserving consensus changes proposals and QA devs to ensure any consensus
> change proposals has world-class battle-ground testing before to be
> considered for deployment, ideally with the best standards of Bitcoin
> decentralization and FOSS neutrality [6].
>
> If you would like to pursue the maintenance and nurturing of the Bitcoin
> Contracting Primitives WG (or the bitcoin-inquisition fork or collaborate
> with Optech to organize industry-wise workshop on covenants at the image of
> what has been done in 2019 for Taproot), that you're willing to show
> proof-of-work and you estimate that operational ground, legal information
> or financial resources will anchor your individual work on the long-term,
> don't hesitate to reach out, I'll see what I can do with a disinterested
> mind [7].
>
> With humility,
> Antoine
>
> [0]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-July/020763.html
> [1]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020233.html
> [2]
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-September/020921.html
> [3] https://github.com/bitcoinops/bitcoinops.github.io/pull/806
> [4] Version 0.2 of the CoinPool whitepaper addressing most of the
> remaining "Big Problems" is still pending on my visit to co-author Gleb
> Naumenko in Ukraine, which has been postponed few times in light of the
> conflict operational evolutions.
> [5] See
> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-February/017614.html.
> For the philosophical reasons of doing so, I invite you to read Foucault's
> famous essay "Le philosophe masque".
> [6] Somehow I come to share Jeremy's thesis's "Product management is not
> "my Job" it's yours" in matters of consensus changes. I believe we might be
> past the technical complexity threshold where even simple consensus changes
> can be conducted from A to Z as a one man job or even by a group of 2/3
> elite devs.
> [7] I've been reached out multiple times and consistently by R&D
> non-profits, plebs whales and VC firms who were interested to commit
> resources to advance softforks and covenants in the Bitcoin space, no doubt
> when you're reliable and with a track record, folks are ready to offer you
> opportunities to work full-time on consensus changes.
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230719/5dac7ac0/attachment-0001.html>

------------------------------

Message: 2
Date: Wed, 19 Jul 2023 16:45:15 -0400
From: Greg Sanders <gsanders87@gmail.com>
To: Keagan McClelland <keagan.mcclelland@gmail.com>,  Bitcoin Protocol
	Discussion <bitcoin-dev@lists.linuxfoundation.org>
Subject: Re: [bitcoin-dev] On the experiment of the Bitcoin
	Contracting Primitives WG and marking this community process "up for
	grabs"
Message-ID:
	<CAB3F3DsSjtXxA3X34ky7P=QSr3rEcG94dJ6k7sO543G0HvCv-A@mail.gmail.com>
Content-Type: text/plain; charset="utf-8"

Hello Keagen,

Most of the complexity of LN cannot be resolved with covenants. Of the
things that can be simplified in my experience, you're going to need more
than CTV to get significant gains. And in the end, channels can only get so
simple since we have many other BOLTs to deal with. And even then, you're
going to have to convince LN spec writers to include such changes, whatever
they are, then get deployment.

Step 1 is finding a primitive that seems interesting. It's important to
moderate enthusiasm for any primitive with reality, and probably by being
concrete by writing specs that use a primitive, and code it up to discover
what we're overlooking. We're always overlooking something! In my humble
opinion these are step 2 and 3 of gathering mind-share.

As a more productive tact, if we're thinking beyond 2/small party channels,
probably better to snap your fingers, pretend we have Simplicity, see what
we can build, and work backwards from there to see if we can accomplish
this within the confines of bitcoin script?

Cheers,
Greg

On Wed, Jul 19, 2023 at 3:59?PM Keagan McClelland via bitcoin-dev <
bitcoin-dev@lists.linuxfoundation.org> wrote:

> Hi Antoine,
>
> Thank you for the effort you've put towards this. I generally agree that a
> smooth functioning Lightning Network is of greater importance than advanced
> contracting capabilities. However, as I dive deeper into some of the more
> ambitious goals for LN development I am learning that a great deal of
> complexity of some current lightning (LN) proposals can be handily
> discharged with CTV. While I am not intimately familiar with all of the
> other covenant schemes to the same level of technical proficiency, I have a
> suspicion that a number of them, if not all of them, are capable of
> discharging the same flavor and amount of complexity as well. Others should
> chime in if they can confirm this claim.
>
> I have been publicly on the record as supporting the addition of some
> covenant scheme into Bitcoin for some time and have long held on
> theoretical grounds that the addition of such a mechanism is both necessary
> and inevitable if Bitcoin is to survive in the long term. However, as I've
> started to work more directly with the Lightning protocol, these
> theoretical and purely logical arguments became far more concrete and
> immediately beneficial.
>
> I say this primarily to challenge the idea that covenants are a
> distraction from lightning development. It may very well be that your areas
> of focus on LN preclude you from splitting your attention and none of this
> email should be interpreted as a criticism of you applying your efforts in
> the highest leverage manner you can manage. That said, I don't want
> observers of this thread to walk away with the impression that they are two
> independent efforts as covenants can significantly contribute to LN's
> maturity. When and how should they be prioritized? Unfortunately I don't
> feel able to comment on that at this time. All I know is that Lightning
> would almost certainly benefit substantially from having a covenant
> primitive.
>
> Cheers,
> Keags
>
> On Tue, Jul 18, 2023 at 3:40?PM Antoine Riard via bitcoin-dev <
> bitcoin-dev@lists.linuxfoundation.org> wrote:
>
>> Hi list,
>>
>> Last year amid the failure of the CTV speedy trial activation and intense
>> conversations about a rainbow of covenant proposals, I introduced the idea
>> of a new community process to specify covenants [0]. This post is to resume
>> the experiment so far and officially mark the process maintenance as "up
>> for grabs", as I won't actively pursue it further (after wavering on such a
>> decision a bit during May / June).
>>
>> Few of the goals announced at that time were to build a consistent
>> framework to evaluate covenant proposals, see the common grounds between
>> proposals if they could be composed or combined by their authors, open the
>> consensus  changes development process beyond the historical boundaries of
>> Bitcoin Core and maintain high-quality technical archive as a consensus
>> discussions have spawned half a decade from intellectual conception to
>> activation in average (at least for segwit, schnorr, taproot).
>>
>> Such effort was a speak-by-the-act answer to the issues in
>> consensus development changes pointed out by Jeremy Rubin in April of last
>> year [1]: namely the lack of a "codified checklist" for consensus changes,
>> that "consensus is memoryless" and "bitcoin core is not bitcoin"
>> (independently of the technical concerns as I have as limited or
>> non-adequate primitive for vaults / payment pools I expressed during the
>> same time). Other complementary initiatives have been undertaken during the
>> same period, AJ with the bitcoin-inquisition fork where the community of
>> developers and contracting primitives of researchers on a consensus-enabled
>> fork of core [2]. And Dave Harding with the careful archiving of all
>> covenant proposals under the Optech umbrella [3].
>>
>> About the Bitcoin Contracting Primitives WG, a Github repository was
>> started and maintained to archive and document all the primitives (apo,
>> tluv, ctv, the taproot annex, sighash_group, CSFS, cat, txhash, evict,
>> check_output_covenant_verify, inherited ids, anyamount, singletons,
>> op_vault) and the corresponding protocols (payment pools, vaults,
>> drivechains, trust-minimized mining pools payouts). We had a total of 6
>> monthly meetings on the Libera chat #bitcoin-contracting-primitives-wg for
>> a number of more than 20 individual attendees representing most of the
>> parts of the community. I think (missing march logs). Numerous in-depth
>> discussions did happen on the repository and on the channel on things like
>> "merkelized all the things" or "payment pools for miners payoffs".
>>
>> As I've been busy on the Lightning-side and other Bitcoin projects, I've
>> not run an online meeting since the month of April, while still having a
>> bunch of fruitful technical discussions with folks involved in the effort
>> at conferences and elsewhere. I launched the effort as an experiment with
>> the soft commitment to dedicate 20% of my time on it, after few successful
>> sessions I think such a process has an interest of its own, however it
>> comes with direct competition of my time to work on Lightning robustness.
>> Getting my hands dirty on low-level LDK development recently made me
>> realize we still have years of titan work to get a secure and reliable
>> Lightning Network.
>>
>> As such, between extended covenant capabilities for advanced contracts
>> coming as a reality for Bitcoin _or_ LN working smoothly at scale with
>> 50-100M UTXO-sharing users on it during the next 5-7 years cycle, I think
>> the latter goal is more critical for Bitcoin existential survival, and
>> where on a personal title I'll allocate the best of my time and energy (and
>> somehow it match the "slow" technical activity on bitcoin-inquisition
>> mostly done by Lightning hands).
>>
>> This is my personal conclusion only on the state of Bitcoin technological
>> momentum, and this is quite tainted by my deep background in Lightning
>> development. If you've been working on covenant changes proposals, please
>> don't take it as a discouragement, I think Taproot (privacy-preserving
>> script policies behind the taproot tree branches) and Schnorr (for native
>> multi-sig) soft forks have shown how it can improve the building of
>> self-custody solutions by one or two order of magnitude, and small
>> incremental changes might be good enough to have a lower technical
>> consensus bar.
>>
>> On my side, I'll pursue pure R&D works on CoinPool, notably coming with
>> better solutions with the interactivity issue and mass-compression of
>> withdrawal and design exotic advanced Bitcoin contracts based on the
>> taproot annex, though more in a "l'art pour l'art" approach for the time
>> being [4]. Additionally, I might start to submit an in-depth security
>> review of consensus changes under pseudonyms, it has already been done in
>> the past and somehow it's good practice in terms of "message neutrality"
>> [5]. If folks wanna experiment in terms of payment pools deployment, Greg
>> Maxwell's old joinpool can be used today (and somehow it's worthy of its
>> own as a net advance for coinjoins).
>>
>> I'll honestly acknowledge towards the community, I might have
>> overpromised with the kickstart of this new process aiming to move the
>> frontlines in matters of Bitcoin consensus changes development process. On
>> the other hand, I think enough sessions of the working group have been
>> runned and enough marks of technical interests have been collected to
>> demonstrate the minimal value of such a process, so I would estimate my
>> open-source balance sheet towards the community to be in good standing ?
>> (open-minded question).
>>
>> I don't think Bitcoin fundamentally lacks compelling technical proposals
>> to advance the capabilities of Bitcoin Script today, nor the crowd of
>> seasoned and smart protocol developers to evaluate mature proposals
>> end-to-end and on multiple dimensions with a spirit of independence.
>> Rather, I believe what Bitcoin is lacking is a small crowd of technical
>> historians and archivist doing the work of assessing, collecting and
>> preserving consensus changes proposals and QA devs to ensure any consensus
>> change proposals has world-class battle-ground testing before to be
>> considered for deployment, ideally with the best standards of Bitcoin
>> decentralization and FOSS neutrality [6].
>>
>> If you would like to pursue the maintenance and nurturing of the Bitcoin
>> Contracting Primitives WG (or the bitcoin-inquisition fork or collaborate
>> with Optech to organize industry-wise workshop on covenants at the image of
>> what has been done in 2019 for Taproot), that you're willing to show
>> proof-of-work and you estimate that operational ground, legal information
>> or financial resources will anchor your individual work on the long-term,
>> don't hesitate to reach out, I'll see what I can do with a disinterested
>> mind [7].
>>
>> With humility,
>> Antoine
>>
>> [0]
>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-July/020763.html
>> [1]
>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-April/020233.html
>> [2]
>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2022-September/020921.html
>> [3] https://github.com/bitcoinops/bitcoinops.github.io/pull/806
>> [4] Version 0.2 of the CoinPool whitepaper addressing most of the
>> remaining "Big Problems" is still pending on my visit to co-author Gleb
>> Naumenko in Ukraine, which has been postponed few times in light of the
>> conflict operational evolutions.
>> [5] See
>> https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2020-February/017614.html.
>> For the philosophical reasons of doing so, I invite you to read Foucault's
>> famous essay "Le philosophe masque".
>> [6] Somehow I come to share Jeremy's thesis's "Product management is not
>> "my Job" it's yours" in matters of consensus changes. I believe we might be
>> past the technical complexity threshold where even simple consensus changes
>> can be conducted from A to Z as a one man job or even by a group of 2/3
>> elite devs.
>> [7] I've been reached out multiple times and consistently by R&D
>> non-profits, plebs whales and VC firms who were interested to commit
>> resources to advance softforks and covenants in the Bitcoin space, no doubt
>> when you're reliable and with a track record, folks are ready to offer you
>> opportunities to work full-time on consensus changes.
>> _______________________________________________
>> bitcoin-dev mailing list
>> bitcoin-dev@lists.linuxfoundation.org
>> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>>
> _______________________________________________
> bitcoin-dev mailing list
> bitcoin-dev@lists.linuxfoundation.org
> https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev
>
-------------- next part --------------
An HTML attachment was scrubbed...
URL: <http://lists.linuxfoundation.org/pipermail/bitcoin-dev/attachments/20230719/3995d4a3/attachment.html>

------------------------------

Subject: Digest Footer

_______________________________________________
bitcoin-dev mailing list
bitcoin-dev@lists.linuxfoundation.org
https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev


------------------------------

End of bitcoin-dev Digest, Vol 98, Issue 4
******************************************
