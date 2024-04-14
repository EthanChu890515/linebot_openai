from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os

app = Flask(__name__)

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('yOBTbdC80uJmcmPQDFW+20TWectJYFzIkXoThbUVsi0Et9jQXecQWnDoK4UzUShO1Q+HoFNimovw1X+zqAhGbaREvHsKm/f0iLIJn9/sP0UWe4I884BgKV+iC5TUKIQRRPA96p02d7OJjoMdnCioowdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('29f84578040cbbb8466a96bcf2c02972')

# MBTI 问卷问题
mbti_questions = [
    "在社交場合中，你更喜歡與人們親近交談（E），還是更喜歡獨自思考（I）？（A. 與人親自交談 / B. 獨自思考）",
    "你更偏向於通過直覺（N）還是通過感覺（S）來認識和理解世界？（A. 直覺 / B. 感覺）",
    "你更偏向於通過思考（T）還是通過感受（F）來做出决定？（A. 思考 / B. 感受）",
    "你更傾向於有明確企劃（J）還是更喜歡靈活應對（P）？（A. 明確計畫 / B. 靈活應對）"
]

# 處存用戶回答的字典
mbti_user_answers = {}

# MBTI 结果和描述
mbti_results = {
    "INTJ": "你可能是一个獨立、思想深邃的人，善於分析和解決问题。",
    "INTP": "你可能是一个理性、好奇的人，喜歡獨自探索和思考。",
    "ENTJ": "你可能是一个果斷、領導能力强的人，善於組織和規劃。",
    "ENTP": "你可能是一个充滿創意、善於挑戰傳統的人，喜歡嘗試新的事物。",
    # 其他 MBTI 類型的結果...
}

# 處理 LINE Webhook 请求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理文本消息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text

    if user_id not in mbti_user_answers:
        mbti_user_answers[user_id] = []

    current_question_index = len(mbti_user_answers[user_id])
    if current_question_index < len(mbti_questions):
        if msg.lower() not in ['a', 'b']:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答'A'或'B'。"))
            return
        mbti_user_answers[user_id].append(msg.lower())
        next_question = mbti_questions[current_question_index]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(next_question))
    else:
        # 计算 MBTI 结果
        mbti_type = calculate_mbti(mbti_user_answers[user_id])
        if mbti_type in mbti_results:
            result_message = mbti_results[mbti_type]
        else:
            result_message = "無法計算你的 MBTI 结果。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(result_message))

# 计算 MBTI 结果的函数
def calculate_mbti(answers):
    mbti_type = ""
    for i in range(len(answers)):
        if i == 0:
            if answers[i] == 'a':
                mbti_type += 'E'
            else:
                mbti_type += 'I'
        elif i == 1:
            if answers[i] == 'a':
                mbti_type += 'N'
            else:
                mbti_type += 'S'
        elif i == 2:
            if answers[i] == 'a':
                mbti_type += 'T'
            else:
                mbti_type += 'F'
        elif i == 3:
            if answers[i] == 'a':
                mbti_type += 'J'
            else:
                mbti_type += 'P'
    return mbti_type

if __name__ == "__main__":
    app.run()

