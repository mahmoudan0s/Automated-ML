import BaseComponent from "./BaseComponent";
import BaseTable from "./BaseTable";

export default function ClassificationReport({ report, className }) {
  const formatMetricValue = (value) => {
    if (value === null || value === undefined || value === "") {
      return "";
    }

    if (typeof value === "number") {
      return Number.isInteger(value) ? value.toFixed(1) : String(value);
    }

    return String(value);
  };

  const tableData = Array.isArray(report)
    ? report.map((row) => ({
        Class: row?.class ?? "",
        Precision: formatMetricValue(row?.precision),
        Recall: formatMetricValue(row?.recall),
        "F1-score": formatMetricValue(row?.f1_score),
        Support: row?.support ?? "",
      }))
    : [];

  return (
    <BaseComponent
      title="Classification Report"
      description="A detailed breakdown of the model's performance for each class."
      className={className}
    >
      <BaseTable
        tableHeaders={["Class", "Precision", "Recall", "F1-score", "Support"]}
        tableData={tableData}
      />
    </BaseComponent>
  );
}
