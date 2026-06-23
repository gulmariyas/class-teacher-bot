from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)
import os

TOKEN = os.getenv("BOT_TOKEN")

# Определяем этапы (состояния) опроса
FIO_CHILD, STATUS_FAMILY, PHONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📋 Расписание уроков"), KeyboardButton("📝 Домашнее задание")],
        [KeyboardButton("🔗 Кунделик"), KeyboardButton("👤 Контакты учителя")],
        [KeyboardButton("📊 Заполнить соц. паспорт")]  # Новая кнопка для начала опроса
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я помощник классного руководителя. Выберите нужный раздел:",
        reply_markup=reply_markup
    )


# --- НАЧАЛО ОПРОСА ---
async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Начинаем заполнение социального паспорта.\n\n"
        "Вопрос 1: Введите ФИО ребенка (полностью) и класс:",
        reply_markup=ReplyKeyboardRemove()  # Убираем обычное меню на время опроса
    )
    return FIO_CHILD


async def answer_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем ответ пользователя в память бота
    context.user_data['fio_child'] = update.message.text
    
    # Задаем следующий вопрос
    await update.message.reply_text(
        "Вопрос 2: Укажите статус семьи (например: полная, многодетная, неполная):"
    )
    return STATUS_FAMILY


async def answer_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status_family'] = update.message.text
    
    await update.message.reply_text(
        "Вопрос 3: Введите ваш контактный номер телефона:"
    )
    return PHONE


async def answer_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    
    # Извлекаем все сохраненные ответы
    fio = context.user_data.get('fio_child')
    status = context.user_data.get('status_family')
    phone = context.user_data.get('phone')
    
    # Формируем итоговое сообщение
    await update.message.reply_text(
        f"Спасибо! Данные успешно приняты.\n\n"
        f"Проверьте ваши ответы:\n"
        f"🔹 ФИО ребенка: {fio}\n"
        f"🔹 Статус семьи: {status}\n"
        f"🔹 Телефон: {phone}"
    )
    
    # TODO: Здесь будет код, который отправляет данные в Excel/Google Таблицу
    
    # Возвращаем главное меню
    await start(update, context)
    return ConversationHandler.END


# Функция отмены опроса, если пользователь передумал
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заполнение анкеты отменено.")
    await start(update, context)
    return ConversationHandler.END


# Обработка остальных кнопок меню
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📋 Расписание уроков":
        await update.message.reply_text("Вот расписание уроков...")
    elif text == "📝 Домашнее задание":
        await update.message.reply_text("Актуальное домашнее задание...")
    elif text == "🔗 Кунделик":
        await update.message.reply_text("Перейти в электронный дневник: https://kundelik.kz")
    elif text == "👤 Контакты учителя":
        await update.message.reply_text("Связаться с классным руководителем: +7...")
    else:
        await update.message.reply_text("Пожалуйста, воспользуйтесь кнопками меню.")


# Сборка приложения
app = ApplicationBuilder().token(TOKEN).build()

# Создаем обработчик диалога (опроса)
survey_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text("📊 Заполнить соц. паспорт"), start_survey)],
    states={
        FIO_CHILD: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_fio)],
        STATUS_FAMILY: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_status)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(survey_handler)  # Сначала проверяем опрос
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) # Потом обычные кнопки

app.run_polling()
