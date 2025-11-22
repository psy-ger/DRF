# API бібліотеки (Django REST Framework)

Коротко
-----

Це просте REST API для керування бібліотекою книг. Реалізовано CRUD-операції, фільтрацію, пошук по назві, пагінацію (10 елементів на сторінку), аутентифікацію через токени і автоматичну документацію.

Основні ендпоінти
-----

- `POST /api/books/` — створити книгу (потрібна автентифікація).
- `GET /api/books/` — отримати список книг (потрібна автентифікація). Підтримує фільтрацію: `?author=`, `?genre=`, `?publication_year=` та пошук по частині назви: `?search=`.
- `GET /api/books/{id}/` — отримати деталі книги.
- `PUT/PATCH /api/books/{id}/` — оновити книгу (потрібна автентифікація).
- `DELETE /api/books/{id}/` — видалити книгу (тільки для адміністраторів / користувачів з `is_staff`).
- `GET /docs/` — документація (ReDoc). Також доступний Swagger UI на `/docs/swagger/`.

Вимоги
-----

Залежності перераховані в `requirements.txt`. Основні пакети:

- `Django`
- `djangorestframework`
- `django-filter`
- `drf-yasg` (Swagger / ReDoc)
- `djangorestframework-simplejwt` (опціонально для JWT)

Встановлення та запуск (macOS / zsh)
-----

1. Створіть віртуальне оточення та встановіть залежності:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Застосуйте міграції та створіть суперкористувача:

```bash
python manage.py migrate
python manage.py createsuperuser
```

3. Запустіть сервер розробки:

```bash
python manage.py runserver
```

4. Документація буде доступна за адресою: `http://127.0.0.1:8000/docs/`.

Авторизація та токени
-----

Проєкт використовує `TokenAuthentication` (DRF token). Після створення користувачів можна створити токен через Django admin або в shell:

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from rest_framework.authtoken.models import Token
>>> u = User.objects.create_user('user','user@example.com','pass')
>>> Token.objects.create(user=u)
>>> exit()
```

Використання токена в запитах (приклад curl):

```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/books/
```

Приклади запитів
-----

- Створити книгу:

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <token>" \
  -d '{"title":"Нова книга","author":"Автор","genre":"Fiction","publication_year":2024}' \
  http://127.0.0.1:8000/api/books/
```

- Отримати список, відфільтрований за автором:

```bash
curl -H "Authorization: Token <token>" "http://127.0.0.1:8000/api/books/?author=William"
```

- Пошук по частині назви:

```bash
curl -H "Authorization: Token <token>" "http://127.0.0.1:8000/api/books/?search=Python"
```

- Оновлення книги (PATCH):

```bash
curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Token <token>" \
  -d '{"title":"Оновлена назва"}' \
  http://127.0.0.1:8000/api/books/1/
```

- Видалення (тільки адміністратор):

```bash
curl -X DELETE -H "Authorization: Token <admin_token>" http://127.0.0.1:8000/api/books/1/
```

Пагінація
-----

Список книг повертається сторінками по 10 елементів. У відповіді поле `results` містить елементи поточної сторінки, також присутні посилання `next` і `previous`, якщо вони доступні.

Тести
-----

Запустити тести:

```bash
python manage.py test
```

У проєкт додані базові тести в `library/tests.py`, які покривають створення, отримання/фільтрацію, пошук, оновлення та видалення (перевірка, що видаляти може лише адміністратор).

Далі
-----

- За бажанням можна переключитися на JWT-автентифікацію (`djangorestframework-simplejwt`) — повідомте, і я допоможу замінити.
- Можу додати Postman-колекцію або приклади на Python (`requests`) для зручності.

Файли
-----

- Основна логіка знаходиться у застосунку `library` (`models.py`, `serializers.py`, `views.py`, `urls.py`).
- Документація доступна за шляхом `/docs/`.

Якщо потрібно, можу додатково покращити README або додати приклади запитів у Postman.

