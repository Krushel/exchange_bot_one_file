import json
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

TOKEN = '1660123518:AAGdSDHVmQjemThqPXDuuzDoZxSWCzt1KQA'


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests


def strForExchange(msg):
    currencies = msg.text.replace('/exchange ', '')
    currencies = currencies.replace('$', '')
    currencies = currencies.replace(' USD', '')
    currencies = currencies.split(' to ')
    return currencies


response = requests.get('https://api.exchangeratesapi.io/latest?base=USD').json()
response = response['rates']
list = '\n'.join([f'{key}: {round(value, 2)}' for key, value in response.items()])



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Йоу, бой!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler(commands=['list', 'lst'])
async def process_help_command(msg: types.Message):
    print(msg.from_user.id)
    await bot.send_message(msg.from_user.id, list)


@dp.message_handler(commands=['exchange', 'change'])
async def process_help_command(msg: types.Message):
    currencies = strForExchange(msg)
    print(currencies)
    value = float(currencies[0])
    currency  = response[currencies[1]]
    print(currency)
    print(value)
    await bot.send_message(msg.from_user.id, round(value*currency, 2))


@dp.message_handler(commands=['history', 'hstr'])
async def process_help_command(msg: types.Message):
    currency = msg.text.replace('/history ', '')
    currency = currency.replace('$', '')
    currency = currency.replace('USD/', '')
    responsegraph = requests.get(
        f'https://api.exchangeratesapi.io/history?start_at={datetime.now().date() - timedelta(days=7)}'
        f'&end_at={datetime.now().date()}&base=USD&symbols={currency}').json()
    responsegraph = responsegraph['rates']
    responsegraph = responsegraph.values()
    rates = []
    for key in responsegraph:
        rates.append(key[currency])
    plt.plot(rates)
    plt.savefig(f'images/{msg.from_user.id}.png')
    plt.delaxes()
    png = open(f'images/{msg.from_user.id}.png', 'rb')
    await bot.send_photo(msg.from_user.id, png,
                         caption=f"USD to {currency} graph")


@dp.message_handler(content_types=['text'])
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)