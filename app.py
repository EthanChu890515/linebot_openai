from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('yOBTbdC80uJmcmPQDFW+20TWectJYFzIkXoThbUVsi0Et9jQXecQWnDoK4UzUShO1Q+HoFNimovw1X+zqAhGbaREvHsKm/f0iLIJn9/sP0UWe4I884BgKV+iC5TUKIQRRPA96p02d7OJjoMdnCioowdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('29f84578040cbbb8466a96bcf2c02972')

# MBTI 問卷問題
mbti_questions = [
    "1. 當你參加一個聚會時，你更傾向於：\na) 與很多人交流，感覺充滿能量\nb) 與幾個熟悉的朋友深度交談，感覺放鬆",
    "2. 當你面對新任務時，你更傾向於：\na) 注意具體的細節和實際步驟\nb) 想像整體的可能性和未來的結果",
    "3. 當你做決定時，你更傾向於：\na) 根據邏輯和客觀事實來決定\nb) 根據個人價值和他人感受來決定",
    "4. 當你安排日程時，你更傾向於：\na) 提前計劃，喜歡有條理和結構\nb) 隨機應變，喜歡靈活和自發性",
    "5. 當你在學習新知識時，你更喜歡：\na) 實際應用和現實世界的例子\nb) 理論概念和抽象的思考",
    "6. 當你與人交流時，你更傾向於：\na) 直接而坦率\nb) 委婉而顧及他人感受",
    "7. 當你處理問題時，你更傾向於：\na) 以冷静、理性的方式分析和解決\nb) 以同情心和情感的方式理解和處理",
    "8. 當你處於壓力下時，你更傾向於：\na) 維持日常的常規和結構\nb) 尋找新的方法和變通",
    "9. 當你與他人合作時，你更傾向於：\na) 明確的角色和責任分配\nb) 開放的溝通和靈活的合作方式",
    "10. 當你考慮未來時，你更傾向於：\na) 專注於可以預測和控制的事情\nb) 期待未知和新奇的可能性"
]

# 儲存用戶回答的資訊
mbti_user_answers = {}

# MBTI 结果和描述及對應圖片URL
mbti_results = {
    "INTJ": {
        "description": "你的MBTI為INTJ，你可能是一個獨立、思想深邃的人，善於分析和解決問題。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2815.JPG?raw=true"
    },
    "INTP": {
        "description": "你的MBTI為INTP，你可能是一個理性、好奇的人，喜歡獨自探索和思考。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2814.JPG?raw=true"
    },
    "ENTJ": {
        "description": "你的MBTI為ENTJ，你可能是一個果斷、領導能力強的人，善於組織和規劃。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2813.JPG?raw=true"
    },
    "ENTP": {
        "description": "你的MBTI為ENTP，你可能是一個充滿創意、善於挑戰傳統的人，喜歡嘗試新的事物。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2812.JPG?raw=true"
    },
    "INFJ": {
        "description": "你的MBTI為INFJ，你可能是一個理想主義者，具有強烈的直覺和同情心。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2811.JPG?raw=true"
    },
    "INFP": {
        "description": "你的MBTI為INFP，你可能是一個理想主義者，關心他人的感受和內心世界。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2810.JPG?raw=true"
    },
    "ENFJ": {
        "description": "你的MBTI為ENFJ，你可能是一個富有魅力和感染力的領袖，善於激勵和引導他人。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2809.JPG?raw=true"
    },
    "ENFP": {
        "description": "你的MBTI為ENFP，你可能是一個充滿熱情和創造力的人，喜歡探索新的可能性。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2808.JPG?raw=true"
    },
    "ISTJ": {
        "description": "你的MBTI為ISTJ，你可能是一個實事求是、責任感強的人，重視傳統和穩定。",
        "image_url": "https://example.com/istj.png"
    },
    "ISFJ": {
        "description": "你的MBTI為ISFJ，你可能是一個細心周到、富有同情心的人，重視和諧和合作。",
        "image_url": "https://example.com/isfj.png"
    },
    "ESTJ": {
        "description": "你的MBTI為ESTJ，你可能是一個實幹型的人，喜歡組織和管理工作，注重效率和結果。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2816.JPG?raw=true"
    },
    "ESFJ": {
        "description": "你的MBTI為ESFJ，你可能是一個熱心助人、樂於奉獻的人，重視他人的需求和感受。",
        "image_url": "https://example.com/esfj.png"
    },
    "ISTP": {
        "description": "你的MBTI為ISTP，你可能是一個獨立、實用的人，喜歡解決具體的問題和挑戰。",
        "image_url": "https://example.com/istp.png"
    },
    "ISFP": {
        "description": "你的MBTI為ISFP，你可能是一個安靜、敏感的人，重視個人的價值和情感。",
        "image_url": "https://example.com/isfp.png"
    },
    "ESTP": {
        "description": "你的MBTI為ESTP，你可能是一個活力四射、喜歡冒險的人，善於應對突發情況。",
        "image_url": "https://example.com/estp.png"
    },
    "ESFP": {
        "description": "你的MBTI為ESFP，你可能是一個熱情洋溢、樂於與人交往的人，喜歡享受生活的樂趣。",
        "image_url": "https://example.com/esfp.png"
    }
}

# 處理 LINE Webhook 請求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理用戶加入好友事件
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_message = "歡迎使用MBTI機器人！如果要開始測驗，請輸入\"開始\"。"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(welcome_message))

