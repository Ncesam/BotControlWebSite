import {Dispatch, SetStateAction} from "react";

export interface StatusLabelProps {
    value: boolean;
    setValue: Dispatch<SetStateAction<boolean>>;
    botId: number;
}