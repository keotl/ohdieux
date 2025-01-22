FROM eclipse-temurin:21-jdk-alpine as build

RUN apk update
RUN apk add curl bash
RUN curl -fL "https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux-static.gz" | gzip -d > /usr/local/bin/cs
RUN chmod +x /usr/local/bin/cs
RUN cs install --dir /usr/local/bin scalac:3.5.1 sbt:1.10.2


WORKDIR /app
COPY build.sbt .
COPY project project
RUN sbt update

COPY src /app/src
RUN sbt playUpdateSecret
RUN sbt dist

FROM eclipse-temurin:21-jre-alpine

RUN apk add bash ffmpeg
WORKDIR /app
COPY --from=build /app/target/universal/*.zip .
RUN unzip *.zip -d ohdieux/

RUN mkdir -p /tmp/ohdieux /data
RUN chown 2000:2000 /tmp/ohdieux /data

USER 2000:2000
WORKDIR /data

CMD [ "/app/ohdieux/bin/ohdieux", \
  "-Dpidfile.path=/tmp/ohdieux.pid", \
  "-Dlogger.resource=prod-logback.xml", \
  "-Dbase_data_dir=/data/" \
  ]