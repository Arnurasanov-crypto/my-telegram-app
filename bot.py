import os
import asyncio
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message

# 1. Веб-сервер для порта Render
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

# 2. Инициализация Aiogram 3
TOKEN = os.environ.get("BOT_TOKEN")
dp = Dispatcher()

@dp.message(CommandStart())
def command_start_handler(message: Message) -> None:
    message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
