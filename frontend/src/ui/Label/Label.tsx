import type {FC} from "react";
import React from "react";
import {LabelProps, LabelSize} from "./Label.props";

const Label: FC<LabelProps> = ({children, color, size = LabelSize.large}) => {
    return (
        <div className={`font-bold ${size} ${color}`}>
            {children}
        </div>
    );
};

export default Label;

