# Список библиотек для скачивания можно глянуть в requirements.txt
import datetime
from PIL import Image, ImageDraw, ImageFont
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Логгер чтобы был, убрал httpx чтоб он не срал не какал не писял каждые пять секунд
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Не забудь вставить токен в token.txt
token = open('token.txt', 'r').readline()
bot = Bot(token=token)

# Я уже вставил нужный канал, но можно вставить и другой (только добавь туда бота заранее)
# Важно, чтобы формат был именно Bot API, а не Telegram API (разница в -100 в начале айди каналов. я сам без понятия.)
channel = -1002016542799

# Здесь дата уже стоит, но по желанию можно поставить свою
deltaStart = (datetime.datetime(2024, 12, 20) - datetime.datetime.now()).days*-1
deltaFinish = (datetime.datetime(2025, 12, 20) - datetime.datetime.now()).days+1

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
            "3xx":"Триста"
            }

# Команда для запуска расписания (ежедневно в полночь по времени хоста)
# ВЫПОЛНЯТЬ ПРИ КАЖДОМ ЗАПУСКЕ СКРИПТА (извините за костыль)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        scheduler.start()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Таймер запущен. Судьба неизбежна. The fog is coming.")
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Спасибо, я уже завёлся.")

async def countdown():
    # Завершение работы улицы сезам
    if deltaStart == 366:
        await bot.send_photo(chat_id=channel, photo=open("img/fate.png", "rb"), caption=('Дембель.'))
        exit()

    firstNum = int(str(deltaFinish)[-1])
    if firstNum == 1:
        plurDay = "День"
        plurLeft = "Остался"
    elif 2 <= firstNum <= 4:
        plurDay = "Дня"
        plurLeft = "Осталось"
    else:
        plurDay = "Дней"
        plurLeft = "Осталось"

    if not deltaStart in plurCount:
        firstNum = int(str(deltaStart)[-1])
        secondNum = str(deltaStart)[-2]
        if 10 <= deltaStart <= 99:
            count = plurCount[secondNum+'x']+' '+plurCount[firstNum]
        else:
            thirdNum = str(deltaStart)[-3]
            count = plurCount[thirdNum+'xx']+' '+plurCount[secondNum+'x']+' '+plurCount[firstNum]
    else:
        count = plurCount[deltaStart]

    # Генерация изображения и дальнейшая отправка
    image = Image.new("RGB", (1280, 720), "black")
    draw = ImageDraw.Draw(image)
    draw.font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 72)
    draw.text(xy=(640, 240), text="Начало", fill="white", anchor="mm")
    if deltaStart <= 20 or deltaStart == 365:
        draw.font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 108)
    else:
        draw.font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 72)
    draw.text(xy=(640, 330), text=(("Последнего" if deltaStart == 365 else count)+" Дня"), fill="white", anchor="mm")
    draw.font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 60)
    if 363 <= deltaStart <= 365:
        if deltaStart == 363:
            text = "72 Часа"
        elif deltaStart == 364:
            text = "48 Часов"
        else:
            text = "24 Часа"
        draw.text(xy=(640, 480), text=(f"-{text} Осталось-"), fill="white", anchor="mm")
    else:
        draw.text(xy=(640, 480), text=f"-{deltaFinish} {plurDay} {plurLeft}-", fill="white", anchor="mm")

    image.save(fp=("img/coming.png"))

    await bot.send_photo(chat_id=channel, photo=open("img/coming.png", "rb"), caption=(f'До дембеля {plurLeft.lower()} {deltaFinish} {plurDay.lower()} (пройдено {round(deltaStart/365*100,2)}%)'))

# Создание расписания (можно установить своё время)
scheduler = AsyncIOScheduler()
scheduler.add_job(
    countdown,
    trigger='cron',
    hour='00',
    minute='00',
    second='00'
)

# Запуск бота. Можно убить на CTRL + C, но кто я такой, чтобы вас учить?
if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()