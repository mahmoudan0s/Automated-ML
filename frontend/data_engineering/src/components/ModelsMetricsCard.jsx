import BaseComponent from "./BaseComponent";
import BaseTable from "./BaseTable";

const toDisplay = (val) => {
    if (val === null || val === undefined) return "";
    if (Array.isArray(val) || typeof val === "object") return JSON.stringify(val);
    return String(val);
};

export default function ModelsMetricsCard({ trainingResults, className }) {
    const all = trainingResults?.all_metrics;
    if (!all && !(trainingResults && trainingResults.all_models)) return null;
    
    const modelDisplayNames = trainingResults?.model_display_names || {};
    
    if (all && typeof all === 'object') {
        const modelNames = Object.keys(all);
        const metricKeySet = new Set();
        modelNames.forEach((m) => {
            const metricsObj = all[m] || {};
            Object.keys(metricsObj).forEach((k) => metricKeySet.add(k));
        });
        const metricKeys = Array.from(metricKeySet).filter(k => {
            // Exclude array/object columns (like confusion matrix)
            const firstModel = modelNames[0];
            const val = all[firstModel]?.[k];
            return !Array.isArray(val) && typeof val !== 'object';
        });
        const headers = ['Model', ...metricKeys.map(k => k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()))];
        const tableData = modelNames.map((m) => {
            const row = { 
                Model: modelDisplayNames[m] || m,
                _isSelected: m === trainingResults.model_name,
            };
            const metricsObj = all[m] || {};
            metricKeys.forEach((k) => {
                row[k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())] = toDisplay(metricsObj[k]);
            });
            return row;
        });
        
        return (
            <BaseComponent title="Models metrics" description="Comparison of metrics across different models" className={className}>
                <div className="mt-3 w-full max-w-7xl">
                    <BaseTable tableHeaders={headers} tableData={tableData} />
                </div>
            </BaseComponent>
        );
    }
}
