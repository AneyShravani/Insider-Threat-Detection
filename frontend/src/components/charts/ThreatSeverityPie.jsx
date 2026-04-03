export default function ThreatSeverityPie({ data, theme }) {
  if (!data) return null;

  const isDark = theme === "dark";
  const textColor = isDark ? "white" : "#020617";

  return (
    <div style={{ flex: 1, minWidth: 300 }}>
      <h3 style={{ color: textColor }}>Threat Severity Distribution</h3>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} label>
            {data.map((entry, index) => (
              <Cell key={index} fill={['#ef4444', '#f97316', '#22c55e'][index % 3]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}