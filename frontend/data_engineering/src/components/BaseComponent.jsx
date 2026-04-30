export default function BaseComponent({ title, componentButton, description, children, actions, className = '' }) {
    return (
        <div className={"rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-[0_18px_50px_rgba(15,23,42,0.07)] " + className}>
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                <div className="w-full flex flex-col gap-1">
                    {title ? componentButton ? (
                        <div className="flex justify-between gap-4">
                            <h1 className="text-2xl font-bold text-slate-950">{title}</h1>
                            {componentButton}
                        </div>
                    ) : (
                        <h1 className="text-2xl font-bold text-slate-950">{title}</h1>
                    ) : null}
                    {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
                </div>

                {actions}
            </div>

            {children && (
                <div className="mt-4">
                    {children}
                </div>
            )}
        </div>
    );
}