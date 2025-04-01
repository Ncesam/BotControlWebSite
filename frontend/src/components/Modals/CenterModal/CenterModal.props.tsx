import React, {Dispatch, ReactNode, SetStateAction} from "react";

export interface CenterModalProps {
    activity: boolean,
    setActivity: Dispatch<SetStateAction<boolean>>,
    children: ReactNode
}