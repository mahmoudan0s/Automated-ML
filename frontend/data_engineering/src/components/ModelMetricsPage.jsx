import BoxData from "./BoxData";
import ClassificationReport from "./ClassificationReport";
import ConfusionMatrix from "./ConfusionMatrix";
import FeatureImportance from "./FeatureImportance";
import ROCChart from "./ROCChart";
import {
    AngleDownIcon,
    BullseyeIcon,
    CrosshairIcon,
    FloppyDiskIcon,
    LineChartIcon,
    MagnifyingGlassIcon,
    ScaleBalancedIcon,
} from "./icons";

const statsData = [
    {
        id: 1,
        title: "Accuracy",
        value: "89.4%",
        icon: <BullseyeIcon className="w-6 h-6 text-blue-600" />,
        iconStyle: "bg-blue-100 dark:bg-bg-surface-blue-default-dark",
    },
    {
        id: 2,
        title: "Precision",
        value: "88.7%",
        icon: <CrosshairIcon className="w-6 h-6 text-emerald-600" />,
        iconStyle: "bg-green-100 dark:bg-bg-surface-green-default-dark",
    },
    {
        id: 3,
        title: "Recall",
        value: "87.1%",
        icon: <MagnifyingGlassIcon className="w-6 h-6 text-amber-600" />,
        iconStyle: "bg-yellow-100 dark:bg-bg-surface-yellow-default-dark",
    },
    {
        id: 4,
        title: "F1 Score",
        value: "87.9%",
        icon: <ScaleBalancedIcon className="w-6 h-6 text-rose-600" />,
        iconStyle: "bg-red-100 dark:bg-bg-surface-red-default-dark",
    },
    {
        id: 5,
        title: "AUC-ROC",
        value: "0.93",
        icon: <LineChartIcon className="w-6 h-6 text-purple-600" />,
        iconStyle: "bg-purple-100 dark:bg-bg-surface-purple-default-dark",
    },
];

export default function ModelMetricsPage({ onBackToDataset }) {
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

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5 mb-8 mt-8">
                {statsData.map((stat) => (
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
                <ConfusionMatrix />
                <FeatureImportance />
                <ROCChart />
                <ClassificationReport />
            </div>
        </section>
    );
}
