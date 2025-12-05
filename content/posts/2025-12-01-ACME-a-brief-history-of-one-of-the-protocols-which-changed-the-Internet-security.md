---
title: ACME, a brief history of one of the protocols which has changed the Internet Security
date: 2025-12-01
publishdate: 2025-12-01
---

![](/assets/acme-meme.jpg)

## ACME, a brief history of one of the protocols which has changed the Internet Security

### Changelog
- *03 December 2025: article announced on [Mastodon](https://infosec.exchange/@cbrocas/115654600635216276), [LinkedIn](https://www.linkedin.com/posts/cbrocas_a-brief-history-of-acme-blogpost-i-activity-7401895621802131456-WL5j) and [X](https://x.com/cbrocas/status/1996131769221865621).*
- *03 December 2025: J.C. Jones published his [reflections](https://insufficient.coffee/2025/12/03/reflecting-on-lets-encrypt/) about 10 years of Let's Encrypt. **A must read!***
- *03 December 2025: J.C. has also been kind enough to announce this article on [Hacker News](https://news.ycombinator.com/item?id=46141745). It makes it jump in the TOP 25 on the [HN homepage](/assets/screenshot_hackernews.png) and in stats (31k reads after 24h) 💚*
- *04 December 2025: add a link to the [ACME website](https://acmeprotocol.dev/acme/overview/) of [Fabien Hochstrasser](https://www.linkedin.com/in/fhchstr/).*

### Preamble

*I would like to share with you this article I wrote about the ACME protocol, which I "fell in love with" about ten years ago. It is for me a way to give back to this fantastic Free Software and Open Protocols developers community.* 

*This article is about the roots, the conception, the standardization, the relation with its ecosystem and the evolution challenges faced by the ACME protocol.*

*To write this article, I had the privilege of interviewing several people who have been involved in the creation and the evolution of ACME: [Aaron Gable](https://aarongable.com/#about), [Sarah Gran](https://letsencrypt.org/2023/12/28/eoy-letter-2023), [Jacob Hoffman-Andrews](https://www.eff.org/about/staff/jacob-hoffman-andrews) and [J.C. Jones](https://insufficient.coffee/about/) (more below).* 

*Thank you so much to all of you for your time and support! 💚*

## Internet and Network Protocols 

### Open and Standardized Protocols at the Heart of the Internet’s Success

During the 1990s, computing underwent a true revolution driven by the rise and global spread of the Internet. The Internet fulfilled the promise embodied in Sun Microsystems’ slogan [*"The Network is the Computer"*](https://en.wikipedia.org/wiki/The_Network_is_the_Computer).

By interconnecting individual computers, the Internet enabled its users to communicate without limits and without worrying about borders.

This unrestricted interconnection emerged at a pivotal moment in modern history: the opposition between the West and the Eastern Bloc led by the USSR had—albeit temporarily, as we now know—faded away, China was becoming the world’s factory, and the movement and collaboration between people were much freer and open than ever.

The Internet supported a kind of utopia of instant communication and sharing, previously unknown. This utopia was made possible by a set of open and standardized protocols. This was the key to enabling all kinds of different systems to cooperate and communicate seamlessly.

There were, of course, isolationist or monopolistic temptations from certain manufacturers or software editors. But open and standardized protocols ultimately prevailed, enabling unprecedented expansion. Built on top of IP, TCP, UDP, and DNS, among others, the HTTP and HTML duo would propel the Web as the Internet’s preferred communication platform for the next 30 years.

### Limited Use of Encryption

The success of this communication utopia was achieved without much concern for ensuring authentication, integrity, and confidentiality of exchanges.

In 2015, only [~40%](https://transparencyreport.google.com/https/overview) of websites used encryption. The consequences of this negligence in addressing security risks were confirmed by Edward Snowden’s revelations in 2013: our data was exposed to anyone who wanted and could intercept and collect it.

## Let's Encrypt is coming

### The Birth of an Automated and Free Certificate Authority

When asked about the main obstacles to the widespread adoption of encryption, [J.C. Jones](https://insufficient.coffee/about/), one of the architects of Let’s Encrypt and now one of its site reliability engineers after leading Firefox’s cryptographic team, responds: 

![](/assets/jc-jones100.png)

> *"More and more information was flowing across the Web, and most data being transferred did not have integrity or confidential protections from TLS. The biggest stumbling block to using TLS everywhere was obtaining and managing server-side certificates, and so: Let’s Encrypt" --  **J.C. Jones***

Obtaining a certificate was the main obstacle, and this was the priority to address.

This view was shared by a group of partners who, starting in 2013, pooled resources to establish Let’s Encrypt, an automated and free certificate authority. [Sarah Gran](https://letsencrypt.org/2023/12/28/eoy-letter-2023), VP of Advancement at Let’s Encrypt, shares: 

![](/assets/sarah-gran100.png)

> *"Early collaborators included people from Mozilla, Electronic Frontier Foundation, Akamai, Cisco, and the University of Michigan" -- **Sarah Gran***

And that's how Let's Encrypt was born. 

In the Web ecosystem, certificate authorities are organizations from which you can obtain a certificate for a domain  after proving you control it. 

And so, Let's Encrypt is since 2015 a certificate authority that delivers for free (as in free beer) TLS Server certificates. 

On the legal/administrative side, Let's Encrypt certificate authority operates for the public’s benefit and is a service provided by the Internet Security Research Group (ISRG), a California public benefit corporation.

Regarding [Let's Encrypt results](https://letsencrypt.org/stats/) ten years after its birth, they are really impressive (over 700M active certificates, over [60%](https://w3techs.com/technologies/details/sc-letsencrypt) of all the public TLS server certificates) and as Sarah Gran points out, so is the global HTTPS usage:

> *"When we started issuance, only about 39% of website visits were HTTPS. Today, it’s nearly 95% in the United States, and over 83% globally. We still have work to do, but we are proud of the progress we’ve made over the last ten years" -- **Sarah Gran***

Let's Encrypt delivers certificates in a automated manner using the ACME protocol which implies no manual action from the site owner nor the certificate authority. So, let's speak now a little about the automation aspect!

### Automation: The Core of the Operation

From the mid-2020s perspective, the automation at the heart of Let’s Encrypt might seem obvious, but in the first half of the 2010s, it was far from the norm. The ecosystem of public certificate authorities issuing server certificates was no exception.

At first glance, automation appears to be there to help website managers reliably deploy the TLS protocol on their sites, but it was first and foremost an absolute prerequisite for the very viability of the Let's Encrypt project.

As [Aaron Gable](https://aarongable.com/#about), tech lead of Boulder—the software at the core of Let’s Encrypt—, confirms: 

![](/assets/aaron-gable100.png)

> *"Automation was always going to be critical to Let’s Encrypt’s success. From the very beginning, we knew that there was no way we could scale manual validation on a non-profit’s budget" -- **Aaron Gable***

Indeed, it is worth noting that Let’s Encrypt has operated on an Internet scale from the start with a small team of about fifteen engineers, or even fewer at launch. For this team, automation was the only viable way to fulfill the immense mission they had set for themselves.

## ACME

### The Open and automated Protocol That Powers Let’s Encrypt

When we talk about automation in relation to Let’s Encrypt, we are talking about [ACME](https://tools.ietf.org/html/rfc8555) (Automated Certificate Management Environment).

This protocol allows client software to prove to an ACME-compatible certificate authority that it controls the domain for which it is requesting a certificate.

Sarah Gran clarifies an important point: 

> *"An important aspect of how Let’s Encrypt works is that we verify control over a domain, not ownership" -- **Sarah Gran*** 

Control vs. ownership of a domain—a nuance everyone should keep in mind.

This proof of control involves the client responding to a challenge issued by the ACME-compatible certificate authority. The challenge can be an HTTP, DNS, or TLS challenge, depending on the client’s choice and certificate authority support. Completing the challenge requires the ACME client to place a value provided by the ACME server—in a standardized HTTP path, a DNS zone, or a TLS response, respectively. All of these operations involve cryptography, of course.

The key point with ACME is that this entire dialogue between the client and the ACME server is executed without any human intervention, enabling the automatic issuance of certificates. Their deployment and integration into the web service can also generally be automated using scripts triggered after issuance.

On the Let's Encrypt website, you can discover more information about [how ACME works](https://letsencrypt.org/how-it-works/) and get more [detailled information](https://letsencrypt.org/docs/) about it. Even more details on the protocol are available on the [acmeprotocol.dev](https://acmeprotocol.dev/acme/overview/) website maintained by [Fabien Hochstrasser](https://www.linkedin.com/in/fhchstr/).

### Birth of ACME

One might wonder whether ACME was part of Let’s Encrypt’s design from the beginning.

J.C. Jones confirms: 

> *"By late 2014, the idea of an HTTP REST API with "/challenge" and "/certificate" existed, but we hadn’t defined much beyond that. We had a series of in-person meetings, in the Mozilla San Francisco office on Embarcadero and the EFF office in the Tenderloin through the spring of 2015 where we worked out the details" -- **J.C. Jones***

ACME was indeed at the core of Let’s Encrypt from the start and underwent a refinement process to cover all use cases as thoroughly as possible. 

To learn more about the roots of ACME and Let's Encrypt, there is a very informative document to read: the [Let's Encrypt paper](https://dl.acm.org/doi/pdf/10.1145/3319535.3363192) for [ACM CCS 2019](https://ccs2019.sigsac.org/) in London. It mentions the previous work of two teams: 

> *"A group led by Alex Halderman at the University of Michigan and Peter Eckersley at EFF was developing a protocol for automatically issuing and renewing certificates. Simultaneously, a team at Mozilla led by Josh Aas and Eric Rescorla was working on creating a free and automated certificate authority"*. 

When these two teams discovered each other's work, they joined forces. ACME and its implementation in Let's Encrypt were the result of this joint effort supported by the initial partners mentioned above.

### Securing the Web or the Internet?

Speaking of use cases, one might wonder whether the Web was Let’s Encrypt’s primary target, or if securing the Internet with its multiple protocols was also part of the objectives.

Sarah Gran provides an unambiguous first-level answer: 

> *"From Day One, we have sought to get the web to 100% encryption" -- **Sarah Gran***

But when asked about the various types of challenges in the protocol, J.C. Jones offers a nuance: 

> *"DNS, TLS-SNI, and HTTP were all in planning in spring 2015, but many of us were less confident in the procedure around the DNS validation. Which is ironic, as it turned out TLS-SNI had a vulnerability so we had to stop using it and our DNS validation was ultimately fine. In general, the collection of us were simply respectful of the great complexity within the DNS" -- **J.C. Jones***

This is a perspective not often publicly expressed by engineers primarily from the Web: their lack of confidence in implementing a DNS challenge stemmed from their humility regarding the complexity of the DNS ecosystem and the level of expertise required to master it.

The challenge was ultimately met, and this DNS challenge—though not its primary purpose—enabled multiple protocols outside HTTP like SMTP to be secured by ACME.

## Standardization and Open Source

### Developed in the Open

ACME was documented openly from the start, and [Certbot](https://certbot.eff.org/), the first open-source ACME client co-developed with the EFF, served as the client side reference implementation.

Similarly, a standardization process through the IETF resulted in [RFC 8555](https://datatracker.ietf.org/doc/rfc8555/) in March, 2019.

One of the consequences developing an open and standardized protocol was the creation of a multitude of [ACME clients covering a very wide range of use cases](https://letsencrypt.org/docs/client-options/).

J.C. Jones confirms that this was the goal: 

> *"This is what we foresaw, or at least hoped for. The initial client development often had conversations like, ‘oh, if someone wants that, then they’ll write their own client.’ It was a key part of why the REST API needed to be an IETF standard, and was part of the argument at the IETF BoF that resulted in the formation of the ACME Working Group in Q3 2015" -- **J.C. Jones***

Let’s Encrypt has also always provided constant support to developers by responding in its forum or on its GitHub issue tracker, and all this work has truly paid off. [An interesting post](https://letsencrypt.org/2025/10/07/ten-yrs-community-forum) has been recently written about support on the Let's Encrypt blog.

### Standardization for what benefits?

The other question that can be asked is whether or not the standardization process within the IETF has led to an improvement in the ACME protocol thanks to the cooperation that guides this process.

[Jacob Hoffman-Andrews](https://www.eff.org/about/staff/jacob-hoffman-andrews), one of the [RFC 8555](https://datatracker.ietf.org/doc/rfc8555/) authors working for EFF & Let's Encrypt, confirms an initial benefit that the ACME protocol has been able to derive from its standardization process: 

![](/assets/jacob100.png)

> *"One of the big changes was from a validation-first flow to a certificate-request-first flow. In other words, earlier drafts had subscribers requesting validation for domain names and then requesting a certificate once those validations were successful. The final RFC has subscribers request a certificate, and then the CA tells the subscriber what validations are needed. This change originated from within the IETF discussion process, and was intended to make handling of wildcard certificates more natural." -- **Jacob Hoffman-Andrews***  

Aside this first design improvement, Jacob details a second major improvement of the security of the protocol, improvement that also landed during the IETF standardization process: 

> *"Another big change, also originated from within the IETF, was to make all requests authenticated, including GET requests. Since ACME is authenticated with signed POSTs, this necessitated the POST-as-GET concept that’s in ACME today" -- **Jacob Hoffman-Andrews***  

We can see there how IETF iterations can challenge the security of a protocol and leads its development to innovative solutions to tackle the challenges it faces!

Last, Jacob adds another information that illustrates the benefits of developing a protocol into the open: it allows the community to evaluate (and sometimes, fix) its security level due to the availability of all materials and often, of the reference implementation: 

> *"Another very important evolution was the deprecation of the tls-sni-01 challenge method. This was found to be flawed by Frans Rosen, a security researcher. It was replaced with TLS-ALPN-01, developed at IETF with significant input from Google" -- **Jacob Hoffman-Andrews***

### Let’s Encrypt, ACME, and the Public Certificate Authorities Ecosystem

In 2015, the arrival of Let’s Encrypt in the public certificate authorities ecosystem raised a number of questions.

What level of cooperation or hostility? What impact on the viability of existing certificate authorities?

Here again, the fact that Let’s Encrypt was based on an open protocol, immediately subject to an IETF standardization initiative, enabled collaboration and adoption by the most innovative certificate authorities.

I spoke about the [External Account Binding](https://datatracker.ietf.org/doc/html/rfc8555/#section-7.3.4) (EAB) option of the protocol with J.C. Jones. EAB is a way for an ACME client to authenticate to an ACME server using an identifier and a key value which are verifiable by the server in a repository it maintains. With EAB, an ACME server can filter who can uses its service which is useful for commercial certificate authorities for example; it is an alternative model to Let's Encrypt one where anybody can ask for a certificate. 

Using the example of EAB, J.C. Jones confirms the collaboration with certificate authorities that happens during the IETF standardization process:
> *"EAB was an early addition at the IETF ACME Working Group. Many in the room were worried that without a means to bind to a payment method, ACME would not get adoption. In fact, some of the counterarguments to forming ACME were blunted by EAB, as such a mechanism wasn’t in the theoretically-competing, already-existent standard: SCEP. SCEP, it was argued, already handled 'free' certificate issuance, for private certificate authorities. Anything else needed a feasible path for usage payment." -- **J.C. Jones***

Beyond billing, the addition of EAB enabled also some commercial certificate authorities to integrate their existing domain control validation systems with ACME, allowing some of them to skip the challenge step of the ACME protocol.

The IETF standardization process, based on an open process, created the necessary discussion space for cooperation among entities that did not necessarily share the same objectives.

The result, ten years after the introduction of ACME and the completion of its standardization process in 2019, is that ACME has become the primary means by which all public certificate authorities—both free and commercial—rely on for their transition to an automated future of issuing short-lived certificates. 

Effectively, until early this year, the maximum lifespan of a public TLS server certificate was set to 398 days by the CA/B Forum, the organization that set the rules for public certificate authorities. With the vote of the [ballot SC081](https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/) at the CA/B Forum in April 2025, it has been decided that the certificate lifespan will decrease gradually starting March 2026 to reach 47 days in March 2029. The automation provided by ACME seems to be one of the main identified levers to help organizations to adapt to this drastic reduction in the lifespan of public TLS server certificates.

### Created at Let's Encrypt, adopted everywhere 

It is important to note that although ACME was developed by the team managing Let's Encrypt, this protocol is now one of the main protocols for automated certificate acquisition adopted by all public certificate authorities.

And outside the public certificate authorities ecosystem, I think it's fair to say that this protocol is also becoming increasingly popular with technical architects in companies with private certificate authorities. 

This has been the case in my company for several years now, where we have deployed an ACME endpoint in front of our internal certificate authority. Among the benefits we have seen, we have been able to rely on the vast ACME clients ecosystem in order to provide an ACME client to each OS or middleware that powers our infrastructure. We can see there how certificate obtention agility powered by ACME helps organizations in their journey to global IT agility.

## Innovation and the adoption challenge

### The ARI episode

We may fear that the development of a protocol supported primarily by a team as small as Let's Encrypt's will be fairly limited in terms of evolution and innovation. 

But the history of ACME shows that its evolution continues after its initial standardization.

In 2025, we saw with the ARI (ACME Renewal Information -- [RFC 9773](https://www.rfc-editor.org/rfc/rfc9773.html)) extension that the ACME protocol continues to evolve. ARI is a way for a certificate authority to suggest a renewal period to its clients, often earlier than they would have determined themselves. This use case is particularly relevant when the certificate authority needs to mass-revoke certificates that, for example, did not comply with the rules the certificate authority must follow when issuing certificates.

More specifically, J.C. Jones and Aaron Gable point two incidents that had to be handled by the Let's Encrypt team and that were the start for the ARI initiative:

> *"Explicitly, as remediation of https://bugzilla.mozilla.org/show_bug.cgi?id=1619179 and https://bugzilla.mozilla.org/show_bug.cgi?id=1715672 " **J.C. Jones and Aaron Gabble***

### Support to encourage adoption 

Aaron Gable leads the effort of designing and implementing ARI. But even if a new extension to the protocol has been produced, it can only reach its potential users after ACME clients have implemented it into their code base. As previously said, the team and some community members invest a lot on providing support to the community. In the case of ARI, this support is oriented to the ACME clients developers in order to make these clients ARI aware. 

Providing an efficient support and effective resources to the client side ACME actors is a huge part of the challenge in order to keep ACME ecosystem healthy and agile.

As illustrates by Sarah Gran, another way to give momentum to a new feature is to lift certain restrictions on access to the certificate authority:

> *In order to encourage ARI adoption, we’ve configured Let’s Encrypt to allow subscribers who renew via ARI to bypass our rate limits." -- **Sarah Gran***

### Client Side Update Challenge

But despite a good support work and incentive measures, Aaron Gable confirms ARI adoption is just at its start:

> *"There is still much progress to be made. Part of the appeal of the Automated Certificate Management Environment is that many users can set-and-forget their client and configuration. This means that most clients never receive software updates, and even client projects that have implemented ARI in their latest version still have massive install bases that aren’t running that version. We’ve worked closely with many clients developers to implement ARI, and contributed implementations ourselves in several cases, but for widespread adoption the whole ecosystem will need to slowly turn over" **-- Aaron Gable***

This situation is really shared with a lot of client side softwares that *"just work"(c)* and it raises some concerns about how to make an ecosystem keeping track with innovation on its client side. 

This challenge arises not only in terms of updating the client, but also in terms of updating the configuration. Many ACME clients rely on cron tasks. To have an efficient ARI setup, your task has to run ideally on a daily basis be able to ask the certification authority every day whether the certificate needs to be reissued. This is not the classic cron task setup. So, users have to modify this cron task frequency to reach the ARI goal of certificate reissuance led by certificate authority. Client side ACME setup evolution is a really challenging task.

### Evolution on server side ACME implementation

CA/B Forum has recently asked public certificate authorities to adopt [Multi-Perspective Issuance Corroboration](https://blog.citp.princeton.edu/2024/07/05/a-brief-history-of-multi-perspective-issuance-corroboration/) (MPIC) to guard against BGP attacks. We have asked Aaron Gable about the impacts that kind of measure have had on ACME server side implementation in the Let's Encrypt infrastructure:

> *"We’ve had to make few if any changes to our infrastructure to accommodate recent requirements changes such as MPIC and DNSSEC validation. We innovated MPIC (then called Remote Validation) along with a research team at Princeton, and implemented it in 2020. Our experience already running such a service helped inform the requirements as they were incorporated by the CA/B Forum." **-- Aaron Gable***

The lesson learnt here is that being at the edge of the innovation let you shape part of the future of your ecosystem and significantly lower the impact on your infrastructure of many regulatory measures that come into effect over time.

## Future

It is really encouraging to see a lot of innovation in the ACME ecosystem.

So what evolutions can we expect to see in the future? 

We have asked the question to Aaron Gable who gave us two upcoming developments: 
- *"We’re currently working on [standardizing](https://datatracker.ietf.org/doc/draft-ietf-acme-profiles/) **profile selection for ACME**, and our deployment of the early draft of this standard has already brought some much-needed flexibility to the WebPKI, enabling us to make changes to our certificate contents with minimal disruption."* 
- *"I’m also excited about a potential future change which would **introduce a 'pubkey' identifier type**, along with a set of challenges that allow the client to demonstrate control over the corresponding keypair. This would fix the gap today that presenting a CSR does not actually prove possession of the key in that CSR." -- **Araron Gable***

Fastly has also recently [contributed](https://www.fastly.com/blog/smarter-acme-challenge-for-multi-cdn-world) to ACME in order to improve the `dns-01` challenge in a multi-cloud and multi-PKI environment. An [IETF draft](https://datatracker.ietf.org/doc/html/draft-ietf-acme-dns-account-label/) describing this `dns-account-01` challenge is online. This is further proof that the public TLS ecosystem has truly embraced the ACME protocol as its primary automation tool.

Another recent development based on ACME has also shed new light on the potential of this protocol: since 2022, a [draft](https://datatracker.ietf.org/doc/draft-acme-device-attest/) is under progress at the IETF in order to write an ACME extension. The goal of this extension is to use ACME to obtain a certificate for a device in order to prove its identity. The challenge is based on device attestation and what's new in this case is the arrival of a third party, the attestation server.

What is remarkable here is that we are no longer dealing with ACME's initial use case, namely obtaining TLS server certificates: we can see in this IETF draft the potential of ACME as a challenge-based framework to obtain certificate in very different contexts. 

Indeed, we can venture to say that ACME's future looks bright 😊

## Conclusion

It is heartening to see that, 30 years after the widespread adoption of the Internet, open and standardized protocols continue to revolutionize its use. 

ACME and its Let's Encrypt implementation at scale have enabled the widespread adoption of HTTPS, thereby raising the level of security for billions of Internet users and also of private networks.

Having been able to do it inside a non profit organization, providing the Internet with an open and standardized protocol is a great success for all people believing in FreeSoftware and an Open Internet. 

As a community, I really think we can thank these organizations, teams, and engineers who continue to uphold the promise of efficiency and Freedom brought about by cooperation around open protocols. They inspire new generations (and older ones I guess 😉) demonstrating big things can still be achevied today in the open for the common good at the Internet scale!

I would like to extend a special thank you to the members of the Let's Encrypt team, **J.C. Jones**, **Aaron Gable**, **Sarah Gran** and **Jacob Hoffman-Andrews**, for the time and effort they dedicated to answering my questions. Without them, this article would not have been possible. 

A big shout out also to [Eric Leblond](https://github.com/regit) and [Philippe Teuwen](https://infosec.exchange/@doegox) who carefully proofread some early drafts of the article and [Philippe Bonnef](https://github.com/phbnf) and [Thibault Meunier](https://thibmeu.com/) for proofreading some of the last drafts. They all gave me so valuable and insightful advices 🙏