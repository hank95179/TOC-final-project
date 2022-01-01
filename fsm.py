from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message
import utils
import os
import sys
#from bs4 import BeautifulSoup
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
    picture_num = 0
    temp = ''
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "加"
    def is_going_to_state11(self, event):
        text = event.message.text
        return text.lower() == "幫助"
    def is_going_to_state8(self, event):
        text = event.message.text
        return text.lower() == "查詢"
    def is_going_to_state5(self, event):
        text = event.message.text
        return text.lower() == "刪"

    def is_going_to_state6(self, event):#add
        text = event.message.text
        if len(text) <= 10 and len(text) >= 8:
            self.temp = text
            return True
        return False
    def is_going_to_state7(self, event):#delete
        text = event.message.text
        if len(text) <= 10 and len(text) >= 8:
            self.temp = text
            return True
        return False
    def is_going_to_state9(self, event):#delete
        text = event.message.text
        if len(text) <= 10 and len(text) >= 8:
            self.temp = text
            return True
        return False


    def is_going_to_state10(self, event):
        text = event.message.text
        return text.lower() == "我的油圖"
    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "編輯我的油圖"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "今日油圖"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text.lower() == "id"
    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "請問要加入的圖片的id?")
    def on_enter_state11(self, event):
        print("I'm entering state11")

        reply_token = event.reply_token
        title = '請問需要的服務'
        text = '今日油圖為當日Pixiv隨機排行前三\n今日油圖結束後輸入「id」回到原狀態'
        btn = [
            MessageTemplateAction(
                label = '我的油圖',
                text ='我的油圖'
            ),
            MessageTemplateAction(
                label = '編輯我的油圖',
                text = '編輯我的油圖'
            ),
            MessageTemplateAction(
                label = '今日油圖',
                text = '今日油圖'
            ),
            MessageTemplateAction(
                label = '查詢油圖',
                text = '查詢'
            ),
        ]
        url = 'https://upload.wikimedia.org/wikipedia/commons/7/73/Pixiv_logo.svg'
        send_button_message(reply_token, title, text, btn, url)
        self.go_back()

    def on_exit_state11(self):
        print("Leaving state11")
    def on_enter_state8(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "請問要查詢的圖片的id?")

    def on_enter_state6(self, event):
        print("I'm entering state6")
        o = open('mypicture.json')
        data2 = json.load(o)
        data2.setdefault(str(self.picture_num+1),self.temp)
        o.close()
        with open('mypicture.json', 'w', encoding='utf-8') as f:
            json.dump(data2, f, ensure_ascii=False, indent=4)
        self.picture_num += 1
        reply_token = event.reply_token
        send_text_message(reply_token, "加入成功")#"加入成功"
        self.temp = ''
        self.go_back()

    def on_exit_state6(self):
        print("Leaving state6")

    def on_enter_state7(self, event):
        print("I'm entering state6")
        o = open('mypicture.json')
        data2 = json.load(o)
        t = 0
        for i in range(len(data2)):
            if str(data2[str(i+1)]) == self.temp:
                t = i
        for i in range(len(data2)+1):
            if i > t+1:
                data2[str(i-1)] = data2.pop(str(i))
            elif i == t+1:
                data2.pop(str(i))
        o.close()
        with open('mypicture.json', 'w', encoding='utf-8') as f:
            json.dump(data2, f, ensure_ascii=False, indent=4)
        reply_token = event.reply_token
        send_text_message(reply_token, "刪除成功")
        self.picture_num -= 1
        self.go_back()

    def on_exit_state7(self):
        print("Leaving state7")

    def on_enter_state5(self, event):
        print("I'm entering state5")

        reply_token = event.reply_token
        send_text_message(reply_token, "請問要刪除的圖片的id?")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        o = open('mypicture.json')
        data2 = json.load(o)
        o.close()
        #global picture_num 
        self.picture_num = len(data2)
        output = 'picture list\n'
        for i in data2.items():
            output = output + str(i[1]) + "\n"
        title = 'picture list'
        text = output
        btn = [
            MessageTemplateAction(
                label = '刪除',
                text ='刪'
            ),
            MessageTemplateAction(
                label = '加入',
                text = '加'
            ),
        ]
        url = 'https://upload.wikimedia.org/wikipedia/commons/7/73/Pixiv_logo.svg'
        send_button_message(reply_token, title, text, btn, url)
        #send_text_message(reply_token, output)
        #self.state2to1()
    def on_enter_state10(self, event):
        print("I'm entering state10")

        reply_token = event.reply_token
        o = open('mypicture.json')
        data2 = json.load(o)
        o.close()
        #global picture_num 
        self.picture_num = len(data2)
        output = 'picture list\n'
        for i in data2.items():
            output = output + str(i[1]) + "\n"
        send_text_message(reply_token, output)
        self.go_back()
    def on_exit_state10(self):
        print("Leaving state10")
    def on_enter_state3(self, event):
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        line_bot_api = LineBotApi(channel_access_token)
        print("I'm entering state3")
        response = requests.get(
            "https://www.pixiv.net/ranking.php?p=1&format=json")
        soup = BeautifulSoup(response.text, "html.parser")
        """
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
        """
        mes = 'https://upload.wikimedia.org/wikipedia/commons/7/73/Pixiv_logo.svg'
        message = ImageSendMessage(
        original_content_url=mes,
        preview_image_url=mes
        )
        line_bot_api.reply_message(event.reply_token, message)
    def on_enter_state9(self, event):
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        line_bot_api = LineBotApi(channel_access_token)
        print("I'm entering state9")
        mes = "https://www.pixiv.cat/" + str(self.temp) + ".jpg"
        message = ImageSendMessage(
        original_content_url=mes,
        preview_image_url=mes
        )
        line_bot_api.reply_message(event.reply_token, message)
        self.go_back()
    def on_exit_state9(self):
        print("Leaving state4")
    def on_enter_state4(self, event):
        print("I'm entering state4")

        reply_token = event.reply_token
        send_text_message(reply_token, self.picture_id[0])
        del self.picture_id[0]
        self.go_back()

    def on_exit_state4(self):
        print("Leaving state4")

