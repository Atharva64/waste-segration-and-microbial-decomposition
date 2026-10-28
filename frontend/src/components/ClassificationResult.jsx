import { Link } from 'react-router-dom'
import FeedbackForm from './FeedbackForm'

const CATEGORY_META = {
  biodegradable: {
    label: 'Biodegradable',
    biodegradable: true,
    recyclable: false,
    recommendation:
      'Use composting or an appropriate microbial decomposition process. Separate it from dry recyclable waste.',
  },
  plastic: {
    label: 'Plastic',
    biodegradable: false,
    recyclable: true,
    recommendation:
      'Keep it clean and dry, then send it to an appropriate plastic recycling stream when accepted locally.',
  },
  paper: {
    label: 'Paper',
    biodegradable: true,
    recyclable: true,
    recommendation:
      'Keep clean paper dry and recycle it. Heavily food-soiled paper may be better suited to composting where supported.',
  },
  glass: {
    label: 'Glass',
    biodegradable: false,
    recyclable: true,
    recommendation:
      'Rinse the item if needed and place it in an accepted glass recycling stream. Handle broken glass carefully.',
  },
  metal: {
    label: 'Metal',
    biodegradable: false,
    recyclable: true,
    recommendation:
      'Clean the item and send it to a metal recycling stream. Keep sharp edges safely contained.',
  },
  'e-waste': {
    label: 'E-Waste',
    biodegradable: false,
    recyclable: true,
    recommendation:
      'Do not place electronic waste in normal household waste. Use an authorised e-waste collection or recycling channel.',
  },
}

const LOW_CONFIDENCE_THRESHOLD = 0.6

function formatClassLabel(slug) {
  return CATEGORY_META[slug]?.label ?? slug
}

function Flag({ active, label }) {
  return (
    <div
      className={[
        'flex items-center gap-2 rounded-xl border px-4 py-3 text-sm font-semibold',
        active
          ? 'border-green-200 bg-green-50 text-green-700'
          : 'border-slate-200 bg-slate-50 text-slate-500',
      ].join(' ')}
    >
      <span
        className={[
          'flex h-6 w-6 items-center justify-center rounded-full text-xs',
          active
            ? 'bg-green-600 text-white'
            : 'bg-slate-300 text-white',
        ].join(' ')}
      >
        {active ? '✓' : '×'}
      </span>
      {label}
    </div>
  )
}

function ClassificationResult({
  result,
  previewUrl,
  onTryAnother,
}) {
  const categoryKey = result.predicted_class.toLowerCase()
  const meta = CATEGORY_META[categoryKey] ?? {
    label: result.predicted_class,
    biodegradable: false,
    recyclable: false,
    recommendation:
      'Follow your local waste-management guidance for safe disposal.',
  }

  const confidencePercent = Math.round(result.confidence * 100)
  const isLowConfidence = result.confidence < LOW_CONFIDENCE_THRESHOLD
  const showDecompositionLink = categoryKey === 'biodegradable'

  const topPredictions = Object.entries(result.probabilities ?? {})
    .sort(([, a], [, b]) => b - a)
    .slice(0, 3)

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <div className="grid gap-8 md:grid-cols-[0.9fr_1.1fr]">
        <div>
          <div className="overflow-hidden rounded-2xl bg-slate-100">
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Waste prediction input"
                className="h-72 w-full object-contain"
              />
            ) : (
              <div className="flex h-72 items-center justify-center text-slate-400">
                No preview available
              </div>
            )}
          </div>

          <p className="mt-3 text-center text-xs text-slate-400">
            Uploaded / captured image
          </p>
        </div>

        <div>
          <span className="inline-flex rounded-full bg-green-100 px-3 py-1 text-xs font-bold uppercase tracking-wide text-green-700">
            Classification complete
          </span>

          <p className="mt-5 text-sm font-semibold uppercase tracking-wide text-slate-400">
            Predicted category
          </p>

          <h2 className="mt-1 text-4xl font-black tracking-tight text-slate-900">
            {meta.label}
          </h2>

          <div className="mt-6">
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-500">
                  Confidence
                </p>
                <p className="mt-1 text-3xl font-black text-green-700">
                  {confidencePercent}%
                </p>
              </div>

              <p className="text-right text-xs text-slate-400">
                {result.model_name ?? 'AI classifier'}
              </p>
            </div>

            <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-green-600 transition-all"
                style={{
                  width: `${Math.min(confidencePercent, 100)}%`,
                }}
              />
            </div>
          </div>

          {isLowConfidence && (
            <p
              role="status"
              className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-900"
            >
              The model is not very sure about this one. Try a clearer,
              well-lit photo with a single item in the frame.
            </p>
          )}

          {topPredictions.length > 1 && (
            <div className="mt-5">
              <p className="text-sm font-semibold text-slate-500">
                Top predictions
              </p>

              <ul className="mt-2 space-y-2">
                {topPredictions.map(([slug, probability]) => (
                  <li
                    key={slug}
                    className="flex items-center gap-3 text-sm text-slate-700"
                  >
                    <span className="w-28 shrink-0 font-medium">
                      {formatClassLabel(slug)}
                    </span>

                    <span className="h-2 flex-1 overflow-hidden rounded-full bg-slate-100">
                      <span
                        className="block h-full rounded-full bg-green-500"
                        style={{ width: `${Math.round(probability * 100)}%` }}
                      />
                    </span>

                    <span className="w-10 text-right tabular-nums text-slate-500">
                      {Math.round(probability * 100)}%
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            <Flag
              active={meta.biodegradable}
              label="Biodegradable"
            />

            <Flag
              active={meta.recyclable}
              label="Recyclable"
            />
          </div>

          <div className="mt-6 rounded-2xl border border-emerald-100 bg-emerald-50 p-5">
            <p className="text-sm font-bold uppercase tracking-wide text-emerald-700">
              Recommendation
            </p>

            <p className="mt-2 leading-7 text-slate-700">
              {result.recommendation ?? meta.recommendation}
            </p>
          </div>

          {showDecompositionLink && (
            <div className="mt-4 rounded-2xl border border-amber-100 bg-amber-50 p-4 text-sm leading-6 text-amber-900">
              Microbial decomposition guidance is available for biodegradable
              waste.{' '}
              <Link
                to="/decomposition"
                className="font-bold underline underline-offset-2 hover:text-amber-950"
              >
                View decomposition guidance
              </Link>
            </div>
          )}

          {result.prediction_id != null && (
            <FeedbackForm
              key={result.prediction_id}
              predictionId={result.prediction_id}
              predictedClass={categoryKey}
            />
          )}

          <button
            type="button"
            onClick={onTryAnother}
            className="mt-6 w-full rounded-2xl border border-slate-300 px-5 py-3 font-bold text-slate-700 transition hover:bg-slate-50"
          >
            Analyze another image
          </button>
        </div>
      </div>
    </section>
  )
}

export default ClassificationResult
