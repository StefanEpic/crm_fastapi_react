import React from 'react';
import Button from './UI/buttons/Button';

const TaskCard = ({ task, columnTag }) => {
    const takePrio = ({task}) => {
        if (task.priority === 3) {return (<span class="badge badge-center bg-success">3</span>)}
        else if (task.priority === 2) {return (<span class="badge badge-center bg-warning">2</span>)}
        else {return (<span class="badge badge-center bg-danger">1</span>)}
    }

    return (
        <div class="card accordion-item">
            <h2 class="accordion-header text-body d-flex justify-content-between" id={'heading ${ task.id }'}>
                <button type="button" class="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target={'#accordion ${ task.id }'} aria-expanded="false" aria-controls={'accordion ${ task.id }'}>
                    <div class="demo-inline-spacing">
                        {takePrio}
                        {task.name}
                    </div>
                </button>
            </h2>
            <div id={'accordion ${ task.id }'} class="accordion-collapse collapse" data-bs-parent={"#${ columnTag }"}>
                <div class="accordion-body">
                    <p class="card-text">
                        {task.projects.map(project =>
                            <a class="text-muted" href="#">{project}</a>)}
                    </p>
                    <p class="card-text">
                        {task.about}
                    </p>
                    <p class="card-text">
                        <ul class="list-unstyled users-list m-0 avatar-group d-flex align-items-center">

                        </ul>
                    </p>
                    <div class="demo inline-spacing">
                        
                    </div>
                    <div class="demo-inline-spacing">
                        <Button
                            type="button"
                            class="btn btn-sm btn-primary"
                            onclick="document.location='http://127.0.0.1:8000/{{ task.pk }}/edit'"
                        >
                            Редактировать
                        </Button>
                        <Button
                            type="button"
                            class="btn btn-sm btn-primary"
                            onclick="document.location='http://127.0.0.1:8000/{{ task.pk }}/delete'"
                        >
                            Удалить
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TaskCard;