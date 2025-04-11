import React, {lazy, Suspense} from 'react';
import {BrowserRouter,} from "react-router-dom";
import {HexColor} from "@/types/Color";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import {useAuth, useAutoLogin} from "@/hooks/auth";
import AddBot from './pages/AddBot/AddBot';

const Header = lazy(() => import("@/modules/Header/Header"));
const AppRoutes = lazy(() => import("@/AppRoutes"));


const App = () => {
    useAuth()
    useAutoLogin()
    return (
        <BrowserRouter>
            <div className="min-h-screen min-w-screen flex items-center flex-col">
                <Suspense fallback={<Loading type={LoadingType.Large} color={HexColor.black}/>}>
                    <Header/>
                    <AppRoutes/>
                </Suspense>
            </div>
        </BrowserRouter>
    )
}

export default App;
