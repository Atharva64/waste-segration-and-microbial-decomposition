import { useEffect, useState } from 'react'
import { checkHealth } from '../services/wasteService'

const POLL_INTERVAL_MS = 30_000

/**
 * Tracks whether the backend API is reachable.
 * Returns 'checking' | 'online' | 'offline'.
 */
export default function useApiHealth() {
  const [status, setStatus] = useState('checking')

  useEffect(() => {
    let isActive = true
    let controller = null

    const check = async () => {
      controller?.abort()
      controller = new AbortController()

      try {
        await checkHealth({ signal: controller.signal })
        if (isActive) setStatus('online')
      } catch (error) {
        if (isActive && error?.name !== 'CanceledError') {
          setStatus('offline')
        }
      }
    }

    check()

    const intervalId = window.setInterval(check, POLL_INTERVAL_MS)
    window.addEventListener('focus', check)

    return () => {
      isActive = false
      controller?.abort()
      window.clearInterval(intervalId)
      window.removeEventListener('focus', check)
    }
  }, [])

  return status
}
