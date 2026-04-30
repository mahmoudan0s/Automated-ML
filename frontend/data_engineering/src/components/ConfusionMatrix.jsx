import BaseComponent from "./BaseComponent";
import useCountUp from "../hooks/useCountUp";

const getBlueStyle = (value) => {
    if (!Number.isFinite(value) || value <= 0) {
        return { backgroundColor: "rgb(219, 234, 254)" };
    }
    const clamped = Math.min(value, 1600);
    const t = clamped / 1600;
    const r = Math.round(219 - 189 * t);
    const g = Math.round(234 - 176 * t);
    const b = Math.round(254 - 116 * t);
    return { backgroundColor: `rgb(${r}, ${g}, ${b})` };
};

const getTextColor = (value) => {
    if (!Number.isFinite(value)) return "text-slate-900";
    const t = Math.min(value, 1600) / 1600;
    return t > 0.45 ? "text-white" : "text-slate-900";
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
            aspectRatio: "1",
            borderRadius: "6px",
            position: "relative",
        }}
        title={`${label}: ${Math.round(value)}`}
    >
        {Math.round(value)}
    </div>
);

export default function ConfusionMatrix() {
    const { tp, fn, fp, tn } = confusionMatrixData;
    const animatedTp = useCountUp(tp, { duration: 1500 });
    const animatedFn = useCountUp(fn, { duration: 1500, delay: 120 });
    const animatedFp = useCountUp(fp, { duration: 1500, delay: 240 });
    const animatedTn = useCountUp(tn, { duration: 1500, delay: 360 });

    const maxValue = Math.max(tp, fn, fp, tn, 1);

    // Vertical gradient: top = max (dark), bottom = 0 (light)
    const buildLegendGradient = (steps = 8) => {
        const stops = [];
        for (let i = 0; i < steps; i++) {
            const ratio = i / (steps - 1); // 0..1 top->bottom
            const value = maxValue * (1 - ratio);  // top is max, bottom is 0
            const color = getBlueStyle(value).backgroundColor;
            const pos = Math.round(ratio * 100);
            stops.push(`${color} ${pos}%`);
        }
        return `linear-gradient(to bottom, ${stops.join(', ')})`;
    };

    const legendGradient = buildLegendGradient(8);

    return (
        <BaseComponent title="Confusion Matrix" description="A visual representation of the model's performance in terms of true positives, false positives, true negatives, and false negatives." className="w-full">
            <div className="flex flex-row-reverse items-stretch gap-3">

                {/* Vertical Legend */}
                <div className="flex flex-row items-stretch gap-1.5 self-stretch" style={{ paddingTop: "36px" /* offset for header row */ }}>
                    <div className="flex flex-col justify-between text-xs text-slate-500 text-right" style={{ minWidth: "18px" }}>
                        <div className="flex items-center justify-end gap-0.5">
                            <div style={{ width: 6, height: 6, backgroundColor: "rgb(30, 58, 138)", borderRadius: 1 }} />
                            <span>{Math.round(maxValue)}</span>
                        </div>
                        <div className="flex items-center justify-end gap-0.5">
                            <div style={{ width: 6, height: 6, backgroundColor: "rgb(109, 146, 196)", borderRadius: 1 }} />
                            <span>{Math.round(maxValue / 2)}</span>
                        </div>
                        <div className="flex items-center justify-end gap-0.5">
                            <div style={{ width: 6, height: 6, backgroundColor: "rgb(219, 234, 254)", borderRadius: 1 }} />
                            <span>0</span>
                        </div>
                    </div>
                    <div
                        aria-hidden
                        style={{
                            width: 12,
                            borderRadius: 6,
                            background: legendGradient,
                            boxShadow: '0 6px 18px rgba(15,23,42,0.06)',
                            alignSelf: 'stretch',
                        }}
                    />
                </div>

                {/* Matrix */}
                <div className="flex-1 relative">
                    <div
                        className="absolute -left-5 top-1/2 -translate-y-1/2 -rotate-90 text-xs text-slate-400 tracking-wide uppercase"
                        style={{ left: "-22px" }}
                    >
                        Actual
                    </div>
                    <div className="absolute -bottom-5 left-1/2 translate-x-4 text-xs text-slate-400 tracking-wide uppercase">
                        Predicted
                    </div>

                    <div
                        className="grid gap-1 text-center"
                        style={{ gridTemplateColumns: "auto 1fr 1fr", gridTemplateRows: "auto 1fr 1fr" }}
                    >
                        {/* Header row */}
                        <div />
                        <div className="p-2 text-sm font-medium text-slate-500">Positive</div>
                        <div className="p-2 text-sm font-medium text-slate-500">Negative</div>

                        {/* Row: Positive */}
                        <div className="p-2 text-sm font-medium text-slate-500 flex items-center justify-end pr-3">Positive</div>
                        <Cell value={animatedTp} label="True Positives" />
                        <Cell value={animatedFn} label="False Negatives" />

                        {/* Row: Negative */}
                        <div className="p-2 text-sm font-medium text-slate-500 flex items-center justify-end pr-3">Negative</div>
                        <Cell value={animatedFp} label="False Positives" />
                        <Cell value={animatedTn} label="True Negatives" />
                    </div>
                </div>

            </div>
        </BaseComponent>
    );
}

const confusionMatrixData = {
    tp: 120,
    fp: 400,
    fn: 20,
    tn: 800,
};