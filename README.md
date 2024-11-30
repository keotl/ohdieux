# **Oh**dieux
**Oh**dieux est un convertisseur de balados de l'application
Radio-Canada **Oh**dio vers un flux RSS standard. Cela permet l'écoute
de ces émissions dans d'autres applications spécialisées dans la
gestion de balados, telles que *Apple Podcasts*.

**Oh**dieux is a podcast format converter to convert Radio-Canada
**Oh**dio podcasts to a standard RSS feed. This allows the podcasts to
be consumed in any third-party app, such as Apple Podcasts.

## Guide d'utilisation / Getting Started
1. Rendez-vous au [https://ohdieux.ligature.ca](https://ohdieux.ligature.ca).
   Head over to [https://ohdieux.ligature.ca](https://ohdieux.ligature.ca).
2. Prenez note du code d'émission sur le site de Radio-Canada **Oh**dio.
   Write down the programme number on Radio-Canada **Oh**dio.
   [Instructions](/ohdieux/views/instructions.png)
3. Copiez le lien RSS généré par le site pour votre émission dans votre application de balados.
   Copy the generated RSS link into your podcasts application.

## FAQ
- Q: Chaque épisode apparaît plusieurs fois dans mon lecteur de balados! 
  Each episode is duplicated multiple times in my podcast player!

  R: Chaque entrée correspond à un fichier audio différent. Utilisez
  l'option « Numéroter segments » pour rendre cette distinction explicite.

  A: Each feed entry corresponds to a separate audio file. Use the
  "Tag segment numbers" option to make this explicit.


## Déploiement auto-géré (avancé) / Self-hosted deployment (advanced)
Ohdieux a été réécrit pour simplifier le deploiement local. En mode
local, Ohdieux offre une fonctionnalité d'archivage de média
(désactivé par défaut). Voir [DÉPLOIEMENT.md](/docs/DÉPLOIEMENT.md)
pour débuter.

Ohdieux has been rewritten to improve self-hosted deployments. When
deployed locally, Ohdieux supports media archival (disabled by
default). See [DEPLOYMENT.md](/docs/DEPLOYMENT.md) to get started.
