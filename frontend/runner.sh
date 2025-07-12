#!/bin/bash
set -e

set -x

npm install

npm run build

npm start
