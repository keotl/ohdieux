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


## Configuration avancée (pour développeurs) / Advanced Configuration (for developers)
### Exécution locale / Running Locally
**Oh**dieux peut être exécuté localement depuis un environnement Python.

**Oh**dieux can be run locally in a Python environment.

```bash
pipenv install --dev
pipenv run start
```

### Configuration
**Oh**dieux est parfaitement configurable dans les deux langues officielles, en conformité avec la loi sur les langues officielles. 
Le tableau ci-dessous est une liste exhaustive des paramètres d'environnement pouvant
être utilisés pour paramétriser le logiciel.

**Oh**dieux can be completely configured in both official languages, in compliance with the Official Languages Act.
The table below is a complete list of the supported environment variables.

| Propriété (FR)               | Property (EN)       | Description                                                                                                                                               |
|:-----------------------------|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| DELAI_RAFRAICHISSEMENT_CACHE | CACHE_REFRESH_DELAY | Délai au-delà duquel le flux RSS généré est considéré périmé et doit être regénéré. / Delay after which the cached RSS feed should be regenerated.        |
| STRATEGIE_CACHE              | CACHE_STRATEGY      | `"memory"`,`"redis"` Mécanisme de cache. Pour redis, `REDIS_URL` doit être fourni. / Caching provider. If using redis, `REDIS_URL` must also be provided. |

