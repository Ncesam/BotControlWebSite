import {SingleValue} from "react-select";
import {Option} from "@/ui/SelectMenu/SelectMenu.props";
import {Dispatch, SetStateAction} from "react";

export interface AddFormProps {
    selected: SingleValue<Option>,
    errors: Record<string, string>,
    value: any,
    setValue: Dispatch<SetStateAction<any>>,
}