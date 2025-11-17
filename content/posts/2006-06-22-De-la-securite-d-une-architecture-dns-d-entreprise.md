---
title: Article MISC janvier 2006 - De la sécurité d'une architecture DNS d'entreprise
date: 2006-06-22
---

# De la sécurité d'une architecture DNS d'entreprise

_Cet article est issu de l’article publié dans le numéro 23 de MISC. Ses auteurs sont Christophe Brocas (christophe.brocas@free.fr) et Jean-Michel Farin (jeanmichel.farin@free.fr). Tous droits réservés à MISC._

Ces dix dernières années, les entreprises ont vu une interconnexion toujours croissante de leurs systèmes d’informations (SI), entre eux ainsi qu’avec l’internet. Cette interconnexion s’est accompagnée d’une adoption massive de protocoles standards. Parmi ces protocoles, le DNS (Domain Name Service) affiche la double caractéristique d’être le plus systématiquement utilisé et sûrement le moins correctement surveillé.

## 1. Introduction
Le DNS est souvent vu comme un protocole utilitaire au fonctionnement opaque. Et à la vue de son caractère primordial pour le bon fonctionnement des protocoles applicatifs tels SMTP ou HTTP, les portes de ce protocole sont souvent laissées grandes ouvertes tout au long de la chaîne de liaison du SI (postes, serveurs, routeurs etc).

Nous verrons dans cet article comment sécuriser ce protocole et en particulier son implémentation dans un réseau d’entreprise. Les exemples de configuration reposeront sur le logiciel Bind, version 9.1.x et suivantes [^4].

### 1.1 Terminologie
Avant de plonger dans le DNS, accordons nous sur les termes utilisés dans ce document :
* **resolver :** logiciel client DNS sollicité par les applications sur les postes clients afin d’obtenir une résolution ;
* **serveur cache :** serveur sollicité par les resolvers ou par d’autres serveurs cache. Ce type de serveur assure la fonction de récupération d’informations auprès de serveurs de noms ou d’autres serveurs cache. Il stocke les informations collectées dans son cache. Ce serveur ne gérant aucune zone DNS, le type de recherche supportée est récursif ;
* **serveur SOA :** serveur de noms faisant autorité répondant aux requêtes pour une (ou plusieurs) zone(s). Ce serveur n’ayant pour mission que de répondre à des requêtes sur un ou plusieurs domaines, dans notre configuration, nous n’autorisons aucune récursion.

### 1.2 Les vulnérabilités DNS
À présent, regardons les différents types de menaces pouvant toucher le DNS :
* la **fuite d’informations** via des canaux cachés ;
* la **corruption de résolution DNS** permettant d’abuser les utilisateurs du système, d’informations et de leur dérober des informations sensibles ;
* le **déni de services** par l’acceptation de requêtes illégales ou par corruption de données dans les zones hébergées par les serveurs DNS internes.

**La fuite d’informations**
La fuite d’informations par tunnel DNS a été couverte de manière complète dans les pages de MISC [^1]. Les contre-mesures pour lutter contre ce type d’évasion se concentreront autour de la politique d’accès au service DNS ainsi qu’aux requêtes autorisées en fonction du type de client. La mise en oeuvre de cette politique sera décrite dans le paragraphe " Configuration du serveur DNS cache interne ".

**Corruption de résolution**
Ce type d’attaque a pour but de corrompre les données DNS fournies au client afin de, par exemple, le diriger à son insu vers des sites différents de ceux visés. Et ainsi, de lui dérober tout type d’informations sensibles.
Ce type d’attaque peut être réalisé par :
* compromission du processus de résolution ;
* modification du trafic DNS ;
* ou compromission des données dans le cache d’un serveurs de noms.

Les réponses que cet article amènera viseront à :
* sécuriser le processus de résolution et en maîtriser les possibilités de modification ;
* limiter au strict minimum l’usage des requêtes récursives ;
* s’assurer de l’intégrité des transactions.

