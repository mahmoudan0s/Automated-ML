import { useState } from 'react';
import DatasetModelPage from './components/DatasetModelPage';
import ModelMetricsPage from './components/ModelMetricsPage';
import useFetch from './hooks/useFetch';

const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api/v1';

function App() {
  const [tableData, setTableData] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedTarget, setSelectedTarget] = useState(null);
  const [tableHeaders, setTableHeaders] = useState([]);
  const [fileName, setFileName] = useState('');
  const [fileObj, setFileObj] = useState(null);
  const [page, setPage] = useState(1);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingResults, setTrainingResults] = useState(null);
  const { request } = useFetch();

  const handleFileUpload = (data, headers, file) => {
    setTableData(data);
    setTableHeaders(headers);
    setFileName(file.name);
    setFileObj(file);
  };

  const handleTrainModel = async () => {
    if (!fileObj || !selectedModel) {
      alert('Please select a file and model type');
      return;
    }

    if ((selectedModel === 'classification' || selectedModel === 'regression') && !selectedTarget) {
      alert('Please select a target column');
      return;
    }

    setIsTraining(true);
    try {
      // Step 1: Upload file to backend
      const formData = new FormData();
      formData.append('file', fileObj);
      const uploadData = await request(`${API_BASE}/data/upload/1`, {
        method: 'POST',
        body: formData,
      });

      const filePath = uploadData.file_path;

      // Step 2: Train model with uploaded file
      const trainForm = new FormData();
      trainForm.append('file_path', filePath);
      trainForm.append('problem_type', selectedModel);
      if (selectedTarget) trainForm.append('target_column', selectedTarget);

      const results = await request(`${API_BASE}/train/run`, {
        method: 'POST',
        body: trainForm,
      });

      setTrainingResults(results);
      setPage(2);
    } catch (err) {
      console.error('Training error:', err);
      alert(err.message || 'Training failed');
    } finally {
      setIsTraining(false);
    }
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
          onTrainModel={handleTrainModel}
          isTraining={isTraining}
        />
      )}

      {page === 2 && (
        <ModelMetricsPage 
          onBackToDataset={() => setPage(1)} 
          selectedModel={selectedModel}
          trainingResults={trainingResults}
        />
      )}
    </main>
  );
}

export default App;
