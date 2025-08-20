import { useState } from 'react';

const buttonStyles = 'px-4 py-2 rounded transition';

export default function MessageModal({ onClose }) {
  const [recipientEmail, setRecipientEmail] = useState('');
  const [content, setContent] = useState('');

  const handleSendMessage = async (e) => {
    e.preventDefault();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-[30rem]">
        <h3 className="text-lg font-semibold mb-4">Send a Message</h3>
        <form onSubmit={handleSendMessage} className="space-y-3">
          <input
            type="text"
            required
            placeholder="Recipient"
            value={recipientEmail}
            onChange={(e) => setRecipientEmail(e.target.value)}
            className="w-full p-2 border rounded"
          />
          <textarea
            required
            placeholder="Your message"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full p-2 border rounded h-32"
          />
          <div className="flex justify-between items-center">
            <button
              type="submit"
              className={
                buttonStyles + ' text-white bg-blue-500 hover:bg-blue-600'
              }
            >
              Send
            </button>
            <button
              type="button"
              onClick={onClose}
              className={buttonStyles + ' text-red-500 hover:bg-slate-100'}
            >
              Close
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
