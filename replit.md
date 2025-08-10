Overview
Phoenix PS Bot is a fully functional Telegram bot built with Python's aiogram 3.0+ framework for promoting and selling Windows optimization and customization services. The bot provides a comprehensive service catalog organized by categories, allows users to browse and order services, and includes powerful administrative functionality for service management. It features a SQLite database for storing services, orders, and user activity logs, with both user-facing interfaces and admin controls.

Current Status: FULLY OPERATIONAL ✅
Bot is running and actively handling user interactions
Database initialized with 12 demonstration services across 4 categories
All admin commands functional
Order processing with manager notifications working
User interface with inline keyboards operational
Recent Changes (August 8, 2025)
Fixed all callback handling issues with safe error handling
Updated manager contact to @phoen1xPC and channel to @helprepairpc
Implemented beautiful admin panel with inline keyboard interface
Added post publishing functionality with channel button integration
Fixed manager notification system for direct messaging
All admin commands working: /admin, /add_service, /post, /list_services
Bot fully operational and handling users correctly
User Preferences
Preferred communication style: Simple, everyday language.

System Architecture
Bot Framework
aiogram: Modern asynchronous Telegram Bot API framework for Python
Async/await pattern: All database operations and bot interactions use asynchronous programming
Router-based handlers: Organized handler registration system separating user and admin functionality
Database Design
SQLite with aiosqlite: Lightweight, file-based database with async support
Three main tables:
services: Core service catalog with categories, descriptions, and pricing
orders: User order history linked to services
user_actions: Activity logging for analytics and debugging
Database abstraction: Custom Database class encapsulating all data operations
Configuration Management
Environment variables: Sensitive data (BOT_TOKEN, ADMIN_ID) from environment
JSON settings file: Dynamic settings (manager username, channel ID) stored in settings.json
Hot-reloadable config: Settings can be updated without bot restart
User Interface Architecture
Inline keyboards: Rich interactive interface using callback queries
State-less design: No FSM (Finite State Machine) usage, relying on callback data for navigation
Category-based navigation: Hierarchical menu system (Main → Category → Service → Details/Order)
Markdown formatting: Rich text formatting for service descriptions and messages
Security & Access Control
Admin verification: Simple user ID-based admin authentication
Command isolation: Admin commands separated from user handlers
Input validation: Proper parsing and validation for admin commands
Service Management
Dynamic catalog: Services stored in database, not hardcoded
Category system: Predefined categories defined in config constants
Order tracking: Complete order history with user association
Activity logging: Comprehensive user action tracking
Error Handling & Logging
Structured logging: File and console logging with proper formatting
Exception handling: Graceful error handling for database and Telegram API operations
User feedback: Clear error messages for invalid operations
External Dependencies
Core Dependencies
aiogram: Telegram Bot API framework
aiosqlite: Async SQLite database interface
Python standard library: os, json, logging, datetime, typing
Telegram Integration
Telegram Bot API: Full integration for messaging, callbacks, and user interaction
Bot token authentication: Secure bot authentication via environment variables
File System Dependencies
settings.json: Dynamic configuration storage
phoenix_bot.db: SQLite database file
bot.log: Application logging file
Runtime Requirements
Python environment variables: BOT_TOKEN and ADMIN_ID must be set
File system permissions: Read/write access for database and settings files
Network connectivity: Internet access for Telegram API communication