import {$api} from "@/http/index";
import {IBot, IBotForm} from "@/types/Bots";

export const getBots = async () => {
    const { status, data } = await $api.get("/api/bots");
    if (status === 200) {
        let bots: IBot[] = data.result.items[0].bots;
        return bots;
    } else if (status === 401) {
        return null;
    }
}
export const UploadFile = async (file: File) => {
    const {status, data} = await $api.post("/api/upload_file", {file}, {headers: {"Content-Type": file.type, "Content-Length": `${file.size}`}});
    if (status === 200) {
        return data.message;
    } else if (status === 401) {
        return null;
    }
} 

export const addBot = async (bot: IBotForm) => {
    const {status, data} = await $api.post("/api/bots", {...bot});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}

export const editBot = async (bot: IBotForm, botId: number) => {
    const {status, data} = await $api.put("/api/bots", {...bot, id: botId});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}

export const startBot = async (botId: number) => {
    const {status, data} = await $api.put("/api/bots/start", {bot_ids: [botId]});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}
export const stopBot = async (botId: number) => {
    const {status, data} = await $api.put("/api/bots/stop", {bot_ids: [botId]});
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}

export const deleteBot = async (botId: number) => {
    await stopBot(botId);
    const {status, data} = await $api.delete(`/api/bots?bot_id=${botId}`);
    if (status === 200) {
        return data.msg;
    } else if (status === 401) {
        return null;
    }
}
