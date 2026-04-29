export default function BoxData({ icon, title, value, iconStyle = "", className = "", ...props }) {
    return (
        <div
            className={`
                group relative flex items-center gap-4 p-5
                bg-bg-surface-primary-default-light dark:bg-bg-surface-primary-default-dark
                rounded-2xl border border-border-primary-default-light dark:border-border-primary-default-dark
                shadow-sm hover:shadow-md hover:border-primary-300 dark:hover:border-primary-700
                transition-all duration-300 hover:-translate-y-1
                ${className}
            `}
            {...props}
        >
            <div
                className={`
                    shrink-0 w-14 h-14 rounded-2xl
                    flex items-center justify-center
                    bg-linear-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900
                    text-primary-600 dark:text-primary-400
                    shadow-inner group-hover:shadow-md group-hover:scale-105
                    transition-all duration-300
                    ${iconStyle}
                `}
            >
                {icon}
            </div>

            <div className="flex flex-col grow min-w-0">
                <p className="text-xs font-medium uppercase tracking-wider text-text-secondary-default-light dark:text-text-secondary-default-dark">
                    {title}
                </p>
                <h2 className="text-2xl md:text-3xl font-bold text-text-primary-active-light dark:text-text-primary-active-dark leading-tight tracking-tight truncate">
                    {value}
                </h2>
            </div>
        </div>
    );
}