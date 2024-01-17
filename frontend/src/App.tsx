// import { useState } from 'react'
import { BrowserRouter } from 'react-router-dom'
import './App.scss'
import { ToastContainer } from 'react-toastify';
import GetRouters from './router/getRouters'
import AuthRouter from './components/authRouter'
function App() {
 
  return (
    <>
      <BrowserRouter>
        <AuthRouter>
            <GetRouters/>
        </AuthRouter>
        <ToastContainer autoClose={2000} />
      </BrowserRouter>
    </>

  )
}

export default App
