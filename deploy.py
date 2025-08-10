#!/usr/bin/env python3
"""
Скрипт деплоя Phoenix PS Bot на разные платформы
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_requirements():
    """Проверка требований для деплоя"""
    print("🔍 Проверка требований для деплоя...")
    
    # Проверяем наличие .env файла
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("Создайте файл .env с содержимым:")
        print("BOT_TOKEN=your_bot_token_here")
        print("ADMIN_ID=your_telegram_id_here")
        return False
    
    # Проверяем наличие базы данных
    if not os.path.exists('phoenix_bot.db'):
        print("⚠️ База данных не найдена. Запускаем настройку...")
        try:
            subprocess.run([sys.executable, 'setup.py'], check=True)
            print("✅ База данных создана")
        except subprocess.CalledProcessError:
            print("❌ Ошибка при создании базы данных")
            return False
    
    print("✅ Все требования выполнены")
    return True

def deploy_local():
    """Деплой для локального запуска"""
    print("\n🏠 Деплой для локального запуска")
    print("=" * 40)
    
    if not check_requirements():
        return False
    
    print("🚀 Запуск бота...")
    try:
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False
    
    return True

def deploy_replit():
    """Деплой для Replit"""
    print("\n☁️ Деплой для Replit")
    print("=" * 40)
    
    # Создаем .replit файл
    replit_config = {
        "language": "python3",
        "run": "python main.py",
        "entrypoint": "main.py"
    }
    
    with open('.replit', 'w') as f:
        json.dump(replit_config, f, indent=2)
    
    # Создаем pyproject.toml для Replit
    pyproject_content = """[tool.poetry]
name = "phoenix-ps-bot"
version = "1.0.0"
description = "Telegram bot for Phoenix PS services"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
aiogram = "^3.0.0"
aiosqlite = "^0.19.0"
python-dotenv = "^1.0.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
    
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_content)
    
    print("✅ Файлы для Replit созданы")
    print("\n📋 Инструкции для Replit:")
    print("1. Создайте новый проект на replit.com")
    print("2. Выберите Python")
    print("3. Загрузите все файлы проекта")
    print("4. В Secrets добавьте переменные:")
    print("   - BOT_TOKEN: ваш токен бота")
    print("   - ADMIN_ID: ваш Telegram ID")
    print("5. Нажмите Run")
    
    return True

def deploy_railway():
    """Деплой для Railway"""
    print("\n🚂 Деплой для Railway")
    print("=" * 40)
    
    # Создаем Procfile для Railway
    procfile_content = "worker: python main.py"
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    # Создаем runtime.txt
    runtime_content = "python-3.11.0"
    
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    
    print("✅ Файлы для Railway созданы")
    print("\n📋 Инструкции для Railway:")
    print("1. Создайте аккаунт на railway.app")
    print("2. Подключите ваш GitHub репозиторий")
    print("3. В Variables добавьте:")
    print("   - BOT_TOKEN: ваш токен бота")
    print("   - ADMIN_ID: ваш Telegram ID")
    print("4. Railway автоматически развернет бота")
    
    return True

def deploy_heroku():
    """Деплой для Heroku"""
    print("\n🦸 Деплой для Heroku")
    print("=" * 40)
    
    # Создаем Procfile для Heroku
    procfile_content = "worker: python main.py"
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    # Создаем runtime.txt
    runtime_content = "python-3.11.0"
    
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    
    # Создаем app.json
    app_json = {
        "name": "Phoenix PS Bot",
        "description": "Telegram bot for Phoenix PS services",
        "repository": "https://github.com/yourusername/phoenix-ps-bot",
        "keywords": ["python", "telegram", "bot", "aiogram"],
        "env": {
            "BOT_TOKEN": {
                "description": "Telegram Bot Token from @BotFather",
                "required": True
            },
            "ADMIN_ID": {
                "description": "Your Telegram User ID",
                "required": True
            }
        },
        "buildpacks": [
            {
                "url": "heroku/python"
            }
        ]
    }
    
    with open('app.json', 'w') as f:
        json.dump(app_json, f, indent=2)
    
    print("✅ Файлы для Heroku созданы")
    print("\n📋 Инструкции для Heroku:")
    print("1. Установите Heroku CLI")
    print("2. Выполните команды:")
    print("   heroku login")
    print("   heroku create your-bot-name")
    print("   heroku config:set BOT_TOKEN=your_token")
    print("   heroku config:set ADMIN_ID=your_id")
    print("   git add .")
    print("   git commit -m 'Deploy to Heroku'")
    print("   git push heroku main")
    print("   heroku ps:scale worker=1")
    
    return True

def deploy_vps():
    """Деплой для VPS"""
    print("\n🖥️ Деплой для VPS")
    print("=" * 40)
    
    # Создаем systemd сервис
    service_content = """[Unit]
Description=Phoenix PS Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/phoenix-ps-bot
Environment=PATH=/root/phoenix-ps-bot/venv/bin
ExecStart=/root/phoenix-ps-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open('phoenix-bot.service', 'w') as f:
        f.write(service_content)
    
    # Создаем скрипт установки
    install_script = """#!/bin/bash
echo "🚀 Установка Phoenix PS Bot на VPS..."

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Создание директории
mkdir -p /root/phoenix-ps-bot
cd /root/phoenix-ps-bot

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка бота
python setup.py

# Копирование systemd сервиса
sudo cp phoenix-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable phoenix-bot
sudo systemctl start phoenix-bot

echo "✅ Бот установлен и запущен!"
echo "📋 Команды управления:"
echo "  sudo systemctl status phoenix-bot  # Статус"
echo "  sudo systemctl restart phoenix-bot  # Перезапуск"
echo "  sudo systemctl stop phoenix-bot     # Остановка"
echo "  sudo journalctl -u phoenix-bot -f   # Логи"
"""
    
    with open('install_vps.sh', 'w') as f:
        f.write(install_script)
    
    # Делаем скрипт исполняемым
    os.chmod('install_vps.sh', 0o755)
    
    print("✅ Файлы для VPS созданы")
    print("\n📋 Инструкции для VPS:")
    print("1. Загрузите файлы на VPS")
    print("2. Создайте файл .env с переменными")
    print("3. Выполните: chmod +x install_vps.sh")
    print("4. Запустите: ./install_vps.sh")
    
    return True

def main():
    """Главная функция"""
    print("🚀 Деплой Phoenix PS Bot")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("📋 Доступные платформы:")
        print("  local    - Локальный запуск")
        print("  replit   - Replit.com")
        print("  railway  - Railway.app")
        print("  heroku   - Heroku.com")
        print("  vps      - VPS сервер")
        print("\n💡 Пример: python deploy.py local")
        return 1
    
    platform = sys.argv[1].lower()
    
    if platform == "local":
        return 0 if deploy_local() else 1
    elif platform == "replit":
        return 0 if deploy_replit() else 1
    elif platform == "railway":
        return 0 if deploy_railway() else 1
    elif platform == "heroku":
        return 0 if deploy_heroku() else 1
    elif platform == "vps":
        return 0 if deploy_vps() else 1
    else:
        print(f"❌ Неизвестная платформа: {platform}")
        return 1

if __name__ == "__main__":
    exit(main()) 