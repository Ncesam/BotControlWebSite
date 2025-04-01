import {TextColor} from "@/types/Color";
import React from "react";

export interface LabelProps {
    children?: React.ReactNode;
    color?: TextColor;
    size?: LabelSize;
}

export enum LabelSize{
    small = "text-xs",
    medium = "text-lg",
    large = "text-xl"
}