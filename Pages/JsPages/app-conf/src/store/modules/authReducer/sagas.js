import { call, put, all, takeLatest } from 'redux-saga/effects';
import * as actions from './actions';
import * as types from '../types';
import axios from '../../../services/axios';

function* Login({payload}) {
    try{
        const response = yield call(axios.post, "/token/", payload);
        const token = response.token
        axios.defaults.headers.Authorization = `Bearer ${token}`;
        yield put(actions.LoginSuccess({ ...response.data }));
    }catch(err) {
        yield put(actions.LoginFalure());
    }
}

export default all([
    takeLatest(types.LOGIN_REQUEST, Login),
]);
    