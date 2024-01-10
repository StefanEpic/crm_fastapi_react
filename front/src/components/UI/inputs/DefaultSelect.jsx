import React, { useId } from 'react';

const DefaultSelect = ({ title, options, ...props }) => {
    const selectId = useId();
    return (
        <div>
            <label for={selectId} className="form-label">{title}</label>
            <select
                id={selectId}
                {...props}
            >
                {options.map(option =>
                    <option value={option.value} key={option.value}>{option.title}</option>)}
            </select>
        </div>
    );
};

export default DefaultSelect;