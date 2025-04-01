import React from "react";
import type {FC} from "react";
import {CenterModalProps} from "./CenterModal.props";

const CenterModal: FC<CenterModalProps> = ({activity, setActivity, children}) => {
    return (
        <div
            className={`fixed top-0 left-0 w-screen h-screen bg-black/25 flex justify-center items-center transition-opacity duration-500 ${activity ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"}`}
            onClick={() => setActivity(false)}>
            <div
                className={`bg-white p-6 rounded-md w-5/6 lg:w-1/4 lg:max-w-1/2 transition-transform duration-500 ${activity ? "scale-100 opacity-100" : "scale-90 opacity-0"}`}
                onClick={(e) => e.stopPropagation()}>
                {children}
            </div>
        </div>

    );
};

export default CenterModal;

