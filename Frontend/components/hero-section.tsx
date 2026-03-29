"use client"

import { useState } from "react"
import { EngagementForm } from "./engagement-form"

export function HeroSection() {
  return (
    <section className="relative flex flex-col items-center justify-center min-h-screen px-4 py-20 overflow-hidden">
      {/* Animated grid background — slow drift */}
      <div
        className="absolute inset-0 pointer-events-none grid-drift"
        style={{
          backgroundImage: `
            linear-gradient(var(--grid-color) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid-color) 1px, transparent 1px)
          `,
          backgroundSize: "40px 40px",
        }}
      />

      {/* Breathing radial glow */}
      <div
        className="absolute inset-0 pointer-events-none breathing-glow"
        style={{
          background:
            "radial-gradient(ellipse 80% 55% at 50% 0%, oklch(0.60 0.20 230 / 0.22) 0%, transparent 70%)",
        }}
      />

      {/* Secondary breathing glow — bottom pulse */}
      <div
        className="absolute inset-0 pointer-events-none breathing-glow-slow"
        style={{
          background:
            "radial-gradient(ellipse 60% 40% at 50% 100%, oklch(0.55 0.18 220 / 0.10) 0%, transparent 65%)",
        }}
      />

      {/* Top badge */}
      <div className="relative z-10 mb-6 flex items-center gap-2 rounded-full border border-border bg-card/60 px-4 py-1.5 text-xs text-muted-foreground backdrop-blur-sm">
        <span className="inline-block h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
        Financial Fake News Detection
      </div>

      {/* Headline */}
      <h1 className="relative z-10 text-center text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl text-balance mb-4">
        Discover the Truth in{" "}
        <span
          className="text-primary"
          style={{ textShadow: "0 0 30px var(--glow)" }}
        >
          Financial Tweets
        </span>
      </h1>

      <p className="relative z-10 text-center text-muted-foreground text-base sm:text-lg max-w-xl mb-12 text-pretty leading-relaxed">
        Paste any financial tweet, provide its engagement metrics, and our AI engine will analyze sentiment, news similarity, and user credibility to verify its authenticity.
      </p>

      {/* Form card */}
      <EngagementForm />


    </section>
  )
}
