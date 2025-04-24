import { FC } from "react"
import { CheckBoxFormProps } from "./CheckBox.props"


const CheckBox: FC<CheckBoxFormProps> = ({ disabled, placeholder, setValue, value }) => {
    return (
        <label className="inline-flex select-none items-center cursor-pointer">
            <input
                type="checkbox"
                className="hidden"
                checked={value}
                onChange={() => setValue()}
            />
            <span className="relative">
                <span className={`block h-4 lg:h-6 w-6 lg:w-10 rounded-full transition-colors duration-200 ${value ? 'bg-blue-500' : 'bg-gray-400'
                    }`}></span>
                <span className={`absolute left-1 top-1 h-2 lg:h-4 w-2 lg:w-4 rounded-full bg-white transition-transform duration-200 ${value ? 'translate-x-2 lg:translate-x-4' : ''
                    }`}></span>
            </span>
            <span className="ml-2 text-sm">{placeholder}</span>
        </label>
    )
}

export default CheckBox;