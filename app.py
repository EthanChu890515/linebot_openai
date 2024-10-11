from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import random

app = Flask(__name__)

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 定義MBTI問題
mbti_questions_full = [
    "當你參加一個聚會時，你更傾向於：\na) 與很多人交流，感覺充滿能量\nb) 與幾個熟悉的朋友深度交談，感覺放鬆",
    "當你面對新任務時，你更傾向於：\na) 注意具體的細節和實際步驟\nb) 想像整體的可能性和未來的結果",
    "當你做決定時，你更傾向於：\na) 根據邏輯和客觀事實\nb) 根據個人價值和他人感受來決定",
    "當你安排日程時，你更傾向於：\na) 提前計劃，喜歡有條理和結構\nb) 隨機應變，喜歡靈活和自發性",
    "當你在學習新知識時，你更喜歡：\na) 實際應用和現實世界的例子\nb) 理論概念和抽象的思考",
    "當你與人交流時，你更傾向於：\na) 直接而坦率\nb) 委婉而顧及他人感受",
    "當你處理問題時，你更傾向於：\na) 以冷静、理性的方式分析和解決\nb) 以同情心和情感的方式理解和處理",
    "當你處於壓力下時，你更傾向於：\na) 維持日常的常規和結構\nb) 尋找新的方法和變通",
    "當你與他人合作時，你更傾向於：\na) 明確的角色和責任分配\nb) 開放的溝通和靈活的合作方式",
    "當你考慮未來時，你更傾向於：\na) 專注於可以預測和控制的事情\nb) 期待未知和新奇的可能性",
    "當你處理工作時，你更傾向於：\na) 根據計劃和日程完成\nb) 按照當時的靈感和情況完成",
    "當你做事情時，你更喜歡：\na) 按部就班地進行\nb) 嘗試不同的方法",
    "當你學習新知識時，你更傾向於：\na) 關注事實和數據\nb) 關注理論和理念",
    "當你表達自己的觀點時，你更喜歡：\na) 直接明了\nb) 委婉含蓄",
    "當你處理衝突時，你更傾向於：\na) 理智冷靜地面對\nb) 理解和考慮他人的感受",
    "當你計劃未來時，你更喜歡：\na) 詳細計劃和安排\nb) 保持靈活和開放的選擇",
    "當你面對新挑戰時，你更喜歡：\na) 依靠過去的經驗和知識\nb) 探索新的方法和創意",
    "當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 考慮他人的感受",
    "當你處理事情時，你更喜歡：\na) 根據邏輯和事實\nb) 根據價值觀和感受",
    "當你安排活動時，你更傾向於：\na) 預先計劃和組織\nb) 即興發揮和變通",
    "當你做決策時，你更重視：\na) 客觀的數據和信息\nb) 主觀的感受和直覺",
    "當你表達自己時，你更傾向於：\na) 直率和直接\nb) 委婉和間接",
    "當你面對壓力時，你更傾向於：\na) 保持穩定和一致\nb) 尋找新的應對方法",
    "當你與他人合作時，你更喜歡：\na) 明確的分工和責任\nb) 開放的交流和合作",
    "當你處理問題時，你更傾向於：\na) 根據經驗和知識\nb) 探索新的可能性",
    "當你學習新東西時，你更傾向於：\na) 關注具體的事實\nb) 關注整體的概念",
    "當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和含蓄",
    "當你與他人交流時，你更喜歡：\na) 講述事實和細節\nb) 討論想法和觀點",
    "當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "當你處理日常事務時，你更傾向於：\na) 按計劃進行\nb) 靈活變通",
    "當你面對挑戰時，你更傾向於：\na) 使用已知的方法\nb) 探索新的途徑",
    "當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 委婉和考慮他人",
    "當你安排日程時，你更傾向於：\na) 提前計劃和準備\nb) 隨機應變和變通",
    "當你面對新任務時，你更喜歡：\na) 運用過去的經驗\nb) 探索新的方法",
    "當你學習新知識時，你更傾向於：\na) 聚焦於具體的細節\nb) 聚焦於概念和理論",
    "當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和考慮他人",
    "當你處理問題時，你更傾向於：\na) 邏輯分析\nb) 情感理解",
    "當你安排活動時，你更喜歡：\na) 提前計劃和組織\nb) 靈活和即興發揮",
    "當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "當你面對壓力時，你更傾向於：\na) 維持穩定\nb) 尋找新方法",
    "當你與他人合作時，你更傾向於：\na) 明確的分工\nb) 開放的合作",
    "當你處理問題時，你更傾向於：\na) 使用已知的方法\nb) 探索新的可能性",
    "當你學習新知識時，你更喜歡：\na) 關注具體事實\nb) 關注整體概念",
    "當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和含蓄",
    "當你與他人交流時，你更喜歡：\na) 講述事實\nb) 討論想法",
    "當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "當你處理日常事務時，你更傾向於：\na) 按計劃進行\nb) 靈活變通",
    "當你面對挑戰時，你更傾向於：\na) 使用已知的方法\nb) 探索新途徑",
    "當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 委婉和考慮他人",
    "當你安排日程時，你更傾向於：\na) 提前計劃和準備\nb) 隨機應變和變通",
    "當你面對新任務時，你更喜歡：\na) 運用過去的經驗\nb) 探索新的方法",
    "當你學習新知識時，你更喜歡：\na) 聚焦於具體的細節\nb) 聚焦於概念和理論",
    "當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和考慮他人",
    "當你處理問題時，你更傾向於：\na) 邏輯分析\nb) 情感理解",
    "當你安排活動時，你更喜歡：\na) 提前計劃和組織\nb) 靈活和即興發揮",
    "當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "當你面對壓力時，你更傾向於：\na) 維持穩定\nb) 尋找新方法",
    "當你與他人合作時，你更傾向於：\na) 明確的分工\nb) 開放的合作",
    "當你處理問題時，你更傾向於：\na) 使用已知的方法\nb) 探索新的可能性",
    "當你學習新知識時，你更喜歡：\na) 關注具體事實\nb) 關注整體概念",
    "當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和含蓄",
    "當你與他人交流時，你更喜歡：\na) 講述事實\nb) 討論想法",
    "當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "當你處理日常事務時，你更傾向於：\na) 按計劃進行\nb) 靈活變通",
    "當你面對挑戰時，你更傾向於：\na) 使用已知的方法\nb) 探索新途徑",
    "當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 委婉和考慮他人",
    "當你安排日程時，你更傾向於：\na) 提前計劃和準備\nb) 隨機應變和變通",
    "當你面對新任務時，你更喜歡：\na) 運用過去的經驗\nb) 探索新的方法",
    "當你學習新知識時，你更喜歡：\na) 聚焦於具體的細節\nb) 聚焦於概念和理論",
    "當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和考慮他人"
]



