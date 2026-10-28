import { useEffect, useRef, useState } from 'react'
import ImageUpload from '../components/ImageUpload'
import WebcamCapture from '../components/WebcamCapture'
import Results from './Results'
import { isRequestCancelled } from '../services/api'
import { predictImage } from '../services/wasteService'

const MAX_FILE_SIZE = 10 * 1024 * 1024
const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function Predict() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [error, setError] = useState('')
  const [inputMode, setInputMode] = useState('upload')
  const [result, setResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analyzeError, setAnalyzeError] = useState('')
  const abortRef = useRef(null)

  // Cancel any in-flight request when leaving the page.
  useEffect(() => () => abortRef.current?.abort(), [])

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
    setAnalyzeError('')
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
    setAnalyzeError('')
  }

  const handleAnalyze = async () => {
    if (!selectedFile || isAnalyzing) return

    const controller = new AbortController()
    abortRef.current = controller

    setAnalyzeError('')
    setIsAnalyzing(true)

    try {
      const data = await predictImage(selectedFile, {
        signal: controller.signal,
      })
      setResult(data)
    } catch (err) {
      if (!isRequestCancelled(err)) {
        setAnalyzeError(err.message)
      }
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null
        setIsAnalyzing(false)
      }
    }
  }

  const handleCancelAnalyze = () => {
    abortRef.current?.abort()
    abortRef.current = null
    setIsAnalyzing(false)
  }

  const handleTryAnother = () => {
    setSelectedFile(null)
    setResult(null)
    setError('')
    setAnalyzeError('')
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

            {analyzeError && (
              <p
                role="alert"
                className="mt-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700"
              >
                {analyzeError}
              </p>
            )}

            <button
              type="button"
              disabled={!selectedFile || isAnalyzing}
              aria-busy={isAnalyzing}
              onClick={handleAnalyze}
              className="mt-6 flex w-full items-center justify-center gap-3 rounded-2xl bg-green-600 px-6 py-4 text-base font-bold text-white shadow-sm transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {isAnalyzing && (
                <span
                  aria-hidden="true"
                  className="h-5 w-5 animate-spin rounded-full border-2 border-white/40 border-t-white"
                />
              )}
              {isAnalyzing ? 'Analyzing…' : analyzeError ? 'Try again' : 'Analyze Waste'}
            </button>

            {isAnalyzing ? (
              <p
                role="status"
                className="mt-3 text-center text-xs text-slate-500"
              >
                The first analysis can take a few seconds while the model
                loads.{' '}
                <button
                  type="button"
                  onClick={handleCancelAnalyze}
                  className="font-semibold text-slate-700 underline underline-offset-2"
                >
                  Cancel
                </button>
              </p>
            ) : (
              <p className="mt-3 text-center text-xs text-slate-400">
                Results are saved to your prediction history.
              </p>
            )}
          </>
        )}
      </div>
    </main>
  )
}

export default Predict
