from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


button1 = KeyboardButton('/today')
button2 = KeyboardButton('/tomorrow')
button3 = KeyboardButton('/exams')

markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1, button2).add(button3)
