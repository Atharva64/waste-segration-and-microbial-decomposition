const subtypes = [
  {
    slug: 'food_kitchen',
    title: 'Food & Kitchen Waste',
    icon: '🍽️',
    description:
      'Food-related biodegradable material represented in the project knowledge base.',
  },
  {
    slug: 'fruit_vegetable',
    title: 'Fruit & Vegetable Waste',
    icon: '🥕',
    description:
      'Fruit and vegetable residues with evidence-backed decomposition profiles stored in the database.',
  },
  {
    slug: 'yard_green',
    title: 'Yard & Green Waste',
    icon: '🍃',
    description:
      'Leaves, grass, and similar green material covered by the supported knowledge-base subtype.',
  },
  {
    slug: 'plant_crop_residues',
    title: 'Plant & Crop Residues',
    icon: '🌾',
    description:
      'Plant-derived and crop-residue material represented by the project research dataset.',
  },
]

function DecompositionInfo() {
  return (
    <main className="min-h-[calc(100vh-82px)] bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
          <div>
            <span className="inline-flex rounded-full bg-emerald-100 px-4 py-2 text-sm font-semibold text-emerald-700">
              Microbial Decomposition
            </span>

            <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
              Evidence-backed guidance for biodegradable waste
            </h2>

            <p className="mt-5 max-w-3xl text-base leading-7 text-slate-600">
              Your Phase 3 knowledge base stores decomposition profiles,
              microorganisms, operating conditions, recommendations, and source
              references for supported biodegradable waste subtypes.
            </p>

            <div className="mt-8 rounded-3xl border border-emerald-200 bg-emerald-50 p-6">
              <h3 className="text-lg font-black text-emerald-900">
                Why a subtype is required
              </h3>

              <p className="mt-2 leading-7 text-emerald-950/80">
                The image classifier currently predicts the broad class
                “biodegradable”. It does not automatically determine whether
                that material is food waste, fruit and vegetable waste, yard
                waste, or plant/crop residue. The user selects the subtype
                before requesting specific decomposition information.
              </p>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
              Project flow
            </p>

            <div className="mt-5 space-y-3">
              {[
                'AI predicts biodegradable',
                'User selects a supported subtype',
                'Backend queries PostgreSQL',
                'Profiles + microorganisms + sources are returned',
              ].map((step, index) => (
                <div
                  key={step}
                  className="flex items-center gap-4 rounded-2xl bg-slate-50 p-4"
                >
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-green-600 text-sm font-black text-white">
                    {index + 1}
                  </span>
                  <p className="font-semibold text-slate-700">
                    {step}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-12">
          <h3 className="text-2xl font-black text-slate-900">
            Supported biodegradable subtypes
          </h3>

          <p className="mt-2 text-sm text-slate-500">
            These match the subtype slugs already used by your PostgreSQL
            decomposition knowledge base.
          </p>

          <div className="mt-6 grid gap-5 md:grid-cols-2">
            {subtypes.map((subtype) => (
              <article
                key={subtype.slug}
                className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <div className="flex gap-4">
                  <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-green-50 text-3xl">
                    {subtype.icon}
                  </div>

                  <div>
                    <h4 className="text-xl font-black text-slate-900">
                      {subtype.title}
                    </h4>

                    <code className="mt-2 inline-block rounded-lg bg-slate-100 px-2 py-1 text-xs text-slate-600">
                      {subtype.slug}
                    </code>
                  </div>
                </div>

                <p className="mt-4 text-sm leading-6 text-slate-600">
                  {subtype.description}
                </p>

                <div className="mt-5 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                  <p className="text-sm font-semibold text-slate-700">
                    Detailed temperature, moisture, pH, C:N, duration,
                    microorganism, and source data are supplied from the
                    evidence-backed backend records rather than hard-coded here.
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  )
}

export default DecompositionInfo
