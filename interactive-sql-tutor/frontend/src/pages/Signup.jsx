import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FormContainer } from '../components';
import { useAuth, useNotification } from '../utils/hooks';
import { validateUser } from '../utils/helpers';
import { createUser } from '../api/auth';

const inputStyle = 'w-96 px-3 py-1 outline outline-1 outline-gray-300 rounded';

export default function Signup() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmedPassword, setConfirmedPassword] = useState('');
  const { authInfo, handleLogin } = useAuth();
  const { isLoggedIn } = authInfo;
  const navigate = useNavigate();
  const { updateNotification } = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { ok, error } = validateUser(
      username,
      email,
      password,
      confirmedPassword
    );
    if (!ok) return updateNotification('error', error);
    const { error: err, data } = await createUser(
      username,
      email,
      password,
      confirmedPassword
    );

    if (err) return updateNotification('error', JSON.stringify(err));
    updateNotification('success', 'Signup success');
    await handleLogin(email, password);
    navigate('/', { state: { data }, replace: true });
  };

  useEffect(() => {
    if (isLoggedIn) navigate('/');
  }, [isLoggedIn, navigate]);

  return (
    <FormContainer onSubmit={handleSubmit}>
      <input
        required
        className={inputStyle}
        type="text"
        placeholder="Name"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        required
        className={inputStyle}
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        required
        className={inputStyle}
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        required
        className={inputStyle}
        type="password"
        placeholder="Confirm Password"
        value={confirmedPassword}
        onChange={(e) => setConfirmedPassword(e.target.value)}
      />
      <button
        type="submit"
        className="text-white bg-slate-600 hover:bg-slate-500 transition rounded w-full py-1"
      >
        Sign Up
      </button>
      <div className="flex w-full justify-center items-center gap-1 text-sm">
        <span className="text-slate-400">Have an account?</span>
        <Link to="/login">
          <button className="text-slate-600 hover:text-slate-800 transition">
            Sign In
          </button>
        </Link>
      </div>
    </FormContainer>
  );
}
