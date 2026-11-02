import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getAnalytics, getDistricts, getModelInfo, getOptions } from "../services/api";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import ChartCard from "../components/ChartCard";
import { ErrorState, Loading } from "../components/State";

export default function Dashboard() {
  const [data, setData] = useState(null); const [model, setModel] = useState(null); const [counts, setCounts] = useState(null); const [error, setError] = useState("");
  useEffect(() => { Promise.all([getAnalytics(), getModelInfo(), getOptions(), getDistricts()]).then(([a, m, o, d]) => { setData(a.data); setModel(m.data); setCounts({ crops: o[0].data.crops.length, states: o[1].data.states.length, districts: d.data.districts.length }); }).catch(() => setError("Backend data could not be loaded. Start Flask and refresh.")); }, []);
  if (error) return <><PageHeader eyebrow="Overview" title="Agricultural intelligence" /><ErrorState message={error} /></>;
  if (!data || !model || !counts) return <Loading />;
  const d = data.dataset; const test = model.metrics.test;
  return <><PageHeader eyebrow="Overview" title="Agricultural intelligence" description="A clear view of historical crop-yield patterns and model performance." />
    <div className="stat-grid">
      <StatCard label="Dataset records" value={d.records.toLocaleString()} detail={`${d.year_range[0]}–${d.year_range[1]}`} accent="green" />
      <StatCard label="Crops" value={counts.crops} detail="Observed in dataset" />
      <StatCard label="States" value={counts.states} detail="Observed in dataset" />
      <StatCard label="Districts" value={counts.districts} detail="Observed in dataset" />
      <StatCard label="Test R²" value={test.r2.toFixed(3)} detail="Chronological test set" accent="gold" />
      <StatCard label="Test MAE" value={test.mae.toFixed(1)} detail="Native Yield scale" />
      <StatCard label="Test RMSE" value={test.rmse.toFixed(1)} detail="Native Yield scale" />
    </div>
    <div className="chart-grid"><ChartCard title="Average yield by crop" subtitle="Actual historical records, ranked by mean Yield"><ResponsiveContainer width="100%" height={330}><BarChart data={data.by_crop.slice(0, 12)} layout="vertical" margin={{ left: 20, right: 20 }}><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" /><YAxis type="category" dataKey="crop" width={105} tick={{ fontSize: 11 }} /><Tooltip /><Bar dataKey="mean_yield" name="Mean Yield" fill="#287c55" radius={[0, 5, 5, 0]} /></BarChart></ResponsiveContainer></ChartCard>
      <ChartCard title="Average yield by season" subtitle="Historical season comparison"><ResponsiveContainer width="100%" height={330}><BarChart data={data.by_season} margin={{ top: 10, right: 10 }}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="season" /><YAxis /><Tooltip /><Bar dataKey="mean_yield" name="Mean Yield" fill="#d39a3c" radius={[5, 5, 0, 0]} /></BarChart></ResponsiveContainer></ChartCard></div>
  </>;
}
