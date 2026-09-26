# htmlpresent

Платформа для хранения и просмотра онлайн-презентаций с панелью администрирования через Telegram-бот.

Веб-часть написана на **FastAPI** (async) и отдаёт HTML/PDF-презентации, а **Telegram-бот** на `aiogram` отвечает за загрузку файлов превью и документов от админов в хранилище проекта. Данные хранятся в **PostgreSQL** с использованием **SQLAlchemy 2.0** (async ORM) и управляются миграциями через **Alembic**.

## Функционал

- Публикация и просмотр презентаций через веб-интерфейс (HTML и PDF).
- Загрузка превью-изображений и файлов презентаций через Telegram-бота.
- Административная модель с двумя уровнями доступа (`admin`, `high_admin`).
- Ограничение на количество загрузок одного пользователя.
- Возможность скрытия презентации из общего списка (`hidden`).
- REST API для получения списка презентаций.

## Стек

| Назначение | Технология |
| --- | --- |
| Веб-фреймворк | FastAPI + uvicorn |
| ORM | SQLAlchemy 2.0 (async) |
| Драйвер PostgreSQL | asyncpg |
| Миграции | Alembic |
| Шаблоны | Jinja2 |
| Telegram-бот | aiogram 3.x |
| Конфигурация окружения | python-dotenv |

## Структура проекта

```
.
├── main.py                 # точка входа, инициализация приложения (lifespan)
├── path_config.py          # пути к директориям файлов + авто-создание при старте
├── env_loading.py          # загрузка .env
├── templates_config.py     # конфигурация Jinja2 шаблонов
├── utils.py                # утилиты (формирование списка презентаций)
├── Routers/
│   └── presentations.py    # роуты: список, просмотр презентации
├── Database/
│   ├── database.py         # движок БД, сессии, классы-репозитории
│   ├── db_setting.py       # сбор DB_URL из переменных окружения
│   └── models.py           # модели Presentation и Admin
├── AdminPanel/
│   ├── bot.py              # запуск бота
│   ├── bot_config.py       # конфигурация бота, функции скачивания файлов
│   └── fsm*               # машина состояний (загрузка файлов)
├── presentation_asset/
│   └── preview_img/        # превью-изображения презентаций
├── templates/
│   ├── main_page.html      # главная страница
│   └── presentations/      # шаблоны просмотра презентаций
├── static/                 # CSS / JS
└── alembic/                # миграции БД
```

## Установка и запуск

1. Установить зависимости (рекомендуется Poetry):

```bash
poetry install
```

2. Создать файл `.env` на основе переменных окружения:

```dotenv
# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=presentations

# Telegram бот (токен из @BotFather)
TOKEN=<your_bot_token>
```

3. Применить миграции БД:

```bash
alembic upgrade head
```

4. Запустить приложение:

```bash
python main.py
# или через uvicorn
uvicorn main:app --reload
```

Веб-интерфейс доступен по адресу `http://localhost:8000`.

## Переменные окружения

| Переменная | Описание |
| --- | --- |
| `DB_HOST` | Хост PostgreSQL |
| `DB_PORT` | Порт PostgreSQL |
| `DB_USER` | Пользователь БД |
| `DB_PASSWORD` | Пароль БД |
| `DB_NAME` | Имя базы данных |
| `TOKEN` | Токен Telegram-бота |

## API

| Метод | Маршрут | Описание |
| --- | --- | --- |
| GET | `/` | Главная страница |
| GET | `/presentation` | Список презентаций (HTML) |
| GET | `/presentations` | Список презентаций (JSON) |
| GET | `/presentation/{id}` | Просмотр презентации (HTML/PDF) |

## Лицензия

Internal use.
