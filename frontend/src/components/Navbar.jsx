import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/predict', label: 'Classify' },
  { to: '/guide', label: 'Waste Guide' },
  { to: '/decomposition', label: 'Decomposition' },
  { to: '/analytics', label: 'Analytics' },
]

function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-6 py-4 sm:flex-row sm:items-center sm:justify-between">
        <NavLink to="/predict" className="group">
          <h1 className="text-2xl font-black tracking-tight text-green-700">
            WasteAI
          </h1>
          <p className="text-xs font-medium text-slate-500">
            Smart Waste Segregation
          </p>
        </NavLink>

        <nav className="flex flex-wrap items-center gap-1 rounded-2xl bg-slate-100 p-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  'rounded-xl px-3 py-2 text-sm font-semibold transition',
                  isActive
                    ? 'bg-white text-green-700 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900',
                ].join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  )
}

export default Navbar
