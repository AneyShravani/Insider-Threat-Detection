import { useEffect, useState } from "react";

export default function Timeline() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/timeline")
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  const severityColor = (s) => {
    if (s === 'high')   return '#ef4444';
    if (s === 'medium') return '#f97316';
    return '#22c55e';
  };

  return (
    <div style={{ padding: 30, color: "white", background: "#020617", minHeight: "100vh" }}>
      <h1>📅 Threat Timeline</h1>
      <p style={{ color: "#94a3b8" }}>Chronological view of all detected threats</p>

      <div style={{ marginTop: 24, position: "relative" }}>
        {/* Vertical line */}
        <div style={{
          position: "absolute", left: 16,
          top: 0, bottom: 0,
          width: 2, background: "#1e293b"
        }} />

        {events.map((e, i) => (
          <div key={i} style={{ display: "flex", gap: 20, marginBottom: 24, position: "relative" }}>
            {/* Dot */}
            <div style={{
              width: 14, height: 14, borderRadius: "50%",
              background: severityColor(e.severity),
              marginTop: 4, flexShrink: 0,
              zIndex: 1, marginLeft: 10
            }} />

            {/* Content */}
            <div style={{
              background: "#0f172a",
              border: `1px solid #1e293b`,
              borderRadius: 10, padding: 16, flex: 1
            }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong>{e.user_id} — {e.threat_type}</strong>
                <span style={{
                  background: severityColor(e.severity),
                  padding: "2px 10px", borderRadius: 20,
                  fontSize: 12, fontWeight: "bold"
                }}>
                  {e.severity.toUpperCase()}
                </span>
              </div>
              <div style={{ color: "#64748b", fontSize: 13, marginTop: 6 }}>
                🕐 {e.detection_time}
              </div>
              <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>
                Outcome: {e.outcome} | Risk: {Math.round(e.risk_score * 100)}%
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}