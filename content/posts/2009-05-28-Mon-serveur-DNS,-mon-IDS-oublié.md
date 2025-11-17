---
title: Article MISC mai 2007 - Mon serveur DNS, mon IDS oublié
date: 2009-05-28
---

_Cet article est issu de l’article publié dans le numéro de **MISC n°31 de Mai 2007**. J’en suis l’auteur (christophe.brocas@free.fr). Tous droits réservés à MISC._

Je le poste ici car l’idée d’utiliser son serveur DNS semble être dans l’actualité du monde de la détection d’intrusions.

![](/assets/articles/dns-mort1.jpg)

# Mon serveur DNS, mon IDS préféré

*Christophe Brocas, christophe.brocas@free.fr*

Le Système d’Information (SI) des entreprises est un capital de ressources à protéger des attaques et, si une attaque réussit, la compromission et les évasions de données doivent être détectées le plus tôt possible. Pour détecter des postes compromis sur le réseau de l’entreprise, des solutions complexes et onéreuses sont souvent proposées aux Directeurs Informatiques (DSI) mais le plus souvent, peu de solutions de détection anti-intrusions sont effectivement en place. Or, la bonne compréhension à la fois de son architecture et du comportement des codes malicieux présents sur les postes compromis permet de proposer une première réponse élégante, peu couteuse et efficiente à cette problématique.

## 1. Introduction

### 1.1 Compromission de postes : une détection, quelle détection ?

Afin de sécuriser son SI, une entreprise doit déployer une interconnexion applicative filtrée par des proxies et des serveurs dédiées (exemples : filtrage http/smtp, relais dns) afin de pouvoir fixer des règles de sécurité consistantes.

Cependant, une fois cette architecture déployée, la majorité des entreprises ne semble pas se préoccuper des tentatives de contournement/d’accès direct à l’extérieur depuis un poste du LAN compromis. Elles se reposent généralement sur les différentes alertes que peuvent remonter les solutions d’antivirus postes et serveurs.

Or, si les protections amont de filtrages des flux HTTP/SMTP sont utiles, la détection des postes compromis est nécessaire tant sur le plan de l’intégrité des données de son SI que sur le plan de la responsabilité de l’entreprise qui pourrait ainsi fournir, par exemple, une base à des réseaux de postes zombies.

### 1.2 Avoir un IDS sans le savoir

La solution ? L’analyse des serveurs applicatifs est un moyen simple de connaître les compromissions potentielles dans son LAN. Les logs du serveur DNS et, dans une moindre mesure, ceux du pare-feu sont des sources de données disponibles pour effectuer cette veille anti-intrusion.

Concentrons-nous sur le DNS : comment diable un serveur DNS peut-il nous révéler les intrusions déjà effectuées sur son réseau ? Et les réponses sont :

* comprendre le comportement des différents types de codes malicieux présents sur les postes compromis ;
* en déduire les types de requêtes DNS pouvant être émis par ces codes ;
* en fonction de ces profils, analyser les logs du serveur DNS et isoler les postes susceptibles d’être compromis.

## 2. Architecture à base de proxies et de relais : un pré-requis nécessaire

Mais, attention, dans les logs d’un serveur DNS, rien ne distingue une requête émise par un poste de celle émise par un autre. Le seul moyen de stigmatiser une requête émise par un poste en particulier est de pouvoir définir le comportement normal d’un poste en termes de requêtes DNS. Et ce, par rapport à celui, différent, des serveurs de type proxies ou relais.

### 2.1 Flux vers l’Internet : "authentication required" !

Les flux émis vers l’Internet depuis un poste de travail sont nombreux :

* émis consciemment par l’utilisateur : envoi d’email, navigation sur le web ou téléchargement de fichiers etc ;
* mais aussi émis de manière invisible pour l’utilisateur : mise à jour du système d’exploitation, rapatriement de mises à jour antivirales etc .

