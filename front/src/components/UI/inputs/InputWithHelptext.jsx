import React, { useId } from 'react';

const InputWithHelptext = ({ title, helptext, ...props }) => {
    const inputId = useId();
    const helpId = useId();
    return (
        <div>
            <label for={inputId} className="form-label">{title}</label>
            <input id={inputId} aria-describedby={helpId} {...props}/>
            <div id={helpId} className="form-text">
                {helptext}
            </div>
        </div>
    );
};
export default InputWithHelptext;