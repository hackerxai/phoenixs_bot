import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from database import init_db
from handlers import register_user_handlers
from admin_handlers import register_admin_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Глобальный экземпляр бота
bot = None

async def main():
    """Основная функция запуска бота"""
    
    try:
        # Инициализация конфигурации
        logger.info("Загрузка конфигурации...")
        config = Config()
        logger.info(f"Бот токен загружен: {'*' * 10 + config.BOT_TOKEN[-4:] if config.BOT_TOKEN else 'НЕ УСТАНОВЛЕН'}")
        logger.info(f"Admin ID: {config.ADMIN_ID}")
        
        # Создание бота и диспетчера (глобальный экземпляр)
        global bot
        bot = Bot(token=config.BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Инициализация базы данных
        logger.info("Инициализация базы данных...")
        await init_db()
        logger.info("База данных инициализирована")
        
        # Регистрация хендлеров
        logger.info("Регистрация хендлеров...")
        register_user_handlers(dp, config)
        register_admin_handlers(dp, config)
        logger.info("Хендлеры зарегистрированы")
        
        logger.info("🚀 Бот запущен и готов к работе!")
        logger.info(f"📢 Канал для заявок: {config.CHANNEL_ID}")
        
        # Запуск бота
        await dp.start_polling(bot)
        
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        print(f"❌ ОШИБКА: {e}")
        print("📝 Создайте файл .env с переменными BOT_TOKEN и ADMIN_ID")
        print("📋 Пример содержимого .env файла:")
        print("BOT_TOKEN=your_bot_token_here")
        print("ADMIN_ID=your_telegram_id_here")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        sys.exit(1)
        
    finally:
        if bot:
            await bot.session.close()
            logger.info("Сессия бота закрыта")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
        print("👋 Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка в главном цикле: {e}")
        print(f"❌ ОШИБКА: {e}")