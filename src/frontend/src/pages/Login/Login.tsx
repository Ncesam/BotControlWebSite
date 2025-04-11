import React, {ChangeEvent, FC, useContext, useState} from "react";
import {LoginProps} from "./Login.props";
import Label from "@/ui/Label/Label";
import {HexColor, TextColor} from "@/types/Color";
import Input from "@/ui/Input/Input";
import Button, {ButtonType} from "@/ui/Button/Button";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import {Context} from "@/index";
import {login} from "@/http/UserAPI";
import {BOTS_ROUTE, REGISTER_ROUTE} from "@/utils/consts";
import {Link, useNavigate} from "react-router-dom";

const Login: FC<LoginProps> = () => {
    const context = useContext(Context);
    const navigate = useNavigate();
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>("");


    const changeEmail = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value);
    const changePassword = (e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value);

    const click = async () => {
        setLoading(true);
        setErrorMessage("");

        try {
            await login({ email, password });
            context?.user.setUser({email});
            context?.user.setIsAuth(true);
            navigate(BOTS_ROUTE);
        } catch (error) {
            setErrorMessage("Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-1 justify-center items-center w-full h-3/4">
            <div>
                <div className={"flex justify-center mb-4"}>
                    <Label color={TextColor.black}>Войти</Label>
                </div>
                <div className={"flex flex-col items-center gap-2"}>
                    <Input placeholder={"Email"} type={"email"} onChange={changeEmail}/>
                    <Input placeholder={"Password"} type={"password"} onChange={changePassword}/>
                </div>
                <div className={"flex justify-center gap-2"}>
                    <div>Нет аккаунта?</div>
                    <Link to={REGISTER_ROUTE} className={"text-red-500 font-bold"}>Создай</Link>
                </div>
                {errorMessage && (
                    <div className="text-red-500 text-center mt-4">
                        <p>{errorMessage}</p>
                    </div>
                )}
                {!loading ? (
                    <div className={"flex justify-center mt-4"}>
                        <Button type={ButtonType.Submit} onClick={click}>
                            Войти
                        </Button>
                    </div>
                ) : (
                    <div className="flex justify-center mt-4">
                        <Loading color={HexColor.black} type={LoadingType.Small} />
                    </div>
                )}
            </div>
        </div>
    );
};

export default Login;
