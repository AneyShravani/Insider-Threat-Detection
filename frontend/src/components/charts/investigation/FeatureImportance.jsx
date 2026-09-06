import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid, Cell
} from "recharts";

const BAR_COLORS = ["#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe"];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "8px 14px", fontSize: 13,
      }}>
        <div style={{ color: "#94a3b8", fontSize: 11, marginBottom: 2 }}>
          {payload[0].payload.feature}
        </div>
        <div style={{ color: "#818cf8", fontWeight: 600 }}>
          Score: {payload[0].value.toFixed(2)}
        </div>
      </div>
    );
  }
  return null;
};

export default function FeatureImportance({ data, height = 300 }) {
  if (!data) return (
    <div style={{
      height, background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      display: "flex", alignItems: "center", justifyContent: "center",
      color: "#334155", fontSize: 13,
    }}>Loading...</div>
  );

  const HEADER_H  = 52;
  const PADDING_V = 40;
  const BOTTOM_LABEL = 36;   // extra room for x-axis labels
  const CHART_H = height - HEADER_H - PADDING_V;

  return (
    <div style={{
      background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      padding: "18px 20px 18px",
      height,
      display: "flex", flexDirection: "column", overflow: "hidden",
    }}>
      <div style={{ flexShrink: 0, marginBottom: 12 }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>Feature Importance</div>
        <div style={{ fontSize: 12, color: "#475569" }}>ML model input weight scores</div>
      </div>

      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 4, right: 8, left: -16, bottom: BOTTOM_LABEL }}
          >
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis
              dataKey="feature"
              stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              interval={0}
              angle={-20}
              textAnchor="end"
              height={BOTTOM_LABEL}
            />
            <YAxis
              stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              domain={[0, 0.4]}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="score" radius={[6, 6, 0, 0]} maxBarSize={52}>
              {data.map((_, i) => (
                <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}