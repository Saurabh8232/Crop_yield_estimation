import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
import History from "./pages/History";
import Analytics from "./pages/Analytics";
import Model from "./pages/Model";

const links = [
  ["Dashboard", "/"],
  ["Predict yield", "/predict"],
  ["History", "/history"],
  ["Analytics", "/analytics"],
  ["About model", "/model"],
];

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">✦</span><span>AgriSignal</span></div>
        <p className="sidebar-caption">Crop intelligence</p>
        <nav>{links.map(([label, path]) => (
          <NavLink key={path} to={path} end={path === "/"} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <span className="nav-dot" />{label}
          </NavLink>
        ))}</nav>
        <div className="sidebar-note">Historical estimation<br />ANN-powered insights</div>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/predict" element={<Prediction />} />
          <Route path="/history" element={<History />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/model" element={<Model />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
