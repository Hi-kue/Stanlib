#!/usr/bin/bash

@echo off

read -p "Enter PROXY: " $PROXY
read -p "Enter MONGO_URI: " $MONGO_URI
read -p "Enter MONGO_DB: " $MONGO_DB
read -p "Enter MONGO_COLLECTION: " $MONGO_COLLECTION
read -p "Enter MONGO_USER: " $MONGO_USER
read -p "Enter MONGO_PASS: " $MONGO_PASS

cat <<EOL > .env
PROXY="$PROXY"

# MongoDb Configs
MONGO_URI="$MONGO_URI"
MONGO_DB="$MONGO_DB"
MONGO_COLLECTION="$MONGO_COLLECTION"
MONGO_USER="$MONGO_USER"
MONGO_PASS="$MONGO_PASS"
EOL

@echo on

echo "Environment variables successfully written to .env file"

<< ////
# The script will prompt you to enter the values for the environment variables and
# write them to a  .env  file.

# To run the script, execute the following command:
# bash write_env.sh or ./write_env.sh

# The script will prompt you to enter the values for the environment variables,
# which a sample can be found in .env.sample.
////