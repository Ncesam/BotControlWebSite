import React, {FC, lazy, Suspense, useState} from "react";
import CenterModal from "@/components/Modals/CenterModal/CenterModal";
import {ButtonType} from "@/ui/Button/Button.props";
import Button from "@/ui/Button/Button";
import {PoputProps} from "@/modules/Poput/Poput.props";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import {HexColor} from "@/types/Color";

const EditForm = lazy(() => import("@/components/EditForm/EditForm"));

const Poput: FC<PoputProps> = ({id = 1}) => {
    const [activity, setActivity] = useState<boolean>(false);

    return (
        <div>
            <CenterModal activity={activity} setActivity={setActivity}>
                    <Suspense fallback={<Loading type={LoadingType.Medium} color={HexColor.black}/>}>
                        <EditForm id={id} activity={activity} setActivity={setActivity}/>
                    </Suspense>
            </CenterModal>
            <Button type={ButtonType.Submit} onClick={() => setActivity(true)}>
                 Редактировать бота
            </Button>
        </div>
    );
};

export default Poput;
