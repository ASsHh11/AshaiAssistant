from flask import Flask, request
import openai
import os
import telebot

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

@app.route('/')
def home():
    return "AshaiAssistant is live!"

@app.route(f'/{os.getenv("TELEGRAM_BOT_TOKEN")}', methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    reply = response['choices'][0]['message']['content']
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    app.run(port=5050)
