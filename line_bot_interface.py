import openai
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError
import json
import random

#our file
import getdata
import utility
import setting
import statistic_mgr


mode = 0 # 0 : recommend movie ; 1: input watched movie


app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)

    try:
        line_bot = LineBotApi(setting.channel_access_token) # Channel access token
        webhook_handler = WebhookHandler(setting.channel_secret) # channel secret
        signature = request.headers['X-Line-Signature']
        webhook_handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        line_message = json_data['events'][0]['message']['text']
        userid = json_data['events'][0]['source']['userId']
        
        

        if line_message == "input watched movies":
            mode = 1
            reply_message = 'Only one movie can be entered in a message, enter "quit" to leave.'
            text_message = TextSendMessage(text=reply_message)
            line_bot.push_message(userid, text_message) # output predictd movie
            return 'OK'
        elif line_message.lower() == 'quit':
            mode = 0
            reply_message = 'Start recommending movies'
            text_message = TextSendMessage(text=reply_message)
            line_bot.push_message(userid, text_message) # output predictd movie
            return 'OK'
        
        prompt_msg = ''
        try:
            prompt_msg = utility.load_prompt(userid, line_message)
            #print(prompt_msg)
        except: 
            print('prompt error')


        try:
            openai.api_key = setting.openai_api_key # open-ai api_key
            response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=prompt_msg,
                    max_tokens=500,
                    temperature=0.5,
                    )
            reply_message = response["choices"][0]["text"].replace("\n","")
        except:
            print('open ai error')

        movie_name = utility.extract_movie_name(reply_message)
        if movie_name in getdata.get_all_movies():
            img_url = setting.wordcloud_url_format + str(movie_name) + '.png'
        else:
            img_url = setting.wordcloud_url_format + getdata.get_all_movies()[random.randint(0,234)] + '.png'

        img_url = utility.url_translation(img_url)

        statistic_mgr.update_user_input(userid, line_message)
        #print(statistic_mgr.user_input)

        text_message = TextSendMessage(text=reply_message)
        image_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
        
        line_bot.push_message(userid, text_message) # output predictd movie
        line_bot.push_message(userid, image_message) # output word cloud

    except:
        print('System error')

    return 'OK'