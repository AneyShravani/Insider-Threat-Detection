function Layout({ theme, toggleTheme }) {
  const location = useLocation();
  const hideNavbar = location.pathname === "/";

  return (
    <div
      style={{
        display: "flex",
        background: theme === "dark" ? "#020617" : "#f1f5f9",
        minHeight: "100vh",
        color: theme === "dark" ? "white" : "#020617"
      }}
    >
      {!hideNavbar && (
        <Navbar theme={theme} toggleTheme={toggleTheme} />
      )}

      <div style={{ marginLeft: hideNavbar ? 0 : 220, flex: 1 }}>
        <Routes>
          {/* 🔥 IMPORTANT: Login should NOT depend on theme */}
          <Route path="/" element={<Login />} />

          {/* बाकी pages get theme */}
          <Route path="/dashboard" element={<Dashboard theme={theme} />} />
          <Route path="/alerts" element={<Alerts theme={theme} />} />
          <Route path="/users" element={<Users theme={theme} />} />
          <Route path="/investigation" element={<Investigation theme={theme} />} />
          <Route path="/timeline" element={<Timeline theme={theme} />} />
          <Route path="/reports" element={<Reports theme={theme} />} />
          <Route path="/behavior" element={<Behavior theme={theme} />} />
        </Routes>
      </div>
    </div>
  );
}