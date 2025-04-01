import {BOTS_ROUTE, LOGIN_ROUTE, REGISTER_ROUTE} from "@/utils/consts";
import {lazy} from "react";

const Login = lazy(() => import("@/pages/Login/Login"));
const Registration = lazy(() => import("@/pages/Registration/Registration"));
const Bots = lazy(() => import("@/pages/Bots/Bots"));
export const authRoutes = [
    {
        path: BOTS_ROUTE,
        component: Bots
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