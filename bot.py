import os
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdtg2O-cQt91zmbEJe18PSeK--9ClWZ-dgAEvSNc1cKAmD8_Q/viewform?usp=header"
KUNDELIK_URL = "https://kundelik.kz"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📋 Расписание уроков"), KeyboardButton("📝 Домашнее задание")],
        [KeyboardButton("🔗 Кунделик"), KeyboardButton("👤 Контакты учителя")],
        [KeyboardButton("📊 Социальный паспорт")],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Здравствуйте! Выберите нужный раздел:",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📊 Социальный паспорт":
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="📝 Открыть форму соц. паспорта",
                    url=FORM_URL,
                )
            ]
        ]

        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_text(
            "Для заполнения социального паспорта нажмите на кнопку ниже.",
            reply_markup=inline_markup,
        )

    elif text == "📋 Расписание уроков":
        await update.message.reply_text(
            """
Вот расписание уроков

Понедельник
Математика
История Каз.
Физ-ра
Русс. яз.

Вторник
Русс. лит-ра
Математика
История
Худ труд
"""
        )

    elif text == "📝 Домашнее задание":
        await update.message.reply_text(
            "Актуальное домашнее задание по математике №952, №953"
        )

    elif text == "🔗 Кунделик":
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="🌐 Открыть Кунделик",
                    url=KUNDELIK_URL,
                )
            ]
        ]

        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_text(
            "Для перехода в Кунделик нажмите кнопку ниже:",
            reply_markup=inline_markup,
        )

    elif text == "👤 Контакты учителя":
        await update.message.reply_text(
            "Классный руководитель: Гульмария\nТелефон: +7XXXXXXXXXX"
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

app.run_polling()
