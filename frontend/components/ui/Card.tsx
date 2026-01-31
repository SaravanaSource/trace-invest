export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-panel border border-border rounded-xl p-6">
      {children}
    </div>
  );
}

