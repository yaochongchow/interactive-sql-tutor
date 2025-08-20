import { Link } from 'react-router-dom';
import Card from './Card';

export default function InstructorDashboard() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Welcome back, Instructor!</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <h2 className="text-lg font-semibold mb-1">
            ➕ Upload a New Problem
          </h2>
          <p className="text-sm text-gray-600 mb-3">
            Create and submit new SQL problems for students to solve.
          </p>
          <Link
            to="/add-problem"
            className="inline-block text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded transition"
          >
            Go to Problem Upload
          </Link>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold mb-1">
            📊 View Student Analytics
          </h2>
          <p className="text-sm text-gray-600 mb-3">
            Track student progress, performance, and activity insights.
          </p>
          <Link
            to="/analytics"
            className="inline-block text-white bg-green-600 hover:bg-green-700 px-4 py-2 rounded transition"
          >
            View Analytics
          </Link>
        </Card>
      </div>
    </div>
  );
}
