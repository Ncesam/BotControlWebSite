import {makeAutoObservable} from "mobx";
import {IBot} from "@/types/Bots";

export default class BotsStore {
    _bots: IBot[] | undefined | null = null;

    constructor() {
        makeAutoObservable(this);
    }

    setBots(bots: IBot[] | null | undefined) {
        this._bots = bots;
    }

    get bots() {
        return this._bots;
    }
}