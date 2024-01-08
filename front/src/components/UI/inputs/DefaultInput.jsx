import React, { useId } from 'react';

const DefaultInput = ({ title, helptext, ...props }) => {
    const inputId = useId();
    return (
        <div>
            <label for={inputId} className="form-label">{title}</label>
            <input id={inputId} {...props}/>
        </div>
    );
};
export default DefaultInput;