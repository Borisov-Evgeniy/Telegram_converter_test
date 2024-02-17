import logging  # Импортируем модуль logging для логирования
import asyncio  # Импортируем модуль asyncio для асинхронной работы
import requests  # Импортируем модуль requests для работы с HTTP-запросами
from aiogram import Bot, Dispatcher, types  # Импортируем необходимые классы из библиотеки aiogram
from aiogram.filters.command import Command  # Импортируем фильтр для обработки команд

# Включаем логирование на уровне INFO
logging.basicConfig(level=logging.INFO)
# Создаем объект бота с указанием токена
bot = Bot(token="6760477944:AAHI8HTxt8RjNavaqiE-AXn8afN4HD-HGhI")
# Создаем диспетчер для обработки сообщений
dp = Dispatcher()
# API ключ для доступа к сервису
api_key = " af650ecd5c71fd98908bf5d0a1d47a15"

# Функция для получения обменного курса валюты
def get_exchange_rate(api_key, from_currency, to_currency):
    # Формируем URL для запроса
    url = f"https://currate.ru/api/?get=rates&pairs={from_currency}{to_currency}&key={api_key}"
    # Отправляем GET-запрос
    response = requests.get(url)
    # Преобразуем ответ в формат JSON
    data = response.json()

    # Проверяем статус ответа и наличие данных
    if response.status_code == 200 and data.get('data'):
        # Извлекаем обменный курс из данных
        exchange_rate = data['data'].get(f"{from_currency}{to_currency}")
        return exchange_rate
    else:
        return None

# Обработчик команды /start
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply("Привет! Я бот для конвертации валют. Напиши /help, чтобы узнать доступные команды.")

# Обработчик команды /help
@dp.message(Command('help'))
async def help_command(message: types.Message):
    help_text = "Список доступных команд:\n"
    help_text += "/start - начать диалог с ботом\n"
    help_text += "/help - получить справку по доступным командам\n"
    help_text += "/convert <amount> <from_currency> to <to_currency> - конвертировать валюту (например, /convert 100 USDEUR)"
    await message.reply(help_text)

# Обработчик команды /convert
@dp.message(Command('convert'))
async def convert_command(message: types.Message):
    try:
        # Разбиваем текст команды на части
        command = message.text.split()
        print("Command parts:", command)
        amount = float(command[1])  # Извлекаем сумму для конвертации

        # Извлекаем валютные коды из команды
        from_currency = command[2].upper()
        to_currency = command[4].upper()

        # Выполняем конвертацию
        conversion_result = convert_currency(api_key, amount, from_currency, to_currency)
        # Отправляем результат пользователю
        await message.reply(f"{amount} {from_currency} = {conversion_result} {to_currency}")
    except Exception as e:
        # В случае ошибки отправляем сообщение об ошибке пользователю
        await message.reply("Ошибка при конвертации валюты. Пожалуйста, убедитесь, что вы ввели команду правильно и попробуйте снова.")

# Функция для конвертации валюты
def convert_currency(api_key, amount, from_currency, to_currency):
    exchange_rate = get_exchange_rate(api_key, from_currency, to_currency)
    # Проверяем наличие обменного курса
    if exchange_rate is not None:
        try:
            exchange_rate = float(exchange_rate)
            # Выполняем конвертацию
            converted_amount = amount * exchange_rate
            return converted_amount
        except ValueError:
            return "Ошибка при получении курса валюты. Курс обмена не является числом."
    else:
        return "Ошибка при получении курса валюты. Проверьте правильность введенных валютных кодов и повторите попытку."

# Обработчик для приветствия
@dp.message()
async def echo(message: types.Message):
    if message.text.lower() == 'привет':
        await message.reply("Привет! Чем могу помочь?")
    elif message.text.lower() == 'пока':
        await message.reply("До свидания!")
    else:
        await message.reply("Не понимаю, о чем вы. Напишите /help для списка доступных команд.")

# Основная функция для запуска бота
async def main():
    # Запускаем процесс обработки входящих сообщений
    await dp.start_polling(bot)

# Запускаем основную функцию
if __name__ == '__main__':
    asyncio.run(main())
