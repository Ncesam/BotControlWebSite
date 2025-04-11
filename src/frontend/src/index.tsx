import React, {createContext} from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./index.css";
import UserStore from "@/store/UserStore";
import BotsStore from "@/store/BotsStore";

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);

export const Context = createContext<{ user: UserStore; bots: BotsStore } | undefined>(undefined);

root.render(
    <Context.Provider value={{
        user: new UserStore(),
        bots: new BotsStore()
    }}>
        <App/>
    </Context.Provider>
);


