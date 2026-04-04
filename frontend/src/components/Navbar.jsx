import { NavLink } from "react-router-dom";

export default function Navbar() {
  const linkStyle = ({ isActive }) => ({
    color: isActive ? "#38bdf8" : "#94a3b8",
    textDecoration: "none",
    padding: "8px 16px",
    borderRadius: 8,
    background: isActive ? "#1e293b" : "transparent",
    fontWeight: isActive ? "bold" : "normal",
    fontSize: 14
  });

  return (
    <div style={{
      width: 220,
      minHeight: "100vh",
      background: "#020617",
      borderRight: "1px solid #1e293b",
      padding: "24px 12px",
      display: "flex",
      flexDirection: "column",
      gap: 8,
      position: "fixed",
      top: 0,
      left: 0
    }}>

      {/* Logo */}
      <div style={{ marginBottom: 24, padding: "0 16px" }}>
        <div style={{ fontSize: 18, fontWeight: "bold", color: "white" }}>
          🛡️ ThreatGuard
        </div>
        <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>
          Insider Threat Detection
        </div>
      </div>

      <NavLink to="/dashboard" style={linkStyle}>📊 Dashboard</NavLink>
      <NavLink to="/alerts" style={linkStyle}>🚨 Alerts</NavLink>
      <NavLink to="/investigation" style={linkStyle}>🔍 Investigation</NavLink>
      <NavLink to="/users" style={linkStyle}>👥 Users</NavLink>
      <NavLink to="/timeline" style={linkStyle}>📅 Timeline</NavLink>
      <NavLink to="/reports" style={linkStyle}>📄 Reports</NavLink>
      <NavLink to="/behavior" style={linkStyle}>📊 Behavior</NavLink>

      {/* Logout */}
      <div style={{ marginTop: "auto" }}>
        <NavLink to="/" style={() => ({
          color: "#ef4444",
          textDecoration: "none",
          padding: "8px 16px",
          borderRadius: 8,
          fontSize: 14,
          display: "block"
        })}>
          🚪 Logout
        </NavLink>
      </div>
    </div>
  );
}