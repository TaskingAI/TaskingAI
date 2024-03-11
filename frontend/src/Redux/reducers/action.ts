const initialState = {
  loading: false,
  actionLists: { data: [] },
  loaded: false,
  error: '',
};

const actionReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case 'FETCH_ACTION_REQUEST':
      return {
        ...state,
        loading: true,
      };
    case 'FETCH_ACTION_SUCCESS':
      return {
        loading: false,
        loaded: true,
        actionLists: action.payload,
        error: '',
      };
    case 'FETCH_ACTION_FAILURE':
      return {
        loading: false,
        actionLists: { data: [] },
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

export default actionReducer;
