import { useEffect, useState } from "react";

export default function FalseNegatives() {
  const [alerts, setAlerts] = useState([]);
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:5000/alerts-verified").then(res => res.json()),
      fetch("http://localhost:5000/false-negatives").then(res => res.json()),
    ])
      .then(([alertsData, logData]) => {
        setAlerts(alertsData);
        setLog(logData);
      })
      .catch(() => console.log("Backend not connected"))
      .finally(() => setLoading(false));
  }, []);

  const overridden = alerts.filter(a => a.fn_overridden);
  const severityColor = (severity) => {
    if (severity === 'high')   return '#ef4444';
    if (severity === 'medium') return '#f97316';
    return '#22c55e';
  };

  const cardStyle = {
    background: "#0f172a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: 20,
  };

  return (
    <div style={{ padding: 30, background: "#020617", minHeight: "100vh", color: "white" }}>
      <h1>🛡️ False Negative Reduction</h1>
      <p style={{ color: "#94a3b8" }}>
        Cases the ML model called "Normal" that the Risk Verification layer flagged as real threats.
      </p>

      {loading && <p style={{ color: "#64748b" }}>Loading...</p>}

      {/* Summary stats */}
      <div style={{ display: "flex", gap: 16, margin: "20px 0 30px" }}>
        <div style={{ ...cardStyle, flex: 1 }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>Total Cases Checked</div>
          <div style={{ fontSize: 28, fontWeight: "bold" }}>{alerts.length}</div>
        </div>
        <div style={{ ...cardStyle, flex: 1, borderColor: overridden.length > 0 ? "#ef4444" : "#1e293b" }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>False Negatives Caught</div>
          <div style={{ fontSize: 28, fontWeight: "bold", color: overridden.length > 0 ? "#ef4444" : "white" }}>
            {overridden.length}
          </div>
        </div>
        <div style={{ ...cardStyle, flex: 1 }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>Logged Events</div>
          <div style={{ fontSize: 28, fontWeight: "bold" }}>{log.length}</div>
        </div>
      </div>

      {!loading && overridden.length === 0 && (
        <div style={{ ...cardStyle, color: "#94a3b8" }}>
          No false negatives caught in the current dataset run. This means every case the ML model
          predicted as "Normal" also passed the risk verification checks. If you expected an override,
          confirm the Flask backend is running the updated app.py.
        </div>
      )}

      {overridden.length > 0 && (
        <>
          <h2 style={{ fontSize: 18, marginBottom: 12 }}>Overridden Cases</h2>
          {overridden.map((a, i) => (
            <div key={i} style={{
              ...cardStyle,
              marginBottom: 10,
              borderLeft: `5px solid ${severityColor(a.fn_final_severity)}`,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
                  <strong>User:</strong> {a.user} &nbsp;|&nbsp;
                  <strong>Threat Type:</strong> {a.threat_type}
                </div>
                <span style={{
                  background: severityColor(a.fn_final_severity),
                  padding: "2px 12px",
                  borderRadius: 20,
                  fontSize: 12,
                  fontWeight: "bold"
                }}>
                  {a.fn_final_severity?.toUpperCase()}
                </span>
              </div>

              <div style={{ marginTop: 10, fontSize: 13, color: "#94a3b8" }}>
                <div>Original ML Prediction: <span style={{ color: "#22c55e" }}>{a.severity} (Normal)</span></div>
                <div>Verified Decision: <span style={{ color: "#ef4444" }}>{a.fn_final_decision}</span></div>
                <div>Risk Score: {a.fn_risk_score}</div>
                <div>Probability Outside Normal: {a.fn_probability_threat != null ? (a.fn_probability_threat * 100).toFixed(1) + "%" : "N/A"}</div>
                <div>Triggered Rules: {a.fn_triggered_rules?.join(", ") || "none"}</div>
              </div>
            </div>
          ))}
        </>
      )}

      <h2 style={{ fontSize: 18, margin: "30px 0 12px" }}>False Negative Log</h2>
      <div style={{ ...cardStyle, overflowX: "auto" }}>
        {log.length === 0 ? (
          <p style={{ color: "#64748b" }}>logs/false_negative_log.csv is empty — visit the Alerts-Verified check above to populate it.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ textAlign: "left", color: "#94a3b8", borderBottom: "1px solid #1e293b" }}>
                <th style={{ padding: 8 }}>Timestamp</th>
                <th style={{ padding: 8 }}>User</th>
                <th style={{ padding: 8 }}>ML Prediction</th>
                <th style={{ padding: 8 }}>Risk Score</th>
                <th style={{ padding: 8 }}>Triggered Rules</th>
                <th style={{ padding: 8 }}>Final Decision</th>
              </tr>
            </thead>
            <tbody>
              {log.map((row, i) => (
                <tr key={i} style={{ borderBottom: "1px solid #1e293b" }}>
                  <td style={{ padding: 8, color: "#64748b" }}>{row.timestamp}</td>
                  <td style={{ padding: 8 }}>{row.user_id}</td>
                  <td style={{ padding: 8 }}>{row.ml_prediction}</td>
                  <td style={{ padding: 8 }}>{row.risk_score}</td>
                  <td style={{ padding: 8, color: "#94a3b8" }}>{row.triggered_rules}</td>
                  <td style={{ padding: 8, color: "#ef4444" }}>{row.final_decision}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
