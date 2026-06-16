"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Spinner from "@/components/Spinner";

export default function Favorites() {
  const router = useRouter();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetch("http://localhost:8000/favorites/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setFavorites(data);
        setLoading(false);
      });
  }, []);

  async function handleDelete(id) {
    const token = localStorage.getItem("token");
    await fetch(`http://localhost:8000/favorites/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    setFavorites(favorites.filter((f) => f.id !== id));
  }

  return (
    <main className="min-h-screen bg-[#0a0f1c] text-white">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 pt-12">
        <h2 className="text-3xl font-black mb-8">
          My <span className="text-[#f4a10a]">Favorites</span>
        </h2>

        {loading && <Spinner />}

        {!loading && favorites.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-lg">No favorites saved yet.</p>
            <Link href="/dashboard" className="text-[#f4a10a] hover:underline text-sm mt-2 block">
              Go ask something →
            </Link>
          </div>
        )}

        <div className="flex flex-col gap-4">
          {favorites.map((item) => (
            <div
              key={item.id}
              className="bg-[#111827] border border-gray-800 rounded-xl p-5"
            >
              <div className="flex items-start justify-between mb-2">
                <p className="text-white font-medium">{item.query}</p>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-red-500 hover:text-red-400 text-xs ml-4 shrink-0"
                >
                  Remove
                </button>
              </div>
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