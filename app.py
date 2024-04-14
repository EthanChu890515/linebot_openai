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
    "在社交场合中，你更喜欢与人们亲近交谈，还是更喜欢独自思考？（A. 与人亲近交谈 / B. 独自思考）",
    "你更偏向于通过直觉（N）还是通过感觉（S）来认识和理解世界？（A. 直觉 / B. 感觉）",
    "你更偏向于通过思考（T）还是通过感受（F）来做出决定？（A. 思考 / B. 感受）",
    "你更倾向于有明确计划（J）还是更喜欢灵活应对（P）？（A. 明确计划 / B. 灵活应对）"
]

# 存储用户回答的字典
mbti_user_answers = {}

# MBTI 结果
mbti_results = {
    "INTJ": "你可能是一个独立、思想深邃的人，善于分析和解决问题。",
    "INTP": "你可能是一个理性、好奇的人，喜欢独自探索和思考。",
    "ENTJ": "你可能是一个果断、领导能力强的人，善于组织和规划。",
    "ENTP": "你可能是一个充满创意、善于挑战传统的人，喜欢尝试新的事物。",
    # 其他 MBTI 类型的结果...
}

# 处理 LINE Webhook 请求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 处理文本消息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text

    if user_id not in mbti_user_answers:
        mbti_user_answers[user_id] = []

    current_question_index = len(mbti_user_answers[user_id])
    if current_question_index < len(mbti_questions):
        mbti_user_answers[user_id].append(msg)
        next_question = mbti_questions[current_question_index]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(next_question))
    else:
        # 计算 MBTI 结果
        mbti_type = calculate_mbti(mbti_user_answers[user_id])
        if mbti_type in mbti_results:
            result_message = mbti_results[mbti_type]
        else:
            result_message = "无法计算你的 MBTI 结果。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(result_message))

# 计算 MBTI 结果的函数
def calculate_mbti(answers):
    # 这里可以根据用户的回答计算出 MBTI 类型
    # 例如，根据每个问题的答案，计算出用户的四个字母组合
    # 然后根据这个组合来确定用户的 MBTI 类型
    # 这里仅作示例，具体逻辑需要根据实际情况来设计
    return "INTJ"  # 返回一个假设的 MBTI 类型

if __name__ == "__main__":
    app.run()

