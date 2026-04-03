export default function ThreatByHour({ data, theme }) {
  if (!data) return null;

  const isDark = theme === "dark";
  const textColor = isDark ? "white" : "#020617";
  const axisColor = isDark ? "#94a3b8" : "#475569";
  const gridColor = isDark ? "#334155" : "#cbd5f5";

  return (
    <div style={{ flex: 1, minWidth: 300 }}>
      <h3 style={{ color: textColor }}>Threat Detection by Hour</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
          <XAxis dataKey="hour" stroke={axisColor} />
          <YAxis stroke={axisColor} />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="#ef4444" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}