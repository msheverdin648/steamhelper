import config 
import logging

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter



#Задаем уровень логов
logging.basicConfig(level=logging.INFO)



#и=Инициализируем бота
bot = Bot(token=config.token)
dp = Dispatcher(bot)

#Инициализируем базу данных
db = SQLighter('botbd.db')


#Команда активации подписки
@dp.message_handler(commands= ['subscribe'])
async def subscribe(message: types.Message):
    if (not db. subscriber_exists(message.from_user.id)):
    #Если нет юзера, добавляем его
        db.add_subscribers(message.from_user.id)
    else:
    #Если юзер уже есть, то просто обновляем статус подписки
        db.update_subscription(message.from_user.id, True)
    await message.answer('Вы успешно подписались на рассылку! \nЖдите! БУ га га!')

@dp.message_handler(commands = ['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db. subscriber_exists(message.from_user.id)):
    #Если нет юзера, добавляем с некативной подпиской(запоминаем его)
        db.add_subscribers(message.from_user.id, False)
        await message.answer("Вы и так не подписаны.")
    else: 
    #Если есть юзер, то обновляем его статус
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки.")


#Запускаем лонг поллинг

if __name__ == '__main__':  
    executor.start_polling(dp, skip_updates=True)