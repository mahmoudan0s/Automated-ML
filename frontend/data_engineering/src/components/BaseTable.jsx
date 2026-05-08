export default function BaseTable({ tableHeaders, tableData }) {
  return (
    <div className="overflow-hidden rounded-[1.5rem] border border-slate-200">
      <div className="overflow-x-auto">
        <table className="min-w-full border-separate border-spacing-0">
          <thead>
            <tr>
              {tableHeaders.map((header) => (
                <th
                  key={header}
                  className="text-center border-b border-slate-200 bg-slate-50 px-5 py-4 text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 whitespace-nowrap"
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
                className={`group border-b border-slate-200 transition-colors last:border-b-0 hover:bg-blue-50/70 ${
                  row._isSelected ? "bg-yellow-100" : "bg-white"
                }`}
              >
                {tableHeaders.map((header) => {
                  const value = row[header];
                  const parsedNumber = Number(value);
                  const isNumber = !isNaN(parsedNumber) && value !== "";
                  const isPercentage = String(value).includes("%");
                  const isEmpty = value === null || value === undefined || value === "";
                  const alignment =
                    isEmpty || isNumber || isPercentage ? "text-center" : "text-left";

                  return (
                    <td
                      key={`${index}-${header}`}
                      className={`px-5 py-4 text-sm ${alignment} ${
                        isEmpty ? "text-slate-400 italic" : "text-slate-700"
                      }`}
                    >
                      {isEmpty ? "—" : String(value)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
