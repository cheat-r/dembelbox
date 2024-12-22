# Дембельбокс
Телеграм-бот, ведущий ежедневный обратный отсчёт в канале. Скрипт генерирует изображения и выкладывает их в канал, пока обратный отсчёт не закончится.

Также есть команда `/howmuch`, дублирующая данные об обратном отсчёте, которую можно использовать в ЛС бота или в чате, если он туда добавлен.
## Установка и использование
Для запуска скрипта требуются:
- Python 3.8 и выше (может можно и ниже но я не проверял)
- Токен бота (можно взять у [BotFather](https://t.me/botfather))
- Шрифты (по желанию, для удобства в репозиторий вложен Roboto (лицензия Apache 2.0, можете почитать если не пофиг)
- Установленные зависимости из `requirements.txt` (удобнее всего через venv, но тут как хотите)

Вставляем токен в `token.txt`, заходим в `main.py` и меняем некоторые строки (если требуется), запускаем, радуемся жизни! Бот завершит работу по окончании отведённого срока либо по вашей команде в консоли. Сами знаете какой.
## Костыли
После каждого запуска скрипта необходимо выполнять команду `/start` в личке бота, дабы он запустил расписание.

В `deltaFinish` прибавлен один день специально, так как без него он отстаёт, как бы то странно ни звучало.
