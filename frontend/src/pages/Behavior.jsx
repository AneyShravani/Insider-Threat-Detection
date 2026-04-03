import { useEffect, useState } from "react";

export default function Behavior() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/behavior")
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  const riskColor = (score) => {
    if (score >= 0.7) return '#ef4444';
    if (score >= 0.4) return '#f97316';
    return '#22c55e';
  };

  return (
    <div style={{ padding: 30, color: "white", background: "#020617", minHeight: "100vh" }}>
      <h1>📊 User Behavior Analysis</h1>
      <p style={{ color: "#94a3b8" }}>Monitoring user activity patterns and detecting anomalies</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(350px, 1fr))", gap: 20, marginTop: 24 }}>
        {users.map((u, i) => (
          <div key={i} style={{
            background: "#0f172a",
            border: `1px solid ${riskColor(u.avg_risk_score)}40`,
            borderRadius: 12, padding: 20
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h3 style={{ margin: 0 }}>👤 {u.user_id}</h3>
              <span style={{
                background: riskColor(u.avg_risk_score),
                padding: "4px 12px", borderRadius: 20,
                fontWeight: "bold", fontSize: 13
              }}>
                Risk: {u.avg_risk_score}
              </span>
            </div>

            <div style={{ marginTop: 16, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
              <div style={{ background: "#1e293b", padding: 10, borderRadius: 8 }}>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Total Activities</div>
                <div style={{ fontSize: 22, fontWeight: "bold" }}>{u.total_activities}</div>
              </div>
              <div style={{ background: "#1e293b", padding: 10, borderRadius: 8 }}>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Anomalies</div>
                <div style={{ fontSize: 22, fontWeight: "bold", color: u.anomalies_detected > 0 ? '#ef4444' : '#22c55e' }}>
                  {u.anomalies_detected}
                </div>
              </div>
              <div style={{ background: "#1e293b", padding: 10, borderRadius: 8 }}>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Common Activity</div>
                <div style={{ fontSize: 13, fontWeight: "bold", marginTop: 4 }}>{u.most_common_activity}</div>
              </div>
              <div style={{ background: "#1e293b", padding: 10, borderRadius: 8 }}>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Data Types</div>
                <div style={{ fontSize: 22, fontWeight: "bold" }}>{u.data_types_accessed}</div>
              </div>
            </div>

            <div style={{ marginTop: 12 }}>
              <div style={{ color: "#94a3b8", fontSize: 12, marginBottom: 6 }}>Locations</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {u.locations.map((loc, j) => (
                  <span key={j} style={{
                    background: "#1e293b", padding: "2px 8px",
                    borderRadius: 12, fontSize: 12
                  }}>{loc}</span>
                ))}
              </div>
            </div>

            {u.anomalies_detected > 0 && (
              <div style={{
                marginTop: 12, padding: 10,
                background: "#450a0a", borderRadius: 8,
                color: "#ef4444", fontSize: 13
              }}>
                {u.anomalies_detected} suspicious activities detected!
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}