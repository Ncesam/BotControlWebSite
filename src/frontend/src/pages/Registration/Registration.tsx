import React, {ChangeEvent, useContext, useState} from "react";
import type {FC} from "react";
import {RegistrationProps} from "./Registration.props";
import {Context} from "@/index";
import {login, register} from "@/http/UserAPI";
import Label from "@/ui/Label/Label";
import {HexColor, TextColor} from "@/types/Color";
import Input from "@/ui/Input/Input";
import Button, {ButtonType} from "@/ui/Button/Button";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";

const Registration: FC <RegistrationProps> = ({}) => {
    const context = useContext(Context);
    const [email, setEmail] = useState<string>("");
    const [nickname, setNickname] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>("");


    const changeEmail = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value);
    const changeNickname = (e: ChangeEvent<HTMLInputElement>) => setNickname(e.target.value);
    const changePassword = (e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value);

    const click = async () => {
        setLoading(true);
        setErrorMessage("");
        try {
            await register({ email, nickname, password });
            context?.user.setUser({email});
            context?.user.setIsAuth(true);
        } catch (error) {
            setErrorMessage("Registration failed. Please check your email/password");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-1 justify-center items-center w-full h-3/4">
            <div>
                <div className={"flex justify-center mb-4"}>
                    <Label color={TextColor.black}>Регистрация</Label>
                </div>
                <div className={"flex flex-col items-center gap-2"}>
                    <Input placeholder={"Email"} type={"email"} onChange={changeEmail}/>
                    <Input placeholder={"NickName"} type={"text"} onChange={changeNickname}/>
                    <Input placeholder={"Password"} type={"password"} onChange={changePassword}/>
                </div>
                {errorMessage && (
                    <div className="text-red-500 text-center mt-4">
                        <p>{errorMessage}</p>
                    </div>
                )}
                {!loading ? (
                    <div className={"flex justify-center mt-4"}>
                        <Button type={ButtonType.Submit} onClick={click}>
                            Зарегистрироваться
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

export default Registration;

