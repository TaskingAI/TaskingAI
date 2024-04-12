import { combineReducers } from 'redux';
import userReducer from './userReducer';
import modelReducer from './model';
import retrievalReducer from './retrieval';
import apikeyReducer from './apikey'
import pluginReducer from './plugin'
import actionReducer from './action'
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
});

export default rootReducer;