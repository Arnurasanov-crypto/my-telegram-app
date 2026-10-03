import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telebot import TeleBot

# 1. Запуск мини-веб-сервера для Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# 2. Запуск Telegram-бота
TOKEN = os.environ.get("BOT_TOKEN")
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот работает.")

if __name__ == "__main__":
    bot.infinity_polling()
