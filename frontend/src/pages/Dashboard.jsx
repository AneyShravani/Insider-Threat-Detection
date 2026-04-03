import { useEffect, useState } from "react";

export default function Dashboard() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data));
  }, []);

  const severityColor = (s) => {
    if (s === 'high')   return '#ef4444';
    if (s === 'medium') return '#f97316';
    return '#22c55e';
  };

  return (
    <div style={{ padding: 30, color: "white", background: "#020617", minHeight: "100vh" }}>
      <h1>🛡️ Insider Threat Dashboard</h1>
      <h3>Total Alerts: {alerts.length}</h3>

      <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 20 }}>
        <thead>
          <tr style={{ background: "#1e293b", textAlign: "left" }}>
            <th style={{ padding: 12 }}>User</th>
            <th style={{ padding: 12 }}>Threat Type</th>
            <th style={{ padding: 12 }}>Risk %</th>
            <th style={{ padding: 12 }}>Severity</th>
            <th style={{ padding: 12 }}>Financial Impact</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #334155" }}>
              <td style={{ padding: 12 }}>{a.user}</td>
              <td style={{ padding: 12 }}>{a.threat_type}</td>
              <td style={{ padding: 12 }}>{a.risk}%</td>
              <td style={{ padding: 12 }}>
                <span style={{
                  background: severityColor(a.severity),
                  padding: "4px 10px",
                  borderRadius: 20,
                  fontWeight: "bold",
                  fontSize: 13
                }}>
                  {a.severity.toUpperCase()}
                </span>
              </td>
              <td style={{ padding: 12 }}>${a.financial_impact.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}