Et je ne parle que des flux légitimes !

![](/assets/articles/dns-ids-oublie/trame11.jpg)
_**Figure 1 :** architecture proxies et serveurs relais_

Et pour être reconnus comme légitimes, l’ensemble de ces flux doivent être soumis à habilitation. Pour cela, il faut que ces flux soient reroutés de manière systématique vers des équipements de filtrage nécessitant une habilitation, à savoir les proxies ou serveur relais. Habilitation que devra renseigner l’utilisateur pour chaque type de flux.

### 2.2 Proxies et relais, uniques émetteurs de requêtes DNS vers Internet

Les machines proxies ou relais se doivent, pour être utilisées, d’exiger de l’utilisateur une authentification. Cela se traduit par des demandes d’identification HTTP par le proxy HTTP ou l’utilisation de SMTP AUTH pour l’envoi de mail via le serveur SMTP de votre entreprise. Les flux émis par les postes vers Internet sont alors authentifiés, donc moins sujet à être vecteur d’attaques.

![](/assets/articles/dns-ids-oublie/trame31.jpg)
_**Figure 2 :** étapes d’une requête HTTP_

Le gain de cette architecture en termes de détection d’intrusion ? Tout le trafic émis par les postes à destination de l’Internet est dans un premier temps redirigé vers ces machines intermédiaires. Les requêtes DNS de résolution de domaines internet ne sont alors plus émises que par ces équipements proxies et relais :

* En effet, afin de pouvoir router, par exemple, les requêtes HTTP vers `google.fr` émises par un poste (point 1 sur la figure 2) ;
* Le proxy de l’entreprise demande une résolution DNS de type A sur le domaine `google.fr` (point 2) pour le compte de ce poste ;
* La requête peut ensuite être émise vers le serveur HTTP cible (point 3).

**NB :** Il en est de même pour les envois de mails où le serveur SMTP joue le rôle du proxy HTTP.

Comme vous pouvez le voir, grâce à cette architecture centralisée et maîtrisée, les logs de votre serveur DNS deviennent de manière mécanique des sources fiables de données de détection d’intrusion : toute demande de résolution DNS d’un domaine internet émise par un poste lambda peut être considérée comme une alerte d’une compromission potentielle.

## 3. Configuration du serveur DNS Bind

### 3.1 Configuration par défaut : état des lieux

Les configurations figurant dans cet article décrivent la configuration d’un serveur DNS Bind et ont été testées avec un serveur Bind en version stable 9.3.2 sous Ubuntu 6.06.

La configuration par défaut d’un serveur DNS Bind ne collecte pas dans ses fichiers de logs les requêtes émises par les clients DNS. En effet, ces requêtes peuvent générer beaucoup d’écritures dans ces fichiers dont la taille peut donc augmenter rapidement. Nous allons donc utiliser la gestion automatique des fichiers de logs fournie par Bind, gestion améliorée depuis la version 9.3 par la gestion d’une taille maximale de fichiers de logs. Une présentation des options de logging de Bind a été faite dans un article précédent de MISC.

### 3.2 Collecte des requêtes clientes dans les logs de Bind

Voici un exemple de définition d’un channel permettant de collecter les requêtes émises par les clients :

```python
# Declenchement du log des requetes au demarrage de Bind
querylog;

# paragraphe definissant le logging
logging {
   // Parametrage du canal des requetes
   channel querieslogs {
       // Envoi vers le fichier queries.log avec roulement de 10 archives de 20Mo
              file "queries.log" versions 10 size 20m;
       // Affiche la date du message dans les logs
              print-time yes;
       // Affiche le nom de la categorie du message
              print-category yes;
   };

   // Envoi des requetes dans notre canal querieslogs
       category queries { querieslogs; };
};
```

