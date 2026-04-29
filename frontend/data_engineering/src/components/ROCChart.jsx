import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import BaseComponent from "./BaseComponent";

const rocData = [
  { fpr: 0.0, tpr: 0.0 },
  { fpr: 0.02, tpr: 0.45 },
  { fpr: 0.05, tpr: 0.68 },
  { fpr: 0.1, tpr: 0.78 },
  { fpr: 0.15, tpr: 0.85 },
  { fpr: 0.2, tpr: 0.9 },
  { fpr: 0.3, tpr: 0.92 },
  { fpr: 0.4, tpr: 0.94 },
  { fpr: 0.5, tpr: 0.95 },
  { fpr: 1, tpr: 1 }
];

const diagonal = [
  { fpr: 0, tpr: 0 },
  { fpr: 1, tpr: 1 }
];

export default function ROCChart() {
  return (
    <BaseComponent title="ROC Curve" description="A visual representation of the model's performance in terms of true positives, false positives, true negatives, and false negatives." className="w-full">
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rocData} margin={{ top: 10, right: 10, left: 10, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            type="number"
            dataKey="fpr"
            domain={[0, 1]}
            label={{ value: "False Positive Rate", position: "insideBottom", offset: -15, textAnchor: "middle" }}
          />

          <YAxis
            type="number"
            dataKey="tpr"
            domain={[0, 1]}
            label={{ value: "True Positive Rate", angle: -90, position: "insideLeft", offset: 5, textAnchor: "middle" }}
          />

          <Tooltip />

          {/* ROC Curve */}
          <Line
            data={rocData}
            type="monotone"
            dataKey="tpr"
            name="ROC Curve (AUC = 0.93)"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 3 }}
          />

          <Line
            data={rocData}
            type="monotone"
            dataKey="tpr2"
            name="ROC Curve (AUC = 0.78)"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 3 }}
          />

          {/* Diagonal */}
          <Line
            data={diagonal}
            type="linear"
            dataKey="tpr"
            name="Random"
            stroke="#9ca3af"
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
        </ResponsiveContainer>
      </div>
    </BaseComponent>
  );
}
