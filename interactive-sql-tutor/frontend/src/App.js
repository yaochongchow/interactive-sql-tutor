import './App.css';
import { Route, Routes } from 'react-router-dom';
import { Dashboard, Login, Signup, NotFound, Problem, Inbox, Profile, Problems, AddProblem, Analytics } from './pages'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/problems" element={<Problems />} />
      <Route path="/problems/:problemId" element={<Problem />} />
      <Route path='/add-problem' element={<AddProblem />} />
      <Route path='/analytics' element={<Analytics />} />
      <Route path="/inbox" element={<Inbox />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