# 處理文本消息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text

    if user_id not in mbti_user_answers:
        mbti_user_answers[user_id] = []

    current_question_index = len(mbti_user_answers[user_id])

    # 如果用戶輸入"開始"或"重新開始測試"
    if msg.lower() in ['開始', '重新開始測試']:
        mbti_user_answers[user_id] = []
        current_question_index = 0
        line_bot_api.reply_message(event.reply_token, TextSendMessage(mbti_questions[0]))
        return

    if current_question_index < len(mbti_questions):
        if msg.lower() not in ['a', 'b']:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答'A'或'B'。"))
            return
        mbti_user_answers[user_id].append(msg.lower())
        if current_question_index + 1 < len(mbti_questions):
            next_question = mbti_questions[current_question_index + 1]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(next_question))
        else:
            # 計算 MBTI 结果
            mbti_type = calculate_mbti(mbti_user_answers[user_id])
            if mbti_type in mbti_results:
                result_message = mbti_results[mbti_type]["description"]
                image_url = mbti_results[mbti_type]["image_url"]
                # 發送 MBTI 結果的圖片
                image_message = ImageSendMessage(
                    original_content_url=image_url,
                    preview_image_url=image_url
                )
                line_bot_api.reply_message(event.reply_token, [
                    TextSendMessage(result_message),
                    image_message,
                    TextSendMessage("如果要重新測驗可以輸入重新開始測試。")
                ])
            else:
                result_message = "無法計算您的 MBTI 結果。請重新開始測試。"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(result_message))

# 計算 MBTI 结果的函数
def calculate_mbti(answers):
    e_count = answers[0:10:4].count('a')  # 1, 5, 9
    i_count = answers[0:10:4].count('b')
    n_count = answers[1:10:4].count('b')  # 2, 6, 10
    s_count = answers[1:10:4].count('a')
    t_count = answers[2:10:4].count('a')  # 3, 7
    f_count = answers[2:10:4].count('b')
    j_count = answers[3:10:4].count('a')  # 4, 8
    p_count = answers[3:10:4].count('b')
    
    mbti_type = \
        ('E' if e_count > i_count else 'I') + \
        ('N' if n_count > s_count else 'S') + \
        ('T' if t_count > f_count else 'F') + \
        ('J' if j_count > p_count else 'P')
    
    return mbti_type

if __name__ == "__main__":
    app.run(port=5000)


