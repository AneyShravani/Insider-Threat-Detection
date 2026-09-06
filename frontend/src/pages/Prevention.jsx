import { useEffect, useState } from "react";

const API = "http://localhost:5000";

export default function Prevention() {
  const [blockedUsers, setBlockedUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [actionMsg, setActionMsg] = useState("");

  // manual block form
  const [blockUser, setBlockUser] = useState("");
  const [blockReason, setBlockReason] = useState("");
  const [blockLevel, setBlockLevel] = useState("high");

  // simulate file transfer form
  const [tUser, setTUser] = useState("");
  const [tFile, setTFile] = useState("");
  const [tMethod, setTMethod] = useState("usb");
  const [tLevel, setTLevel] = useState("high");
  const [transferResult, setTransferResult] = useState(null);

  const loadAll = () => {
    setLoading(true);
    Promise.all([
      fetch(`${API}/prevention/blocked-users`).then(r => r.json()),
      fetch(`${API}/prevention/logs`).then(r => r.json()),
      fetch(`${API}/prevention/notifications`).then(r => r.json()),
    ])
      .then(([b, l, n]) => {
        setBlockedUsers(b);
        setLogs(l);
        setNotifications(n);
      })
      .catch(() => console.log("Prevention backend not connected"))
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadAll(); }, []);

  const statusMeta = (status) => {
    if (status === 'blocked')    return { icon: '🔴', label: 'Blocked',    color: '#ef4444' };
    if (status === 'restricted') return { icon: '🟡', label: 'Restricted', color: '#f97316' };
    return { icon: '🟢', label: 'Normal', color: '#22c55e' };
  };

  const cardStyle = {
    background: "#0f172a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: 20,
  };

  const inputStyle = {
    width: "100%", padding: "10px 12px",
    background: "#1e293b", color: "white",
    border: "1px solid #334155", borderRadius: 8,
    fontSize: 14, outline: "none", marginTop: 6
  };

  const buttonStyle = (bg) => ({
    padding: "10px 18px",
    background: bg,
    color: "white",
    border: "none",
    borderRadius: 8,
    fontSize: 14,
    fontWeight: "bold",
    cursor: "pointer",
    marginTop: 14,
  });

  const counts = {
    blocked: blockedUsers.filter(u => u.status === 'blocked').length,
    restricted: blockedUsers.filter(u => u.status === 'restricted').length,
    normal: blockedUsers.filter(u => u.status === 'normal').length,
  };

  // Runs the ML + false-negative verification pass across all alerts,
  // which is what actually triggers the Threat -> Prevention pipeline
  // on the backend (see /alerts-verified in app.py).
  const runThreatScan = () => {
    setScanning(true);
    setActionMsg("");
    fetch(`${API}/alerts-verified`)
      .then(res => res.json())
      .then(data => {
        const prevented = data.filter(a => a.action_prevented).length;
        setActionMsg(`Scan complete — ${prevented} high-risk action(s) prevented across ${data.length} alerts.`);
        loadAll();
      })
      .catch(() => setActionMsg("Could not reach backend to run scan."))
      .finally(() => setScanning(false));
  };

  const handleManualBlock = (e) => {
    e.preventDefault();
    if (!blockUser.trim()) return;
    fetch(`${API}/prevention/block`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: blockUser.trim(),
        reason: blockReason.trim() || "Manually blocked by admin",
        threat_level: blockLevel,
      }),
    })
      .then(res => res.json())
      .then(data => {
        setActionMsg(data.message || "Action complete");
        setBlockUser(""); setBlockReason("");
        loadAll();
      })
      .catch(() => setActionMsg("Could not reach backend."));
  };

  const handleUnblock = (userId) => {
    fetch(`${API}/prevention/unblock`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, admin_id: "admin", note: "Verified false alarm" }),
    })
      .then(res => res.json())
      .then(data => {
        setActionMsg(data.message || "User unblocked");
        loadAll();
      })
      .catch(() => setActionMsg("Could not reach backend."));
  };

  const handleTransferCheck = (e) => {
    e.preventDefault();
    if (!tUser.trim() || !tFile.trim()) return;
    fetch(`${API}/prevention/check-transfer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: tUser.trim(),
        file_name: tFile.trim(),
        method: tMethod,
        threat_level: tLevel,
      }),
    })
      .then(res => res.json())
      .then(data => {
        setTransferResult(data);
        loadAll();
      })
      .catch(() => setActionMsg("Could not reach backend."));
  };

  return (
    <div style={{ padding: 30, background: "#020617", minHeight: "100vh", color: "white" }}>
      <h1>🛑 Prevention Engine</h1>
      <p style={{ color: "#94a3b8" }}>
        Turning a threat detection into an actual blocked action, with full admin control.
      </p>

      {loading && <p style={{ color: "#64748b" }}>Loading...</p>}

      {/* Summary stats */}
      <div style={{ display: "flex", gap: 16, margin: "20px 0 24px" }}>
        <div style={{ ...cardStyle, flex: 1 }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>🔴 Blocked Users</div>
          <div style={{ fontSize: 28, fontWeight: "bold", color: "#ef4444" }}>{counts.blocked}</div>
        </div>
        <div style={{ ...cardStyle, flex: 1 }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>🟡 Restricted Users</div>
          <div style={{ fontSize: 28, fontWeight: "bold", color: "#f97316" }}>{counts.restricted}</div>
        </div>
        <div style={{ ...cardStyle, flex: 1 }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>Prevention Log Entries</div>
          <div style={{ fontSize: 28, fontWeight: "bold" }}>{logs.length}</div>
        </div>
        <div style={{ ...cardStyle, flex: 1 }}>
          <div style={{ color: "#94a3b8", fontSize: 13 }}>Admin Notifications</div>
          <div style={{ fontSize: 28, fontWeight: "bold" }}>{notifications.length}</div>
        </div>
      </div>

      {/* Run scan button */}
      <div style={{ ...cardStyle, marginBottom: 24, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <div style={{ fontWeight: "bold" }}>Threat → Prevention Scan</div>
          <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>
            Runs current alerts through ML + false-negative verification, then auto-blocks/restricts
            any user whose final severity is medium or high.
          </div>
        </div>
        <button onClick={runThreatScan} disabled={scanning} style={buttonStyle("#3b82f6")}>
          {scanning ? "Scanning..." : "▶ Run Scan"}
        </button>
      </div>

      {actionMsg && (
        <div style={{ ...cardStyle, marginBottom: 24, color: "#38bdf8", fontSize: 14 }}>
          {actionMsg}
        </div>
      )}

      {/* Two-column: manual block + simulate transfer */}
      <div style={{ display: "flex", gap: 20, marginBottom: 30 }}>
        {/* Manual block/restrict */}
        <form onSubmit={handleManualBlock} style={{ ...cardStyle, flex: 1 }}>
          <h3 style={{ marginTop: 0 }}>Manual Block / Restrict</h3>
          <label style={{ fontSize: 13, color: "#94a3b8" }}>User ID</label>
          <input style={inputStyle} value={blockUser} onChange={e => setBlockUser(e.target.value)} placeholder="e.g. U045" />

          <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 12 }}>Reason</label>
          <input style={inputStyle} value={blockReason} onChange={e => setBlockReason(e.target.value)} placeholder="e.g. Unusual download volume" />

          <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 12 }}>Threat Level</label>
          <select style={inputStyle} value={blockLevel} onChange={e => setBlockLevel(e.target.value)}>
            <option value="high">High → Block</option>
            <option value="medium">Medium → Restrict</option>
          </select>

          <button type="submit" style={buttonStyle("#ef4444")}>Apply</button>
        </form>

        {/* Simulate file transfer */}
        <form onSubmit={handleTransferCheck} style={{ ...cardStyle, flex: 1 }}>
          <h3 style={{ marginTop: 0 }}>Simulate File Transfer</h3>
          <label style={{ fontSize: 13, color: "#94a3b8" }}>User ID</label>
          <input style={inputStyle} value={tUser} onChange={e => setTUser(e.target.value)} placeholder="e.g. U045" />

          <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 12 }}>File Name</label>
          <input style={inputStyle} value={tFile} onChange={e => setTFile(e.target.value)} placeholder="e.g. customer_data.xlsx" />

          <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: 13, color: "#94a3b8" }}>Transfer Method</label>
              <select style={inputStyle} value={tMethod} onChange={e => setTMethod(e.target.value)}>
                <option value="usb">USB</option>
                <option value="email">Email Attachment</option>
                <option value="cloud_upload">Cloud Upload</option>
                <option value="network_share">Network Share</option>
                <option value="ftp">FTP</option>
              </select>
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: 13, color: "#94a3b8" }}>Threat Level</label>
              <select style={inputStyle} value={tLevel} onChange={e => setTLevel(e.target.value)}>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
          </div>

          <button type="submit" style={buttonStyle("#3b82f6")}>Check Transfer</button>

          {transferResult && (
            <div style={{
              marginTop: 14, padding: 12, borderRadius: 8,
              background: transferResult.transfer_allowed ? "#052e16" : "#450a0a",
              color: transferResult.transfer_allowed ? "#86efac" : "#fecaca",
              fontSize: 13,
            }}>
              {transferResult.transfer_allowed
                ? `✅ Transfer allowed (action: ${transferResult.action})`
                : `🚫 Transfer blocked via ${transferResult.method}`}
            </div>
          )}
        </form>
      </div>

      {/* Blocked/restricted users table */}
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>User Prevention Status</h2>
      <div style={{ ...cardStyle, overflowX: "auto", marginBottom: 30 }}>
        {blockedUsers.length === 0 ? (
          <p style={{ color: "#64748b" }}>No users flagged yet. Run a scan or manually block a user above.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ textAlign: "left", color: "#94a3b8", borderBottom: "1px solid #1e293b" }}>
                <th style={{ padding: 8 }}>Status</th>
                <th style={{ padding: 8 }}>User</th>
                <th style={{ padding: 8 }}>Threat Level</th>
                <th style={{ padding: 8 }}>Reason</th>
                <th style={{ padding: 8 }}>Updated</th>
                <th style={{ padding: 8 }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {blockedUsers.map((u, i) => {
                const meta = statusMeta(u.status);
                return (
                  <tr key={i} style={{ borderBottom: "1px solid #1e293b" }}>
                    <td style={{ padding: 8 }}>
                      <span style={{ color: meta.color, fontWeight: "bold" }}>{meta.icon} {meta.label}</span>
                    </td>
                    <td style={{ padding: 8 }}>{u.user_id}</td>
                    <td style={{ padding: 8 }}>{u.threat_level || "—"}</td>
                    <td style={{ padding: 8, color: "#94a3b8" }}>{u.reason || "—"}</td>
                    <td style={{ padding: 8, color: "#64748b" }}>
                      {u.updated_at ? new Date(u.updated_at).toLocaleString() : "—"}
                    </td>
                    <td style={{ padding: 8 }}>
                      {u.status !== 'normal' && (
                        <button
                          onClick={() => handleUnblock(u.user_id)}
                          style={{
                            padding: "4px 10px", background: "#22c55e", color: "white",
                            border: "none", borderRadius: 6, fontSize: 12, cursor: "pointer",
                          }}
                        >
                          Unblock
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Prevention logs */}
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>Prevention Log</h2>
      <div style={{ ...cardStyle, overflowX: "auto", marginBottom: 30 }}>
        {logs.length === 0 ? (
          <p style={{ color: "#64748b" }}>No prevention actions logged yet.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ textAlign: "left", color: "#94a3b8", borderBottom: "1px solid #1e293b" }}>
                <th style={{ padding: 8 }}>Timestamp</th>
                <th style={{ padding: 8 }}>User</th>
                <th style={{ padding: 8 }}>File/Action</th>
                <th style={{ padding: 8 }}>Threat Level</th>
                <th style={{ padding: 8 }}>Reason</th>
                <th style={{ padding: 8 }}>Action Taken</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((row, i) => (
                <tr key={i} style={{ borderBottom: "1px solid #1e293b" }}>
                  <td style={{ padding: 8, color: "#64748b" }}>
                    {row.timestamp ? new Date(row.timestamp).toLocaleString() : "—"}
                  </td>
                  <td style={{ padding: 8 }}>{row.user_id}</td>
                  <td style={{ padding: 8, color: "#94a3b8" }}>
                    {row.file_or_action || "—"}{row.method ? ` (${row.method})` : ""}
                  </td>
                  <td style={{ padding: 8 }}>{row.threat_level || "—"}</td>
                  <td style={{ padding: 8, color: "#94a3b8" }}>{row.reason}</td>
                  <td style={{ padding: 8, color: row.action_taken === 'blocked' ? '#ef4444' : '#f97316' }}>
                    {row.action_taken}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Admin notifications */}
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>Admin Notifications</h2>
      <div style={{ ...cardStyle, overflowX: "auto" }}>
        {notifications.length === 0 ? (
          <p style={{ color: "#64748b" }}>No notifications sent yet.</p>
        ) : (
          notifications.map((n, i) => (
            <div key={i} style={{ padding: "10px 0", borderBottom: i < notifications.length - 1 ? "1px solid #1e293b" : "none" }}>
              <div style={{ fontWeight: "bold", fontSize: 13 }}>{n.subject}</div>
              <div style={{ color: "#64748b", fontSize: 12, marginTop: 2 }}>
                {n.simulated ? "📨 Simulated (configure SMTP_* env vars to send real email)" : "✅ Sent"} · {n.timestamp ? new Date(n.timestamp).toLocaleString() : ""}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
