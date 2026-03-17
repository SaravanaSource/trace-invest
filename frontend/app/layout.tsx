import "./globals.css";
import Link from "next/link";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="w-60 bg-panel border-r border-border p-6">
          <h1 className="text-xl font-bold mb-8">TRACE MARKETS</h1>

          <nav className="space-y-4 text-muted">
            <Link href="/dashboard" className="block hover:text-text">
              Dashboard
            </Link>
            <Link href="/stocks" className="block hover:text-text">
              Stocks
            </Link>
            <Link href="/portfolio" className="block hover:text-text">Portfolio</Link>
            <Link href="/watchlist" className="block hover:text-text">Watchlists</Link>
            <Link href="/alerts" className="block hover:text-text">Alerts</Link>
            <Link href="/admin" className="block hover:text-text">Admin</Link>
          </nav>
        </aside>

        {/* Content */}
        <main className="flex-1 p-10">{children}</main>
      </body>
    </html>
  );
}
