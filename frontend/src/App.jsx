function App() {
  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-green-700">
              WasteAI
            </h1>

            <p className="text-sm text-gray-500">
              Smart Waste Segregation System
            </p>
          </div>

          <nav className="flex gap-6 text-gray-700 font-medium">
            <a href="#home" className="hover:text-green-600">
              Home
            </a>

            <a href="#features" className="hover:text-green-600">
              Features
            </a>

            <a href="#about" className="hover:text-green-600">
              About
            </a>
          </nav>
        </div>
      </header>

      <main>
        <section
          id="home"
          className="max-w-6xl mx-auto px-6 py-24 text-center"
        >
          <span className="inline-block px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
            AI + Waste Management
          </span>

          <h2 className="mt-6 text-5xl font-bold text-gray-900 leading-tight">
            AI-Based Waste Segregation
            <span className="block text-green-600">
              & Microbial Decomposition
            </span>
          </h2>

          <p className="mt-6 max-w-3xl mx-auto text-lg text-gray-600">
            Upload a waste image and let our AI identify its category.
            For biodegradable waste, the system also provides
            evidence-backed microbial decomposition recommendations.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <button
              type="button"
              className="px-7 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition"
            >
              Upload Waste Image
            </button>

            <button
              type="button"
              className="px-7 py-3 bg-white text-gray-700 border border-gray-300 rounded-xl font-semibold hover:bg-gray-50 transition"
            >
              View History
            </button>
          </div>
        </section>

        <section
          id="features"
          className="max-w-6xl mx-auto px-6 pb-24"
        >
          <h3 className="text-3xl font-bold text-center text-gray-900">
            System Features
          </h3>

          <div className="grid md:grid-cols-3 gap-6 mt-10">
            <div className="bg-white p-7 rounded-2xl shadow-sm">
              <div className="text-4xl">🤖</div>

              <h4 className="mt-4 text-xl font-bold text-gray-900">
                AI Classification
              </h4>

              <p className="mt-3 text-gray-600">
                Classifies waste into biodegradable, plastic, paper,
                glass, metal and e-waste categories.
              </p>
            </div>

            <div className="bg-white p-7 rounded-2xl shadow-sm">
              <div className="text-4xl">🦠</div>

              <h4 className="mt-4 text-xl font-bold text-gray-900">
                Microbial Decomposition
              </h4>

              <p className="mt-3 text-gray-600">
                Provides microbial decomposition information for
                supported biodegradable waste types.
              </p>
            </div>

            <div className="bg-white p-7 rounded-2xl shadow-sm">
              <div className="text-4xl">📊</div>

              <h4 className="mt-4 text-xl font-bold text-gray-900">
                Prediction History
              </h4>

              <p className="mt-3 text-gray-600">
                Stores predictions and user feedback for future
                analysis and model improvement.
              </p>
            </div>
          </div>
        </section>

        <section
          id="about"
          className="bg-green-700 text-white"
        >
          <div className="max-w-4xl mx-auto px-6 py-16 text-center">
            <h3 className="text-3xl font-bold">
              Sustainable Waste Management Using AI
            </h3>

            <p className="mt-4 text-green-100">
              This project combines computer vision, FastAPI,
              PostgreSQL and React to build an intelligent waste
              segregation and decomposition recommendation system.
            </p>
          </div>
        </section>
      </main>

      <footer className="bg-gray-900 text-gray-400 text-center py-6">
        <p>
          AI-Based Waste Segregation & Microbial Decomposition System
        </p>
      </footer>
    </div>
  )
}

export default App