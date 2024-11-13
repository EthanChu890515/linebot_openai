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
    "當你參加社交聚會時，你更喜歡：\na) 認識新朋友並享受熱鬧的氣氛\nb) 與親近的朋友談心，享受安靜的互動",
    "在處理新任務時，你通常：\na) 將重點放在細節和逐步完成\nb) 思考最終目標和可能的長遠影響",
    "當面臨困難的選擇時，你會：\na) 依據邏輯和客觀事實來決定\nb) 考慮對你和他人感受的影響",
    "安排你的日常時，你偏好：\na) 擁有固定計劃，讓一切有序進行\nb) 保持彈性，隨時調整行程",
    "當你學習一門新技能時，你：\na) 喜歡了解具體步驟和實踐應用\nb) 更感興趣於背後的理論概念",
    "與別人討論時，你習慣：\na) 坦率地說出你的想法\nb) 考慮語氣並顧及對方的感受",
    "處理複雜問題時，你傾向於：\na) 運用冷靜分析來找出最佳解決方案\nb) 從感性角度理解並設法平息情緒",
    "在緊張狀況下，你更喜歡：\na) 保持規律，依賴熟悉的日常\nb) 靈活變通，快速找出替代方案",
    "參與團隊項目時，你通常：\na) 喜歡有清晰的分工和規範\nb) 鼓勵創意，讓每個人自由發揮",
    "當你想到未來時，你會：\na) 設想可預測的事情，確保一切穩妥\nb) 期待未知，探索各種新可能性",
    "執行任務時，你更傾向於：\na) 完全按計劃進行\nb) 依據當下的直覺和情況調整",
    "處理挑戰時，你的做法是：\na) 重複你曾經成功的策略\nb) 尋求新的方法和不同的嘗試",
    "學習新知識時，你更關注：\na) 具體的數據和實際應用\nb) 抽象的理論和可能性",
    "表達意見時，你傾向於：\na) 簡單直接，避免誤解\nb) 委婉細緻，考慮到他人反應",
    "當面對衝突時，你會：\na) 保持理性，避免情緒化反應\nb) 優先考慮和解與關係修復",
    "計劃未來時，你更習慣：\na) 做詳細的準備，確保有序進行\nb) 留出空間，允許自己適應變化",
    "面對新挑戰時，你：\na) 依賴已知的經驗來應對\nb) 熱衷於嘗試新策略，激發創意",
    "當你與別人互動時，你更喜歡：\na) 簡潔有力地表達觀點\nb) 考慮他人的反應，調整表達",
    "做決策時，你更注重：\na) 真實的數據和分析結果\nb) 你的直覺和情感反應",
    "當突發情況出現時，你通常：\na) 嘗試迅速穩定現狀\nb) 把它看作是新機會，迎接挑戰",
    "在社交場合中，你通常：\na) 喜歡擔任主導角色，活躍氣氛\nb) 偏愛觀察和與少數人深談",
    "工作中遇到新問題時，你：\na) 從每個細節入手，逐步分析\nb) 一開始就構思大方向和整體策略",
    "當你分析情況時，你：\na) 偏好從邏輯層面做出判斷\nb) 考慮人際影響和人們的情感",
    "安排一天行程時，你：\na) 事先計劃好每個環節\nb) 根據當天情況決定下一步",
    "在學習中，你會選擇：\na) 實際練習來加深理解\nb) 先深入理解理論架構",
    "表達自己時，你通常：\na) 清楚明確地說出意見\nb) 留意措辭，盡量不冒犯他人",
    "面對問題時，你：\na) 尋求合理的解決方案，避免情緒波動\nb) 嘗試理解各方的情緒需求",
    "計劃未來時，你更看重：\na) 確定可控的部分，避免風險\nb) 保持開放，願意接受意外驚喜",
    "接受新任務時，你會：\na) 準備周全，以降低失敗風險\nb) 把重心放在創新和突破上",
    "在溝通中，你喜歡：\na) 用簡單直白的語言表達\nb) 花心思讓對方感到舒服",
    "當遇到壓力時，你：\na) 試圖按部就班處理\nb) 立即找替代方案解決",
    "在合作中，你會：\na) 確認每個人的責任和範圍\nb) 鼓勵大家自由發揮想法",
    "解決問題時，你：\na) 依賴過去經驗和可靠方法\nb) 挑戰自我，探索新可能",
    "學習新概念時，你：\na) 首先理解具體的事實\nb) 研究背後的理論推導",
    "與他人溝通時，你：\na) 將重點放在實際的數據上\nb) 討論各種想法和視角",
    "當你作出決定時，你：\na) 完全依據邏輯推理\nb) 把個人感受納入考量",
    "在日常中，你更喜歡：\na) 按照計劃行事，避免變數\nb) 靈活處理，不排斥改變",
    "面對未知挑戰時，你：\na) 利用自己熟悉的方法解決\nb) 喜歡突破傳統，尋找創新",
    "談話時，你：\na) 直截了當，表達自己的觀點\nb) 委婉些，避免引發衝突",
    "當安排活動時，你：\na) 預先計劃好細節\nb) 開放態度，隨機應變",
    "處理新事物時，你：\na) 利用已掌握的知識來應對\nb) 挑戰自我，嘗試新路線",
    "學習時，你：\na) 注重事實與應用價值\nb) 探討理論與概念的連結"
]



