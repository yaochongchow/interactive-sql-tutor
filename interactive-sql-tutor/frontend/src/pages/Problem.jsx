import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Loading,
  Navbar,
  CommentsSection,
  HintDialog,
  DescriptionSection,
  TabBar,
  AttemptsSection,
  Section,
  SQLEditor,
} from '../components';
import { getSingleProblem } from '../api/problem';
import { useNotification } from '../utils/hooks';
import { debounce } from 'lodash';
import { IoBulbOutline } from 'react-icons/io5';
import { generatePromptFromProblem } from '../utils/helpers';

const tabs = ['Description', 'Comments', 'Attempts'];

export default function Problem() {
  const { problemId } = useParams();
  const [ready, setReady] = useState(false);
  const [problem, setProblem] = useState({});
  const [solution, setSolution] = useState('');
  const [showDialog, setShowDialog] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [hintStep, setHintStep] = useState(0);
  const [hintResponses, setHintResponses] = useState([]);
  const [questionResponses, setQuestionResponses] = useState([]);

  const navigate = useNavigate();
  const { updateNotification } = useNotification();

  const handleChange = (code) => {
    setSolution(code);
    debouncedSave(code);
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debouncedSave = useCallback(
    debounce((newSolution) => {
      localStorage.setItem('p' + problemId, newSolution);
    }, 500),
    [problemId]
  );

  useEffect(() => {
    return () => debouncedSave.cancel();
  }, [debouncedSave]);

  useEffect(() => {
    const prevSolution = localStorage.getItem('p' + problemId);
    if (prevSolution) setSolution(prevSolution);
  }, [problemId]);

  useEffect(() => {
    const fetchCurrentProblem = async () => {
      const { data, error } = await getSingleProblem(problemId);
      if (error) {
        updateNotification('error', JSON.stringify(error));
        navigate('/');
      }
      setReady(true);
      setProblem({ ...data });
    };
    fetchCurrentProblem();
  }, [navigate, problemId, updateNotification]);

  return (
    <div className="min-h-screen bg-slate-200 flex flex-col">
      <Navbar
        isProblem={true}
        problemId={problemId}
        solution={solution}
        hintsStep={hintStep}
      />
      <div className="flex flex-grow">
        <Section className="w-1/2 ml-2 mr-1">
          {!ready ? (
            <Loading />
          ) : (
            <>
              <TabBar
                tabs={tabs}
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                prevDisabled={parseInt(problemId) === 1}
                onPrev={() => navigate(`/problems/${parseInt(problemId) - 1}`)}
                onNext={() => navigate(`/problems/${parseInt(problemId) + 1}`)}
              />
              {activeTab === 0 && <DescriptionSection problem={problem} />}
              {activeTab === 1 && <CommentsSection problemId={problemId} />}
              {activeTab === 2 && <AttemptsSection problemId={problemId} />}
            </>
          )}
        </Section>

        <Section className="w-1/2 ml-1 mr-2">
          <SQLEditor value={solution} onValueChange={handleChange} />
          <button
            onClick={() => setShowDialog(true)}
            className="absolute bottom-4 right-4 w-12 h-12 rounded-full bg-blue-500 text-white flex items-center justify-center shadow-lg hover:bg-blue-600 transition"
          >
            <IoBulbOutline className="text-2xl" />
          </button>
        </Section>
      </div>
      {showDialog && (
        <HintDialog
          prompt={generatePromptFromProblem(problem, hintResponses, hintStep)}
          hintStep={hintStep}
          setHintStep={setHintStep}
          onClose={() => setShowDialog(false)}
          hintResponses={hintResponses}
          setHintResponses={setHintResponses}
          questionResponses={questionResponses}
          setQuestionResponses={setQuestionResponses}
        />
      )}
    </div>
  );
}
