import Link from "next/link";

const pillars = [
  {
    title: "Decision Intelligence",
    copy:
      "Daily market context, stock-level conviction, risk framing, and explainable reasoning in one workflow.",
  },
  {
    title: "Alpha Research Stack",
    copy:
      "Signal discovery, strategy generation, ranking, and monitoring designed for reproducible research.",
  },
  {
    title: "Operator Controls",
    copy:
      "Portfolio, watchlist, alerting, and admin surfaces to support a real operating cadence instead of ad hoc analysis.",
  },
];

const surfaces = [
  "Daily Control Center",
  "Alpha Lab",
  "Opportunity Scanner",
  "Stock Deep Dives",
  "Portfolio + Watchlists",
  "Admin Metrics",
];

export default function Home() {
  return (
    <div className="space-y-16 pb-12">
      <section className="hero-panel overflow-hidden rounded-[2rem] border border-white/10 px-6 py-10 sm:px-10 sm:py-14">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(110,231,183,0.2),transparent_28%),radial-gradient(circle_at_top_right,rgba(96,165,250,0.2),transparent_30%)]" />
        <div className="relative grid gap-10 lg:grid-cols-[1.15fr_0.85fr] lg:items-end">
          <div className="space-y-6">
            <div className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-semibold uppercase tracking-[0.28em] text-slate-200">
              Production-ready investing workspace
            </div>
            <div className="space-y-4">
              <h1 className="max-w-3xl text-4xl font-semibold leading-tight text-white sm:text-5xl">
                TRACE turns raw investing workflows into a clear operating system.
              </h1>
              <p className="max-w-2xl text-base leading-8 text-slate-300 sm:text-lg">
                Built for fundamentals-first investors who want explainability,
                repeatability, and a product that feels like a control room
                instead of a notebook dump.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link href="/dashboard" className="primary-cta">
                Open Dashboard
              </Link>
              <Link href="/alpha-lab" className="secondary-cta">
                Explore Alpha Lab
              </Link>
              <Link href="/stocks" className="secondary-cta">
                Review Stocks
              </Link>
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-8 rounded-full bg-emerald-400/10 blur-3xl" />
            <div className="relative rounded-[1.75rem] border border-white/10 bg-slate-950/70 p-6 shadow-2xl shadow-emerald-950/30 backdrop-blur">
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-400">
                    Live product surfaces
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-white">
                    What ships in this repo
                  </p>
                </div>
                <div className="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1 text-sm font-medium text-emerald-200">
                  Reproducible
                </div>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                {surfaces.map((surface) => (
                  <div
                    key={surface}
                    className="rounded-2xl border border-white/8 bg-white/5 px-4 py-4 text-sm text-slate-200"
                  >
                    {surface}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-3">
        {pillars.map((pillar) => (
          <article
            key={pillar.title}
            className="rounded-[1.5rem] border border-white/10 bg-white/5 p-6 backdrop-blur"
          >
            <div className="mb-3 h-10 w-10 rounded-2xl bg-gradient-to-br from-emerald-300/25 to-sky-300/20" />
            <h2 className="text-xl font-semibold text-white">{pillar.title}</h2>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              {pillar.copy}
            </p>
          </article>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="rounded-[1.75rem] border border-white/10 bg-slate-950/60 p-8">
          <p className="text-xs uppercase tracking-[0.26em] text-slate-400">
            Product posture
          </p>
          <h2 className="mt-3 text-3xl font-semibold text-white">
            Built to help you decide, not just inspect data.
          </h2>
          <p className="mt-4 max-w-xl text-sm leading-7 text-slate-300">
            The platform already includes backend routes, deterministic research
            artifacts, authenticated portfolio surfaces, and a multi-page
            frontend. This pass upgrades the presentation layer so the repo
            opens like a real product and not an unfinished starter template.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Link href="/dashboard" className="feature-link">
            <span className="feature-kicker">Operate</span>
            <span className="feature-title">Daily Control Center</span>
            <span className="feature-copy">
              Market tone, actionable guidance, and ranked ideas.
            </span>
          </Link>
          <Link href="/alpha-lab" className="feature-link">
            <span className="feature-kicker">Research</span>
            <span className="feature-title">Alpha Lab</span>
            <span className="feature-copy">
              Signals, strategies, backtests, and explainable scoring.
            </span>
          </Link>
          <Link href="/portfolio" className="feature-link">
            <span className="feature-kicker">Manage</span>
            <span className="feature-title">Portfolio</span>
            <span className="feature-copy">
              Holdings, exposure, and performance-aware workflows.
            </span>
          </Link>
          <Link href="/admin" className="feature-link">
            <span className="feature-kicker">Monitor</span>
            <span className="feature-title">Admin</span>
            <span className="feature-copy">
              Strategy result counts and queue visibility for operations.
            </span>
          </Link>
        </div>
      </section>
    </div>
  );
}
