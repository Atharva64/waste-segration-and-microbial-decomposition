import { useEffect, useState } from 'react'
import ImageUpload from '../components/ImageUpload'

const MAX_FILE_SIZE = 10 * 1024 * 1024
const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function Predict() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [error, setError] = useState('')

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

  const handleRemove = () => {
    setSelectedFile(null)
    setError('')
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-2xl font-black tracking-tight text-green-700">
              WasteAI
            </h1>
            <p className="text-xs font-medium text-slate-500">
              AI Waste Segregation System
            </p>
          </div>

          <span className="rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700">
            Image Classification
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-14">
        <div className="text-center">
          <span className="inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
            Step 1 · Upload
          </span>

          <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
            Identify your waste
          </h2>

          <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-slate-600">
            Upload a clear photo of one waste item. The AI model will classify
            it into one of the supported waste categories.
          </p>
        </div>

        <div className="mt-10">
          <ImageUpload
            file={selectedFile}
            previewUrl={previewUrl}
            error={error}
            onFileSelect={handleFileSelect}
            onRemove={handleRemove}
          />
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-4">
            <p className="text-sm font-bold text-slate-900">Good lighting</p>
            <p className="mt-1 text-xs leading-5 text-slate-500">
              Use a bright image so the object is clearly visible.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-4">
            <p className="text-sm font-bold text-slate-900">One main item</p>
            <p className="mt-1 text-xs leading-5 text-slate-500">
              Keep the waste object centered and avoid a cluttered scene.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-4">
            <p className="text-sm font-bold text-slate-900">Supported formats</p>
            <p className="mt-1 text-xs leading-5 text-slate-500">
              JPG, PNG, and WEBP images up to 10 MB.
            </p>
          </div>
        </div>

        <button
          type="button"
          disabled={!selectedFile}
          className="mt-8 w-full rounded-2xl bg-green-600 px-6 py-4 text-base font-bold text-white shadow-sm transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          Analyze Waste
        </button>

        <p className="mt-3 text-center text-xs text-slate-400">
          API prediction will be connected in the next integration step.
        </p>
      </main>
    </div>
  )
}

export default Predict
