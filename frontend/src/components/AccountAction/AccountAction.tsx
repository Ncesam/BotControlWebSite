import {FC, useContext} from "react";
import React from "react";
import {AccountActionProps, AccountActionType} from "./AccountAction.props";
import AccountLogo from "../../assets/svg/AccountLogo.svg";
import Button, {ButtonType} from "@/ui/Button/Button";
import {useNavigate} from "react-router-dom";
import {LOGIN_ROUTE} from "@/utils/consts";
import {Context} from "@/index";
import {logout} from "@/http/UserAPI";

const AccountAction: FC<AccountActionProps> = ({type}) => {
    const navigate = useNavigate();
    const context = useContext(Context);
    const click = async () => {
        await logout();
        context?.user.setIsAuth(false);
        context?.user.setUser(null);
        navigate(LOGIN_ROUTE);
    }
    return (type === AccountActionType.Logged ?
        <div className="container flex justify-end items-center mr-4">
            <AccountLogo height={50} width={50} color={"white"}/>
            <Button type={ButtonType.Logout} onClick={click}>Logout</Button>
        </div> :
        <div className="container flex justify-end items-center mr-4">
            <Button type={ButtonType.Login}>Login</Button>
        </div>
    )
};


export default AccountAction;
export {AccountActionType};
