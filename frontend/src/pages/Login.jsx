import { NavLink, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const Login = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-red-50 px-4">
      {/* Animated Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8, y: 50 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        whileHover={{ scale: 1.03 }}
        className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md"
      >
        {/* Heading */}
        <motion.h2
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="text-3xl font-bold text-center text-blue-600 mb-6"
        >
          Welcome Back
        </motion.h2>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="text-center text-gray-500 mb-8"
        >
          Please login to continue to{" "}
          <span className="text-red-500 font-semibold">CardioPredict</span>
        </motion.p>

        {/* Form */}
        <motion.form
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="space-y-5"
        >
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <motion.input
              whileFocus={{ scale: 1.02, borderColor: "#2563eb" }}
              type="email"
              placeholder="Enter your email"
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <motion.input
              whileFocus={{ scale: 1.02, borderColor: "#2563eb" }}
              type="password"
              placeholder="Enter your password"
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
            />
          </div>

          {/* Login Button */}
          <motion.button
            onClick={() => navigate('/home')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg shadow-md hover:bg-blue-700 transition"
          >
            Login
          </motion.button>
        </motion.form>

        {/* Extra Options */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="mt-6 flex justify-between text-sm"
        >
          <NavLink to="/forgot-password" className="text-blue-500 hover:underline">
            Forgot Password?
          </NavLink>
          <NavLink to="/signup" className="text-blue-500 hover:underline">
            Create Account
          </NavLink>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Login;
