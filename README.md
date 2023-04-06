# Приложение для Благотворительного фонда поддержки котиков QRKot



## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Getting Started <a name = "getting_started"></a>

Эти инструкции помогут вам запустить и запустить копию проекта на вашем локальном компьютере для целей разработки и тестирования.

Клонируем репозиторий:
```
git clone https://github.com/Eltimccc/cat_charity_fund.git
```

Переходим в дирректорию:
```
cd cat_charity_fund
```

Устанавливаем venv питона:
```
py -3.9 -m venv venv
```
Активируем его:
```
source venv/script/activate
```

Обновляем PIP:
```
python -m pip install --upgrade pip
```
Установка зависимостей:
```
pip install -r requirements.txt
```
Создаем дирректорию .env:
```
touch .env
```
Пример заполнения .env с указанием данных суперпользователя:
```
APP_TITLE=Сервис QRKot
DESCRIPTION=Благотворительный фонд поддержки котиков QRKot
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRETAPI
FIRST_SUPERUSER_EMAIL=root@root.ru
FIRST_SUPERUSER_PASSWORD=root
```
ЗАПУСК!
```
uvicorn app.main:app
```

## Usage

Если вы хотите использовать наше приложение с умом, то слушайте внимательно! Не забывайте, что QRKOT - это приложение для поддержки кошачьей популяции, а не для кормления своих соседских котов. Мы не несем ответственности за любые последствия, связанные с неправильным использованием нашего приложения! Так что, прежде чем начать пользоваться, убедитесь, что вы не пытаетесь покормить домашних питомцев своих соседей, потому что это может привести к конфликтам с соседями и даже к судебным разбирательствам! Давайте используем наше приложение с умом, чтобы сделать мир лучше для наших братьев меньших!
