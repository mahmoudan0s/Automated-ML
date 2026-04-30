import { useEffect, useState } from "react";

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

export default function useCountUp(
    targetValue,
    { duration = 1200, delay = 0, startValue = 0, enabled = true } = {}
) {
    const [displayValue, setDisplayValue] = useState(startValue);

    useEffect(() => {
        const target = Number.isFinite(targetValue) ? targetValue : 0;

        if (!enabled) {
            setDisplayValue(target);
            return;
        }

        let animationFrameId;
        let timeoutId;
        let startTime;

        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const elapsed = timestamp - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = easeOutCubic(progress);
            setDisplayValue(startValue + (target - startValue) * eased);

            if (progress < 1) {
                animationFrameId = requestAnimationFrame(step);
            }
        };

        setDisplayValue(startValue);
        timeoutId = setTimeout(() => {
            animationFrameId = requestAnimationFrame(step);
        }, Math.max(0, delay));

        return () => {
            clearTimeout(timeoutId);
            cancelAnimationFrame(animationFrameId);
        };
    }, [targetValue, duration, delay, startValue, enabled]);

    return displayValue;
}
