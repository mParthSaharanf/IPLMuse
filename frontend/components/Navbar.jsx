"use client";
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();

  function handleLogout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  function navLink(href, label) {
    const isActive = pathname === href;
    return (
      <Link
        href={href}
        className={`transition text-sm ${
          isActive
            ? "text-[#f4a10a] font-semibold"
            : "text-gray-400 hover:text-[#f4a10a]"
        }`}
      >
        {label}
      </Link>
    );
  }

  return (
    <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <Link href="/dashboard">
        <h1 className="text-xl font-black cursor-pointer">
          IPL <span className="text-[#f4a10a]">Muse</span>
        </h1>
      </Link>
      <div className="flex items-center gap-6 text-sm">
        {navLink("/dashboard", "Dashboard")}
        {navLink("/history", "History")}
        {navLink("/favorites", "Favorites")}
        <button
          onClick={handleLogout}
          className="text-gray-400 hover:text-red-400 transition text-sm"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}