import { useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";

// Small helper to simulate a realistic network delay
const fakeDelay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const OTP_VALID_SECONDS = 60;
const MAX_LOGIN_ATTEMPTS = 5;
const LOCKOUT_SECONDS = 30;

// ---- Reusable password field with a show/hide eye icon ----
function PasswordField({ value, onChange, placeholder, onKeyDown, style, disabled }) {
  const [visible, setVisible] = useState(false);

  return (
    <div style={{ position: "relative" }}>
      <input
        style={{ ...style, paddingRight: 42 }}
        type={visible ? "text" : "password"}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        disabled={disabled}
      />
      <span
        onClick={() => setVisible(v => !v)}
        title={visible ? "Hide password" : "Show password"}
        style={{
          position: "absolute", right: 14, top: "50%",
          transform: "translateY(-6px)", cursor: "pointer",
          fontSize: 16, userSelect: "none"
        }}
      >
        {visible ? "🙈" : "👁️"}
      </span>
    </div>
  );
}

export default function Login() {
  const navigate = useNavigate();

  // ---- Login state ----
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");

  const [adminPassword, setAdminPassword] = useState("admin123");

  // ---- Login attempt limiting ----
  const [loginAttempts, setLoginAttempts] = useState(0);
  const [lockSecondsLeft, setLockSecondsLeft] = useState(0);
  const lockTimerRef = useRef(null);

  // ---- Forgot Password + OTP state ----
  const [view, setView] = useState("login");
  const [resetEmail, setResetEmail]     = useState("");
  const [resetTarget, setResetTarget]   = useState(null);
  const [generatedOtp, setGeneratedOtp] = useState("");
  const [otpInput, setOtpInput]         = useState("");
  const [newPassword, setNewPassword]         = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [flowError, setFlowError] = useState("");

  // ---- OTP expiry timer ----
  const [otpSecondsLeft, setOtpSecondsLeft] = useState(0);
  const otpTimerRef = useRef(null);

  // ---- Register state ----
  const [registeredUsers, setRegisteredUsers] = useState([]);
  const [regFullName, setRegFullName] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regUsername, setRegUsername] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConfirmPassword, setRegConfirmPassword] = useState("");
  const [regError, setRegError] = useState("");

  // ---- Loading state ----
  const [loading, setLoading] = useState(false);
  const [loadingLabel, setLoadingLabel] = useState("");

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
    cursor: "pointer", fontWeight: "bold",
    transition: "opacity 0.2s"
  };

  const disabledButtonStyle = {
    ...buttonStyle,
    background: "#334155",
    cursor: "not-allowed",
    opacity: 0.8
  };

  const linkStyle = {
    color: "#38bdf8", cursor: "pointer",
    fontSize: 13, textDecoration: "underline"
  };

  // ---------------- LOGIN LOCKOUT TIMER ----------------
  const startLockout = () => {
    setLockSecondsLeft(LOCKOUT_SECONDS);
    clearInterval(lockTimerRef.current);
    lockTimerRef.current = setInterval(() => {
      setLockSecondsLeft(prev => {
        if (prev <= 1) {
          clearInterval(lockTimerRef.current);
          setLoginAttempts(0);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  useEffect(() => {
    return () => clearInterval(lockTimerRef.current);
  }, []);

  // ---------------- LOGIN ----------------
  const handleLogin = async () => {
    if (lockSecondsLeft > 0) return;

    setError("");
    setLoading(true);
    setLoadingLabel("Logging in...");
    await fakeDelay(700);
    setLoading(false);

    const isDefaultAdmin = username === "admin" && password === adminPassword;
    const matchedUser = registeredUsers.find(
      u => u.username === username && u.password === password
    );

    if (isDefaultAdmin || matchedUser) {
      setLoginAttempts(0);
      navigate("/dashboard");
    } else {
      const nextAttempts = loginAttempts + 1;
      setLoginAttempts(nextAttempts);

      if (nextAttempts >= MAX_LOGIN_ATTEMPTS) {
        setError(`Too many failed attempts. Locked for ${LOCKOUT_SECONDS}s.`);
        startLockout();
      } else {
        setError(`Invalid credentials! (${MAX_LOGIN_ATTEMPTS - nextAttempts} attempt(s) left)`);
      }
    }
  };

  // ---------------- OTP HELPERS ----------------
  const startOtpTimer = () => {
    setOtpSecondsLeft(OTP_VALID_SECONDS);
    clearInterval(otpTimerRef.current);
    otpTimerRef.current = setInterval(() => {
      setOtpSecondsLeft(prev => {
        if (prev <= 1) {
          clearInterval(otpTimerRef.current);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  useEffect(() => {
    return () => clearInterval(otpTimerRef.current);
  }, []);

  const generateAndShowOtp = () => {
    const code = Math.floor(100000 + Math.random() * 900000).toString();
    setGeneratedOtp(code);
    console.log("DEMO OTP (would be emailed in production):", code);
    startOtpTimer();
    return code;
  };

  const findAccountByEmailOrUsername = (value) => {
    const trimmed = value.trim();
    if (trimmed === "admin") return "admin";

    const match = registeredUsers.find(
      u => u.username === trimmed || u.email === trimmed
    );
    return match ? match.username : null;
  };

  const handleSendOtp = async () => {
    setFlowError("");
    if (!resetEmail.trim()) {
      setFlowError("Please enter your registered email/username.");
      return;
    }

    const target = findAccountByEmailOrUsername(resetEmail);
    if (!target) {
      setFlowError("No account found with that email/username.");
      return;
    }

    setLoading(true);
    setLoadingLabel("Sending OTP...");
    await fakeDelay(900);
    setLoading(false);

    setResetTarget(target);
    generateAndShowOtp();
    setOtpInput("");
    setView("forgotOtp");
  };

  const handleResendOtp = async () => {
    setFlowError("");
    setLoading(true);
    setLoadingLabel("Resending OTP...");
    await fakeDelay(700);
    setLoading(false);

    generateAndShowOtp();
    setOtpInput("");
  };

  const handleVerifyOtp = async (codeOverride) => {
    const codeToCheck = codeOverride ?? otpInput;
    setFlowError("");

    if (otpSecondsLeft <= 0) {
      setFlowError("OTP expired. Please click Resend OTP.");
      setOtpInput("");
      return;
    }

    setLoading(true);
    setLoadingLabel("Verifying...");
    await fakeDelay(600);
    setLoading(false);

    if (codeToCheck.trim() === generatedOtp) {
      clearInterval(otpTimerRef.current);
      setNewPassword("");
      setConfirmPassword("");
      setView("forgotReset");
    } else {
      setFlowError("Incorrect OTP. Please try again.");
      setOtpInput("");
    }
  };

  useEffect(() => {
    if (view === "forgotOtp" && otpInput.length === 6 && !loading) {
      handleVerifyOtp(otpInput);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [otpInput]);

  const handleResetPassword = async () => {
    setFlowError("");
    if (!newPassword || !confirmPassword) {
      setFlowError("Please fill in both password fields.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setFlowError("Passwords do not match.");
      return;
    }

    setLoading(true);
    setLoadingLabel("Resetting...");
    await fakeDelay(800);
    setLoading(false);

    if (resetTarget === "admin") {
      setAdminPassword(newPassword);
    } else {
      setRegisteredUsers(prev =>
        prev.map(u => u.username === resetTarget ? { ...u, password: newPassword } : u)
      );
    }

    setView("success");
  };

  // ---------------- PASSWORD VALIDATION / STRENGTH ----------------
  const validatePassword = (pwd) => {
    if (pwd.length < 6) return "Password must be at least 6 characters long.";
    if (!/[a-zA-Z]/.test(pwd)) return "Password must contain at least one letter.";
    if (!/[0-9]/.test(pwd)) return "Password must contain at least one number.";
    return "";
  };

  const getPasswordStrength = (pwd) => {
    if (!pwd) return { label: "", color: "#334155", percent: 0 };
    let score = 0;
    if (pwd.length >= 6) score++;
    if (pwd.length >= 10) score++;
    if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^a-zA-Z0-9]/.test(pwd)) score++;

    if (score <= 1) return { label: "Weak", color: "#ef4444", percent: 25 };
    if (score <= 3) return { label: "Medium", color: "#eab308", percent: 60 };
    return { label: "Strong", color: "#22c55e", percent: 100 };
  };

  const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

  // ---------------- REGISTER ----------------
  const handleRegister = async () => {
    setRegError("");

    if (!regFullName.trim() || !regEmail.trim() || !regUsername.trim() || !regPassword || !regConfirmPassword) {
      setRegError("Please fill in all fields.");
      return;
    }
    if (!isValidEmail(regEmail.trim())) {
      setRegError("Please enter a valid email address.");
      return;
    }
    const passwordIssue = validatePassword(regPassword);
    if (passwordIssue) {
      setRegError(passwordIssue);
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
    if (registeredUsers.some(u => u.email === regEmail.trim())) {
      setRegError("An account with that email already exists.");
      return;
    }

    setLoading(true);
    setLoadingLabel("Creating account...");
    await fakeDelay(900);
    setLoading(false);

    setRegisteredUsers(prev => [
      ...prev,
      { fullName: regFullName, email: regEmail.trim(), username: regUsername, password: regPassword }
    ]);
    setView("registerSuccess");
  };

  const goToRegister = () => {
    setRegFullName("");
    setRegEmail("");
    setRegUsername("");
    setRegPassword("");
    setRegConfirmPassword("");
    setRegError("");
    setView("register");
  };

  const backToLogin = () => {
    setView("login");
    setResetEmail("");
    setResetTarget(null);
    setGeneratedOtp("");
    setOtpInput("");
    setNewPassword("");
    setConfirmPassword("");
    setFlowError("");
    setError("");
    clearInterval(otpTimerRef.current);
    setOtpSecondsLeft(0);
  };

  const strength = getPasswordStrength(regPassword);
  const isLocked = lockSecondsLeft > 0;

  const renderButton = (label, onClick, extraDisabled) => (
    <button
      onClick={onClick}
      disabled={loading || extraDisabled}
      style={(loading || extraDisabled) ? disabledButtonStyle : buttonStyle}
    >
      {loading ? (
        <span style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
          <span className="spinner" />
          {loadingLabel}
        </span>
      ) : label}
    </button>
  );

  return (
    <div style={{
      height: "100vh", display: "flex",
      justifyContent: "center", alignItems: "center",
      background: "#020617", color: "white"
    }}>
      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(6px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .view-fade { animation: fadeInUp 0.25s ease-out; }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        .spinner {
          width: 14px; height: 14px;
          border: 2px solid rgba(255,255,255,0.4);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.6s linear infinite;
          display: inline-block;
        }

        @keyframes popIn {
          0%   { transform: scale(0.6); opacity: 0; }
          70%  { transform: scale(1.1); opacity: 1; }
          100% { transform: scale(1); }
        }
        .pop-in { animation: popIn 0.4s ease-out; }
      `}</style>

      <div style={{
        background: "#0f172a", padding: 40,
        borderRadius: 16, width: 380,
        border: "1px solid #1e293b",
        boxShadow: "0 0 40px rgba(56,189,248,0.1)"
      }}>
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div style={{ fontSize: 48 }}>🛡️</div>
          <h2 style={{ margin: "8px 0 4px", fontSize: 24 }}>ThreatGuard</h2>
          <p style={{ color: "#64748b", margin: 0, fontSize: 14 }}>
            Insider Threat Detection System
          </p>
        </div>

        {/* ---------------- LOGIN VIEW ---------------- */}
        {view === "login" && (
          <div className="view-fade" key="login">
            <label style={{ fontSize: 13, color: "#94a3b8" }}>👤 Username</label>
            <input
              style={inputStyle}
              placeholder="Enter username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              disabled={isLocked}
            />
            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              🔒 Password
            </label>
            <PasswordField
              style={inputStyle}
              placeholder="Enter password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !loading && !isLocked && handleLogin()}
              disabled={isLocked}
            />

            {error && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {error}
              </div>
            )}

            {isLocked && (
              <div style={{ color: "#eab308", fontSize: 13, marginTop: 6 }}>
                🔒 Try again in {lockSecondsLeft}s
              </div>
            )}

            {renderButton("Login →", handleLogin, isLocked)}

            <p style={{ textAlign: "center", marginTop: 16, marginBottom: 4 }}>
              <span style={linkStyle} onClick={() => !loading && setView("forgotEmail")}>
                Forgot Password?
              </span>
            </p>

            <p style={{ textAlign: "center", color: "#94a3b8", fontSize: 13, marginTop: 4 }}>
              New student?{" "}
              <span style={linkStyle} onClick={() => !loading && goToRegister()}>
                Create an account
              </span>
            </p>
          </div>
        )}

        {/* ---------------- REGISTER VIEW ---------------- */}
        {view === "register" && (
          <div className="view-fade" key="register">
            <h3 style={{ marginTop: 0 }}>Create an account</h3>

            <label style={{ fontSize: 13, color: "#94a3b8" }}>🙋 Full Name</label>
            <input
              style={inputStyle}
              placeholder="Enter your full name"
              value={regFullName}
              onChange={e => setRegFullName(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              📧 Email
            </label>
            <input
              style={inputStyle}
              type="email"
              placeholder="name@college.edu"
              value={regEmail}
              onChange={e => setRegEmail(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              👤 Username
            </label>
            <input
              style={inputStyle}
              placeholder="Choose a username"
              value={regUsername}
              onChange={e => setRegUsername(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              🔒 Password
            </label>
            <PasswordField
              style={inputStyle}
              placeholder="Choose a password"
              value={regPassword}
              onChange={e => setRegPassword(e.target.value)}
            />

            {regPassword && (
              <div style={{ marginTop: 8 }}>
                <div style={{ height: 6, background: "#1e293b", borderRadius: 4, overflow: "hidden" }}>
                  <div style={{
                    height: "100%", width: `${strength.percent}%`,
                    background: strength.color, transition: "width 0.3s, background 0.3s"
                  }} />
                </div>
                <p style={{ fontSize: 11, color: strength.color, marginTop: 4, marginBottom: 0 }}>
                  {strength.label} password
                </p>
              </div>
            )}
            <p style={{ color: "#64748b", fontSize: 11, marginTop: 4, marginBottom: 0 }}>
              At least 6 characters, with one letter and one number.
            </p>

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              🔒 Confirm Password
            </label>
            <PasswordField
              style={inputStyle}
              placeholder="Re-enter password"
              value={regConfirmPassword}
              onChange={e => setRegConfirmPassword(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !loading && handleRegister()}
            />

            {regError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {regError}
              </div>
            )}

            {renderButton("Create Account", handleRegister)}

            <p style={{ textAlign: "center", marginTop: 16 }}>
              <span style={linkStyle} onClick={() => !loading && backToLogin()}>
                Back to Login
              </span>
            </p>
          </div>
        )}

        {/* ---------------- REGISTER SUCCESS ---------------- */}
        {view === "registerSuccess" && (
          <div className="view-fade" key="registerSuccess">
            <div style={{ textAlign: "center" }}>
              <div className="pop-in" style={{ fontSize: 40, marginBottom: 8 }}>✅</div>
              <h3>Account created!</h3>
              <p style={{ color: "#94a3b8", fontSize: 13 }}>
                You can now log in with your new username and password.
              </p>
            </div>
            <button onClick={backToLogin} style={buttonStyle}>
              Back to Login
            </button>
          </div>
        )}

        {/* ---------------- STEP 1: ENTER EMAIL (Forgot Password) ---------------- */}
        {view === "forgotEmail" && (
          <div className="view-fade" key="forgotEmail">
            <h3 style={{ marginTop: 0 }}>Forgot Password</h3>
            <p style={{ color: "#94a3b8", fontSize: 13, marginTop: -8 }}>
              Enter your registered email/username
            </p>
            <input
              style={inputStyle}
              placeholder="Email / Username"
              value={resetEmail}
              onChange={e => setResetEmail(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !loading && handleSendOtp()}
            />

            {flowError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {flowError}
              </div>
            )}

            {renderButton("Send OTP", handleSendOtp)}

            <p style={{ textAlign: "center", marginTop: 16 }}>
              <span style={linkStyle} onClick={() => !loading && backToLogin()}>
                Back to Login
              </span>
            </p>
          </div>
        )}

        {/* ---------------- STEP 2: VERIFY OTP ---------------- */}
        {view === "forgotOtp" && (
          <div className="view-fade" key="forgotOtp">
            <h3 style={{ marginTop: 0 }}>Verify OTP</h3>
            <p style={{ color: "#94a3b8", fontSize: 13, marginTop: -8 }}>
              Enter the 6-digit OTP sent to your email
            </p>

            <div style={{
              background: "#422006", border: "1px solid #eab308",
              color: "#fde68a", padding: "8px 12px",
              borderRadius: 8, fontSize: 13, marginBottom: 12,
              display: "flex", justifyContent: "space-between", alignItems: "center"
            }}>
              <span>DEMO — OTP: <b>{generatedOtp}</b></span>
              <span style={{ color: otpSecondsLeft <= 10 ? "#ef4444" : "#fde68a", fontWeight: "bold" }}>
                {otpSecondsLeft > 0 ? `${otpSecondsLeft}s` : "Expired"}
              </span>
            </div>

            <input
              style={{ ...inputStyle, letterSpacing: 10, textAlign: "center", fontSize: 22 }}
              placeholder="______"
              maxLength={6}
              value={otpInput}
              disabled={loading || otpSecondsLeft <= 0}
              onChange={e => setOtpInput(e.target.value.replace(/\D/g, ""))}
              autoFocus
            />
            <p style={{ color: "#64748b", fontSize: 11, marginTop: 4 }}>
              {otpSecondsLeft > 0
                ? "Auto-verifies once all 6 digits are entered."
                : "This OTP has expired — click Resend OTP below."}
            </p>

            {flowError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {flowError}
              </div>
            )}

            {loading && (
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 16, color: "#94a3b8", fontSize: 13 }}>
                <span className="spinner" /> {loadingLabel}
              </div>
            )}

            <p style={{ textAlign: "center", marginTop: 16 }}>
              <span style={linkStyle} onClick={() => !loading && handleResendOtp()}>
                Resend OTP
              </span>
            </p>
          </div>
        )}

        {/* ---------------- STEP 3: RESET PASSWORD ---------------- */}
        {view === "forgotReset" && (
          <div className="view-fade" key="forgotReset">
            <h3 style={{ marginTop: 0 }}>Reset Password</h3>

            <label style={{ fontSize: 13, color: "#94a3b8" }}>New Password</label>
            <PasswordField
              style={inputStyle}
              placeholder="********"
              value={newPassword}
              onChange={e => setNewPassword(e.target.value)}
            />

            <label style={{ fontSize: 13, color: "#94a3b8", display: "block", marginTop: 16 }}>
              Confirm Password
            </label>
            <PasswordField
              style={inputStyle}
              placeholder="********"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !loading && handleResetPassword()}
            />

            {flowError && (
              <div style={{ color: "#ef4444", fontSize: 13, marginTop: 10 }}>
                ⚠️ {flowError}
              </div>
            )}

            {renderButton("Reset Password", handleResetPassword)}
          </div>
        )}

        {/* ---------------- FORGOT PASSWORD SUCCESS ---------------- */}
        {view === "success" && (
          <div className="view-fade" key="success">
            <div style={{ textAlign: "center" }}>
              <div className="pop-in" style={{ fontSize: 40, marginBottom: 8 }}>✅</div>
              <h3>Password reset successfully!</h3>
            </div>
            <button onClick={backToLogin} style={buttonStyle}>
              Back to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
