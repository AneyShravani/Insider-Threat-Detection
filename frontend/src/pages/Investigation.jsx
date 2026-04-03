import { useState } from "react";

export default function Investigation() {
  const [form, setForm] = useState({
    risk_score: '',
    false_positive: 0,
    response_time: '',
    financial_impact: ''
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        risk_score: parseFloat(form.risk_score),
        false_positive: parseInt(form.false_positive),
        response_time: parseFloat(form.response_time),
        financial_impact: parseFloat(form.financial_impact)
      })
    });
    const data = await res.json();
    setResult(data);
  };

  const inputStyle = {
    width: "100%", padding: 10, marginTop: 6,
    background: "#1e293b", color: "white",
    border: "1px solid #334155", borderRadius: 8
  };

  return (
    <div style={{ padding: 30, color: "white", background: "#020617", minHeight: "100vh" }}>
      <h1>🔍 Threat Investigation</h1>
      <p style={{ color: "#94a3b8" }}>Enter user activity details to detect insider threats</p>

      <div style={{ maxWidth: 500, marginTop: 20 }}>
        <label>Risk Score (0.0 to 1.0)</label>
        <input name="risk_score" type="number" step="0.01"
          placeholder="e.g. 0.85" style={inputStyle} onChange={handleChange} />

        <label style={{ marginTop: 16, display: "block" }}>Response Time (minutes)</label>
        <input name="response_time" type="number"
          placeholder="e.g. 5" style={inputStyle} onChange={handleChange} />

        <label style={{ marginTop: 16, display: "block" }}>Financial Impact ($)</label>
        <input name="financial_impact" type="number"
          placeholder="e.g. 50000" style={inputStyle} onChange={handleChange} />

        <label style={{ marginTop: 16, display: "block" }}>False Positive?</label>
        <select name="false_positive" style={inputStyle} onChange={handleChange}>
          <option value={0}>No</option>
          <option value={1}>Yes</option>
        </select>

        <button onClick={handleSubmit} style={{
          marginTop: 20, padding: "12px 30px",
          background: "#3b82f6", color: "white",
          border: "none", borderRadius: 8,
          fontSize: 16, cursor: "pointer"
        }}>
          🔍 Analyze Threat
        </button>

        {result && (
          <div style={{
            marginTop: 24, padding: 20,
            background: "#1e293b", borderRadius: 12,
            borderLeft: `5px solid ${result.color}`
          }}>
            <h2 style={{ color: result.color }}>{result.message}</h2>
            <p>Severity Level: <strong style={{ color: result.color }}>
              {result.severity.toUpperCase()}
            </strong></p>
          </div>
        )}
      </div>
    </div>
  );
}