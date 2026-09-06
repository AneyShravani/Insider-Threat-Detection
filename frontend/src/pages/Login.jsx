import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const navigate = useNavigate();

  // ---- Existing login state ----
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");

  // ---- Forgot Password + OTP state ----
  const [view, setView] = useState("login"); // login | forgotEmail | forgotOtp | forgotReset | success | register | registerSuccess
  const [resetEmail, setResetEmail]     = useState("");
  const [generatedOtp, setGeneratedOtp] = useState("");
  const [otpInput, setOtpInput]         = useState("");
  const [newPassword, setNewPassword]         = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [flowError, setFlowError] = useState("");

  // ---- Register state ----
  // In-memory list of accounts created this session (resets on page reload)
  const [registeredUsers, setRegisteredUsers] = useState([]);
  const [regFullName, setRegFullName] = useState("");
  const [regUsername, setRegUsername] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConfirmPassword, setRegConfirmPassword] = useState("");
  const [regError, setRegError] = useState("");

  const handleLogin = () => {
    const isDefaultAdmin = username === "admin" && password === "admin123";
    const matchedUser = registeredUsers.find(
      u => u.username === username && u.password === password
    );

    if (isDefaultAdmin || matchedUser) {
      navigate("/dashboard");
    } else {
      setError("Invalid credentials! Use admin / admin123");
    }
  };

  // Generates a random 6-digit code and "sends" it (demo: shows it on screen + console)
  const generateAndShowOtp = () => {
    const code = Math.floor(100000 + Math.random() * 900000).toString();
    setGeneratedOtp(code);
    console.log("DEMO OTP (would be emailed in production):", code);
    return code;
  };

  const handleSendOtp = () => {
    setFlowError("");
    if (!resetEmail.trim()) {
      setFlowError("Please enter your registered email/username.");
      return;
    }
    generateAndShowOtp();
    setOtpInput("");
    setView("forgotOtp");
  };

  const handleResendOtp = () => {
    setFlowError("");
    generateAndShowOtp();
    setOtpInput("");
  };

  const handleVerifyOtp = () => {
    setFlowError("");
    if (otpInput.trim() === generatedOtp) {
      setNewPassword("");
      setConfirmPassword("");
      setView("forgotReset");
    } else {
      setFlowError("Incorrect OTP. Please try again.");
    }
  };

  const handleResetPassword = () => {
    setFlowError("");
    if (!newPassword || !confirmPassword) {
      setFlowError("Please fill in both password fields.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setFlowError("Passwords do not match.");
      return;
    }
    // NOTE: Frontend-only demo. A production version would call the
    // Flask backend here to actually update the stored password.
    setView("success");
  };

  // ---- Register handlers ----
  const handleRegister = () => {
    setRegError("");

    if (!regFullName.trim() || !regUsername.trim() || !regPassword || !regConfirmPassword) {
      setRegError("Please fill in all fields.");
      return;
    }
    if (regPassword !== regConfirmPassword) {
      setRegError("Passwords do not match.");
      return;
    }
    if (regUsername === "admin" || registeredUsers.some(u => u.username === regUsername)) {
      setRegError("That username is already taken.");
      return;
    }

    // Save the new account in memory so it can be used to log in this session
    setRegisteredUsers(prev => [
      ...prev,
      { fullName: regFullName, username: regUsername, password: regPassword }
    ]);

    setView("registerSuccess");
  };

  const goToRegister = () => {
    setRegFullName("");
    setRegUsername("");
    setRegPassword("");
    setRegConfirmPassword("");
    setRegError("");
    setView("register");
  };

  const backToLogin = () => {
    setView("login");
    setResetEmail("");
    setGeneratedOtp("");
    setOtpInput("");
    setNewPassword("");
    setConfirmPassword("");
    setFlowError("");
    setError("");
  };

  const inputStyle = {
    width: "100%", padding: "12px 16px",
    background: "#1e293b", color: "white",
    border: "1px solid #334155", borderRadius: 8,
    fontSize: 15, outline: "none", marginTop: 6
  };

  const buttonStyle = {
    width: "100%", marginTop: 24,
    padding: "13px", background: "#3b82f6",
    color: "white", border: "none",
    borderRadius: 8, fontSize: 16,
    cursor: "pointer", fontWeight: "bold"
  };

  const linkStyle = {
    color: "#38bdf8", cursor: "pointer",
    fontSize: 13, textDecoration: "underline"
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
        {/* Header (same on every screen) */}
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div style={{ fontSize: 48 }}>🛡️</div>
          <h2 style={{ margin: "8px 0 4px", fontSize: 24 }}>ThreatGuard</h2>
          <p style={{ color: "#64748b", margin: 0, fontSize: 14 }}>
            Insider Threat Detection System
          </p>
        </div>

        {/* ---------------- LOGIN VIEW ---------------- */}
        {view === "login" && (
          <>
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

            <button onClick={handleLogin} style={buttonStyle}>
              Login →
            </button>

            <p style={{ textAlign: "center", marginTop: 16, marginBottom: 4 }}>
              <span style={linkStyle} onClick={() => setView("forgotEmail")}>
                Forgot Password?
              </span>
            </p>

            <p style={{ textAlign: "center", color: "#94a3b8", fontSize: 13, marginTop: 4 }}>
              New user?{" "}
              <span style={linkStyle} onClick={goToRegister}>
                Create an account
              </span>
            </p>

            <p style={{ textAlign: "center", color: "#475569", fontSize: 12, marginTop: 8 }}>
              Demo: admin / admin123
            </p>
          </>
        )}

        {/* ---------------- REGISTER VIEW ---------------- */}
        {view === "register" && (
          <>
            <h3 style={{ marginTop: 0 }}>Create an account</h3>

            <label style={{ fontSize: 13, color: "#94a3b8" }}>Full Name</label>
            <input
              style={inputStyle}
              placeholder="Enter your full name"
              value={regFullName}
              onChange={e => setRegFullName(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              Username
            </label>
            <input
              style={inputStyle}
              placeholder="Choose a username"
              value={regUsername}
              onChange={e => setRegUsername(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              Password
            </label>
            <input
              style={inputStyle}
              type="password"
              placeholder="Choose a password"
              value={regPassword}
              onChange={e => setRegPassword(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              Confirm Password
            </label>
            <input
              style={inputStyle}
              type="password"
              placeholder="Re-enter password"
              value={regConfirmPassword}
              onChange={e => setRegConfirmPassword(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleRegister()}
            />

            {regError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {regError}
              </div>
            )}

            <button onClick={handleRegister} style={buttonStyle}>
              Create Account
            </button>

            <p style={{ textAlign: "center", marginTop: 16 }}>
              <span style={linkStyle} onClick={backToLogin}>
                Back to Login
              </span>
            </p>
          </>
        )}

        {/* ---------------- REGISTER SUCCESS ---------------- */}
        {view === "registerSuccess" && (
          <>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 40, marginBottom: 8 }}>✅</div>
              <h3>Account created!</h3>
              <p style={{ color: "#94a3b8", fontSize: 13 }}>
                You can now log in with your new username and password.
              </p>
            </div>
            <button onClick={backToLogin} style={buttonStyle}>
              Back to Login
            </button>
          </>
        )}

        {/* ---------------- STEP 1: ENTER EMAIL (Forgot Password) ---------------- */}
        {view === "forgotEmail" && (
          <>
            <h3 style={{ marginTop: 0 }}>Forgot Password</h3>
            <p style={{ color: "#94a3b8", fontSize: 13, marginTop: -8 }}>
              Enter your registered email/username
            </p>
            <input
              style={inputStyle}
              placeholder="Email / Username"
              value={resetEmail}
              onChange={e => setResetEmail(e.target.value)}
            />

            {flowError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {flowError}
              </div>
            )}

            <button onClick={handleSendOtp} style={buttonStyle}>
              Send OTP
            </button>

            <p style={{ textAlign: "center", marginTop: 16 }}>
              <span style={linkStyle} onClick={backToLogin}>
                Back to Login
              </span>
            </p>
          </>
        )}

        {/* ---------------- STEP 2: VERIFY OTP ---------------- */}
        {view === "forgotOtp" && (
          <>
            <h3 style={{ marginTop: 0 }}>Verify OTP</h3>
            <p style={{ color: "#94a3b8", fontSize: 13, marginTop: -8 }}>
              Enter the 6-digit OTP sent to your email
            </p>

            {/* DEMO ONLY: shows the OTP on screen since there's no real email service yet */}
            <div style={{
              background: "#422006", border: "1px solid #eab308",
              color: "#fde68a", padding: "8px 12px",
              borderRadius: 8, fontSize: 13, marginBottom: 12
            }}>
              DEMO MODE — your OTP is: <b>{generatedOtp}</b> (also printed in browser console)
            </div>

            <input
              style={{ ...inputStyle, letterSpacing: 6, textAlign: "center", fontSize: 20 }}
              placeholder="______"
              maxLength={6}
              value={otpInput}
              onChange={e => setOtpInput(e.target.value.replace(/\D/g, ""))}
            />

            {flowError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {flowError}
              </div>
            )}

            <button onClick={handleVerifyOtp} style={buttonStyle}>
              Verify OTP
            </button>

            <p style={{ textAlign: "center", marginTop: 16 }}>
              <span style={linkStyle} onClick={handleResendOtp}>
                Resend OTP
              </span>
            </p>
          </>
        )}

        {/* ---------------- STEP 3: RESET PASSWORD ---------------- */}
        {view === "forgotReset" && (
          <>
            <h3 style={{ marginTop: 0 }}>Reset Password</h3>

            <label style={{ fontSize: 13, color: "#94a3b8" }}>New Password</label>
            <input
              style={inputStyle}
              type="password"
              placeholder="********"
              value={newPassword}
              onChange={e => setNewPassword(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              Confirm Password
            </label>
            <input
              style={inputStyle}
              type="password"
              placeholder="********"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
            />

            {flowError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {flowError}
              </div>
            )}

            <button onClick={handleResetPassword} style={buttonStyle}>
              Reset Password
            </button>
          </>
        )}

        {/* ---------------- FORGOT PASSWORD SUCCESS ---------------- */}
        {view === "success" && (
          <>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 40, marginBottom: 8 }}>✅</div>
              <h3>Password reset successfully!</h3>
            </div>
            <button onClick={backToLogin} style={buttonStyle}>
              Back to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
}
