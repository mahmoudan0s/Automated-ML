import BaseComponent from "./BaseComponent";
import BaseTable from "./BaseTable";

export default function ClassificationReport({ className }) {
    const tableData = (sampleClassificationReportData || []).map((row) => ({
        Class: row?.class ?? '-',
        Precision: row?.precision == null ? '-' : Number(row.precision).toFixed(2),
        Recall: row?.recall == null ? '-' : Number(row.recall).toFixed(2),
        'F1-score': row?.f1_score == null ? '-' : Number(row.f1_score).toFixed(2),
        Support: row?.support ?? '-',
    }));

    return (
        <BaseComponent title="Classification Report" description="A detailed breakdown of the model's performance for each class." className={className}>
            <BaseTable tableHeaders={["Class", "Precision", "Recall", "F1-score", "Support"]} tableData={tableData} />
        </BaseComponent>
    );
}

const sampleClassificationReportData = [
    { class: "Class 0", precision: 0.89, recall: 0.87, f1_score: 0.88, support: 200 },
    { class: "Class 1", precision: 0.91, recall: 0.93, f1_score: 0.92, support: 300 },
    { class: "Class 2", precision: 0.85, recall: 0.82, f1_score: 0.83, support: 150 },
];