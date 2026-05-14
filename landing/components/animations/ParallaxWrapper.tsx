"use client"

import { useRef } from "react"
import { motion, useScroll, useTransform } from "framer-motion"
import { cn } from "@/lib/utils"

interface ParallaxWrapperProps {
  children: React.ReactNode
  className?: string
  speed?: number
}

export function ParallaxWrapper({
  children,
  className,
  speed = 0.3,
}: ParallaxWrapperProps) {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  })

  const y = useTransform(scrollYProgress, [0, 1], [`${speed * -100}px`, `${speed * 100}px`])

  return (
    <div ref={ref} className={cn("overflow-hidden", className)}>
      <motion.div style={{ y }}>{children}</motion.div>
    </div>
  )
}
