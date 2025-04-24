import type { FC } from "react";
import React, { useState } from "react";
import Label from "@/ui/Label/Label";
import { TextColor } from "@/types/Color";
import Input from "@/ui/Input/Input";
import Button, { ButtonType } from "@/ui/Button/Button";
import { boolean, string, z } from "zod";
import { Command, IBotForm } from "@/types/Bots";
import { addBot, UploadFile } from "@/http/BotsAPI";
import SelectMenu from "@/ui/SelectMenu/SelectMenu";
import { SingleValue } from "react-select";
import { Option } from "@/ui/SelectMenu/SelectMenu.props";
import ArrowLeft from "@/assets/svg/ArrowLeft.svg";
import { BOTS_ROUTE, commands, options } from "@/utils/consts";
import { AddBotProps } from "@/pages/AddBot/AddBot.props";
import AddForm from "@/components/AddForm/AddForm";
import { useNavigate } from "react-router-dom";
import CheckBox from "@/ui/CheckBox/CheckBox";
import CenterModal from "@/components/Modals/CenterModal/CenterModal";
import { LabelSize } from "@/ui/Label/Label.props";
const commandSchema = z.object({
    id: z.number(),
    regex: z.string(),
    answer: z.string(),
    name: z.string(),
    enabled: z.boolean().optional()
});
const botSchema = z.object({
    title: z.string().min(3, "Название должно быть минимум 3 символа").nonempty("Название обязательно для заполнения"),
    description: z.string().min(5, "Описание слишком короткое").nonempty("Описание обязательно для заполнения"),
    token: z.string().min(10, "Токен слишком короткий").nonempty("Токен обязательно для заполнения"),
    group_name: z.string().min(3, "Название группы должно быть минимум 3 символа").nonempty("Название группы обязательно для заполнения"),
    answers_type: z.record(string()).optional(),
    nicknames: z.string().optional(),
    text: z.string().optional(),
    commands: z.array(commandSchema).optional()
});

const AddBot: FC<AddBotProps> = ({ }) => {
    const [isSettings, setIsSettings] = useState<boolean>(false);
    const [title, setTitle] = useState<string>("");
    const [file, setFile] = useState<File | null>(null);
    const [description, setDescription] = useState<string>("");
    const [token, setToken] = useState<string>("");
    const [group_name, setGroupName] = useState<string>("");
    const [nicknames, setNickNames] = useState<string>("");
    const [text, setText] = useState<string>("");
    const [answers_type, setAnswersType] = useState<SingleValue<Option>>(options[0]);
    const [active, setIsActive] = useState<boolean>(false);
    const [ads_delay, setAdsDelay] = useState<number>(10)
    const [commandsState, setCommands] = useState<Command[]>(commands);
    const [errors, setErrors] = useState<Record<string, string>>({});
    const navigate = useNavigate();

    const toggleCommand = (id: number) => {
        setCommands(prevCommands =>
            prevCommands.map(cmd =>
                cmd.id === id ? { ...cmd, enabled: !cmd.enabled } : cmd
            )
        );
    };
    const click = async () => {
        const bot: IBotForm = { title, description, token, group_name, answers_type, nicknames, text, ads_delay };
        console.log(commandsState)
        const result = botSchema.safeParse(bot);
        if (!result.success) {
            const errorObj: Record<string, string> = {};
            result.error.issues.forEach((issue) => {
                errorObj[issue.path[0]] = issue.message;
            });
            console.log(errorObj);
            setErrors(errorObj);
            return;
        }
        try {
            if (answers_type && 'value' in answers_type) {
                bot.answers_type = answers_type.value;
            }
            if (file) {
                await addBot(bot, file);
            } else {
                await addBot(bot);
            }
            setErrors({});
        } catch (e) {
            setErrors({ form: "Ошибка при добавлении бота" });
        }
        navigate(BOTS_ROUTE);
    }
    return (
        <div className={"flex-1 flex w-full justify-center items-center"}>
            {!isSettings ?
                <div className="flex flex-col justify-center items-center gap-4">
                    <Label color={TextColor.gray}>Добавить Бота</Label>
                    <Input
                        placeholder="Название"
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                    {errors.title && <p className="text-red-500">{errors.title}</p>}

                    <Input
                        placeholder="Описание"
                        type="text"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                    {errors.description && <p className="text-red-500">{errors.description}</p>}

                    <Input
                        placeholder="Токен ВК"
                        type="text"
                        value={token}
                        onChange={(e) => setToken(e.target.value)}
                    />
                    {errors.token && <p className="text-red-500">{errors.token}</p>}

                    <Input
                        placeholder="Название группы"
                        type="text"
                        value={group_name}
                        onChange={(e) => setGroupName(e.target.value)}
                    />
                    {errors.group_name && <p className="text-red-500">{errors.group_name}</p>}

                    {errors.form && (
                        <div className="text-red-500 text-center mt-4">
                            <p>{errors.form}</p>
                        </div>
                    )}
                    <div className={"flex justify-center items-center gap-4"}>
                        <Button type={ButtonType.Submit} onClick={click}>Добавить</Button>
                        <Button type={ButtonType.Submit} onClick={() => setIsSettings(true)}>Настройки</Button>
                    </div>
                </div> :
                <div className={"flex flex-col h-full w-1/2 gap-4"}>
                    <div className={"gap-2"}>
                        <div className={"self-start w-1/2"}>
                            <Label color={TextColor.blue}>Тип Бота</Label>
                            <SelectMenu options={options} selected={answers_type} setSelected={setAnswersType} />
                        </div>
                        {!answers_type ? null : answers_type?.value === "baf" || answers_type?.value === "shop" ?
                            <AddForm file={file} setFile={setFile} errors={errors} isAds={false} value={nicknames}
                                setValue={setNickNames} /> :
                            <div className={"gap-3"}>
                                <AddForm file={file} setFile={setFile} errors={errors} isAds={true} value={text}
                                setValue={setText} />
                                <Label size={LabelSize.medium} color={TextColor.blue    }>Время между рекламой</Label>
                                <Input placeholder={"Время между рекламой"} type="text" value={ads_delay.toString()} onChange={(e) => setAdsDelay(Number(e.target.value))} /></div>
                        }
                    </div>
                    <div className={"self-start"}>
                        <Button type={ButtonType.Back} onClick={() => setIsSettings(false)}>
                            <ArrowLeft color={"#2b7fff"} width={20} height={20} />
                        </Button>
                    </div>
                </div>
            }
        </div>)
};

export default AddBot;

