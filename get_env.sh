#!/bin/sh
heroku config:get DATABASE_URL -a sleepy-plains-10293 -s > .env

# This bash script deletes and recreates the env file. This is so that the app always has the latest config var as heroku updates the credentials.

