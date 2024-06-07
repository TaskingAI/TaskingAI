import { BrowserRouter } from 'react-router-dom'
import './App.scss'
import { useSelector, useDispatch } from 'react-redux';
import { useEffect, useState } from 'react';
import { themeColorRedux } from '@/Redux/actions'
import { ConfigProvider, theme } from 'antd'

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import GetRouters from './router/getRouters'
import AuthRouter from './components/authRouter'
function App() {
  const dispatch = useDispatch()
  const { themeStore } = useSelector((state: any) => state.themeColor)
  const [themeColor, setThemeColor] = useState<any>(localStorage.getItem('themeColor') || 'systemColor')
  const darkTheme = {
    algorithm: theme.darkAlgorithm,
    token: {
      colorPrimary: '#099250',
      colorBgContainer: '#1F1F1F',
      colorBorder: '#404040'
    },
    components: {
      Button: {
        defaultColor: 'white',
        defaultBg: '#1F1F1F',
        defaultHoverBg: '#2B2B2B',
        defaultBorderColor: '#404040',
        defaultHoverBorderColor: '#404040',
        defaultHoverColor: 'white',
        primaryShadow: 'none',
        dangerShadow: 'none',
        dangerColor: 'white'
      },
      Input: {
        activeBorderColor: '#099250',
        activeBg: '#2B2B2B',
        activeShadow: 'none',
        hoverBorderColor: '#099250',
        hoverBg: '#2B2B2B'
      },
      InputNumber: {
        activeShadow: 'none'
      },
      Select: {
        optionSelectedBg: 'rgba(14, 195, 108, 0.15)',
        optionSelectedColor: '#8DF7C7'
      },
      Menu: {
        itemSelectedBg: '#20362D',
        itemSelectedColor: '#8DF7C7',
        itemActiveBg: '#20362D'
      },
      Pagination: {
        itemActiveBgDisabled: '#8DF7C7'
      }
    }
  }
  const lightTheme = {
    algorithm: theme.defaultAlgorithm,
    token: {
      colorPrimary: '#099250',
      colorBgContainer: 'white',
      colorBorder: '#e4e4e4',
    },
    components: {
      Button: {
        defaultColor: 'black',
        defaultBg: 'white',
        defaultHoverBg: '#FAFAFA',
        defaultBorderColor: '#E4e4e4',
        defaultHoverBorderColor: '#E4e4e4',
        defaultHoverColor: 'black',
        primaryShadow: 'none',
        dangerShadow: 'none',
        dangerColor: 'white'
      },
      Input: {
        activeBorderColor: '#099250',
        activeBg: '#FAFAFA',
        activeShadow: 'none',
        hoverBorderColor: '#099250',
        hoverBg: '#FAFAFA'
      },
      InputNumber: {
        activeShadow: 'none'
      },
      Select: {
        optionSelectedBg: 'rgba(14, 195, 108, 0.15)',
        optionSelectedColor: '#087443'
      },
      Menu: {
        itemSelectedBg: '#f3f8f6',
        itemSelectedColor: '#087443',
        itemActiveBg: '#f3f8f6'
      },
      Pagination: {
        itemActiveBgDisabled: '#087443'
      }
    }
  }
  useEffect(() => {
    if (themeColor !== themeStore) {
      dispatch(themeColorRedux(themeColor) as any)
    }
  }, [])
  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light-theme', 'dark-theme', 'systemColor-theme');
    if (themeStore === 'dark') {
      root.classList.add('dark-theme');
      setThemeColor(darkTheme)

    } else if (themeStore === 'light') {
      root.classList.add('light-theme');
      setThemeColor(lightTheme)
    } else {
      const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (isDarkMode) {
        root.classList.add('dark-theme');
        setThemeColor(darkTheme)
      } else {
        root.classList.add('light-theme');
        setThemeColor(lightTheme)
      }

    }
  }, [themeStore])
  return (
    <>
      <ConfigProvider theme={themeColor}>
        <BrowserRouter>
          <AuthRouter>
            <GetRouters />
          </AuthRouter>
          <ToastContainer autoClose={2000} className="custom-toast-container" />
        </BrowserRouter>
      </ConfigProvider>

    </>

  )
}

export default App
