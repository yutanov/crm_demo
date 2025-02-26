from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.db import connection
from datetime import datetime, timedelta
import random


from crm.models import Department, Employee

# example names
MALE_NAMES = ["Иван", "Алексей", "Олег", "Дмитрий", "Максим"]
FEMALE_NAMES = ["Мария", "Ольга", "Екатерина", "Анастасия", "Светлана"]

MALE_LAST_NAMES = ["Смирнов", "Иванов", "Кузнецов", "Петров", "Сидоров"]
FEMALE_LAST_NAMES = ["Смирнова", "Иванова", "Кузнецова", "Петрова", "Сидорова"]

MALE_PATRONYMICS = ["Алексеевич", "Дмитриевич", "Максимович", "Игоревич"]
FEMALE_PATRONYMICS = ["Сергеевна", "Владимировна", "Игоревна", "Петровна"]


# example departments
DEPARTMENT_NAMES = [
    "Финансовый отдел",
    "Отдел продаж",
    "ИТ-отдел",
    "Юридический отдел",
    "Отдел маркетинга",
]

# example postitions
POSITIONS = [
    "Менеджер",
    "Инженер",
    "Аналитик",
    "Разработчик",
    "Директор",
    "Бухгалтер",
    "HR-специалист",
]


# random date from 2010 to 2024
def random_date():
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2024, 1, 1)
    random_days = random.randint(0, (end_date - start_date).days)
    return make_aware(start_date + timedelta(days=random_days))


# creating 25 departments and 50 000 employees if tables are empty
def create_departments_and_employees():
    if Department.objects.exists() or Employee.objects.exists():
        return

    departments = []

    for level in range(5):
        parent_departments = departments[-5:] if level > 0 else [None]
        for i in range(5):
            department = Department.objects.create(
                name=f"{DEPARTMENT_NAMES[i]} (Уровень {level + 1})",
                parent=random.choice(parent_departments),
            )
            departments.append(department)
    print("Сгенерированы подразделения компании.")

    employees = []
    for _ in range(50_000):
        is_male = random.choice([True, False])

        if is_male:
            first_name = random.choice(MALE_NAMES)
            patronymic = random.choice(MALE_PATRONYMICS)
            last_name = random.choice(MALE_LAST_NAMES)
        else:
            first_name = random.choice(FEMALE_NAMES)
            patronymic = random.choice(FEMALE_PATRONYMICS)
            last_name = random.choice(FEMALE_LAST_NAMES)

        fio = f"{last_name} {first_name} {patronymic}"

        employees.append(
            Employee(
                fio=fio,
                position=random.choice(POSITIONS),
                employment_date=random_date(),
                salary=round(random.uniform(50_000, 300_000), 2),
                department=random.choice(departments),
            )
        )

    Employee.objects.bulk_create(employees)
    print("Сгенерированы сотрудники компании.")


class Command(BaseCommand):
    help = "Автоматически применяет миграции и заполняет базу при первом запуске"

    def handle(self, *args, **kwargs):
        tables = connection.introspection.table_names()
        if "crm_department" not in tables or "crm_employee" not in tables:
            print("Таблицы не найдены. Применяем миграции...")
            self.stdout.write(self.style.SUCCESS("Применяем миграции..."))
            self.call_command("migrate")

        create_departments_and_employees()
