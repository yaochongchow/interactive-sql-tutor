import Navbar from './Navbar';

export default function FormContainer({ children, onSubmit }) {
  return (
    <div className="w-full h-screen flex flex-col">
      <Navbar />
      <div className="bg-slate-200 flex flex-1 justify-center items-center">
        <form
          className="flex flex-col bg-white rounded justify-center items-center gap-5 p-5 w-fit h-fit"
          onSubmit={onSubmit}
        >
          {children}
        </form>
      </div>
    </div>
  );
}
