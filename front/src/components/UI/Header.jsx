import React from 'react';

const Header = () => {
    return (
        <div>
            <h4 class="fw-bold"><span class="text-muted fw-light"><a class="text-muted fw-light" href="/">Главная</a></span>{% if page_title %} / {{ page_title }}{% endif %}</h4>

            <div class="container-fluid d-flex flex-md-row flex-column justify-content-between align-items-md-center gap-1 container-p-x mb-4">
                <div class="demo-inline-spacing">
                    <button type="button" class="btn btn-primary" onclick="document.location='{% url 'task_create' %}'">Создать задачу</button>
                </div>
                <div class="demo-inline-spacing">
                    <button type="button" class="btn btn-primary" onclick="document.location='http://127.0.0.1:8000/my/{{ user.pk }}'">Мои задачи</button>
                    <button type="button" class="btn btn-primary dropdown-toggle me-2" data-bs-toggle="dropdown" aria-expanded="false">Проекты</button>
                    <ul class="dropdown-menu">
                        {% for project in projects %}
                        <li><a class="dropdown-item" href="{% url 'kanban_project_page' project.id %}">{{ project }}</a></li>
                        {% endfor %}
                    </ul>
                    <button type="button" class="btn btn-primary dropdown-toggle me-2" data-bs-toggle="dropdown" aria-expanded="false">Отделы</button>
                    <ul class="dropdown-menu">
                        {% for department in departments %}
                        <li><a class="dropdown-item" href="{% url 'kanban_department_page' department.id %}">{{ department }}</a></li>
                        {% endfor %}
                    </ul>
                    <button type="button" class="btn btn-primary dropdown-toggle me-2" data-bs-toggle="dropdown" aria-expanded="false">Сотрудники</button>
                    <ul class="dropdown-menu">
                        {% for employee in employees %}
                        <li><a class="dropdown-item" href="{% url 'kanban_employee_page' employee.id %}">{{ employee }}</a></li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Header;