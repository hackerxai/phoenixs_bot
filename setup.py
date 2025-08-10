#!/usr/bin/env python3
"""
Скрипт первоначальной настройки Phoenix PS Bot
Добавляет тестовые услуги в базу данных
"""

import asyncio
import logging
from database import init_db, db
from config import CATEGORIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Тестовые услуги для добавления
TEST_SERVICES = [
    # Оптимизация и разгон ПК
    {
        "name": "⚡ Базовая оптимизация Windows",
        "description": "Очистка системы от мусора, отключение ненужных служб, оптимизация автозагрузки. Подходит для начинающих пользователей.",
        "price": "1500 руб.",
        "category": "📦 Услуги по оптимизации и разгону ПК"
    },
    {
        "name": "🔥 Расширенная оптимизация Windows",
        "description": "Полная оптимизация системы: очистка реестра, настройка производительности, оптимизация игр, удаление вирусов.",
        "price": "2500 руб.",
        "category": "📦 Услуги по оптимизации и разгону ПК"
    },
    {
        "name": "🌐 Оптимизация сетевого контроллера",
        "description": "Настройка сетевых параметров для максимальной скорости интернета, оптимизация DNS, настройка QoS.",
        "price": "1000 руб.",
        "category": "📦 Услуги по оптимизации и разгону ПК"
    },
    {
        "name": "🚀 Разгон CPU",
        "description": "Безопасный разгон процессора с тестированием стабильности, настройка вольтажа и частот.",
        "price": "2000 руб.",
        "category": "📦 Услуги по оптимизации и разгону ПК"
    },
    {
        "name": "🎮 Разгон GPU",
        "description": "Разгон видеокарты с настройкой памяти и ядра, тестирование в играх, оптимизация драйверов.",
        "price": "1800 руб.",
        "category": "📦 Услуги по оптимизации и разгону ПК"
    },
    {
        "name": "💾 Разгон RAM",
        "description": "Настройка таймингов памяти, разгон частот, тестирование стабильности, оптимизация XMP профилей.",
        "price": "1200 руб.",
        "category": "📦 Услуги по оптимизации и разгону ПК"
    },
    
    # Комплектующие
    {
        "name": "💻 Подбор игровой сборки",
        "description": "Консультация по выбору комплектующих для игрового ПК с учетом бюджета и требований.",
        "price": "800 руб.",
        "category": "💻 Комплектующие"
    },
    {
        "name": "🔧 Консультация по апгрейду",
        "description": "Анализ текущей системы и рекомендации по апгрейду для повышения производительности.",
        "price": "500 руб.",
        "category": "💻 Комплектующие"
    },
    
    # Девайсы
    {
        "name": "🖱 Настройка игровой мыши",
        "description": "Настройка DPI, кнопок, макросов, профилей для игровой мыши под ваши игры.",
        "price": "400 руб.",
        "category": "🖱 Девайсы"
    },
    {
        "name": "⌨️ Настройка механической клавиатуры",
        "description": "Настройка подсветки, макросов, профилей, программирование клавиш для механической клавиатуры.",
        "price": "350 руб.",
        "category": "🖱 Девайсы"
    },
    
    # Школа
    {
        "name": "🎓 Курс оптимизации для начинающих",
        "description": "Обучающий курс по оптимизации Windows: от основ до продвинутых техник. 10 уроков с практикой.",
        "price": "3000 руб.",
        "category": "🎓 Школа"
    },
    {
        "name": "🔥 Мастер-класс по разгону",
        "description": "Индивидуальный мастер-класс по разгону комплектующих с практическими занятиями и теорией.",
        "price": "4500 руб.",
        "category": "🎓 Школа"
    }
]

async def setup_database():
    """Настройка базы данных и добавление тестовых услуг"""
    try:
        logger.info("Инициализация базы данных...")
        await init_db()
        
        # Проверяем, есть ли уже услуги в базе
        existing_services = await db.get_all_services()
        if existing_services:
            logger.info(f"В базе уже есть {len(existing_services)} услуг. Пропускаем добавление тестовых данных.")
            return
        
        logger.info("Добавление тестовых услуг...")
        for service in TEST_SERVICES:
            service_id = await db.add_service(
                service["name"],
                service["description"],
                service["price"],
                service["category"]
            )
            logger.info(f"Добавлена услуга: {service['name']} (ID: {service_id})")
        
        logger.info(f"✅ Успешно добавлено {len(TEST_SERVICES)} тестовых услуг!")
        
        # Показываем статистику
        services = await db.get_all_services()
        logger.info(f"📊 Всего услуг в базе: {len(services)}")
        
        # Группируем по категориям
        categories = {}
        for service in services:
            cat = service['category']
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        logger.info("📂 Распределение по категориям:")
        for category, count in categories.items():
            logger.info(f"  • {category}: {count} услуг")
            
    except Exception as e:
        logger.error(f"Ошибка при настройке базы данных: {e}")
        raise

async def main():
    """Главная функция"""
    print("🚀 Настройка Phoenix PS Bot")
    print("=" * 40)
    
    try:
        await setup_database()
        print("\n✅ Настройка завершена успешно!")
        print("\n📋 Следующие шаги:")
        print("1. Создайте файл .env с переменными BOT_TOKEN и ADMIN_ID")
        print("2. Установите зависимости: pip install -r requirements.txt")
        print("3. Запустите бота: python main.py")
        
    except Exception as e:
        print(f"\n❌ Ошибка при настройке: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 