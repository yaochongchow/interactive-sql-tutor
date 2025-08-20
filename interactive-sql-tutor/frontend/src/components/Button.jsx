import { FaSpinner } from 'react-icons/fa6';

export default function Button({
  className,
  text,
  disabled,
  pending,
  onClick,
}) {
  return (
    <button
      disabled={disabled}
      onClick={onClick}
      className={`${className} w-fit min-w-32 flex justify-center items-center text-white rounded disabled:opacity-50 transition px-4 py-1`}
    >
      {pending ? (
        <FaSpinner className="animate-spin" size={24} />
      ) : (
        <span>{text}</span>
      )}
    </button>
  );
}
