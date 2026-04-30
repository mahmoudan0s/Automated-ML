import BaseComponent from "./BaseComponent";
import useCountUp from "../hooks/useCountUp";

const xAxisTicks = [0, 25, 50, 75, 100];
const labelWidthClass = "w-[20ch]";
const labelColumnClass = "grid-cols-[20ch_1fr]";

export default function FeatureImportance() {
    const sortedFeatures = [...featureImportanceData].sort((a, b) => b.importance - a.importance);

    return (
        <BaseComponent title="Feature Importance" description="The importance of each feature in the model's predictions." className="w-full">
            <div className="w-full overflow-x-hidden">
                <div className="pl-4">
                    {sortedFeatures.map((feature, index) => (
                        <FeatureRow key={index} feature={feature} index={index} />
                    ))}
                </div>
                <div className="w-full ml-2">
                    <div className={`grid ${labelColumnClass} items-end gap-4 pb-2`}>
                        <div />
                        <div className="relative h-6 border-t border-gray-300 pl-8 pr-8">
                            {xAxisTicks.map((tick) => {
                                const transform = tick === 0 ? 'translateX(0)' : tick === 100 ? 'translateX(-100%)' : 'translateX(-50%)';
                                return (
                                    <span
                                        key={tick}
                                        className="absolute bottom-0 text-xs font-medium text-slate-500 whitespace-nowrap"
                                        style={{ left: `${tick}%`, transform }}
                                    >
                                        {tick}%
                                    </span>
                                );
                            })}
                        </div>
                    </div>
                </div>
            </div>
        </BaseComponent>
    );
}

function FeatureRow({ feature, index }) {
    const targetPercent = feature.importance * 100;
    const animatedPercent = useCountUp(targetPercent, {
        duration: 1200,
        delay: index * 60,
    });

    return (
        <div className="group flex items-center gap-0 py-2 relative before:absolute before:ml-2 before:left-[20ch] before:top-0 before:h-full before:w-px before:bg-gray-300 before:content-[''] hover:bg-gray-100/80 hover:text-blue-600 transition-colors duration-200 rounded-md">
            <span className={`${labelWidthClass} shrink-0 truncate font-bold text-right mr-2`}>{feature.name}</span>
            <div className="flex items-center gap-2 w-full">
                <div
                    className="group-hover:h-3.5 group-hover:bg-blue-700 transition-[height,background-color] duration-200 h-2.5 rounded-r-full bg-blue-600"
                    style={{ width: `${animatedPercent}%` }}
                />
                <span className="text-xs text-gray-600 group-hover:text-blue-700 transition-colors duration-200 group-hover:font-medium">
                    {animatedPercent.toFixed(1)}%
                </span>
            </div>
        </div>
    );
}

const featureImportanceData = [
  { name: "Monthly Charges", importance: 0.215 },
  { name: "Total Charges", importance: 0.189 },
  { name: "Contract Length", importance: 0.156 },
  { name: "Tenure", importance: 0.25 },
  { name: "Payment Method", importance: 0.12 },
  { name: "Customer Service Calls", importance: 0.075 },
  { name: "Internet Service", importance: 0.05 },
  { name: "Senior Citizen", importance: 0.03 },
  { name: "Dependents", importance: 0.02 },
  { name: "Multiple Lines", importance: 0.01 },
];
