# Self-hosted Deployment

## Basic Deployment
This setup is fine for simple local deployments. See [Production
Considerations](#production-considerations) to configure a production
deployment.

0. Build the docker image.
```bash
docker build . -t ohdieux:latest
```
1. Run a basic docker installation.
```bash
docker run --restart always \
  -p 8080:8080 \
  -e PORT=8080 \
  -e PUBLIC_URL="http://<my-accessible-ip>:8080" \
  -v ./data:/data \
  --name ohdieux \
  ohdieux:latest
```
2. Head over to `http://localhost:8080/admin` to start adding programmes.

## Simple Deployment (with media archival)
This deployment will save the audio files for every episode.
**Ensure that you have a large amount of hard drive space.***

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

## Production Considerations
* The admin dashboard is available on `/admin` **without any
  authentication**. Therefore, if exposing to the internet, you should
  forbid unauthenticated requests to `/admin/**`. 
  ```
  # nginx example
  location ~* /admin {
      return 403;
  }
  ```
  
* By default, Ohdieux is set to start tracking every queried
  manifest. If you are using the media archive, it is **highly
  recommended** to disable this setting by setting
  `SCRAPER_AUTO_ADD_PROGRAMME` to `false` to avoid filling up your
  hard drive.

* By default, Ohdieux uses an SQLite database. Consider using another
  JDBC driver or a caching load balancer if serving a large number of
  requests.


## Environment Variables
Environment variables are defined and used in [application.conf](/src/main/resources/application.conf).

| Environment variable        | Description                                                                       | Default value                       |
|-----------------------------|-----------------------------------------------------------------------------------|-------------------------------------|
| PORT                        | Listening port                                                                    | 9000                                |
| HTTP_ADDRESS                | Binding address                                                                   | 0.0.0.0                             |
| DATA_DIR                    | Global default data directory.                                                    | `./` locally, `/data/` in docker.   |
| PUBLIC_URL                  | Public-facing base URL. (**Required if using archive**)                           | `unset`, e.g. `https://example.com` |
| JDBC_DRIVER                 | Database driver class-name. Currently, only `org.sqlite.JDBC` is supported.       | `org.sqlite.JDBC`                   |
| JDBC_URL                    | Database connection string (JDBC format)                                          | `jdbc:sqlite:${DATA_DIR}ohdieux.db` |
| JDBC_USERNAME               | Database username (if required)                                                   | `unset`                             |
| JDBC_PASSWORD               | Database password (if required)                                                   | `unset`                             |
| RC_BASE_URL                 | Base RC API URL                                                                   | `https://services.radio-canada.ca`  |
| USER_AGENT                  | User-Agent string                                                                 | See _application.conf_              |
| ARCHIVE_MEDIA               | Whether to download discovered audio files (true/false)                           | `false`                             |
| ARCHIVE_BASEDIR             | Where to save audio/image files (if archive is enabled).                          | `${DATA_DIR}archive`                |
| ARCHIVE_TEMP_DIR            | Where to save in-progress downloads.                                              | `/tmp/ohdieux`                      |
| ARCHIVE_PROGRAMME_BLACKLIST | List of programmes for which to ignore archive setting.                           | `[]`                                |
| SCRAPER_REFRESH_INTERVAL    | Scraping interval in seconds.                                                     | `3600`                              |
| SCRAPER_MAX_EPISODES        | Max number of episodes to scrape per programme.                                   | `500`                               |
| SCRAPER_AUTO_ADD_PROGRAMME  | Whether to automatically start tracking every queried programme (true/false).     | `true`                              |
| MANIFEST_SERVE_IMAGES       | Whether to serve manifest images from local archive or upstream CDN. (true/false) | `false`                             |
| MANIFEST_SERVE_MEDIA        | Whether to serve audio files from archive instead of upstream CDN. (true/false)   | `false`                             |
| MANIFEST_IMAGE_BASE_URL     | Override image archive public URL. (Advanced deployments only.)                   | `${PUBLIC_URL}/media/image/`        |
| MANIFEST_AUDIO_BASE_URL     | Override audio archive public URL. (Advanced deployments only.)                   | `${PUBLIC_URL}/media/audio/`        |



