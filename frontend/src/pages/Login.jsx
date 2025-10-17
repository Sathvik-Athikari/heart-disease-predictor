import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      console.log("🔹 Login Response:", data);

      if (res.ok && data.message === "Login successful") {
        localStorage.setItem("token", data.token || "dummy-token");
        localStorage.setItem("username", data.username || email);
        // ✅ Navigate after a short delay to ensure React Router is ready
        setTimeout(() => navigate("/home", { replace: true }), 300);
      } else {
        setError(data.error || "Invalid credentials");
      }
    } catch (err) {
      console.error(err);
      setError("Server error. Please try again later.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-red-50 px-4">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-blue-600 mb-6">
          Welcome Back
        </h2>

        <p className="text-center text-gray-500 mb-8">
          Please login to continue to{" "}
          <span className="text-red-500 font-semibold">CardioPredict</span>
        </p>

        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full mt-2 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition"
              required
            />
          </div>

          {error && (
            <p className="text-center text-sm text-red-500">{error}</p>
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg shadow-md hover:bg-blue-700 transition"
          >
            Login
          </button>
        </form>

        <div className="mt-6 flex justify-between text-sm">
          <NavLink to="/forgot-password" className="text-blue-500 hover:underline">
            Forgot Password?
          </NavLink>
          <NavLink to="/signup" className="text-blue-500 hover:underline">
            Create Account
          </NavLink>
        </div>
      </div>
    </div>
  );
};

export default Login;
