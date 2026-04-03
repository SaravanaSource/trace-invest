import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

const primaryNav = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/stocks", label: "Stocks" },
  { href: "/alpha-lab", label: "Alpha Lab" },
  { href: "/portfolio", label: "Portfolio" },
];

const secondaryNav = [
  { href: "/watchlist", label: "Watchlists" },
  { href: "/alerts", label: "Alerts" },
  { href: "/admin", label: "Admin" },
];

export const metadata: Metadata = {
  title: "TRACE MARKETS",
  description:
    "A decision-support platform for fundamentals-first investing, alpha research, and portfolio operations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <aside className="sidebar-shell">
            <Link href="/" className="brand-block">
              <div className="brand-mark">TR</div>
              <div>
                <p className="text-xs uppercase tracking-[0.32em] text-slate-400">
                  Trace Markets
                </p>
                <h1 className="mt-2 text-lg font-semibold text-white">
                  Investment OS
                </h1>
              </div>
            </Link>

            <div className="sidebar-group">
              <p className="sidebar-label">Core</p>
              <nav className="space-y-2">
                {primaryNav.map((item) => (
                  <Link key={item.href} href={item.href} className="nav-link">
                    {item.label}
                  </Link>
                ))}
              </nav>
            </div>

            <div className="sidebar-group">
              <p className="sidebar-label">Operations</p>
              <nav className="space-y-2">
                {secondaryNav.map((item) => (
                  <Link key={item.href} href={item.href} className="nav-link">
                    {item.label}
                  </Link>
                ))}
              </nav>
            </div>

            <div className="status-panel">
              <p className="text-xs uppercase tracking-[0.22em] text-slate-400">
                Deployment posture
              </p>
              <p className="mt-3 text-sm leading-6 text-slate-200">
                Deterministic research engine, API surface, and operator UI in a
                single workspace.
              </p>
            </div>
          </aside>

          <div className="content-shell">
            <header className="topbar-shell">
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">
                  Fundamentals-first decision support
                </p>
                <p className="mt-2 text-sm text-slate-300">
                  Research, monitor, and operate from one interface.
                </p>
              </div>
              <div className="topbar-actions">
                <Link href="/alpha-lab" className="secondary-cta">
                  Research Stack
                </Link>
                <Link href="/dashboard" className="primary-cta">
                  Open Product
                </Link>
              </div>
            </header>

            <main className="main-shell">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
