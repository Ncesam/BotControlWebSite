import {observer} from "mobx-react";
import React, {FC, lazy, Suspense, useContext} from "react";
import {Context} from "@/index";
import {Navigate, Route, Routes} from "react-router-dom";
import {authRoutes, publicRoutes} from "@/routes";
import {BOTS_ROUTE, LOGIN_ROUTE} from "@/utils/consts";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import {HexColor} from "@/types/Color";


const AppRoutes: FC = observer(() => {
    const context = useContext(Context);

    return (
        <Suspense fallback={<Loading type={LoadingType.Medium} color={HexColor.black} />}>
            <Routes>
                {context?.user.isAuth ? (
                    <>
                        {authRoutes.map(({ path, component }) => (
                            <Route key={path} path={path} element={React.createElement(component)} />
                        ))}
                        <Route path="*" element={<Navigate to={BOTS_ROUTE} replace />} />
                    </>
                ) : (
                    <>
                        {publicRoutes.map(({ path, component }) => (
                            <Route key={path} path={path} element={React.createElement(component)} />
                        ))}
                        <Route path="*" element={<Navigate to={LOGIN_ROUTE} replace />} />
                    </>
                )}
            </Routes>
        </Suspense>
    );
});

export default AppRoutes;