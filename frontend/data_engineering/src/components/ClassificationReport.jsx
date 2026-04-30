import BaseComponent from "./BaseComponent";
import BaseTable from "./BaseTable";
import { DownloadIcon } from "./icons";


const downloadReportButton = (
    <button className="flex items-center gap-2 rounded-lg bg-blue-50 px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-100 hover:text-blue-800 transition-colors shadow-sm shadow-blue-300/25 active:scale-95">
        <DownloadIcon size={20} />
        Download Report
    </button>
);

export default function ClassificationReport({ className }) {
    const tableData = (sampleClassificationReportData || []).map((row) => ({
        Class: row?.class ?? '-',
        Precision: row?.precision == null ? '-' : Number(row.precision).toFixed(2),
        Recall: row?.recall == null ? '-' : Number(row.recall).toFixed(2),
        'F1-score': row?.f1_score == null ? '-' : Number(row.f1_score).toFixed(2),
        Support: row?.support ?? '-',
    }));

    return (
        <BaseComponent 
            title="Classification Report"
            componentButton={downloadReportButton}
            description="A detailed breakdown of the model's performance for each class." 
            className={className}
        >
            <BaseTable tableHeaders={["Class", "Precision", "Recall", "F1-score", "Support"]} tableData={tableData} />
        </BaseComponent>
    );
}

const sampleClassificationReportData = [
    { class: "Class 0", precision: 0.89, recall: 0.87, f1_score: 0.88, support: 200 },
    { class: "Class 1", precision: 0.91, recall: 0.93, f1_score: 0.92, support: 300 },
    { class: "Class 2", precision: 0.85, recall: 0.82, f1_score: 0.83, support: 150 },
    { class: "Class 3", precision: 0.88, recall: 0.90, f1_score: 0.89, support: 250 },
    { class: "Class 4", precision: 0.92, recall: 0.91, f1_score: 0.91, support: 100 },
];