#!/usr/bin/env python3

###################################
# WHAT IS IN THIS EXAMPLE?
#
# This bot listens to every channel and every
# available message type. It prints all parsed
# events to STDOUT. This is the simplest bot
# in the set of examples.
###################################
### export KEYBASE_PAPERKEY="recall armed vicious wife flee bounce where tuna enlist turkey smart hungry check"
###################################
import requests
import asyncio
import logging
import os
import json
import random

from pykeybasebot import Bot
from pykeybasebot.types import chat1

from itertools import combinations
from requests import *

logging.basicConfig(level=logging.DEBUG)

class Handler:
    async def __call__(self, bot, event):
        if event.msg.sender.username != bot.username:
            channel = event.msg.channel
            msg = event.msg.content.text.body

            if "!evaluate" in msg:
                terms_list = []
                goodbad_list = []

                keyword = msg.split(" ")
                keyword.remove("!evaluate")
                companies = ["amazon", "duckduckgo", "github", "youtube"]
                companies_json = ["json/amazon.json", "json/duckduckgo.json", "json/github.json", "json/youtube.json"]
                for i in range(4):
                    if keyword[0] == companies[i]:
                        company_json = companies_json[i]
                with open(company_json, 'r') as json_file:
                    data = json_file.read()
                    tosdr = json.loads(data)
                    points = tosdr["points"]
                    for point in points:
                        terms_list += [tosdr["pointsData"][point]["title"]]
                        goodbad_list += [tosdr["pointsData"][point]["tosdr"]["point"]]

                emoji_list = [None] * len(goodbad_list)
                for x in range(len(goodbad_list)):
                    if goodbad_list[x] == "good":
                        emoji_list[x] = ':+1:'#'/U0001F44D'
                    elif goodbad_list[x] == "bad":
                        emoji_list[x] = ':-1:'#'/U0001F44E'
                    elif goodbad_list[x] == "neutral":
                        emoji_list[x] = ':neutral_face:'#'/U0001F636'

                goodctr = 0
                neutralctr = 0
                badctr = 0

                for y in range(len(goodbad_list)):
                    if goodbad_list[y] == "good":
                        goodctr += 1
                    elif goodbad_list[y] == "bad":
                        badctr += 1
                    elif goodbad_list[y] == "neutral":
                        neutralctr += 1

                for j in range(len(terms_list)):
                    await bot.chat.send(channel, str((j + 1)) + ". " + emoji_list[j]+ " " + terms_list[j])

                await bot.chat.send(channel, ':+1:' + ": " + str(goodctr) + ", " + ':neutral_face:' + ": " + str(neutralctr) + ", " + ':-1:' + ": " + str(badctr))

listen_options = {
    "local": True,
    "wallet": True,
    "dev": True,
    "hide-exploding": False,
    "filter_channel": None,
    "filter_channels": None,
}

bot = Bot(
    username="test200", paperkey=os.environ["KEYBASE_PAPERKEY"], handler=Handler()
)

asyncio.run(bot.start(listen_options))
