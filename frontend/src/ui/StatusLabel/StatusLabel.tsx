import React from "react";
import type {FC} from "react";
import {StatusLabelProps} from "./StatusLabel.props";
import {startBot, stopBot} from "@/http/BotsAPI";

const StatusLabel: FC<StatusLabelProps> = ({value, setValue, botId}) => {
    const handleClick = async () => {
        if (value) {
            await stopBot(botId);
            setValue(false);
        } else {
            await startBot(botId);
            setValue(true);
        }
    };

    return (
        <div
            className={`rounded-lg p-0.5 inline-block text-2xl cursor-pointer ${
                value ? "bg-green-500" : "bg-red-500"
            }`}
            onClick={handleClick}
        >
            {value ? "✔" : "✖"}
        </div>
    );
};
export default StatusLabel;

