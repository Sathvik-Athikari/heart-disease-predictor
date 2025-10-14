import React from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Contact from "./pages/Contact"; 
import About from './pages/About'
import Profile from './pages/Profile'
import Prediction from './pages/Prediction'
import Footer from './components/Footer'
import Login from './pages/Login'
import History from './pages/History';
import SignUp from './pages/SignUp';
import Hero from './pages/Hero';

const App = () => {
  const location = useLocation();

  const hideLayout = location.pathname === "/login" || location.pathname === "/signup" || location.pathname === '/';
  return (
    <div>
        {!hideLayout && <Navbar />}      
        <Routes>
          <Route path="/" element={<Hero />} />
          <Route path='/home' element={<Home/>}/>
          <Route path='/about' element={<About/>}/>
          <Route path='/contact' element={<Contact/>}/>
          <Route path='/profile' element={<Profile/>}/>
          <Route path='/prediction' element={<Prediction/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/history' element={<History/>}/>
          <Route path='/signup' element={<SignUp/>}/>
      </Routes>
      {!hideLayout && <Footer/>}
    </div>
  )
}

export default App