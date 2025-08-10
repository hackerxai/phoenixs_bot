import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import Config, CATEGORIES
from database import db
from keyboards import get_channel_post_keyboard

logger = logging.getLogger(__name__)

# Состояния для админа
admin_states = {}

def safe_callback_answer(callback):
    """Безопасный ответ на callback"""
    try:
        return callback.answer()
    except Exception:
        pass

def register_admin_handlers(dp, config: Config):
    """Регистрация админских хендлеров с красивым интерфейсом"""
    
    def is_admin(user_id: int) -> bool:
        """Проверка на права администратора"""
        return user_id == config.ADMIN_ID
    
    @dp.message(Command("admin"))
    async def cmd_admin(message: Message):
        """Главная админ-панель"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="📦 Управление услугами", callback_data="admin_services"))
        keyboard.row(InlineKeyboardButton(text="➕ Добавить услугу", callback_data="admin_add_service"))
        keyboard.row(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
        keyboard.row(InlineKeyboardButton(text="📝 Пост в канал", callback_data="admin_post"))
        keyboard.row(InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings"))
        keyboard.row(InlineKeyboardButton(text="❌ Закрыть", callback_data="admin_close"))
        
        admin_text = f"""🔧 **Админ-панель Phoenix PS Bot**

⚙️ **Текущие настройки:**
📢 Канал для заявок: {config.CHANNEL_ID or "не установлен"}

Выберите действие:"""
        
        await message.answer(
            admin_text,
            reply_markup=keyboard.as_markup(),
            parse_mode="Markdown"
        )
    
    @dp.callback_query(F.data == "admin_services")
    async def show_services_menu(callback: CallbackQuery):
        """Меню управления услугами"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        services_count = len(await db.get_all_services())
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="📋 Список услуг", callback_data="admin_list"))
        keyboard.row(InlineKeyboardButton(text="🗑️ Удалить услугу", callback_data="admin_delete_service"))
        keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu"))
        
        services_text = f"""📦 **Управление услугами**

📊 Всего услуг: {services_count}

Выберите действие:"""
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                services_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_add_service")
    async def start_add_service(callback: CallbackQuery):
        """Начало добавления услуги"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        admin_states[user.id] = "waiting_category"
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        keyboard = InlineKeyboardBuilder()
        
        # Добавляем кнопки для каждой категории
        for key, name in CATEGORIES.items():
            if key not in ['about', 'contacts']:  # Исключаем служебные категории
                keyboard.row(InlineKeyboardButton(text=name, callback_data=f"add_cat_{key}"))
        
        keyboard.row(InlineKeyboardButton(text="🔙 Отмена", callback_data="admin_menu"))
        
        add_text = """➕ **Добавление новой услуги**

📂 Выберите категорию для новой услуги:"""
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                add_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("add_cat_"))
    async def select_category_for_add(callback: CallbackQuery):
        """Выбор категории для добавления услуги"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        category_key = callback.data.split("_")[2]
        category_name = CATEGORIES.get(category_key, "Неизвестная категория")
        
        admin_states[user.id] = f"waiting_name_{category_key}"
        
        await callback.message.answer(
            f"📝 **Добавление услуги в категорию: {category_name}**\n\n"
            "Введите название услуги (например: '⚡ Базовая оптимизация Windows'):",
            parse_mode="Markdown"
        )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_delete_service")
    async def start_delete_service(callback: CallbackQuery):
        """Начало удаления услуги"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        services = await db.get_all_services()
        
        if not services:
            await callback.message.answer("📭 Услуг для удаления нет.")
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        keyboard = InlineKeyboardBuilder()
        
        # Показываем первые 10 услуг для удаления
        for service in services[:10]:
            service_name = service['name'][:30] + "..." if len(service['name']) > 30 else service['name']
            keyboard.row(InlineKeyboardButton(
                text=f"🗑️ {service_name}",
                callback_data=f"del_service_{service['id']}"
            ))
        
        keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_services"))
        
        delete_text = f"""🗑️ **Удаление услуги**

