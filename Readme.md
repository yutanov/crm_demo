# Проект: CRM для управления сотрудниками

## Описание проекта

Этот проект представляет собой CRM-систему для управления сотрудниками и подразделениями компании. Реализована древовидная структура отделов, с возможностью подгрузки сотрудников по 100 человек.

---

## Зависимости

Проект использует следующие зависимости:

```bash
Django==5.1.6
```

---

## Запуск через Docker Compose

1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/yutanov/crm_demo
   cd crm_demo
   ```

3. Соберите и запустите контейнеры:

   ```bash
   docker-compose up --build -d
   ```

4. Применение миграциий и инициализация базы данных (выполняется автоматически):

   ```bash
   docker-compose exec crm python manage.py migrate
   docker-compose exec crm python manage.py init_db
   ```

5. Создайте суперпользователя:

   ```bash
   docker-compose exec crm python manage.py createsuperuser
   ```

7. Проект доступен по адресу: `http://127.0.0.1:9000`  
Панель администратора Django: `http://127.0.0.1:9000/admin`

---

## Запуск вручную (локально)

1. Убедитесь, что у вас установлен Python 3.12 и виртуальное окружение.
2. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/yutanov/crm_demo
   cd crm_demo
   ```

3. Установите зависимости:

   ```bash
   pip install -r crm/requirements.txt
   ```

4. Выполните миграции базы данных (база данных SQLite создается автоматически):

   ```bash
   python crm/manage.py migrate
   ```

5. Загрузите начальные данные:

   ```bash
   python crm/manage.py init_db
   ```

6. Создайте суперпользователя:

   ```bash
   python crm/manage.py createsuperuser
   ```

7. Запустите сервер разработки:

   ```bash
   python crm/manage.py runserver
   ```

8. Проект доступен по адресу: `http://127.0.0.1:8000`  
Панель администратора Django: `http://127.0.0.1:8000/admin`
