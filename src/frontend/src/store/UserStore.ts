import {makeAutoObservable} from "mobx";
import {ILoginUser, IUser} from "@/types/User";

export default class UserStore {
    _isAuth: boolean;
    _user: IUser | null;

    constructor() {
        this._isAuth = false
        this._user = null;
        makeAutoObservable(this)
    }

    setIsAuth(bool: boolean) {
        this._isAuth = bool
    }

    get User() {
        return this._user;
    }
    get isAuth() {
        return this._isAuth
    }

    setUser(user: IUser | null) {
        this._user = user;
    }
}