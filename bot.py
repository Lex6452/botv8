from vkbottle import Bot, Message
from vkbottle.ext import Middleware
import vkbottle
import config
import random
import sqlite3


bot=Bot("0b5d858d41b1cebd0e960ade68f2e4514ede299d91413194135df0bfbde6bf7eeb1ccafd24b80154c88ea")#авторизация

#связь с базой
file="data.db"
db=sqlite3.connect(file)
cursor=db.cursor()

#предобработчик 
@bot.middleware.middleware_handler()
class MeddlewarePre(Middleware):
    async def pre(seld,ans:Message,*args):
    	#регистрация беседы
        if ans.from_chat:
           cursor.execute(f'SELECT * FROM "беседы" WHERE id = {ans.chat_id}')
           result = cursor.fetchall()
           if len(result) == 0:
               db.execute(f'INSERT INTO "беседы" (id,num,num_1) VALUES ({ans.chat_id}, 20,0)')
           
           #проверка количества сообщений
           else:
               num = cursor.execute(f'SELECT num FROM "беседы" WHERE id={ans.chat_id}').fetchall()[0][0]
               num_1 = cursor.execute(f'SELECT num_1 FROM "беседы" WHERE id={ans.chat_id}').fetchall()[0][0]
               if int(num)==int(num_1):
                   await ans(generation(5))
               num_1=0 if int(num_1)>=int(num) else num_1+1
               cursor.execute(f'UPDATE "беседы" SET num_1={num_1} WHERE id={ans.chat_id}')
        db.commit()
  


#генерация предложений
def generation(number):
    slovo=""
    i=random.choice(config.list)
    while len(slovo.split())<number:
        slovo+=f" {i}"
        if i not in config.bd:
            i=random.choice(config.list)
        i=random.choice(config.bd[i])
    slovo=slovo.replace("  ",". ").replace(". .",".").replace(". .",".")
    return slovo

	
#реация на сообщение "/gen"
@bot.on.message_handler(text="/gen")
@bot.on.message_handler(text="/gen <num:int>")
async def gen(ans:Message,num:int=5):
    text=generation(num)
    await ans(text)

#изменения нужного количества сообщений 
@bot.on.message_handler(text="/set")
@bot.on.message_handler(text="/set <num:int>")
async def gen(ans:Message,num:int=None):
    if num==None:
        await ans('вы не указали нужные аргументы\n"/set <число>"')
    else:
        await ans("настройки сохранены")
        cursor.execute(f'UPDATE "беседы" SET num={num} WHERE id={ans.chat_id}')
        db.commit()



bot.run_polling()