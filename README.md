# Telegram-BOT-with-database
An asynchronous Telegram calculator bot built with aiogram 3.x, featuring aiosqlite database integration and a built-in admin panel

# Telegram Bot Calculator with SQLite

An asynchronous Telegram bot that performs mathematical calculations on the fly and saves the complete operation history to a local SQLite database.

## 🛠 Tech Stack:
* **Python 3.12+**
* **Aiogram 3.x** — A modern asynchronous framework for the Telegram Bot API.
* **Aiosqlite** — An asynchronous library for interacting with SQLite3 without blocking the main event loop.

## ⚙️ Key Features:
1. **String Parsing Calculator:** The bot accepts math expressions separated by spaces (e.g., `10 * 5`), processes them using `.split()`, validates the input, and returns the correct result.
2. **Asynchronous Database:** All calculation history is safely recorded in a database file. Each user has access strictly to their own isolated history logs.
3. **Secure Admin System:** Integrated access control based on unique Telegram IDs. Users added to the administrator list unlock a secret menu capable of fetching full logs of all calculations from the DB.
4. **Exception Handling:** Robust crash protection using `try/except` blocks (handles division by zero `ZeroDivisionError` and character-instead-of-number inputs `ValueError`).

## 🚀 How to Run:
1. Provide your BotFather token in the `bot = Bot(token="...")` variable.
2. Add your numeric Telegram ID to the `ADMIN = [...]` list.
3. Run the script. The `users_database.db` file and its tables will be created automatically on startup.
