import ClassificationResult from '../components/ClassificationResult'

function Results({
  result,
  previewUrl,
  onTryAnother,
}) {
  if (!result) {
    return (
      <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <h2 className="text-2xl font-black text-slate-900">
          No classification result yet
        </h2>

        <p className="mt-2 text-slate-500">
          Upload or capture an image and run the classifier first.
        </p>

        <button
          type="button"
          onClick={onTryAnother}
          className="mt-6 rounded-xl bg-green-600 px-5 py-3 font-bold text-white transition hover:bg-green-700"
        >
          Go to image selection
        </button>
      </div>
    )
  }

  return (
    <ClassificationResult
      result={result}
      previewUrl={previewUrl}
      onTryAnother={onTryAnother}
    />
  )
}

export default Results
