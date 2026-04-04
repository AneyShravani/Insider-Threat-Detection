import { useEffect, useState } from "react";
import UEBAActivity from "../components/charts/behavior/UEBAActivity";
import MalwareImpact from "../components/charts/behavior/MalwareImpact";

const CHART_HEIGHT = 300;

const riskColor = (score) => {
  if (score >= 0.7) return "#ef4444";
  if (score >= 0.4) return "#f97316";
  return "#22c55e";
};

export default function Behavior() {
  const [users, setUsers]         = useState([]);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:5000/behavior").then(r => r.json()),
      fetch("http://localhost:5000/api/behavior-charts").then(r => r.json()),
    ]).then(([userData, charts]) => {
      setUsers(userData);
      setChartData(charts);
    });
  }, []);

  return (
    <div style={{
      padding: "28px 32px",
      color: "white",
      background: "#020617",
      minHeight: "100vh",
      fontFamily: "'Inter', sans-serif",
    }}>

      {/* Header */}
      <div style={{ marginBottom: 28, borderBottom: "1px solid #1e293b", paddingBottom: 18 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 8,
            background: "linear-gradient(135deg, #10b981, #059669)",
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18
          }}>📊</div>
          <div>
            <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: "-0.3px" }}>
              User Behavior Analysis
            </h1>
            <p style={{ fontSize: 12, color: "#64748b", margin: 0 }}>
              Monitoring activity patterns and detecting anomalies
            </p>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 16,
        marginBottom: 28,
      }}>
        <div style={{ height: CHART_HEIGHT, overflow: "hidden" }}>
          <UEBAActivity data={chartData?.ueba_activity} height={CHART_HEIGHT} />
        </div>
        <div style={{ height: CHART_HEIGHT, overflow: "hidden" }}>
          <MalwareImpact data={chartData?.malware_impact} height={CHART_HEIGHT} />
        </div>
      </div>

      {/* User Cards */}
      <div style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0", marginBottom: 4 }}>
          User Risk Profiles
        </div>
        <div style={{ fontSize: 12, color: "#475569" }}>
          {users.length} users monitored — click a card to investigate
        </div>
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))",
        gap: 16,
      }}>
        {users.map((u, i) => {
          const rc = riskColor(u.avg_risk_score);
          return (
            <div key={i} style={{
              background: "#0f172a",
              border: `1px solid ${rc}30`,
              borderRadius: 14,
              padding: "20px 22px",
              position: "relative",
              overflow: "hidden",
              transition: "border-color 0.2s",
            }}>
              {/* Top accent bar */}
              <div style={{
                position: "absolute", top: 0, left: 0, right: 0,
                height: 3, background: rc, borderRadius: "14px 14px 0 0"
              }} />

              {/* Card Header */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={{
                    width: 36, height: 36, borderRadius: "50%",
                    background: `${rc}20`, border: `1px solid ${rc}40`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 16,
                  }}>👤</div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 15, color: "#e2e8f0" }}>{u.user_id}</div>
                    <div style={{ fontSize: 11, color: "#475569" }}>{u.most_common_activity}</div>
                  </div>
                </div>
                <div style={{
                  background: `${rc}20`, border: `1px solid ${rc}40`,
                  padding: "4px 12px", borderRadius: 20,
                  fontSize: 12, fontWeight: 700, color: rc,
                }}>
                  {u.avg_risk_score} Risk
                </div>
              </div>

              {/* Stats Grid */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 14 }}>
                {[
                  { label: "Total Activities", value: u.total_activities, color: "#e2e8f0" },
                  { label: "Anomalies",         value: u.anomalies_detected, color: u.anomalies_detected > 0 ? "#ef4444" : "#22c55e" },
                  { label: "Data Types",        value: u.data_types_accessed, color: "#e2e8f0" },
                  { label: "Locations",         value: u.locations.length, color: "#e2e8f0" },
                ].map((stat, j) => (
                  <div key={j} style={{
                    background: "#020617", borderRadius: 8,
                    padding: "10px 12px", border: "1px solid #1e293b"
                  }}>
                    <div style={{ fontSize: 11, color: "#475569", marginBottom: 4 }}>{stat.label.toUpperCase()}</div>
                    <div style={{ fontSize: 20, fontWeight: 700, color: stat.color }}>{stat.value}</div>
                  </div>
                ))}
              </div>

              {/* Locations */}
              <div style={{ marginBottom: u.anomalies_detected > 0 ? 12 : 0 }}>
                <div style={{ fontSize: 11, color: "#475569", marginBottom: 6, letterSpacing: "0.3px" }}>
                  LOCATIONS
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {u.locations.map((loc, j) => (
                    <span key={j} style={{
                      background: "#1e293b", border: "1px solid #334155",
                      padding: "3px 10px", borderRadius: 12,
                      fontSize: 11, color: "#94a3b8"
                    }}>{loc}</span>
                  ))}
                </div>
              </div>

              {/* Anomaly Warning */}
              {u.anomalies_detected > 0 && (
                <div style={{
                  marginTop: 12, padding: "10px 14px",
                  background: "#ef444410", border: "1px solid #ef444430",
                  borderRadius: 8, color: "#ef4444", fontSize: 13,
                  display: "flex", alignItems: "center", gap: 8,
                }}>
                  <span>⚠️</span>
                  <span>{u.anomalies_detected} suspicious {u.anomalies_detected === 1 ? "activity" : "activities"} detected</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}