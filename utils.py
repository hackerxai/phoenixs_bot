from typing import Optional
from config import CATEGORIES

def get_category_by_name(category_name: str) -> Optional[str]:
    """Получение ключа категории по названию"""
    for key, name in CATEGORIES.items():
        if name == category_name:
            return key
    return None

def format_service_message(service: dict) -> str:
    """Форматирование сообщения об услуге"""
    return f"""💼 **{service['name']}**

💰 **Цена:** {service['price']}

📝 **Описание:**
{service['description']}

Выберите действие:"""

def format_detailed_service_message(service: dict) -> str:
    """Форматирование подробного сообщения об услуге"""
    return f"""📄 **Подробная информация**

💼 **Услуга:** {service['name']}
💰 **Цена:** {service['price']}
📂 **Категория:** {service['category']}

📝 **Полное описание:**
{service['description']}

🔥 **Что входит в услугу:**
• Диагностика текущего состояния системы
• Профессиональная оптимизация
• Тестирование после выполнения работ
• Консультация по дальнейшему использованию
• Поддержка в течение 7 дней после оказания услуги

⚡ **Время выполнения:** от 1 до 3 часов
🛡 **Гарантия:** 30 дней

Готовы заказать? Нажмите кнопку ниже! 👇"""

def truncate_text(text: str, max_length: int = 4000) -> str:
    """Обрезка текста до максимальной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def escape_markdown(text: str) -> str:
    """Экранирование специальных символов для Markdown"""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_username(username: Optional[str]) -> str:
    """Форматирование username для отображения"""
    if not username:
        return "Не указан"
    return f"@{username}" if not username.startswith("@") else username