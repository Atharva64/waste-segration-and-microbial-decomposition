import axios from 'axios'

/**
 * Base URL of the FastAPI backend.
 *
 * - Development: leave VITE_API_BASE_URL empty. Requests such as
 *   `/api/predict` go to the Vite dev server, which proxies them to
 *   the backend (see vite.config.js), so no CORS setup is needed.
 * - Production: set VITE_API_BASE_URL to the deployed API URL
 *   (for example https://api.example.com) when building.
 */
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(
  /\/+$/,
  '',
)

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30_000,
})

/** Error with a message that is safe to show directly to the user. */
export class ApiError extends Error {
  constructor(message, { status = null, code = null, details = null } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }
}

export function isRequestCancelled(error) {
  return axios.isCancel(error)
}

function firstValidationMessage(details) {
  if (!Array.isArray(details) || details.length === 0) return null

  const first = details[0]
  const field = Array.isArray(first?.loc)
    ? first.loc.filter((part) => part !== 'body').join('.')
    : ''

  if (!first?.msg) return null

  return field ? `${field}: ${first.msg}` : first.msg
}

/**
 * Convert any axios failure into an ApiError.
 * The backend returns errors as { error: { code, message, details? } }.
 */
export function toApiError(error) {
  if (error instanceof ApiError || axios.isCancel(error)) return error

  if (error?.response) {
    const { status, data } = error.response
    const payload = data?.error

    let message =
      payload?.message ||
      (typeof data?.detail === 'string' ? data.detail : null) ||
      `The server returned an error (${status}).`

    if (status === 422) {
      const detail = firstValidationMessage(payload?.details)
      if (detail) message = `Invalid request — ${detail}`
    }

    return new ApiError(message, {
      status,
      code: payload?.code ?? null,
      details: payload?.details ?? null,
    })
  }

  if (error?.code === 'ECONNABORTED') {
    return new ApiError(
      'The request timed out. The server may still be loading the AI model — please try again.',
      { code: 'timeout' },
    )
  }

  return new ApiError(
    'Cannot reach the server. Make sure the backend is running (uvicorn backend.app.main:app --reload).',
    { code: 'network_error' },
  )
}

/** Run an axios call and return `response.data`, throwing ApiError on failure. */
export async function request(config) {
  try {
    const response = await apiClient.request(config)
    return response.data
  } catch (error) {
    throw toApiError(error)
  }
}
