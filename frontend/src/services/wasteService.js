import { request } from './api'

/** GET /health */
export function checkHealth({ signal } = {}) {
  return request({ method: 'get', url: '/health', signal, timeout: 5_000 })
}

/**
 * POST /api/predict
 * Sends one image as multipart form data (field name: "image").
 * The first request can be slow while the server loads the TensorFlow model.
 */
export function predictImage(file, { signal } = {}) {
  const formData = new FormData()
  formData.append('image', file, file.name)

  return request({
    method: 'post',
    url: '/api/predict',
    data: formData,
    signal,
    timeout: 90_000,
  })
}

/** GET /api/waste/categories */
export function getWasteCategories({ signal } = {}) {
  return request({ method: 'get', url: '/api/waste/categories', signal })
}

/**
 * GET /api/decomposition/{waste}
 * `waste` is either "biodegradable" (returns the available subtypes)
 * or a subtype slug such as "food_kitchen" (returns its profiles).
 */
export function getDecomposition(waste, { signal } = {}) {
  return request({
    method: 'get',
    url: `/api/decomposition/${encodeURIComponent(waste)}`,
    signal,
  })
}

/** GET /api/predictions */
export function getPredictionHistory({ limit = 50, signal } = {}) {
  return request({
    method: 'get',
    url: '/api/predictions',
    params: { limit },
    signal,
  })
}

/** POST /api/feedback */
export function submitFeedback(payload, { signal } = {}) {
  return request({
    method: 'post',
    url: '/api/feedback',
    data: payload,
    signal,
  })
}

/** GET /api/analytics/summary */
export function getAnalyticsSummary({ days = 7, signal } = {}) {
  return request({
    method: 'get',
    url: '/api/analytics/summary',
    params: { days },
    signal,
  })
}