# 各維度題目索引
ei_questions = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63]
sn_questions = [1, 2, 8, 9, 15, 16, 22, 23, 29, 30, 36, 37, 43, 44, 50, 51, 57, 58, 64, 65]
tf_questions = [3, 4, 10, 11, 17, 18, 24, 25, 31, 32, 38, 39, 45, 46, 52, 53, 59, 60, 66, 67]
jp_questions = [5, 6, 12, 13, 19, 20, 26, 27, 33, 34, 40, 41, 47, 48, 54, 55, 61, 62, 68, 69]

def select_random_questions():
    selected_ei_questions = random.sample([mbti_questions_full[i] for i in ei_questions], 2)
    selected_sn_questions = random.sample([mbti_questions_full[i] for i in sn_questions], 4)
    selected_tf_questions = random.sample([mbti_questions_full[i] for i in tf_questions], 4)
    selected_jp_questions = random.sample([mbti_questions_full[i] for i in jp_questions], 4)
    return selected_ei_questions + selected_sn_questions + selected_tf_questions + selected_jp_questions

# 儲存用戶回答的資訊
mbti_user_answers = {}
mbti_user_questions = {}

# MBTI 结果和描述及對應圖片URL
mbti_results = {
    "INTJ": {
        "description": "你的MBTI為INTJ，你可能是一個獨立、思想深邃的人，善於分析和解決問題。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/INTJ.jpg?raw=true"
    },
    "INTP": {
        "description": "你的MBTI為INTP，你可能是一個理性、好奇的人，喜歡獨自探索和思考。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/INTP.jpg?raw=true"
    },
    "ENTJ": {
        "description": "你的MBTI為ENTJ，你可能是一個果斷、領導能力強的人，善於組織和規劃。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ENTJ.jpg?raw=true"
    },
    "ENTP": {
        "description": "你的MBTI為ENTP，你可能是一個充滿創意、善於挑戰傳統的人，喜歡嘗試新的事物。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ENTP.jpg?raw=true"
    },
    "INFJ": {
        "description": "你的MBTI為INFJ，你可能是一個理想主義者，具有強烈的直覺和同情心。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/INFJ.jpg?raw=true"
    },
    "INFP": {
        "description": "你的MBTI為INFP，你可能是一個理想主義者，關心他人的感受和內心世界。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/INFP.jpg?raw=true"
    },
    "ENFJ": {
        "description": "你的MBTI為ENFJ，你可能是一個富有魅力和感染力的領袖，善於激勵和引導他人。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ENFJ.jpg?raw=true"
    },
    "ENFP": {
        "description": "你的MBTI為ENFP，你可能是一個充滿熱情和創造力的人，喜歡探索新的可能性。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ENFP.jpg?raw=true"
    },
    "ISTJ": {
        "description": "你的MBTI為ISTJ，你可能是一個實事求是、責任感強的人，重視傳統和穩定。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ISTJ.jpg?raw=true"
    },
    "ISFJ": {
        "description": "你的MBTI為ISFJ，你可能是一個細心周到、富有同情心的人，重視和諧和合作。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ISFJ.jpg?raw=true"
    },
    "ESTJ": {
        "description": "你的MBTI為ESTJ，你可能是一個實幹型的人，喜歡組織和管理工作，注重效率和結果。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ESTJ.jpg?raw=true"
    },
    "ESFJ": {
        "description": "你的MBTI為ESFJ，你可能是一個熱心助人、樂於奉獻的人，重視他人的需求和感受。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ESFJ.jpg?raw=true"
    },
    "ISTP": {
        "description": "你的MBTI為ISTP，你可能是一個獨立、實用的人，喜歡解決具體的問題和挑戰。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ISTP.jpg?raw=true"
    },
    "ISFP": {
        "description": "你的MBTI為ISFP，你可能是一個溫和、靈活的人，喜歡追求個人的自由和創造力。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ISFP.jpg?raw=true"
    },
    "ESTP": {
        "description": "你的MBTI為ESTP，你可能是一個熱愛冒險、富有活力的人，喜歡嘗試新的經歷和挑戰。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ESTP.jpg?raw=true"
    },
    "ESFP": {
        "description": "你的MBTI為ESFP，你可能是一個活潑、熱情的人，喜歡與他人互動和享受生活。",
        "image_url": "https://github.com/MarrowTseng/linebot_openai/blob/master/ESFP.jpg?raw=true"
    }
}

