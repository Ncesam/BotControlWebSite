import {$api} from "@/http/index";
import {IBot, IBotForm} from "@/types/Bots";

export const getBots = async () => {
    const {status, data} = await $api.get("/bots");
    if (status === 200) {
        let bots: IBot[] = data.result.items[0].bots;
        return bots;
    } else if (status === 401) {
        return null;
    }
}
export const UploadFile = async (file: File, bot_id: number, user_id: number) => {
    const {
        status,
        data
    } = await $api.post(`/upload_file?user_id=${user_id}&bot_id=${bot_id}`, {file}, {
        headers: {
            "Content-Type": file.type,
            "Content-Length": `${file.size}`
        }
    });
    if (status === 200) {
        return data.message;
    } else if (status === 401) {
        return null;
    }
}

export const addBot = async (bot: IBotForm, file?: File) => {
    try {
        const {status, data} = await $api.post("/bots", {file}, {
            headers: {
                "Content-Type": "multipart/form-data"
            },
            params: {
                ...bot
            }
        });

        // Обрабатываем результат
        if (status === 200) {
            return data.msg;
        } else if (status === 401) {
            return;
        } else {
            return;
        }
    } catch (error) {
        return;
    }
};


export const editBot = async (bot: IBotForm, botId: number, file?: File) => {
    const {status, data} = await $api.put("/bots", {file}, {headers: {"Content-Type": "multipart/form-data"}, params: {...bot, id: botId}});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}

export const startBot = async (botId: number) => {
    const {status, data} = await $api.put("/bots/start", {bot_ids: [botId]});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}
export const stopBot = async (botId: number) => {
    const {status, data} = await $api.put("/bots/stop", {bot_ids: [botId]});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}

export const deleteBot = async (botId: number) => {
    await stopBot(botId);
    const {status, data} = await $api.delete(`/bots?bot_id=${botId}`);
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}
