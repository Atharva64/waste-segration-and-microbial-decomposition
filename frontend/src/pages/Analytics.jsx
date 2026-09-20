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

const categoryData = [
  { name: 'Biodegradable', value: 34 },
  { name: 'Plastic', value: 24 },
  { name: 'Paper', value: 16 },
  { name: 'Glass', value: 10 },
  { name: 'Metal', value: 9 },
  { name: 'E-Waste', value: 7 },
]

const scansPerDay = [
  { day: 'Mon', scans: 8 },
  { day: 'Tue', scans: 14 },
  { day: 'Wed', scans: 11 },
  { day: 'Thu', scans: 18 },
  { day: 'Fri', scans: 21 },
  { day: 'Sat', scans: 16 },
  { day: 'Sun', scans: 12 },
]

const PIE_COLORS = [
  '#16a34a',
  '#2563eb',
  '#f59e0b',
  '#0ea5e9',
  '#64748b',
  '#7c3aed',
]

function StatCard({ label, value, helper }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-semibold text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-3xl font-black tracking-tight text-slate-900">
        {value}
      </p>

      <p className="mt-2 text-xs leading-5 text-slate-400">
        {helper}
      </p>
    </div>
  )
}

function Analytics() {
  const totalScans = scansPerDay.reduce(
    (sum, item) => sum + item.scans,
    0
  )

  const topCategory = categoryData.reduce(
    (top, item) => (
      item.value > top.value ? item : top
    ),
    categoryData[0]
  )

  return (
    <main className="min-h-[calc(100vh-82px)] bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <span className="inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
              Analytics Dashboard
            </span>

            <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
              Waste classification insights
            </h2>

            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
              This Day 30 dashboard uses temporary frontend data to build the
              analytics UI. Live prediction-history data can replace it during
              API integration.
            </p>
          </div>

          <span className="w-fit rounded-2xl border border-amber-200 bg-amber-50 px-4 py-2 text-xs font-bold text-amber-700">
            Demo data
          </span>
        </div>

        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            label="Total scans"
            value={totalScans}
            helper="Demo scans for the current week"
          />

          <StatCard
            label="Top category"
            value={topCategory.name}
            helper={`${topCategory.value}% of demo classifications`}
          />

          <StatCard
            label="Supported classes"
            value="6"
            helper="Biodegradable, plastic, paper, glass, metal, e-waste"
          />

          <StatCard
            label="Model"
            value="MobileNetV3"
            helper="Classification model used by the backend"
          />
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <p className="text-sm font-semibold text-green-700">
                Category distribution
              </p>

              <h3 className="mt-1 text-2xl font-black text-slate-900">
                Classification share
              </h3>

              <p className="mt-2 text-sm text-slate-500">
                Percentage split across the six waste categories.
              </p>
            </div>

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
                    {categoryData.map((entry, index) => (
                      <Cell
                        key={entry.name}
                        fill={PIE_COLORS[index % PIE_COLORS.length]}
                      />
                    ))}
                  </Pie>

                  <Tooltip
                    formatter={(value) => [`${value}%`, 'Share']}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {categoryData.map((item, index) => (
                <div
                  key={item.name}
                  className="flex items-center gap-2 text-xs font-semibold text-slate-600"
                >
                  <span
                    className="h-3 w-3 rounded-full"
                    style={{
                      backgroundColor:
                        PIE_COLORS[index % PIE_COLORS.length],
                    }}
                  />

                  <span>
                    {item.name} · {item.value}%
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <p className="text-sm font-semibold text-green-700">
                Scans per day
              </p>

              <h3 className="mt-1 text-2xl font-black text-slate-900">
                Weekly activity
              </h3>

              <p className="mt-2 text-sm text-slate-500">
                Number of classification requests recorded each day.
              </p>
            </div>

            <div className="mt-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={scansPerDay}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                  />

                  <XAxis
                    dataKey="day"
                    tickLine={false}
                    axisLine={false}
                  />

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
            What will become live later?
          </h3>

          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="font-bold text-slate-800">
                Category counts
              </p>
              <p className="mt-1 text-sm leading-6 text-slate-500">
                Derived from the prediction history returned by the backend.
              </p>
            </div>

            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="font-bold text-slate-800">
                Scans per day
              </p>
              <p className="mt-1 text-sm leading-6 text-slate-500">
                Group prediction timestamps by date for daily activity.
              </p>
            </div>

            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="font-bold text-slate-800">
                Accuracy feedback
              </p>
              <p className="mt-1 text-sm leading-6 text-slate-500">
                User feedback can later be summarised for model monitoring.
              </p>
            </div>
          </div>
        </section>
      </section>
    </main>
  )
}

export default Analytics
