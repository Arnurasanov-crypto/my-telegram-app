import os
import asyncio
import logging
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

# 1. Веб-сервер для Render
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

# 2. Инициализация Ботa
TOKEN = os.environ.get("BOT_TOKEN")
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Привет! Открой мини-приложение через меню слева внизу, чтобы начать играть и управлять балансом.")

# Обработка данных, пришедших из Web App
@dp.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    data = json.loads(message.web_app_data.data)
    action = data.get("action")

    if action == "deposit":
        await message.answer("💳 **Пополнение баланса**\n\nОтправьте сумму пополнения или переведите средства на указанный кошелек.")
    elif action == "withdraw":
        await message.answer("💸 **Вывод средств**\n\nВведите ваш адрес кошелька (USDT TON / TRC20) для вывода средств.")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
