const tdStyles = 'text-sm border border-dashed border-slate-300 px-2 py-1';

export default function TableSection({
  tableName = '',
  header = [],
  rows = [],
}) {
  return (
    <div className="flex flex-col gap-2" key={tableName}>
      <span className="font-semibold">{tableName}</span>
      <table className="text-left">
        <thead>
          <tr>
            {header.map((item) => (
              <th key={item} className={tdStyles}>
                {item}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {row.map((item, i2) => (
                <td key={i2} className={tdStyles}>
                  {typeof item === 'string' ? item : JSON.stringify(item)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
