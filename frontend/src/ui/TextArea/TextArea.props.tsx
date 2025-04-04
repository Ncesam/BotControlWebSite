import {Dispatch, SetStateAction} from "react";

export interface TextAreaProps {
    placeholder?: string;
    value: string;
    setValue: Dispatch<SetStateAction<string>>;
    type?: TextAreaType;
}

export enum TextAreaType {
    bordered = "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-12 h-auto overflow-y-hidden",
    ads = "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-64 h-auto resize-none overflow-y-hidden",
}