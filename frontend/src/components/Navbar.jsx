import { NavLink } from "react-router-dom";

export default function Navbar({ theme, toggleTheme }) {
  const isDark = theme === "dark";

  const sidebarBg = isDark ? "#0f172a" : "#ffffff";
  const borderColor = isDark ? "#1e293b" : "#e2e8f0";
  const textColor = isDark ? "white" : "#020617";
  const subText = "#64748b";

  const linkStyle = ({ isActive }) => ({
    color: isActive ? "#38bdf8" : (isDark ? "#94a3b8" : "#475569"),
    textDecoration: "none",
    padding: "8px 16px",
    borderRadius: 8,
    background: isActive ? (isDark ? "#1e293b" : "#e2e8f0") : "transparent",
    fontWeight: isActive ? "bold" : "normal",
    fontSize: 14
  });

  return (
    <div style={{
      width: 220,
      minHeight: "100vh",
      background: sidebarBg,
      borderRight: `1px solid ${borderColor}`,
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
        <div style={{ fontSize: 18, fontWeight: "bold", color: textColor }}>
          🛡️ ThreatGuard
        </div>
        <div style={{ fontSize: 11, color: subText, marginTop: 4 }}>
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

      {/* Theme Button */}
      <button
        onClick={toggleTheme}
        style={{
          marginTop: 20,
          padding: "8px 12px",
          borderRadius: 8,
          border: "none",
          cursor: "pointer",
          background: isDark ? "#1e293b" : "#e2e8f0",
          color: textColor
        }}
      >
        {isDark ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>

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