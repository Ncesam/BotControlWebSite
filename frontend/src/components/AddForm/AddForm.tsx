import React, {useState} from "react";
import type {FC} from "react";
import {AddFormProps} from "./AddForm.props";
import Label from "@/ui/Label/Label";
import {TextColor} from "@/types/Color";
import {LabelSize} from "@/ui/Label/Label.props";
import TextArea from "@/ui/TextArea/TextArea";
import {TextAreaType} from "@/ui/TextArea/TextArea.props";
import Input from "@/ui/Input/Input";

const AddForm: FC<AddFormProps> = ({selected, value, setValue, errors}) => {
    const [file, setFile] = useState<File | null>(null)
    if (!selected) {
        return null;
    }
    if (selected.value === "storage" || selected.value === "baf") {
        return (<div>
            <Label color={TextColor.blue} size={LabelSize.medium}>Имена людей</Label>
            <TextArea
                value={value}
                type={TextAreaType.bordered}
                setValue={setValue}
                placeholder="Через запятую"
            />
            {errors.nicknames && <p className="text-red-500">{errors.nicknames}</p>}
        </div>)
    } else if (selected.value === "ads") {
        return (
            <div>
                <Label color={TextColor.blue} size={LabelSize.medium}>Текст Рекламы</Label>
                <TextArea
                    value={value}
                    type={TextAreaType.ads}
                    setValue={setValue}
                    placeholder="Текст Рекламы"
                />
                {errors.nicknames && <p className="text-red-500">{errors.nicknames}</p>}
                <div>
                   <Input type={"file"} onChange={(e) => setFile(e.target.)} value={file}/>
                </div>
            </div>
        )
    }

};

export default AddForm;

