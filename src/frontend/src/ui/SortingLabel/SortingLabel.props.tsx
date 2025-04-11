import {Dispatch, SetStateAction} from "react";

export interface SortingLabelProps {
    isAscending: boolean;
    setIsAscending: Dispatch<SetStateAction<boolean>>;
}