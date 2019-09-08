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
from getFromGoogle import *
from getFromReddit import *

from pykeybasebot import Bot
from pykeybasebot.types import chat1

logging.basicConfig(level=logging.DEBUG)
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

temp_pic = '/Users/histo/Documents/Github/keybase-python-bot/tmp.jpg'
companies = []

class Handler:
    isQuiz = False
    async def __call__(self, bot, event):
        if event.msg.sender.username != bot.username:
            channel = event.msg.channel
            msg = event.msg.content.text.body
            msg_id = event.msg.id

            if "!helpmemydude" in msg:
                await bot.chat.send(channel, "*Here are some commands you can use:* \n `!sendmeme` to send a meme \n " +
                "`!quizme` to quiz yourself about security and privacy \n `!ask` to ask a question about security \n " +
                "`"
                "`!virusgame` to learn more about viruses and cybersecurity :slightly_smiling_face: ")

            #meme function
            elif "!sendmeme" in msg:
                keyword = msg.split(" ")
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
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
                self.isQuiz = True
                self.quizIndex = 0
                self.quizScore = 0
                self.quizQuestions = list(questions)
                await bot.chat.send(channel, "Let's test your cyber-security knowledge! Please answer all questions with no caps. Good Luck!")
                #shuffle questions
                for i in range(100):
                    randint1 = random.randint(0,len(self.quizQuestions)-1)
                    randint2 = random.randint(0,len(self.quizQuestions)-1)
                    temp = self.quizQuestions[randint1]
                    self.quizQuestions[randint1] = self.quizQuestions[randint2]
                    self.quizQuestions[randint2] = temp
                
                await bot.chat.send(channel, self.quizQuestions[self.quizIndex][0])
                await bot.chat.send(channel, "Type your answer: ")

            elif self.isQuiz:
                answer = msg.lower()
                ans_bool = False
                for ans in self.quizQuestions[self.quizIndex][1]:
                    if answer == ans:
                        ans_bool = True
                if ans_bool == False:
                    await bot.chat.send(channel, "You got it wrong my dude")
                    await bot.chat.send(channel, self.quizQuestions[self.quizIndex][2])
                else:
                    self.quizScore += 1
                    await bot.chat.send(channel, "You got it my dude!")
                    await bot.chat.react(channel, msg_id, ":+1:")

                self.quizIndex += 1

                if self.quizIndex == len(self.quizQuestions):
                    await bot.chat.send(channel, event.msg.sender.username + " hello my dude, you got a score of " + str(self.quizScore) + " out of " + str(len(self.quizQuestions)))
                    self.quizQuestions = []
                    self.quizIndex = 0
                    self.quizScore = 0
                else:
                    await bot.chat.send(channel, self.quizQuestions[self.quizIndex][0])

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

            elif '!findme' in msg:
                self.findMe = True
                self.company = msg.split(" ")[1]
                await bot.chat.send(channel, "What would you like to find about yourself? \nPut in a few key words with spaces in between")

            elif self.findMe:
                await bot.chat.send(channel, "one moment ...")
                keyword = msg.split(" ")
                urlList = []
                if self.company == "google":
                    urlList = list(gSearch(keyword, 2))
                elif self.company == "reddit":
                    urlList = list(rSearch(keyword, 2))

                if len(urlList) > 0:
                    for i in range(len(urlList)):
                        await bot.chat.send(channel, "*Here are some useful links that the public knows about you:* \n\n" + urlList[i])
                else:
                    await bot.chat.send(channel, "Sorry, we didn't find anything about you :confused:")
                self.findMe = False


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
