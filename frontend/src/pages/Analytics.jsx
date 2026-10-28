import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { isRequestCancelled } from '../services/api'
import { getAnalyticsSummary } from '../services/wasteService'

const DAYS = 7

const CATEGORY_COLORS = {
  biodegradable: '#16a34a',
  plastic: '#2563eb',
  paper: '#f59e0b',
  glass: '#0ea5e9',
  metal: '#64748b',
  'e-waste': '#7c3aed',
}

function colorFor(slug) {
  return CATEGORY_COLORS[slug] ?? '#94a3b8'
}

function formatDay(isoDate) {
  // Parse as local midnight so the weekday never shifts across time zones.
  const date = new Date(`${isoDate}T00:00:00`)

  return date.toLocaleDateString(undefined, {
    weekday: 'short',
    day: 'numeric',
  })
}

function StatCard({ label, value, helper }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-semibold text-slate-500">{label}</p>

      <p className="mt-2 text-3xl font-black tracking-tight text-slate-900">
        {value}
      </p>

      <p className="mt-2 text-xs leading-5 text-slate-400">{helper}</p>
    </div>
  )
}

function Analytics() {
  const [summary, setSummary] = useState(null)
  const [status, setStatus] = useState('loading') // loading | ready | error
  const [error, setError] = useState('')

  const load = useCallback(async (signal) => {
    setStatus('loading')
    setError('')

    try {
      const data = await getAnalyticsSummary({ days: DAYS, signal })
      setSummary(data)
      setStatus('ready')
    } catch (err) {
      if (isRequestCancelled(err)) return
      setError(err.message)
      setStatus('error')
    }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    load(controller.signal)
    return () => controller.abort()
  }, [load])

  const header = (
    <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <span className="inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
          Analytics Dashboard
        </span>

        <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
          Waste classification insights
        </h2>

        <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
          Live statistics from the predictions saved by the backend.
        </p>
      </div>

      <button
        type="button"
        onClick={() => load()}
        disabled={status === 'loading'}
        className="w-fit rounded-2xl border border-slate-300 bg-white px-4 py-2 text-sm font-bold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {status === 'loading' ? 'Refreshing…' : 'Refresh'}
      </button>
    </div>
  )

  let body

  if (status === 'loading' && !summary) {
    body = (
      <p role="status" className="mt-10 text-sm text-slate-500">
        Loading analytics…
      </p>
    )
  } else if (status === 'error' && !summary) {
    body = (
      <div
        role="alert"
        className="mt-10 rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700"
      >
        <p className="font-semibold">Could not load analytics.</p>
        <p className="mt-1">{error}</p>
        <button
          type="button"
          onClick={() => load()}
          className="mt-3 rounded-xl border border-red-300 px-4 py-2 font-bold hover:bg-red-100"
        >
          Retry
        </button>
      </div>
    )
  } else if (summary && summary.total_predictions === 0) {
    body = (
      <div className="mt-10 rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
        <h3 className="text-xl font-black text-slate-900">No scans yet</h3>

        <p className="mt-2 text-sm text-slate-500">
          Classify a waste image and the dashboard will fill in automatically.
        </p>

        <Link
          to="/predict"
          className="mt-6 inline-flex rounded-xl bg-green-600 px-5 py-3 text-sm font-bold text-white transition hover:bg-green-700"
        >
          Classify waste
        </Link>
      </div>
    )
  } else if (summary) {
    const categoryData = summary.by_category
      .filter((item) => item.count > 0)
      .map((item) => ({
        name: item.name,
        slug: item.slug,
        value: item.count,
      }))

    const dailyData = summary.scans_per_day.map((item) => ({
      day: formatDay(item.date),
      scans: item.count,
    }))

    const recentScans = summary.scans_per_day.reduce(
      (sum, item) => sum + item.count,
      0,
    )

    const topCategory = summary.by_category.find(
      (item) => item.slug === summary.top_category,
    )

    const answered =
      summary.feedback_correct + summary.feedback_incorrect

    body = (
      <>
        {status === 'error' && (
          <p
            role="alert"
            className="mt-6 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700"
          >
            Refresh failed: {error}. Showing the last loaded data.
          </p>
        )}

        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            label="Total scans"
            value={summary.total_predictions}
            helper="All predictions saved so far"
          />

          <StatCard
            label={`Last ${summary.days} days`}
            value={recentScans}
            helper="Scans in the recent period"
          />

          <StatCard
            label="Top category"
            value={topCategory?.name ?? '—'}
            helper={
              topCategory
                ? `${topCategory.count} of ${summary.total_predictions} scans`
                : 'No data yet'
            }
          />

          <StatCard
            label="Average confidence"
            value={
              summary.average_confidence == null
                ? '—'
                : `${Math.round(summary.average_confidence * 100)}%`
            }
            helper="Mean model confidence across all scans"
          />
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-green-700">
              Category distribution
            </p>

            <h3 className="mt-1 text-2xl font-black text-slate-900">
              Classification share
            </h3>

            <p className="mt-2 text-sm text-slate-500">
              Number of scans predicted for each waste category.
            </p>

            <div className="mt-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={65}
                    outerRadius={105}
                    paddingAngle={3}
                  >
                    {categoryData.map((entry) => (
                      <Cell key={entry.slug} fill={colorFor(entry.slug)} />
                    ))}
                  </Pie>

                  <Tooltip
                    formatter={(value) => [value, 'Scans']}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {categoryData.map((item) => (
                <li
                  key={item.slug}
                  className="flex items-center gap-2 text-xs font-semibold text-slate-600"
                >
                  <span
                    aria-hidden="true"
                    className="h-3 w-3 rounded-full"
                    style={{ backgroundColor: colorFor(item.slug) }}
                  />
                  {item.name}: {item.value}
                </li>
              ))}
            </ul>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-green-700">
              Scans per day
            </p>

            <h3 className="mt-1 text-2xl font-black text-slate-900">
              Recent activity
            </h3>

            <p className="mt-2 text-sm text-slate-500">
              Classification requests recorded each day.
            </p>

            <div className="mt-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dailyData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="day" tickLine={false} axisLine={false} />
                  <YAxis
                    allowDecimals={false}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip />
                  <Bar
                    dataKey="scans"
                    fill="#16a34a"
                    radius={[8, 8, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>
        </div>

        <section className="mt-8 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-xl font-black text-slate-900">
            User feedback on predictions
          </h3>

          {summary.feedback_total === 0 ? (
            <p className="mt-3 text-sm text-slate-500">
              No feedback yet. Users can confirm or correct a prediction on the
              result screen.
            </p>
          ) : (
            <div className="mt-5 grid gap-4 md:grid-cols-3">
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">
                  Marked correct
                </p>
                <p className="mt-1 text-2xl font-black text-green-700">
                  {summary.feedback_correct}
                </p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">
                  Marked wrong
                </p>
                <p className="mt-1 text-2xl font-black text-red-600">
                  {summary.feedback_incorrect}
                </p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">
                  Reported accuracy
                </p>
                <p className="mt-1 text-2xl font-black text-slate-900">
                  {answered > 0
                    ? `${Math.round(
                        (summary.feedback_correct / answered) * 100,
                      )}%`
                    : '—'}
                </p>
              </div>
            </div>
          )}
        </section>
      </>
    )
  }

  return (
    <main className="min-h-[calc(100vh-82px)] bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-14">
        {header}
        {body}
      </section>
    </main>
  )
}

export default Analytics
