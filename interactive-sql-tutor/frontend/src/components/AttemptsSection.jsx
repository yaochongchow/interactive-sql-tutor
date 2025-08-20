import { useEffect, useState } from 'react';
import { getAttemptHistory } from '../api/problem';
import { useAuth, useNotification } from '../utils/hooks';

const tdStyles = 'px-4 py-2 border-b text-center';

export default function AttemptsSection({ problemId }) {
  const [attempts, setAttempts] = useState([]);
  const { updateNotification } = useNotification();
  const { authInfo } = useAuth();
  const { isLoggedIn } = authInfo;

  useEffect(() => {
    const fetchAttemptHistory = async () => {
      const { data, error } = await getAttemptHistory(problemId);
      if (error) return updateNotification('error', JSON.stringify(error));
      setAttempts([...data]);
    };
    if (isLoggedIn) fetchAttemptHistory();
  }, [isLoggedIn, problemId, updateNotification]);

  if (!isLoggedIn)
    return (
      <div className="flex items-center gap-1">
        <a href="/login" className="text-blue-500 hover:underline">
          log in
        </a>
        <span>or</span>
        <a href="/signup" className="text-blue-500 hover:underline">
          sign up
        </a>
        <span>to view your attempt history</span>
      </div>
    );

  return (
    <>
      <table className="w-full table-auto border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className={tdStyles}>Status</th>
            <th className={tdStyles}>Score</th>
            <th className={tdStyles}>Time Taken (s)</th>
            <th className={tdStyles}>Hints Used</th>
            <th className={tdStyles}>Submission Date</th>
          </tr>
        </thead>
        <tbody>
          {attempts.map(
            (
              { submission_date, score, time_taken, status, hints_used },
              index
            ) => (
              <tr key={index}>
                <td
                  className={`${tdStyles} font-semibold 
                    ${
                      status === 'Completed' ? 'text-green-500' : 'text-red-500'
                    }`}
                >
                  {status}
                </td>
                <td className={tdStyles}>{Math.round(score)}</td>
                <td className={tdStyles}>{time_taken}</td>
                <td className={tdStyles}>{hints_used}</td>
                <td className={`${tdStyles} text-sm text-slate-800`}>
                  {new Date(submission_date).toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false,
                  })}
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </>
  );
}
