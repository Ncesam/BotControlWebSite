import React, {FC} from "react";
import {ButtonProps, ButtonType} from "./Button.props";

const Button: FC<ButtonProps> = ({children, type, onClick}) => {
    return (
        <div>
            <button onClick={onClick} className={type}>{children}</button>
        </div>
    )
}

export default Button;
export {ButtonType};