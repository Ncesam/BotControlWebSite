import {Dispatch, SetStateAction} from "react";

export interface TextAreaProps {
    placeholder?: string;
    value: string;
    setValue: Dispatch<SetStateAction<string>>;
    type?: TextAreaType;
}

export enum TextAreaType {
    bordered = "w-full h-32 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-12 h-auto overflow-y-hidden"
}