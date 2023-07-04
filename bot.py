import os
import logging

from aiogram import Bot, Dispatcher, executor, types


TOKEN = os.environ.get('TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Create Russian-English translitiration dictionary for small letters and 2 addition symbols(' ', '-')
translit_dict_lower = {'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 'ж':'zh', 'з':'z', 'и':'i', 'й':'i', 'к':'k', 
                'л':'l', 'м':'m', 'н':'n', 'о':'o','п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 'ф':'f', 'х':'kh', 'ц':'ts', 
                'ч':'ch', 'ш':'sh', 'щ':'shch', 'ъ':'ie', 'ы':'y', 'ь':'', 'э':'e', 'ю':'iu', 'я':'ia', ' ':' ', '-':'-'}

# Create full Russian-English translitiration dictionary for small and big letters and 2 addition symbols(' ', '-')
translit_dict_upper = {}
translit_dict_upper = {i.capitalize(): j.capitalize() for i, j in translit_dict_lower.items() if isinstance(i, str)}
translit_dict = {**translit_dict_lower, ** translit_dict_upper}

# Greeting new user
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Hello, {user_name}!'
    
    logging.info(f'{user_name=} {user_id=} sent message: {message.text}')
    await message.reply(text)

# Transliteration of input text. Works only for Russian text
def translit_name(text):
    result = ''
    for char in text: 
        try: 
            result += translit_dict[char]
        except: 
            return 'Попробуйте ввести другое имя'
    return result

# Messaging back with proper English transliteration 
@dp.message_handler()
async def send_translit(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = translit_name(message.text)
    logging.info(f'{user_name=} {user_id=} sent message: {message.text}')
    await bot.send_message(user_id, text)


if __name__ == '__main__':
    executor.start_polling(dp)