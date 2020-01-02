import logging
import os
from api import get_today_lessons, get_exams, get_tomorrow_lessons
from config import API_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from keyboard import markup

# TOKEN = os.environ['TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет, это бот расписания группы 622401!\nИспользуй /help, '
                        'чтобы узнать список доступных команд!', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Команды:\n/today - получение расписания на сегодня\n/tomorrow - получение расписания на завтра\n/exams - получчение расписания экзаменов\n/cat - фоткa котика)\n/dog - фотка песика)')


@dp.message_handler(commands=['cat'])
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(commands=['dog'])
async def cats(message: types.Message):
    with open('data/dogs.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Dogs are here 🐶')


@dp.message_handler(commands=['today'])
async def schedule(message: types.Message):
    schedule, current_week, current_day_schedule = get_today_lessons()
    msg = f"Сегодня: {current_day_schedule.upper()}\n \n"
    for index, value in enumerate(schedule):
        if current_week in value['weekNumber']:
            if value['lessonType'] == 'ЛК':
                lesson_type_emodji = '📗'
            elif value['lessonType'] == 'ЛР':
                lesson_type_emodji = '📕'
            elif value['lessonType'] == 'ПЗ':
                lesson_type_emodji = '📙'
            msg += f"{index+1}. {value['subject']}\n 🕑{value['lessonTime']}\n{lesson_type_emodji}{value['lessonType']}\n🚪{value['auditory'][0]}\n👤{value['employee'][0]['fio']}\n \n"

    await message.reply(msg)


@dp.message_handler(commands=['tomorrow'])
async def schedule(message: types.Message):
    schedule, current_week, tomorrow_day_schedule = get_tomorrow_lessons()
    msg = f"Завтра: {tomorrow_day_schedule.upper()}\n \n"
    for index, value in enumerate(schedule):
        if current_week in value['weekNumber']:
            if value['lessonType'] == 'ЛК':
                lesson_type_emodji = '📗'
            elif value['lessonType'] == 'ЛР':
                lesson_type_emodji = '📕'
            elif value['lessonType'] == 'ПЗ':
                lesson_type_emodji = '📙'
            msg += f"{index+1}. {value['subject']}\n 🕑{value['lessonTime']}\n{lesson_type_emodji}{value['lessonType']}\n🚪{value['auditory'][0]}\n👤{value['employee'][0]['fio']}\n \n"

    await message.reply(msg)


@dp.message_handler(commands=['exams'])
async def schedule(message: types.Message):
    exams = get_exams()
    msg = f"Экзамены:\n \n"
    for value in exams:
        if value['schedule'][0]['lessonType'] == 'Экзамен':
            lesson_type_emodji = '📕'
        elif value['schedule'][0]['lessonType'] == 'Консультация':
            lesson_type_emodji = '📙'

        msg += f"📅{value['weekDay']}\n🕑{value['schedule'][0]['lessonTime']}\n🚪{value['schedule'][0]['auditory'][0]}\n{lesson_type_emodji}{value['schedule'][0]['subject']}({value['schedule'][0]['lessonType']})\n👤{value['schedule'][0]['employee'][0]['fio']}\n \n"
    await message.reply(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
