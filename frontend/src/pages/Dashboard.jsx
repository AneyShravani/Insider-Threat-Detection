import { useEffect, useState } from "react";
import ThreatSeverityPie from "../components/charts/dashboard/ThreatSeverityPie";
import ThreatByHour from "../components/charts/dashboard/ThreatByHour";
import DLPViolations from "../components/charts/dashboard/DLPViolations";

const CARD_HEIGHT = 480;
const RIGHT_GAP   = 16;
const RIGHT_CHART_H = (CARD_HEIGHT - RIGHT_GAP) / 2; // 232px each

export default function Dashboard() {
  const [alerts, setAlerts]       = useState([]);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:5000/alerts").then(r => r.json()),
      fetch("http://localhost:5000/api/dashboard").then(r => r.json()),
    ]).then(([alertData, dashData]) => {
      setAlerts(alertData);
      setChartData(dashData);
      setLoading(false);
    });
  }, []);

  const high   = alerts.filter(a => a.severity === "high").length;
  const medium = alerts.filter(a => a.severity === "medium").length;
  const low    = alerts.filter(a => a.severity === "low").length;

  const statCards = [
    { label: "Total Alerts", value: alerts.length, color: "#3b82f6" },
    { label: "High Risk",    value: high,           color: "#ef4444" },
    { label: "Medium Risk",  value: medium,         color: "#f97316" },
    { label: "Low Risk",     value: low,            color: "#22c55e" },
  ];

  return (
    <div style={{
      padding: "28px 32px",
      color: "white",
      background: "#020617",
      minHeight: "100vh",
      fontFamily: "'Inter', sans-serif",
    }}>

      {/* Header */}
      <div style={{ marginBottom: 28, borderBottom: "1px solid #1e293b", paddingBottom: 18 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 8,
            background: "linear-gradient(135deg, #3b82f6, #1d4ed8)",
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18
          }}>🛡️</div>
          <div>
            <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: "-0.3px" }}>ThreatGuard</h1>
            <p style={{ fontSize: 12, color: "#64748b", margin: 0 }}>Insider Threat Detection — Live Dashboard</p>
          </div>
        </div>
      </div>

      {/* Stat Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        {statCards.map((card, i) => (
          <div key={i} style={{
            background: "#0f172a", border: `1px solid ${card.color}30`,
            borderRadius: 14, padding: "18px 22px", position: "relative", overflow: "hidden"
          }}>
            <div style={{
              position: "absolute", top: 0, left: 0, right: 0,
              height: 3, background: card.color, borderRadius: "14px 14px 0 0"
            }} />
            <div style={{ fontSize: 34, fontWeight: 800, color: card.color, letterSpacing: "-1px", lineHeight: 1 }}>
              {loading ? "—" : card.value}
            </div>
            <div style={{ fontSize: 13, color: "#64748b", marginTop: 8, fontWeight: 500 }}>
              {card.label}
            </div>
          </div>
        ))}
      </div>

      {/* Charts — STRICT height matching */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 16,
      }}>

        {/* LEFT — exact CARD_HEIGHT, no overflow */}
        <div style={{ height: CARD_HEIGHT, overflow: "hidden" }}>
          <ThreatSeverityPie data={chartData?.threat_severity} height={CARD_HEIGHT} />
        </div>

        {/* RIGHT — exact same CARD_HEIGHT, split into 2 equal boxes */}
        <div style={{
          height: CARD_HEIGHT,
          display: "flex",
          flexDirection: "column",
          gap: RIGHT_GAP,
          overflow: "hidden"
        }}>
          <div style={{ height: RIGHT_CHART_H, overflow: "hidden" }}>
            <ThreatByHour data={chartData?.detections_by_hour} height={RIGHT_CHART_H} />
          </div>
          <div style={{ height: RIGHT_CHART_H, overflow: "hidden" }}>
            <DLPViolations data={chartData?.dlp_violations} height={RIGHT_CHART_H} />
          </div>
        </div>

      </div>
    </div>
  );
}