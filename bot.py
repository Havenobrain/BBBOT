import telebot
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_TOKEN = "7383584321:AAG2s-2lNn9VMtMYLKN5S_kiReFMGos_82w"


bot = telebot.TeleBot(API_TOKEN)


TARGET_CHANNEL_ID = '@thebestdream33'
TRIGGER_WORD = 'нет'


bot.remove_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Бот запущен и готов к работе.")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Доступные команды:\n"
        "/start - Запустить бота\n"
        "/help - Показать это сообщение\n"
        "/settrigger <слово> - Установить триггерное слово\n"
        "/settarget <канал> - Установить целевой канал\n"
    )
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['settrigger'])
def set_trigger(message):
    global TRIGGER_WORD
    args = message.text.split()[1:]
    if args:
        TRIGGER_WORD = args[0]
        bot.reply_to(message, f'Триггерное слово установлено: {TRIGGER_WORD}')
    else:
        bot.reply_to(message, 'Пожалуйста, укажите триггерное слово после команды /settrigger.')


@bot.message_handler(commands=['settarget'])
def set_target(message):
    global TARGET_CHANNEL_ID
    args = message.text.split()[1:]
    if args:
        TARGET_CHANNEL_ID = args[0]
        bot.reply_to(message, f'Целевой канал установлен: {TARGET_CHANNEL_ID}')
    else:
        bot.reply_to(message, 'Пожалуйста, укажите ID канала после команды /settarget.')


@bot.channel_post_handler(func=lambda message: True)
@bot.message_handler(func=lambda message: True)
def forward_message(message):
    if TRIGGER_WORD in message.text:
        bot.forward_message(TARGET_CHANNEL_ID, message.chat.id, message.message_id)
        logger.info(f"Сообщение переслано в канал {TARGET_CHANNEL_ID}")


if __name__ == '__main__':
    logger.info("Запуск бота...")
    bot.polling(none_stop=True)
