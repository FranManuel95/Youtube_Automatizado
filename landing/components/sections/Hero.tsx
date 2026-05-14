"use client"

import { useRef } from "react"
import { motion, useScroll, useTransform } from "framer-motion"
import { ArrowRight, Play } from "lucide-react"
import { StaggerText } from "@/components/animations/StaggerText"
import { FadeIn } from "@/components/animations/FadeIn"

export function Hero() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  })

  const videoOpacity = useTransform(scrollYProgress, [0, 0.6], [1, 0])
  const videoScale = useTransform(scrollYProgress, [0, 1], [1, 1.08])
  const contentY = useTransform(scrollYProgress, [0, 1], ["0%", "20%"])

  return (
    <section
      ref={ref}
      className="relative flex min-h-screen items-center justify-center overflow-hidden"
    >
      {/* Background video */}
      <motion.div
        className="absolute inset-0 z-0"
        style={{ opacity: videoOpacity, scale: videoScale }}
      >
        <video
          autoPlay
          muted
          loop
          playsInline
          className="absolute inset-0 h-full w-full object-cover"
          poster="/assets/images-ai/hero-poster.jpg"
        >
          <source src="/assets/videos-ai/hero.webm" type="video/webm" />
          <source src="/assets/videos-ai/hero.mp4" type="video/mp4" />
        </video>

        {/* Fallback gradient when no video */}
        <div className="absolute inset-0 bg-gradient-to-br from-violet-950/80 via-slate-950 to-indigo-950/60" />
      </motion.div>

      {/* Multi-layer overlay for depth */}
      <div className="absolute inset-0 z-10">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#060608]" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#060608]/60 via-transparent to-transparent" />
        <div className="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-[#060608] to-transparent" />
      </div>

      {/* Ambient glow orbs */}
      <div className="pointer-events-none absolute inset-0 z-10 overflow-hidden">
        <motion.div
          className="absolute -left-1/4 top-1/4 h-[600px] w-[600px] rounded-full bg-violet-600/10 blur-[120px]"
          animate={{ scale: [1, 1.1, 1], opacity: [0.5, 0.8, 0.5] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute -right-1/4 top-1/3 h-[500px] w-[500px] rounded-full bg-indigo-600/8 blur-[120px]"
          animate={{ scale: [1, 1.15, 1], opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        />
      </div>

      {/* Content */}
      <motion.div
        className="relative z-20 mx-auto max-w-6xl px-6 text-center"
        style={{ y: contentY }}
      >
        {/* Badge */}
        <FadeIn delay={0.1}>
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-white/60 backdrop-blur-sm">
            <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" />
            Powered by AI — Built for the future
            <ArrowRight className="h-3.5 w-3.5" />
          </div>
        </FadeIn>

        {/* Headline */}
        <div className="mb-6">
          <StaggerText
            text="The future of premium web design"
            className="gradient-text text-5xl font-bold leading-[1.08] tracking-tight sm:text-7xl lg:text-8xl"
            as="h1"
            delay={0.2}
            stagger={0.06}
          />
        </div>

        {/* Sub-headline */}
        <FadeIn delay={0.6} duration={0.8}>
          <p className="mx-auto mb-12 max-w-2xl text-lg text-white/45 sm:text-xl leading-relaxed">
            Ultra-premium landing pages with cinematic motion design.
            Inspired by Stripe, Vercel and Linear — built with AI.
          </p>
        </FadeIn>

        {/* CTAs */}
        <FadeIn delay={0.8} duration={0.7}>
          <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <button className="group relative inline-flex items-center gap-2 overflow-hidden rounded-full bg-violet-600 px-8 py-3.5 text-sm font-medium text-white transition-all duration-300 hover:bg-violet-500 hover:shadow-[0_0_40px_rgba(124,58,237,0.5)]">
              <span className="relative z-10">Get started free</span>
              <ArrowRight className="relative z-10 h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
              <div className="absolute inset-0 bg-gradient-to-r from-violet-600 to-indigo-600 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
            </button>

            <button className="group inline-flex items-center gap-2.5 rounded-full border border-white/10 bg-white/5 px-8 py-3.5 text-sm font-medium text-white/70 backdrop-blur-sm transition-all duration-300 hover:border-white/20 hover:bg-white/10 hover:text-white">
              <div className="flex h-5 w-5 items-center justify-center rounded-full bg-white/10 transition-colors duration-300 group-hover:bg-white/20">
                <Play className="h-2.5 w-2.5 fill-current" />
              </div>
              Watch demo
            </button>
          </div>
        </FadeIn>

        {/* Social proof */}
        <FadeIn delay={1.0} duration={0.7}>
          <div className="mt-16 flex items-center justify-center gap-6 text-sm text-white/30">
            <span>Trusted by 2,000+ teams</span>
            <span className="h-px w-8 bg-white/20" />
            <span>No credit card required</span>
            <span className="h-px w-8 bg-white/20" />
            <span>Free forever plan</span>
          </div>
        </FadeIn>
      </motion.div>

      {/* Bottom scroll indicator */}
      <FadeIn
        delay={1.4}
        className="absolute bottom-10 left-1/2 z-20 -translate-x-1/2"
      >
        <motion.div
          className="flex h-10 w-6 items-start justify-center rounded-full border border-white/15 p-1.5"
          animate={{ opacity: [1, 0.4, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <motion.div
            className="h-1.5 w-1 rounded-full bg-white/50"
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          />
        </motion.div>
      </FadeIn>
    </section>
  )
}
