import { useEffect, useState } from 'react'
import { getWasteCategories, submitFeedback } from '../services/wasteService'
import { isRequestCancelled } from '../services/api'

function FeedbackForm({ predictionId, predictedClass }) {
  const [verdict, setVerdict] = useState(null) // 'correct' | 'incorrect'
  const [categories, setCategories] = useState([])
  const [categoriesError, setCategoriesError] = useState('')
  const [correctedId, setCorrectedId] = useState('')
  const [rating, setRating] = useState(0)
  const [comments, setComments] = useState('')
  const [status, setStatus] = useState('idle') // idle | submitting | done
  const [error, setError] = useState('')

  // Load categories only when the user says the prediction was wrong.
  useEffect(() => {
    if (verdict !== 'incorrect' || categories.length > 0) return undefined

    const controller = new AbortController()

    getWasteCategories({ signal: controller.signal })
      .then((data) => {
        setCategories(data)
        setCategoriesError('')
      })
      .catch((err) => {
        if (!isRequestCancelled(err)) setCategoriesError(err.message)
      })

    return () => controller.abort()
  }, [verdict, categories.length])

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!verdict || status === 'submitting') return

    setStatus('submitting')
    setError('')

    const payload = {
      prediction_id: predictionId,
      was_prediction_correct: verdict === 'correct',
    }

    if (verdict === 'incorrect' && correctedId) {
      payload.corrected_category_id = Number(correctedId)
    }
    if (rating > 0) payload.rating = rating
    if (comments.trim()) payload.comments = comments.trim()

    try {
      await submitFeedback(payload)
      setStatus('done')
    } catch (err) {
      setError(err.message)
      setStatus('idle')
    }
  }

  if (status === 'done') {
    return (
      <div
        role="status"
        className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-4 text-sm font-semibold text-green-800"
      >
        Thanks — your feedback was saved and helps us check the model.
      </div>
    )
  }

  const otherCategories = categories.filter(
    (category) => category.slug !== predictedClass,
  )

  return (
    <form
      onSubmit={handleSubmit}
      className="mt-6 rounded-2xl border border-slate-200 p-5"
    >
      <p className="font-bold text-slate-900">Was this prediction correct?</p>

      <div className="mt-3 grid grid-cols-2 gap-3">
        {[
          { key: 'correct', label: 'Yes, correct' },
          { key: 'incorrect', label: 'No, wrong' },
        ].map((option) => (
          <button
            key={option.key}
            type="button"
            aria-pressed={verdict === option.key}
            onClick={() => setVerdict(option.key)}
            className={[
              'rounded-xl border px-4 py-2.5 text-sm font-bold transition',
              verdict === option.key
                ? 'border-green-600 bg-green-600 text-white'
                : 'border-slate-300 text-slate-700 hover:bg-slate-50',
            ].join(' ')}
          >
            {option.label}
          </button>
        ))}
      </div>

      {verdict === 'incorrect' && (
        <div className="mt-4">
          <label
            htmlFor="corrected-category"
            className="text-sm font-semibold text-slate-700"
          >
            What is it actually?
          </label>

          <select
            id="corrected-category"
            value={correctedId}
            onChange={(event) => setCorrectedId(event.target.value)}
            className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-800"
          >
            <option value="">Not sure / skip</option>
            {otherCategories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>

          {categoriesError && (
            <p className="mt-2 text-xs text-red-600">{categoriesError}</p>
          )}
        </div>
      )}

      {verdict && (
        <>
          <div className="mt-4">
            <p className="text-sm font-semibold text-slate-700">
              Rate the recommendation (optional)
            </p>

            <div className="mt-2 flex gap-1" role="group" aria-label="Rating">
              {[1, 2, 3, 4, 5].map((value) => (
                <button
                  key={value}
                  type="button"
                  aria-label={`${value} out of 5`}
                  aria-pressed={rating === value}
                  onClick={() => setRating(rating === value ? 0 : value)}
                  className={[
                    'h-10 w-10 rounded-lg text-xl transition',
                    value <= rating
                      ? 'text-amber-500'
                      : 'text-slate-300 hover:text-amber-400',
                  ].join(' ')}
                >
                  ★
                </button>
              ))}
            </div>
          </div>

          <div className="mt-4">
            <label
              htmlFor="feedback-comments"
              className="text-sm font-semibold text-slate-700"
            >
              Comments (optional)
            </label>

            <textarea
              id="feedback-comments"
              value={comments}
              onChange={(event) => setComments(event.target.value)}
              maxLength={2000}
              rows={3}
              className="mt-2 w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm text-slate-800"
            />
          </div>

          {error && (
            <p
              role="alert"
              className="mt-3 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700"
            >
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={status === 'submitting'}
            className="mt-4 w-full rounded-xl bg-slate-900 px-5 py-3 text-sm font-bold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {status === 'submitting' ? 'Sending…' : 'Send feedback'}
          </button>
        </>
      )}
    </form>
  )
}

export default FeedbackForm
