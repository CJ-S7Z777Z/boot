import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Определяем тарифы
tariffs = [
    {"name": "Новичок", "cost": "900руб", "videos": 500},
    {"name": "Любитель", "cost": "4000руб", "videos": 1000},
    {"name": "Профи", "cost": "7500руб", "videos": 2000},
    {"name": "Бизнес", "cost": "14500руб", "videos": 3000},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение при команде /start."""
    keyboard = [
        [InlineKeyboardButton(tariff['name'], callback_data=f"tariff_{idx}")]
        for idx, tariff in enumerate(tariffs)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "У вас нет активного тарифа. Для использования бота вам нужно приобрести тариф.",
        reply_markup=reply_markup
    )

async def tariff_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия кнопок."""
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("tariff_"):
        idx = int(data.split('_')[1])
        tariff = tariffs[idx]
        # Показываем детали тарифа с кнопками Оплатить и Назад
        keyboard = [
            [InlineKeyboardButton("Оплатить", callback_data="pay")],
            [InlineKeyboardButton("Назад", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"Тариф: {tariff['name']}\nСтоимость: {tariff['cost']}\nКоличество видео: {tariff['videos']}"
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    elif data == "pay":
        # Ничего не происходит при нажатии Оплатить
        await query.answer("Функция оплаты пока не реализована.")
    elif data == "back":
        # Показываем снова список тарифов
        keyboard = [
            [InlineKeyboardButton(tariff['name'], callback_data=f"tariff_{idx}")]
            for idx, tariff in enumerate(tariffs)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="У вас нет активного тарифа. Для использования бота вам нужно приобрести тариф.",
            reply_markup=reply_markup
        )

def main():
    """Запуск бота."""
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token('7846138041:AAEu94LKLIr2D16xTGwN0emEczOHub2CP6I').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(tariff_callback))

    # Запускаем бота до нажатия Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
