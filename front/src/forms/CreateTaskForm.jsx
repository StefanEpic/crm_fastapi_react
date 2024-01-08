import React from 'react';
import DefaultInput from '../components/UI/inputs/DefaultInput';
import DefaultTextArea from '../components/UI/inputs/DefaultTextArea';
import SelectWithHelptext from '../components/UI/inputs/SelectWithHelptext';
import DefaultSelect from '../components/UI/inputs/DefaultSelect';
import ButtonPrimary from '../components/UI/buttons/Button';
import InputWithHelptext from '../components/UI/inputs/InputWithHelptext';

const CreateTaskForm = ({ title, buttonTitle, selectObjects, selectEmployees, selectStatus, selectPriority, selectDate }) => {
    return (
        <div class="row justify-content-md-center">
            <div class="col-xl-6">
                <div class="card mb-4">
                    <h5 class="card-header">{title}</h5>
                    <div class="card-body">
                        <form method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <InputWithHelptext
                                    title='Название'
                                    placeholder='Введите название задачи'
                                    helptext='Указывается сокращенное название задачи'
                                    typy='text'
                                    className='form-control'
                                />
                            </div>
                            <div class="mb-3">
                                <DefaultTextArea
                                    title='Описание'
                                    placeholder='Введите описание задачи'
                                    helptext='Указывается полное описание задачи'
                                    rows='3'
                                    className='form-control'
                                />
                            </div>
                            <div class="row g-2">
                                <div class="col mb-3">
                                    <SelectWithHelptext
                                        title='Объекты'
                                        helptext='Выберите объекты'
                                        multiple
                                        options={selectObjects}
                                        className='form-select'
                                    />
                                </div>
                                <div class="col mb-3">
                                    <SelectWithHelptext
                                        title='Сотрудники'
                                        helptext='Выберите сотрудников'
                                        multiple
                                        options={selectEmployees}
                                        className='form-select'
                                    />
                                </div>
                            </div>
                            <div class="row g-3">
                                <div class="col mb-3">
                                    <DefaultSelect
                                        title='Статус'
                                        options={selectStatus}
                                        className='form-select'
                                    />
                                </div>
                                <div class="col mb-3">
                                    <DefaultSelect
                                        title='Статус'
                                        options={selectPriority}
                                        className='form-select'
                                    />
                                </div>
                                <div class="col mb-3">
                                    <DefaultInput
                                        title='Срок'
                                        options={selectDate}
                                        type='datetime-local'
                                        className='form-control'
                                    />
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="d-grid gap-2 col-lg-4 mx-auto">
                                    <ButtonPrimary
                                        className='btn btn-primary btn-lg'
                                    >
                                        {buttonTitle}
                                    </ButtonPrimary>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CreateTaskForm;