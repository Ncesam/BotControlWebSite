import {ILoginUser, IRegisterUser} from "@/types/User";
import {$api} from "@/http/index";

export const login = async ({email, password}: ILoginUser) => {
    const {status, data} = await $api.post("api/auth/login", {email, password});
    if (status === 200) {
        return data;
    } else if (status === 401) {
        return null;
    }
}

export const register = async ({email, nickname, password}: IRegisterUser) => {
    const {status, data} = await $api.post("api/auth/register", {email, nickname, password});
    if (status === 200) {
        return data;
    } else if (status === 401) {
        return null;
    }
}

export const logout = async () => {
    const {status} = await $api.post("api/auth/logout");
    if (status === 200) {
        return status;
    } else if (status === 500) {
        return null;
    }
}