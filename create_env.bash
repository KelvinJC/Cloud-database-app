# A bash script. Not useful in this project but I'm keeping it.


#!/bin/bash
filename='.env'
# Create an empty file
touch $filename
# Check if the file exists or not
if [ -f $filename ]; then
   rm .env
   echo "$filename is removed"
# Get config var from heroku app 
heroku config:get DATABASE_URL -a sleepy-plains-10293 -s >> .env
fi

# This bash script deletes and recreates the env file. This is so that the app always has the latest config var as heroku updates the credentials.