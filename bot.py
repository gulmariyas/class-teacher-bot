import os
import asyncio
import requests  # Нужна для отправки данных по ссылке
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
)

# Токен берется из переменных окружения
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
    
    # ССЫЛКА НА ФОРМУ: Вместо viewform в конце должно быть именно formResponse
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLS................/formResponse"
    
    # СВЯЗЫВАНИЕ ДАННЫХ: Замените 'entry.XXXXXXXXX' на реальные ID вопросов вашей формы
    form_data = {
        'entry.111111111': context.user_data.get('fio'),        # Поле 1 (ФИО)
        'entry.222222222': context.user_data.get('birth'),      # Поле 2 (Дата рождения)
        'entry.333333333': context.user_data.get('iin'),        # Поле 3 (ИИН)
        'entry.444444444': context.user_data.get('nat'),        # Поле 4 (Национальность)
        'entry.555555555': context.user_data.get('parents'),    # Поле 5 (ФИО родителей)
        'entry.666666666': context.user_data.get('edu'),        # Поле 6 (Образование)
        'entry.777777777': context.user_data.get('job'),        # Поле 7 (Место работы)
        'entry.888888888': context.user_data.get('addr'),       # Поле 8 (Адрес и телефон)
        'entry.999999999': context.user_data.get('status'),     # Поле 9 (Соц. статус)
        'entry.000000000': context.user_data.get('members'),    # Поле 10 (Состав семьи)
    }
    
    try:
        # Выполняем синхронный requests.post в асинхронном режиме, чтобы бот не зависал
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.post(form_url, data=form_data))
        
        if response.status_code == 200:
            await update.message.reply_text("✨ Спасибо! Данные успешно сохранены.")
        else:
            await update.message.reply_text("⚠️ Google отклонил запрос. Проверьте entry.ID полей.")
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка сети при отправке данных.")
        print(f"Ошибка Google Формы: {e}")
        
    # Очищаем данные текущего пользователя, чтобы при повторном заполнении не было старых значений
    context.user_data.clear()
        
    await start(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заполнение отменено.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # Очищаем временные данные
    await start(update, context)
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Обработка остальных ваших кнопок
    if text == "📋 Расписание уроков":
        await update.message.reply_text("Вот ваше расписание...")
    elif text == "📝 Домашнее задание":
        await update.message.reply_text("Домашнее задание на сегодня...")
    elif text == "🔗 Кунделик":
        await update.message.reply_text("Ссылка на Кунделик: https://kundelik.kz")
    elif text == "👤 Контакты учителя":
        await update.message.reply_text("Контакты классного руководителя: +7 (XXX) XXX-XX-XX")
    else:
        await update.message.reply_text("Пожалуйста, используйте меню для навигации.")

def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Описываем логику диалога
    survey_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^📊 Заполнить соц. паспорт$"), start_survey)],
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
        fallbacks=[CommandHandler("cancel", cancel), MessageHandler(filters.Regex("^Отмена$"), cancel)],
    )

    # Добавляем хендлеры в правильном порядке
    app.add_handler(CommandHandler("start", start))
    app.add_handler(survey_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот успешно запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
