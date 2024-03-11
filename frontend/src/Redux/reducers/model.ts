const initialState = {
  loading: false,
  modelLists: { data: [] },
  loaded: false,
  error: '',
};

const modelReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case 'FETCH_MODEL_REQUEST':
      return {
        ...state,
        loading: true,
      };
    case 'FETCH_MODEL_SUCCESS':
      return {
        loading: false,
        loaded: true,
        modelLists: action.payload,
        error: '',
      };
    case 'FETCH_MODEL_FAILURE':
      return {
        loading: false,
        modelLists: { data: [] },
        error: action.payload,
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
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

export default modelReducer;