**Le déni de services**
Le déni de services distribué est une menace commune à tous les protocoles TCP/IP implémentés sur les serveurs accessibles de l’internet. En dehors des mesures de protections réseau (IPS) ou de répartition de charges, peu de réponses spécifiques à la configuration DNS peuvent être appliquées. Cependant, les mesures suivantes permettent limiter l’impact et l’implication des serveurs dns dans ces attaques :
* restriction des transferts de zone ;
* interdiction de toute récursion ;
* contrôle des requêtes simples ;
* restriction des notifications.

## 2. Architecture

Pour maitriser au mieux le DNS et son utilisation, nous fixons les règles suivantes :
* Aucune machine du réseau interne ne peut accèder à l’internet. Elles utilisent toutes un proxy HTTP pour le web ou un relais SMTP pour la messagerie;
* Aucune machine ne peut donc résoudre autre chose que le domaine `mondomaine.fr`.
Cela permet d’être sûr de pouvoir déployer une politique de sécurité maitrisable.

### 2.1 Les serveurs DNS et leur rôle
La base pour fixer une politique de résolution est donc de définir un périmètre et des règles d’accès :
* Un **serveur DNS cache interne** assure la résolution de tout type de requête issue d’une machine du réseau interne ;
* Un **serveur DNS SOA** assure la gestion du domaine de l’entreprise pour le réseau interne de l’entreprise. Ce serveur ne peut être sollicité que par le serveur de résolution ;
* Un **serveur DNS cache en DMZ** assure la résolution des requêtes sur les noms internet issues du serveur DNS cache interne ;
* Un **serveur DNS SOA externe** assure la gestion du domaine de l’entreprise pour les macines de l’internet. Ce serveur sera sollicitable par toute machine sur l’internet.

![Architecture DNS et rôles de chaque serveur](/assets/articles/archi-dns/archi.png)

### 2.2 Résolution d’une requête interne du domaine ou d’un sous-domaine de l’entreprise
Tout d’abord, le resolver envoie sa requête au serveur DNS référencé dans sa configuration. Ce serveur est un DNS cache qui vérifie que le resolver est habilité à demander des résolutions pour le domaine ou sous-domaine demandé via la mise en place d’ACL sur adresses IP (directive `acl`) et de vues (directive `view`). Le DNS cache ne contient aucune zone mais sait trouver le serveur maître de la zone interrogée (directive `forwarders`). Nous utilisons les fonctionnalités de retransmission sélective pour ce type de résolution (définition de zones de type forward et non maître ou esclave). Afin de préserver les serveurs maîtres au mieux des attaques, ceux-ci sont placés dans des DMZ et seuls les serveurs cache sont autorisés à y accéder.

### 2.3 Résolution d’une requête interne d’un domaine Internet
Le resolver interroge le serveur cache référencé. Le serveur cache vérifie que le resolver est habilité à résoudre les domaines inconnus (donc Internet). Le domaine interrogé n’étant pas connu par le serveur cache comme zone faisant l’objet d’une retransmission sélective, le serveur cache retransmet la requête au serveur cache délégué aux résolutions externes que nous avons pris soin de positionner dans une DMZ. Ici aussi, seuls les serveurs cache sont autorisés à y accéder.

En cas d’attaque (via une hypothétique mauvaise implémentation du contrôle d’état UDP sur notre pare-feu par exemple!), l’attaquant n’accédera qu’à un serveur en DMZ uniquement capable de résoudre des requêtes vers Internet.

### 2.4 Résolution d’une requête externe du domaine de l’entreprise
Dans ce cas, les requêtes proveniennent d’Internet vers un serveur que nous hébergeons. Bien entendu ce serveur est en DMZ. Étant donné le peu de sûreté que constitue Internet, il ne nous semble pas utile de mettre en place des habilitations pour les résolutions. Nous restreignons les données de notre domaine au strict minimum pour Internet. Le resolver trouve alors sa réponse dans le DNS que nous lui proposons, la requête ne doit jamais entrer dans l’entreprise.

