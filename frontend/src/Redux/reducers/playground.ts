const initialPlaygroundModelState = {
    temperatureRedux: false,
    maxTokenRedux: false,
    topPValueRedux: false,
    topKValueRedux: false,
    stopSequenceValueRedux: false,
 }
 const playgroundModelReducer = (state = initialPlaygroundModelState, action: any) => {
   switch (action.type) {
     case 'TEMPERATURE_DATA':
       return {
         ...state,
         temperatureRedux: action.payload,
       };
     case 'MAX_TOKEN_DATA':
       return {
         ...state,
         maxTokenRedux: action.payload,
       };
     case 'TOP_P_DATA':
       return {
         ...state,
         topPValueRedux: action.payload,
       };
     case 'TOP_K_DATA':
       return {
         ...state,
         topKValueRedux: action.payload,
       };
     case 'STOP_SEQUENCES_DATA':
       return {
         ...state,
         stopSequenceValueRedux: action.payload,
       };
     default:
       return state;
   }
 
 }
 export {playgroundModelReducer}