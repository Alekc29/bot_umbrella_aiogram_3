![workflow status](https://github.com/Alekc29/bot_umbrella_aiogram_3/actions/workflows/main.yml/badge.svg)

# bot_umbrella_aiogram_3
## Погодный помощник

#### Телеграмм-бот умеет:
- хранить ваш профиль с информацией о вашем городе;
- показывать прогноз погоды на 1-5 дней;
- напоминать взять зонтик в указанное время, если днём будет дождь;
- анализировать погоду за указанное количество дней и давать рекомендацию, стоит ли мыть машину. 

#### Администратор может:
- получить статистику по количеству пользователей;
- отправлять сообщение всем пользователям через бота.

#### Запуск бота на локальной машине
- клонируйте удалённый репозиторий
``` bash
git clone git@github.com:Alekc29/bot_umbrella_aiogram_3.git
```
- В директории /bot_umbrella_aiogram_3 создайте файл .env, с переменными окружения, используя образец [.env.example](.env.example).
- Создайте виртуальное окружение и установите зависимости
```bash
python -m venv venv
. venv/Scripts/activate (windows)
. venv/bin/activate (linux)
pip install --upgade pip
pip install -r -requirements.txt
```
- Запустите бота
```bash
python3 main.py
```

#### Запуск бота в контейнере

- клонируйте удалённый репозиторий
``` bash
git clone git@github.com:Alekc29/bot_umbrella_aiogram_3.git
```
- В директории /bot_umbrella_aiogram_3 создайте файл .env, с переменными окружения, используя образец [.env.example](.env.example).
- Сборка и развертывание контейнера
```bash
docker-compose up -d --build
```

Телеграмм-бот доступен по адресу: [@reminder_umbrella_bot](https://t.me/reminder_umbrella_bot)
<div style='text-align: center;'>
<img src="image.png" width="200" height="200">
</div>