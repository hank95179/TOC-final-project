from transitions.extensions import GraphMachine

from utils import send_text_message
import utils
import os
import sys
from bs4 import BeautifulSoup
import json
import requests
import random

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
class TocMachine(GraphMachine):
    picture_id = []
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "加"
    def is_going_to_state5(self, event):
        text = event.message.text
        return text.lower() == "刪"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "我的油圖"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "今日油圖"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text.lower() == "id"
    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")
    def on_enter_state5(self, event):
        print("I'm entering state5")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state5")
        self.go_back()

    def on_exit_state5(self):
        print("Leaving state5")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        #self.state2to1()

    #def on_exit_state2(self):
        #print("Leaving state2")
    def on_enter_state3(self, event):
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        line_bot_api = LineBotApi(channel_access_token)
        print("I'm entering state3")
        response = requests.get(
            "https://www.pixiv.net/ranking.php?p=1&format=json")
        soup = BeautifulSoup(response.text, "html.parser")
        j = json.loads(str(soup))
        k = j['contents']
        t = random.randint(0,2)
        i = k[t]
        paintcount = int(i['illust_page_count'])

        uid = str(i['illust_id'])
        #print(uid)
        if paintcount == 1:
            mes = "https://www.pixiv.cat/" + uid + ".jpg"
            self.picture_id.append(uid)
        else:
            mes = "https://www.pixiv.cat/" + uid + "-1.jpg"
            self.picture_id.append(uid+"-1")
        message = ImageSendMessage(
        original_content_url=mes,
        preview_image_url=mes
        )
        line_bot_api.reply_message(event.reply_token, message)

    def on_enter_state4(self, event):
        print("I'm entering state4")

        reply_token = event.reply_token
        send_text_message(reply_token, self.picture_id[0])
        del self.picture_id[0]
        self.go_back()

    def on_exit_state4(self):
        print("Leaving state4")

