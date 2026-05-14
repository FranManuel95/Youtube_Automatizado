import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import "./globals.css"
import { LenisProvider } from "@/components/animations/LenisProvider"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
})

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "Studio — Premium AI Landing Pages",
  description:
    "Ultra-premium landing pages with cinematic motion design, inspired by Stripe, Vercel and Linear. Built with AI.",
  openGraph: {
    title: "Studio — Premium AI Landing Pages",
    description: "Ultra-premium landing pages powered by AI.",
    type: "website",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="bg-[#060608] text-white antialiased">
        <LenisProvider>{children}</LenisProvider>
      </body>
    </html>
  )
}
