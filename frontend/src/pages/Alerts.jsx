import { useEffect, useState } from "react";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data))
      .catch(() => console.log("Backend not connected"));
  }, []);

  const borderColor = (severity) => {
    if (severity === 'high')   return '#ef4444';
    if (severity === 'medium') return '#f97316';
    return '#22c55e';
  };

  return (
    <div style={{ padding: 30, background: "#020617", minHeight: "100vh", color: "white" }}>
      <h1>🚨 Alerts</h1>
      <p style={{ color: "#94a3b8" }}>Total: {alerts.length} alerts detected</p>

      {alerts.map((a, i) => (
        <div key={i} style={{
          padding: 16,
          marginBottom: 10,
          background: "#0f172a",
          borderLeft: `5px solid ${borderColor(a.severity)}`,
          borderRadius: 8
        }}>
          <strong>User:</strong> {a.user} &nbsp;|&nbsp;
          <strong>Threat:</strong> {a.threat_type} &nbsp;|&nbsp;
          <strong>Risk:</strong> {a.risk}%
          <span style={{
            float: "right",
            background: borderColor(a.severity),
            padding: "2px 12px",
            borderRadius: 20,
            fontSize: 12,
            fontWeight: "bold"
          }}>
            {a.severity?.toUpperCase()}
          </span>
          {a.financial_impact > 0 && (
            <div style={{ marginTop: 6, color: "#94a3b8", fontSize: 13 }}>
              Financial Impact: ${a.financial_impact.toLocaleString()}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}