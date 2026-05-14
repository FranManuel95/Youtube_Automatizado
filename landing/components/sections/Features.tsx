"use client"

import { motion, useInView } from "framer-motion"
import { useRef } from "react"
import { Zap, Layers, Sparkles, Shield, Globe, Code2 } from "lucide-react"
import { FadeIn } from "@/components/animations/FadeIn"

const features = [
  {
    icon: Sparkles,
    title: "AI-Powered Design",
    description: "Generate stunning visuals and layouts in seconds with state-of-the-art AI models.",
  },
  {
    icon: Zap,
    title: "Cinematic Motion",
    description: "GSAP + Framer Motion animations that make every scroll feel like a movie scene.",
  },
  {
    icon: Layers,
    title: "Modular Components",
    description: "Reusable, composable sections. Build entire landing pages like stacking Lego.",
  },
  {
    icon: Globe,
    title: "Global Performance",
    description: "Deployed on Vercel's edge network. Sub-100ms TTFB anywhere in the world.",
  },
  {
    icon: Shield,
    title: "Production Ready",
    description: "TypeScript, a11y-first, SEO optimized, and Lighthouse 100 out of the box.",
  },
  {
    icon: Code2,
    title: "Clean Architecture",
    description: "Next.js App Router, server components, and a clear opinionated file structure.",
  },
]

function FeatureCard({ feature, index }: { feature: typeof features[0]; index: number }) {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: "-60px" })
  const Icon = feature.icon

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 32 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: index * 0.08, ease: [0.21, 0.47, 0.32, 0.98] }}
      className="group relative rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6 transition-all duration-500 hover:border-violet-500/20 hover:bg-white/[0.04]"
    >
      {/* Hover glow */}
      <div className="absolute inset-0 rounded-2xl bg-violet-600/0 transition-all duration-500 group-hover:bg-violet-600/[0.03]" />

      <div className="relative">
        <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl border border-violet-500/20 bg-violet-500/10">
          <Icon className="h-5 w-5 text-violet-400" />
        </div>
        <h3 className="mb-2 text-base font-semibold text-white/90">{feature.title}</h3>
        <p className="text-sm leading-relaxed text-white/40">{feature.description}</p>
      </div>
    </motion.div>
  )
}

export function Features() {
  return (
    <section className="relative py-32 px-6">
      {/* Section ambient */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute left-1/2 top-1/2 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-violet-600/5 blur-[100px]" />
      </div>

      <div className="relative mx-auto max-w-6xl">
        {/* Header */}
        <FadeIn className="mb-16 text-center">
          <p className="mb-4 text-sm font-medium uppercase tracking-widest text-violet-400/80">
            Why this stack
          </p>
          <h2 className="mb-5 text-4xl font-bold tracking-tight text-white/90 sm:text-5xl">
            Built for speed.
            <span className="gradient-text-purple"> Designed to impress.</span>
          </h2>
          <p className="mx-auto max-w-xl text-base text-white/40 leading-relaxed">
            Every decision in this stack was made to maximize visual impact
            while keeping performance at the top of every chart.
          </p>
        </FadeIn>

        {/* Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, i) => (
            <FeatureCard key={feature.title} feature={feature} index={i} />
          ))}
        </div>
      </div>
    </section>
  )
}
