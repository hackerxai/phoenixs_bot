import sqlite3
import aiosqlite
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self, db_path: str = "phoenix_bot.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    service_id INTEGER NOT NULL,
                    service_name TEXT NOT NULL,
                    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (service_id) REFERENCES services (id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
            logger.info("База данных инициализирована")
    
    async def add_service(self, name: str, description: str, price: str, category: str) -> int:
        """Добавление новой услуги"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO services (name, description, price, category) VALUES (?, ?, ?, ?)",
                (name, description, price, category)
            )
            await db.commit()
            return cursor.lastrowid or 0
    
    async def get_services_by_category(self, category: str) -> List[Dict]:
        """Получение услуг по категории"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM services WHERE category = ? ORDER BY name",
                (category,)
            )
            rows = await cursor.fetchall()
            
            services = []
            for row in rows:
                services.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'category': row[4],
                    'created_at': row[5]
                })
            return services
    
    async def get_service_by_id(self, service_id: int) -> Optional[Dict]:
        """Получение услуги по ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM services WHERE id = ?",
                (service_id,)
            )
            row = await cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'category': row[4],
                    'created_at': row[5]
                }
            return None
    
    async def get_all_services(self) -> List[Dict]:
        """Получение всех услуг"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM services ORDER BY category, name"
            )
            rows = await cursor.fetchall()
            
            services = []
            for row in rows:
                services.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'category': row[4],
                    'created_at': row[5]
                })
            return services
    
    async def delete_service(self, service_id: int) -> bool:
        """Удаление услуги"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM services WHERE id = ?",
                (service_id,)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def add_order(self, user_id: int, username: str, service_id: int, service_name: str):
        """Добавление заказа"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO orders (user_id, username, service_id, service_name) VALUES (?, ?, ?, ?)",
                (user_id, username, service_id, service_name)
            )
            await db.commit()
    
    async def log_user_action(self, user_id: int, username: str, action: str, details: str = ""):
        """Логирование действий пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO user_actions (user_id, username, action, details) VALUES (?, ?, ?, ?)",
                (user_id, username, action, details)
            )
            await db.commit()

# Глобальный экземпляр базы данных
db = Database()

async def init_db():
    """Инициализация базы данных"""
    await db.init_db()
