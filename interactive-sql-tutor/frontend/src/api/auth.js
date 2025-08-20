import { getHeaders } from '../utils/helpers';
import client from './client';

export const createUser = async (name, email, password, verify_password) => {
  try {
    const { data } = await client.post('/auth/register/', {
      name,
      email,
      password,
      verify_password,
    });
    return { data };
  } catch (error) {
    const { response } = error;
    if (response?.data) return { error: response.data };
    return { error: error.message || error };
  }
};

export const signInUser = async (email, password) => {
  try {
    const { data } = await client.post('/auth/login/', { email, password });
    return { data };
  } catch (error) {
    const { response } = error;
    if (response?.data) return { error: response.data };
    return { error: error.message || error };
  }
};

export const logOutUser = async (refresh) => {
  try {
    const { data } = await client.post('/logout/', { refresh });
    return { data };
  } catch (error) {
    const { response } = error;
    if (response?.data) return { error: response.data };
    return { error: error.message || error };
  }
};

export const updateUser = async (
  name,
  profile_info,
  password,
  verify_password
) => {
  try {
    const { data } = await client.put(
      '/auth/update/',
      { name, profile_info, password, verify_password },
      {
        headers: getHeaders(),
      }
    );
    return { data };
  } catch (error) {
    const { response } = error;
    if (response?.data) return { error: response.data };
    return { error: error.message || error };
  }
};
