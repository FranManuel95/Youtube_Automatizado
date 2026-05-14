"use client"

import { motion } from "framer-motion"
import { ArrowRight } from "lucide-react"
import { FadeIn } from "@/components/animations/FadeIn"

export function CTA() {
  return (
    <section className="relative py-32 px-6">
      <div className="mx-auto max-w-4xl">
        <FadeIn>
          <div className="relative overflow-hidden rounded-3xl border border-white/[0.07] bg-gradient-to-br from-violet-950/60 via-slate-950/80 to-indigo-950/40 p-12 text-center sm:p-20">
            {/* Inner glow */}
            <div className="pointer-events-none absolute inset-0">
              <div className="absolute left-1/2 top-0 h-px w-2/3 -translate-x-1/2 bg-gradient-to-r from-transparent via-violet-400/40 to-transparent" />
              <div className="absolute left-1/2 -top-px h-40 w-80 -translate-x-1/2 rounded-full bg-violet-600/15 blur-[60px]" />
            </div>

            {/* Grid lines decoration */}
            <div
              className="pointer-events-none absolute inset-0 opacity-[0.03]"
              style={{
                backgroundImage: `linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)`,
                backgroundSize: "64px 64px",
              }}
            />

            <div className="relative">
              <motion.div
                className="mb-3 inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-500/10 px-4 py-1.5 text-xs font-medium text-violet-300"
                animate={{ y: [0, -4, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              >
                <span className="h-1 w-1 rounded-full bg-violet-400 animate-pulse" />
                Start building today — free forever
              </motion.div>

              <h2 className="mb-5 text-4xl font-bold tracking-tight text-white sm:text-5xl">
                Ready to build something
                <br />
                <span className="gradient-text-purple">extraordinary?</span>
              </h2>

              <p className="mx-auto mb-10 max-w-lg text-white/40 leading-relaxed">
                Join thousands of teams shipping premium landing pages with AI.
                No design skills required — just your vision.
              </p>

              <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
                <button className="group inline-flex items-center gap-2 rounded-full bg-white px-8 py-3.5 text-sm font-semibold text-slate-900 transition-all duration-300 hover:bg-white/90 hover:shadow-[0_0_40px_rgba(255,255,255,0.2)]">
                  Get started free
                  <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
                </button>
                <button className="text-sm text-white/40 transition-colors hover:text-white/70">
                  Talk to sales →
                </button>
              </div>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  )
}
