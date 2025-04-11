import React, {useState} from "react";
import type {ChangeEvent, FC} from "react";
import {AddFormProps} from "./AddForm.props";
import Label from "@/ui/Label/Label";
import {TextColor} from "@/types/Color";
import {LabelSize} from "@/ui/Label/Label.props";
import TextArea from "@/ui/TextArea/TextArea";
import {TextAreaType} from "@/ui/TextArea/TextArea.props";
import Input from "@/ui/Input/Input";
import UploadFile from "@/ui/UploadFile/UploadFile";

const AddForm: FC<AddFormProps> = ({file, setFile, isAds, value, setValue, errors}) => {
    const handlerFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) {
            return;
        }
        setFile(e.target.files[0])
    }
    if (!isAds) {
        return (<div>
            <Label color={TextColor.blue} size={LabelSize.medium}>Имена людей
            </Label>
            <TextArea
                value={value}
                type={TextAreaType.bordered}
                setValue={setValue}
                placeholder="Через запятую"
            />
            {errors.nicknames && <p className="text-red-500">{errors.nicknames}</p>}
        </div>)
    } else {
        return (
            <div>
                <Label color={TextColor.blue} size={LabelSize.medium}>Текст Рекламы</Label>
                <TextArea
                    value={value}
                    type={TextAreaType.ads}
                    setValue={setValue}
                    placeholder="Текст Рекламы"
                />
                {
                    errors.nicknames && <p className="text-red-500">{errors.nicknames}</p>
                }
                <div>
                    <UploadFile onChange={handlerFileChange}/>
                </div>
            </div>
        )
    }
}

export default AddForm;

