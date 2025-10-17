// src/App.jsx
import React from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Profile from "./pages/Profile";
import Prediction from "./pages/Prediction";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Hero from "./pages/Hero";

import ProtectedRoute from "./components/ProtectedRoute";

const LayoutWrapper = ({ children }) => {
  const location = useLocation();
  const hideLayout =
    location.pathname === "/login" ||
    location.pathname === "/signup" ||
    location.pathname === "/";

  return (
    <div className="flex flex-col min-h-screen">
      <AnimatePresence mode="wait">
        {!hideLayout && (
          <motion.div key="navbar" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Navbar />
          </motion.div>
        )}
      </AnimatePresence>

      <main className="flex-grow">
        <AnimatePresence mode="wait">
          <motion.div key={location.pathname} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            {children}
          </motion.div>
        </AnimatePresence>
      </main>

      <AnimatePresence mode="wait">
        {!hideLayout && (
          <motion.div key="footer" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Footer />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const App = () => (
  <LayoutWrapper>
    <Routes>
      <Route path="/" element={<Hero />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/login" element={<Login />} />

      <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/prediction" element={<ProtectedRoute><Prediction /></ProtectedRoute>} />
      <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      <Route path="/about" element={<ProtectedRoute><About /></ProtectedRoute>} />
      <Route path="/contact" element={<ProtectedRoute><Contact /></ProtectedRoute>} />
    </Routes>
  </LayoutWrapper>
);

export default App;
