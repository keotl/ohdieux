name := """ohdieux"""
organization := "ca.ligature"

version := "1.0-SNAPSHOT"


lazy val root: Project = (project in file("."))
  .enablePlugins(PlayScala)
  // Use sbt default layout
  .disablePlugins(PlayLayoutPlugin)

scalaVersion := "3.5.1"

libraryDependencies += guice
libraryDependencies += "org.scalatestplus.play" %% "scalatestplus-play" % "7.0.1" % Test

libraryDependencies += "com.softwaremill.sttp.client4" %% "core" % "4.0.0-M6"

// libraryDependencies += "redis.clients" % "jedis" % "5.2.0"

libraryDependencies += jdbc
libraryDependencies += "org.playframework.anorm" %% "anorm" % "2.7.0"

libraryDependencies += "org.postgresql" % "postgresql" % "42.7.4"
libraryDependencies += "org.xerial" % "sqlite-jdbc" % "3.46.1.3"

libraryDependencies += "org.apache.commons" % "commons-text" % "1.12.0"

// Adds additional packages into Twirl
//TwirlKeys.templateImports += "ca.ligature.controllers._"

// Adds additional packages into conf/routes
// play.sbt.routes.RoutesKeys.routesImport += "ca.ligature.binders._"

// Packaging
topLevelDirectory := None
