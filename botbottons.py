from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

# Функция, которая срабатывает на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Создаем список кнопок. Каждый внутренний список — это один ряд кнопок.
    keyboard = [
        [KeyboardButton("📋 Расписание уроков"), KeyboardButton("📝 Домашнее задание")],
        [KeyboardButton("🔗 Кунделик"), KeyboardButton("👤 Контакты учителя")]
    ]
    
    # 2. Создаем саму клавиатуру
    # resize_keyboard=True делает кнопки аккуратными по размеру текста
    # one_time_keyboard=False означает, что кнопки не исчезнут после одного нажатия
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    # 3. Отправляем приветствие вместе с кнопками
    await update.message.reply_text(
        "Здравствуйте! Я помощник классного руководителя. Выберите нужный раздел на кнопках ниже:",
        reply_markup=reply_markup
    )

# Функция, которая обрабатывает нажатия на кнопки (читает текст сообщений)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Расписание уроков":
        await update.message.reply_text("Вот расписание уроков на эту неделю:\n1. Математика\n2. Русский язык\n3. Литература")
        
    elif text == "📝 Домашнее задание":
        await update.message.reply_text("Актуальное домашнее задание вы можете проверить в системе Кунделик или здесь (текст задания).")
        
    elif text == "🔗 Кунделик":
        # Тут можно сразу дать ссылку на сайт электронного дневника
        await update.message.reply_text("Перейти в электронный дневник: https://kundelik.kz")
        
    elif text == "👤 Контакты учителя":
        await update.message.reply_text("Связаться с классным руководителем можно по телефону:\n+7 (XXX) XXX-XX-XX\nЧасы для связи: с 15:00 до 18:00.")
        
    else:
        # Ответ, если пользователь просто напишет боту что-то свое
        await update.message.reply_text("Пожалуйста, воспользуйтесь кнопками меню для получения информации.")

# Сборка приложения
app = ApplicationBuilder().token(TOKEN).build()

# Регистрируем обработчик для команды /start
app.add_handler(CommandHandler("start", start))

# Регистрируем обработчик для текста (он будет ловить нажатия на кнопки)
# filters.TEXT & ~filters.COMMAND означает: ловить любой текст, кроме команд (вроде /start)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
app.run_polling()
