import React, {FC, useContext} from "react";
import {HeaderProps} from "./Header.props";
import AccountAction, {AccountActionType} from "@/components/AccountAction/AccountAction";
import {Context} from "@/index";

const Header: FC<HeaderProps> = ({}) => {
    const context = useContext(Context);
    return (
        <div className={"w-full h-1/4 p-2 lg:p-4 bg-gray-600 flex items-center justify-between"}>
            <AccountAction type={context?.user?.isAuth ? AccountActionType.Logged : AccountActionType.Unlogged}/>
        </div>
    );
};

export default Header;

