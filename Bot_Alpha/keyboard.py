from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button = KeyboardButton('Авторизаця')
replay_button = ReplyKeyboardMarkup()
replay_button.add(button)



def function_button(my_list: list):
    replay_button = ReplyKeyboardMarkup()
    for i in my_list:
        replay_button.add(KeyboardButton(i))