import React from 'react'
import { User } from "lucide-react"; // profile icon
import { NavLink, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <nav className="px-8 py-4 flex justify-between items-center fixed top-0 left-0 w-full z-50 bg-white/50 backdrop-blur-md shadow-md">
      
      {/* Left side - Brand */}
      <div className="flex items-center gap-2 text-2xl font-bold text-blue-600">
        <img src="/logo.png" alt="logo" className="w-[50px] h-[50px]" />
        <h1>CardioPredict</h1>
      </div>

      {/* Right side - menu */}
       <div className="flex items-center space-x-8">
        <NavLink
          to="/home"
          className={({ isActive }) =>
            isActive ? "text-blue-600 font-medium" : "text-gray-700 hover:text-blue-600"
          }
        >
          Home
        </NavLink>

        <NavLink
          to="/about"
          className={({ isActive }) =>
            isActive ? "text-blue-600 font-medium" : "text-gray-700 hover:text-blue-600"
          }
        >
          About
        </NavLink>

        <NavLink
          to="/contact"
          className={({ isActive }) =>
            isActive ? "text-blue-600 font-medium" : "text-gray-700 hover:text-blue-600"
          }
        >
          Contact
        </NavLink>

        <NavLink
          to="/prediction"
          className={({ isActive }) =>
            isActive ? "text-blue-600 font-medium" : "text-gray-700 hover:text-blue-600"
          }
        >
          Prediction
        </NavLink>

         <div className="relative group">
          <User size={22}/>

          {/* Dropdown Menu */}
          <div className="absolute right-0 mt-2 w-40 bg-white shadow-lg rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
            <NavLink
              to="/profile"
              className="block px-4 py-2 text-blue-700 hover:bg-red-400 hover:text-gray-100"
            >
              My Profile
            </NavLink>
            <NavLink
              to="/history"
              className="block px-4 py-2 text-blue-700 hover:bg-red-400 hover:text-gray-100"
            >
              History
            </NavLink>
            <button
              onClick={() => navigate('/login')}
              className="w-full text-left px-4 py-2 text-blue-700 hover:bg-red-400 hover:text-gray-100"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar