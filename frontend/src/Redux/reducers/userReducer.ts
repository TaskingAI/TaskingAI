const initialState = {
  loading: false,
  users: { data: [] },
  loaded: false,
  error: '',
};

const userReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case 'FETCH_ASSISTANT_REQUEST':
      return {
        ...state,
        loading: true,
      };
    case 'FETCH_ASSISTANT_SUCCESS':
      return {
        loading: false,
        loaded: true,
        users: action.payload,
        error: '',
      };
    case 'FETCH_ASSISTANT_FAILURE':
      return {
        loading: false,
        users: { data: [] },
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

export default userReducer;
