from django.contrib import admin

from crm.models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["fio", "position", "employment_date", "salary", "department"]
    search_fields = ["fio", "position", "employment_date", "department"]
    list_filter = ["position", "department"]
