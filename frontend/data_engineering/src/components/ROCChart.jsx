import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import BaseComponent from "./BaseComponent";


const diagonal = [
  { fpr: 0, tpr: 0 },
  { fpr: 1, tpr: 1 }
];

export default function ROCChart({ roc }) {
  const data = roc && roc.points ? roc.points : Array.isArray(roc) ? roc : [];
  const auc = roc && roc.auc ? roc.auc : null;
  
  return (
    <BaseComponent title={auc ? `ROC Curve (AUC = ${auc})` : "ROC Curve"} description="A visual representation of classifier trade-offs (TPR vs FPR)." className="w-full">
    <div className="h-80 w-full">
    <ResponsiveContainer width="100%" height="100%">
    <LineChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 40 }}>
    <CartesianGrid strokeDasharray="3 3" />
    
    <XAxis
    type="number"
    dataKey="fpr"
    domain={[0, 1]}
    label={{ value: "False Positive Rate", position: "insideBottom", offset: -15, textAnchor: "middle" }}
    tickFormatter={(v) => Number(v).toFixed(2)}
    />
    
    <YAxis
    type="number"
    dataKey="tpr"
    domain={[0, 1]}
    label={{ value: "True Positive Rate", angle: -90, position: "insideLeft", offset: 5, textAnchor: "middle" }}
    tickFormatter={(v) => Number(v).toFixed(2)}
    />
    
    <Tooltip formatter={(value) => Number(value).toFixed(3)} />
    
    {/* ROC Curve */}
    <Line
    data={data}
    type="monotone"
    dataKey="tpr"
    name={auc ? `ROC Curve (AUC = ${auc})` : "ROC Curve"}
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
