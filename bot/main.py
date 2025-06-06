import logging
from pathlib import Path
import django
import sys
import os

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()

from aiogram import Bot, Dispatcher
from config import config
import asyncio

from handlers import router
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from panel.models import Template


async def on_startup():
    await Template.objects.aget_or_create(name='Дневной отчет')
    await Template.objects.aget_or_create(name='Вечерний отчет')


async def main():
    await on_startup()

    bot = Bot(token=config.BOT_TOKEN)

    dp = Dispatcher()
    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