📋 Выберите услугу для удаления (показано {min(len(services), 10)} из {len(services)}):"""
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                delete_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("del_service_"))
    async def confirm_delete_service(callback: CallbackQuery):
        """Подтверждение удаления услуги"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        service_id = int(callback.data.split("_")[2])
        service = await db.get_service_by_id(service_id)
        
        if not service:
            await callback.message.answer("❌ Услуга не найдена.")
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_del_{service_id}"))
        keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data="admin_delete_service"))
        
        confirm_text = f"""🗑️ **Подтверждение удаления**

📋 Услуга: {service['name']}
💰 Цена: {service['price']}
📂 Категория: {service['category']}

❓ Вы уверены, что хотите удалить эту услугу?"""
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                confirm_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data.startswith("confirm_del_"))
    async def delete_service_confirmed(callback: CallbackQuery):
        """Удаление услуги после подтверждения"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        service_id = int(callback.data.split("_")[2])
        service = await db.get_service_by_id(service_id)
        
        if not service:
            await callback.message.answer("❌ Услуга не найдена.")
            await safe_callback_answer(callback)
            return
        
        success = await db.delete_service(service_id)
        
        if success:
            await callback.message.answer(f"✅ Услуга '{service['name']}' успешно удалена!")
        else:
            await callback.message.answer("❌ Ошибка при удалении услуги.")
        
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_settings")
    async def show_settings(callback: CallbackQuery):
        """Настройки бота"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="📢 Изменить канал для заявок", callback_data="admin_set_channel"))
        keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu"))
        
        settings_text = f"""⚙️ **Настройки бота**

📢 **Канал для заявок:** {config.CHANNEL_ID or "не установлен"}

Выберите настройку для изменения:"""
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                settings_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_set_manager")
    async def set_manager_ui(callback: CallbackQuery):
        """Установка менеджера через UI"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        admin_states[user.id] = "waiting_manager"
        
        await callback.message.answer(
            "👤 **Установка менеджера**\n\n"
            "Введите username менеджера (например: phoen1xPC):",
            parse_mode="Markdown"
        )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_set_channel")
    async def set_channel_ui(callback: CallbackQuery):
        """Установка канала через UI"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        admin_states[user.id] = "waiting_channel"
        
        await callback.message.answer(
            "📢 **Установка канала для заявок**\n\n"
            "Введите ID канала, куда будут публиковаться заявки (например: @helprepairpc или -1001234567890):",
            parse_mode="Markdown"
        )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_list")
    async def list_services(callback: CallbackQuery):
        """Список всех услуг"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        services = await db.get_all_services()
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_services"))
        
        if not services:
            list_text = """📭 **Список услуг пуст**

