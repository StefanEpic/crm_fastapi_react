import React from 'react';

const DropdownPrimary = ({ title, options, ...props }) => {
    return (
        <div>
            <button type="button" {...props}>{title}</button>
            <ul class="dropdown-menu">
                {options.map(option =>
                    <li><a class='dropdown-item' href={option.href}>{option.title}</a></li>)}
            </ul>
        </div>
    );
};

export default DropdownPrimary;