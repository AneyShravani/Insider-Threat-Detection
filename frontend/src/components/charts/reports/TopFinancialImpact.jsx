import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid, Cell
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "8px 14px", fontSize: 13,
      }}>
        <div style={{ color: "#94a3b8", fontSize: 11, marginBottom: 2 }}>
          {payload[0].payload.scenario}
        </div>
        <div style={{ color: "#f59e0b", fontWeight: 600 }}>
          ${payload[0].value.toLocaleString()}
        </div>
      </div>
    );
  }
  return null;
};

export default function TopFinancialImpact({ data, height = 300 }) {
  if (!data) return (
    <div style={{
      height, background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      display: "flex", alignItems: "center", justifyContent: "center",
      color: "#334155", fontSize: 13,
    }}>Loading...</div>
  );

  const HEADER_H  = 52;
  const PADDING_V = 36;
  const CHART_H   = height - HEADER_H - PADDING_V;

  // color bars by intensity
  const max = Math.max(...data.map(d => d.impact));

  return (
    <div style={{
      background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      padding: "18px 20px", height,
      display: "flex", flexDirection: "column", overflow: "hidden",
    }}>
      <div style={{ flexShrink: 0, marginBottom: 12 }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>
          Top Financial Impact Scenarios
        </div>
        <div style={{ fontSize: 12, color: "#475569" }}>Highest cost threat events</div>
      </div>

      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height={CHART_H}>
          <BarChart
            data={data} layout="vertical"
            margin={{ top: 4, right: 16, left: 8, bottom: 0 }}
          >
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" horizontal={false} />
            <XAxis
              type="number" stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              tickFormatter={v => `$${(v / 1000).toFixed(0)}k`}
            />
            <YAxis
              dataKey="scenario" type="category"
              stroke="#334155"
              tick={{ fill: "#94a3b8", fontSize: 11 }}
              width={72}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="impact" radius={[0, 6, 6, 0]} maxBarSize={22}>
              {data.map((d, i) => {
                const intensity = d.impact / max;
                const opacity = 0.45 + intensity * 0.55;
                return <Cell key={i} fill={`rgba(245, 158, 11, ${opacity})`} />;
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}