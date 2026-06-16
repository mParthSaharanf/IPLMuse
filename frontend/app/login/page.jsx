"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Login() {
  const router = useRouter();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username: form.username,
          password: form.password,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Login failed");
      } else {
        localStorage.setItem("token", data.access_token);
        router.push("/dashboard");
      }
    } catch (err) {
      setError("Could not connect to server");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#0a0f1c] text-white flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-[#111827] p-8 rounded-xl border border-gray-800">
        <h2 className="text-3xl font-black mb-1">
          IPL <span className="text-[#f4a10a]">Muse</span>
        </h2>
        <p className="text-gray-400 mb-8 text-sm">Welcome back</p>

        {error && (
          <div className="mb-4 p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-400 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="text-sm text-gray-400 mb-1 block">Username</label>
            <input
              name="username"
              type="text"
              value={form.username}
              onChange={handleChange}
              required
              className="w-full bg-[#1a2235] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#f4a10a] transition"
              placeholder="virat18"
            />
          </div>
          <div>
            <label className="text-sm text-gray-400 mb-1 block">Password</label>
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              required
              className="w-full bg-[#1a2235] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#f4a10a] transition"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="mt-2 bg-[#f4a10a] text-black font-bold py-3 rounded-lg hover:bg-[#e09200] transition disabled:opacity-50"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500">
          Don't have an account?{" "}
          <Link href="/register" className="text-[#f4a10a] hover:underline">
            Register
          </Link>
        </p>
      </div>
    </main>
  );
}