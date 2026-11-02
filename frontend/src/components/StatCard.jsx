export default function StatCard({ label, value, detail, accent = "" }) {
  return <article className={`stat-card ${accent}`}><p>{label}</p><strong>{value}</strong>{detail && <span>{detail}</span>}</article>;
}
