import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FormContainer } from '../components';
import { useAuth, useNotification } from '../utils/hooks';
import { isValidEmail } from '../utils/helpers';

const inputStyle = 'w-96 px-3 py-1 outline outline-1 outline-gray-300 rounded';

const validateUser = (email, password) => {
  if (!email.trim()) return { ok: false, error: 'Email is missing!' };
  if (!isValidEmail(email)) return { ok: false, error: 'Invalid email!' };
  if (!password.trim()) return { ok: false, error: 'Password is missing!' };
  if (password.length < 8)
    return { ok: false, error: 'Password must be at least 8 characters!' };
  return { ok: true };
};

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { authInfo, handleLogin } = useAuth();
  const { isLoggedIn } = authInfo;
  const navigate = useNavigate();
  const { updateNotification } = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { ok, error } = validateUser(email, password);
    if (!ok) return updateNotification('error', error);
    await handleLogin(email, password);
    if (isLoggedIn) updateNotification('success', 'Login success');
  };

  useEffect(() => {
    if (isLoggedIn) navigate('/');
  }, [isLoggedIn, navigate]);

  return (
    <FormContainer onSubmit={handleSubmit}>
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
      <button
        type="submit"
        className="text-white bg-slate-600 hover:bg-slate-500 transition rounded w-full py-1"
      >
        Sign In
      </button>
      <div className="flex w-full justify-center items-center gap-1 text-sm">
        <span className="text-slate-400">Don't have an account?</span>
        <Link to="/signup">
          <button className="text-slate-600 hover:text-slate-800 transition">
            Sign Up
          </button>
        </Link>
      </div>
    </FormContainer>
  );
}
