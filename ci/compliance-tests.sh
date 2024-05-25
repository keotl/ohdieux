#!/bin/sh
set -e
apk add openjdk21
cd api-spec
npm ci
npm run tsoa
npm run apiclient:generate
npm run test
