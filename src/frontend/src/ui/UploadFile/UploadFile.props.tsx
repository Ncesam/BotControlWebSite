import { ChangeEvent } from "react";

export interface UploadFileProps {
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;
}