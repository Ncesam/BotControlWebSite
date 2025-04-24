import React, { FC, useContext, useEffect, useState } from "react";
import { EditFormProps } from "./EditForm.props";
import Label from "@/ui/Label/Label";
import { HexColor, TextColor } from "@/types/Color";
import Input from "@/ui/Input/Input";
import Button, { ButtonType } from "@/ui/Button/Button";
import SelectMenu from "@/ui/SelectMenu/SelectMenu";
import { LabelSize } from "@/ui/Label/Label.props";
import TextArea from "@/ui/TextArea/TextArea";
import { TextAreaType } from "@/ui/TextArea/TextArea.props";
import ArrowLeft from "@/assets/svg/ArrowLeft.svg";
import { Context } from "@/index";
import { SingleValue } from "react-select";
import { Option } from "@/ui/SelectMenu/SelectMenu.props";
import { commands, options } from "@/utils/consts";
import { Command, IBotForm } from "@/types/Bots";
import { deleteBot, editBot, sendCommands } from "@/http/BotsAPI";
import { string, z } from "zod";
import Loading from "@/ui/Loading/Loading";
import { LoadingType } from "@/types/Loading";
import TrashIcon from "@/assets/svg/TrashIcon.svg"
import AddForm from "@/components/AddForm/AddForm";
import CheckBox from "@/ui/CheckBox/CheckBox";
import CenterModal from "../Modals/CenterModal/CenterModal";
import { time } from "console";
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
    group_name: z.string().min(3, "Название группы должно быть минимум 3 символа").nonempty("Название группы обязательно для заполнения"),
    answers_type: z.record(string()).optional(),
    nicknames: z.string().optional().nullable(),
    text: z.string().optional().nullable(),
    commands: z.array(commandSchema).optional()
});
const EditForm: FC<EditFormProps> = ({ id, activity, setActivity }) => {
    const context = useContext(Context);
    const [isSettings, setIsSettings] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    const [title, setTitle] = useState<string>("");
    const [description, setDescription] = useState<string>("");
    const [group_name, setGroupName] = useState<string>("");
    const [nicknames, setNickNames] = useState<string>("");
    const [token, setToken] = useState<string>("");
    const [answers_type, setAnswersType] = useState<SingleValue<Option>>(options[0]);
    const [text, setText] = useState<string>("");
    const [file, setFile] = useState<File | null>(null);
    const [active, setIsActive] = useState<boolean>(false);
    const [commandsState, setCommands] = useState<Command[]>(commands)
    const [ads_delay, setAdsDelay] = useState<number>(10);

    const [errors, setErrors] = useState<Record<string, string>>({});

    const toggleCommand = (id: number) => {
        setCommands(prevCommands =>
            prevCommands.map(cmd =>
                cmd.id === id ? { ...cmd, enabled: !cmd.enabled } : cmd
            )
        );
    };
    const sendActiveCommands = async () => {
        const activeCommands = commandsState.filter(cmd => cmd.enabled);
        if (activeCommands.length === 0) {
            return null;
        }
        await sendCommands(activeCommands, id);
    }
    const click = async () => {
        const bot: IBotForm = { title, description, token, group_name, answers_type, nicknames, text, ads_delay };
        const result = botSchema.safeParse(bot);
        console.log(result);
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
                await editBot(bot, id, file);
            } else {
                await editBot(bot, id);
            }
            setActivity(false);
            setErrors({});
        } catch (e) {
            setErrors({ form: "Ошибка при измении бота" });
        }
    }
    useEffect(() => {
        setIsLoading(true);
        const bot = context?.bots.bots?.find(bot => bot.id === id);
        if (bot) {
            setErrors({});
            setDescription(bot.description);
            setTitle(bot.title);
            setToken(bot.token);
            setGroupName(bot.group_name);
            setNickNames(
                Array.isArray(bot?.nicknames) ? bot?.nicknames.join(", ") : bot?.nicknames
            );
            setText(bot.text);
            const selectedOption = options.find(option => option.value === bot.answers_type);
            setAnswersType(selectedOption || null);
            if (bot.commands) {
                const mergedMap = new Map<number, Command>();
                commands.forEach(cmd => mergedMap.set(cmd.id, { ...cmd }));
                bot.commands.forEach(cmd => mergedMap.set(cmd.id, { ...cmd, enabled: true }));
                const commandsArray = Array.from(mergedMap.values())
                setCommands(commandsArray)
            }
            setAdsDelay(bot.ads_delay)
        } else {
            setErrors({ form: "Бот с таким ID не найден" });
        }
        setIsLoading(false);
    }, [id, context?.bots.bots])
    useEffect(() => {
        sendActiveCommands()
    }, [commandsState])
    return (
        <div>
            <Label size={LabelSize.small} color={TextColor.black}>{id}</Label>
            {
                isLoading ? <Loading type={LoadingType.Small} color={HexColor.blue} /> :
                    !isSettings ?
                        <div className="flex flex-col justify-center items-center gap-2">
                            <Label color={TextColor.gray}>Изменить Бота</Label>

                            <Label color={TextColor.blue} size={LabelSize.medium}>Название</Label>
                            <Input
                                placeholder="Название"
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                            />
                            {errors.title && <p className="text-red-500">{errors.title}</p>}

                            <Label color={TextColor.blue} size={LabelSize.medium}>Описание</Label>
                            <Input
                                placeholder="Описание"
                                type="text"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                            />
                            {errors.description && <p className="text-red-500">{errors.description}</p>}

                            <Label color={TextColor.blue} size={LabelSize.medium}>Название группы</Label>
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
                            <div className={"flex justify-between items-center gap-2 lg:gap-4"}>
                                <Button type={ButtonType.Submit} onClick={click}>Изменить</Button>
                                <Button type={ButtonType.Submit} onClick={() => setIsSettings(true)}>Настройки</Button>
                                <Button type={ButtonType.Delete} onClick={async () => await deleteBot(id)}><TrashIcon
                                    color={"white"} /></Button>
                            </div>
                        </div> :
                        <div className={"flex flex-col items-center w-full gap-4"}>
                            <div className={"w-full gap-2"}>
                                <div className={"self-start w-1/2"}>
                                    <Label color={TextColor.blue}>Тип Бота</Label>
                                    <SelectMenu options={options} selected={answers_type} setSelected={setAnswersType} />
                                </div>
                                {!answers_type ? null : answers_type?.value === "baf" || answers_type?.value === "shop" ?
                                    <AddForm file={file} setFile={setFile} errors={errors} isAds={false}
                                        value={nicknames}
                                        setValue={setNickNames} /> :
                                    <div className={"gap-3"}>
                                        <AddForm file={file} setFile={setFile} errors={errors} isAds={true} value={text}
                                            setValue={setText} />
                                        <Label size={LabelSize.medium} color={TextColor.blue}>Время между рекламой</Label>
                                        <Input placeholder={"Время между рекламой"} type="text" value={ads_delay.toString()} onChange={(e) => setAdsDelay(Number(e.target.value))} /></div>
                                }
                            </div>
                            {!answers_type ? null : answers_type?.value === "baf" ?
                                <Button type={ButtonType.Submit} onClick={() => setIsActive(!active)}>
                                    Открыть команды
                                </Button> : null}
                            {
                                active ? <CenterModal activity={active} setActivity={setIsActive}>
                                    <div className={"h-full w-full grid grid-cols-2 gap-1"}>
                                        {commandsState.map((command) => <CheckBox key={command.id} setValue={async () => {
                                            toggleCommand(command.id)
                                        }} placeholder={command.name} value={command.enabled} />
                                        )}
                                    </div>
                                </CenterModal> : null
                            }
                            <div className={"self-start"}>
                                <Button type={ButtonType.Back} onClick={() => setIsSettings(false)}>
                                    <ArrowLeft color={"#2b7fff"} width={20} height={20} />
                                </Button>
                            </div>
                        </div>
            }
        </div>)
};

export default EditForm;