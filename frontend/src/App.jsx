import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import ErrorBoundary from './components/ErrorBoundary'
import Navbar from './components/Navbar'
import Analytics from './pages/Analytics'
import DecompositionInfo from './pages/DecompositionInfo'
import Predict from './pages/Predict'
import WasteGuide from './pages/WasteGuide'

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <ErrorBoundary>
      <Routes>
        <Route
          path="/"
          element={<Navigate to="/predict" replace />}
        />

        <Route
          path="/predict"
          element={<Predict />}
        />

        <Route
          path="/guide"
          element={<WasteGuide />}
        />

        <Route
          path="/decomposition"
          element={<DecompositionInfo />}
        />

        <Route
          path="/analytics"
          element={<Analytics />}
        />

        <Route
          path="*"
          element={<Navigate to="/predict" replace />}
        />
      </Routes>
      </ErrorBoundary>
    </BrowserRouter>
  )
}

export default App
