import type {FC} from "react";
import React from "react";
import {CardContentProps} from "./CardContent.props";
import Label from "@/ui/Label/Label";
import {TextColor} from "@/types/Color";

const CardContent: FC<CardContentProps> = ({content}) => {
    const maxLength = 10
    const truncatedText = content.description.length > maxLength ? content.description.slice(0, maxLength) + "..." : content.description;
    return (<div className={"text-2xl"}>
            <div className={"flex items-center justify-between"}>
                <Label color={TextColor.white}>Id:</Label>
                <span className={"text-white ml-5"}>{content.id}</span>
            </div>
            <div className={"flex items-center justify-between"}>
                <Label color={TextColor.white}>Title:</Label>
                <span className={"text-white ml-5"}>{content.title}</span>
            </div>
            <div className={"flex items-center justify-between"}>
                <Label color={TextColor.white}>Description:</Label>
                <span className={"text-white ml-5"}>{truncatedText}</span>
            </div>
        </div>
    );
};

export default CardContent;

