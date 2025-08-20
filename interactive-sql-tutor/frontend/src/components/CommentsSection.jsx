import mockComments from '../data/comments';
import { useState } from 'react';

export default function CommentsSection({ problemId }) {
  const [comments, setComments] = useState(
    mockComments[problemId] ? [...mockComments[problemId]] : []
  );
  const [newComment, setNewComment] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    const newEntry = {
      id: comments.length + 1,
      userId: 0,
      content: newComment.trim(),
      timestamp: new Date().toISOString().slice(0, 19).replace('T', ' '),
    };

    setComments([...comments, newEntry]);
    setNewComment('');
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          className="w-full border rounded px-2 py-1"
          rows={2}
          placeholder="Add a comment..."
        />
        <button
          type="submit"
          className="mt-1 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          Post
        </button>
      </form>

      <ul className="space-y-1">
        {comments.map((comment) => (
          <li key={comment.id} className="border-t pt-1 flex flex-col gap-1">
            <div className="font-semibold text-gray-800">
              User {comment.userId}
            </div>
            <div>{comment.content}</div>
            <div className="text-xs text-gray-500">{comment.timestamp}</div>
          </li>
        ))}
      </ul>
    </>
  );
}
