import { useEffect, useState } from 'react';
import { Navbar } from '../components';
import { useAuth, useNotification } from '../utils/hooks';
import { useNavigate } from 'react-router-dom';
import { updateUser } from '../api/auth';
import { validateUser } from '../utils/helpers';
import { FaSpinner } from 'react-icons/fa6';

const buttonStyles =
  'w-64 text-white px-3 py-1 rounded transition flex justify-center';

export default function Profile() {
  const { authInfo, handleLogout, handleProfileUpdate } = useAuth();
  const { profile, isLoggedIn } = authInfo;
  const prevProfile = {
    email: profile.email,
    name: profile.name,
    profile_info: profile.profile_info || '',
    password: '',
    verify_password: '',
  };
  const [pending, setPending] = useState(false);
  const [newProfile, setNewProfile] = useState({ ...prevProfile });
  const navigate = useNavigate();
  const { updateNotification } = useNotification();

  const { name, email, password, verify_password, profile_info } = newProfile;

  const handleProfileChange = async (e) => {
    e.preventDefault();
    const { ok, error: err } = validateUser(
      name,
      email,
      password,
      verify_password
    );
    if (!ok) return updateNotification('error', err);
    setPending(true);
    const { error } = await updateUser(
      name,
      profile_info,
      password,
      verify_password
    );
    setPending(false);
    if (error) return updateNotification('error', JSON.stringify(error));
    updateNotification('success', 'Profile updated successfully');
    handleProfileUpdate(name, password, profile_info);
  };

  const handleUserLogout = async () => {
    await handleLogout();
    updateNotification('success', 'You are now logged out');
  };

  useEffect(() => {
    if (!isLoggedIn) navigate('/login');
  }, [isLoggedIn, navigate]);

  return (
    <div className="flex flex-col w-full h-screen">
      <Navbar selected={3} />
      <div className="flex justify-center">
        <form
          className="flex flex-col gap-5 p-10 justify-center items-center"
          onSubmit={handleProfileChange}
        >
          <FormEntry label="Email" value={email} isEditable={false} />
          <FormEntry
            label="Name"
            value={name}
            onChange={(e) =>
              setNewProfile({ ...newProfile, name: e.target.value })
            }
          />
          <FormEntry
            label="Password"
            value={password}
            type="password"
            onChange={(e) =>
              setNewProfile({ ...newProfile, password: e.target.value })
            }
          />
          <FormEntry
            label="Verify Password"
            value={verify_password}
            type="password"
            onChange={(e) =>
              setNewProfile({ ...newProfile, verify_password: e.target.value })
            }
          />
          <FormEntry
            label="About Me"
            isTextarea
            value={profile_info}
            onChange={(e) =>
              setNewProfile({ ...newProfile, profile_info: e.target.value })
            }
          />

          <button
            type="submit"
            className={
              buttonStyles +
              ' bg-green-500  disabled:bg-green-300 hover:bg-green-600'
            }
            disabled={
              JSON.stringify(prevProfile) === JSON.stringify(newProfile)
            }
          >
            {!pending ? (
              <span>Submit Change</span>
            ) : (
              <FaSpinner className="animate-spin" size={24} />
            )}
          </button>
          <button
            type="button"
            className={buttonStyles + ' bg-red-500 hover:bg-red-600'}
            onClick={handleUserLogout}
          >
            Log Out
          </button>
        </form>
      </div>
    </div>
  );
}

const FormEntry = ({
  label,
  value,
  onChange,
  type = 'text',
  isEditable = true,
  isTextarea = false,
}) => {
  const commonStyles =
    'w-96 outline outline-1 outline-gray-300 px-2 py-1 rounded';
  return (
    <div className="flex gap-2 items-center text-slate-800">
      <label className="w-20" htmlFor={label}>
        {label}
      </label>
      {!isEditable ? (
        <span className="w-96">{value}</span>
      ) : !isTextarea ? (
        <input
          id={label}
          className={commonStyles}
          type={type}
          value={value}
          onChange={onChange}
        />
      ) : (
        <textarea
          id={label}
          className={commonStyles + ' h-24'}
          type={type}
          value={value}
          onChange={onChange}
        />
      )}
    </div>
  );
};
