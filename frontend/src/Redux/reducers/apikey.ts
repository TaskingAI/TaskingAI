const initialState = {
  loading: false,
  apiKeyLists: { data: [] },
  loaded: false,
  error: '',
};

const apikeyReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case 'FETCH_APIKEY_REQUEST':
      return {
        ...state,
        loading: true,
      };
    case 'FETCH_APIKEY_SUCCESS':
      return {
        loading: false,
        loaded: true,
        apiKeyLists: action.payload,
        error: '',
      };
    case 'FETCH_APIKEY_FAILURE':
      return {
        loading: false,
        apiKeyLists: { data: [] },
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

export default apikeyReducer;
