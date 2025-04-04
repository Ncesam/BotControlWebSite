import {ChangeEvent} from "react";

export interface InputProps {
    placeholder?: string;
    type?: string;
    value?: string;
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;
}
