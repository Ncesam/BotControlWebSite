import {Dispatch, SetStateAction} from "react";
import {SingleValue} from "react-select";

export interface SelectMenuProps {
    options: Option[];
    selected: SingleValue<Option>;
    setSelected: Dispatch<SetStateAction<SingleValue<Option>>>
}

export interface Option {
    value: string;
    label: string;
}
