import { getHeaders } from '../utils/helpers';
import client from './client';

export const getAllowedSchemas = async () => {
  try {
    const { data } = await client.get('/instructor/allowed-schema/', {
      headers: getHeaders(),
    });
    return { data };
  } catch (error) {
    const { response } = error;
    if (response?.data) return { error: response.data };
    return { error: error.message || error };
  }
};

export const submitSqlQuery = async (query) => {
  try {
    const { data } = await client.post(
      '/instructor/query-sql/',
      { query },
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

export const getQueryFromLLM = async (prompt) => {
  try {
    const { data } = await client.post(
      '/llm-analytics/generate/',
      { prompt },
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
