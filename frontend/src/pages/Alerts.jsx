import { useEffect, useState } from "react";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [blockedUsers, setBlockedUsers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/alerts")
      .then(res => res.json())
      .then(data => setAlerts(data))
      .catch(() => console.log("Backend not connected"));

    // Objective 6: pull current prevention status so we can flag
    // alerts whose user has already been blocked/restricted.
    fetch("http://localhost:5000/prevention/blocked-users")
      .then(res => res.json())
      .then(data => setBlockedUsers(data))
      .catch(() => console.log("Prevention backend not connected"));
  }, []);

  const borderColor = (severity) => {
    if (severity === 'high')   return '#ef4444';
    if (severity === 'medium') return '#f97316';
    return '#22c55e';
  };

  // Objective 4: Prioritize alerts based on threat severity.
  // High severity alerts are shown first, then medium, then low —
  // instead of the raw dataset row order.
  const severityRank = { high: 0, medium: 1, low: 2 };
  const sortedAlerts = [...alerts].sort(
    (a, b) => (severityRank[a.severity] ?? 3) - (severityRank[b.severity] ?? 3)
  );

  const preventionFor = (userId) =>
    blockedUsers.find(u => u.user_id === userId);

  return (
    <div style={{ padding: 30, background: "#020617", minHeight: "100vh", color: "white" }}>
      <h1>🚨 Alerts</h1>
      <p style={{ color: "#94a3b8" }}>
        Total: {alerts.length} alerts detected — sorted by severity (High → Medium → Low)
      </p>

      {sortedAlerts.map((a, i) => {
        const prevention = preventionFor(a.user);
        const wasBlocked = prevention?.status === 'blocked';
        const wasRestricted = prevention?.status === 'restricted';

        return (
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

            {(wasBlocked || wasRestricted) && (
              <div style={{
                marginTop: 8,
                display: "inline-block",
                background: wasBlocked ? "#7f1d1d" : "#78350f",
                color: wasBlocked ? "#fecaca" : "#fde68a",
                padding: "3px 10px",
                borderRadius: 6,
                fontSize: 12,
                fontWeight: "bold"
              }}>
                {wasBlocked ? "🛑 Action Prevented" : "🟡 User Restricted"}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}