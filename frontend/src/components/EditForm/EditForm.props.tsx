import {Dispatch, SetStateAction} from "react";

export interface EditFormProps {
    id: number;
    activity: boolean;
    setActivity: Dispatch<SetStateAction<boolean>>;

}