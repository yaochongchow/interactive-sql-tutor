import { FaBookOpen, FaCheckCircle, FaTrophy } from 'react-icons/fa';
import Card from './Card';

export default function StudentDashboard() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Welcome back, Student!</h1>
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="flex items-center gap-4 p-4">
          <FaBookOpen className="text-blue-600" size={32} />
          <div>
            <h2 className="text-lg font-semibold">Problems Solved</h2>
            <p className="text-2xl font-bold">42</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4 p-4">
          <FaCheckCircle className="text-green-600" size={32} />
          <div>
            <h2 className="text-lg font-semibold">Accuracy</h2>
            <p className="text-2xl font-bold">88%</p>
          </div>
        </Card>
        <Card className="flex items-center gap-4 p-4">
          <FaTrophy className="text-yellow-500" size={32} />
          <div>
            <h2 className="text-lg font-semibold">Rank</h2>
            <p className="text-2xl font-bold">#15</p>
          </div>
        </Card>
      </div>

      {/* Progress */}
      <Card>
        <h2 className="text-xl font-semibold mb-2">Weekly Progress</h2>
        <p className="text-sm text-muted mt-2">
          65% of your weekly goal completed
        </p>
      </Card>

      {/* Upcoming Challenges */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Upcoming Challenges</h2>
        <ul className="space-y-2 text-sm">
          <li>📅 April 9 - SQL Joins Mastery Quiz</li>
          <li>📅 April 11 - Window Functions Challenge</li>
          <li>📅 April 13 - Mini Hackathon</li>
        </ul>
      </Card>
    </div>
  );
}
