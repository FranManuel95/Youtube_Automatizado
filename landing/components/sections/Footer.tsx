import { FadeIn } from "@/components/animations/FadeIn"

const footerLinks = {
  Product: ["Features", "Pricing", "Changelog", "Roadmap"],
  Company: ["About", "Blog", "Careers", "Press"],
  Resources: ["Docs", "Templates", "Integrations", "Community"],
  Legal: ["Privacy", "Terms", "Security", "Cookies"],
}

export function Footer() {
  return (
    <footer className="relative border-t border-white/[0.05] px-6 pt-20 pb-10">
      <div className="mx-auto max-w-6xl">
        <FadeIn>
          <div className="mb-16 grid gap-12 sm:grid-cols-2 lg:grid-cols-5">
            {/* Brand */}
            <div className="lg:col-span-1">
              <div className="mb-4 flex items-center gap-2">
                <div className="h-6 w-6 rounded-md bg-gradient-to-br from-violet-500 to-indigo-600" />
                <span className="text-sm font-semibold text-white/90">Studio</span>
              </div>
              <p className="text-sm leading-relaxed text-white/35">
                Premium landing pages, powered by AI and built for the future.
              </p>
            </div>

            {/* Links */}
            {Object.entries(footerLinks).map(([category, items]) => (
              <div key={category}>
                <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-white/30">
                  {category}
                </p>
                <ul className="space-y-3">
                  {items.map((item) => (
                    <li key={item}>
                      <a
                        href="#"
                        className="text-sm text-white/40 transition-colors hover:text-white/70"
                      >
                        {item}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Bottom bar */}
          <div className="flex flex-col items-center justify-between gap-4 border-t border-white/[0.05] pt-8 sm:flex-row">
            <p className="text-xs text-white/25">
              © 2026 Studio. All rights reserved.
            </p>
            <p className="text-xs text-white/20">
              Built with Next.js · Deployed on Vercel
            </p>
          </div>
        </FadeIn>
      </div>
    </footer>
  )
}
