import { CitationChip } from "./CitationChip";

export function CitationRow({ citations, onCitationClick }) {
  if (!citations || citations.length === 0) return null;

  return (
    <div className="mt-3 flex flex-wrap gap-1.5">
      {citations.map((citation) => (
        <CitationChip key={citation.id} citation={citation} onClick={onCitationClick} />
      ))}
    </div>
  );
}
