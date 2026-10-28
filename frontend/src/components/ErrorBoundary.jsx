import { Component } from 'react'

class ErrorBoundary extends Component {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error, info) {
    console.error('Unhandled UI error:', error, info.componentStack)
  }

  render() {
    if (!this.state.hasError) return this.props.children

    return (
      <main className="mx-auto max-w-xl px-6 py-24 text-center">
        <h2 className="text-3xl font-black text-slate-900">
          Something went wrong
        </h2>

        <p className="mt-3 text-slate-600">
          The page hit an unexpected error. Reloading usually fixes it.
        </p>

        <button
          type="button"
          onClick={() => window.location.reload()}
          className="mt-6 rounded-xl bg-green-600 px-5 py-3 font-bold text-white transition hover:bg-green-700"
        >
          Reload page
        </button>
      </main>
    )
  }
}

export default ErrorBoundary
