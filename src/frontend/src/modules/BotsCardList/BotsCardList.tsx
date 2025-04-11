import {FC, useState} from "react";
import {BotsCardListProps} from "./BotsCardList.props";
import Card from "@/components/Card/Card";
import SortingLabel from "@/ui/SortingLabel/SortingLabel";

const BotsCardList: FC<BotsCardListProps> = ({ bots }) => {
    const [isAscending, setIsAscending] = useState<boolean>(true);
    const sortedBots = bots?.sort((a, b) => (isAscending ? a.id - b.id : b.id - a.id));

    return (
        <div className="w-full flex flex-col flex-grow lg:h-[calc(3*200px+50px)]">
            {sortedBots && sortedBots.length > 0 ? (
                <>
                    {/* Sorting header */}
                    <div className="flex w-full items-start">
                        <SortingLabel isAscending={isAscending} setIsAscending={setIsAscending} />
                    </div>

                    {/* Bots grid */}
                    <div className="w-full scrollbar-hidden">
                        <div className="grid grid-cols-1 sm:grid-cols-2 m-2 md:grid-cols-3 lg:grid-cols-4 gap-2 lg:gap-4 lg:max-h-[650px] overflow-y-auto scrollbar-hidden">
                            {sortedBots.map((bot) => (
                                <Card card={bot} key={bot.id ?? bot.title} />
                            ))}
                        </div>
                    </div>
                </>
            ) : (
                <div className="bg-gray-600 rounded-md p-6 text-white font-bold text-lg m-8">
                    Ты не имеешь ботов
                </div>
            )}
        </div>
    );
};

export default BotsCardList;