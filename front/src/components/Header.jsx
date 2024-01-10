import React from 'react';
import Button from './UI/buttons/Button';
import DropdownPrimary from './UI/buttons/DropdownButton';

const Header = ({ pageTitle, projects, departments, employees }) => {
    return (
        <div className="container-xxl flex-grow-1 container-p-y">
            <h4 className="fw-bold"><span className="text-muted fw-light"><a className="text-muted fw-light" href="/">Главная</a></span>{pageTitle ? ' / ' + {pageTitle} : ''}</h4>

            <div className="container-fluid d-flex flex-md-row flex-column justify-content-between align-items-md-center gap-1 container-p-x mb-4">
                <div className="demo-inline-spacing">
                    <Button
                        type="button"
                        className="btn btn-primary"
                        onclick="document.location='{% url 'task_create' %}'"
                    >
                        Создать задачу
                    </Button>
                </div>
                <div className="demo-inline-spacing">
                    <Button
                        type="button"
                        className="btn btn-primary"
                        onclick="document.location='{% url 'task_create' %}'"
                    >
                        Мои задачи
                    </Button>
                    <DropdownPrimary
                        type="button"
                        className="btn btn-primary dropdown-toggle me-2"
                        data-bs-toggle="dropdown"
                        aria-expanded="false"
                        title='Проекты'
                        options={projects}
                    />
                    <DropdownPrimary
                        type="button"
                        className="btn btn-primary dropdown-toggle me-2"
                        data-bs-toggle="dropdown"
                        aria-expanded="false"
                        title='Отделы'
                        options={departments}
                    />
                    <DropdownPrimary
                        type="button"
                        className="btn btn-primary dropdown-toggle me-2"
                        data-bs-toggle="dropdown"
                        aria-expanded="false"
                        title='Сотрудники'
                        options={employees}
                    />
                </div>
            </div>
        </div>
    );
};

export default Header;