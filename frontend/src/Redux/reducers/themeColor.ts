const initialThemeState = {
    themeColor: 'light',
  };
  const themeReducer = (state = initialThemeState, action: any) => {
    switch (action.type) {
      case 'SET_THEME_COLOR':
        localStorage.setItem('themeColor', action.payload)
        console.log(action.payload)
        return {
          themeStore: action.payload,
        };
      default:
        return state;
    }
  };
  
  export default themeReducer;