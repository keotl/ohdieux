# Déploiement autogéré

## Déploiement de base
Ce déploiement est adéquat pour un environment local. Voir [Considérations de
production](#considérations-de-production) pour configurer un
déploiment de production.

0. Créer l'image docker
```bash
docker build . -t ohdieux:latest
```
1. Créer un container docker
```bash
docker run --restart always \
  -p 8080:8080 \
  -e PORT=8080 \
  -e PUBLIC_URL="http://<my-accessible-ip>:8080" \
  -v ./data:/data \
  --name ohdieux \
  ohdieux:latest
```
2. Rendez vous au `http://localhost:8080/admin` pour ajouter de
   nouveaux programmes.

## Déploiement simple (avec archive média)
Ce déploiement sauvegarde les fichiers audio de chaque épisode découvert.
**Assurez-vous d'avoir beaucoup d'espace de disque disponible.***

```bash
docker run --restart always \
  -p 8080:8080 \
  -e PORT=8080 \
  -e PUBLIC_URL="http://<my-accessible-ip>:8080" \
  -e ARCHIVE_MEDIA=true \
  -e MANIFEST_SERVE_IMAGES=true \
  -e MANIFEST_SERVE_MEDIA=true \
  -v ./data:/data \
  --name ohdieux \
  ohdieux:latest
```

## Considérations de production
* Le tableau de bord d'administrateur est disponible sous le chemin
  `/admin` **sans authentification**. Assurez-vous de restreindre
  l'accès au routes sous `/admin/**` si votre serveur est exposé à l'internet.
  ```
  # exemple pour nginx
  location ~* /admin {
      return 403;
  }
  ```
  
* Par défaut, Ohdieux ajoute à sa base de données tous les programmes
  demandés sur la route `/rss`. Si vous utilisez la fonctionnalité
  d'archivage média, il est **fortement recommandé** de désactiver
  cette fonctionnalité en assignant la valeur `false` à la variable
  `SCRAPER_AUTO_ADD_PROGRAMME` pour éviter de remplir votre disque dur.

* Par défault, Ohdieux utilise une base de données SQLite. Considérez
  l'utilisation d'un autre pilote JDBC ou un _load balancer_ avec une
  fonction de cache pour servir un grand nombre de requêtes.


## Variables d'environnement
Les variables d'environnement sont définies dans [application.conf](/src/main/resources/application.conf).

| Environment variable        | Description                                                                               | Default value                             |
|-----------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------|
| PORT                        | Port d'écoute                                                                             | 9000                                      |
| HTTP_ADDRESS                | Address réseau d'écoute                                                                   | 0.0.0.0                                   |
| DATA_DIR                    | Dossier de base pour les données locales.                                                 | `./` localement, `/data/` dans docker.    |
| PUBLIC_URL                  | URL publique du serveur. (**Nécéssaire avec fonctionnalité d'archivage**)                 | _non spécifié_, ex. `https://example.com` |
| JDBC_DRIVER                 | Pilote de base de données. Pour le moment, seul `org.sqlite.JDBC` est supporté.           | `org.sqlite.JDBC`                         |
| JDBC_URL                    | Descriptif de connection pour la base de données (format JDBC)                            | `jdbc:sqlite:${DATA_DIR}ohdieux.db`       |
| JDBC_USERNAME               | Nom d'utilisateur pour la base de données (si requis)                                     | _non spécifié_                            |
| JDBC_PASSWORD               | Mot de passe pour la base de données (si requis)                                          | _non spécifié_                            |
| RC_BASE_URL                 | URL de base pour RC.                                                                      | `https://services.radio-canada.ca`        |
| USER_AGENT                  | Descriptif User-Agent                                                                     | Voir _application.conf_                   |
| ARCHIVE_MEDIA               | Activation de la fonction d'archivage (true/false)                                        | `false`                                   |
| ARCHIVE_BASEDIR             | Dossier de sauvegarde pour l'archivage (si activé).                                       | `${DATA_DIR}archive`                      |
| ARCHIVE_TEMP_DIR            | Dossier de sauvegarde pour téléchargements en cours                                       | `/tmp/ohdieux`                            |
| ARCHIVE_PROGRAMME_BLACKLIST | List de programmes à ne jamais archiver.                                                  | `[]`                                      |
| SCRAPER_REFRESH_INTERVAL    | Intervalle de rafraîchissement en secondes.                                               | `3600`                                    |
| SCRAPER_MAX_EPISODES        | Nombre maximal d'épisodes à sauvegarder (par programme).                                  | `500`                                     |
| SCRAPER_AUTO_ADD_PROGRAMME  | Activer l'ajout automatique de chaque programme demandé sur la route `/rss` (true/false). | `true`                                    |
| MANIFEST_SERVE_IMAGES       | Servir les fichiers images depuis l'archive locale. (true/false)                          | `false`                                   |
| MANIFEST_SERVE_MEDIA        | Servir les fichiers audio depuis l'archive locale. (true/false)                           | `false`                                   |
| MANIFEST_IMAGE_BASE_URL     | Configuration manuelle de l'URL de base pour les images à servir (déploiements avancés)   | `${PUBLIC_URL}/media/image/`              |
| MANIFEST_AUDIO_BASE_URL     | Configuration manuelle de l'URL de base pour les fichiers audio (déploiement avancés)     | `${PUBLIC_URL}/media/audio/`              |



