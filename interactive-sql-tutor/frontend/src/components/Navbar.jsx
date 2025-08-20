import { useRef, useState } from 'react';
import { FaRegCircleUser } from 'react-icons/fa6';
import { Link, useNavigate } from 'react-router-dom';
import {
  IoTimerOutline,
  IoPauseCircleOutline,
  IoPlayCircleOutline,
} from 'react-icons/io5';
import { FaSpinner } from 'react-icons/fa6';
import { useAuth, useNotification } from '../utils/hooks';
import { submitProblemAttempt } from '../api/problem';

const buttonSelected = 'text-white py-3 font-semibold border-b-2 border-white';
const buttonUnselected = 'py-3 text-slate-200 hover:text-white transition border-b-2 border-blue-500';

export default function Navbar({
  isProblem,
  problemId,
  solution,
  selected = -1,
  hintsStep = 0,
}) {
  const [timerOn, setTimerOn] = useState(false);
  const [paused, setPaused] = useState(false);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const intervalId = useRef(null);
  const { authInfo } = useAuth();
  const { isLoggedIn } = authInfo;
  const { updateNotification } = useNotification();
  const navigate = useNavigate();

  const handleStartTimer = () => {
    setTimerOn(true);
    intervalId.current = setInterval(() => {
      setTimeElapsed((prev) => prev + 1);
    }, 1000);
  };

  const handlePauseTimer = () => {
    clearInterval(intervalId.current);
    setPaused(true);
  };

  const handleContinueTimer = () => {
    setPaused(false);
    intervalId.current = setInterval(() => {
      setTimeElapsed((prev) => prev + 1);
    }, 1000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isLoggedIn) {
      updateNotification('warning', 'You are not logged in!');
      navigate('/login');
      return;
    }
    handlePauseTimer();
    setSubmitLoading(true);
    const { data, error } = await submitProblemAttempt(
      problemId,
      solution,
      hintsStep,
      timeElapsed
    );
    setSubmitLoading(false);
    if (error) return updateNotification('error', JSON.stringify(error));
    const { result, feedback } = data;
    if (result === 'wrong') {
      updateNotification('error', feedback);
    } else {
      updateNotification('success', 'You have passed this problem!');
    }
  };

  const hours = Math.floor(timeElapsed / 3600);
  const minutes = Math.floor((timeElapsed % 3600) / 60);
  const seconds = timeElapsed % 60;

  return (
    <form className="bg-blue-500" onSubmit={handleSubmit}>
      <div className="flex justify-between px-4">
        <div className="flex items-center space-x-10">
          <Link to={'/'}>
            <button
              type="button"
              className={selected === 0 ? buttonSelected : buttonUnselected}
            >
              Dashboard
            </button>
          </Link>
          <Link to="/problems">
            <button
              type="button"
              className={selected === 1 ? buttonSelected : buttonUnselected}
            >
              Problems
            </button>
          </Link>
          <Link to={isLoggedIn ? '/inbox' : '/login'}>
            <button
              type="button"
              className={selected === 2 ? buttonSelected : buttonUnselected}
            >
              Inbox
            </button>
          </Link>
        </div>
        {isProblem && (
          <div className="flex items-center space-x-10 text-slate-200">
            {!timerOn ? (
              <NavbarButton type="button" onClick={handleStartTimer}>
                <IoTimerOutline title="Start timer" size={24} />
              </NavbarButton>
            ) : !paused ? (
              <NavbarButton type="button" onClick={handlePauseTimer}>
                <IoPauseCircleOutline title="Pause" size={24} />
              </NavbarButton>
            ) : (
              <NavbarButton type="button" onClick={handleContinueTimer}>
                <IoPlayCircleOutline title="Continue" size={24} />
              </NavbarButton>
            )}
            <span>{`${hours.toString().padStart(2, '0')}:${minutes
              .toString()
              .padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`}</span>
            <div className="w-40">
              {submitLoading ? (
                <FaSpinner className="animate-spin" size={24} />
              ) : (
                <NavbarButton type="submit">Submit</NavbarButton>
              )}
            </div>
          </div>
        )}
        <Link to={isLoggedIn ? '/profile' : '/login'}>
          <button
            type="button"
            className={selected === 3 ? buttonSelected : buttonUnselected}
          >
            <FaRegCircleUser size={24} />
          </button>
        </Link>
      </div>
    </form>
  );
}

const NavbarButton = ({ children, type, onClick }) => {
  return (
    <button
      type={type}
      className="text-white rounded px-3 bg-blue-400 hover:text-green-200 transition"
      onClick={onClick}
    >
      {children}
    </button>
  );
};
