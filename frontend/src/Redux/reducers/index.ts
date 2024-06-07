import { combineReducers } from 'redux';
import userReducer from './userReducer';
import modelReducer from './model';
import retrievalReducer from './retrieval';
import apikeyReducer from './apikey'
import pluginReducer from './plugin'
import actionReducer from './action'
import {playgroundModelReducer} from './playground'
import themeReducer from './themeColor'

import { playgroundTypeReducer,assistantIdReducer,modelIdReducer} from './space'
const rootReducer = combineReducers({
    user: userReducer,
    model: modelReducer,
    retrieval: retrievalReducer,
    apikey: apikeyReducer,
    plugin: pluginReducer,
    action: actionReducer,
    playgroundType: playgroundTypeReducer,
    assistantId: assistantIdReducer,
    modelId: modelIdReducer,
    playgroundModelRedux: playgroundModelReducer,
    themeColor:themeReducer,
});

export default rootReducer;