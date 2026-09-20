import { useRef, useState } from 'react'

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function ImageUpload({ file, previewUrl, error, onFileSelect, onRemove }) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFiles = (files) => {
    if (!files || files.length === 0) return
    onFileSelect(files[0])
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragging(false)
    handleFiles(event.dataTransfer.files)
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      inputRef.current?.click()
    }
  }

  if (file && previewUrl) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="overflow-hidden rounded-2xl bg-slate-100">
          <img
            src={previewUrl}
            alt="Selected waste preview"
            className="h-80 w-full object-contain"
          />
        </div>

        <div className="mt-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="min-w-0">
            <p className="truncate font-semibold text-slate-900">{file.name}</p>
            <p className="mt-1 text-sm text-slate-500">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </p>
          </div>

          <button
            type="button"
            onClick={onRemove}
            className="rounded-xl border border-red-200 px-4 py-2 text-sm font-semibold text-red-600 transition hover:bg-red-50"
          >
            Remove image
          </button>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div
        role="button"
        tabIndex={0}
        onKeyDown={handleKeyDown}
        onClick={() => inputRef.current?.click()}
        onDragEnter={(event) => {
          event.preventDefault()
          setIsDragging(true)
        }}
        onDragOver={(event) => {
          event.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={(event) => {
          event.preventDefault()
          setIsDragging(false)
        }}
        onDrop={handleDrop}
        className={[
          'cursor-pointer rounded-3xl border-2 border-dashed p-10 text-center transition',
          isDragging
            ? 'border-green-500 bg-green-50'
            : 'border-slate-300 bg-white hover:border-green-400 hover:bg-green-50/40',
        ].join(' ')}
      >
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED_TYPES.join(',')}
          className="hidden"
          onChange={(event) => handleFiles(event.target.files)}
        />

        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-green-100 text-green-700">
          <svg
            viewBox="0 0 24 24"
            className="h-8 w-8"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 16V4m0 0-4 4m4-4 4 4M5 14v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4"
            />
          </svg>
        </div>

        <h2 className="mt-5 text-xl font-bold text-slate-900">
          Upload a waste image
        </h2>

        <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
          Drag and drop an image here, or click to choose one from your computer.
        </p>

        <span className="mt-6 inline-flex rounded-xl bg-green-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-green-700">
          Choose image
        </span>

        <p className="mt-4 text-xs text-slate-400">
          JPG, PNG or WEBP · Maximum 10 MB
        </p>
      </div>

      {error && (
        <p className="mt-3 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
          {error}
        </p>
      )}
    </div>
  )
}

export default ImageUpload
