import { useState } from 'react';
import QuickUpload from "./components/QuickUpload";
import PreviewDataTable from "./components/PreviewDataTable";
import BoxData from "./components/BoxData";
import ROCChart from './components/ROCChart';
import ModelSelection from "./components/ModelSelection";
import ConfusionMatrix from './components/ConfusionMatrix';
import FeatureImportance from './components/FeatureImportance';
import ClassificationReport from './components/ClassificationReport';
import TargetColumnSelection from './components/TargetColumnSelection';
import { AngleDownIcon, BullseyeIcon, CrosshairIcon, LineChartIcon, MagnifyingGlassIcon, ScaleBalancedIcon } from './components/icons';

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
  }
];

function App() {
  const [tableData, setTableData] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedTarget, setSelectedTarget] = useState(null);
  const [tableHeaders, setTableHeaders] = useState([]);
  const [fileName, setFileName] = useState('');
  const [page, setPage] = useState(1);

  const handleFileUpload = (data, headers, file) => {
    setTableData(data);
    setTableHeaders(headers);
    setFileName(file.name);
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.12),_transparent_32%),radial-gradient(circle_at_top_right,_rgba(14,165,233,0.10),_transparent_28%),linear-gradient(180deg,_#f8fafc_0%,_#eef2ff_100%)] text-slate-900">
      {/* Page 1 */}
      {page === 1 && (
        <section className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-950">Dataset & Model</h1>
              <p className="mt-1 text-sm text-slate-500">Upload your dataset and configure your model.</p>
            </div>
            <button
              onClick={() => setPage(2)}
              className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 flex items-center gap-2 shadow-md shadow-blue-600/20 active:scale-95"
            >
              View Model Metrics
              <AngleDownIcon size={24} className="-rotate-90" />
            </button>
          </div>

          <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
            <QuickUpload onFileUpload={handleFileUpload} />

            <div className="grid gap-6">
              <ModelSelection selectedModel={selectedModel} setSelectedModel={setSelectedModel} />
              {fileName && (selectedModel === 'classification' || selectedModel === 'regression') ? (
                <TargetColumnSelection headers={tableHeaders} selectedTarget={selectedTarget} setSelectedTarget={setSelectedTarget} />
              ) : null}
            </div>
          </section>

          <section className="rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-[0_18px_50px_rgba(15,23,42,0.07)]">
            <div className="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-xl font-semibold text-slate-950">Data preview</h2>
                <p className="mt-1 text-sm text-slate-500">{fileName ? `Preview of ${fileName}` : 'Upload a file to see a data preview'}</p>
              </div>
              {tableData.length > 0 && <p className="text-sm font-medium text-slate-500">{tableData.length} rows loaded</p>}
            </div>
            {tableData.length > 0 ? (
              <PreviewDataTable tableHeaders={tableHeaders} tableData={tableData} />
            ) : (
              <div className="flex items-center justify-center rounded-[1.5rem] border border-slate-200 bg-slate-50/80 py-12 text-center">
                <p className="text-sm text-slate-500">No data uploaded yet. Use the Quick upload section above to add a file.</p>
              </div>
            )}
          </section>
        </section>
      )}

      {/* Page 2 */}
      {page === 2 && (
        <section className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-950">Model Metrics</h1>
              <p className="mt-1 text-sm text-slate-500">Review the performance of your trained model.</p>
            </div>
            <button
              onClick={() => setPage(1)}
              className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-medium text-blue-600 shadow-sm transition hover:bg-slate-50 active:scale-95"
            >
              <AngleDownIcon size={24} className="rotate-90" />
              Back to Dataset
            </button>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5 mb-8 mt-8">
            {statsData.map((stat) => (
              <BoxData key={stat.id} title={stat.title} value={stat.value} icon={stat.icon} iconStyle={stat.iconStyle} />
            ))}
          </div>

          <div className="grid gap-6 grid-cols-2">
            <ConfusionMatrix />
            <ROCChart />
            <FeatureImportance />
            <ClassificationReport />
          </div>
        </section>
      )}
    </main>
  );
}

export default App;
