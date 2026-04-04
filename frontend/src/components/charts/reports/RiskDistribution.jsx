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
          Risk Score: {payload[0].payload.score}
        </div>
        <div style={{ color: "#67e8f9", fontWeight: 600 }}>
          {payload[0].value} cases
        </div>
      </div>
    );
  }
  return null;
};

// color each bar by risk level
const barColor = (score) => {
  const s = parseFloat(score);
  if (s >= 0.8) return "#ef4444";
  if (s >= 0.6) return "#f97316";
  if (s >= 0.4) return "#f59e0b";
  return "#22c55e";
};

export default function RiskDistribution({ data, height = 300 }) {
  if (!data) return (
    <div style={{
      height, background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      display: "flex", alignItems: "center", justifyContent: "center",
      color: "#334155", fontSize: 13,
    }}>Loading...</div>
  );

  const HEADER_H  = 52;
  const PADDING_V = 52;   // extra for bottom axis label
  const CHART_H   = height - HEADER_H - PADDING_V;

  return (
    <div style={{
      background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      padding: "18px 20px", height,
      display: "flex", flexDirection: "column", overflow: "hidden",
    }}>
      <div style={{ flexShrink: 0, marginBottom: 12 }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>Risk Score Distribution</div>
        <div style={{ fontSize: 12, color: "#475569" }}>Frequency of threats by risk bucket</div>
      </div>

      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height={CHART_H}>
          <BarChart
            data={data}
            margin={{ top: 4, right: 8, left: -16, bottom: 24 }}
          >
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis
              dataKey="score" stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              label={{
                value: "Risk Score", position: "insideBottom",
                offset: -14, fill: "#475569", fontSize: 11
              }}
            />
            <YAxis
              stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              allowDecimals={false}
              label={{
                value: "Frequency", angle: -90,
                position: "insideLeft", offset: 16,
                fill: "#475569", fontSize: 11
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="frequency" radius={[6, 6, 0, 0]} maxBarSize={36}>
              {data.map((d, i) => (
                <Cell key={i} fill={barColor(d.score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}