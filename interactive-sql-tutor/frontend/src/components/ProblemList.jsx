import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllProblems } from '../api/problem';
import { useNotification } from '../utils/hooks';
import Loading from './Loading';

const TOPICS = [
  'Aggregation Functions',
  'In-Line View',
  'Join',
  'Select',
  'Sub Query',
  'Window Function',
  'With',
];

const DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard'];

export default function ProblemList() {
  const [loading, setLoading] = useState(true);
  const [problems, setProblems] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const navigate = useNavigate();
  const { updateNotification } = useNotification();

  useEffect(() => {
    const fetchProblems = async () => {
      const query = [];
      if (selectedDifficulty) query.push(`difficulty=${selectedDifficulty}`);
      if (selectedTopic) query.push(`topic=${selectedTopic}`);
      const queryString = query.length ? `?${query.join('&')}` : '';

      const { data, error } = await getAllProblems(queryString);
      setLoading(false);
      if (error) return updateNotification('error', JSON.stringify(error));
      setProblems(data);
    };

    fetchProblems();
  }, [selectedTopic, selectedDifficulty, updateNotification]);

  return (
    <>
      <div className="flex gap-4 mb-4">
        <DropDown
          title="All Topics"
          options={TOPICS}
          selectedValue={selectedTopic}
          setSelectedValue={setSelectedTopic}
        />
        <DropDown
          title="All Difficulty Levels"
          options={DIFFICULTY_LEVELS}
          selectedValue={selectedDifficulty}
          setSelectedValue={setSelectedDifficulty}
        />
      </div>

      {loading ? (
        <Loading />
      ) : (
        <table className="w-full">
          <thead>
            <tr className="text-left">
              <th className="p-2">ID</th>
              <th>Title</th>
              <th>Topic</th>
              <th>Acceptance</th>
              <th>Difficulty</th>
            </tr>
          </thead>
          <tbody>
            {problems.map(
              (
                { problem_id, title, topic, difficulty_level, acceptance },
                index
              ) => (
                <tr
                  key={problem_id}
                  className={
                    (index % 2 === 0 ? 'bg-slate-100' : '') + ' cursor-pointer'
                  }
                  onClick={() => navigate(`/problems/${problem_id}`)}
                >
                  <td className="p-2 rounded">{problem_id}</td>
                  <td className="hover:text-blue-400 transition">{title}</td>
                  <td>{topic}</td>
                  <td>{Math.round(acceptance * 10) / 10 + '%'}</td>
                  <td
                    className={
                      difficulty_level === 'Easy'
                        ? 'text-green-500'
                        : difficulty_level === 'Medium'
                        ? 'text-yellow-500'
                        : 'text-red-500'
                    }
                  >
                    {difficulty_level}
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      )}
    </>
  );
}

const DropDown = ({ title, options, selectedValue, setSelectedValue }) => {
  return (
    <select
      className="text-sm border p-2 rounded"
      value={selectedValue}
      onChange={(e) => setSelectedValue(e.target.value)}
    >
      <option value="">{title}</option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
};
