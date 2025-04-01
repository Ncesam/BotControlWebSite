import React, {FC, lazy, Suspense, useState} from "react";
import CenterModal from "@/components/Modals/CenterModal/CenterModal";
import {ButtonType} from "@/ui/Button/Button.props";
import Button from "@/ui/Button/Button";
import {PoputProps, PoputType} from "@/modules/Poput/Poput.props";
import Loading from "@/ui/Loading/Loading";
import {LoadingType} from "@/types/Loading";
import {HexColor} from "@/types/Color";

const EditForm = lazy(() => import("@/components/EditForm/EditForm"));
const AddForm = lazy(() => import("@/components/AddForm/AddForm"));

const Poput: FC<PoputProps> = ({type, id = 1}) => {
    const [activity, setActivity] = useState<boolean>(false);

    return (
        <div>
            <CenterModal activity={activity} setActivity={setActivity}>
                {type === PoputType.AddBot ? (
                    <Suspense fallback={<Loading type={LoadingType.Medium} color={HexColor.black}/>}>
                        <AddForm activity={activity} setActivity={setActivity}/>
                    </Suspense>
                ) : type === PoputType.EditBot ? (
                    <Suspense fallback={<Loading type={LoadingType.Medium} color={HexColor.black}/>}>
                        <EditForm id={id} activity={activity} setActivity={setActivity}/>
                    </Suspense>
                ) : null}
            </CenterModal>

            <Button type={ButtonType.Submit} onClick={() => setActivity(true)}>
                {type === PoputType.AddBot ? "Добавить бота" : "Редактировать бота"}
            </Button>
        </div>
    );
};

export default Poput;
