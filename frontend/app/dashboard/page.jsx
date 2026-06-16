"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Spinner from "@/components/Spinner";
import ResultCard from "@/components/ResultCard";
import Navbar from "@/components/Navbar";

export default function Dashboard() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, []);

  async function handleAsk(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(
        `http://localhost:8000/ask?q=${encodeURIComponent(query)}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Something went wrong");
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Could not connect to server");
    } finally {
      setLoading(false);
    }
  }

  async function handleFavorite() {
    const token = localStorage.getItem("token");
    try {
      await fetch("http://localhost:8000/favorites/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ query, result, label: query }),
      });
      alert("Added to favorites!");
    } catch (err) {
      alert("Could not save favorite");
    }
  }

  return (
    <main className="min-h-screen bg-[#0a0f1c] text-white">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 pt-20">
        <h2 className="text-4xl font-black text-center mb-2">
          Ask a <span className="text-[#f4a10a]">cricket</span> question
        </h2>
        <p className="text-center text-gray-400 mb-10 text-sm">
          Powered by Cricksheets IPL data from 2008 to 2026
        </p>

        <form onSubmit={handleAsk} className="flex gap-3 mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="How many runs did Rohit score in 2023?"
            required
            className="flex-1 bg-[#111827] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#f4a10a] transition"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-[#f4a10a] text-black font-bold px-6 py-3 rounded-lg hover:bg-[#e09200] transition disabled:opacity-50 min-w-[80px] flex items-center justify-center"
          >
            {loading ? <Spinner /> : "Ask"}
          </button>
        </form>

        {error && (
          <div className="p-4 bg-red-900/30 border border-red-700 rounded-lg text-red-400 text-sm mb-4">
            {error}
          </div>
        )}

        {result && (
          <div className="bg-[#111827] border border-gray-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <p className="text-gray-400 text-sm">Result</p>
              <button
                onClick={handleFavorite}
                className="text-xs text-[#f4a10a] border border-[#f4a10a] px-3 py-1 rounded-full hover:bg-[#f4a10a] hover:text-black transition"
              >
                ★ Save to Favorites
              </button>
            </div>
            <ResultCard result={result} query={query} />
          </div>
        )}
      </div>
    </main>
  );
}