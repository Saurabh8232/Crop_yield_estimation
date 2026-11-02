import { useEffect, useState } from "react";
import { getModelInfo } from "../services/api";
import PageHeader from "../components/PageHeader";
import { ErrorState, Loading } from "../components/State";

export default function Model() {
  const [info, setInfo] = useState(null); const [error, setError] = useState("");
  useEffect(() => { getModelInfo().then((r) => setInfo(r.data)).catch(() => setError("Could not load model information.")); }, []);
  if (error) return <><PageHeader eyebrow="Methodology" title="About the model" /><ErrorState message={error} /></>;
  if (!info) return <Loading />;
  return <><PageHeader eyebrow="Methodology" title="About the model" description="The saved ANN and its leakage-safe preprocessing pipeline." /><div className="info-grid"><section className="info-card"><p className="eyebrow">Architecture</p><h2>MLPRegressor</h2><p>Two hidden layers (64, 32) with ReLU activation and Adam optimization.</p><div className="metric-list"><Metric label="Train R²" value={info.metrics.train.r2.toFixed(3)} /><Metric label="Validation R²" value={info.metrics.validation.r2.toFixed(3)} /><Metric label="Test R²" value={info.metrics.test.r2.toFixed(3)} /><Metric label="Test MAE" value={info.metrics.test.mae.toFixed(1)} /><Metric label="Test RMSE" value={info.metrics.test.rmse.toFixed(1)} /></div></section><section className="info-card"><p className="eyebrow">Inputs</p><h2>{info.features.length} approved features</h2><div className="tag-list">{info.features.map((feature) => <span key={feature}>{feature}</span>)}</div><p className="muted">Target: <strong>{info.target}</strong> · Unit: unknown</p></section><section className="info-card full"><p className="eyebrow">Limitations</p><h2>Interpret results in context</h2><p className="callout">This system performs retrospective, season-level historical crop yield estimation. It is not an operational pre-season or during-season forecasting system.</p><ul className="limitations">{info.limitations.map((item) => <li key={item}>{item}</li>)}</ul></section></div></>;
}
function Metric({ label, value }) { return <div><span>{label}</span><strong>{value}</strong></div>; }
