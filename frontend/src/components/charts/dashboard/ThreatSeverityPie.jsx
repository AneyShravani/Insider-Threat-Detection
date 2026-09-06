import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const COLORS = ["#ef4444", "#f97316", "#22c55e"];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    const d = payload[0];
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "8px 14px", fontSize: 13
      }}>
        <span style={{ color: d.payload.fill, fontWeight: 600 }}>{d.name}</span>
        <span style={{ color: "#94a3b8", marginLeft: 8 }}>{d.value}%</span>
      </div>
    );
  }
  return null;
};

const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  const RADIAN = Math.PI / 180;
  const r = innerRadius + (outerRadius - innerRadius) * 0.55;
  const x = cx + r * Math.cos(-midAngle * RADIAN);
  const y = cy + r * Math.sin(-midAngle * RADIAN);
  return (
    <text x={x} y={y} fill="white" textAnchor="middle"
      dominantBaseline="central" fontSize={13} fontWeight={600}>
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

export default function ThreatSeverityPie({ data, height = 480 }) {
  if (!data) return (
    <div style={{
      height, background: "#0f172a", borderRadius: 14,
      display: "flex", alignItems: "center", justifyContent: "center",
      color: "#334155", fontSize: 14, border: "1px solid #1e293b"
    }}>Loading...</div>
  );

  const HEADER_H  = 52;   // title + subtitle
  const LEGEND_H  = 32;   // legend row
  const PADDING_V = 36;   // top + bottom padding
  const PIE_H = height - HEADER_H - LEGEND_H - PADDING_V;

  return (
    <div style={{
      background: "#0f172a", borderRadius: 14, border: "1px solid #1e293b",
      padding: "18px 20px 18px",
      height,
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{ marginBottom: 8, flexShrink: 0 }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>
          Threat Severity Distribution
        </div>
        <div style={{ fontSize: 12, color: "#475569" }}>ML model classification results</div>
      </div>

      {/* Pie — fixed pixel height, no ResponsiveContainer height surprises */}
      <div style={{ flexShrink: 0, height: PIE_H }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data} dataKey="value" nameKey="name"
              cx="50%" cy="50%"
              outerRadius="72%" innerRadius="40%"
              labelLine={false} label={renderCustomLabel}
              strokeWidth={2} stroke="#020617"
            >
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend — manual, fixed height, no overflow */}
      <div style={{
        flexShrink: 0,
        display: "flex", justifyContent: "center", gap: 24,
        marginTop: 10, height: LEGEND_H, alignItems: "center"
      }}>
        {data.map((entry, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <div style={{
              width: 10, height: 10, borderRadius: "50%",
              background: COLORS[i % COLORS.length], flexShrink: 0
            }} />
            <span style={{ fontSize: 12, color: "#94a3b8" }}>{entry.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}