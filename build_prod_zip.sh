#!/bin/bash

# Prepare a .zip bundle for easy transfer to deploy destination

# Create folder with all the relevant production files
mkdir prod && cp requirements.txt prod/ \
           && cp start_bot.py prod/ \
           && cp -r data/ prod/ \
           && mkdir prod/bot \
           && cp -r bot/*.py prod/bot \

# Remove the token file if exists
TOKEN_LOC=prod/bot/token.py
if [ -f "${TOKEN_LOC}" ]; then
    rm ${TOKEN_LOC}
fi

# Remove old zip folder if exists, otherwise removed files persist
if [ -f prod.zip ]; then
    rm prod.zip
fi

# Zip
zip -r prod.zip prod

# Remove the temp file
rm -rf prod
