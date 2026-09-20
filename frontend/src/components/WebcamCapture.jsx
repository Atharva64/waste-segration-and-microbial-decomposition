import { useEffect, useRef, useState } from 'react'

function WebcamCapture({ onCapture, onClose }) {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)

  const [isStarting, setIsStarting] = useState(true)
  const [cameraError, setCameraError] = useState('')

  useEffect(() => {
    let isMounted = true

    const startCamera = async () => {
      setIsStarting(true)
      setCameraError('')

      try {
        if (!navigator.mediaDevices?.getUserMedia) {
          throw new Error(
            'Camera access is not supported in this browser.'
          )
        }

        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: 'environment',
          },
          audio: false,
        })

        if (!isMounted) {
          stream.getTracks().forEach((track) => track.stop())
          return
        }

        streamRef.current = stream

        if (videoRef.current) {
          videoRef.current.srcObject = stream
          await videoRef.current.play()
        }
      } catch (error) {
        if (!isMounted) return

        if (error.name === 'NotAllowedError') {
          setCameraError(
            'Camera permission was denied. Please allow camera access and try again.'
          )
        } else if (error.name === 'NotFoundError') {
          setCameraError(
            'No camera was found on this device.'
          )
        } else if (error.name === 'NotReadableError') {
          setCameraError(
            'The camera is already in use by another application.'
          )
        } else {
          setCameraError(
            error.message || 'Unable to start the camera.'
          )
        }
      } finally {
        if (isMounted) {
          setIsStarting(false)
        }
      }
    }

    startCamera()

    return () => {
      isMounted = false

      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) => track.stop())

        streamRef.current = null
      }
    }
  }, [])

  const captureImage = () => {
    const video = videoRef.current
    const canvas = canvasRef.current

    if (!video || !canvas) return

    const width = video.videoWidth
    const height = video.videoHeight

    if (!width || !height) {
      setCameraError(
        'Camera is not ready yet. Please try again in a moment.'
      )
      return
    }

    canvas.width = width
    canvas.height = height

    const context = canvas.getContext('2d')

    if (!context) {
      setCameraError(
        'Unable to capture the camera image.'
      )
      return
    }

    context.drawImage(
      video,
      0,
      0,
      width,
      height
    )

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setCameraError(
            'Unable to create the captured image.'
          )
          return
        }

        const file = new File(
          [blob],
          `webcam-${Date.now()}.jpg`,
          {
            type: 'image/jpeg',
          }
        )

        onCapture(file)
      },
      'image/jpeg',
      0.92
    )
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">
            Capture from webcam
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Place one waste item clearly inside the camera frame.
          </p>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
        >
          Close
        </button>
      </div>

      <div className="mt-5 overflow-hidden rounded-2xl bg-slate-950">
        {isStarting && (
          <div className="flex h-80 items-center justify-center text-sm font-medium text-white">
            Starting camera...
          </div>
        )}

        {cameraError && !isStarting && (
          <div className="flex h-80 items-center justify-center p-8 text-center">
            <div>
              <div className="text-4xl">📷</div>

              <p className="mt-4 font-semibold text-white">
                Camera unavailable
              </p>

              <p className="mt-2 max-w-md text-sm leading-6 text-slate-300">
                {cameraError}
              </p>
            </div>
          </div>
        )}

        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={`h-80 w-full object-cover ${
            isStarting || cameraError
              ? 'hidden'
              : 'block'
          }`}
        />
      </div>

      <canvas
        ref={canvasRef}
        className="hidden"
      />

      {!cameraError && (
        <button
          type="button"
          disabled={isStarting}
          onClick={captureImage}
          className="mt-5 w-full rounded-2xl bg-green-600 px-6 py-4 font-bold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          Capture Photo
        </button>
      )}

      <p className="mt-3 text-center text-xs text-slate-400">
        Camera access works on localhost or secure HTTPS pages.
      </p>
    </div>
  )
}

export default WebcamCapture
