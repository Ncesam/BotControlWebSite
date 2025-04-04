import {ChangeEvent} from "react";

export interface InputProps {
    placeholder?: string;
    type?: string;
    value?: object | null;
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;

}