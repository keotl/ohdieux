#!/bin/sh
set -e
cd api-spec
npm ci
npm run tsoa
npm run apiclient:generate
npm run test
