import React, {useState} from 'react';
// import './styles/vendor/fonts/boxicons.css';
import './styles/vendor/css/core.css';
import './styles/vendor/css/theme-default.css';
import './styles/css/demo.css';
import './styles/vendor/libs/perfect-scrollbar/perfect-scrollbar.css';
import './styles/vendor/js/helpers.js';
import './styles/js/config.js';
import CreateTaskForm from './forms/CreateTaskForm.jsx';

function App() {
  const [selectObjects, setPosts] = useState([
    { value: 1, title: "JS hyita", key: 'Doggy language' },
    { value: 2, title: "Python the best", description: 'The language of the kings' },
    { value: 3, title: "SQL norm", description: 'Norm? Norm...' },
  ])


  return (
    <div className="App">
      <CreateTaskForm
      title='Создать задачу'
      buttonTitle='Создать'
      selectObjects={selectObjects}
      selectEmployees={selectObjects}
      selectStatus={selectObjects}
      selectPriority={selectObjects}
      selectDate={selectObjects}
      />

    </div>
  );
}

export default App;
