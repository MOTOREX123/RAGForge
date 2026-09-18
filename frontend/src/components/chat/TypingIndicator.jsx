export function TypingIndicator() {
  return (
    <div className="border-l-2 border-ink-dim/40 py-1 pl-4">
      <div className="flex items-center gap-1 py-2">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="h-1.5 w-1.5 animate-pulse rounded-full bg-ink-dim"
            style={{ animationDelay: `${i * 150}ms` }}
          />
        ))}
      </div>
    </div>
  );
}
