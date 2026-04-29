export default function BaseTable({ tableHeaders, tableData, DISPLAY_ROW_LIMIT = 10 }) {
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full border-separate border-spacing-0">
                <thead>
                    <tr>
                        {tableHeaders.map((header) => (
                            <th
                                key={header}
                                className="border-b border-slate-200 bg-slate-50 px-5 py-4 text-left text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 whitespace-nowrap"
                            >
                                {header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {tableData.map((row, index) => (
                        <tr
                            key={index}
                            className="group border-b border-slate-200 bg-white transition-colors last:border-b-0 hover:bg-blue-50/70"
                        >
                            {tableHeaders.map((header) => (
                                <td
                                    key={`${index}-${header}`}
                                    className="px-5 py-4 text-sm text-slate-700 whitespace-nowrap truncate max-w-xs"
                                >
                                    {String(row[header] || '').substring(0, DISPLAY_ROW_LIMIT)}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}