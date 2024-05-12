import { persistStore } from 'redux-persist';
import { configureStore } from '@reduxjs/toolkit';
import createSagaMiddleware from 'redux-saga';
import rootReducer from './modules/rootReducer';
import rootSaga from './modules/rootsagas';
import persistedReducers from './modules/reduxpersist';

const sagamiddleware = createSagaMiddleware();

const store = configureStore({
    reducer: persistedReducers(rootReducer),
    middleware: (getDefaultMiddleware) => {
        // aqui eu adiciono futuros sagas que eu for precisar
        return getDefaultMiddleware({serializableCheck: false}).concat(sagamiddleware)
    }
});

sagamiddleware.run(rootSaga);

export const persistor = persistStore(store);
export default store;
