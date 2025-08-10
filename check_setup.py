#!/usr/bin/env python3
"""
Скрипт проверки готовности Phoenix PS Bot к запуску
"""

import os
import sys
import importlib.util

def check_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка версии Python...")
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Проверка зависимостей"""
    print("\n📦 Проверка зависимостей...")
    required_packages = ['aiogram', 'aiosqlite', 'dotenv']
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package}")
    
    if missing_packages:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите их командой: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Проверка файла .env"""
    print("\n🔧 Проверка конфигурации...")
    
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        print("Создайте файл .env с содержимым:")
        print("BOT_TOKEN=your_bot_token_here")
        print("ADMIN_ID=your_telegram_id_here")
        return False
    
    # Проверяем содержимое .env
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'BOT_TOKEN=' not in content:
        print("❌ BOT_TOKEN не найден в .env файле")
        return False
    
    if 'ADMIN_ID=' not in content:
        print("⚠️ ADMIN_ID не найден в .env файле (админские функции будут недоступны)")
    
    print("✅ Файл .env найден")
    return True

def check_database():
    """Проверка базы данных"""
    print("\n🗄️ Проверка базы данных...")
    
    if not os.path.exists('phoenix_bot.db'):
        print("⚠️ База данных не найдена")
        print("Запустите: python setup.py")
        return False
    
    print("✅ База данных найдена")
    return True

def check_files():
    """Проверка основных файлов"""
    print("\n📁 Проверка файлов проекта...")
    
    required_files = [
        'main.py',
        'config.py', 
        'database.py',
        'handlers.py',
        'admin_handlers.py',
        'keyboards.py',
        'utils.py',
        'settings.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Главная функция проверки"""
    print("🔍 Проверка готовности Phoenix PS Bot к запуску")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_env_file,
        check_database,
        check_files
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Все проверки пройдены! Бот готов к запуску.")
        print("\n🚀 Для запуска выполните:")
        print("python main.py")
    else:
        print("❌ Обнаружены проблемы. Исправьте их перед запуском.")
        print("\n📋 Рекомендуемые действия:")
        print("1. Установите зависимости: pip install -r requirements.txt")
        print("2. Создайте файл .env с BOT_TOKEN и ADMIN_ID")
        print("3. Запустите настройку: python setup.py")
        print("4. Запустите бота: python main.py")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main()) 