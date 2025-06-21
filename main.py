# Список библиотек для скачивания можно глянуть в requirements.txt
import datetime
from PIL import Image, ImageDraw, ImageFont
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update, Bot, MessageEntity
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import traceback

# Логгер, чтобы был
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Не забудь вставить токен в token.txt!
token = open('token.txt', 'r').readline()

# Это фикс для Linux.
if '\n' in token:
    token = token[:-1]

bot = Bot(token=token)

# Я уже вставил нужный канал, но можно вставить и другой (только добавь туда бота заранее)
# Важно, чтобы формат был именно Bot API, а не Telegram API (если не знаешь, просто добавь -100 в начале айди)
channel = -1001760814576

plurCount = {
            0:"Нулевого",
            1:"Первого",
            2:"Второго",
            3:"Третьего",
            4:"Четвёртого",
            5:"Пятого",
            6:"Шестого",
            7:"Седьмого",
            8:"Восьмого",
            9:"Девятого",
            10:"Десятого",
            11:"Одиннадцатого",
            12:"Двенадцатого",
            13:"Тринадцатого",
            14:"Четырнадцатого",
            15:"Пятнадцатого",
            16:"Шестнадцатого",
            17:"Семнадцатого",
            18:"Восемнадцатого",
            19:"Девятнадцатого",
            20:"Двадцатого",
            "2x":"Двадцать",
            30:"Тридцатого",
            "3x":"Тридцать",
            40:"Сорокового",
            "4x":"Сорок",
            50:"Пятидесятого",
            "5x":"Пятьдесят",
            60:"Шестидесятого",
            "6x":"Шестьдесят",
            70:"Семидесятого",
            "7x":"Семьдесят",
            80:"Восьмидесятого",
            "8x":"Восемьдесят",
            90:"Девяностого",
            "9x":"Девяносто",
            100:"Сотого",
            "1xx":"Сто",
            200:"Двухсотого",
            "2xx":"Двести",
            300:"Трёхсотого",
            "3xx":"Триста" # мне дальше лень
            }

# Плейсхолдер, можно вырезать
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Часики тикают. Судьба неизбежна. The fog is coming.\nХотите узнать точное время до анонсов в канале - используйте /howmuch.")

# Запуск расписания
async def start_countdown():
    scheduler.start()

# Отсчёт в реальном времени (на момент запроса) ((работает в ЛС и в чате, НЕ В САМОМ КАНАЛЕ))
async def howmuch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    much = datetime.datetime(2025, 12, 20) - datetime.datetime.now()
    left = (datetime.datetime(2024, 12, 20) - datetime.datetime.now()) * -1
    await update.message.reply_text(text=f"До дембеля (20 декабря 2025 0:00 МСК) осталось {much.days} дн., {much.seconds//3600} ч., {much.seconds%3600//60} мин., {much.seconds%60} сек. В процентах это {(left.days*86400+left.seconds)*100/(365*86400)}%")

# На случай, если генерация пойдёт не по плану, эта команда может выполнить досрочную генерацию в канал (работает в ЛС и в чате)
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = False
    try:
        member = await bot.get_chat_member(channel, update.effective_user.id)
    except:
        await update.message.reply_text(text="Что-то пошло не так. Либо вас нет в канале, либо меня...")
    if member:
        if member.status == 'creator' or (member.status == 'administrator' and member.can_post_messages):
            try:
                await countdown()
            except Exception as e:
                await update.message.reply_text(text=f'Всё ещё хуже, чем ожидалось.\nПожалуйста, уведомите @cheat_r о случившейся катастрофе:\n{traceback.format_exc()}', entities=[MessageEntity(MessageEntity.PRE,86,len(traceback.format_exc()),language='py')])
        else:
            await update.message.reply_text(text="Для выполнения команды требуются права на отправку сообщений в канале.")



