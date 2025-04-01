import {FC, useState} from "react";
import React from "react";
import {CardProps} from "./Card.props";
import CardContent from "@/components/CardContent/CardContent";
import StatusLabel from "@/ui/StatusLabel/StatusLabel";
import Poput from "@/modules/Poput/Poput";
import {PoputType} from "@/modules/Poput/Poput.props";

const Card: FC<CardProps> = ({card}) => {
    const [status, setStatus] = useState<boolean>(card.status)
    return (
        <div className={`bg-gray-700 w-full rounded-md p-5 shadow-md shadow-blue-500`}>
            <CardContent content={card}/>
            <div className="flex justify-between items-end mt-10">
                <Poput type={PoputType.EditBot} id={card.id}/>
                <StatusLabel value={status} setValue={setStatus} botId={card.id}/>
            </div>
        </div>
    )
};

export default Card;

