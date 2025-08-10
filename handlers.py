import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import Config, CATEGORIES, MESSAGES
from database import db
from keyboards import (
    get_main_menu_keyboard, 
    get_category_keyboard, 
    get_service_keyboard,
    get_details_keyboard,
    get_back_to_main_keyboard,
    get_contact_keyboard
)
from utils import get_category_by_name, format_service_message, format_detailed_service_message

logger = logging.getLogger(__name__)
router = Router()

def safe_callback_answer(callback):
    """Безопасный ответ на callback"""
    try:
        return callback.answer()
    except Exception:
        pass

def register_user_handlers(dp, config: Config):
    """Регистрация пользовательских хендлеров"""
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        """Обработчик команды /start"""
        user = message.from_user
        
        # Логирование действия
        if user:
            await db.log_user_action(
                user.id, 
                user.username or "unknown", 
                "start_command"
            )
        
        await message.answer(
            MESSAGES["welcome"],
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
    
    @dp.callback_query(F.data == "main_menu")
    async def show_main_menu(callback: CallbackQuery):
        """Показать главное меню"""
        user = callback.from_user
        
        if user:
            await db.log_user_action(
                user.id,
                user.username or "unknown",
                "main_menu_accessed"
            )
        
        try:
            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    MESSAGES["welcome"],
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode="Markdown"
                )
        except TelegramBadRequest:
            if callback.message:
                await callback.message.answer(
                    MESSAGES["welcome"],
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode="Markdown"
                )
        
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("category_"))
    async def show_category(callback: CallbackQuery):
        """Показать услуги категории"""
        user = callback.from_user
        if not callback.data:
            return
            
        category_key = callback.data.split("_")[1]
        
        if category_key not in CATEGORIES:
            await safe_callback_answer(callback)
            return
        
        category_name = CATEGORIES[category_key]
        
        # Логирование
        if user:
            await db.log_user_action(
                user.id,
                user.username or "unknown",
                "category_viewed",
                category_name
            )
        
        # Обработка специальных категорий
        if category_key == "about":
            about_text = """🧾 **О нас**

Phoenix PS - профессиональная команда специалистов по оптимизации Windows и разгону компьютеров.

🔥 **Наши преимущества:**
• Многолетний опыт работы
• Индивидуальный подход к каждому клиенту
• Гарантия на все выполненные работы
• Поддержка после оптимизации

💪 **Мы поможем вам:**
• Увеличить производительность ПК
• Избавиться от лагов и зависаний
• Настроить систему под ваши задачи
• Разогнать комплектующие безопасно"""

            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    about_text,
                    reply_markup=get_back_to_main_keyboard(),
                    parse_mode="Markdown"
                )
            await safe_callback_answer(callback)
            return
        
        elif category_key == "contacts":
            contacts_text = """📞 **Контакты и заказ**

📱 **Канал:** @helprepairpc
🕐 **Время работы:** 9:00 - 21:00 (МСК)

📋 **Как заказать:**
1. Выберите услугу из меню
2. Нажмите "Заказать"
3. Ваша заявка будет отправлена
4. Мы свяжемся с вами для обсуждения деталей

💳 **Способы оплаты:**
• Банковская карта
• СБП
• Криптовалюта"""

            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    contacts_text,
                    reply_markup=get_contact_keyboard(),
                    parse_mode="Markdown"
                )
            await safe_callback_answer(callback)
            return
        
        # Получение услуг категории
        services = await db.get_services_by_category(category_name)
        
        if not services:
            no_services_text = f"📭 В категории **{category_name}** пока нет услуг.\n\nСкоро здесь появятся новые предложения!"
            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    no_services_text,
                    reply_markup=get_back_to_main_keyboard(),
                    parse_mode="Markdown"
                )
        else:
            services_text = f"📋 **{category_name}**\n\nВыберите интересующую вас услугу:"
            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    services_text,
                    reply_markup=get_category_keyboard(category_key, services),
                    parse_mode="Markdown"
                )
        
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("service_"))
    async def show_service(callback: CallbackQuery):
        """Показать информацию об услуге"""
        user = callback.from_user
        if not callback.data:
            return
            
        service_id = int(callback.data.split("_")[1])
        
        service = await db.get_service_by_id(service_id)
        if not service:
            await safe_callback_answer(callback)
            return
        
        # Логирование
        if user:
            await db.log_user_action(
                user.id,
                user.username or "unknown",
                "service_viewed",
                service['name']
            )
        
        # Определение категории для навигации
        category_key = get_category_by_name(service['category'])
        
        service_text = format_service_message(service)
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                service_text,
                reply_markup=get_service_keyboard(service_id, category_key),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("details_"))
    async def show_service_details(callback: CallbackQuery):
        """Показать подробную информацию об услуге"""
        user = callback.from_user
        if not callback.data:
            return
            
        service_id = int(callback.data.split("_")[1])
        
        service = await db.get_service_by_id(service_id)
        if not service:
            await safe_callback_answer(callback)
            return
        
        # Логирование
        if user:
            await db.log_user_action(
                user.id,
                user.username or "unknown",
                "service_details_viewed",
                service['name']
            )
        
        category_key = get_category_by_name(service['category'])
        detailed_text = format_detailed_service_message(service)
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                detailed_text,
                reply_markup=get_details_keyboard(service_id, category_key),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("order_"))
    async def process_order(callback: CallbackQuery):
        """Обработка заказа"""
        user = callback.from_user
        if not callback.data or not user:
            return
            
        service_id = int(callback.data.split("_")[1])
        
        service = await db.get_service_by_id(service_id)
        if not service:
            await safe_callback_answer(callback)
            return
        
        # Проверка настроек канала для заявок
        if not config.CHANNEL_ID:
            await safe_callback_answer(callback)
            return
        
        try:
            # Добавление заказа в базу
            await db.add_order(user.id, user.username or "unknown", service_id, service['name'])
            
            # Логирование
            await db.log_user_action(
                user.id,
                user.username or "unknown",
                "order_created",
                f"Service: {service['name']}, Price: {service['price']}"
            )
            
            # Уведомление клиента
            client_message = MESSAGES["order_success"].format(service_name=service['name'])
            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    client_message,
                    reply_markup=get_back_to_main_keyboard(),
                    parse_mode="Markdown"
                )
            
            # Публикация заявки в канал
            try:
                # Используем bot из контекста callback
                bot = callback.bot
                
                order_message = MESSAGES["manager_notification"].format(
                    service_name=service['name'],
                    username=user.username or "unknown",
                    time=datetime.now().strftime("%d.%m.%Y %H:%M"),
                    price=service['price'],
                    description=service['description']
                )
                
                # Публикуем заявку в канал
                if config.CHANNEL_ID:
                    try:
                        await bot.send_message(config.CHANNEL_ID, order_message, parse_mode="Markdown")
                        logger.info(f"Заявка опубликована в канал {config.CHANNEL_ID}")
                    except Exception as channel_error:
                        logger.error(f"Не удалось опубликовать в канал {config.CHANNEL_ID}: {channel_error}")
                        
                        # Если не удалось отправить в канал, уведомляем админа
                        if config.ADMIN_ID:
                            error_msg = f"⚠️ Не удалось опубликовать заявку от @{user.username or 'unknown'} в канал. Проверьте настройки канала."
                            try:
                                await bot.send_message(config.ADMIN_ID, error_msg)
                            except Exception as admin_error:
                                logger.error(f"Не удалось уведомить админа: {admin_error}")
                else:
                    # Если канал не настроен, уведомляем админа
                    if config.ADMIN_ID:
                        error_msg = f"⚠️ Канал для заявок не настроен! Заявка от @{user.username or 'unknown'} не была опубликована."
                        try:
                            await bot.send_message(config.ADMIN_ID, error_msg)
                        except Exception as admin_error:
                            logger.error(f"Не удалось уведомить админа: {admin_error}")
            
            except Exception as e:
                logger.error(f"Ошибка при отправке уведомления: {e}")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке заказа: {e}")
            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    "❌ Произошла ошибка при обработке заказа. Попробуйте позже.",
                    reply_markup=get_back_to_main_keyboard()
                )
        
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "back_to_main")
    async def back_to_main(callback: CallbackQuery):
        """Возврат в главное меню"""
        await show_main_menu(callback)
    