## 3. Serveur DNS cache interne
### 3.1 Attention au poste de travail !
Comme nous le disions en introduction, la corruption de données de résolution est le problème majeur du DNS.

Et bien, la première attaque DNS est d’éviter toute requête DNS ! En effet, la résolution de noms dans les systèmes d’exploitation modernes impliquent des composants autres que les serveurs DNS.

Par exemple sous un système Microsoft Windows, le processus de résolution suit les étapes suivantes :
* vérification si on demande la résolution du propre nom de la machine ;
* présence du nom dans le fichier hosts (`%Systemroot%\System32\Drives\Etc\hosts`) ;
* DNS ;
* WINS ;
* broadcast réseaux ;
* LMHOSTS.

Ainsi, si vous modifier le contenu du fichier hosts, la chaîne de résolution DNS est corrompue. Toute la politique de sécurité DNS est déjà réduite à néant !

Cette méthode est utilisée par exemple par les vers de la lignée MYTOB [^2] qui font ainsi pointer des sites de type `symantec.com` ou `update.symantec.com` vers `127.0.0.1` et empêcher ainsi toute mise à jour de l’antivirus.

La solution est donc de s’assurer que les utilisateurs n’ont pas les droits administrateur et donc ne peuvent exécuter de processus pouvant modifier le fichier hosts. Idem pour ce qui est de l’accès aux paramètres DNS.

### 3.2 Configuration du serveur DNS cache interne
Une fois que le poste client nous semble correctement configuré, voyons la configuration du serveur de cache interne. Dans notre exemple, les machines du réseau interne sont dans le réseau `10.1.0.0/16` et le serveur cache interne a l’adresse `10.1.255.4`. 

**Les vues sous Bind**

Nos besoins nous conduiront dans le paragraphe suivant à vouloir faire varier les résultats des requêtes en fonction du type de client (ici PC normaux et machines proxies/pivots). Or, Bind nous donne le moyen de réaliser cela : les vues. Une vue est une configuration de Bind pour répondre à certains clients certains résultats grâce aux instructions suivantes :
* `acl` : permet de définir sous un nom un jeu de clients (adresses IP);
* `view` : définit une configuration complète pour un type de client;
* `match-clients` : instruction indiquant les clients à qui s’adressent une vue.

![Principes des vues DNS](/assets/articles/archi-dns/vues.png)

Au chapitre 2, nous avons défini différents types de clients au sein du réseau interne (machines standards et machines passerelles). Ces différents types de clients vont se traduire par 2 ACLs différentes :

**NB:** tous les fichiers de configuration sont disponibles sur le site [^3].

``` go
// ENTETE DU FICHIER NAMED.CONF du DNS CACHE INTERNE
// Definition des différents types de clients

// les proxies
acl "passerelles" { 10.1.255.3/32; };
// les machines du reseau interne de l entreprise
acl "reseaulocal" { 10.1.0.0/16; };
// le DNS cache en DMZ
acl "dns-cache-internet" { 10.255.1.4/32; };
// le DNS soa interne
acl "dns-soa" { 10.255.2.4/32; };

// localisation des fichiers de configuration
options { directory "/var/named"; 
version "unavailable"; };
```

À ces 2 types de clients vont correspondre 2 types de vues qui fourniront 2 types de résolution . Voici la vue fournie aux clients de type proxies ou passerelles.

```go
// Suite du FICHIER NAMED.CONF du DNS CACHE INTERNE
// vue s adressant aux proxies
view "passerelles" { 
    // machines a qui s'adressent cette vue. Ici les proxies de l'entreprise.
    match-clients { "passerelles"; };

    // en cas de requete faite sur un domaine non géré par ce serveur,
    // envoi des requêtes sur le DNS cache internet
    forward only;        
    forwarders { 10.255.1.4; };

    // requete sur le mondomaine.fr :
    // redirection de la requete vers le DNS SOA interne
    zone "mondomaine.fr" {
	  type forward;
	  forwarders { 10.255.2.4;};
          forward only;
	};

    // redirection identique pour les requetes sur la zone reverse
    zone "10.in-addr.arpa" {
	  type forward;
	  forwarders { 10.255.2.4; };
      forward only;
	};
};
```

