import { useEffect, useState } from "react";
import { getDistricts, getOptions, predictYield } from "../services/api";
import PageHeader from "../components/PageHeader";
import { ErrorState, Loading } from "../components/State";

const fields = [
  ["Temperature", "number", -2.84, 29.12], ["Rainfall", "number", 7, 8409], ["Humidity", "number", 24.6, 83.4], ["pH", "number", 5.6, 8],
  ["Nitrogen", "number", 0, 470.97], ["Phosphorus", "number", 0, 251.16], ["Potassium", "number", 0, 222.54], ["Fertilizer", "number", 0, 804.53], ["Pesticide", "number", 0.09, 0.44],
];
const initial = { Year: "", Temperature: "", Rainfall: "", Humidity: "", "Soil Type": "", pH: "", Nitrogen: "", Phosphorus: "", Potassium: "", Fertilizer: "", Pesticide: "", State: "", District: "", Crop: "", Season: "" };

export default function Prediction() {
  const [form, setForm] = useState(initial); const [options, setOptions] = useState({ crops: [], states: [], seasons: [], soilTypes: [], years: [], districts: [] }); const [result, setResult] = useState(null); const [error, setError] = useState(""); const [loading, setLoading] = useState(true); const [districtLoading, setDistrictLoading] = useState(false); const [submitting, setSubmitting] = useState(false);
  useEffect(() => { getOptions().then(([c, s, se, soil, years]) => setOptions((o) => ({ ...o, crops: c.data.crops, states: s.data.states, seasons: se.data.seasons, soilTypes: soil.data.soil_types, years: years.data.years }))).catch(() => setError("Could not load form options from the dataset.")).finally(() => setLoading(false)); }, []);
  useEffect(() => { if (!form.State) { setOptions((o) => ({ ...o, districts: [] })); return; } setDistrictLoading(true); getDistricts(form.State).then((r) => setOptions((o) => ({ ...o, districts: r.data.districts }))).catch(() => setError("Could not load districts for the selected state.")).finally(() => setDistrictLoading(false)); }, [form.State]);
  const update = (name, value) => { setForm((f) => ({ ...f, [name]: value, ...(name === "State" ? { District: "" } : {}) })); setResult(null); };
  const submit = async (event) => { event.preventDefault(); setError(""); setResult(null); const missing = Object.entries(form).filter(([, value]) => value === "").map(([name]) => name); if (missing.length) { setError(`Complete all fields: ${missing.join(", ")}.`); return; } setSubmitting(true); try { const payload = Object.fromEntries(Object.entries(form).map(([k, v]) => [k, fields.some(([name]) => name === k) ? Number(v) : v])); const response = await predictYield(payload); setResult(response.data); } catch (e) { setError(e.response?.data?.details?.join(" ") || "Prediction failed."); } finally { setSubmitting(false); } };
  if (loading) return <Loading />;
  return <><PageHeader eyebrow="Estimation" title="Predict historical yield" description="Enter a complete season-level record using the same 15 inputs used by the ANN." />
    <div className="prediction-layout"><form className="form-card" onSubmit={submit}><div className="form-section"><h2>Context</h2><div className="form-grid">
      <Select label="Year" name="Year" value={form.Year} options={options.years} onChange={update} note="Historical dataset years only" />
      <Select label="State" name="State" value={form.State} options={options.states} onChange={update} />
      <Select label="District" name="District" value={form.District} options={options.districts} onChange={update} disabled={!form.State || districtLoading} placeholder={districtLoading ? "Loading districts..." : undefined} note={!form.State ? "Select a State first" : districtLoading ? "Loading districts for this State..." : `${options.districts.length} districts available`} />
      <Select label="Crop" name="Crop" value={form.Crop} options={options.crops} onChange={update} />
      <Select label="Season" name="Season" value={form.Season} options={options.seasons} onChange={update} />
      <Select label="Soil Type" name="Soil Type" value={form["Soil Type"]} options={options.soilTypes} onChange={update} /></div></div>
      <div className="form-section"><h2>Conditions and inputs</h2><div className="form-grid">{fields.map(([name, type, min, max]) => <Field key={name} label={name} name={name} type={type} min={min} max={max} value={form[name]} onChange={update} />)}</div><p className="field-note">Numeric ranges reflect observed values in the processed historical dataset. Dataset units are not specified.</p></div>
      {error && <div className="inline-error">{error}</div>}<button className="primary-button" disabled={submitting}>{submitting ? "Estimating..." : "Estimate Yield"}</button></form>
      <aside className="result-card">{result ? <><p className="eyebrow">Prediction #{result.prediction_id}</p><h2>{result.predicted_yield.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h2><p className="result-label">Predicted Yield · native dataset scale</p><div className="notice">The physical measurement unit of Yield is unknown in the source dataset.</div></> : <div className="result-empty"><span>✦</span><h2>Your estimate will appear here</h2><p>Submit a complete historical record to view the ANN result.</p></div>}</aside></div></>;
}
function Field({ label, name, type = "text", value, onChange, min, max }) { return <label className="field"><span>{label}</span><input required name={name} type={type} min={min} max={max} value={value} onChange={(e) => onChange(name, e.target.value)} step={type === "number" ? "any" : undefined} /></label>; }
function Select({ label, name, value, options, onChange, disabled, placeholder, note }) { return <label className="field"><span>{label}</span><select required name={name} value={value} disabled={disabled} onChange={(e) => onChange(name, e.target.value)}><option value="">{placeholder || `Select ${label}`}</option>{options.map((option) => <option key={option} value={option}>{option}</option>)}</select>{note && <small className="field-note">{note}</small>}</label>; }
