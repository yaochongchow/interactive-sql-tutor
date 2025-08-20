import { useState } from 'react';

export default function TableBuilder({ tables, setTables }) {
  const [newTableName, setNewTableName] = useState('');

  const addTable = () => {
    if (newTableName.trim() === '') return;
    setTables([...tables, { table_name: newTableName, columns: [] }]);
    setNewTableName('');
  };

  const addColumn = (tableIndex, columnName, columnType) => {
    const newTables = [...tables];
    newTables[tableIndex].columns.push({ name: columnName, type: columnType });
    setTables(newTables);
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="New table name"
          value={newTableName}
          onChange={(e) => setNewTableName(e.target.value)}
          className="border p-2 rounded w-full"
        />
        <button
          type="button"
          onClick={addTable}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Add Table
        </button>
      </div>

      {tables.map((table, index) => (
        <TableEditor
          key={index}
          table={table}
          onAddColumn={(name, type) => addColumn(index, name, type)}
        />
      ))}

      <textarea
        className="border p-2 w-full"
        rows={6}
        value={JSON.stringify(tables, null, 2)}
        readOnly
      />
    </div>
  );
}

const TableEditor = ({ table, onAddColumn }) => {
  const [columnName, setColumnName] = useState('');
  const [columnType, setColumnType] = useState('');
  const [columnDescription, setColumnDescription] = useState('');

  return (
    <div className="border p-4 rounded bg-gray-50">
      <h3 className="font-bold mb-2">Table: {table.table_name}</h3>
      <ul className="mb-2">
        {table.columns.map((col, i) => (
          <li key={i}>
            - {col.name} ({col.type})
          </li>
        ))}
      </ul>
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Column name"
          value={columnName}
          onChange={(e) => setColumnName(e.target.value)}
          className="border p-2 rounded w-1/2"
          required
        />
        <input
          type="text"
          placeholder="Type (e.g. int, string)"
          value={columnType}
          onChange={(e) => setColumnType(e.target.value)}
          className="border p-2 rounded w-1/2"
          required
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={columnDescription}
          onChange={(e) => setColumnDescription(e.target.value)}
          className="border p-2 rounded w-1/2"
        />
        <button
          type="button"
          onClick={() => {
            if (columnName && columnType && columnDescription) {
              onAddColumn(columnName, columnType);
              setColumnName('');
              setColumnType('');
              setColumnDescription('');
            }
          }}
          className="bg-green-500 text-white px-3 rounded"
        >
          Add Column
        </button>
      </div>
    </div>
  );
};
