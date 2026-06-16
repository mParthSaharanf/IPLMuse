import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0f1c] text-white flex flex-col items-center justify-center px-4">
      
      {/* Logo / Title */}
      <div className="mb-6 text-center">
        <h1 className="text-6xl font-black tracking-tight text-white">
          IPL <span className="text-[#f4a10a]">Muse</span>
        </h1>
        <p className="mt-3 text-gray-400 text-lg">
          Ask anything about IPL stats. Get answers instantly.
        </p>
      </div>

      {/* Example queries */}
      <div className="mb-10 flex flex-col items-center gap-2 text-sm text-gray-500">
        <span>"How many runs did Kohli score in 2016?"</span>
        <span>"What is Bumrah's economy rate?"</span>
        <span>"How many sixes has Rohit hit?"</span>
      </div>

      {/* CTA Buttons */}
      <div className="flex gap-4">
        <Link
          href="/register"
          className="bg-[#f4a10a] text-black font-bold px-8 py-3 rounded-lg hover:bg-[#e09200] transition"
        >
          Get Started
        </Link>
        <Link
          href="/login"
          className="border border-gray-600 text-white font-bold px-8 py-3 rounded-lg hover:border-[#f4a10a] hover:text-[#f4a10a] transition"
        >
          Login
        </Link>
      </div>

      {/* Footer */}
      <p className="absolute bottom-6 text-gray-600 text-xs">
        Built with FastAPI + Next.js
      </p>
    </main>
  );
}