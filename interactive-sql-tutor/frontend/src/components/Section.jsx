export default function Section({ children, className }) {
  return (
    <div
      className={
        className +
        ' flex flex-col gap-4 my-2 p-5 rounded bg-white overflow-y-auto h-[calc(100vh-4rem)]'
      }
    >
      {children}
    </div>
  );
}