Des fichiers de configuration complets pour chaque type de serveur (cache interne, cache internet, maitre interne et maitre internet avec des sections de logs complètes sont disponibles sur le site de MISC. De plus, vous trouverez la documentation exhaustive des options de log de Bind en ligne sur le site du logiciel.

## 4. Que chercher dans les logs ?

### 4.1 Topologie du comportement réseaux des codes malicieux

Un poste de travail compromis par un code malicieux a pour vocation de devenir une source d’informations émises à destination de serveurs externes, ou une source d’attaques pouvant être pilôtées ou pas depuis Internet. Dans les deux cas, une communication vers des serveurs externes tentera d’être initiée. Ces serveurs peuvent être des cibles d’attaques (spams, dénis de services distribuées), des serveurs de contrôle fournissant des instructions aux codes malicieux distribuées ou bien des serveurs de collecte d’informations usurpées à l’utilisateur du poste.

### 4.2 Requêtes DNS émises par des codes malicieux

Ils existent deux grands types de requêtes :

* les requêtes de type `MX` qui sont émises par les moteurs d’envoi de spams et de virus qui sont lancés sur les postes une fois compromis. De même, ces requêtes servent à ces codes malicieux pour se propager via email. Ce type de requête fournit le nom et l’adresse IP du(des) serveur(s) SMTP réceptionnant pour le domaine passé en paramètre ;
* les requêtes de type `A` représentent la majeure partie des requêtes restantes. Ces requêtes peuvent alors correspondre à des demandes de résolution de noms de futures cibles, de serveurs de téléchargement de nouveaux codes malicieux (ou de mises à jour) ou encore de sites fournissant des ordres aux codes malicieux(serveurs IRC par exemple) .

Pour les requêtes `MX`, on peut en avoir la trace pas plus loin que dans sa messagerie. Exemple d’entête de spam dans la BAL de votre serviteur :

```python
[...]
Received: from 200.253.154.11 (HELO data-app.com) (200.253.154.11)
  by mrelay5-1.free.fr with SMTP; 14 Dec 2006 19:44:31 -0000
Message-ID: <01c71fb7$588313d0$0200a8c0@servidor>
Reply-To: "Kalpana Lo" 
From: "Kalpana Lo" 
To: "Charles Chickering" 
Subject: Re:
[...]
```

On y voit un mail émis directement depuis un poste sur l’Internet vers le serveur `MX` de l’hébergeur de ma BAL. Cette émission a donc fait l’objet d’une demande de résolution `MX` pour le domaine `free.fr` sur le serveur DNS du poste internet.

## 5. Exploitation des logs DNS

### 5.1 Extraction des données

```bash
$ egrep -v -i "@IP1|@IP2" /var/log/queries.1og | egrep -v -i mondomaine.fr
```

La ligne de commandes précédente permet :

* d’isoler l’ensemble des requêtes émises par les postes de travail (premier grep) ;
* demandant une requête sur un domaine différent du domaine de l’entreprise ici nommé mondomaine.fr (second grep).

Les données produites par cette commande correspondent à une liste d’adresses IP ayant un comportement DNS anormal selon les critères décrit dans le [chapitre 4](#42-requêtes-dns-émises-par-des-codes-malicieux) :

```
[...]
22-Jan-2007 22:55:24.978 queries: client 192.168.0.190#32788: query: google.fr IN A +
22-Jan-2007 22:55:49.228 queries: client 192.168.0.190#32788: query: hotmail.com IN MX +
[...]
```

On voit dans l’exemple ci-dessus un poste interne d’adresse IP `192.168.0.190` demander au DNS l’adresse IP de google.fr ainsi que celle du serveur SMTP gérant le domaine `hotmail.com`. Or, ces deux requêtes ne devraient jamais être émises par un poste du LAN car elles portent sur un domaine différent de celui de l’entreprise.

En effet, ces deux requêtes DNS devraient avoir été émises respectivement par le proxy HTTP et par le relais de messagerie de l’entreprise. Ces deux machines ayant auparavant demandé son habilitation HTTP ou l’utilisateur de messagerie à l’utilisateur du poste.

**NB :** On peut bien entendu spécialiser cette ligne de commandes pour obtenir soit les requêtes de type `MX` soit les requêtes de type `A`.

### 5.2 Faux positifs ? Explications et actions correctrices

Nous avons décrit dans le chapitre 2 un [pré-requis ambitieux](#2-architecture-à-base-de-proxies-et-de-relais--un-pré-requis-nécessaire) qui était que toutes les communications ou tentatives de communication vers Internet émises par les postes de travail passaient par un proxy ou une machine relais. Or, la première analyse que vous allez mener sur les données extraites des logs de votre serveur DNS risque fort de plus vous mettre sur la trace de postes lançant des Windows Update que sur celle de postes zombies (du moins je l’espère pour votre LAN ;-) ).

Vos premières actions vont donc être de travailler sur ces mécanismes légitimes s’exécutant sur vos postes et émettant des requêtes vers l’Internet :

* de forcer le passage par proxy des actions qui le peuvent ;
* d’inactiver les mécanismes s’exécutant mais finalement ne le devant pas ;
* de noter les mécanismes devant absolument exécuter des connexions externes directes afin de les exclure des remontées des logs DNS. Notez bien que ce type de connexion devrait être rarissime car étant anormales en termes de politique de sécurité.

### 5.3 Gestion des alarmes

La liste des adresses IP ainsi remontées par la scrutation du fichier queries.log permet aux administrateurs des postes et au responsable sécurité de déclencher les actions appropriées.

Parmi elles, on peut lister les quelques actions suivantes :
* mise hors réseau du poste incriminé ;
* recherche du code malicieux ;
* recherche de l’explication de la compromission : manque de suivi des mises à jour antivirales, mise en ligne du poste directement sur le net (ex: à domicile), contournement de la politique de sécurité etc ;
* remasterisation du poste avec restauration des données sauvegardées à une date antérieure à la compromission si la date est identifiée ;

## 6. Limites et pistes d’améliorations 

### 6.1 Limites

Le processus de recherche de postes compromis que nous venons de décrire possède des limites liées au fait que nous travaillons sur le serveur DNS.

Les limites majeures viennent du fait que l’on suppose que le code malicieux n’utilisera pas de données d’authentification dérobées à l’utilisateur du poste. Ainsi, l’émission de mails en SMTP authentifié à travers le relais SMTP de l’entreprise. Idem pour l’utilisation du proxy HTTP de l’entreprise pour attaquer un site extérieur ou récupérer des ordres d’un serveur de synchronisation.

La remarque que l’on peut faire est que la majorité des codes malicieux sont conçus pour travailler sur des architectures ouvertes (DNS/SMTP/HTTP ouverts vers l’extérieur).

### 6.2 Pistes d’amélioration

Elles sont de deux ordres : exploitabilité de la solution et consolidation des données DNS avec les tentatives d’accès direct à l’extérieur par adresses IP.

L’exploitabilité de cette solution serait de travailler sur l’enchainement des opérations de recherche dans les fichiers de logs, cyclage, compression et suppression de ces fichiers.

Pour ce qui est de la consolidation, il faudrait déclencher de telles recherches sur les rejets du Firewall concernant des requêtes en provenance de postes en plan d’adressage interne (ex: `10.0.0.0/8`) à destination d’adresses externes (vers l’internet donc).

## 7. Conclusion

Comme nous venons de le voir, une architecture qui permet de bien maîtriser les flux de données couplée à une analyse des logs de son (ses) serveur(s) DNS permet de disposer d’une sonde de détection de postes compromis. Cette solution a l’avantage d’être légère, non structurante et ... ne coûte rien ! Cela n’empêche en aucun cas le RSSI ou le DSI de doter l’entreprise de solutions plus complète (et complexe), intrusive et chère.
