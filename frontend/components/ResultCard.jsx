export default function ResultCard({ result, query }) {
  if (!result) return null;

  function renderResult() {
    const entries = Object.entries(result);

    return entries.map(([key, value]) => {
      const label = key
        .replace(/_/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());

      if (typeof value === "object" && value !== null) {
        return (
          <div key={key} className="flex flex-col gap-1">
            <p className="text-gray-400 text-sm">{label}</p>
            <p className="text-[#f4a10a] text-3xl font-black">
              {Object.entries(value)
                .map(([k, v]) => `${k}: ${v}`)
                .join("  |  ")}
            </p>
          </div>
        );
      }

      return (
        <div key={key} className="flex flex-col gap-1">
          <p className="text-gray-400 text-sm">{label}</p>
          <p className="text-[#f4a10a] text-4xl font-black">
            {typeof value === "number" ? value.toLocaleString() : value}
          </p>
        </div>
      );
    });
  }

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-xl p-6">
      <p className="text-gray-500 text-xs mb-4 italic">"{query}"</p>
      <div className="flex flex-col gap-4">{renderResult()}</div>
    </div>
  );
}