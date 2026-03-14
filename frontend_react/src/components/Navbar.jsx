import React from 'react';
import { ShoppingCart, Leaf, Home, MessageSquare, Phone } from 'lucide-react';

const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50 border-b border-calm-green-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          <div className="flex items-center gap-2 cursor-pointer">
            <div className="bg-calm-green-600 p-2 rounded-xl">
              <Leaf className="h-6 w-6 text-white" />
            </div>
            <span className="text-2xl font-black tracking-tight text-calm-green-900">Agri<span className="text-calm-green-600">AI</span></span>
          </div>
          
          {/* Desktop Nav */}
          <div className="hidden md:flex space-x-10 items-center">
            <a href="#" className="flex items-center text-sm font-semibold text-gray-600 hover:text-calm-green-600 transition-all">Home</a>
            <a href="#" className="flex items-center text-sm font-semibold text-gray-600 hover:text-calm-green-600 transition-all">Marketplace</a>
            <a href="#" className="flex items-center text-sm font-semibold text-gray-600 hover:text-calm-green-600 transition-all">Community</a>
            <a href="#" className="flex items-center text-sm font-semibold text-gray-600 hover:text-calm-green-600 transition-all">Advisor</a>
            <button className="bg-calm-green-600 text-white px-6 py-2.5 rounded-full text-sm font-bold hover:bg-calm-green-700 hover:shadow-lg transition-all active:scale-95">
              Get Started
            </button>
          </div>

          {/* Mobile Toggle */}
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="md:hidden text-gray-600">
             <div className="space-y-1.5">
               <div className="w-6 h-0.5 bg-gray-600"></div>
               <div className="w-6 h-0.5 bg-gray-600"></div>
               <div className="w-6 h-0.5 bg-gray-600"></div>
             </div>
          </button>
        </div>
      </div>
      
      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 p-4 space-y-4 shadow-xl animate-in slide-in-from-top duration-300">
          <a href="#" className="block text-lg font-medium text-gray-800">Home</a>
          <a href="#" className="block text-lg font-medium text-gray-800">Marketplace</a>
          <a href="#" className="block text-lg font-medium text-gray-800">Community</a>
          <a href="#" className="block text-lg font-medium text-gray-800">Advisor</a>
          <button className="w-full bg-calm-green-600 text-white py-3 rounded-xl font-bold">Get Started</button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
