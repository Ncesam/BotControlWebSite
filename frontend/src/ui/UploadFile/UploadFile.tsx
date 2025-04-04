import { FC, useRef } from "react";
import { UploadFileProps } from "./UploadFile.props";
import Input from "../Input/Input";
import Button, { ButtonType } from "../Button/Button";


const UploadFile: FC<UploadFileProps> = ({onChange}) => {
    const inputRef = useRef<HTMLInputElement | null>(null);
    return (
        <div>
            <Button type={ButtonType.Submit} onClick={() => inputRef?.current?.click()}>Выбрать файл</Button>
            <input ref={inputRef} className={"hidden"} onChange={onChange} type="file"/>
        </div>
    )
}

export default UploadFile;