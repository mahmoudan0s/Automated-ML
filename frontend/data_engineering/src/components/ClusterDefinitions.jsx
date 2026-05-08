import BaseComponent from "./BaseComponent";
import BaseTable from "./BaseTable";

export default function ClusterDefinitions({ definitions, className = "" }) {
  const tableHeaders = ["Cluster", "Definition"];
  const tableData = Object.entries(definitions).map(([clusterId, description]) => ({
    Cluster: `Cluster ${clusterId}`,
    Definition: description,
  }));

  return (
    <BaseComponent title="Cluster Definitions" className={className}>
      <BaseTable tableHeaders={tableHeaders} tableData={tableData} />
    </BaseComponent>
  );
}
