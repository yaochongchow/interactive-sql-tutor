import { createContext, useState } from 'react';
import { signInUser } from '../api/auth';
import { useNotification } from '../utils/hooks';

export const AuthContext = createContext();

const defaultAuthInfo = {
  profile: {},
  isLoggedIn: false,
  isPending: false,
  error: '',
};

export default function AuthProvider({ children }) {
  const [authInfo, setAuthInfo] = useState({ ...defaultAuthInfo });
  const { updateNotification } = useNotification();

  const handleLogin = async (email, password) => {
    setAuthInfo({ ...authInfo, isPending: true });
    const { error, data } = await signInUser(email, password);

    if (error) {
      updateNotification('error', JSON.stringify(error));
      return setAuthInfo({ ...authInfo, isPending: false, error });
    }

    setAuthInfo({
      ...authInfo,
      profile: { ...data },
      isLoggedIn: true,
      isPending: false,
      error: '',
    });

    const { access, refresh } = data;
    localStorage.setItem('access-token', access);
    localStorage.setItem('refresh-token', refresh);
  };

  const handleLogout = async () => {
    setAuthInfo({ ...defaultAuthInfo });
  };

  const handleProfileUpdate = (name, password, profile_info) => {
    const { profile } = authInfo;
    profile.name = name;
    profile.password = password;
    profile.profile_info = profile_info;
    setAuthInfo({ ...authInfo, profile });
  };

  const isAuth = async () => {
    const token = localStorage.getItem('access-token');
    if (!token) return;
  };

  return (
    <AuthContext.Provider
      value={{
        authInfo,
        handleLogin,
        handleLogout,
        handleProfileUpdate,
        isAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
