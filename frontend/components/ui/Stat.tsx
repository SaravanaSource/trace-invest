export function Stat({
  label,
  value,
  tone = "default",
}: {
  label: string;
  value: string | number;
  tone?: "good" | "warn" | "bad" | "default";
}) {
  const tones: any = {
    good: "text-good",
    warn: "text-warn",
    bad: "text-bad",
    default: "text-text",
  };

  return (
    <div className="bg-panel border border-border rounded-xl p-6">
      <p className="text-muted text-sm">{label}</p>
      <p className={`text-3xl font-semibold mt-1 ${tones[tone]}`}>
        {value}
      </p>
    </div>
  );
}

