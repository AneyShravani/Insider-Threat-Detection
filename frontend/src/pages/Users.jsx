import { useEffect, useState } from "react";

export default function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/users")
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  const severityColor = (s) => {
    if (s === 'high') return '#ef4444';
    if (s === 'medium') return '#f97316';
    return '#22c55e';
  };

  const styles = {
    page: {
      padding: 30,
      background: "#020617",
      minHeight: "100vh",
      color: "white"
    },
    card: (severity) => ({
      background: "#0f172a",
      border: `1px solid ${severityColor(severity)}40`,
      borderRadius: 12,
      padding: 20
    }),
    subText: {
      color: "#94a3b8"
    }
  };

  return (
    <div style={styles.page}>
      <h1>👥 Users</h1>
      <p style={styles.subText}>All users monitored by the system</p>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
        gap: 16,
        marginTop: 24
      }}>
        {users.map((u, i) => (
          <div key={i} style={styles.card(u.severity)}>

            {/* Header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h3 style={{ margin: 0 }}>👤 {u.user_id}</h3>

              <span style={{
                background: severityColor(u.severity),
                padding: "4px 10px",
                borderRadius: 20,
                fontSize: 12,
                fontWeight: "bold",
                color: "white"
              }}>
                {u.severity.toUpperCase()}
              </span>
            </div>

            {/* Info */}
            <div style={{ marginTop: 12, fontSize: 14, ...styles.subText }}>
              <p>🎯 <strong style={{ color: "white" }}>Threat:</strong> {u.threat_type}</p>
              <p>📊 <strong style={{ color: "white" }}>Risk Score:</strong> {Math.round(u.risk_score * 100)}%</p>
              <p>🔧 <strong style={{ color: "white" }}>Mitigation:</strong> {u.mitigation}</p>
              <p>✅ <strong style={{ color: "white" }}>Outcome:</strong> {u.outcome}</p>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}