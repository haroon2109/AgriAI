import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Marketplace from './components/Marketplace'
import Chatbot from './components/Chatbot'
import YieldMap from './components/YieldMap'

function App() {
  return (
    <div className="min-h-screen bg-calm-green-50">
      <Navbar />
      <Hero />
      <Marketplace />
      
      {/* Yield Map Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">Satellite Yield Forecast</h2>
          <p className="text-gray-600 mb-8">View real-time Sentinel-2 health indices for your district.</p>
          <div className="h-[400px] w-full bg-gray-100 rounded-2xl overflow-hidden">
            <YieldMap />
          </div>
        </div>
      </section>

      <Chatbot />

      <footer className="bg-white py-12 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-500 text-sm">
          © 2026 AgriAI - Empowering Farmers in Tamil Nadu.
        </div>
      </footer>
    </div>
  )
}

export default App
