import requests
import datetime
from requests.exceptions import HTTPError


def get_connection():
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=622401'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = response.json()

        return data


def get_today_lessons():
    data = get_connection()
    current_weekday = datetime.datetime.today().weekday()
    current_week = data['currentWeekNumber']
    schedule = data['schedules']

    try:
        current_day_schedule = schedule[current_weekday]
    except IndexError:
        current_day_schedule = []

    if current_day_schedule:
        lessons = current_day_schedule['schedule']
        return lessons, current_week, current_day_schedule['weekDay']
    else:
        return 'выходной'


def get_tomorrow_lessons():
    data = get_connection()
    if datetime.datetime.today().weekday() == 6:
        tomorrow_weekday = 0
    else:
        tomorrow_weekday = datetime.datetime.today().weekday() + 1
    current_week = data['currentWeekNumber']
    schedule = data['schedules']

    try:
        tomorrow_day_schedule = schedule[tomorrow_weekday]
    except IndexError:
        tomorrow_day_schedule = []

    if tomorrow_day_schedule:
        lessons = tomorrow_day_schedule['schedule']
        return lessons, current_week, tomorrow_day_schedule['weekDay']
    else:
        return 'выходной'


def get_exams():
    data = get_connection()
    exams = data['examSchedules']

    return exams
