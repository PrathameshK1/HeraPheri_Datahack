import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { MyContextProvider } from './contexts/MyContext.jsx'

createRoot(document.getElementById('root')).render(
  <MyContextProvider>
    <App />
  </MyContextProvider>
)
