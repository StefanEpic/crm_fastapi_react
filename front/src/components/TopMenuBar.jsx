import React from 'react';
import ExitButton from './UI/buttons/ExitButton';

const TopMenuBar = ({ username, avatar }) => {
    return (
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <div class="navbar-nav me-auto mb-2 mb-lg-0">
                        <div class="avatar">
                            {avatar}
                        </div>
                        <a href="#" class="nav-item nav-link">{username}</a>
                    </div>
                    <div>
                        <ExitButton
                            title='Выход'
                            href='#'
                        />
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default TopMenuBar;