import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid, Cell
} from "recharts";

const BAR_COLORS = [
  "#6366f1","#818cf8","#a5b4fc","#6366f1",
  "#818cf8","#a5b4fc","#6366f1","#818cf8"
];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "8px 14px", fontSize: 13,
      }}>
        <div style={{ color: "#94a3b8", fontSize: 11, marginBottom: 2 }}>
          {payload[0].payload.activity}
        </div>
        <div style={{ color: "#818cf8", fontWeight: 600 }}>
          {payload[0].value} events
        </div>
      </div>
    );
  }
  return null;
};

export default function UEBAActivity({ data, height = 300 }) {
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

  return (
    <div style={{
      background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      padding: "18px 20px", height,
      display: "flex", flexDirection: "column", overflow: "hidden",
    }}>
      <div style={{ flexShrink: 0, marginBottom: 12 }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>UEBA Activity Distribution</div>
        <div style={{ fontSize: 12, color: "#475569" }}>User and entity behavior events</div>
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
              allowDecimals={false}
            />
            <YAxis
              dataKey="activity" type="category"
              stroke="#334155"
              tick={{ fill: "#94a3b8", fontSize: 11 }}
              width={110}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" radius={[0, 6, 6, 0]} maxBarSize={22}>
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