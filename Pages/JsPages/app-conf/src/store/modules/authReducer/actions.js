import * as types from '../types'

export function Login(payload){
    return {
        type: types.LOGIN_REQUEST,
        payload: payload,  
    };
}

export function Loguot(){
    return {
        type: types.LOGOUT,
    };
}

export function LoginFalure(payload){
    return  {
        type: types.LOGIN_FALURE,
        payload: payload,
    };
}

export function LoginSuccess(payload){
    return  {
        type: types.LOGIN_SUCCESS,
        payload: payload,
    };
}

 