export const LOGIN_ROUTE = '/login'
export const BOTS_ROUTE = '/bots'
export const ADD_BOT_ROUTE = '/add_bot'
export const REGISTER_ROUTE = '/register'
export const options = [
    { value: "shop", label: "Магазин" },
    { value: "baf", label: "Баф" },
    { value: "ads", label: "Реклама" }
]

export const commands = [
    { id: 2, regex: "{title} у", enabled: false, answer: "благословение удачи", name: "Благо Удачи" },
    { id: 3, regex: "{title} г", enabled: false, answer: "благословение гоблина", name: "Благо Гоблина" },
    { id: 4, regex: "{title} н", enabled: false, answer: "благословение нежити", name: "Благо Нежити" },
    { id: 1, regex: "{title} а", enabled: false, answer: "благословение атаки", name: "Благо Атаки" },
    { id: 5, regex: "{title} д", enabled: false, answer: "благословение демона", name: "Благо Демона" },
    { id: 6, regex: "{title} м", enabled: false, answer: "благословение гнома", name: "Благо Гнома" },
    { id: 7, regex: "{title} о", enabled: false, answer: "благословение орка", name: "Благо Орка" },
    { id: 8, regex: "{title} л", enabled: false, answer: "проклятие неудачи", name: "Проклятие Неудачи" },
    { id: 9, regex: "{title} б", enabled: false, answer: "проклятие боли", name: "Проклятие Боли" },
    { id: 10, regex: "{title} ю", enabled: false, answer: "проклятие добычи", name: "Проклятие Добычи" },
    { id: 11, regex: "{title} и", enabled: false, answer: "очищение", name: "Очищение" },
    { id: 12, regex: "{title} т", enabled: false, answer: "очищение огнем", name: "Очищение Огнем" },
    { id: 13, regex: "{title} с", enabled: false, answer: "очищение светом", name: "Очищение Светом" },
];
