import React, { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const navigate = useNavigate();

  // State for profile image preview
  const [profileImage, setProfileImage] = useState("/default-avatar.png"); // fallback image

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-red-50 px-6 py-10 pt-24">
      {/* Heading */}
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-4xl font-bold text-center text-blue-600 mb-8"
      >
        Patient Profile
      </motion.h1>

      {/* Profile Section */}
      <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8">
        {/* Profile Image */}
        <div className="flex flex-col items-center mb-6">
          <img
            src={profileImage}
            alt="Profile"
            className="w-32 h-32 rounded-full object-cover border-4 border-blue-500 shadow-md"
          />
          <label className="mt-4 cursor-pointer text-blue-600 hover:underline">
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleImageUpload}
            />
            Upload New Photo
          </label>
        </div>

        {/* Basic Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Name
            </label>
            <input
              type="text"
              defaultValue="John Doe"
              className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              defaultValue="johndoe@email.com"
              className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Phone Number
            </label>
            <input
              type="tel"
              defaultValue="+91 9876543210"
              className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Predictions Taken
            </label>
            <input
              type="number"
              value={5}
              readOnly
              className="mt-1 block w-full rounded-lg border px-3 py-2 bg-gray-100 shadow-sm"
            />
          </div>
        </div>

        {/* Extra Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Age
            </label>
            <input
              type="number"
              defaultValue="28"
              className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Sex
            </label>
            <select className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500">
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Marital Status
            </label>
            <select className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500">
              <option>Single</option>
              <option>Married</option>
              <option>Divorced</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Occupation
            </label>
            <input
              type="text"
              defaultValue="Software Engineer"
              className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* History Button */}
        <div className="mt-8 flex justify-center">
          <button
            onClick={() => navigate("/history")}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg shadow-md hover:bg-blue-700 transition"
          >
            View History
          </button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