@app.route("/")
def home():
    return "Hello, this is the MBTI Line Bot application. Please use the appropriate endpoint."

# 處理 LINE Webhook 請求
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取請求標頭中的簽名
    signature = request.headers['X-Line-Signature']
    # 獲取請求正文
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 處理 webhook 正文
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
    user_message = event.message.text.lower()

    if user_id not in mbti_user_answers:
        mbti_user_answers[user_id] = []

    if user_message in ["開始", "重新開始測試"]:
        mbti_user_questions[user_id] = select_random_questions()
        mbti_user_answers[user_id] = []
        question = mbti_user_questions[user_id][0]
        send_question_with_buttons(event.reply_token, question)
    elif user_id in mbti_user_questions:
        answers = mbti_user_answers[user_id]
        questions = mbti_user_questions[user_id]

        if len(answers) < len(questions):
            answers.append(user_message)
            if len(answers) < len(questions):
                question = questions[len(answers)]
                send_question_with_buttons(event.reply_token, question)
            else:
                mbti_result = calculate_mbti_result(answers)
                result = mbti_results.get(mbti_result, None)
                if result:
                    line_bot_api.reply_message(
                        event.reply_token,
                        [TextSendMessage(text=result["description"]),
                         ImageSendMessage(original_content_url=result["image_url"],
                                          preview_image_url=result["image_url"])]
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="無法計算您的 MBTI 結果。請重新開始測試。")
                    )
                del mbti_user_answers[user_id]
                del mbti_user_questions[user_id]
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無法計算您的 MBTI 結果。請重新開始測試。")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='歡迎使用MBTI機器人！如果要開始測驗，請輸入"開始"。')
        )

def send_question_with_buttons(reply_token, question):
    question_parts = question.split("\na) ")
    text = question_parts[0]
    options = question_parts[1].split("\nb) ")
    
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": text,
                    "wrap": True,
                    "weight": "bold",
                    "size": "md"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": options[0],
                        "text": "a"
                    },
                    "style": "primary",
                    "color": "#FF6F61",
                    "margin": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": options[1],
                        "text": "b"
                    },
                    "style": "primary",
                    "color": "#FF6F61",
                    "margin": "sm"
                }
            ]
        }
    }
    
    line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='MBTI問題', contents=flex_message))

def calculate_mbti_result(answers):
    counts = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }

    for i, answer in enumerate(answers):
        if i < 2:
            counts["E" if answer == "a" else "I"] += 1
        elif i < 6:
            counts["S" if answer == "a" else "N"] += 1
        elif i < 10:
            counts["T" if answer == "a" else "F"] += 1
        elif i < 14:
            counts["J" if answer == "a" else "P"] += 1

    mbti_type = "".join([
        "E" if counts["E"] > counts["I"] else "I",
        "S" if counts["S"] > counts["N"] else "N",
        "T" if counts["T"] > counts["F"] else "F",
        "J" if counts["J"] > counts["P"] else "P"
    ])

    return mbti_type

if __name__ == "__main__":
    app.run()