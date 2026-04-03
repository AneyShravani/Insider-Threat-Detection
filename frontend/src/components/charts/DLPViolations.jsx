export default function DLPViolations({ data, theme }) {
  if (!data) return null;

  const isDark = theme === "dark";
  const textColor = isDark ? "white" : "#020617";
  const axisColor = isDark ? "#94a3b8" : "#475569";
  const gridColor = isDark ? "#334155" : "#cbd5f5";

  return (
    <div style={{ flex: 1, minWidth: 300 }}>
      <h3 style={{ color: textColor }}>DLP Violations by Risk Level</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
          <XAxis dataKey="name" stroke={axisColor} />
          <YAxis stroke={axisColor} />
          <Tooltip />
          <Bar dataKey="count" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}