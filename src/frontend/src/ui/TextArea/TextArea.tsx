import React from "react";
import type {FC} from "react";
import {TextAreaProps} from "./TextArea.props";

const TextArea: FC<TextAreaProps> = ({type, placeholder, value, setValue}) => {
    return (
            <div>
                <textarea className={type} value={value} placeholder={placeholder} onChange={(e) => setValue(e.target.value)}></textarea>
            </div>
    );
};

export default TextArea;

