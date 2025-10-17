import { NavLink, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useState } from "react";
import axios from "axios";

const Signup = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    phone: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/signup", form);
      setMessage(response.data.message || "Signup successful!");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setMessage(err.response?.data?.error || "Signup failed. Try again.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-blue-50 px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.8, y: 50 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        whileHover={{ scale: 1.03 }}
        className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md"
      >
        <motion.h2
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="text-3xl font-bold text-center text-blue-600 mb-6"
        >
          Create Account
        </motion.h2>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="text-center text-gray-500 mb-8"
        >
          Join <span className="text-red-500 font-semibold">CardioPredict</span> and take charge of your heart health ❤️
        </motion.p>

        <motion.form
          onSubmit={handleSignup}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="space-y-5"
        >
          <div>
            <label className="block text-sm font-medium text-gray-700">Username</label>
            <motion.input
              whileFocus={{ scale: 1.02, borderColor: "#2563eb" }}
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder="Enter your username"
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Phone Number</label>
            <motion.input
              whileFocus={{ scale: 1.02, borderColor: "#2563eb" }}
              type="tel"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              placeholder="Enter your phone number"
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <motion.input
              whileFocus={{ scale: 1.02, borderColor: "#2563eb" }}
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="Enter your email"
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <motion.input
              whileFocus={{ scale: 1.02, borderColor: "#2563eb" }}
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter your password"
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
            />
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg shadow-md hover:bg-blue-700 transition"
          >
            Sign Up
          </motion.button>
        </motion.form>

        {message && <p className="text-center text-sm mt-3 text-blue-600">{message}</p>}

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="mt-6 text-center text-sm"
        >
          <span className="text-gray-600">Already have an account? </span>
          <NavLink to="/login" className="text-blue-500 hover:underline">
            Login
          </NavLink>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Signup;
