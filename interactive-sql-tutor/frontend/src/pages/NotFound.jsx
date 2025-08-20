import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function NotFound() {
  return (
    <div className="w-full h-screen flex flex-col">
      <Navbar />
      <div className="bg-slate-200 flex flex-col gap-10 flex-1 justify-center items-center">
        <h1 className="text-3xl text-slate-800">
          We couldn't find the page you're requesting...
        </h1>
        <Link to="/">
          <button className="text-white bg-slate-600 hover:bg-slate-500 transition rounded px-3 py-1">
            Go to home page
          </button>
        </Link>
      </div>
    </div>
  );
}
