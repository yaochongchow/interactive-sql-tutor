import { useState } from 'react';
import { useNotification } from '../utils/hooks';
import { getHint } from '../api/problem';
import { FaSpinner } from 'react-icons/fa6';
import { marked } from 'marked';

const maxHints = 3;
const buttonStyles =
  'flex justify-center items-center w-full text-white py-1 rounded disabled:opacity-50';
const dialogStyles = 'min-w-full w-fit mb-4 px-4 pt-2 bg-gray-50 rounded-md border border-gray-300';

export default function HintDialog({
  onClose,
  prompt,
  hintStep,
  setHintStep,
  hintResponses,
  setHintResponses,
  questionResponses,
  setQuestionResponses
}) {
  const [activeTab, setActiveTab] = useState('hints');
  const [questionInput, setQuestionInput] = useState('');
  const [pending, setPending] = useState(false);
  const { updateNotification } = useNotification();

  const handleFetchHint = async () => {
    if (pending) return;
    if (hintStep >= maxHints) {
      return updateNotification(
        'error',
        `You have used ${maxHints} hints already`
      );
    }
    setPending(true);
    const { data, error } = await getHint(prompt);
    setPending(false);
    if (error) return updateNotification('error', JSON.stringify(error));
    setHintResponses((prev) => [...prev, data.hint]);
    setHintStep((prev) => prev + 1);
  };

  const handleSendQuestion = async () => {
    if (pending || !questionInput.trim()) return;
    setPending(true);
    const { data, error } = await getHint(questionInput);
    setPending(false);
    if (error) return updateNotification('error', JSON.stringify(error));
    setQuestionResponses((prev) => [
      ...prev,
      `You: ${questionInput}\nAI: ${data.hint}`,
    ]);
    setQuestionInput('');
  };

  return (
    <div className="fixed bottom-4 right-4 w-[30rem] bg-white border shadow-lg rounded-lg p-4 z-50">
      {/* Tabs */}
      <div className="flex border-b text-sm mb-2">
        <button
          className={`flex-1 py-2 ${
            activeTab === 'hints'
              ? 'border-b-2 border-blue-500 font-semibold'
              : 'text-gray-500'
          }`}
          onClick={() => setActiveTab('hints')}
        >
          Hints
        </button>
        <button
          className={`flex-1 py-2 ${
            activeTab === 'questions'
              ? 'border-b-2 border-blue-500 font-semibold'
              : 'text-gray-500'
          }`}
          onClick={() => setActiveTab('questions')}
        >
          Ask a Question
        </button>
      </div>

      <div className="h-96 overflow-y-auto mb-2 text-sm whitespace-pre-line">
        {activeTab === 'hints' &&
          hintResponses.map((hint, idx) => (
            <div
              key={idx}
              className={dialogStyles}
              dangerouslySetInnerHTML={{ __html: marked(hint) }}
            />
          ))}

        {activeTab === 'questions' &&
          questionResponses.map((msg, idx) => (
            <div
              key={idx}
              className={dialogStyles}
              dangerouslySetInnerHTML={{ __html: marked(msg) }}
            />
          ))}
      </div>

      {activeTab === 'hints' ? (
        <button
          onClick={handleFetchHint}
          disabled={pending || hintStep >= maxHints}
          className={`${buttonStyles} bg-blue-500 hover:bg-blue-600`}
        >
          {pending ? (
            <FaSpinner className="animate-spin" size={24} />
          ) : hintStep < maxHints ? (
            'Next Hint'
          ) : (
            'No more hints'
          )}
        </button>
      ) : (
        <div>
          <textarea
            value={questionInput}
            onChange={(e) => setQuestionInput(e.target.value)}
            rows={2}
            className="w-full border rounded px-2 py-1 text-sm mb-1"
            placeholder="Type your question..."
            onKeyDown={async (e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                await handleSendQuestion();
              }
            }}
          />
          <button
            onClick={handleSendQuestion}
            disabled={pending || !questionInput.trim()}
            className={`${buttonStyles} bg-green-500 hover:bg-green-600`}
          >
            {pending ? (
              <FaSpinner className="animate-spin" size={24} />
            ) : (
              <span>Send</span>
            )}
          </button>
        </div>
      )}

      {/* Close Button */}
      <button
        onClick={onClose}
        className="absolute top-2 right-2 text-gray-400 hover:text-black"
      >
        &times;
      </button>
    </div>
  );
}
