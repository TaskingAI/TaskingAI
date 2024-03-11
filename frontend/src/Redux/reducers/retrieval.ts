const initialState = {
  loading: false,
  retrievalLists: { data: [] },
  loaded: false,
  error: '',
};

const retrievalReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case 'FETCH_RETRIEVAL_REQUEST':
      return {
        ...state,
        loading: true,
      };
    case 'FETCH_RETRIEVAL_SUCCESS':
      return {
        loading: false,
        loaded: true,
        retrievalLists: action.payload,
        error: '',
      };
    case 'FETCH_RETRIEVAL_FAILURE':
      return {
        loading: false,
        retrievalLists: { data: [] },
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

export default retrievalReducer;
