from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота из переменных окружения
TOKEN = os.getenv('BOT_TOKEN', '8240288411:AAEWHQn56pn6An6xAtN_V_lmzNUUGK7Z0Bk')

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ID канала для проверки подписки (замените на реальный)
CHANNEL_ID = '-1003022523420'

@dp.message(Command('start'))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    await message.answer('Привет! Я бот, который проверит твою подписку на канал.')
    await check_subscription(message)

@dp.message()
async def handle_all_messages(message: types.Message):
    """Обработчик всех сообщений для проверки подписки"""
    await check_subscription(message)

async def check_subscription(message: types.Message):
    """Проверка подписки пользователя на канал"""
    try:
        # Получаем статус пользователя в канале
        user_status = await bot.get_chat_member(
            chat_id=CHANNEL_ID, 
            user_id=message.from_user.id
        )
        
        # Проверяем, что пользователь не покинул канал
        if user_status.status not in ['left', 'kicked']:
            await message.answer('Вы подписаны на канал, можете получать контент!')
            await send_content(message)
        else:
            # Создаем кнопку для подписки
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text='Подписаться на канал', 
                    url='https://t.me/PlantsvsZombiesFusionLegend'  # Замените на реальную ссылку
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
        logging.error(f"Ошибка при проверке подписки: {e}")
        await message.answer('Произошла ошибка при проверке подписки. Попробуйте позже.')

@dp.callback_query(lambda callback: callback.data == 'check_subscription')
async def check_subscription_callback(callback: types.CallbackQuery):
    """Обработчик нажатия кнопки проверки подписки"""
    try:
        # Получаем статус пользователя в канале
        user_status = await bot.get_chat_member(
            chat_id=CHANNEL_ID, 
            user_id=callback.from_user.id
        )
        
        # Проверяем, что пользователь не покинул канал
        if user_status.status not in ['left', 'kicked']:
            await callback.message.answer('Вы подписаны на канал, можете получать контент!')
            await send_content(callback.message)
            await callback.answer('✅ Подписка подтверждена!')
        else:
            # Создаем кнопку для подписки
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text='Подписаться на канал', 
                    url='https://t.me/PlantsvsZombiesFusionLegend'
                )],
                [types.InlineKeyboardButton(
                    text='Проверить подписку', 
                    callback_data='check_subscription'
                )]
            ])
            
            await callback.message.answer(
                'Вы еще не подписаны на канал! Пожалуйста, подпишитесь и нажмите "Проверить подписку" снова.',
                reply_markup=markup
            )
            await callback.answer('❌ Вы не подписаны на канал!')
    
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        await callback.message.answer('Произошла ошибка при проверке подписки. Попробуйте позже.')
        await callback.answer('⚠️ Произошла ошибка!')

async def send_content(message: types.Message):
    """Отправка контента пользователю"""
    # Здесь можно добавить различный контент
    content_messages = [
        "🎉 Вот ваш промокод на скин Подсолнуха Нян Кэта - TGSKIN245",
        "✅ Промокод вводить в Магазине!"
    ]
    
    for msg in content_messages:
        await message.answer(msg)

async def main():
    """Основная функция запуска бота"""
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())