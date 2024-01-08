import React, { useId } from 'react';

// multiple for multiple select
const SelectWithHelptext = ({ title, helptext, options, ...props }) => {
    const selectId = useId();
    const helpId = useId();
    return (
        <div>
            <label for={selectId} className="form-label">{title}</label>
            <select
                id={selectId}
                aria-describedby={helpId}
                {...props}
            >
                {options.map(option =>
                    <option value={option.value} key={option.value}>{option.title}</option>)}
            </select>
            <div id={helpId} className="form-text">
                {helptext}
            </div>
        </div>
    );
};

export default SelectWithHelptext;