Используйте команды для добавления:
/add_service категория|название|описание|цена"""
        else:
            list_text = "📋 **Список всех услуг:**\n\n"
            
            for service in services:
                list_text += f"🔹 **ID {service['id']}**: {service['name']}\n"
                list_text += f"   💰 {service['price']} | 📂 {service['category']}\n\n"
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                list_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_stats")
    async def show_stats(callback: CallbackQuery):
        """Статистика бота"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        services_count = len(await db.get_all_services())
        orders_count = len(await db.get_all_orders())
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu"))
        
        stats_text = f"""📊 **Статистика бота**

📦 **Услуги:** {services_count}
📋 **Заказы:** {orders_count}
🕐 **Обновлено:** {datetime.now().strftime("%d.%m.%Y %H:%M")}

📈 **По категориям:**"""
        
        # Статистика по категориям
        for category_key, category_name in CATEGORIES.items():
            if category_key not in ['about', 'contacts']:
                cat_services = await db.get_services_by_category(category_name)
                stats_text += f"\n• {category_name}: {len(cat_services)} услуг"
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                stats_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_post")
    async def request_post(callback: CallbackQuery):
        """Запрос текста для поста"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        if not config.CHANNEL_ID:
            await callback.message.answer("❌ Канал не настроен! Используйте /set_channel")
            await safe_callback_answer(callback)
            return
        
        admin_states[user.id] = "waiting_post"
        
        await callback.message.answer(
            f"📝 **Отправьте текст для публикации в канал {config.CHANNEL_ID}:**\n\nБот автоматически добавит кнопку '🔥 Открыть меню'."
        )
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_close")
    async def close_admin(callback: CallbackQuery):
        """Закрыть админ-панель"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        if callback.message:
            await callback.message.delete()
        await safe_callback_answer(callback)
    
    @dp.callback_query(F.data == "admin_menu")
    async def show_admin_menu(callback: CallbackQuery):
        """Показать админ-меню"""
        user = callback.from_user
        if not user or not is_admin(user.id):
            await safe_callback_answer(callback)
            return
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="📦 Управление услугами", callback_data="admin_services"))
        keyboard.row(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
        keyboard.row(InlineKeyboardButton(text="📝 Пост в канал", callback_data="admin_post"))
        keyboard.row(InlineKeyboardButton(text="❌ Закрыть", callback_data="admin_close"))
        
        admin_text = f"""🔧 **Админ-панель Phoenix PS Bot**

⚙️ **Текущие настройки:**
📢 Канал для заявок: {config.CHANNEL_ID or "не установлен"}

Выберите действие:"""
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                admin_text,
                reply_markup=keyboard.as_markup(),
                parse_mode="Markdown"
            )
        await safe_callback_answer(callback)
    
    # Обработка текстовых сообщений от админа
    @dp.message()
    async def handle_admin_text(message: Message):
        """Обработка текстовых сообщений админа"""
        user = message.from_user
        if not user or not is_admin(user.id):
            return
        
        user_state = admin_states.get(user.id)
        
        # Если нет активного состояния, игнорируем сообщение
        if not user_state:
            return
        
        if user_state == "waiting_post":
            # Публикация поста с кнопкой
            if not message.text:
                await message.answer("❌ Отправьте текстовое сообщение.")
                return
            
            try:
                # Используем bot из контекста сообщения
                bot = message.bot
                
                # Отправка поста в канал
                await bot.send_message(
                    config.CHANNEL_ID,
                    message.text,
                    reply_markup=get_channel_post_keyboard(),
                    parse_mode="Markdown"
                )
                
                from aiogram.utils.keyboard import InlineKeyboardBuilder
                from aiogram.types import InlineKeyboardButton
                
                keyboard = InlineKeyboardBuilder()
                keyboard.row(InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_menu"))
                
                await message.answer(
                    f"✅ Пост опубликован в канале {config.CHANNEL_ID}!",
                    reply_markup=keyboard.as_markup()
                )
                
                admin_states.pop(user.id, None)
                
            except Exception as e:
                logger.error(f"Ошибка публикации поста: {e}")
                await message.answer(f"❌ Ошибка публикации: {str(e)}")
                admin_states.pop(user.id, None)
        
        elif user_state == "waiting_channel":
            # Установка канала для заявок
            if not message.text:
                await message.answer("❌ Отправьте ID канала для заявок.")
                return
            
            channel_id = message.text.strip()
            config.set_channel(channel_id)
            
            from aiogram.utils.keyboard import InlineKeyboardBuilder
            from aiogram.types import InlineKeyboardButton
            
            keyboard = InlineKeyboardBuilder()
            keyboard.row(InlineKeyboardButton(text="🔙 В настройки", callback_data="admin_settings"))
            
            await message.answer(
                f"✅ Канал для заявок установлен: {channel_id}",
                reply_markup=keyboard.as_markup()
            )
            admin_states.pop(user.id, None)
        
        elif user_state.startswith("waiting_name_"):
            # Добавление названия услуги
            if not message.text:
                await message.answer("❌ Отправьте название услуги.")
                return
            
            category_key = user_state.split("_")[2]
            category_name = CATEGORIES.get(category_key, "Неизвестная категория")
            service_name = message.text.strip()
            
            # Сохраняем название и переходим к описанию
            admin_states[user.id] = f"waiting_description_{category_key}_{service_name}"
            
            await message.answer(
                f"📝 **Добавление услуги: {service_name}**\n\n"
                "Введите описание услуги (например: 'Очистка системы от мусора, оптимизация автозагрузки'):",
                parse_mode="Markdown"
            )
        
        elif user_state.startswith("waiting_description_"):
            # Добавление описания услуги
            if not message.text:
                await message.answer("❌ Отправьте описание услуги.")
                return
            
            # Разбираем состояние: waiting_description_category_key_service_name
            parts = user_state.split("_", 3)  # Разделяем максимум на 3 части
            if len(parts) < 4:
                await message.answer("❌ Ошибка состояния. Начните заново.")
                admin_states.pop(user.id, None)
                return
            
            category_key = parts[2]
            service_name = parts[3]
            description = message.text.strip()
            
            # Сохраняем описание и переходим к цене
            admin_states[user.id] = f"waiting_price_{category_key}_{service_name}_{description}"
            
            await message.answer(
                f"💰 **Добавление услуги: {service_name}**\n\n"
                "Введите цену услуги (например: '1500 руб.' или 'Бесплатно'):",
                parse_mode="Markdown"
            )
        
        elif user_state.startswith("waiting_price_"):
            # Добавление цены услуги
            if not message.text:
                await message.answer("❌ Отправьте цену услуги.")
                return
            
            # Разбираем состояние: waiting_price_category_key_service_name_description
            parts = user_state.split("_", 4)  # Разделяем максимум на 4 части
            if len(parts) < 5:
                await message.answer("❌ Ошибка состояния. Начните заново.")
                admin_states.pop(user.id, None)
                return
            
            category_key = parts[2]
            service_name = parts[3]
            description = parts[4]
            price = message.text.strip()
            
            try:
                # Добавляем услугу в базу данных
                category_name = CATEGORIES.get(category_key, "Неизвестная категория")
                service_id = await db.add_service(service_name, description, price, category_name)
                
                from aiogram.utils.keyboard import InlineKeyboardBuilder
                from aiogram.types import InlineKeyboardButton
                
                keyboard = InlineKeyboardBuilder()
                keyboard.row(InlineKeyboardButton(text="➕ Добавить еще", callback_data="admin_add_service"))
                keyboard.row(InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_menu"))
                
                await message.answer(
                    f"✅ **Услуга успешно добавлена!**\n\n"
                    f"📋 Название: {service_name}\n"
                    f"💰 Цена: {price}\n"
                    f"📂 Категория: {category_name}\n"
                    f"🆔 ID: {service_id}",
                    reply_markup=keyboard.as_markup(),
                    parse_mode="Markdown"
                )
                
                admin_states.pop(user.id, None)
                
            except Exception as e:
                logger.error(f"Ошибка при добавлении услуги: {e}")
                await message.answer(f"❌ Ошибка при добавлении услуги: {str(e)}")
                admin_states.pop(user.id, None)
    
    # Старые команды для совместимости
    @dp.message(Command("add_service"))
    async def cmd_add_service(message: Message):
        """Добавление услуги (старая команда)"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        if not message.text:
            return
            
        try:
            args = message.text.split(" ", 1)[1].split("|")
            
            if len(args) != 4:
                await message.answer(
                    "❌ Формат: /add_service категория|название|описание|цена\n\n" +
                    "Категории:\n" + "\n".join([f"• {cat}" for cat in CATEGORIES.values() if cat not in ["🧾 О нас", "📞 Контакты и заказ"]])
                )
                return
            
            category, name, description, price = [arg.strip() for arg in args]
            
            service_id = await db.add_service(name, description, price, category)
            
            await message.answer(f"✅ Услуга добавлена! ID: {service_id}")
            
        except Exception as e:
            await message.answer(f"❌ Ошибка: {str(e)}")
    
    @dp.message(Command("delete_service"))
    async def cmd_delete_service(message: Message):
        """Удаление услуги"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        if not message.text:
            return
            
        try:
            service_id = int(message.text.split()[1])
            success = await db.delete_service(service_id)
            
            if success:
                await message.answer(f"✅ Услуга {service_id} удалена!")
            else:
                await message.answer("❌ Услуга не найдена.")
                
        except (IndexError, ValueError):
            await message.answer("❌ Укажите ID услуги: /delete_service 1")
        except Exception as e:
            await message.answer(f"❌ Ошибка: {str(e)}")
    
    @dp.message(Command("list_services"))
    async def cmd_list_services(message: Message):
        """Список услуг"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        services = await db.get_all_services()
        
        if not services:
            await message.answer("📭 Услуг пока нет.")
            return
        
        text = "📋 **Список услуг:**\n\n"
        for service in services:
            text += f"🔹 **ID {service['id']}**: {service['name']}\n"
            text += f"   💰 {service['price']} | 📂 {service['category']}\n\n"
        
        await message.answer(text, parse_mode="Markdown")
    
    @dp.message(Command("set_manager"))
    async def cmd_set_manager(message: Message):
        """Установка менеджера"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        if not message.text:
            return
            
        try:
            username = message.text.split(" ", 1)[1].strip().replace("@", "")
            config.set_manager(username)
            await message.answer(f"✅ Менеджер установлен: @{username}")
            
        except IndexError:
            await message.answer("❌ Укажите username: /set_manager phoen1xPC")
    
    @dp.message(Command("set_channel"))
    async def cmd_set_channel(message: Message):
        """Установка канала"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        if not message.text:
            return
            
        try:
            channel_id = message.text.split(" ", 1)[1].strip()
            config.set_channel(channel_id)
            await message.answer(f"✅ Канал установлен: {channel_id}")
            
        except IndexError:
            await message.answer("❌ Укажите канал: /set_channel @helprepairpc")
    
    @dp.message(Command("post"))
    async def cmd_post(message: Message):
        """Публикация в канал"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        if not message.text:
            return
            
        if not config.CHANNEL_ID:
            await message.answer("❌ Канал не установлен.")
            return
        
        try:
            post_text = message.text.split(" ", 1)[1]
            # Используем bot из контекста сообщения
            bot = message.bot
            
            await bot.send_message(
                config.CHANNEL_ID,
                post_text,
                reply_markup=get_channel_post_keyboard(),
                parse_mode="Markdown"
            )
            
            await message.answer(f"✅ Пост опубликован в {config.CHANNEL_ID}!")
            
        except IndexError:
            await message.answer("❌ Укажите текст: /post Ваш текст")
        except Exception as e:
            await message.answer(f"❌ Ошибка: {str(e)}")
    
    @dp.message(Command("admin_help"))
    async def cmd_admin_help(message: Message):
        """Помощь по админским командам"""
        user = message.from_user
        if not user or not is_admin(user.id):
            await message.answer("❌ Доступ запрещен.")
            return
        
        help_text = """🔧 **Админские команды Phoenix PS Bot**

**Интерфейс:**
• /admin - Админ-панель с кнопками

**Команды:**
• /add_service категория|название|описание|цена
• /list_services - список услуг
• /delete_service ID - удалить услугу
• /set_manager username - менеджер
• /set_channel @channel - канал
• /post текст - пост в канал

**Текущие настройки:**
• Менеджер: @{manager}
• Канал: {channel}""".format(
            manager=config.MANAGER_USERNAME or "не установлен",
            channel=config.CHANNEL_ID or "не установлен"
        )
        
        await message.answer(help_text, parse_mode="Markdown")