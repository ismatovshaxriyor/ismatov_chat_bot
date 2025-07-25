from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

user_histories = {}
group_histories = {}

client = OpenAI(api_key=api_key)

def get_answer_user(user_id, user_text):
    try:
        if user_id not in user_histories:
            user_histories[user_id] = [{"role": "system", "content": "O'zbek tilida javob ber"}]
        
        user_histories[user_id].append({"role": "user", "content": user_text})

        recent_messages = user_histories[user_id][-2:]  

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=recent_messages,
            max_tokens=500,
            temperature=0.6
        )

        assistant_reply = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except:
        return "Xatolik yuzaga keldi, iltimos qayta urining!"

def get_answer_group(history):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=history,
            max_tokens=500,
            temperature=0.6
        )
        assistant_reply = response.choices[0].message.content

        return assistant_reply
    except:
        return "Xatolik yuzaga keldi, iltimos qayta urining!"


