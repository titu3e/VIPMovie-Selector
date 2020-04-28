# Telegram Movie Bot

## Usage

Get your token from [BotFather](https://telegram.me/botfather), store it in a
file named `TOKEN`, and keep it in the cloned repo folder.

Then `cd` into it and run `./filmBot.py` from an internet connected machine.

Or you can try it [here](http://telegram.me/vipmovieselectbot).

## Current implementation

Keeps track of what me and some friends watch in our movie group.

Directly curls webpages from IMDb.

Implements a basic search function, a like/import function, a random pick, and computes simple
charts of top liked features.

It locally stores actors, directors, genres and keywords of liked movies.

## In the future

The idea is to get tailored movie suggestions based on what information has been
stored. It is now based on IMDb's recommended feature, but I would like to implement a more refined system for modeling users taste.

## Depends

https://github.com/python-telegram-bot/python-telegram-bot
