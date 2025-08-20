import TableSection from "./TableSection";

const labelStyles = ' text-xs w-fit bg-slate-100 px-2 py-1 rounded-full';
const formatColumns = ['Column Name', 'Type', 'Description'];

export default function DescriptionSection({ problem }) {
  const {
    problem_id,
    title,
    description,
    difficulty_level,
    topic,
    acceptance,
    tables,
    input_data = {},
    expected_output = [],
  } = problem;
  const inputTables = Object.entries(input_data);

  return (
    <>
      <h1 className="text-2xl font-semibold">{problem_id + '. ' + title}</h1>
      <div className="flex gap-3">
        <label
          title="difficulty level"
          className={
            (difficulty_level === 'Easy'
              ? 'text-green-500'
              : difficulty_level === 'Medium'
              ? 'text-yellow-500'
              : 'text-red-500') + labelStyles
          }
        >
          {difficulty_level}
        </label>
        <label title="topic" className={'text-slate-800' + labelStyles}>
          {topic}
        </label>
        <label title="acceptance rate" className={'text-slate-800' + labelStyles}>
          {acceptance + '%'}
        </label>
      </div>
      <p>{description}</p>
      {tables?.map(({ table_name, columns }) => (
        <TableSection
          key={table_name}
          tableName={'Schema: ' + table_name}
          header={formatColumns}
          rows={columns?.map(({ name, type, description = '' }) => [
            name,
            type,
            description,
          ])}
        />
      ))}
      {inputTables?.map(([table_name, value]) => (
        <TableSection
          key={table_name}
          tableName={'Example input: ' + table_name}
          header={value[0]}
          rows={value.slice(1)}
        />
      ))}
      <TableSection
        tableName="Example output"
        header={expected_output[0]}
        rows={expected_output.slice(1)}
      />
    </>
  );
}
