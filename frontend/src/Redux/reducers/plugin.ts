const initialState = {
    loading: false,
    pluginLists: {data:[]},
    loaded: false,
    error: '',
  };
  
  const pluginReducer = (state = initialState, action:any) => {
    switch (action.type) {
      case 'FETCH_PLUGIN_REQUEST':
        return {
          ...state,
          loading: true,
        };
      case 'FETCH_PLUGIN_SUCCESS':
        return {
          loading: false,
          loaded: true, 
          pluginLists: action.payload,
          error: '',
        };
      case 'FETCH_PLUGIN_FAILURE':
        return {
          loading: false,
          pluginLists: {data:[]},
          error: action.payload,
        };
        case 'SET_LOADED':
      return {
        ...state,
        loaded: action.payload,
      };
      default:
        return state;
    }
  };
  
  export default pluginReducer;
  