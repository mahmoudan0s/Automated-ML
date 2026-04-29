import BaseComponent from "./BaseComponent"

export default function ModelSelection({ selectedModel, setSelectedModel }) {
    const actions = (
        <div className="w-full max-w-md">
            <label htmlFor="model-select" className="mb-2 block text-sm font-medium text-slate-700">
                Select model
            </label>

            <select
                id="model-select"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none transition focus:border-blue-300 focus:bg-white focus:ring-4 focus:ring-blue-100"
            >
                <option value="">-- Choose a model --</option>
                <option value="classification">Classification model</option>
                <option value="regression">Regression model</option>
                <option value="clustering">Clustering model</option>
            </select>
        </div>
    );

    return (
        <BaseComponent title="Model Selection" description="Choose the type of model you want to train on your dataset." actions={actions} />
    );
}