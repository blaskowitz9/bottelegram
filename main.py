from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
TOKEN = '8240288411:AAEWHQn56pn6An6xAtN_V_lmzNUUGK7Z0Bk'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ID канала для проверки подписки
CHANNEL_ID = '-1003022523420'

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привет! Я бот, который проверит твою подписку на канал.')
    await check_subscription(message)

async def check_subscription(message: types.Message):
    try:
        user_status = await bot.get_chat_member(
            chat_id=CHANNEL_ID, 
            user_id=message.from_user.id
        )
        
        if user_status.status != 'left':
            await message.answer('Вы подписаны на канал, можете получать контент!')
            await send_content(message)
        else:
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text='Подписаться на канал', 
                    url='https://t.me/your_channel'
                )],
                [types.InlineKeyboardButton(
                    text='Проверить подписку', 
                    callback_data='check_subscription'
                )]
            ])
            await message.answer(
                'Для получения контента необходимо подписаться на канал!',
                reply_markup=markup
            )
    
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer('Произошла ошибка. Попробуйте позже.')

@dp.callback_query(lambda callback: callback.data == 'check_subscription')
async def check_subscription_callback(callback: types.CallbackQuery):
    await callback.answer()
    await check_subscription(callback.message)

async def send_content(message: types.Message):
    content_messages = [
        "🎉 Вот ваш контент!",
        "📚 Полезные материалы:",
        "1. Первый материал",
        "2. Второй материал", 
        "3. Третий материал",
        "✅ Продолжайте следить за обновлениями!"
    ]
    for msg in content_messages:
        await message.answer(msg)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())