import { useState } from 'react';
import { AngleDownIcon } from './icons';
import BaseComponent from './BaseComponent';
import BaseTable from './BaseTable';

export default function PreviewDataTable({ tableHeaders, tableData }) {
    const DISPLAY_ROW_LIMIT = 10;
  
    const [currentPage, setCurrentPage] = useState(1);
    const numOfPages = Math.ceil(tableData.length / DISPLAY_ROW_LIMIT);
    const displayData = tableData.slice((currentPage - 1) * DISPLAY_ROW_LIMIT, currentPage * DISPLAY_ROW_LIMIT);
    
    // Handle empty data
    if (!tableHeaders || tableHeaders.length === 0 || !tableData || tableData.length === 0) {
        return (
            <div className="flex items-center justify-center rounded-[1.5rem] border border-slate-200 bg-slate-50/80 py-12 text-center">
                <p className="text-sm text-slate-500">No data to display</p>
            </div>
        );
    }
    
    return (
        <BaseComponent title="Preview Data" description="Inspect the uploaded dataset before training.">
            <div className="overflow-hidden rounded-[1.5rem] border border-slate-200 bg-slate-50/80 shadow-inner">
                <BaseTable tableHeaders={tableHeaders} tableData={displayData} DISPLAY_ROW_LIMIT={DISPLAY_ROW_LIMIT} />
                
                {tableData.length > DISPLAY_ROW_LIMIT && (
                    <div className="flex flex-row justify-between items-center border-t border-slate-200 bg-slate-50 px-5 py-3 text-center text-xs text-slate-600">
                        <div className="text-center text-xs text-slate-600">
                            Showing first {DISPLAY_ROW_LIMIT} of {tableData.length} rows
                        </div>

                        {numOfPages > 1 && (
                            <div className="flex items-center justify-center gap-2 p-4">
                                <button onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1}>
                                    <AngleDownIcon size={16} className="rotate-90 text-slate-500" />
                                </button>

                                <span className="text-sm text-slate-500">Page {currentPage} of {numOfPages}</span>

                                <button onClick={() => setCurrentPage((prev) => Math.min(prev + 1, numOfPages))} disabled={currentPage === numOfPages}>
                                    <AngleDownIcon size={16} className="-rotate-90 text-slate-500" />
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </BaseComponent>
    );
}