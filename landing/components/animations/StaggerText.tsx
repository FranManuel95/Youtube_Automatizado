"use client"

import { motion, useInView } from "framer-motion"
import { useRef } from "react"

interface StaggerTextProps {
  text: string
  className?: string
  delay?: number
  stagger?: number
  as?: "h1" | "h2" | "h3" | "p" | "span"
}

export function StaggerText({
  text,
  className,
  delay = 0,
  stagger = 0.04,
  as: Tag = "h1",
}: StaggerTextProps) {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: "-60px" })

  const words = text.split(" ")

  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: delay,
        staggerChildren: stagger,
      },
    },
  }

  const wordVariant = {
    hidden: { opacity: 0, y: 24, filter: "blur(8px)" },
    visible: {
      opacity: 1,
      y: 0,
      filter: "blur(0px)",
      transition: { duration: 0.6, ease: "easeOut" as const },
    },
  }

  return (
    <motion.div
      ref={ref}
      variants={container}
      initial="hidden"
      animate={inView ? "visible" : "hidden"}
      className={className}
      style={{ display: "block" }}
    >
      <Tag style={{ display: "inline" }}>
        {words.map((word, i) => (
          <motion.span
            key={i}
            variants={wordVariant}
            style={{ display: "inline-block", marginRight: "0.25em" }}
          >
            {word}
          </motion.span>
        ))}
      </Tag>
    </motion.div>
  )
}
