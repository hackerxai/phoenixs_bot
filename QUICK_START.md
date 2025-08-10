# 🚀 Быстрый запуск Phoenix PS Bot

## ⚡ За 5 минут

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Создание .env файла
Создайте файл `.env` в корневой папке:
```env
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_telegram_id
```

### 3. Настройка базы данных
```bash
python setup.py
```

### 4. Запуск бота
```bash
python main.py
```

## 🔧 Получение токена бота

1. Напишите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env`

## 👤 Получение вашего ID

1. Напишите [@userinfobot](https://t.me/userinfobot)
2. Скопируйте ваш ID в `.env`

## 🎯 Проверка готовности

```bash
python check_setup.py
```

## 🚀 Деплой на хостинг

### Replit.com (бесплатно)
```bash
python deploy.py replit
```

### Railway.app (бесплатно)
```bash
python deploy.py railway
```

### VPS
```bash
python deploy.py vps
```

## 📱 Использование

1. Отправьте боту `/start`
2. Выберите категорию услуг
3. Выберите услугу
4. Нажмите "Заказать"

## 🔧 Админ-панель

Отправьте `/admin` для доступа к админ-панели с кнопками.

## 🆘 Проблемы?

1. Проверьте логи: `tail -f bot.log`
2. Убедитесь, что `.env` файл создан правильно
3. Проверьте, что все зависимости установлены

## 📞 Поддержка

- Менеджер: @phoen1xPC
- Канал: @helprepairpc 