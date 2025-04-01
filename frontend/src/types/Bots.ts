export interface IBot {
    id: number
    title: string,
    description: string,
    token: string,
    answers_type: string,
    group_name: string,
    status: boolean
    nicknames: string | string[],
}

export interface IBotForm {
    title: string,
    description: string,
    token: string,
    group_name: string,
    answers_type: string | null | object,
    nicknames: string
}