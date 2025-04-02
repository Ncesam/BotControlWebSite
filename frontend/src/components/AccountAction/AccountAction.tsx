import {FC, useContext} from "react";
import React from "react";
import {AccountActionProps, AccountActionType} from "./AccountAction.props";
import AccountLogo from "../../assets/svg/AccountLogo.svg";
import Button, {ButtonType} from "@/ui/Button/Button";
import {useNavigate} from "react-router-dom";
import {LOGIN_ROUTE, REGISTER_ROUTE} from "@/utils/consts";
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
            <Button type={ButtonType.Logout} onClick={click}>Выйти</Button>
        </div> :
        <div className="container flex justify-end items-center mr-4 gap-2">
            <Button type={ButtonType.Login} onClick={() => navigate(LOGIN_ROUTE)}>Войти</Button>
            <Button type={ButtonType.Login} onClick={() => navigate(REGISTER_ROUTE)}>Зарегистрироваться</Button>
        </div>
    )
};


export default AccountAction;
export {AccountActionType};
