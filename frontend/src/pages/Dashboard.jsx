import { useEffect, useState } from "react";
import ThreatSeverityPie from "../components/charts/ThreatSeverityPie";
import ThreatByHour from "../components/charts/ThreatByHour";
import DLPViolations from "../components/charts/DLPViolations";
import RiskyUsers from "../components/charts/RiskyUsers";

export default function Dashboard({ theme }) {
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [riskData, setRiskData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data));

    fetch("http://localhost:5000/api/dashboard")
      .then(res => res.json())
      .then(data => setChartData(data));

    fetch("http://localhost:5000/api/user-risk")
      .then(res => res.json())
      .then(data => setRiskData(data));
  }, []);

  const isDark = theme === "dark";

  const colors = {
    bg: isDark ? "#020617" : "#f1f5f9",
    text: isDark ? "white" : "#020617",
    subText: isDark ? "#94a3b8" : "#475569",
    tableHeader: isDark ? "#1e293b" : "#e2e8f0",
    border: isDark ? "#334155" : "#cbd5f5"
  };

  const severityColor = (s) => {
    if (s === 'high') return '#ef4444';
    if (s === 'medium') return '#f97316';
    return '#22c55e';
  };

  return (
    <div style={{
      padding: 30,
      color: colors.text,
      background: colors.bg,
      minHeight: "100vh"
    }}>
      
      <h1>🛡️ Insider Threat Dashboard</h1>

      {/* Charts */}
      <div style={{
        display: "flex",
        gap: 30,
        flexWrap: "wrap",
        marginBottom: 40
      }}>
        <ThreatSeverityPie data={chartData?.threat_severity} theme={theme} />
        <ThreatByHour data={chartData?.detections_by_hour} theme={theme} />
        <DLPViolations data={chartData?.dlp_violations} theme={theme} />
        <RiskyUsers data={riskData?.risky_users} theme={theme} />
      </div>

      {/* Alerts Table */}
      <h3>Total Alerts: {alerts.length}</h3>

      <table style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: 20,
        background: isDark ? "#0f172a" : "#ffffff",
        borderRadius: 10,
        overflow: "hidden"
      }}>
        
        <thead>
          <tr style={{
            background: colors.tableHeader,
            textAlign: "left"
          }}>
            <th style={{ padding: 12 }}>User</th>
            <th style={{ padding: 12 }}>Threat Type</th>
            <th style={{ padding: 12 }}>Risk %</th>
            <th style={{ padding: 12 }}>Severity</th>
            <th style={{ padding: 12 }}>Financial Impact</th>
          </tr>
        </thead>

        <tbody>
          {alerts.map((a, i) => (
            <tr key={i} style={{
              borderBottom: `1px solid ${colors.border}`
            }}>
              <td style={{ padding: 12 }}>{a.user}</td>
              <td style={{ padding: 12 }}>{a.threat_type}</td>
              <td style={{ padding: 12 }}>{a.risk}%</td>

              <td style={{ padding: 12 }}>
                <span style={{
                  background: severityColor(a.severity),
                  padding: "4px 10px",
                  borderRadius: 20,
                  fontWeight: "bold",
                  fontSize: 13,
                  color: "white"
                }}>
                  {a.severity.toUpperCase()}
                </span>
              </td>

              <td style={{ padding: 12 }}>
                ${a.financial_impact.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>

      </table>
    </div>
  );
}