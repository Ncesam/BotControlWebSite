import {Dispatch, SetStateAction} from "react";

export interface AddFormProps {
    file: File | null;
    setFile: Dispatch<SetStateAction<File | null>>;
    isAds: boolean;
    errors: Record<string, string>,
    value: any,
    setValue: Dispatch<SetStateAction<any>>,
}