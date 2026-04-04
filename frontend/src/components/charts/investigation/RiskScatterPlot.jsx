import {
  ScatterChart, Scatter, XAxis, YAxis,
  Tooltip, ResponsiveContainer, CartesianGrid, ZAxis
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    const d = payload[0].payload;
    return (
      <div style={{
        background: "#0f172a", border: "1px solid #1e293b",
        borderRadius: 8, padding: "8px 14px", fontSize: 13,
      }}>
        <div style={{ color: "#94a3b8", fontSize: 11, marginBottom: 4 }}>Data Point</div>
        <div style={{ color: "#f87171", fontWeight: 600 }}>
          Risk: {d.risk_score?.toFixed(2)}
        </div>
        <div style={{ color: "#94a3b8" }}>
          Impact: ${Number(d.financial_impact).toLocaleString()}
        </div>
      </div>
    );
  }
  return null;
};

const CustomDot = (props) => {
  const { cx, cy } = props;
  return (
    <g>
      <circle cx={cx} cy={cy} r={6} fill="#f87171" fillOpacity={0.85} stroke="#ef4444" strokeWidth={1} />
      <circle cx={cx} cy={cy} r={10} fill="#f87171" fillOpacity={0.12} />
    </g>
  );
};

export default function RiskScatterPlot({ data, height = 280 }) {
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
        <div style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0" }}>
          Risk Score vs Financial Impact
        </div>
        <div style={{ fontSize: 12, color: "#475569" }}>Correlation between risk and cost</div>
      </div>

      <div style={{ flex: 1, height: CHART_H }}>
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 4, right: 8, left: -16, bottom: 12 }}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis
              dataKey="risk_score" name="Risk Score"
              type="number" domain={[0, 1]}
              stroke="#334155" tick={{ fill: "#475569", fontSize: 11 }}
              label={{ value: "Risk Score", position: "insideBottom", offset: -6, fill: "#475569", fontSize: 11 }}
            />
            <YAxis
              dataKey="financial_impact" name="Financial Impact"
              stroke="#334155" tick={{ fill: "#475569", fontSize: 11 }}
              tickFormatter={v => `$${(v / 1000).toFixed(0)}k`}
            />
            <ZAxis range={[40, 40]} />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: "#334155", strokeDasharray: "4 4" }} />
            <Scatter data={data} shape={<CustomDot />} />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}