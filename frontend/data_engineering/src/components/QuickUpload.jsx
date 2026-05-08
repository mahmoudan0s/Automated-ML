import { useRef, useState } from 'react';
import { CloudUploadIcon } from "./icons";

// Simple CSV parser
const parseCSV = (text) => {
  const lines = text.trim().split('\n');
  if (lines.length === 0) return { headers: [], data: [] };
  
  const headers = lines[0].split(',').map(h => h.trim());
  const data = lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim());
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index] || '';
    });
    return row;
  });
  
  return { headers, data };
};

// XLSX parser using xlsx library
const parseXLSX = async (file) => {
  try {
    const url = URL.createObjectURL(file);
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    
    // Import xlsx dynamically
    const XLSX = await import('xlsx');
    const workbook = XLSX.read(new Uint8Array(arrayBuffer), { type: 'array' });
    const worksheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[worksheetName];
    const data = XLSX.utils.sheet_to_json(worksheet);
    
    if (data.length === 0) return { headers: [], data: [] };
    
    const headers = Object.keys(data[0]);
    return { headers, data };
  } catch (error) {
    console.error('Error parsing XLSX:', error);
    throw new Error('Failed to parse XLSX file');
  }
};

export default function QuickUpload({ onFileUpload }) {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFile = async (file) => {
    if (!file) return;

    setError('');
    setUploading(true);

    try {
      let result;
      const ext = file.name.split('.').pop().toLowerCase();

      if (ext === 'csv') {
        const text = await file.text();
        result = parseCSV(text);
      } else if (['xlsx', 'xls'].includes(ext)) {
        result = await parseXLSX(file);
      } else {
        throw new Error('Unsupported file format. Please use CSV, XLSX, or XLS.');
      }

      if (result.data.length === 0) {
        throw new Error('File is empty or contains no data rows.');
      }

      onFileUpload(result.data, result.headers, file);
    } catch (err) {
      setError(err.message || 'Failed to parse file');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
      // Reset input so same file can be uploaded again
      e.target.value = '';
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  return (
    <section className="relative overflow-hidden rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-[0_18px_50px_rgba(15,23,42,0.07)]">
      <div className="absolute right-0 top-0 h-32 w-32 translate-x-12 -translate-y-12 rounded-full bg-blue-100/60 blur-3xl" />
      <div className="relative flex flex-col gap-6">
        <div>
          <h2 className="text-xl font-semibold text-slate-950">Quick upload</h2>
          <p className="mt-1 text-sm text-slate-500">Add a file to start the pipeline with a focused, guided flow.</p>
        </div>

        <div 
          className="flex min-h-[20rem] flex-col items-center justify-center gap-5 rounded-[1.5rem] border-2 border-dashed border-slate-200 bg-slate-50/70 p-6 text-center transition hover:border-blue-300 hover:bg-white"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50 text-[var(--color-icon-accent-default-light)] shadow-sm">
            <CloudUploadIcon size={32} />
          </div>

          <div className="max-w-xs">
            <h3 className="text-base font-semibold text-slate-950">Drop a file here</h3>
            <p className="mt-2 text-sm leading-6 text-slate-500">CSV, XLSX, or XLS are supported. Click the button below to browse your local files.</p>
          </div>

          <button 
            onClick={handleButtonClick}
            disabled={uploading}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-950/10 transition hover:-translate-y-0.5 hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span className="text-base leading-none">{uploading ? '...' : '+'}</span>
            {uploading ? 'Processing...' : 'Choose files'}
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileInput}
            className="hidden"
          />
        </div>

        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-4">
            <p className="text-sm font-medium text-red-900">{error}</p>
          </div>
        )}

        <div className="grid gap-3 sm:grid-cols-2">
          <div className="rounded-2xl bg-slate-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Formats</p>
            <p className="mt-2 text-sm font-medium text-slate-900">CSV, XLSX, XLS</p>
          </div>
          <div className="rounded-2xl bg-slate-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Max size</p>
            <p className="mt-2 text-sm font-medium text-slate-900">50MB</p>
          </div>
        </div>
      </div>
    </section>
  );
}