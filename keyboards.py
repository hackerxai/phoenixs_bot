from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_keyboard():
    """Главное меню бота"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="📦 Оптимизация ПК", callback_data="category_optimization"),
        width=1
    )
    keyboard.row(
        InlineKeyboardButton(text="💻 Комплектующие", callback_data="category_components"),
        InlineKeyboardButton(text="🖱 Девайсы", callback_data="category_devices"),
        width=2
    )

    keyboard.row(
        InlineKeyboardButton(text="🧾 О нас", callback_data="category_about"),
        InlineKeyboardButton(text="📞 Контакты", callback_data="category_contacts"),
        width=2
    )
    
    return keyboard.as_markup()

def get_category_keyboard(category_key: str, services: list):
    """Клавиатура для услуг категории"""
    keyboard = InlineKeyboardBuilder()
    
    for service in services:
        # Ограничиваем длину названия
        service_name = service['name'][:50] + "..." if len(service['name']) > 50 else service['name']
        
        keyboard.row(
            InlineKeyboardButton(
                text=service_name,
                callback_data=f"service_{service['id']}"
            ),
            width=1
        )
    
    keyboard.row(
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
        width=1
    )
    
    return keyboard.as_markup()

def get_service_keyboard(service_id: int, category_key: str):
    """Клавиатура для конкретной услуги"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="📄 Подробнее", callback_data=f"details_{service_id}"),
        InlineKeyboardButton(text="✅ Заказать", callback_data=f"order_{service_id}"),
        width=2
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 К категории", callback_data=f"category_{category_key}"),
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
        width=2
    )
    
    return keyboard.as_markup()

def get_details_keyboard(service_id: int, category_key: str):
    """Клавиатура для подробной информации об услуге"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="✅ Заказать", callback_data=f"order_{service_id}"),
        width=1
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 К услуге", callback_data=f"service_{service_id}"),
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
        width=2
    )
    
    return keyboard.as_markup()

def get_back_to_main_keyboard():
    """Кнопка возврата в главное меню"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
        width=1
    )
    
    return keyboard.as_markup()

def get_contact_keyboard():
    """Клавиатура для контактов"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="💬 Написать менеджеру", url="https://t.me/phoen1xPC"),
        width=1
    )
    keyboard.row(
        InlineKeyboardButton(text="📢 Наш канал", url="https://t.me/helprepairpc"),
        width=1
    )
    keyboard.row(
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
        width=1
    )
    
    return keyboard.as_markup()

def get_channel_post_keyboard():
    """Кнопка для постов в канале"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="🔥 Открыть меню", url="https://t.me/Phoen1xPC_bot?start=channel"),
        width=1
    )
    
    return keyboard.as_markup()