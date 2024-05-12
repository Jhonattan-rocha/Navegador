import {all} from 'redux-saga/effects';

import LoginSagas from './authReducer/sagas';

export default function* rootSaga(){
    return yield all([LoginSagas]);
}
