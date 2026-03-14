import React from 'react';

const Hero = () => {
  return (
    <div className="bg-calm-green-50 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto text-center">
        <h1 className="text-4xl font-extrabold text-calm-green-900 sm:text-5xl md:text-6xl">
          Empowering Farmers with <span className="text-calm-green-600">Smart Technology</span>
        </h1>
        <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-600">
          Everything you need for your fields, from high-quality seeds to AI-powered crop advice.
        </p>
        <div className="mt-10 flex justify-center gap-4">
          <button className="bg-calm-green-600 text-white px-8 py-3 rounded-full font-bold hover:bg-calm-green-700 transition shadow-lg">
            Shop Tools & Fertilizer
          </button>
          <button className="border-2 border-calm-green-600 text-calm-green-700 px-8 py-3 rounded-full font-bold hover:bg-calm-green-50 transition">
            Get Yield Forecast
          </button>
        </div>
      </div>
    </div>
  );
};

export default Hero;
