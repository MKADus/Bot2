# импорт необходимых модулей для работы
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from Bot_Alpha.config import TOKEN
from Bot_Alpha import db_session
from Bot_Alpha.keyboard import function_button
from Bot_Alpha.users import User

bot = Bot(token = TOKEN)

dp = Dispatcher(bot)

async def on_startup(_):
    print('Bot online. OK!')


# start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


class SateBot(StatesGroup):
    authorization = State()
    general = State()




@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    db_session.global_init('db/bot.db')
    await message.answer("Привет!",reply_markup=function_button(['Авторизация']))
    await message.delete()


@dp.message_handler()
async def command_dialog(message: types.Message):
    msg = message.text
    if msg == 'Авторизация':
        await SateBot.authorization.set()
        await message.answer('Введите пароль: ')


@dp.message_handler(state=SateBot.authorization)
async def password(message: types.Message):
    user = User()
    user_all = db_session.create_session().query(User).filter(User.name_id == str(message.from_user.id)).first()

    if not user_all:
        user.name = message.from_user.username
        user.name_id = message.from_user.id
        user.password = message.text
        db_sess = db_session.create_session()
        await message.answer('Авторизация прошла успешно!')
        db_sess.add(user)
        db_sess.commit()

        await SateBot.general.set()
    else:
        if db_session.create_session().query(User).filter(
                User.name_id == str(message.from_user.id)).first().password == message.text:
            await message.answer('Авторизация прошла успешно')

            await SateBot.general.set()
        else:
            await message.answer('Пароль неверный!\nПопробуйте еще раз')


@dp.message_handler(state=SateBot.general)
async def general(message: types.Message):
    pass





def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'], state='*')
