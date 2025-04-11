import type {FC} from "react";
import React from "react";
import {SortingLabelProps} from "./SortingLabel.props";
import ArrowDown from "@/assets/svg/ArrowDown.svg";
import ArrowUp from "@/assets/svg/ArrowUp.svg";

const SortingLabel: FC<SortingLabelProps> = ({isAscending, setIsAscending}) => {
    return (
        <div onClick={() => setIsAscending(prev => !prev)}
             className={"flex items-center gap-2 px-6 py-2 m-2 w-fit text-white bg-blue-600 rounded-lg shadow-md transition-all duration-300 ease-in-out hover:bg-blue-700 hover:scale-105 active:scale-95"}>
            <span>Сортировка</span>
            {isAscending ? (<ArrowDown/>) : (<ArrowUp/>)}
        </div>
    );
};

export default SortingLabel;

