from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Подразделение")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subdepartments",
        verbose_name="Начальное подразделение",
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Должность")
    employment_date = models.DateField(verbose_name="Дата приема на работу")
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Заработная плата"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Подразделение",
    )

    def __str__(self):
        return f"{self.fio} - {self.position}"
