import React, {FC, useContext, useEffect} from "react";
import {HeaderProps} from "./Header.props";
import AccountAction, {AccountActionType} from "@/components/AccountAction/AccountAction";
import {Context} from "@/index";
import { observer } from "mobx-react";

const Header: FC<HeaderProps> = observer(() => {
    const context = useContext(Context);

    return (
        <div className={`
            w-full lg:w-3/5 
            h-1/4 p-2 lg:p-4 
            bg-baseColor 
            shadow-md rounded-b-lg shadow-baseColor 
            flex items-center justify-between 
            lg:opacity-0 lg:delay-75 
            lg:duration-500 lg:ease-in-out 
            lg:transition-all lg:hover:opacity-100
        `}>
            <AccountAction
                type={context?.user?.isAuth
                    ? AccountActionType.Logged
                    : AccountActionType.Unlogged
                }
            />
        </div>
    );
});

export default Header;

