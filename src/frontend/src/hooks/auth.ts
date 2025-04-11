import {useContext, useEffect, useState} from "react";
import {$api} from "@/http";
import {Context} from "@/index";


const useAuth = () => {
    const context = useContext(Context);

    useEffect(() => {
        const refreshToken = async () => {
            try {
                console.log("Refresh token...");
                await $api.put("/api/auth/refresh", {}, {withCredentials: true});
            } catch (error) {
                console.error("Ошибка обновления токена:", error);
                window.location.href = "/login";
            }
        };

        const interval = setInterval(() => {
            refreshToken();
        }, 20 * 1000 * 60);

        return () => clearInterval(interval);
    }, []);

};

export {useAuth};

const useAutoLogin = () => {
    const context = useContext(Context);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const {status, data} = await $api.get("/api/auth/me", {withCredentials: true});

                if (status === 403) {
                    window.location.href = "/login";
                    return;
                }

                context?.user.setUser({email: data.result.email});
                context?.user.setIsAuth(true);
                return;
            } catch (e) {
                console.log("error: ", e);
            }

        };

        checkAuth();
    }, []);

    return;
};

export {useAutoLogin};