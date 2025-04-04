import type {FC} from "react";
import React, {useState} from "react";
import Label from "@/ui/Label/Label";
import {TextColor} from "@/types/Color";
import Input from "@/ui/Input/Input";
import Button, {ButtonType} from "@/ui/Button/Button";
import {string, z} from "zod";
import {IBotForm} from "@/types/Bots";
import {addBot, UploadFile} from "@/http/BotsAPI";
import SelectMenu from "@/ui/SelectMenu/SelectMenu";
import {SingleValue} from "react-select";
import {Option} from "@/ui/SelectMenu/SelectMenu.props";
import ArrowLeft from "@/assets/svg/ArrowLeft.svg";
import TextArea from "@/ui/TextArea/TextArea";
import {TextAreaType} from "@/ui/TextArea/TextArea.props";
import {LabelSize} from "@/ui/Label/Label.props";
import {options} from "@/utils/consts";
import {AddBotProps} from "@/pages/AddBot/AddBot.props";
import AddForm from "@/components/AddForm/AddForm";

const botSchema = z.object({
    title: z.string().min(3, "Название должно быть минимум 3 символа").nonempty("Название обязательно для заполнения"),
    description: z.string().min(5, "Описание слишком короткое").nonempty("Описание обязательно для заполнения"),
    token: z.string().min(10, "Токен слишком короткий").nonempty("Токен обязательно для заполнения"),
    group_name: z.string().min(3, "Название группы должно быть минимум 3 символа").nonempty("Название группы обязательно для заполнения"),
    answers_type: z.record(string()).optional(),
    nicknames: z.string().nonempty("Имена людей должны быть обязательно"),
});

const AddBot: FC<AddBotProps> = ({}) => {
    const [isSettings, setIsSettings] = useState<boolean>(false);
    const [title, setTitle] = useState<string>("");
    const [file, setFile] = useState<File| null>(null);
    const [description, setDescription] = useState<string>("");
    const [token, setToken] = useState<string>("");
    const [group_name, setGroupName] = useState<string>("");
    const [nicknames, setNickNames] = useState<string>("");
    const [answers_type, setAnswersType] = useState<SingleValue<Option>>(options[0]);
    const [errors, setErrors] = useState<Record<string, string>>({});

    const click = async () => {
        const bot: IBotForm = {title, description, token, group_name, answers_type, nicknames};
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
            await addBot(bot);
            if (file) {
                await UploadFile(file);
            }
            setErrors({});
        } catch (e) {
            setErrors({form: "Ошибка при добавлении бота"});
        }
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
                            <SelectMenu options={options} selected={answers_type} setSelected={setAnswersType}/>
                        </div>
                        <AddForm file={file} setFile={setFile} errors={errors} selected={answers_type} value={nicknames} setValue={setNickNames}/>
                    </div>
                    <div className={"self-start"}>
                        <Button type={ButtonType.Back} onClick={() => setIsSettings(false)}>
                            <ArrowLeft color={"#2b7fff"} width={20} height={20}/>
                        </Button>
                    </div>
                </div>
            }
        </div>)
};

export default AddBot;

