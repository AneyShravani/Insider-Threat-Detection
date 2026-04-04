import { useState, useEffect } from "react";
import FeatureImportance from "../components/charts/investigation/FeatureImportance";
import RiskScatterPlot from "../components/charts/investigation/RiskScatterPlot";

const CHART_HEIGHT = 300;

const inputStyle = {
  width: "100%",
  padding: "10px 14px",
  marginTop: 6,
  background: "#0f172a",
  color: "white",
  border: "1px solid #1e293b",
  borderRadius: 8,
  fontSize: 14,
  outline: "none",
  transition: "border-color 0.2s",
  boxSizing: "border-box",
};

const SEVERITY_CONFIG = {
  high:   { color: "#ef4444", bg: "#ef444415", icon: "🔴", label: "HIGH RISK" },
  medium: { color: "#f97316", bg: "#f9731615", icon: "🟠", label: "MEDIUM RISK" },
  low:    { color: "#22c55e", bg: "#22c55e15", icon: "🟢", label: "LOW RISK" },
};

export default function Investigation() {
  const [form, setForm] = useState({
    risk_score: "", false_positive: 0,
    response_time: "", financial_impact: ""
  });
  const [result, setResult]   = useState(null);
  const [mlData, setMlData]   = useState(null);
  const [invData, setInvData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [focusField, setFocusField] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:5000/api/ml-analysis").then(r => r.json()),
      fetch("http://localhost:5000/api/investigation-charts").then(r => r.json()),
    ]).then(([ml, inv]) => {
      setMlData(ml);
      setInvData(inv);
    });
  }, []);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    if (!form.risk_score || !form.response_time || !form.financial_impact) return;
    setLoading(true);
    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        risk_score:       parseFloat(form.risk_score),
        false_positive:   parseInt(form.false_positive),
        response_time:    parseFloat(form.response_time),
        financial_impact: parseFloat(form.financial_impact),
      }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  const sev = result ? SEVERITY_CONFIG[result.severity] : null;

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
            background: "linear-gradient(135deg, #6366f1, #4338ca)",
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18
          }}>🔍</div>
          <div>
            <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: "-0.3px" }}>
              Threat Investigation
            </h1>
            <p style={{ fontSize: 12, color: "#64748b", margin: 0 }}>
              ML-powered insider threat analysis — enter user activity to detect risk
            </p>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 16,
        marginBottom: 20,
      }}>
        <div style={{ height: CHART_HEIGHT, overflow: "hidden" }}>
          <FeatureImportance data={mlData?.feature_importance} height={CHART_HEIGHT} />
        </div>
        <div style={{ height: CHART_HEIGHT, overflow: "hidden" }}>
          <RiskScatterPlot data={invData?.scatter} height={CHART_HEIGHT} />
        </div>
      </div>

      {/* Form + Result — stretch to same height */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 16,
        alignItems: "stretch",   // KEY: both columns same height
      }}>

        {/* Form Card */}
        <div style={{
          background: "#0f172a",
          border: "1px solid #1e293b",
          borderRadius: 14,
          padding: "24px 28px",
          display: "flex",
          flexDirection: "column",
        }}>
          <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0", marginBottom: 4 }}>
            Analyze User Activity
          </div>
          <div style={{ fontSize: 12, color: "#475569", marginBottom: 20 }}>
            Input parameters for ML threat classification
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500, letterSpacing: "0.3px" }}>
              RISK SCORE <span style={{ color: "#475569" }}>(0.0 – 1.0)</span>
            </label>
            <input
              name="risk_score" type="number" step="0.01"
              placeholder="e.g. 0.85" onChange={handleChange}
              onFocus={() => setFocusField("risk_score")}
              onBlur={() => setFocusField(null)}
              style={{ ...inputStyle, borderColor: focusField === "risk_score" ? "#6366f1" : "#1e293b" }}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500, letterSpacing: "0.3px" }}>
              RESPONSE TIME <span style={{ color: "#475569" }}>(minutes)</span>
            </label>
            <input
              name="response_time" type="number"
              placeholder="e.g. 5" onChange={handleChange}
              onFocus={() => setFocusField("response_time")}
              onBlur={() => setFocusField(null)}
              style={{ ...inputStyle, borderColor: focusField === "response_time" ? "#6366f1" : "#1e293b" }}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500, letterSpacing: "0.3px" }}>
              FINANCIAL IMPACT <span style={{ color: "#475569" }}>($)</span>
            </label>
            <input
              name="financial_impact" type="number"
              placeholder="e.g. 50000" onChange={handleChange}
              onFocus={() => setFocusField("financial_impact")}
              onBlur={() => setFocusField(null)}
              style={{ ...inputStyle, borderColor: focusField === "financial_impact" ? "#6366f1" : "#1e293b" }}
            />
          </div>

          <div style={{ marginBottom: 24 }}>
            <label style={{ fontSize: 12, color: "#94a3b8", fontWeight: 500, letterSpacing: "0.3px" }}>
              FALSE POSITIVE?
            </label>
            <select
              name="false_positive" onChange={handleChange}
              onFocus={() => setFocusField("fp")}
              onBlur={() => setFocusField(null)}
              style={{ ...inputStyle, borderColor: focusField === "fp" ? "#6366f1" : "#1e293b", cursor: "pointer" }}
            >
              <option value={0}>No — Treat as real threat</option>
              <option value={1}>Yes — Mark as false positive</option>
            </select>
          </div>

          {/* Button pinned to bottom */}
          <div style={{ marginTop: "auto" }}>
            <button
              onClick={handleSubmit}
              disabled={loading}
              style={{
                width: "100%",
                padding: "13px 0",
                background: loading ? "#1e293b" : "linear-gradient(135deg, #6366f1, #4338ca)",
                color: loading ? "#475569" : "white",
                border: "none", borderRadius: 10,
                fontSize: 15, fontWeight: 600,
                cursor: loading ? "not-allowed" : "pointer",
                letterSpacing: "0.3px",
              }}
            >
              {loading ? "Analyzing..." : "🔍 Analyze Threat"}
            </button>
          </div>
        </div>

        {/* Result Card — stretches to match form height */}
        <div style={{
          background: "#0f172a",
          border: `1px solid ${sev ? sev.color + "40" : "#1e293b"}`,
          borderRadius: 14,
          padding: "24px 28px",
          display: "flex",
          flexDirection: "column",
          justifyContent: sev ? "flex-start" : "center",
          alignItems: sev ? "flex-start" : "center",
          transition: "border-color 0.3s",
        }}>

          {!sev ? (
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 52, marginBottom: 14 }}>🎯</div>
              <div style={{ fontSize: 14, color: "#334155", fontWeight: 500 }}>
                Result will appear here
              </div>
              <div style={{ fontSize: 12, color: "#1e293b", marginTop: 4 }}>
                Fill the form and click Analyze
              </div>
            </div>
          ) : (
            <div style={{ width: "100%", display: "flex", flexDirection: "column", height: "100%" }}>

              {/* Badge */}
              <div style={{
                display: "inline-flex", alignItems: "center", gap: 8,
                background: sev.bg, border: `1px solid ${sev.color}40`,
                borderRadius: 8, padding: "6px 14px", marginBottom: 16,
                alignSelf: "flex-start",
              }}>
                <span style={{ fontSize: 14 }}>{sev.icon}</span>
                <span style={{ fontSize: 13, fontWeight: 700, color: sev.color, letterSpacing: "1px" }}>
                  {sev.label}
                </span>
              </div>

              <div style={{ fontSize: 18, fontWeight: 700, color: "#e2e8f0", marginBottom: 16 }}>
                {result.message}
              </div>

              <div style={{ height: 1, background: "#1e293b", width: "100%", marginBottom: 16 }} />

              {/* Stats Grid */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, width: "100%" }}>
                {[
                  { label: "Risk Score",      value: form.risk_score || "—" },
                  { label: "Response Time",   value: form.response_time ? `${form.response_time}m` : "—" },
                  { label: "Financial Impact",value: form.financial_impact ? `$${Number(form.financial_impact).toLocaleString()}` : "—" },
                  { label: "False Positive",  value: parseInt(form.false_positive) === 1 ? "Yes" : "No" },
                ].map((item, i) => (
                  <div key={i} style={{
                    background: "#020617", borderRadius: 8,
                    padding: "14px 16px", border: "1px solid #1e293b"
                  }}>
                    <div style={{ fontSize: 11, color: "#475569", marginBottom: 6, letterSpacing: "0.3px" }}>
                      {item.label.toUpperCase()}
                    </div>
                    <div style={{ fontSize: 18, fontWeight: 600, color: "#e2e8f0" }}>
                      {item.value}
                    </div>
                  </div>
                ))}
              </div>

              {/* Severity Meter — pinned to bottom */}
              <div style={{ marginTop: "auto", paddingTop: 20, width: "100%" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                  <span style={{ fontSize: 11, color: "#475569", letterSpacing: "0.5px" }}>
                    SEVERITY METER
                  </span>
                  <span style={{ fontSize: 11, color: sev.color, fontWeight: 700 }}>
                    {result.severity === "high" ? "85%" : result.severity === "medium" ? "50%" : "20%"}
                  </span>
                </div>
                <div style={{ background: "#1e293b", borderRadius: 6, height: 8, width: "100%" }}>
                  <div style={{
                    height: "100%", borderRadius: 6,
                    background: `linear-gradient(90deg, ${sev.color}99, ${sev.color})`,
                    width: result.severity === "high" ? "85%" : result.severity === "medium" ? "50%" : "20%",
                    transition: "width 0.8s ease",
                    boxShadow: `0 0 8px ${sev.color}60`,
                  }} />
                </div>

                {/* Threat level indicators */}
                <div style={{
                  display: "flex", justifyContent: "space-between",
                  marginTop: 6,
                }}>
                  {["Low", "Medium", "High"].map((lvl, i) => (
                    <span key={i} style={{
                      fontSize: 10, color: "#334155",
                      fontWeight: result.severity === lvl.toLowerCase() ? 700 : 400,
                      color: result.severity === lvl.toLowerCase() ? sev.color : "#334155",
                    }}>{lvl}</span>
                  ))}
                </div>
              </div>

            </div>
          )}
        </div>

      </div>
    </div>
  );
}