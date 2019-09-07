#!/usr/bin/env python3

###################################
# WHAT IS IN THIS EXAMPLE?
#
# This bot listens to every channel and every
# available message type. It prints all parsed
# events to STDOUT. This is the simplest bot
# in the set of examples.
###################################
import requests
import asyncio
import logging
import os
import json
import random
from bs4 import BeautifulSoup
from quiz_data import *

from pykeybasebot import Bot
from pykeybasebot.types import chat1

logging.basicConfig(level=logging.DEBUG)
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

isQuiz = False
quizQCount = 0
quizQuestions = []
temp_pic = '/Users/histo/Documents/Github/keybase-python-bot/tmp.jpg'

class Handler:
    async def __call__(self, bot, event):
        if event.msg.sender.username != bot.username:
            channel = event.msg.channel
            msg = event.msg.content.text.body
                
            #help function    
            if "!helpmemydude" in msg:
                await bot.chat.send(channel, "*Here are some commands you can use:* \n `!sendmeme` to send a meme \n " + 
                "`!quizme` to quiz yourself about security and privacy \n `!ask` to ask a question about security \n " +
                "`"
                "`!virusgame` to learn more about viruses and cybersecurity :slightly_smiling_face: ")
            
            #meme function
            elif "!sendmeme" in msg:
                keyword = msg.split(" ")
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                #"https://www.reddit.com/r/" + keyword[1]+ "/search.json?q=" + keyword[2] + "&restrict_sr=1"
                r = requests.get("https://www.reddit.com/r/{}/search.json?q={}&restrict_sr=1".format(keyword[1], keyword[2]), headers = headers)
                jsonBody = json.loads(r.text)
                children = jsonBody["data"]["children"]

                if len(children) > 0:
                    child = children[random.randint(0,len(children) - 1)]["data"]
                    url = child["url"]
                    if url.endswith('.jpg') or url.endswith('.png'):
                        print('Sending picture ' + child["title"] + ' from ' + url)
                        r = requests.get(url)
                        with open(temp_pic, 'wb') as f:
                            f.write(r.content)
                        await bot.chat.attach(channel, temp_pic, "meme")
                        os.remove(temp_pic)

            #quiz function
            elif msg == "!quizme":
                quizQCount = 1
                isQuiz = True
                quizQuestions = list(questions)
                #mix questions
                for i in range(100):
                    randint1 = random.randint(0,len(quizQuestions) - 1)
                    randint2 = random.randint(0,len(quizQuestions) - 1)
                    temp = quizQuestions[randint1]
                    quizQuestions[randint1] = quizQuestions[randint2]
                    quizQuestions[randint2] = temp

                print(questions[quizQCount])

            #answers security questions
            elif "!ask" in msg:
                answered = False
                text = ""
                numParas = 3
                paraCount = 0
                words = msg.split(" ")
                if words[0] == "!ask":
                    search = msg[5:]
                    print(search)
                    r = requests.get("https://www.priv.gc.ca/en/search/?t={}&Page=1".format(search))
                    c = r.content
                    soup = BeautifulSoup(c, features="lxml")
                    title = soup.findAll("h2", {"class": "item-title"})

                    keyword = search.split(" ")[2].lower()

                    for i in range(len(title)):
                        infoPage = title[i].a["href"]
                        r = requests.get(infoPage)
                        c = r.content
                        soup = BeautifulSoup(c, features="lxml")
                        para = soup.findAll("p")
                        for p in para:
                            if keyword in p.text.lower() and p.findChild() is None:
                                print(p.text)
                                text += p.text.replace(keyword, "`" + keyword + "`")\
                                              .replace(keyword[0].upper() + keyword[1:], "`" + keyword + "`")\
                                              .replace(keyword + "s", "`" + keyword + "`") + "\n\n"
                                paraCount+=1
                                if paraCount == numParas:
                                    answered = True
                                    break
                        if answered:
                            await bot.chat.send(channel, "*Information on " + keyword + ":* " + text)
                            break



listen_options = {
    "local": True,
    "wallet": True,
    "dev": True,
    "hide-exploding": False,
    "filter_channel": None,
    "filter_channels": None,
}

bot = Bot(
    username="mydude", paperkey=os.environ["KEYBASE_PAPERKEY"], handler=Handler()
)

asyncio.run(bot.start(listen_options))