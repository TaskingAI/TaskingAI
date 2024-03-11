import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './react-i18next/i18n.js'

import './index.scss'
import { Provider } from 'react-redux';
import store from '../src/Redux/store.ts';
ReactDOM.createRoot(document.getElementById('root')!).render(
  <Provider store={store}>

    <App />
    </Provider>,
)
