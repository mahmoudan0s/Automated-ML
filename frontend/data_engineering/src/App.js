import { useState } from 'react';
import DatasetModelPage from './components/DatasetModelPage';
import ModelMetricsPage from './components/ModelMetricsPage';

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
      {page === 1 && (
        <DatasetModelPage
          tableData={tableData}
          tableHeaders={tableHeaders}
          fileName={fileName}
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
          selectedTarget={selectedTarget}
          setSelectedTarget={setSelectedTarget}
          onFileUpload={handleFileUpload}
          onViewModelMetrics={() => setPage(2)}
        />
      )}

      {page === 2 && (
        <ModelMetricsPage onBackToDataset={() => setPage(1)} />
      )}
    </main>
  );
}

export default App;
