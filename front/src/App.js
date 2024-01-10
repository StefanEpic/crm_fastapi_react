import React, { useState, useEffect } from 'react';
// import './styles/vendor/fonts/boxicons.css';
import './styles/vendor/css/core.css';
import './styles/vendor/css/theme-default.css';
import './styles/css/demo.css';
import './styles/vendor/libs/perfect-scrollbar/perfect-scrollbar.css';
import './styles/vendor/js/helpers.js';
import './styles/js/config.js';
import CreateTaskForm from './forms/CreateTaskForm.jsx';
import { BaseAPI } from './js/BaseAPI.js';

function App() {
  const [objects, setObjects] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [status, setStatus] = useState([
    { value: 'todo', title: "Запланировано" },
    { value: 'doing', title: "В работе" },
    { value: 'done', title: "На проверке" },
    { value: 'release', title: "Завершено" },
  ]);
  const [priority, setPriority] = useState([
    { value: 'height', title: "Высокий приоритет" },
    { value: 'normal', title: "Средний приоритет" },
    { value: 'low', title: "Низкий приоритет" },
    { value: 'none', title: "Приоритет не указан" },
  ]);
  const [date, setDate] = useState('');

  return (
    <div className="App">
      <div class="layout-wrapper layout-content-navbar">
        <div class="layout-container">
          <div class="layout-page">

            <CreateTaskForm
              title='Создать задачу'
              buttonTitle='Создать'
              selectObjects={objects}
              selectEmployees={employees}
              selectStatus={status}
              selectPriority={priority}
              selectDate={date}
            />

          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
