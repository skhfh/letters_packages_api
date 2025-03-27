# Letters & Packages API

### Описание

**Letters & Packages API** — API для управления письмами
и посылками. Позволяет создавать, редактировать, удалять и получать информацию
о почтовых отправлениях.

### Технологии

- Python 3.9
- Django 3.2
- Django REST Framework 3.12
- SQLite
- Pytest
---

### Установка и запуск

1. Клонирование репозитория, перейти в директорию backend

```bash
git clone git@github.com:skhfh/letters_packages_api.git
cd letters_packages_api/backend
```

2. Создание виртуального окружения и установка зависимостей

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

3. Применение миграций и наполнение БД данными Клиентов и Почтовых пунктов

```bash
python manage.py migrate
python manage.py fill_db
```

4. Создание суперпользователя (по желанию)

```bash
python manage.py createsuperuser
```

5. Запуск сервера

```bash
python manage.py runserver
```

API будет доступен по адресу: `http://127.0.0.1:8000/api/` \
API писем: `http://127.0.0.1:8000/api/letters/` \
API посылок: `http://127.0.0.1:8000/api/packages/`
___

### Тестирование

Для запуска тестов в запущенном ВО используйте:

```bash
pytest
```
---

### Эндпоинты API

1. Письма (`/api/letters/`)

| Метод  | URL                    | Описание                     |
|--------|------------------------|------------------------------|
| GET    | `/api/letters/`        | Получить список писем        |
| POST   | `/api/letters/`        | Создать письмо               |
| GET    | `/api/letters/{id}/`   | Получить информацию о письме |
| PATCH  | `/api/letters/{id}/`   | Частичное обновление         |
| PUT    | `/api/letters/{id}/`   | Полное обновление            |
| DELETE | `/api/letters/{id}/`   | Удалить письмо               |


2. Посылки (`/api/packages/`)

| Метод  | URL                   | Описание                      |
|--------|-----------------------|-------------------------------|
| GET    | `/api/packages/`      | Получить список посылок       |
| POST   | `/api/packages/`      | Создать посылку               |
| GET    | `/api/packages/{id}/` | Получить информацию о посылке |
| PATCH  | `/api/packages/{id}/` | Частичное обновление          |
| PUT    | `/api/packages/{id}/` | Полное обновление             |
| DELETE | `/api/packages/{id}/` | Удалить посылку               |


Более детальную информацию о запросах можно посмотреть 
в документации DRF к API (OPTIONS) по соответствующим эндпоинтам.

___
### Автор
[skhfh](https://github.com/skhfh) 
