import { useEffect, useState } from 'react'
import ImageUpload from '../components/ImageUpload'
import WebcamCapture from '../components/WebcamCapture'
import Results from './Results'

const MAX_FILE_SIZE = 10 * 1024 * 1024
const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function Predict() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [error, setError] = useState('')
  const [inputMode, setInputMode] = useState('upload')
  const [result, setResult] = useState(null)

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl('')
      return undefined
    }

    const objectUrl = URL.createObjectURL(selectedFile)
    setPreviewUrl(objectUrl)

    return () => URL.revokeObjectURL(objectUrl)
  }, [selectedFile])

  const handleFileSelect = (file) => {
    setError('')
    setResult(null)

    if (!ACCEPTED_TYPES.includes(file.type)) {
      setSelectedFile(null)
      setError('Please upload a JPG, PNG, or WEBP image.')
      return
    }

    if (file.size > MAX_FILE_SIZE) {
      setSelectedFile(null)
      setError('The selected image must be 10 MB or smaller.')
      return
    }

    setSelectedFile(file)
  }

  const handleWebcamCapture = (file) => {
    handleFileSelect(file)
    setInputMode('upload')
  }

  const handleRemove = () => {
    setSelectedFile(null)
    setResult(null)
    setError('')
  }

  const handleAnalyze = () => {
    setResult({
      predicted_class: 'biodegradable',
      confidence: 0.93,
      model_name: 'MobileNetV3Small',
    })
  }

  const handleTryAnother = () => {
    setSelectedFile(null)
    setResult(null)
    setError('')
    setInputMode('upload')
  }

  return (
    <main className="min-h-[calc(100vh-82px)] bg-slate-50">
      <div className="mx-auto max-w-4xl px-6 py-14">
        {result ? (
          <Results
            result={result}
            previewUrl={previewUrl}
            onTryAnother={handleTryAnother}
          />
        ) : (
          <>
            <div className="text-center">
              <span className="inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
                Step 1 · Select Image
              </span>

              <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
                Identify your waste
              </h2>

              <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-slate-600">
                Upload an existing photo or capture one directly using
                your webcam.
              </p>
            </div>

            <div className="mt-8 grid grid-cols-2 rounded-2xl border border-slate-200 bg-white p-1.5 shadow-sm">
              <button
                type="button"
                onClick={() => setInputMode('upload')}
                className={`rounded-xl px-4 py-3 text-sm font-bold transition ${
                  inputMode === 'upload'
                    ? 'bg-green-600 text-white shadow-sm'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                Upload Image
              </button>

              <button
                type="button"
                onClick={() => setInputMode('camera')}
                className={`rounded-xl px-4 py-3 text-sm font-bold transition ${
                  inputMode === 'camera'
                    ? 'bg-green-600 text-white shadow-sm'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                Use Webcam
              </button>
            </div>

            <div className="mt-6">
              {inputMode === 'upload' ? (
                <ImageUpload
                  file={selectedFile}
                  previewUrl={previewUrl}
                  error={error}
                  onFileSelect={handleFileSelect}
                  onRemove={handleRemove}
                />
              ) : (
                <WebcamCapture
                  onCapture={handleWebcamCapture}
                  onClose={() => setInputMode('upload')}
                />
              )}
            </div>

            <button
              type="button"
              disabled={!selectedFile}
              onClick={handleAnalyze}
              className="mt-8 w-full rounded-2xl bg-green-600 px-6 py-4 text-base font-bold text-white shadow-sm transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              Analyze Waste
            </button>

            <p className="mt-3 text-center text-xs text-slate-400">
              The result is still temporary until the frontend API integration step.
            </p>
          </>
        )}
      </div>
    </main>
  )
}

export default Predict
