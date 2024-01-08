import React, { useId } from 'react';

const DefaultTextArea = ({ title, helptext, ...props }) => {
    const textAreaId = useId();
    const helpId = useId();
    return (
        <div>
            <label for={textAreaId} className="form-label">{title}</label>
            <textarea id={textAreaId} aria-describedby={helpId} {...props}></textarea>
            <div id={helpId} className="form-text">
                {helptext}
            </div>
        </div>
    );
};

export default DefaultTextArea;