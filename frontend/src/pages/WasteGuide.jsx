const categories = [
  {
    name: 'Biodegradable',
    slug: 'biodegradable',
    icon: '🌿',
    description:
      'Organic waste that can break down biologically. Your project provides decomposition guidance for supported biodegradable subtypes.',
    examples: ['Food scraps', 'Fruit & vegetable waste', 'Yard waste'],
    biodegradable: true,
    recyclingNote: 'Composting / biological treatment',
  },
  {
    name: 'Plastic',
    slug: 'plastic',
    icon: '♻️',
    description:
      'Plastic items should be separated from organic waste and handled according to the accepted recycling stream in your area.',
    examples: ['Bottles', 'Containers', 'Packaging'],
    biodegradable: false,
    recyclingNote: 'Recycling depends on plastic type and local rules',
  },
  {
    name: 'Paper',
    slug: 'paper',
    icon: '📄',
    description:
      'Clean and dry paper is commonly collected separately for recycling. Food-soiled paper may need different handling.',
    examples: ['Newspaper', 'Cardboard', 'Office paper'],
    biodegradable: true,
    recyclingNote: 'Commonly recyclable when clean and dry',
  },
  {
    name: 'Glass',
    slug: 'glass',
    icon: '🫙',
    description:
      'Glass should be kept separate from general waste where glass collection is available. Broken glass requires careful handling.',
    examples: ['Bottles', 'Jars', 'Glass containers'],
    biodegradable: false,
    recyclingNote: 'Commonly recyclable where accepted',
  },
  {
    name: 'Metal',
    slug: 'metal',
    icon: '🥫',
    description:
      'Metal waste can often be recovered through recycling systems. Clean items are easier to sort and process.',
    examples: ['Cans', 'Metal containers', 'Scrap metal'],
    biodegradable: false,
    recyclingNote: 'Commonly recyclable where accepted',
  },
  {
    name: 'E-Waste',
    slug: 'e-waste',
    icon: '🔌',
    description:
      'Electronic waste should not be mixed with ordinary household waste. Use an authorised e-waste collection or recycling channel.',
    examples: ['Small electronics', 'Cables', 'Electronic accessories'],
    biodegradable: false,
    recyclingNote: 'Use a dedicated e-waste channel',
  },
]

function WasteGuide() {
  return (
    <main className="min-h-[calc(100vh-82px)] bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="max-w-3xl">
          <span className="inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
            Waste Guide
          </span>

          <h2 className="mt-5 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">
            Know where your waste belongs
          </h2>

          <p className="mt-4 text-base leading-7 text-slate-600">
            The classifier currently works with six broad categories. Use this
            guide as a simple overview; actual recycling acceptance can vary by
            material and local collection rules.
          </p>
        </div>

        <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {categories.map((category) => (
            <article
              key={category.slug}
              className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
            >
              <div className="flex items-start justify-between gap-4">
                <span className="text-4xl" aria-hidden="true">
                  {category.icon}
                </span>

                <span
                  className={[
                    'rounded-full px-3 py-1 text-xs font-bold',
                    category.biodegradable
                      ? 'bg-green-100 text-green-700'
                      : 'bg-slate-100 text-slate-600',
                  ].join(' ')}
                >
                  {category.biodegradable
                    ? 'Biodegradable'
                    : 'Non-biodegradable'}
                </span>
              </div>

              <h3 className="mt-5 text-2xl font-black text-slate-900">
                {category.name}
              </h3>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {category.description}
              </p>

              <div className="mt-5">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                  Examples
                </p>

                <div className="mt-2 flex flex-wrap gap-2">
                  {category.examples.map((example) => (
                    <span
                      key={example}
                      className="rounded-lg bg-slate-100 px-2.5 py-1.5 text-xs font-medium text-slate-600"
                    >
                      {example}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mt-5 rounded-2xl bg-green-50 p-4">
                <p className="text-xs font-bold uppercase tracking-wide text-green-700">
                  Handling note
                </p>
                <p className="mt-1 text-sm leading-6 text-slate-700">
                  {category.recyclingNote}
                </p>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}

export default WasteGuide
