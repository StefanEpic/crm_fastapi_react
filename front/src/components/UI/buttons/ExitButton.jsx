import React from 'react';

const ExitButton = ({ title, ...props }) => {
    return (
        <a {...props}><i class="bx bx-log-out-circle"></i>{title}</a>
    );
};

export default ExitButton;