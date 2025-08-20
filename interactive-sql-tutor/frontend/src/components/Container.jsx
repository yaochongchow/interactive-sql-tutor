export default function Container({ children, className }) {
  return (
    <div className={'w-full px-4 py-2 text-slate-800 ' + className}>
      {children}
    </div>
  );
}
