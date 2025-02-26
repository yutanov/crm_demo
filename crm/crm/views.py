from django.shortcuts import render
from django.http import JsonResponse

from crm.models import Department, Employee


def department_tree_view(request):
    return render(request, "index.html")


def get_department_tree(request):

    departments = Department.objects.all()
    department_dict = {}

    for department in departments:
        department_dict[department.id] = {
            "id": department.id,
            "name": department.name,
            "parent_id": department.parent.id if department.parent else None,
            "subdepartments": [],
            "employees": [],
        }

    root_departments = []
    for department in department_dict.values():
        if department["parent_id"]:
            department_dict[department["parent_id"]]["subdepartments"].append(
                department
            )
        else:
            root_departments.append(department)

    employees = Employee.objects.all().values(
        "fio", "position", "salary", "employment_date", "department_id"
    )
    for emp in employees:
        if emp["department_id"] in department_dict:
            department_dict[emp["department_id"]]["employees"].append(
                {
                    "fio": emp["fio"],
                    "position": emp["position"],
                    "salary": float(emp["salary"]),
                    "employment_date": emp["employment_date"].strftime("%Y-%m-%d"),
                }
            )

    return JsonResponse(root_departments, safe=False)


def get_employees(request, department_id):
    offset = int(request.GET.get("offset", 0))
    employees = Employee.objects.filter(department_id=department_id).order_by("fio")[
        offset : offset + 100
    ]

    return JsonResponse(
        {
            "employees": [
                {"fio": e.fio, "position": e.position, "salary": str(e.salary)}
                for e in employees
            ]
        }
    )
