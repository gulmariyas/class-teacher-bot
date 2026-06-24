import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

# Ссылка на вашу Google Форму (или любую другую форму)
# Замените этот URL на реальную ссылку для заполнения родителями
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdtg2O-cQt91zmbEJe18PSeK--9ClWZ-dgAEvSNc1cKAmD8_Q/viewform?usp=header"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Главное меню бота (обычные кнопки внизу экрана)
    keyboard = [
        [KeyboardButton("📋 Расписание уроков"), KeyboardButton("📝 Домашнее задание")],
        [KeyboardButton("🔗 Кунделик"), KeyboardButton("👤 Контакты учителя")],
        [KeyboardButton("📊 Социальный паспорт")],  # Изменили текст кнопки на актуальный
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Выберите нужный раздел:", reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📊 Социальный паспорт":
        # Создаем инлайн-кнопку со ссылкой прямо под сообщением
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="📝 Открыть форму соц. паспорта", url=FORM_URL
                )
            ]
        ]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        # Отправляем сообщение с кнопкой-ссылкой
        await update.message.reply_text(
            "Для заполнения социального паспорта нажмите на кнопку ниже.\n"
            "Вы перейдете на форму, где сможете спокойно заполнить все данные.",
            reply_markup=inline_markup,
        )

    # Здесь вы можете обрабатывать остальные ваши кнопки
    elif text == "📋 Расписание уроков":
        await update.message.reply_text("Вот расписание уроков...")
    elif text == "📝 Домашнее задание":
        await update.message.reply_text("Вот домашнее задание...")
    elif text == "🔗 Кунделик":
        await update.message.reply_text("Ссылка на Кунделик...")
    elif text == "👤 Контакты учителя":
        await update.message.reply_text("Контакты учителя...")


# Настройка и запуск приложения
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
# Все текстовые сообщения (включая нажатия кнопок нижнего меню) летят сюда
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
