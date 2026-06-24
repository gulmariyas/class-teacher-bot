from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
)
import os
import requests  # Нужна для отправки данных по ссылке

TOKEN = os.getenv("BOT_TOKEN")

# Определение 10 этапов опроса
(
    FIO_STUDENT, BIRTH_DATE, IIN, NATIONALITY, PARENTS_FIO,
    EDUCATION, JOB, ADDRESS_PHONE, SOCIAL_STATUS, FAMILY_MEMBERS,
) = range(10)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📋 Расписание уроков"), KeyboardButton("📝 Домашнее задание")],
        [KeyboardButton("🔗 Кунделик"), KeyboardButton("👤 Контакты учителя")],
        [KeyboardButton("📊 Заполнить соц. паспорт")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Здравствуйте! Выберите нужный раздел:", reply_markup=reply_markup)

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вопрос 1: Введите ФИО ученика:", reply_markup=ReplyKeyboardRemove())
    return FIO_STUDENT

async def answer_fio_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fio'] = update.message.text
    await update.message.reply_text("Вопрос 2: Введите дату рождения ученика:")
    return BIRTH_DATE

async def answer_birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['birth'] = update.message.text
    await update.message.reply_text("Вопрос 3: Введите ИИН ученика:")
    return IIN

async def answer_iin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['iin'] = update.message.text
    await update.message.reply_text("Вопрос 4: Укажите национальность ученика:")
    return NATIONALITY

async def answer_nationality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nat'] = update.message.text
    await update.message.reply_text("Вопрос 5: Введите ФИО родителей:")
    return PARENTS_FIO

async def answer_parents_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['parents'] = update.message.text
    await update.message.reply_text("Вопрос 6: Укажите образование родителей:")
    return EDUCATION

async def answer_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['edu'] = update.message.text
    await update.message.reply_text("Вопрос 7: Укажите место работы родителей:")
    return JOB

async def answer_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['job'] = update.message.text
    await update.message.reply_text("Вопрос 8: Введите адрес проживания и телефон:")
    return ADDRESS_PHONE

async def answer_address_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['addr'] = update.message.text
    await update.message.reply_text("Вопрос 9: Укажите социальный статус семьи:")
    return SOCIAL_STATUS

async def answer_social_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = update.message.text
    await update.message.reply_text("Вопрос 10: Укажите состав семьи (количество детей):")
    return FAMILY_MEMBERS

async def answer_family_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['members'] = update.message.text
    
    # URL вашей формы. Вместо viewform в конце пишем formResponse
    # ЗАМЕНИТЕ ЭТОТ URL НА СВОЙ ИЗ ШАГА 1 (поставив ваши номера entry.XXXXX)
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLS................/formResponse"
    
    # Связываем ответы из бота с полями формы Google
    form_data = {
        'entry.111111111': context.user_data.get('fio'),        # Замените 111111111 на ваш ID первого поля
        'entry.222222222': context.user_data.get('birth'),      # Замените 222222222 на ваш ID второго поля
        'entry.333333333': context.user_data.get('iin'),
        'entry.444444444': context.user_data.get('nat'),
        'entry.555555555': context.user_data.get('parents'),
        'entry.666666666': context.user_data.get('edu'),
        'entry.777777777': context.user_data.get('job'),
        'entry.888888888': context.user_data.get('addr'),
        'entry.999999999': context.user_data.get('status'),
        'entry.000000000': context.user_data.get('members'),
    }
    
    try:
        # Бот сам «нажимает» кнопку отправить в Google Форме
        requests.post(form_url, data=form_data)
        await update.message.reply_text("✨ Спасибо! Данные успешно сохранены.")
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка при сохранении.")
        print(e)
        
    await start(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.")
    await start(update, context)
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Код обработки остальных ваших кнопок (расписание, кунделик...)
    pass

app = ApplicationBuilder().token(TOKEN).build()
survey_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text("📊 Заполнить соц. паспорт"), start_survey)],
    states={
        FIO_STUDENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_fio_student)],
        BIRTH_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_birth_date)],
        IIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_iin)],
        NATIONALITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_nationality)],
        PARENTS_FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_parents_fio)],
        EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_education)],
        JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_job)],
        ADDRESS_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_address_phone)],
        SOCIAL_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_social_status)],
        FAMILY_MEMBERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_family_members)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
app.add_handler(CommandHandler("start", start))
app.add_handler(survey_handler)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
