import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";
import Users from "./pages/Users";
import Investigation from "./pages/Investigation";
import Timeline from "./pages/Timeline";
import Reports from "./pages/Reports";
import Behavior from "./pages/Behavior";

function Layout() {
  const location = useLocation();
  const hideNavbar = location.pathname === "/";

  return (
    <div style={{
      display: "flex",
      background: "#020617",
      minHeight: "100vh",
      color: "white"
    }}>
      {!hideNavbar && <Navbar />}

      <div style={{ marginLeft: hideNavbar ? 0 : 220, flex: 1 }}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/users" element={<Users />} />
          <Route path="/investigation" element={<Investigation />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/behavior" element={<Behavior />} />
        </Routes>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}