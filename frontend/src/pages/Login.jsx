import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");

  const handleLogin = () => {
    if (username === "admin" && password === "admin123") {
      navigate("/dashboard");
    } else {
      setError("Invalid credentials! Use admin / admin123");
    }
  };

  const inputStyle = {
    width: "100%", padding: "12px 16px",
    background: "#1e293b", color: "white",
    border: "1px solid #334155", borderRadius: 8,
    fontSize: 15, outline: "none", marginTop: 6
  };

  return (
    <div style={{
      height: "100vh", display: "flex",
      justifyContent: "center", alignItems: "center",
      background: "#020617", color: "white"
    }}>
      <div style={{
        background: "#0f172a", padding: 40,
        borderRadius: 16, width: 380,
        border: "1px solid #1e293b",
        boxShadow: "0 0 40px rgba(56,189,248,0.1)"
      }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div style={{ fontSize: 48 }}>🛡️</div>
          <h2 style={{ margin: "8px 0 4px", fontSize: 24 }}>ThreatGuard</h2>
          <p style={{ color: "#64748b", margin: 0, fontSize: 14 }}>
            Insider Threat Detection System
          </p>
        </div>

        {/* Form */}
        <label style={{ fontSize: 13, color: "#94a3b8" }}>Username</label>
        <input
          style={inputStyle}
          placeholder="Enter username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
          Password
        </label>
        <input
          style={inputStyle}
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleLogin()}
        />

        {error && (
          <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
            ⚠️ {error}
          </div>
        )}

        <button onClick={handleLogin} style={{
          width: "100%", marginTop: 24,
          padding: "13px", background: "#3b82f6",
          color: "white", border: "none",
          borderRadius: 8, fontSize: 16,
          cursor: "pointer", fontWeight: "bold"
        }}>
          Login →
        </button>

        <p style={{ textAlign: "center", color: "#475569", fontSize: 12, marginTop: 16 }}>
          Demo: admin / admin123
        </p>
      </div>
    </div>
  );
}