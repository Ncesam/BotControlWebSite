import React from "react";
import type {FC} from "react";
import {Option, SelectMenuProps} from "./SelectMenu.props";
import Select, {OnChangeValue} from "react-select";

const SelectMenu: FC<SelectMenuProps> = ({options, selected ,setSelected}) => {
    return (
        <Select
            options={options}
            className={"w-full"}
            isClearable
            defaultValue={options[0]}
            value={selected}
            onChange={(newValue: OnChangeValue<Option, false>) =>
                setSelected(newValue)
            }
            placeholder={"Выбери тип"}
        />
    );
};

export default SelectMenu;

