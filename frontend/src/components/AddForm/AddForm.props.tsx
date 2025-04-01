import {Dispatch, SetStateAction} from "react";

export interface AddFormProps {
    activity: boolean;
    setActivity: Dispatch<SetStateAction<boolean>>;
}