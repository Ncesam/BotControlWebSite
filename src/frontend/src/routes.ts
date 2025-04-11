import {ADD_BOT_ROUTE, BOTS_ROUTE, LOGIN_ROUTE, REGISTER_ROUTE} from "@/utils/consts";
import {lazy} from "react";

const AddBot = lazy(() => import("@/pages/AddBot/AddBot"));
const Login = lazy(() => import("@/pages/Login/Login"));
const Registration = lazy(() => import("@/pages/Registration/Registration"));
const Bots = lazy(() => import("@/pages/Bots/Bots"));
export const authRoutes = [
    {
        path: BOTS_ROUTE,
        component: Bots
    }, {
        path: ADD_BOT_ROUTE,
        component: AddBot
    }
]
export const publicRoutes = [
    {
        path: REGISTER_ROUTE,
        component: Registration
    },
    {
        path: LOGIN_ROUTE,
        component: Login
    }
]