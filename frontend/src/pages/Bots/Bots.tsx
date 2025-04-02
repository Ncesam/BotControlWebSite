import {FC, useContext, useEffect, useState} from "react";
import {BotsProps} from "./Bots.props";
import {Context} from "@/index";
import BotsCardList from "@/modules/BotsCardList/BotsCardList";
import {HexColor} from "@/types/Color";
import {getBots} from "@/http/BotsAPI";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import Button, {ButtonType} from "@/ui/Button/Button";
import {ADD_BOT_ROUTE} from "@/utils/consts";
import {useNavigate} from "react-router-dom";

const Bots: FC<BotsProps> = ({}) => {
    const context = useContext(Context);
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        let isMounted = true;

        const fetchBots = async () => {
            setIsLoading(true);
            try {
                const bots = await getBots();
                if (isMounted) {
                    context?.bots.setBots(bots);
                }
            } catch (error) {
                console.error("Ошибка загрузки ботов:", error);
            } finally {
                if (isMounted) {
                    setIsLoading(false);
                }
            }
        };

        fetchBots();
        const interval = setInterval(fetchBots, 1000 * 60);

        return () => {
            isMounted = false;
            clearInterval(interval);
        };
    }, [context?.bots]);

    return isLoading ? (
        <div className={"items-center justify-center flex"}>
            <Loading type={LoadingType.Medium} color={HexColor.blue} />
        </div>
    ) : (
        <div className={"w-full"}>
            <div className={"flex flex-1 items-start justify-start"}>
                <div className="flex w-full flex-col gap-2 items-center">
                    <BotsCardList bots={context?.bots.bots} />
                    <div className={"fixed bottom-5"}>
                        <Button type={ButtonType.Submit} onClick={() => navigate(ADD_BOT_ROUTE)}>Добавить Бота</Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Bots;