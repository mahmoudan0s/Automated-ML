import BoxData from "./BoxData";
import ClassificationReport from "./ClassificationReport";
import ClusterDefinitions from "./ClusterDefinitions";
import ConfusionMatrix from "./ConfusionMatrix";
import FeatureImportance from "./FeatureImportance";
import ROCChart from "./ROCChart";
import ScatterPlot from "./ScatterPlot";
import {
  AngleDownIcon,
  BullseyeIcon,
  CrosshairIcon,
  FloppyDiskIcon,
  MagnifyingGlassIcon,
  ScaleBalancedIcon,
} from "./icons";

import ModelsMetricsCard from "./ModelsMetricsCard";
import useFetch from "../hooks/useFetch";

export default function ModelMetricsPage({ onBackToDataset, selectedModel, trainingResults }) {
  // Backend returns formatted metric values; display them directly
  const toDisplay = (v) => {
    if (v === null || v === undefined) return "";
    if (Array.isArray(v) || typeof v === "object") return JSON.stringify(v);
    return String(v);
  };

  const getMetrics = () => {
    const icons = [BullseyeIcon, CrosshairIcon, MagnifyingGlassIcon, ScaleBalancedIcon];
    const iconStyles = [
      "text-green-500 bg-green-100",
      "text-blue-500 bg-blue-100",
      "text-yellow-500 bg-yellow-100",
      "text-purple-500 bg-purple-100",
    ];

    // Get metrics from backend (either from metrics or best model in all_metrics)
    let backend = null;
    if (trainingResults && trainingResults.metrics) {
      backend = trainingResults.metrics;
    } else if (trainingResults && trainingResults.all_metrics && trainingResults.model_name) {
      // Use best model's metrics from all_metrics
      backend = trainingResults.all_metrics[trainingResults.model_name];
    }

    if (backend) {
      // Dynamically use all available keys from backend, excluding arrays and objects
      const keys = Object.keys(backend).filter((k) => {
        const value = backend[k];
        return !Array.isArray(value) && typeof value !== "object";
      });

      return keys.map((k, i) => {
        const raw = backend[k];
        return {
          id: k,
          title: k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
          value: raw !== undefined ? toDisplay(raw) : "",
          icon: icons[i % icons.length],
          iconStyle: iconStyles[i % iconStyles.length],
        };
      });
    }

    return [];
  };

  const metrics = getMetrics();

  const API_BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000/api/v1";
  const { request: fetchRequest } = useFetch();

  const downloadModelPackage = async () => {
    const modelId = trainingResults?.model_id;
    if (!modelId) {
      alert("No model available to download");
      return;
    }

    try {
      const res = await fetchRequest(`${API_BASE}/download/model-package/${modelId}`);
      // hook returns Response for non-json content types
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${modelId}_package.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download error", err);
      alert(err.message || "Download failed");
    }
  };

  return (
    <section className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-950">
            {selectedModel.charAt(0).toUpperCase() + selectedModel.slice(1)} Metrics —{" "}
            {trainingResults?.model_display_name}
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Review the performance of your trained model.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={onBackToDataset}
            className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-medium text-blue-600 shadow-sm transition hover:bg-slate-50 active:scale-95"
          >
            <AngleDownIcon size={24} className="rotate-90" />
            Back to Dataset
          </button>

          <button
            onClick={downloadModelPackage}
            className="flex items-center gap-2 rounded-xl bg-green-600 px-6 py-3 text-sm font-medium text-white shadow-md transition hover:bg-green-700 active:scale-95"
          >
            Save Model
            <FloppyDiskIcon size={20} />
          </button>
        </div>
      </div>

      <div
        className={`mx-auto mb-8 mt-8 grid w-full gap-4 sm:grid-cols-2 lg:grid-cols-4 max-w-7xl`}
      >
        {metrics.slice(0, 4).map((stat) => (
          <BoxData
            key={stat.id}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            iconStyle={stat.iconStyle}
          />
        ))}
      </div>

      <div className="grid gap-6 grid-cols-2">
        {selectedModel === "classification" || selectedModel === "regression" ? (
          <FeatureImportance
            featureImportances={trainingResults?.feature_importance}
            className={selectedModel === "regression" ? "col-span-2" : ""}
          />
        ) : null}

        {selectedModel === "classification" ? (
          <>
            <ConfusionMatrix
              data={trainingResults?.all_metrics?.[trainingResults?.model_name]?.confusion_matrix}
            />
            <ClassificationReport
              report={
                trainingResults?.all_metrics?.[trainingResults?.model_name]?.classification_report
              }
            />
            <ROCChart roc={trainingResults?.roc_curve} />
          </>
        ) : selectedModel === "clustering" ? (
          <>
            <ScatterPlot
              className="col-span-2"
              clusters={trainingResults?.scatter_points?.clusters}
              xAxis={trainingResults?.scatter_points?.x_axis}
              yAxis={trainingResults?.scatter_points?.y_axis}
            />
            <ClusterDefinitions
              definitions={trainingResults?.cluster_definitions}
              className="col-span-2"
            />
          </>
        ) : null}

        <ModelsMetricsCard trainingResults={trainingResults} className="col-span-2" />
      </div>
    </section>
  );
}
