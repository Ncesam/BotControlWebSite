import React from "react";
import type { FC } from "react";
import { CenterModalProps } from "./CenterModal.props";


const CenterModal: FC<CenterModalProps> = ({ activity, setActivity, children }) => {
    return (
        <div
            className={`fixed inset-0 z-50 flex items-center justify-center transition-all duration-300 ${activity
                    ? "bg-black/25 opacity-100 pointer-events-auto"
                    : "bg-transparent opacity-0 pointer-events-none"
                }`}
            onClick={() => setActivity(false)}
        >
            <div
                className={`relative bg-white p-6 rounded-lg shadow-xl w-11/12 lg:w-3/4 max-h-[150vh] overflow-y-auto transform transition-all duration-300 ease-out ${activity
                        ? "translate-y-0 opacity-100 scale-100"
                        : "translate-y-4 opacity-0 scale-95"
                    }`}
                onClick={(e) => e.stopPropagation()}
            >
                {children}
            </div>
        </div>
    );
};

export default CenterModal;
