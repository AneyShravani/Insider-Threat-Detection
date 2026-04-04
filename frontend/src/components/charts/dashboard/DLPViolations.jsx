import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Cell, ResponsiveContainer
} from "recharts";

const COLORS = ["#ef4444", "#f97316", "#22c55e"];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "7px 12px", fontSize: 13
      }}>
        <div style={{ color: "#64748b", fontSize: 11 }}>{label} Risk</div>
        <div style={{ color: payload[0].fill, fontWeight: 600 }}>{payload[0].value} violations</div>
      </div>
    );
  }
  return null;
};

export default function DLPViolations({ data, height = 224 }) {
  if (!data) return (
    <div style={{
      height, background: "#0f172a", borderRadius: 14,
      display: "flex", alignItems: "center", justifyContent: "center",
      color: "#334155", fontSize: 13
    }}>Loading...</div>
  );

  const innerH = height - 68;

  return (
    <div style={{
      background: "#0f172a",
      borderRadius: 14,
      border: "1px solid #1e293b",
      padding: "16px 20px 12px",
      height,
      display: "flex",
      flexDirection: "column"
    }}>
      <div style={{ marginBottom: 8 }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#e2e8f0" }}>
          DLP Violations by Risk Level
        </div>
        <div style={{ fontSize: 11, color: "#475569" }}>Data loss prevention events</div>
      </div>

      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height={innerH}>
          <BarChart data={data} margin={{ top: 4, right: 8, left: -18, bottom: 0 }}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis
              dataKey="name" stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
            />
            <YAxis
              stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              allowDecimals={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" radius={[5, 5, 0, 0]} maxBarSize={52}>
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}