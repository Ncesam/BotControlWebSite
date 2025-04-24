export interface IBot {
    id: number
    title: string,
    description: string,
    token: string,
    answers_type: string,
    group_name: string,
    status: boolean
    nicknames: string | string[],
    commands: Command[],
    text: string,
    ads_delay: number
}

export interface IBotForm {
    title: string,
    description: string,
    token: string,
    group_name: string,
    answers_type: string | null | object,
    nicknames: string,
    text: string,
    ads_delay: number,
}

export type Command = {
    id: number;
    regex: string;
    answer: string;
    name: string;
    enabled: boolean;
};