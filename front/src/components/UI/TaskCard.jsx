import React from 'react';
import DropdownPrimary from './buttons/DropdownButton';

const TaskCard = () => {
    return (
        <div class="card accordion-item">
            <h2 class="accordion-header text-body d-flex justify-content-between" id="heading{{ task.pk }}">
                <button type="button" class="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target="#accordion{{ task.pk }}" aria-expanded="false" aria-controls="accordion{{ task.pk }}">
                    <div class="demo-inline-spacing">
                        {% if task.priority == 3 %}
                        <span class="badge badge-center bg-success">3</span>
                        {% elif task.priority == 2 %}
                        <span class="badge badge-center bg-warning">2</span>
                        {% elif task.priority == 1 %}
                        <span class="badge badge-center bg-danger">1</span>
                        {% endif %}
                        {{ task.name }}
                    </div>
                </button>
            </h2>
            <div id="accordion{{ task.pk }}" class="accordion-collapse collapse" data-bs-parent="#{{ column.tag }}" style="">
                <div class="accordion-body">
                    <p class="card-text">
                        {% for project in task.project.all %}
                        <a class="text-muted" href="{% url 'kanban_project_page' project.id %}">{{ project }}</a>&nbsp&nbsp&nbsp&nbsp
                        {% endfor %}
                    </p>
                    <p class="card-text">
                        {{ task.about | truncatewords:20 }}
                    </p>
                    <p class="card-text">
                        <ul class="list-unstyled users-list m-0 avatar-group d-flex align-items-center">
                            {% for employee in task.employee.all %}
                            <li data-bs-toggle="tooltip" data-popup="tooltip-custom" data-bs-placement="top" class="avatar avatar-xs pull-up" title="" data-bs-original-title="{{ employee }}">
                                <a href="{% url 'kanban_employee_page' employee.id %}">
                                    {% if employee.photo %}
                                    <img src="{{ MEDIA_DIR }}{{ employee.photo.url }}" alt="Avatar" class="rounded-circle">
                                        {% else %}
                                        <img src="/media/photos_of_employees/default.png" alt="Avatar" class="rounded-circle">
                                            {% endif %}
                                        </a>
                                    </li>
                                    {% endfor %}
                                </ul>
                            </p>
                            {% if task.author_id == user_pk or is_manager %}
                            <div class="demo inline-spacing">
                                <DropdownPrimary
                                
                                />
                            </div>
                            <div class="demo-inline-spacing">
                                <button type="button" class="btn btn-sm btn-primary" onclick="document.location='http://127.0.0.1:8000/{{ task.pk }}/edit'">Редактировать</button>
                                <button type="button" class="btn btn-sm btn-primary" onclick="document.location='http://127.0.0.1:8000/{{ task.pk }}/delete'">Удалить</button>
                            </div>
                            );
};

                            export default TaskCard;