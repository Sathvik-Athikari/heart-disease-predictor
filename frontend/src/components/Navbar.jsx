import React from "react";
import { User } from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem("token"));
  const username = localStorage.getItem("username") || "User";

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    navigate("/login", { replace: true });
  };

  const handleLogin = () => {
    navigate("/login", { replace: true });
  };

  return (
    <nav className="px-8 py-4 flex justify-between items-center fixed top-0 left-0 w-full z-50 bg-white/50 backdrop-blur-md shadow-md">
      {/* Left side - Brand */}
      <div
        className="flex items-center gap-2 text-2xl font-bold text-blue-600 cursor-pointer"
        onClick={() => navigate("/home")}
      >
        <img src="/logo.png" alt="logo" className="w-[50px] h-[50px]" />
        <h1>CardioPredict</h1>
      </div>

      {/* Right side - Menu */}
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

        {/* Profile / Login Dropdown */}
        <div className="relative group">
          <div className="flex items-center gap-2 cursor-pointer text-gray-700 hover:text-blue-600">
            <User size={22} />
            <span>{isLoggedIn ? username : "Account"}</span>
          </div>

          {/* Dropdown Menu */}
          <div className="absolute right-0 mt-2 w-40 bg-white shadow-lg rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
            {isLoggedIn ? (
              <>
                <NavLink
                  to="/profile"
                  className="block px-4 py-2 text-blue-700 hover:bg-red-400 hover:text-gray-100"
                >
                  My Profile
                </NavLink>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-blue-700 hover:bg-red-400 hover:text-gray-100"
                >
                  Logout
                </button>
              </>
            ) : (
              <button
                onClick={handleLogin}
                className="w-full text-left px-4 py-2 text-blue-700 hover:bg-red-400 hover:text-gray-100"
              >
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
