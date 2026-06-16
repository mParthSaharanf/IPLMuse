"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Spinner from "@/components/Spinner";


export default function History() {
  const router = useRouter();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetch("http://localhost:8000/history/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setHistory(data);
        setLoading(false);
      });
  }, []);

  return (
    <main className="min-h-screen bg-[#0a0f1c] text-white">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 pt-12">
        <h2 className="text-3xl font-black mb-8">
          Query <span className="text-[#f4a10a]">History</span>
        </h2>

        {loading && <Spinner />}

        {!loading && history.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-lg">No queries yet.</p>
            <Link href="/dashboard" className="text-[#f4a10a] hover:underline text-sm mt-2 block">
              Ask your first question →
            </Link>
          </div>
        )}

        <div className="flex flex-col gap-4">
          {history.map((item) => (
            <div
              key={item.id}
              className="bg-[#111827] border border-gray-800 rounded-xl p-5"
            >
              <p className="text-white font-medium mb-2">{item.query}</p>
              <pre className="text-[#f4a10a] text-sm font-mono">
                {JSON.stringify(item.result, null, 2)}
              </pre>
              <p className="text-gray-600 text-xs mt-3">
                {new Date(item.created_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}