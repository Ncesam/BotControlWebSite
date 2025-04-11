import type {FC} from "react";
import React from "react";
import {LoadingProps} from "./Loading.props";
import {RotateLoader} from "react-spinners";
import {LoadingType} from "@/types/Loading";

const Loading: FC<LoadingProps> = ({type, color}) => {
    let size: string;
    let className: string;
    if (type === LoadingType.Large) {
        size = "15px";
        className = "flex items-center justify-center h-screen";
    } else if (type === LoadingType.Medium) {
        size = "10px";
        className = "flex flex-1 items-center justify-center h-3/4 w-full";
    } else {
        size = "5px";
        className = "flex items-center justify-center";
    }
    return (
        <div className={className}>
            <RotateLoader color={color} size={size}/>
        </div>
    );
};

export default Loading;

