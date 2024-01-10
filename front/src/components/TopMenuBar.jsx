import React from 'react';
import ExitButton from './UI/buttons/ExitButton';

const TopMenuBar = ({ username, avatar }) => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <div className="navbar-nav me-auto mb-2 mb-lg-0">
                        <div className="avatar">
                            {avatar}
                        </div>
                        <a href="#" className="nav-item nav-link">{username}</a>
                    </div>
                    <div>
                        <ExitButton
                            title='Выход'
                            href='#'
                            className='btn btn-sm btn-outline-danger'
                        />
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default TopMenuBar;