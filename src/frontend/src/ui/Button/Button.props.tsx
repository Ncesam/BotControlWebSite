import React, {MouseEventHandler} from "react";

export interface ButtonProps {
    onClick?: MouseEventHandler<HTMLButtonElement>;
    type: ButtonType;
    children?: React.ReactNode;
}

enum ButtonType {
    Login = "rounded-md bg-blue-800 text-white font-bold text-sm lg:text-lg px-5 py-2 transition-all duration-300 ease-in-out hover:scale-105 active:scale-95",
    Logout = "text-white font-bold m-4 transition-all duration-300 ease-in-out hover:scale-105 active:scale-95",
    Submit = "rounded-md bg-blue-700 text-white font-bold px-2 lg:px-5 py-1 lg:py-2 transition-all duration-300 ease-in-out hover:scale-105",
    Back = "rounded-xl border-2 border-blue-500 px-3 py-1 transition-all duration-300 ease-in-out hover:scale-105 active:scale-95",
    Delete = "rounded-3xl bg-red-700 text-white font-bold p-2 m-4 transition-all duration-300 ease-in-out hover:scale-105 active:scale-95",
}

export {ButtonType};