async def countdown():
    try:
        # Здесь стоит начало и завершение таймера
        deltaStart = (datetime.datetime(2024, 12, 20) - datetime.datetime.now()).days*-1
        deltaFinish = (datetime.datetime(2025, 12, 20) - datetime.datetime.now()).days+1
        
        # Завершение таймера (костыльное немного)
        if deltaStart == 366:
            await bot.send_photo(chat_id=channel, photo=open("img/fate.png", "rb"), caption=('Дембель.'))
            exit()

        firstNum = int(str(deltaFinish)[-1])
        if firstNum == 1:
            plurDay = "ДЕНЬ"
            plurLeft = "ОСТАЛСЯ"
        elif 2 <= firstNum <= 4:
            plurDay = "ДНЯ"
            plurLeft = "ОСТАЛОСЬ"
        else:
            plurDay = "ДНЕЙ"
            plurLeft = "ОСТАЛОСЬ"

        if not deltaStart in plurCount:
            firstNum = int(str(deltaStart)[-1])
            secondNum = str(deltaStart)[-2]
            if 10 <= deltaStart <= 99:
                count = plurCount[secondNum+'x'].upper()+' '+plurCount[firstNum].upper()
            else:
                thirdNum = str(deltaStart)[-3]
                if secondNum == '0':
                    count = plurCount[thirdNum+'xx'].upper()+' '+plurCount[firstNum].upper()
                elif int(secondNum + str(firstNum)) in plurCount:
                    count = plurCount[thirdNum+'xx'].upper()+' '+plurCount[int(secondNum+str(firstNum))].upper()
                else:
                    count = plurCount[thirdNum+'xx'].upper()+' '+plurCount[secondNum+'x'].upper()+' '+plurCount[firstNum].upper()
        else:
            count = plurCount[deltaStart].upper()

        # Генерация изображения и дальнейшая отправка
        image = Image.new("RGB", (1280, 720), "black")
        draw = ImageDraw.Draw(image)
        draw.font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 72)
        draw.text(xy=(640, 240), text="НАЧАЛО", fill="white", anchor="mm")
        if deltaStart <= 20 or deltaStart == 365:
            draw.font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 108)
        else:
            draw.font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 72)
        draw.text(xy=(640, 330), text=(("ПОСЛЕДНЕГО" if deltaStart == 365 else count.upper())+" ДНЯ"), fill="white", anchor="mm")
        draw.font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 60)
        if 363 <= deltaStart <= 365:
            if deltaStart == 363:
                text = "72 ЧАСА"
            elif deltaStart == 364:
                text = "48 ЧАСОВ"
            else:
                text = "24 ЧАСА"
            draw.text(xy=(640, 480), text=(f"-ОСТАЛОСЬ {text}-"), fill="white", anchor="mm")
        else:
            draw.text(xy=(640, 480), text=f"-{plurLeft.upper()} {deltaFinish} {plurDay.upper()}-", fill="white", anchor="mm")

        image.save(fp=("img/coming.png"))

        await bot.send_photo(chat_id=channel, photo=open("img/coming.png", "rb"), caption=(f'До дембеля {plurLeft.lower()} {deltaFinish} {plurDay.lower()} (пройдено {round((deltaStart-1)/365*100,2)}%)'))
    except Exception:
        await bot.send_message(chat_id=channel, text=f'Я сбился со счёту времени... (произошла ошибка со стороны разработчика)\nПожалуйста, перегенерируйте сообщение вручную с помощью команды /gen в ЛС.\nДалее следует информация, полезная для разработчика:\n{traceback.format_exc()}',entities=[MessageEntity(MessageEntity.ITALIC,0,28),MessageEntity(MessageEntity.PRE,200,len(traceback.format_exc()),language='py')])

# Создание расписания (можно установить своё время)
scheduler = AsyncIOScheduler()
scheduler.add_job(
    countdown,
    trigger='cron',
    hour='00',
    minute='00',
    second='00'
)

# Запуск бота
if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('howmuch', howmuch))
    application.add_handler(CommandHandler('gen', gen))
    asyncio.get_event_loop().create_task(start_countdown())
    application.run_polling()
