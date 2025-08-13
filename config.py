import os
import json
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Класс конфигурации бота"""
    
    def __init__(self):
        # Основные настройки
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")
        self.ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
        
        # Проверка обязательных настроек
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен! Создайте .env файл или установите переменную окружения.")
        
        if not self.ADMIN_ID:
            print("⚠️ ВНИМАНИЕ: ADMIN_ID не установлен! Админские функции будут недоступны.")
        
        # Загрузка динамических настроек из файла
        self.settings_file = "settings.json"
        self.load_settings()
        
    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.MANAGER_USERNAME = settings.get("manager_username", "")
                    self.CHANNEL_ID = settings.get("channel_id", "")
                    self.GIVEAWAY_DESCRIPTION = settings.get(
                        "giveaway_description",
                        """🎁 **Розыгрыш**\n\nЗдесь публикуем актуальные розыгрыши и условия участия.\n\n- Подпишитесь на наш канал\n- Нажмите участвовать\n- Ждите итоги в канале\n\nУдачи!"""
                    )
            else:
                self.MANAGER_USERNAME = "phoen1xPC"
                self.CHANNEL_ID = "@helprepairpc"
                self.GIVEAWAY_DESCRIPTION = (
                    """🎁 **Розыгрыш**\n\nЗдесь публикуем актуальные розыгрыши и условия участия.\n\n- Подпишитесь на наш канал\n- Нажмите участвовать\n- Ждите итоги в канале\n\nУдачи!"""
                )
                self.save_settings()
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            self.MANAGER_USERNAME = "phoen1xPC"
            self.CHANNEL_ID = "@helprepairpc"
            self.GIVEAWAY_DESCRIPTION = (
                """🎁 **Розыгрыш**\n\nЗдесь публикуем актуальные розыгрыши и условия участия.\n\n- Подпишитесь на наш канал\n- Нажмите участвовать\n- Ждите итоги в канале\n\nУдачи!"""
            )
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            settings = {
                "manager_username": self.MANAGER_USERNAME,
                "channel_id": self.CHANNEL_ID,
                "giveaway_description": self.GIVEAWAY_DESCRIPTION
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def set_manager(self, username: str):
        """Установка username менеджера"""
        self.MANAGER_USERNAME = username.replace("@", "")
        self.save_settings()
    
    def set_channel(self, channel_id: str):
        """Установка ID канала"""
        self.CHANNEL_ID = channel_id
        self.save_settings()

    def set_giveaway_description(self, description: str):
        """Установка описания раздела Розыгрыш"""
        self.GIVEAWAY_DESCRIPTION = description
        self.save_settings()

# Категории услуг
CATEGORIES = {
    "optimization": "📦 Услуги по оптимизации и разгону ПК",
    "components": "💻 Комплектующие", 
    "devices": "🖱 Девайсы",
    "giveaway": "🎁 Розыгрыш",
    "about": "🧾 О нас",
    "contacts": "📞 Контакты и заказ"
}

# Сообщения
MESSAGES = {
    "welcome": """🔥 **Phoenix PS Bot** 🔥

Добро пожаловать! Мы предоставляем профессиональные услуги по оптимизации и кастомизации Windows.

Выберите категорию из меню ниже:""",
    
    "order_success": "✅ Вы выбрали: **{service_name}**.\nВаша заявка отправлена! Мы скоро с вами свяжемся.",
    
    "manager_notification": """🔔 **Новая заявка!**

📋 Услуга: {service_name}
👤 Клиент: @{username}
🔗 Профиль: t.me/{username}
🕐 Время: {time}

💰 Цена: {price}

📝 Описание:
{description}""",
    
    "error": "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
    "admin_only": "❌ Эта команда доступна только администратору.",
    "invalid_choice": "❌ Пожалуйста, выберите опцию из предложенного меню."
}
