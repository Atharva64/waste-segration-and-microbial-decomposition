import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import Navbar from './components/Navbar'
import DecompositionInfo from './pages/DecompositionInfo'
import Predict from './pages/Predict'
import WasteGuide from './pages/WasteGuide'

function App() {
  return (
    <BrowserRouter>
      <Navbar />

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
          path="*"
          element={<Navigate to="/predict" replace />}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
