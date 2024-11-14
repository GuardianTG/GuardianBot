import telebot
from telebot.types import ChatPermissions
import time
import os

# Токен бота, полученный от BotFather
TOKEN = os.getenv("7233973848:AAHpq0nfBC26yXbGhSKWI135T85h4egb1vs")  # замените на ваш токен, если запускаете локально

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Настройки
MUTE_DURATION = 30 * 60  # Мут на 30 минут (в секундах)
FORBIDDEN_WORDS = ["хуй"]

# Функция для проверки наличия запрещенных слов
def contains_forbidden_word(text):
    for word in FORBIDDEN_WORDS:
        if word in text.lower():
            return True
    return False

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text

    # Проверяем, содержит ли сообщение запрещенное слово
    if contains_forbidden_word(text):
        # Устанавливаем права для мута
        mute_permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False
        )
        
        # Мутим пользователя
        bot.restrict_chat_member(chat_id, user_id, permissions=mute_permissions, until_date=time.time() + MUTE_DURATION)
        
        # Отвечаем, что пользователь был замучен
        bot.reply_to(message, f"{message.from_user.first_name}, вы получили мут на 30 минут за использование запрещенных слов.")
        
        # Сразу отправляем сообщение о поддержании чистоты чата
        bot.send_message(chat_id, "Я Guardian, и я обеспечу чистый чат.")

# Запуск бота
bot.polling(none_stop=True)
