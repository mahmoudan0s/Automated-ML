import BoxData from "./BoxData";
import ClassificationReport from "./ClassificationReport";
import ConfusionMatrix from "./ConfusionMatrix";
import FeatureImportance from "./FeatureImportance";
import ROCChart from "./ROCChart";
import ScatterPlot from "./ScatterPlot";
import {
    AngleDownIcon,
    BullseyeIcon,
    CrosshairIcon,
    DiagramProjectIcon,
    FloppyDiskIcon,
    LayerGroupIcon,
    LineChartIcon,
    MagnifyingGlassIcon,
    Minimize2Icon,
    RulerIcon,
    ScaleBalancedIcon,
    UsersIcon,
    WarningIcon,
} from "./icons";

const statsData = {
    "classification": [
        {
            id: "accuracy",
            title: "Accuracy",
            value: "92.5%",
            icon: BullseyeIcon,
            iconStyle: "text-green-500 bg-green-100",
        },
        {
            id: "precision",
            title: "Precision",
            value: "89.3%",
            icon: CrosshairIcon,
            iconStyle: "text-blue-500 bg-blue-100",
        },
        {
            id: "recall",
            title: "Recall",
            value: "94.1%",
            icon: MagnifyingGlassIcon,
            iconStyle: "text-yellow-500 bg-yellow-100",
        },
        {
            id: "f1_score",
            title: "F1 Score",
            value: "91.6%",
            icon: ScaleBalancedIcon,
            iconStyle: "text-purple-500 bg-purple-100",
        },
    ],
    "regression": [
        {
            id: "r2_score",
            title: "R² Score",
            value: "0.89",
            icon: BullseyeIcon,
            iconStyle: "text-green-500 bg-green-100",
        },
        {
            id: "mse",
            title: "Mean Squared Error",
            value: "0.025",
            icon: WarningIcon,
            iconStyle: "text-red-500 bg-red-100",
        },
        {
            id: "rmse",
            title: "Root Mean Squared Error",
            value: "0.158",
            icon: LineChartIcon,
            iconStyle: "text-blue-500 bg-blue-100",
        },
        {
            id: "mae",
            title: "Mean Absolute Error",
            value: "0.012",
            icon: RulerIcon,
            iconStyle: "text-orange-500 bg-orange-100",
        },
    ],
    "clustering": [
        {
            id: "silhouette",
            title: "Silhouette Score",
            value: "0.65",
            icon: DiagramProjectIcon,
            iconStyle: "text-blue-500 bg-blue-100",
        },
        {
            id: "clusters",
            title: "Number of Clusters",
            value: "4",
            icon: LayerGroupIcon,
            iconStyle: "text-purple-500 bg-purple-100",
        },
        {
            id: "inertia",
            title: "Inertia (WCSS)",
            value: "123.4",
            icon: Minimize2Icon,
            iconStyle: "text-green-500 bg-green-100",
        },
        {
            id: "avg-size",
            title: "Avg Cluster Size",
            value: "250",
            icon: UsersIcon,
            iconStyle: "text-indigo-500 bg-indigo-100",
        }
    ],
};

export default function ModelMetricsPage({ onBackToDataset, selectedModel }) {
    const metrics = statsData[selectedModel] ?? [];

    return (
        <section className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-950">Model Metrics</h1>
                    <p className="mt-1 text-sm text-slate-500">Review the performance of your trained model.</p>
                </div>

                <div className="flex items-center gap-4">
                    <button
                        onClick={onBackToDataset}
                        className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-medium text-blue-600 shadow-sm transition hover:bg-slate-50 active:scale-95"
                    >
                        <AngleDownIcon size={24} className="rotate-90" />
                        Back to Dataset
                    </button>

                    <button className="flex items-center gap-2 rounded-xl bg-green-600 px-6 py-3 text-sm font-medium text-white shadow-md transition hover:bg-green-700 active:scale-95">
                        Save Model
                        <FloppyDiskIcon size={20} />
                    </button>
                </div>
            </div>

            <div className={`mx-auto mb-8 mt-8 grid w-full gap-4 sm:grid-cols-2 lg:grid-cols-4 max-w-7xl`}>
                {metrics.map((stat) => (
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
                {selectedModel === "classification" ? (
                    <ConfusionMatrix />

                ) : selectedModel === "regression" ? (
                    <ROCChart />

                ) : selectedModel === "clustering" ? ( 
                    <ScatterPlot className="col-span-2" />
                ) : null}

                {selectedModel === "classification" || selectedModel === "regression" ? <FeatureImportance /> : null}
                <ClassificationReport className="col-span-2" />
            </div>
        </section>
    );
}
