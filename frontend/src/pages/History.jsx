import { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import PageHeader from "../components/PageHeader";
import { EmptyState, ErrorState, Loading } from "../components/State";

export default function History() {
  const [items, setItems] = useState(null); const [error, setError] = useState("");
  useEffect(() => { getHistory().then((r) => setItems(r.data.predictions)).catch(() => setError("Could not load prediction history.")); }, []);
  return <><PageHeader eyebrow="Records" title="Prediction history" description="Saved estimates from this application session and earlier runs." />{error ? <ErrorState message={error} /> : items === null ? <Loading /> : items.length === 0 ? <EmptyState text="No predictions have been saved yet. Your completed estimates will appear here." /> : <div className="table-card"><table><thead><tr><th>ID</th><th>Crop</th><th>State</th><th>District</th><th>Predicted Yield</th><th>Date</th></tr></thead><tbody>{items.map((item) => <tr key={item.id}><td>#{item.id}</td><td>{item.inputs.Crop}</td><td>{item.inputs.State}</td><td>{item.inputs.District}</td><td className="strong">{item.predicted_yield.toLocaleString(undefined, { maximumFractionDigits: 2 })}</td><td>{new Date(item.predicted_at).toLocaleString()}</td></tr>)}</tbody></table></div>}</>;
}
