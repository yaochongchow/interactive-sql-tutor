import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, MessageModal, Navbar } from '../components';
import notifications from '../data/notifications';
import { useAuth } from '../utils/hooks';
import { trim } from '../utils/helpers';
import {
  MdMarkEmailUnread,
  MdOutlineMarkEmailRead,
  MdOutlineDeleteForever,
} from 'react-icons/md';
import { IoIosSend } from 'react-icons/io';
import { GoRead } from 'react-icons/go';

const buttonStyles =
  'flex items-center gap-2 bg-blue-500 text-white py-2 px-3 rounded hover:bg-blue-600 transition-colors';

export default function Inbox() {
  const [messages, setMessages] = useState([...notifications]);
  const [showModal, setShowModal] = useState(false);

  const { authInfo } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!authInfo.isLoggedIn) navigate('/login');
  }, [authInfo.isLoggedIn, navigate]);

  const handleMarkAllAsRead = async () => {
    setMessages(messages.map((message) => ({ ...message, is_read: true })));
  };

  const handleMarkAsRead = async (id) => {
    setMessages(
      messages.map((message) =>
        message.id === id ? { ...message, is_read: true } : message
      )
    );
  };

  const handleMarkAsUnread = async (id) => {
    setMessages(
      messages.map((message) =>
        message.id === id ? { ...message, is_read: false } : message
      )
    );
  };

  const handleDelete = async (id) => {
    setMessages(messages.filter((message) => message.id !== id));
  };

  const unread_count = messages.filter((message) => !message.is_read).length;

  return (
    <>
      <Navbar selected={2} />
      <Container className="flex flex-col gap-5">
        <div className="px-3 mt-6 flex gap-5">
          <button
            onClick={() => setShowModal((prev) => !prev)}
            className={buttonStyles}
          >
            <IoIosSend size={20} />
            Send Message
          </button>
          <button onClick={handleMarkAllAsRead} className={buttonStyles}>
            <GoRead size={20} />
            {`Mark All (${unread_count}) as Read`}
          </button>
        </div>

        {showModal && <MessageModal onClose={() => setShowModal(false)} />}

        <div>
          {messages
            .toSorted((a, b) => b.timestamp.localeCompare(a.timestamp))
            .map(({ id, content, is_read, timestamp }) => (
              <div
                key={id}
                className="flex justify-between items-center p-2 rounded border-b"
              >
                <div className="flex gap-1">
                  {!is_read ? (
                    <button
                      title="Mark as read"
                      className="px-2 hover:bg-slate-100"
                      onClick={() => handleMarkAsRead(id)}
                    >
                      <MdMarkEmailUnread size={20} />
                    </button>
                  ) : (
                    <button
                      title="Mark as unread"
                      className="px-2 hover:bg-slate-100"
                      onClick={() => handleMarkAsUnread(id)}
                    >
                      <MdOutlineMarkEmailRead size={20} />
                    </button>
                  )}
                  <div className={!is_read ? 'font-semibold' : ''}>
                    {trim(content)}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500">{timestamp}</span>
                  <button
                    title="Delete"
                    onClick={() => handleDelete(id)}
                    className="text-red-500 px-2 rounded hover:bg-slate-100 transition"
                  >
                    <MdOutlineDeleteForever size={20} />
                  </button>
                </div>
              </div>
            ))}
        </div>
      </Container>
    </>
  );
}
