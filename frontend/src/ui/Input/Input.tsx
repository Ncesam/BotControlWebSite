import React from "react";
import type {FC} from "react";
import {InputProps} from "./Input.props";

const Input: FC<InputProps> = ({type, placeholder, onChange, value}) => {
    return (
        <input placeholder={placeholder || ""} type={type || "text"} value={value} onChange={onChange}
               className={"bg-gray-600 rounded-lg w-3/4 lg:w-full placeholder:text-gray-300 placeholder:opacity-55 p-2 focus:outline-blue-500 text-gray-300"}/>
    );
};

export default Input;