![Résolution DNS d'un serveur proxy](/assets/articles/archi-dns/resolution-dns-proxy.png)

Les passerelles peuvent effectuer tout type de requête. Ces requêtes seront satisfaites de la maniêre suivante :
* requête sur le domaine `mondomaine.fr` : envoi d’une requête auprès du serveur maître interne (IP : `10.255.2.4`) ;
* requête sur tout autre domaine : envoi vers le serveur cache en DMZ (adresse IP `10.255.1.4`).

Voici ensuite la vue pour les postes lambda du réseau local :

```go
// Fin du FICHIER NAMED.CONF du DNS CACHE INTERNE
// vue s adressant aux PC du reseau interne de l entreprise
view "reseaulocal" {
        // Machines a qui s adressent cette vue. 
        // Ici, les machines lambda (PC) du reseau interne.
	match-clients { "reseaulocal"; };
      
        // requete sur le mondomaine.fr :
        // redirection de la requete vers le DNS SOA interne
	zone "mondomaine.fr" {
		type forward;
		forwarders { 10.255.2.4; };
                forward only;
	};
    
        // redirection identique pour les requetes sur la zone reverse
	zone "10.in-addr.arpa" {
		type forward;
		forwarders { 10.255.2.4; };
                forward only;
	};
};
```

**Note :** les zones de type forward ont été introduites en version 9.1.x de Bind.

![Resolution poste](/assets/articles/archi-dns/resolution-dns-poste-client.png)

Cette configuration ne permet de résoudre que des noms dans le domaine `mondomaine.fr`. Les autres noms de domaines ne sont résolus que pour les machines passerelles.

Cette mesure combinée à la fermeture de tous les ports réseaux (comme HTTP/S ou SMTP) pour les machines du LAN au niveau du firewall empêche toute capacité d’évasion par tunnel DNS autonome. Pour que l’évasion soit désormais possible, il faut que l’attaquant dispose du code d’authentification de l’utilisateur sur le proxy applicatif ce qui limite grandement la menace des attaques automatisées. Et nous sortons là du périmètre de la sécurisation du DNS.

### 4.1 Mise en sûreté des informations
Les informations contenues dans le DNS SOA interne font de ce DNS le coeur de notre système. En effet, il est le seul à contenir les données de résolution et doit à ce titre être le plus protégé. Ce DNS est placé derrière un pare-feu voire un IPS implémentant un contrôle d’état sur UDP performant. Des règles de sécurité sont mises en place pour n’autoriser que les DNS cache interne à interroger notre DNS SOA interne. Ces règles sont mises en place sur l’équipement de sécurité réseau et dans la configuration du DNS.

Ces restrictions limitent les risques de déni de services sur notre DNS SOA interne, le nombre de clients simultanés étant limité par le nombre de DNS cache.

### 4.2 Les mises à jour dynamiques
Certaines applications de l’entreprise peuvent nécessiter la mise en place des mises à jour dynamiques (serveur DHCP, contrôleur de domaine, etc.) sur notre DNS SOA. Dans ce cas, il est intéressant de créer des sous-domaines particuliers pour ces applications, celles-ci ne peuvent alors pas tout modifier dans notre DNS.

Par exemple, on peut créer le sous-domaine dhcp.mondomaine.fr sur notre DNS et autoriser le serveur DHCP à y effectuer ses mises à jour sans lui donner de droits sur mondomaine.fr. L’option `update-policy` permet de plus de limiter les opérations possibles sur la zone. Ainsi, nous pouvons n’autoriser le serveur DHCP à ne modifier que les enregistrements de type A, garantissant ainsi l’impossibilité de modification nos enregistrements de type NS par exemple.

L’utilisation de clef TSIG est également une sécurité à mettre en oeuvre autant que possible.

### 4.3 Création d’une clef pour mises à jour dynamiques
Nous commençons par mettre en place des clefs TSIG pour les serveurs utilisant les mises à jour dynamiques et acceptant d’utiliser ce type de clefs. Nous générerons notre clef avec l’outil dnssec-keygen. Prenons par exemple la mise en place d’une clef pour notre serveur DHCP: `dnssec-keygen -a HMAC-MD5 -b 512 -n HOST dhcp.mondomaine.fr`

Explication des options :
* L’option `-a` permet de choisir l’algorithme utilisé par la clef (ici HMAC-MD5) ;
* L’option `-b` est la longueur de la clef (ici 512 bits) ;
* L’option `-n` spécifie le type de clef créé (dans notre cas, il s’agit d’une clef de type HOST) ;
* Le dernier paramètre est le nom de la clef.

Nous obtenons deux fichiers du type `Kdhcp.mondomaine.fr.+157+55315.key` et `Kdhcp.mondomaine.fr.+157+55315.private` contenant chacun la clef. En effet, dans notre cas ces deux fichiers sont identiques. Les noms de ces fichiers sont toujours formés par la lettre K majuscule, suivie du nom de la clef, puis de l’identifiant de l’algorithme utilisé et un identifiant.

Le fichier en `.key` contient notre clef sous la forme:
```go
dhcp.mondomaine.fr. IN KEY 512 3 157 S5m+161iLtk6Y7+nK+8jpV1fll2AHLxN8SqVeZqzxQyg+L1187PbT5wO pteHcN4NdwO59t2TYZkpsbUocMv1+g==
```
et le fichier `.private` contient cette même clef mais sous la forme:
```go
Private-key-format: v1.2
Algorithm: 157 (HMAC_MD5)
Key: S5m+161iLtk6Y7+nK+8jpV1fll2AHLxN8SqVeZqzxQyg+L1187PbT5wOpteHcN4NdwO59t2TYZkpsbUocMv1+g==
```
Pour nos besoins, nous créons un nouveau fichier ne contenant que la clef. Ce fichier s’appelle `clefdhcp.key` et contient :
```go
secret "S5m+161iLtk6Y7+nK+8jpV1fll2AHLxN8SqVeZqzxQyg+L1187PbT5wOpteHcN4NdwO59t2TYZkpsbUocMv1+g==";
```
### 4.4 Configuration
Nous filtrons les adresses ip source via l’option `allow-query`.

```go
acl "dns-cache-interne" { 10.1.255.4/32; };
acl "updateservers" { 10.1.255.7/32; };

options { 
	// Répertoire où se trouvent les fichiers de zone
	directory "/var/named";

	// Modification du nom de version renvoyé
	version "unavailable";

	// Interdiction des transferts de zone
	allow-transfer{"none";};

	// Interdiction des notifications de mise à jour
	allow-notify {none;};

	// Autorisations de requêtes internes et pour le DNS cache
	allow-query {127.0.0.1; "dns-cache-interne";"updateservers";};

	// Pas de récursion
	recursion no;
};

// Définition de la clef du serveur DHCP
key "key.dhcp.mondomaine.fr" {
	algorithm hmac-md5;
	include "clefdhcp.key";
};

// Définition de la sous-zone maitre dhcp
zone "dhcp.mondomaine.fr" {
	type master;
	file "db.dhcp.mondomaine.fr";

	// Définition des droits de mise à jour (type A pour le serveur utilisant la clef dhcp)
	update-policy {
		grant key.dhcp.mondomaine.fr name dhcp.mondomaine.fr A ;
        };
	forwarders {};
};

// Définition de la zone maitre
zone "mondomaine.fr" {
	type master;
	file "db.mondomaine.fr";
	forwarders {};
};
```

## 5. Serveur DNS cache en DMZ
Ce serveur a pour vocation d’effectuer pour le compte du serveur DNS cache interne les résolutions de noms de domaines internet. Cette particularité nous permet de restreindre les clients pouvant le solliciter à ce seul serveur.

**Note :** si vous utilisez une version de Bind inférieure à 9.x, il faut prendre soin de se prémunir de 2 risques majeurs de corruption de caches:
* le glue fetching qui consiste pour un serveur, recevant un enregistrement NS sans enregistrement de type A, à chercher à obtenir cet enregistrement A entrainant des risques de corruption du cache,
* la prédiction du numéro de l’ID du message DNS [^5] qui rend le serveur sensible aux attaques de force brute.

Voici la configuration du serveur :
```go
// définition d une ACL pointant le DNS cache interne
acl "dns-cache-interne" { 10.255.1.4/32; };

options {
  // repertoire contenant les fichiers de configuration
  directory "/var/named";

  // aucun transfert de zone autorise
  allow-transfer{"none";};
  // seul le dns cache interne est autorisé à 
  allow-query { "dns-cache-interne"; };
  
  // pour BIND 8 : randomisation de l ID de message DNS 
  //use-id-pool yes; 
  // pour Bind 8 : pas de glue fetching
  //fetch-glue no;   
};

// Definition de la zone racine :
// Elle contient la liste des serveurs racines à qui le serveur va s adresser 
// pour commencer à resoudre les requetes.
zone "." {
  type hint;
  file "/var/named/named.root";
}
```
**Ports DNS et Firewall**
Voici un petit mémento sur les ports utilisés pour les requêtes DNS :
* envoi de la requête port > 1023 vers port 53 en tcp ou udp ;
* réponse à la requête : port 53 vers port > 1023 en tcp ou udp.

On dit généralement que l’udp est utilisée pour les requêtes simples et tcp pour les transferts de zones. Mais, en fait, en fonction de la taille de la réponse, tcp peut être obligatoire même pour les requêtes simples.

## 6. Serveur DNS SOA externe
Le serveur DNS Internet est celui le plus exposé en considérant le danger extérieur (nous ne reviendrons pas sur ce vaste sujet...). Il est donc important de bien lui appliquer les règles de sécurité appliquées à tout serveur disponible sur Internet. Au niveau de la configuration DNS, elle est très simple. Il suffit de créer une zone de type maître sur ce serveur et d’interdire toute récursion. Il faut ensuite remplir la zone avec les données devant être disponibles sur Internet.
``` go
options { 
	// Répertoire où se trouvent les fichiers de zone
	directory "/var/named";

	// Modification du nom de version renvoyé
	version "unavailable";

	// Interdiction des transferts de zone
	allow-transfer{"none";};

	// Interdiction des notifications de mise à jour
	allow-notify {none;};

	// Autorisations de requêtes
	allow-query {any;};

	// Pas de récursion
	recursion no;
};

// Définition de la zone maitre
zone "mondomaine.fr" {
	type master;
	file "db.mondomaine.fr";
	forwarders {};
};
```
![Résolution depuis Internet](/assets/articles/archi-dns/resolution-dns-depuis-internet.png)

**Note :** Nous pouvons fusionner physiquement les 2 serveurs DNS Internet (le cache et le serveur DNS internet). La configuration utiliserait alors le principe des vues en fonction de l’adresse appelante comme nous l’avons vu en chapitre 3 pour la configuration du DNS cache interne.

## 7. Les logs
Par défaut, le démon named envoie tous ses messages au syslog de la machine qui peut aussi recevoir les messages des autres démons du système. Le manque de lisibilité d’un tel syslog nuit de manière à la sécurité du DNS en gênant sa supervision.

Heureusement, il est possible de configurer les logs de named via des canaux de logs afin de, dans notre cas, rediriger certains types de messages dans des fichiers spécifiques. Named peut utiliser plusieurs canaux de logs en parallèle traitant les mêmes informations ou non. Dans notre exemple, nous utilisons deux canaux de logs, un premier pour les messages concernant les problèmes de sécurité et les transferts de zone et un second pour les autres messages et les transferts de zone (messages par défaut).

Ces lignes de configuration sont à placer dans les fichiers `/etc/named.conf` de tous les DNS.
``` go
logging {
   // Paramétrage du canal des messages de sécurité
   channel securitylogs {
       // Envoi vers le fichier dns_security.log avec roulement de 10 archives de 5Mo
           file "/var/log/named-sec.log" versions 10 size 5m;
       // Affichage de tous les messages (+messages debug si activation du mode debug)
           severity dynamic;
       // Affiche le nom de la catégorie du message
           print-category yes;
       // Affiche la sévérité du message dans les logs
           print-severity yes;
       // Affiche la date du message dans les logs
           print-time yes;
   };

   // Paramétrage du canal par défaut
   channel defaultlogs {
       // Envoi vers le fichier dns_default.log avec roulement de 10 archives de 5Mo
           file "/var/log/named-default.log" versions 10 size 5m;
       // Affiche les messages de sévérité "info" et supérieur
           severity info;
       // Affiche le nom de la catégorie du message
           print-category yes;
       // Affiche la sévérité du message dans les logs
           print-severity yes;
       // Affiche la date du message dans les logs
           print-time yes;
       };

   // Envoi des messages par défaut à notre canal defaultlogs
       category default { defaultlogs; };

   // Envoi des messages de transferts a nos canaux defaultlogs et securitylogs
       category xfer-in {  securitylogs; defaultlogs; };
       category xfer-out {  securitylogs; defaultlogs; };

   // Envoi des messages de sécurité à notre canal securitylogs
       category security { securitylogs; };
};
```
Il est également possible de créer un canal spécial pour les mises a jour dynamiques sur les serveurs utilisant ce service :

``` go
channel updatelogs {
           file "/var/log/named-update.log" versions 10 size 5m;
           severity dynamic;
           print-category yes;
           print-severity yes;
           print-time yes;
       };
category update { updatelogs; };
```
Voici deux exemples de messages lus dans le fichier de logs de sécurité :

``` 
Nov 25 10:34:57.910 security: info: client 192.168.9.9#1349: query (cache) denied
Nov 25 15:22:53.390 security: error: client 192.168.9.9#32776: zone transfer 'mondomaine.fr/IN' denied
```
Ces deux messages ont les significations suivantes :
* Le premier est une interdiction d’interrogation ;
* Le second est une interdiction de transfert de zone.

## 8. Conclusion
Comme nous avons pu le voir, la sécurisation du DNS passe avant tout par le fait de se poser les bonnes questions sur son utilisation : qui l’utilise ? pour quels types de résolution ? est-ce légitime ?

La réponse à ces questions sous l’angle de la sécurité nous a permis d’arriver aux solutions suivantes :
* une séparation des différents services DNS (résolution internet vs résolution du domaine interne) par spécialisation des serveurs ;
* une politique centralisée et maîtrisée d’accès à l’internet limitant le spectre de clients pouvant solliciter et donc potentiellement exploiter le DNS.

Une amélioration supplémentaire pourrait être l’utilisation de DNSSEC [^6] pour le contrôle d’intégrité et l’authentification des demandes de résolutions de noms et les réponses associées. Cette utilisation serait à implémenter au niveau du DNS SOA internet.

**Références :**

[^1]: [TUN] VUILLARD, V. Tunnel DNS : fuite d’information universelle. In:MISC 18, Mars-Avril 2005.
[^2]: [VER] TREND Micro System. Description du virus MYTOB.KG,
[^3]: [MISC23] BROCAS C., FARIN J.M.. fichiers de configuration des différents serveurs DNS décrits dans l’article.
[^4]: [BIND] Page d’accueil de BIND,
[^5]: [HEADER] RFC 1035, domain names - implementation and specification, chapitre 4.1.1
[^6]: [DNSSEC] RFC 4033, 4034 et 4035, Ressources DNSSEC
