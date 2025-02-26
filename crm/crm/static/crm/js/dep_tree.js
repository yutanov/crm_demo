let departmentData = [];
let loadedEmployees = {};

$(document).ready(function () {
  function loadDepartments() {
    console.log("Загрузка списка подразделений...");
    $.getJSON("/api/get_department_tree/", function (data) {
      departmentData = data;
      $("#department-tree").html(buildTree(data, 1));
      console.log("Подразделения загружены.");
    });
  }

  function buildTree(departments, level) {
    let html = "<ul>";
    departments.forEach(function (department) {
      const bgColor = getDepartmentBgColor(level);
      html += `
                <li>
                    <div class="department-node p-3 border rounded" data-id="${department.id}" data-level="${level}" style="background-color: ${bgColor};">
                        <strong>${department.name}</strong>
                    </div>
                    <div class="employee-list" id="employees-${department.id}">
                        <ul></ul>
                        <div class="loading-spinner text-center" id="spinner-${department.id}" style="display: none;">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Загрузка...</span>
                            </div>
                        </div>
                        <button class="load-more btn btn-sm text-white mt-2" data-id="${department.id}" style="background-color: #343a40; display: none;">
                            Загрузить еще
                        </button>
                    </div>
                </li>
            `;
      if (department.subdepartments.length > 0) {
        html += buildTree(department.subdepartments, level + 1);
      }
    });
    html += "</ul>";
    return html;
  }

  function getDepartmentBgColor(level) {
    const colors = ["#f8f9fa", "#e9ecef", "#dee2e6", "#ced4da", "#adb5bd"];
    return colors[Math.min(level - 1, colors.length - 1)];
  }

  function loadEmployees(departmentId, offset = 0) {
    if (!loadedEmployees[departmentId]) {
      loadedEmployees[departmentId] = { employees: [], allLoaded: false };
    }

    if (loadedEmployees[departmentId].allLoaded) {
      console.log(`Все сотрудники загружены для отдела ID ${departmentId}`);
      return;
    }

    console.log(
      `Запрос на загрузку сотрудников для отдела ID ${departmentId}, offset: ${offset}`
    );

    $(`#spinner-${departmentId}`).show();

    $.getJSON(
      `/api/get_employees/${departmentId}/?offset=${offset}`,
      function (data) {
        const employeeList = $(`#employees-${departmentId} ul`);
        const loadMoreBtn = $(`#employees-${departmentId} .load-more`);

        if (data.employees.length === 0) {
          console.log(`Больше нет сотрудников в отделе ID ${departmentId}`);
          loadedEmployees[departmentId].allLoaded = true;
          loadMoreBtn.hide();
        } else {
          loadedEmployees[departmentId].employees.push(...data.employees);
          data.employees.forEach((emp, index) => {
            const bgClass =
              (offset + index) % 2 === 0
                ? "bg-light"
                : "bg-secondary text-white";
            employeeList.append(
              `<li class="p-2 ${bgClass}">${emp.fio} - ${emp.position} (Зарплата: ${emp.salary} руб.)</li>`
            );
          });
          console.log(
            `Загружено ${data.employees.length} сотрудников для отдела ID ${departmentId}`
          );
        }

        if (!loadedEmployees[departmentId].allLoaded) {
          loadMoreBtn.show();
        } else {
          loadMoreBtn.hide();
        }

        $(`#spinner-${departmentId}`).hide();
      }
    );
  }

  $("#department-tree").on("click", ".department-node", function () {
    const departmentId = $(this).data("id");
    const employeeList = $(`#employees-${departmentId}`);

    if (!employeeList.is(":visible")) {
      console.log(`Разворачиваем отдел ID ${departmentId}`);
      employeeList.slideDown();
      loadEmployees(departmentId, 0);
    } else {
      console.log(`Сворачиваем отдел ID ${departmentId}`);
      employeeList.slideUp();
    }
  });

  $("#department-tree").on("click", ".load-more", function () {
    const departmentId = $(this).data("id");
    console.log(`Кнопка "Загрузить еще" нажата в отделе ID ${departmentId}`);
    loadEmployees(departmentId, loadedEmployees[departmentId].employees.length);
  });

  loadDepartments();
});
