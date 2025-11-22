from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
TOKEN = '8240288411:AAEWHQn56pn6An6xAtN_V_lmzNUUGK7Z0Bk'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ID канала для проверки подписки (замените на реальный)
CHANNEL_ID = '-1003022523420'  # Пример: '-1001234567890'

@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    await message.answer('Привет! Я бот, который проверит твою подписку на канал.')
    await check_subscription(message)

@dp.message_handler()
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
        if user_status.status != 'left':
            await message.answer('Вы подписаны на канал, можете получать контент!')
            await send_content(message)
        else:
            # Создаем кнопку для подписки
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                'Подписаться на канал', 
                url='https://t.me/your_channel'  # Замените на реальную ссылку
            ))
            markup.add(types.InlineKeyboardButton(
                'Проверить подписку', 
                callback_data='check_subscription'
            ))
            
            await message.answer(
                'Для получения контента необходимо подписаться на канал!',
                reply_markup=markup
            )
    
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        await message.answer('Произошла ошибка при проверке подписки. Попробуйте позже.')

@dp.callback_query_handler(lambda callback: callback.data == 'check_subscription')
async def check_subscription_callback(callback: types.CallbackQuery):
    """Обработчик нажатия кнопки проверки подписки"""
    await callback.answer()
    await check_subscription(callback.message)

async def send_content(message: types.Message):
    """Отправка контента пользователю"""
    # Здесь можно добавить различный контент
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)