import { useCallback, useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { isRequestCancelled } from '../services/api'
import { getDecomposition } from '../services/wasteService'

const SUBTYPE_ICONS = {
  food_kitchen: '🍽️',
  fruit_vegetable: '🥕',
  yard_green: '🍃',
  plant_crop_residues: '🌾',
}

const EVIDENCE_LABELS = {
  government_guidance: 'Government guidance',
  multi_source_synthesis: 'Multi-source synthesis',
  study_reported: 'Study reported',
}

function formatRange(min, max, unit = '') {
  const suffix = unit ? ` ${unit}` : ''

  if (min == null && max == null) return 'Not specified'
  if (min == null) return `up to ${max}${suffix}`
  if (max == null) return `${min}+${suffix}`
  if (min === max) return `${min}${suffix}`

  return `${min}–${max}${suffix}`
}

function titleCase(value) {
  return value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function Metric({ label, value }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-4">
      <p className="text-xs font-semibold text-slate-500">{label}</p>
      <p className="mt-1 text-lg font-black text-slate-900">{value}</p>
    </div>
  )
}

function ProfileCard({ profile }) {
  return (
    <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center gap-2">
        <h4 className="text-xl font-black text-slate-900">
          {titleCase(profile.treatment_method)}
        </h4>

        {profile.compost_stage && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">
            {titleCase(profile.compost_stage)} stage
          </span>
        )}

        <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-700">
          {EVIDENCE_LABELS[profile.evidence_scope] ??
            titleCase(profile.evidence_scope)}
        </span>
      </div>

      {profile.recommendation_text && (
        <p className="mt-4 leading-7 text-slate-700">
          {profile.recommendation_text}
        </p>
      )}

      <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        <Metric
          label="Temperature"
          value={formatRange(
            profile.temperature_min_c,
            profile.temperature_max_c,
            '°C',
          )}
        />
        <Metric
          label="Moisture"
          value={formatRange(
            profile.moisture_min_percent,
            profile.moisture_max_percent,
            '%',
          )}
        />
        <Metric label="pH" value={formatRange(profile.ph_min, profile.ph_max)} />
        <Metric
          label="C:N ratio"
          value={formatRange(profile.cn_ratio_min, profile.cn_ratio_max)}
        />
        <Metric
          label="Duration"
          value={formatRange(
            profile.expected_days_min,
            profile.expected_days_max,
            'days',
          )}
        />
      </div>

      {profile.notes && (
        <p className="mt-4 text-sm leading-6 text-slate-500">
          {profile.notes}
        </p>
      )}

      {profile.microorganisms.length > 0 && (
        <div className="mt-6">
          <h5 className="font-bold text-slate-900">
            Microorganisms reported
          </h5>

          <ul className="mt-3 grid gap-3 md:grid-cols-2">
            {profile.microorganisms.map((organism) => (
              <li
                key={organism.id}
                className="rounded-2xl border border-slate-100 bg-slate-50 p-4"
              >
                <p className="font-semibold text-slate-900">
                  <i>{organism.scientific_name}</i>
                  {organism.common_name && (
                    <span className="font-normal text-slate-500">
                      {' '}
                      ({organism.common_name})
                    </span>
                  )}
                </p>

                <p className="mt-1 text-xs font-semibold text-emerald-700">
                  {titleCase(organism.microbial_type)}
                </p>

                {(organism.role_in_profile || organism.role_description) && (
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {organism.role_in_profile || organism.role_description}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {profile.sources.length > 0 && (
        <div className="mt-6">
          <h5 className="font-bold text-slate-900">Sources</h5>

          <ul className="mt-3 space-y-3">
            {profile.sources.map((source) => (
              <li
                key={source.source_ref}
                className="text-sm leading-6 text-slate-600"
              >
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-semibold text-green-700 underline underline-offset-2 hover:text-green-800"
                >
                  {source.title}
                </a>

                <span className="block text-xs text-slate-500">
                  {[
                    source.authors,
                    source.publication,
                    source.publication_year,
                  ]
                    .filter(Boolean)
                    .join(' · ')}
                </span>

                {source.evidence_note && (
                  <span className="block text-xs text-slate-400">
                    {source.evidence_note}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  )
}

function DecompositionInfo() {
  const [searchParams, setSearchParams] = useSearchParams()
  const selectedSlug = searchParams.get('subtype')

  const [subtypes, setSubtypes] = useState([])
  const [subtypesStatus, setSubtypesStatus] = useState('loading')
  const [subtypesError, setSubtypesError] = useState('')

  const [detail, setDetail] = useState(null)
  const [detailStatus, setDetailStatus] = useState('idle')
  const [detailError, setDetailError] = useState('')

  const loadSubtypes = useCallback(async (signal) => {
    setSubtypesStatus('loading')
    setSubtypesError('')

    try {
      const data = await getDecomposition('biodegradable', { signal })
      setSubtypes(data.available_subtypes ?? [])
      setSubtypesStatus('ready')
    } catch (err) {
      if (isRequestCancelled(err)) return
      setSubtypesError(err.message)
      setSubtypesStatus('error')
    }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    loadSubtypes(controller.signal)
    return () => controller.abort()
  }, [loadSubtypes])

  useEffect(() => {
    if (!selectedSlug) {
      setDetail(null)
      setDetailStatus('idle')
      return undefined
    }

    const controller = new AbortController()

    setDetailStatus('loading')
    setDetailError('')

    getDecomposition(selectedSlug, { signal: controller.signal })
      .then((data) => {
        setDetail(data)
        setDetailStatus('ready')
      })
      .catch((err) => {
        if (isRequestCancelled(err)) return
        setDetailError(err.message)
        setDetailStatus('error')
      })

    return () => controller.abort()
  }, [selectedSlug])

  const selectSubtype = (slug) => {
    setSearchParams(slug === selectedSlug ? {} : { subtype: slug })
  }

  return (
    <main className="min-h-[calc(100vh-82px)] bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="max-w-3xl">
          <span className="inline-flex rounded-full bg-emerald-100 px-4 py-2 text-sm font-semibold text-emerald-700">
            Microbial Decomposition
          </span>

          <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
            Evidence-backed guidance for biodegradable waste
          </h2>

          <p className="mt-5 text-base leading-7 text-slate-600">
            Pick the kind of biodegradable waste you have. The classifier only
            predicts the broad class “biodegradable”, so the subtype is chosen
            here. Every profile below comes from the project’s knowledge base
            and links to its sources.
          </p>
        </div>

        <div className="mt-10">
          <h3 className="text-2xl font-black text-slate-900">
            Biodegradable subtypes
          </h3>

          {subtypesStatus === 'loading' && (
            <p role="status" className="mt-4 text-sm text-slate-500">
              Loading subtypes…
            </p>
          )}

          {subtypesStatus === 'error' && (
            <div
              role="alert"
              className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
            >
              <p className="font-semibold">Could not load subtypes.</p>
              <p className="mt-1">{subtypesError}</p>
              <button
                type="button"
                onClick={() => loadSubtypes()}
                className="mt-3 rounded-xl border border-red-300 px-4 py-2 font-bold hover:bg-red-100"
              >
                Retry
              </button>
            </div>
          )}

          {subtypesStatus === 'ready' && subtypes.length === 0 && (
            <p className="mt-4 rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600">
              No subtypes are stored yet. Run <code>database/schema.sql</code>{' '}
              and <code>database/seed.sql</code> to load the knowledge base.
            </p>
          )}

          {subtypes.length > 0 && (
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {subtypes.map((subtype) => {
                const isSelected = subtype.slug === selectedSlug

                return (
                  <button
                    key={subtype.slug}
                    type="button"
                    aria-pressed={isSelected}
                    onClick={() => selectSubtype(subtype.slug)}
                    className={[
                      'flex gap-4 rounded-3xl border p-5 text-left transition',
                      isSelected
                        ? 'border-green-600 bg-green-50 shadow-sm'
                        : 'border-slate-200 bg-white hover:border-green-300',
                    ].join(' ')}
                  >
                    <span
                      aria-hidden="true"
                      className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-green-50 text-3xl"
                    >
                      {SUBTYPE_ICONS[subtype.slug] ?? '🌱'}
                    </span>

                    <span>
                      <span className="block text-lg font-black text-slate-900">
                        {subtype.name}
                      </span>

                      {subtype.description && (
                        <span className="mt-1 block text-sm leading-6 text-slate-600">
                          {subtype.description}
                        </span>
                      )}
                    </span>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        <div className="mt-10" aria-live="polite">
          {!selectedSlug && subtypesStatus === 'ready' && subtypes.length > 0 && (
            <p className="rounded-2xl border border-dashed border-slate-300 p-6 text-center text-sm text-slate-500">
              Select a subtype above to see temperature, moisture, pH, C:N
              ratio, duration, microorganisms, and sources.
            </p>
          )}

          {detailStatus === 'loading' && (
            <p role="status" className="text-sm text-slate-500">
              Loading decomposition profiles…
            </p>
          )}

          {detailStatus === 'error' && (
            <p
              role="alert"
              className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700"
            >
              {detailError}
            </p>
          )}

          {detailStatus === 'ready' && detail && (
            <div className="space-y-6">
              {detail.message && detail.profiles.length === 0 && (
                <p className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600">
                  {detail.message}
                </p>
              )}

              {detail.profiles.map((profile) => (
                <ProfileCard key={profile.profile_id} profile={profile} />
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  )
}

export default DecompositionInfo