# 各維度題目索引
ei_questions = [0, 1, 8, 9, 16, 17, 24, 25, 32, 33]  # 10題
sn_questions = [2, 3, 10, 11, 18, 19, 26, 27, 34, 35]  # 10題
tf_questions = [4, 5, 12, 13, 20, 21, 28, 29, 36, 37]  # 10題
jp_questions = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39]  # 10題

# 選擇隨機問題的函數，確保問題不會重複
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
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/INTJ.jpg?raw=true"
    },
    "INTP": {
        "description": "你的MBTI為INTP，你可能是一個理性、好奇的人，喜歡獨自探索和思考。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/INTP.jpg?raw=true"
    },
    "ENTJ": {
        "description": "你的MBTI為ENTJ，你可能是一個果斷、領導能力強的人，善於組織和規劃。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ESTJ.jpg?raw=true"
    },
    "ENTP": {
        "description": "你的MBTI為ENTP，你可能是一個充滿創意、善於挑戰傳統的人，喜歡嘗試新的事物。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ENTP.jpg?raw=true"
    },
    "INFJ": {
        "description": "你的MBTI為INFJ，你可能是一個理想主義者，具有強烈的直覺和同情心。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/INFJ.jpg?raw=true"
    },
    "INFP": {
        "description": "你的MBTI為INFP，你可能是一個理想主義者，關心他人的感受和內心世界。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/INFP.jpg?raw=true"
    },
    "ENFJ": {
        "description": "你的MBTI為ENFJ，你可能是一個富有魅力和感染力的領袖，善於激勵和引導他人。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ENFJ.jpg?raw=true"
    },
    "ENFP": {
        "description": "你的MBTI為ENFP，你可能是一個充滿熱情和創造力的人，喜歡探索新的可能性。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ENFP.jpg?raw=true"
    },
    "ISTJ": {
        "description": "你的MBTI為ISTJ，你可能是一個實事求是、責任感強的人，重視傳統和穩定。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ISTJ.jpg?raw=true"
    },
    "ISFJ": {
        "description": "你的MBTI為ISFJ，你可能是一個細心周到、富有同情心的人，重視和諧和合作。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ISFJ.jpg?raw=true"
    },
    "ESTJ": {
        "description": "你的MBTI為ESTJ，你可能是一個實幹型的人，喜歡組織和管理工作，注重效率和結果。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ESTJ.jpg?raw=true"
    },
    "ESFJ": {
        "description": "你的MBTI為ESFJ，你可能是一個熱心助人、樂於奉獻的人，重視他人的需求和感受。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ESFJ.jpg?raw=true"
    },
    "ISTP": {
        "description": "你的MBTI為ISTP，你可能是一個獨立、實用的人，喜歡解決具體的問題和挑戰。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ISTP.jpg?raw=true"
    },
    "ISFP": {
        "description": "你的MBTI為ISFP，你可能是一個溫和、靈活的人，喜歡追求個人的自由和創造力。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ISFP.jpg?raw=true"
    },
    "ESTP": {
        "description": "你的MBTI為ESTP，你可能是一個熱愛冒險、富有活力的人，喜歡嘗試新的經歷和挑戰。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ESTP.jpg?raw=true"
    },
    "ESFP": {
        "description": "你的MBTI為ESFP，你可能是一個活潑、熱情的人，喜歡與他人互動和享受生活。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/ESFP.jpg?raw=true"
    }
}



@app.route("/")
def home():
    return "Hello, this is the MBTI Line Bot application. Please use the appropriate endpoint."

# 處理 LINE Webhook 請求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
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
        if i < 2:  # EI 維度
            counts["E" if answer == "a" else "I"] += 1
        elif i < 6:  # SN 維度
            counts["S" if answer == "a" else "N"] += 1
        elif i < 10:  # TF 維度
            counts["T" if answer == "a" else "F"] += 1
        else:  # JP 維度
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
