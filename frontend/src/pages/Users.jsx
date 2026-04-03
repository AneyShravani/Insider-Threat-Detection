import { useEffect, useState } from "react";

export default function Users({ theme }) {
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
      background: theme === "dark" ? "#020617" : "#f1f5f9",
      minHeight: "100vh",
      color: theme === "dark" ? "white" : "#020617"
    },
    card: (severity) => ({
      background: theme === "dark" ? "#0f172a" : "#ffffff",
      border: `1px solid ${severityColor(severity)}40`,
      borderRadius: 12,
      padding: 20,
      boxShadow: theme === "light" ? "0 2px 8px rgba(0,0,0,0.1)" : "none"
    }),
    subText: {
      color: theme === "dark" ? "#94a3b8" : "#475569"
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
              <p>🎯 <strong style={{ color: theme === "dark" ? "white" : "#020617" }}>Threat:</strong> {u.threat_type}</p>
              <p>📊 <strong style={{ color: theme === "dark" ? "white" : "#020617" }}>Risk Score:</strong> {Math.round(u.risk_score * 100)}%</p>
              <p>🔧 <strong style={{ color: theme === "dark" ? "white" : "#020617" }}>Mitigation:</strong> {u.mitigation}</p>
              <p>✅ <strong style={{ color: theme === "dark" ? "white" : "#020617" }}>Outcome:</strong> {u.outcome}</p>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}