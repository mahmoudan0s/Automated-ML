import PreviewDataTable from "./PreviewDataTable";
import QuickUpload from "./QuickUpload";
import ModelSelection from "./ModelSelection";
import TargetColumnSelection from "./TargetColumnSelection";
import { AngleDownIcon, PlayIcon } from "./icons";

export default function DatasetModelPage({
    tableData,
    tableHeaders,
    fileName,
    selectedModel,
    setSelectedModel,
    selectedTarget,
    setSelectedTarget,
    onFileUpload,
    onViewModelMetrics,
}) {
    const isTrainDisabled =
        !fileName ||
        !selectedModel ||
        (selectedModel === "classification" && !selectedTarget);

    const isViewMetricsDisabled = !fileName || !selectedModel || (selectedModel === "classification" && !selectedTarget) || (selectedModel === "regression" && !selectedTarget);

    return (
        <section className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-950">Dataset & Model</h1>
                    <p className="mt-1 text-sm text-slate-500">Upload your dataset and configure your model.</p>
                </div>
                <button
                    onClick={onViewModelMetrics}
                    disabled={isViewMetricsDisabled}
                    className={`flex items-center gap-2 rounded-lg px-6 py-3 text-sm font-semibold transition ${
                        isViewMetricsDisabled
                            ? "cursor-not-allowed bg-slate-200 text-slate-400 shadow-none"
                            : "bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-md shadow-blue-600/20 hover:shadow-lg hover:shadow-blue-600/30 active:scale-95"
                    }`}
                >
                    View Model Metrics
                    <AngleDownIcon size={24} className="-rotate-90" />
                </button>
            </div>

            <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
                <QuickUpload onFileUpload={onFileUpload} />

                <div className="grid gap-6">
                    <ModelSelection selectedModel={selectedModel} setSelectedModel={setSelectedModel} />
                    {fileName &&
                    (selectedModel === "classification" || selectedModel === "regression") ? (
                        <TargetColumnSelection
                            headers={tableHeaders}
                            selectedTarget={selectedTarget}
                            setSelectedTarget={setSelectedTarget}
                        />
                    ) : null}

                    <button
                        disabled={isTrainDisabled}
                        className={`group inline-flex w-full items-center justify-center gap-3 rounded-2xl border px-6 py-3.5 text-sm font-semibold tracking-wide transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 ${
                            isTrainDisabled
                                ? "cursor-not-allowed border-slate-200 bg-slate-200 text-slate-400 shadow-none"
                                : "border-emerald-500/20 bg-gradient-to-r from-emerald-500 via-green-600 to-teal-600 text-white shadow-[0_14px_35px_rgba(22,163,74,0.28)] hover:-translate-y-0.5 hover:shadow-[0_18px_45px_rgba(22,163,74,0.32)] active:translate-y-0 active:scale-[0.99]"
                        }`}
                    >
                        <span className={`flex h-8 w-8 items-center justify-center rounded-full transition ${isTrainDisabled ? "bg-white/60 ring-slate-300/60" : "bg-white/15 ring-1 ring-inset ring-white/20 group-hover:bg-white/20"}`}>
                            <PlayIcon size={11} className="shrink-0" />
                        </span>
                        Train Model
                    </button>
                </div>
            </section>

            <section className="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-[0_18px_50px_rgba(15,23,42,0.07)]">
                <div className="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <h2 className="text-xl font-semibold text-slate-950">Data preview</h2>
                        <p className="mt-1 text-sm text-slate-500">
                            {fileName ? `Preview of ${fileName}` : "Upload a file to see a data preview"}
                        </p>
                    </div>
                    {tableData.length > 0 && (
                        <p className="text-sm font-medium text-slate-500">{tableData.length} rows loaded</p>
                    )}
                </div>
                {tableData.length > 0 ? (
                    <PreviewDataTable tableHeaders={tableHeaders} tableData={tableData} />
                ) : (
                    <div className="flex items-center justify-center rounded-[1.5rem] border border-slate-200 bg-slate-50/80 py-12 text-center">
                        <p className="text-sm text-slate-500">
                            No data uploaded yet. Use the Quick upload section above to add a file.
                        </p>
                    </div>
                )}
            </section>
        </section>
    );
}
