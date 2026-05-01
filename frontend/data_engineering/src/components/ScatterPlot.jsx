import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import BaseComponent from "./BaseComponent";

const CLUSTER_COLORS = [
  "#7c3aed", "#0ea5e9", "#10b981",
  "#f59e0b", "#ec4899", "#14b8a6",
  "#f97316", "#6366f1", "#ef4444",
  "#22c55e",
];

const sampleClusters = [
  {
    id: 0,
    members: [
      { CustomerID: 1, Gender: "Male", Age: 19, "Annual Income (k$)": 15, "Spending Score (1-100)": 39 },
      { CustomerID: 2, Gender: "Male", Age: 21, "Annual Income (k$)": 15, "Spending Score (1-100)": 81 },
      { CustomerID: 3, Gender: "Female", Age: 20, "Annual Income (k$)": 16, "Spending Score (1-100)": 6 },
      { CustomerID: 4, Gender: "Female", Age: 23, "Annual Income (k$)": 16, "Spending Score (1-100)": 77 },
    ],
  },
  {
    id: 1,
    members: [
      { CustomerID: 5,  Gender: "Female", Age: 31, "Annual Income (k$)": 17, "Spending Score (1-100)": 40 },
      { CustomerID: 6, Gender: "Female", Age: 22, "Annual Income (k$)": 17, "Spending Score (1-100)": 76 },
      { CustomerID: 7, Gender: "Female", Age: 35, "Annual Income (k$)": 18, "Spending Score (1-100)": 6 },
      { CustomerID: 8, Gender: "Female", Age: 28, "Annual Income (k$)": 18, "Spending Score (1-100)": 76 },
    ],
  },
];

const xAxis = "Annual Income (k$)";
const yAxis = "Spending Score (1-100)";

export default function ScatterPlot({ clusters = sampleClusters, className = '' }) {
  const safeClusters = Array.isArray(clusters) ? clusters : sampleClusters;
  const hasPoints = safeClusters.some(
    (cluster) => Array.isArray(cluster?.members) && cluster.members.length > 0
  );

  return (
    <BaseComponent
      title="Scatter Visualization"
      description="Cluster distribution across the selected feature space."
      className={`w-full ${className}`}
    >
      {hasPoints ? (
        <ResponsiveContainer width="100%" height={380}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(249,115,22,0.18)"
            />
            <XAxis
              dataKey={xAxis}
              name={xAxis}
              tick={{ fill: "#475569", fontFamily: "'IBM Plex Mono', monospace", fontSize: 11 }}
              axisLine={{ stroke: "rgba(249,115,22,0.4)" }}
              tickLine={false}
              label={{
                value: xAxis,
                position: "insideBottom",
                offset: -12,
                fill: "#475569",
                fontFamily: "'IBM Plex Mono', monospace",
                fontSize: 11,
              }}
            />
            <YAxis
              dataKey={yAxis}
              name={yAxis}
              tick={{ fill: "#475569", fontFamily: "'IBM Plex Mono', monospace", fontSize: 11 }}
              axisLine={{ stroke: "rgba(249,115,22,0.4)" }}
              tickLine={false}
              label={{
                value: yAxis,
                angle: -90,
                position: "insideLeft",
                fill: "#475569",
                fontFamily: "'IBM Plex Mono', monospace",
                fontSize: 11,
              }}
            />
            <Tooltip />
            <Legend
              wrapperStyle={{
                fontFamily: "'IBM Plex Mono', monospace",
                fontSize: "11px",
                color: "#475569",
                paddingTop: "16px",
              }}
            />

            {safeClusters.map((cluster, i) => {
              const members = Array.isArray(cluster?.members) ? cluster.members : [];

              return (
                <Scatter
                  key={cluster?.id ?? i}
                  name={`Cluster ${cluster?.id != null ? cluster.id + 1 : i + 1}`}
                  data={members.map((member) => ({
                    ...member,
                    [xAxis]: member?.[xAxis],
                    [yAxis]: member?.[yAxis],
                  }))}
                  fill={CLUSTER_COLORS[i % CLUSTER_COLORS.length]}
                  fillOpacity={0.8}
                  r={5}
                />
              );
            })}
          </ScatterChart>
        </ResponsiveContainer>
      ) : (
        <div className="flex h-[380px] items-center justify-center rounded-xl border border-dashed border-orange-200 bg-orange-50/40 text-sm text-slate-500">
          No clustering data available.
        </div>
      )}
    </BaseComponent>
  );
}