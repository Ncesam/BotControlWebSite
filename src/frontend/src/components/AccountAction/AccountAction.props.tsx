export interface AccountActionProps {
    type?: AccountActionType;
}

enum AccountActionType {
    Unlogged = 0,
    Logged = 1,
}

export {AccountActionType};