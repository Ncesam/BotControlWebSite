export interface PoputProps {
    type: PoputType,
    id?: number
}

export enum PoputType {
    EditBot,
    AddBot,
}