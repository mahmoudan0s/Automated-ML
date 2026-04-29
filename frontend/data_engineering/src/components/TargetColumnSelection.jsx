import BaseComponent from "./BaseComponent";

export default function TargetColumnSelection({ headers, selectedTarget, setSelectedTarget }) {
    const actions = (
        <div className="w-full max-w-md">
            <label htmlFor="target-select" className="mb-2 block text-sm font-medium text-slate-700">
                Select target column
            </label>

            <select
                id="target-select"
                value={selectedTarget}
                onChange={(e) => setSelectedTarget(e.target.value)}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none transition focus:border-blue-300 focus:bg-white focus:ring-4 focus:ring-blue-100"
            >
                <option value="">-- Choose a target column --</option>
                {headers.map((header, index) => (
                    <option key={index} value={header}>
                        {header}
                    </option>
                ))}
            </select>
        </div>
    );

    return (
        <BaseComponent title="Target Column Selection" description="Choose the target column for your model training." actions={actions} />
    );
}