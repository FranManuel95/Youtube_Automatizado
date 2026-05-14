"use client"

import { useEffect, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"

const links = [
  { label: "Product", href: "#" },
  { label: "Features", href: "#features" },
  { label: "Pricing", href: "#pricing" },
  { label: "Docs", href: "#" },
]

export function Navbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <motion.header
      initial={{ opacity: 0, y: -16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.21, 0.47, 0.32, 0.98] }}
      className="fixed top-0 left-0 right-0 z-50 flex justify-center px-6 pt-4"
    >
      <div
        className={cn(
          "flex w-full max-w-5xl items-center justify-between rounded-2xl px-5 py-3 transition-all duration-500",
          scrolled
            ? "border border-white/[0.07] bg-[#060608]/80 backdrop-blur-xl shadow-[0_8px_32px_rgba(0,0,0,0.4)]"
            : "border border-transparent bg-transparent"
        )}
      >
        {/* Logo */}
        <a href="/" className="flex items-center gap-2">
          <div className="h-6 w-6 rounded-md bg-gradient-to-br from-violet-500 to-indigo-600" />
          <span className="text-sm font-semibold text-white/90">Studio</span>
        </a>

        {/* Nav links */}
        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="rounded-lg px-3.5 py-1.5 text-sm text-white/50 transition-colors hover:bg-white/5 hover:text-white/80"
            >
              {link.label}
            </a>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button className="hidden rounded-lg px-4 py-1.5 text-sm text-white/50 transition-colors hover:text-white/80 md:block">
            Sign in
          </button>
          <button className="rounded-full bg-violet-600 px-4 py-1.5 text-sm font-medium text-white transition-all duration-300 hover:bg-violet-500 hover:shadow-[0_0_20px_rgba(124,58,237,0.4)]">
            Get started
          </button>
        </div>
      </div>
    </motion.header>
  )
}
