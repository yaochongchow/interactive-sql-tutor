import React, { useEffect, useState } from 'react';
import { useAuth, useNotification } from '../utils/hooks';
import { Container, Navbar } from '../components';
import { FaSpinner } from 'react-icons/fa6';
import { useNavigate } from 'react-router-dom';
import { uploadProblem } from '../api/problem';

const labelStyles = 'block font-medium mb-1';
const inputStyles = 'border p-2 w-full';

export default function AddProblem() {
  const [files, setFiles] = useState({
    metadata: null,
    problem: null,
    solution: null,
  });
  const [pending, setPending] = useState(false);

  const { authInfo } = useAuth();
  const { profile, isLoggedIn } = authInfo;
  const { updateNotification } = useNotification();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      updateNotification('error', 'You are not logged in!');
      navigate('/login');
      return;
    }
    if (profile.role !== 'Instructor') {
      updateNotification('error', 'You are not authorized!');
      navigate('/');
    }
  }, [isLoggedIn, navigate, profile.role, updateNotification]);

  const handleFileChange = (e, key) => {
    const file = e.target.files[0];
    if (!file) return;
    setFiles({ ...files, [key]: file });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (pending) return;
    const formData = new FormData();
    const { metadata, problem, solution } = files;
    if (!metadata || !problem || !solution) {
      updateNotification('error', 'Please upload all 3 required files.');
      return;
    }
    formData.append('metadata_file', metadata);
    formData.append('problem_file', problem);
    formData.append('solution_file', solution);
    setPending(true);
    const { error } = await uploadProblem(formData);
    if (error) {
      updateNotification('error', JSON.stringify(error));
    } else {
      updateNotification('success', 'Problem uploaded successfully!');
    }
    setFiles({ metadata: null, problem: null, solution: null });
    setPending(false);
  };

  return (
    <>
      <Navbar />
      <Container className="flex justify-center items-start min-h-screen pt-10">
        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-6 border p-6 rounded w-full max-w-xl"
        >
          <h2 className="text-xl font-bold">Upload SQL Problem</h2>
          <div>
            <label className={labelStyles}>Metadata (JSON)</label>
            <input
              type="file"
              accept=".json"
              onChange={(e) => handleFileChange(e, 'metadata')}
              required
              className={inputStyles}
            />
          </div>

          <div>
            <label className={labelStyles}>Problem SQL</label>
            <input
              type="file"
              accept=".sql"
              onChange={(e) => handleFileChange(e, 'problem')}
              required
              className={inputStyles}
            />
          </div>

          <div>
            <label className={labelStyles}>Solution SQL</label>
            <input
              type="file"
              accept=".sql"
              onChange={(e) => handleFileChange(e, 'solution')}
              required
              className={inputStyles}
            />
          </div>

          <button
            type="submit"
            disabled={pending}
            className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 flex items-center justify-center"
          >
            {pending ? <FaSpinner className="animate-spin mr-2" /> : null}
            {pending ? 'Uploading...' : 'Upload Problem'}
          </button>
        </form>
      </Container>
    </>
  );
}
