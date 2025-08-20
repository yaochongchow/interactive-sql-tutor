import { MdNavigateBefore, MdNavigateNext } from 'react-icons/md';

const navButtonStyles =
  'text-slate-700 hover:bg-slate-100 disabled:text-slate-400 px-1 rounded transition';

export default function TabBar({
  tabs,
  activeTab,
  setActiveTab,
  prevDisabled,
  nextDiasbled,
  onPrev,
  onNext,
}) {
  return (
    <div className="flex justify-between border-b border-slate-300 mb-2">
      <div className="flex gap-4">
        {tabs.map((tab, index) => (
          <button
            key={tab}
            onClick={() => setActiveTab(index)}
            className={`px-4 pb-2 text-sm font-medium transition ${
              activeTab === index
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="flex gap-3">
        <button
          title="Prev Question"
          className={navButtonStyles}
          disabled={prevDisabled}
          onClick={onPrev}
        >
          <MdNavigateBefore size={24} />
        </button>
        <button
          title="Next Question"
          className={navButtonStyles}
          disabled={nextDiasbled}
          onClick={onNext}
        >
          <MdNavigateNext size={24} />
        </button>
      </div>
    </div>
  );
}
