# Музыкальное хранилище
### REST API системы прослушивания и хранения музыкальных композиций.

## Установка и запуск:
1. Клонировать репозиторий:
   ```bash
   git clone 
   ```
2. Создать и заполнить файл`.env` по шаблону `/config/.env.template`. Файл`.env` дожен находится в одной директории с `settings.py`.
   
   Переменные для заполнения:
   ```
   DEBUG=on
   SQL_DEBUG=on
   SECRET_KEY=XXXXXX
   POSTGRES_ENGINE=django.db.backends.postgresql
   POSTGRES_DB=audio-library-db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   DJANGO_ALLOWED_HOSTS=*
   STATIC_ROOT=var/www/staticfiles
   ```
   
3. Установить витуальное окружение для проекта `venv` в директории проекта:
    ```bash
    python3 -m venv venv
    ```
4. Активировать виртуальное окружение:
   - для Linux: 
       ```bash
       source venv/bin/activate
       ```
   - для Windows:
       ```bash
       .\venv\Scripts\activate.ps1
       ```
5. Установить зависимости из `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
6. Выполнить миграции:
    ```bash
    python3 manage.py migrate
    ```
7. Запустить сервер:
    ```bash
    python3 manage.py runserver
    ```
8. Список эндпоинтов (документация swagger):
   ```angular2html
   http://127.0.0.1:8000/api/v1/swagger/ - документация к API
   ```
9. Запуск в контейнерах:
   ```bash
   docker-compose up --build
   docker exec -it sound_cloud_web bash
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

