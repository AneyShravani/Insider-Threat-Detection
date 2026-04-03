export default function RiskyUsers({ data, theme }) {
  if (!data) return null;

  const isDark = theme === "dark";
  const textColor = isDark ? "white" : "#020617";
  const axisColor = isDark ? "#94a3b8" : "#475569";
  const gridColor = isDark ? "#334155" : "#cbd5f5";

  return (
    <div style={{ flex: 1, minWidth: 300 }}>
      <h3 style={{ color: textColor }}>Top 10 Risky Users</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
          <XAxis type="number" stroke={axisColor} />
          <YAxis dataKey="user" type="category" width={50} stroke={axisColor} />
          <Tooltip />
          <Bar dataKey="score" fill="#82c4f8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}