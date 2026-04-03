import { useEffect, useState } from "react";

export default function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/users")
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  const severityColor = (s) => {
    if (s === 'high')   return '#ef4444';
    if (s === 'medium') return '#f97316';
    return '#22c55e';
  };

  return (
    <div style={{ padding: 30, color: "white", background: "#020617", minHeight: "100vh" }}>
      <h1>👥 Users</h1>
      <p style={{ color: "#94a3b8" }}>All users monitored by the system</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16, marginTop: 24 }}>
        {users.map((u, i) => (
          <div key={i} style={{
            background: "#0f172a",
            border: `1px solid ${severityColor(u.severity)}40`,
            borderRadius: 12, padding: 20
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h3 style={{ margin: 0 }}>👤 {u.user_id}</h3>
              <span style={{
                background: severityColor(u.severity),
                padding: "3px 10px", borderRadius: 20,
                fontSize: 12, fontWeight: "bold"
              }}>
                {u.severity.toUpperCase()}
              </span>
            </div>

            <div style={{ marginTop: 12, fontSize: 14, color: "#94a3b8" }}>
              <p style={{ margin: "6px 0" }}>🎯 <strong style={{ color: "white" }}>Threat:</strong> {u.threat_type}</p>
              <p style={{ margin: "6px 0" }}>📊 <strong style={{ color: "white" }}>Risk Score:</strong> {Math.round(u.risk_score * 100)}%</p>
              <p style={{ margin: "6px 0" }}>🔧 <strong style={{ color: "white" }}>Mitigation:</strong> {u.mitigation}</p>
              <p style={{ margin: "6px 0" }}>✅ <strong style={{ color: "white" }}>Outcome:</strong> {u.outcome}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}