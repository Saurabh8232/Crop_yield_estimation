export default function ChartCard({ title, subtitle, children, wide = false }) {
  return <section className={`chart-card ${wide ? "wide" : ""}`}><div className="chart-heading"><div><h2>{title}</h2><p>{subtitle}</p></div></div>{children}</section>;
}
