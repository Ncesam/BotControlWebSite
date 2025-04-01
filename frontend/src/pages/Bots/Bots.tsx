import {FC, useContext, useEffect, useState} from "react";
import {BotsProps} from "./Bots.props";
import {Context} from "@/index";
import BotsCardList from "@/modules/BotsCardList/BotsCardList";
import {Color, HexColor} from "@/types/Color";
import {getBots} from "@/http/BotsAPI";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import Poput from "@/modules/Poput/Poput";
import {PoputType} from "@/modules/Poput/Poput.props";

const Bots: FC<BotsProps> = ({}) => {
    const context = useContext(Context);
    const [isLoading, setIsLoading] = useState<boolean>(false)
    useEffect(() => {
        let isMounted = true; // Флаг для предотвращения обновления размонтированного компонента

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

    return (
        <div className={"flex flex-1 items-start justify-start"}>
            {isLoading
                ? <div className={"fixed center"}>
                    <Loading type={LoadingType.Medium} color={HexColor.blue}/>
                </div>
                :
                <div className="flex w-full flex-col gap-2 items-center">
                    <BotsCardList bots={context?.bots.bots}/>
                    <div className={"fixed bottom-5"}>
                        <Poput type={PoputType.AddBot}/>
                    </div>
                </div>
            }
        </div>
    );

}

export default Bots;

