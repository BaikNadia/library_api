# Library Management System API

Django REST Framework API для управления библиотечной системой с JWT аутентификацией, ролевой системой и полным CRUD функционалом.

## 🚀 Функциональность

### 📚 Управление книгами
- Полный CRUD для книг
- Поиск по названию, ISBN, автору
- Фильтрация по жанру, автору
- Учет количества экземпляров

### 👥 Пользователи и роли
- **Читатели** - просмотр книг, управление своими займами
- **Библиотекари** - полное управление книгами, авторами, займами
- **Администраторы** - полный доступ ко всем функциям


# 📚 Library Management System API

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/Django%20REST%20Framework-3.15%2B-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-Auth-orange?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2B-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-25%2B-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![Swagger](https://img.shields.io/badge/Swagger-UI-green?logo=swagger&logoColor=white)](https://swagger.io/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub Stars](https://img.shields.io/github/stars/BaikNadia/library-management-api?style=social)](https://github.com/BaikNadia/library-management-api)

**RESTful API для управления библиотечной системой**  
Реализовано на Django REST Framework с JWT аутентификацией, ролевой системой и полным CRUD функционалом для книг, авторов, читателей и займов.


**👩‍💻 Автор:** [BaikNadia](https://github.com/BaikNadia)  
**📦 Репозиторий:** [Library Management System API](https://github.com/BaikNadia/library-management-api)  
**📜 Лицензия:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)


## 🚀 Функциональность

### 📚 Управление книгами
- Полный CRUD для книг
- Поиск по названию, ISBN, автору
- Фильтрация по жанру, автору
- Учет количества экземпляров

### 👥 Пользователи и роли
- **Читатели** - просмотр книг, управление своими займами
- **Библиотекари** - полное управление книгами, авторами, займами
- **Администраторы** - полный доступ ко всем функциям


### 🔐 Аутентификация и авторизация
- JWT токены для безопасной аутентификации
- Ролевая система доступа
- Защищенные эндпоинты

### 📖 Система займов книг
- Создание займов книг
- Автоматический расчет просрочек
- Возврат книг
- История займов

## 🛠 Технологии

- **Backend**: Django 4.2, Django REST Framework
- **База данных**: PostgreSQL
- **Аутентификация**: JWT (Simple JWT)
- **Документация**: Swagger/OpenAPI
- **CORS**: django-cors-headers
- **Фильтрация**: django-filter

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/BaikNadia/library_api.git
cd library_api

### 2. Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# ИЛИ
.venv\Scripts\activate     # Windows

### 3. Установка зависимостей
pip install -r requirements.txt

### 4. Настройка окружения
Создайте файл .env в корневой директории:
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=library_api
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

### 5. Настройка базы данных
Убедитесь, что PostgreSQL запущен, и создайте базу данных:
CREATE DATABASE library_api;

### 6. Миграции
python manage.py makemigrations
python manage.py migrate

### 7. Создание суперпользователя (опционально)
python manage.py createsuperuser

### 8. Запуск сервера
python manage.py runserver
Приложение будет доступно по адресу: http://127.0.0.1:8000

📖 Документация API
После запуска сервера документация доступна по адресам:

Swagger UI: http://127.0.0.1:8000/swagger/

ReDoc: http://127.0.0.1:8000/redoc/

🔌 API Эндпоинты
Аутентификация
POST /api/auth/register/ - Регистрация нового пользователя

POST /api/auth/login/ - Вход в систему (получение JWT токенов)

POST /api/auth/token/refresh/ - Обновление access токена

Пользователи
GET /api/users/profile/ - Профиль текущего пользователя

GET /api/users/ - Список пользователей (только для библиотекарей/админов)

Книги
GET /api/books/ - Список всех книг

POST /api/books/ - Создание новой книги (библиотекари/админы)

GET /api/books/{id}/ - Детальная информация о книге

PUT/PATCH /api/books/{id}/ - Обновление книги (библиотекари/админы)

DELETE /api/books/{id}/ - Удаление книги (админы)

Авторы
GET /api/authors/ - Список авторов

POST /api/authors/ - Создание автора (библиотекари/админы)

GET /api/authors/{id}/ - Детальная информация об авторе

PUT/PATCH /api/authors/{id}/ - Обновление автора (библиотекари/админы)

DELETE /api/authors/{id}/ - Удаление автора (админы)

Займы книг
GET /api/loans/ - Список займов (свои для читателей, все для библиотекарей)

POST /api/loans/ - Создание нового займа

GET /api/loans/{id}/ - Детальная информация о займе

PATCH /api/loans/{id}/ - Обновление займа (возврат книги)

DELETE /api/loans/{id}/ - Удаление займа (библиотекари/админы)

🔒 Модели данных
Пользователь (User)
username, email, first_name, last_name

user_type: reader/librarian/admin

phone, address

Автор (Author)
name, bio, birth_date, death_date

Книга (Book)
title, isbn, genre, publication_date

publisher, description

total_copies, available_copies

Связь many-to-many с авторами

Займ книги (BookLoan)
book (ForeignKey), user (ForeignKey)

borrowed_date, due_date, returned_date

status: borrowed/returned/overdue

Метод is_overdue() - автоматический расчет просрочки

🎯 Примеры использования
Регистрация пользователя:
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "user_type": "reader"
  }'

Вход в систему:
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'

Создание займа книги:
curl -X POST http://127.0.0.1:8000/api/loans/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "due_date": "2024-12-31"
  }'

Возврат книги:
curl -X PATCH http://127.0.0.1:8000/api/loans/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "returned"
  }'

📁 Структура проекта:
library_api/
├── core/                    # Основное приложение
│   ├── models.py           # Модели данных
│   ├── serializers.py      # Сериализаторы DRF
│   ├── views.py            # Представления
│   ├── permissions.py      # Кастомные permissions
│   └── admin.py            # Админ-панель
├── library/                # Настройки проекта
│   ├── settings.py         # Настройки Django
│   ├── urls.py             # Маршруты
│   └── wsgi.py             # WSGI конфигурация
├── static/                 # Статические файлы
├── .env.example            # Пример переменных окружения
├── requirements.txt        # Зависимости
└── manage.py              # Управление Django

👥 Роли и разрешения:
Читатель (Reader)
Просмотр книг и авторов

Создание займов книг

Просмотр и управление своими займами

Обновление профиля

Библиотекарь (Librarian)
Все права читателя

Создание, редактирование книг и авторов

Просмотр всех займов

Управление займами любого пользователя

Администратор (Admin)
Все права библиотекаря

Удаление книг, авторов, займов

Управление пользователями

Полный доступ ко всем функциям

🐛 Troubleshooting
Проблемы с базой данных
Убедитесь, что PostgreSQL запущен

Проверьте правильность настроек в .env

Выполните python manage.py migrate

Проблемы с аутентификацией
Проверьте корректность JWT токена

Убедитесь, что токен не истек

Используйте /api/auth/token/refresh/ для обновления

Проблемы с правами доступа
Проверьте user_type пользователя

Убедитесь, что пользователь аутентифицирован

📄 Лицензия
Этот проект является учебным и предназначен для демонстрации возможностей Django REST Framework.

👨‍💻 Автор
BaikNadia

GitHub: @BaikNadia

⭐ Не забудьте поставить звезду репозиторию, если проект был полезен!
