import BaseComponent from "./BaseComponent";

const getBlueStyle = (value) => {
    if (!Number.isFinite(value) || value <= 0) {
        return { backgroundColor: "rgb(219, 234, 254)" }; // blue-200ish for zero
    }
    const clamped = Math.min(value, 1600);
    const t = clamped / 1600;
    // Interpolate from light blue → dark navy
    const r = Math.round(219 - 189 * t);  // 219 → 30
    const g = Math.round(234 - 176 * t);  // 234 → 58
    const b = Math.round(254 - 116 * t);  // 254 → 138
    return { backgroundColor: `rgb(${r}, ${g}, ${b})` };
};

const getTextColor = (value) => {
    if (!Number.isFinite(value)) return "text-slate-700";
    const t = Math.min(value, 1600) / 1600;
    return t > 0.45 ? "text-white" : "text-slate-800";
};

const Cell = ({ value, label }) => (
    <div
        className={`
            flex items-center justify-center text-lg font-bold
            transition-all duration-200 ease-out
            cursor-pointer select-none
            hover:scale-[1.06] hover:brightness-110 hover:z-10 hover:ring-2 hover:ring-blue-400 hover:ring-offset-1
            ${getTextColor(value)}
        `}
        style={{
            ...getBlueStyle(value),
            minHeight: "72px",
            borderRadius: "6px",
            position: "relative",
        }}
        title={`${label}: ${value}`}
    >
        {value}
    </div>
);

export default function ConfusionMatrix() {
    const { tp, fn, fp, tn } = confusionMatrixData;

    return (
        <BaseComponent title="Confusion Matrix" description="A visual representation of the model's performance in terms of true positives, false positives, true negatives, and false negatives." className="w-full">
            <div className="p-4">
                <div
                    className="grid gap-1 text-center relative"
                    style={{ gridTemplateColumns: "auto 1fr 1fr", gridTemplateRows: "auto 1fr 1fr" }}
                >
                    {/* Axis labels */}
                    <div className="absolute -left-6 top-1/2 -translate-y-1/2 -rotate-90 text-xs text-slate-400 tracking-wide uppercase">
                        Actual
                    </div>
                    <div className="absolute -bottom-7 left-1/2 translate-x-4 text-xs text-slate-400 tracking-wide uppercase">
                        Predicted
                    </div>

                    {/* Header row */}
                    <div />
                    <div className="p-2 text-sm font-medium text-slate-500">Positive</div>
                    <div className="p-2 text-sm font-medium text-slate-500">Negative</div>

                    {/* Row: Positive */}
                    <div className="p-2 text-sm font-medium text-slate-500 flex items-center justify-end pr-3">Positive</div>
                    <Cell value={tp} label="True Positives" />
                    <Cell value={fn} label="False Negatives" />

                    {/* Row: Negative */}
                    <div className="p-2 text-sm font-medium text-slate-500 flex items-center justify-end pr-3">Negative</div>
                    <Cell value={fp} label="False Positives" />
                    <Cell value={tn} label="True Negatives" />
                </div>
            </div>
        </BaseComponent>
    );
}

const confusionMatrixData = {
  tp: 120, // True Positives
  fp: 30,  // False Positives
  fn: 20,  // False Negatives
  tn: 150, // True Negatives
};