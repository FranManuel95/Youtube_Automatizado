# CLAUDE.md — Premium AI Landing Pages

## Project Goal

Build ultra-premium, conversion-focused landing pages with a cinematic aesthetic inspired by Stripe, Vercel, Linear, OpenAI, ElevenLabs and Perplexity. Stack must stay free and lightweight.

---

## Core Stack

| Layer | Tools |
|---|---|
| Framework | Next.js + React + TypeScript |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui, Magic UI, Aceternity UI |
| Animation | GSAP + ScrollTrigger, Framer Motion, Lenis smooth scroll |
| Hosting | Vercel (free tier) |

---

## Design Language

Always think: **"high-end startup landing page"**.

**Use:**
- Soft gradients, blur, glassmorphism
- Glow effects, subtle borders
- Premium typography (never generic fonts)
- Spacing-heavy layouts, generous whitespace
- Dark luxury or futuristic minimal aesthetics

**Never use:**
- Cluttered UI or excessive text
- Generic/template-looking layouts
- Aggressive colors or outdated patterns
- Cheesy or overexposed visuals

---

## Motion Design Rules

Motion is **extremely important** — it's one of the top 3 factors that make a site feel premium.

**Use:**
- GSAP reveal animations on scroll
- Lenis smooth scrolling (always)
- Staggered text entrance animations
- Parallax on hero sections
- Subtle hover states and opacity transitions
- Cinematic section entrances

**Never use:**
- Distracting or chaotic animations
- Slow or performance-heavy motion
- Over-animated UI elements

Motion must feel: smooth → premium → elegant → intentional.

---

## What Makes the Site Feel Premium (Priority Order)

1. Smooth scrolling
2. Motion design
3. Typography
4. Spacing
5. Cinematic visuals
6. Subtle interactions
7. Blur/glass effects
8. High-quality gradients
9. Good composition
10. Performance

---

## Performance Rules (Non-Negotiable)

- Lazy load all videos and images
- Videos: WebM preferred, MP4 fallback, under 3MB, 4–8s loops
- Keep Lighthouse score high
- Prefer server components when possible
- Minimal bundle size, avoid unnecessary dependencies

---

## Hero Section Pattern

Every hero should have:
- Cinematic AI-generated background video (or gradient fallback)
- Overlay gradients for text readability
- Strong headline + minimal supporting text
- Premium CTA
- Subtle animated elements

Video implementation:

```tsx
<video
  autoPlay
  muted
  loop
  playsInline
  className="absolute inset-0 h-full w-full object-cover"
>
  <source src="/videos/hero.webm" type="video/webm" />
  <source src="/videos/hero.mp4" type="video/mp4" />
</video>
```

Always add overlay div on top of the video for readability.

---

## File Structure

```
/app
/components
  /ui          ← shadcn + Magic UI + Aceternity components
  /sections    ← Hero, Features, Pricing, CTA, Footer...
  /animations  ← Reusable GSAP/Framer wrappers
/assets
  /images-ai   ← AI-generated images
  /videos-ai   ← Raw AI videos
  /compressed  ← Production-ready compressed assets
/lib
/styles
```

---

## Component Strategy

All components must be:
- Reusable and modular
- Animation-friendly (accept motion props)
- Responsive (desktop → tablet → mobile)
- Built with clean architecture

Prioritize: reusable sections, cards, CTA blocks, and motion wrapper components.

---

## AI Content Pipeline

**Images:** ChatGPT image gen → Gemini Nano Banana (primary free tools)

**Videos:**
1. Generate cinematic image (ChatGPT / Gemini)
2. Convert to short video loop (Kling AI / Hailuo AI / Luma Dream Machine)
3. Compress aggressively (under 3MB)
4. Deploy as hero background or section transition

**Preferred video aesthetic:** futuristic, minimal, cinematic, dark luxury, soft gradients, particles, holographic UI, abstract environments.

---

## Development Priorities

1. Performance
2. Visual quality
3. Reusability
4. Conversion
5. Accessibility
6. Scalability

---

## Code Generation Rules

When generating code:
- Use clean architecture and reusable patterns
- Modern React practices (server components where possible)
- Production-ready, no unnecessary complexity
- Elegant minimalism over complexity
- Heavily focus on aesthetics

When generating animations:
- Smooth, cinematic, subtle, performant

When generating layouts:
- Prioritize whitespace and premium spacing
- Strong visual hierarchy
- Modern SaaS/startup aesthetic

---

## Cost Philosophy

Maximum visual impact, minimum cost. Prefer free tiers, open-source libraries, AI-generated assets, and compressed files. Avoid paid APIs and over-engineering.

---

## Future Vision

This system will scale into a **premium landing page production agency** — multiple landing pages, reusable templates, fast client delivery powered by AI.
