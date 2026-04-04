import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from "recharts";

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "7px 12px", fontSize: 13
      }}>
        <div style={{ color: "#64748b", fontSize: 11 }}>Hour {label}:00</div>
        <div style={{ color: "#ef4444", fontWeight: 600 }}>{payload[0].value} detections</div>
      </div>
    );
  }
  return null;
};

export default function ThreatByHour({ data, height = 224 }) {
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
          Threat Detection by Hour
        </div>
        <div style={{ fontSize: 11, color: "#475569" }}>Activity timeline across working hours</div>
      </div>

      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height={innerH}>
          <AreaChart data={data} margin={{ top: 4, right: 8, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="threatGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis
              dataKey="hour" stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              tickFormatter={v => `${v}h`}
            />
            <YAxis
              stroke="#334155"
              tick={{ fill: "#475569", fontSize: 11 }}
              allowDecimals={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone" dataKey="count"
              stroke="#ef4444" strokeWidth={2}
              fill="url(#threatGrad)"
              dot={{ r: 3, fill: "#ef4444", strokeWidth: 0 }}
              activeDot={{ r: 5, fill: "#ef4444" }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}