import { useEffect, useState } from "react";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getAnalytics } from "../services/api";
import PageHeader from "../components/PageHeader";
import ChartCard from "../components/ChartCard";
import { ErrorState, Loading } from "../components/State";

export default function Analytics() {
  const [data, setData] = useState(null); const [error, setError] = useState("");
  useEffect(() => { getAnalytics().then((r) => setData(r.data)).catch(() => setError("Could not load analytics.")); }, []);
  if (error) return <><PageHeader eyebrow="Explore" title="Historical analytics" /><ErrorState message={error} /></>;
  if (!data) return <Loading />;
  return <><PageHeader eyebrow="Explore" title="Historical analytics" description="Aggregations calculated from the complete processed dataset." /><div className="chart-grid"><ChartCard title="Yield trend by year" subtitle="Mean historical Yield by year" wide><ResponsiveContainer width="100%" height={360}><AreaChart data={data.by_year}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="year" interval="preserveStartEnd" /><YAxis /><Tooltip /><Area type="monotone" dataKey="mean_yield" name="Mean Yield" stroke="#287c55" fill="#dcefe4" /></AreaChart></ResponsiveContainer></ChartCard><ChartCard title="State comparison" subtitle="Top 20 states by mean Yield"><ResponsiveContainer width="100%" height={400}><BarChart data={data.by_state} layout="vertical" margin={{ left: 20, right: 20 }}><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" /><YAxis type="category" dataKey="state" width={125} tick={{ fontSize: 10 }} /><Tooltip /><Bar dataKey="mean_yield" name="Mean Yield" fill="#4a9b70" radius={[0, 5, 5, 0]} /></BarChart></ResponsiveContainer></ChartCard><ChartCard title="Crop comparison" subtitle="All crops by historical mean Yield"><ResponsiveContainer width="100%" height={400}><BarChart data={data.by_crop} layout="vertical" margin={{ left: 20, right: 20 }}><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" /><YAxis type="category" dataKey="crop" width={125} tick={{ fontSize: 10 }} /><Tooltip /><Bar dataKey="mean_yield" name="Mean Yield" fill="#d39a3c" radius={[0, 5, 5, 0]} /></BarChart></ResponsiveContainer></ChartCard></div></>;
}
