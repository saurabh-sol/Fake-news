"use client"

import { useEffect, useRef } from "react"

export function RunningBorder({ radius = 20, speed = 3 }: { radius?: number; speed?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const rafRef = useRef<number>(0)
  const progressRef = useRef(0)
  const lastRef = useRef(0)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    function getPerimeter(w: number, h: number, r: number) {
      return 2 * (w - 2 * r) + 2 * (h - 2 * r) + 2 * Math.PI * r
    }

    function drawRoundedRect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
      ctx.beginPath()
      ctx.moveTo(x + r, y)
      ctx.lineTo(x + w - r, y)
      ctx.arcTo(x + w, y, x + w, y + r, r)
      ctx.lineTo(x + w, y + h - r)
      ctx.arcTo(x + w, y + h, x + w - r, y + h, r)
      ctx.lineTo(x + r, y + h)
      ctx.arcTo(x, y + h, x, y + h - r, r)
      ctx.lineTo(x, y + r)
      ctx.arcTo(x, y, x + r, y, r)
      ctx.closePath()
    }

    function frame(now: number) {
      const delta = now - (lastRef.current || now)
      lastRef.current = now

      const dpr = window.devicePixelRatio || 1
      const parent = canvas!.parentElement
      if (!parent) { rafRef.current = requestAnimationFrame(frame); return }

      const W = parent.offsetWidth
      const H = parent.offsetHeight

      // Resize canvas to match parent + dpr
      if (canvas!.width !== W * dpr || canvas!.height !== H * dpr) {
        canvas!.width = W * dpr
        canvas!.height = H * dpr
        canvas!.style.width = W + "px"
        canvas!.style.height = H + "px"
      }

      const ctx = canvas!.getContext("2d")!
      ctx.clearRect(0, 0, canvas!.width, canvas!.height)
      ctx.save()
      ctx.scale(dpr, dpr)

      const pad = 1.5
      const x = pad
      const y = pad
      const w = W - pad * 2
      const h = H - pad * 2
      const r = radius

      const perim = getPerimeter(w, h, r)
      const segLen = perim * 0.14  // length of the bright comet tail

      // Advance progress
      progressRef.current = (progressRef.current + delta / (speed * 1000)) % 1
      const offset = -(progressRef.current * perim)

      // ── 1. Static dim border ──
      drawRoundedRect(ctx, x, y, w, h, r)
      ctx.strokeStyle = "rgba(255, 255, 255, 0.08)"
      ctx.lineWidth = 1
      ctx.setLineDash([])
      ctx.shadowBlur = 0
      ctx.stroke()

      // ── 2. Wide outer glow (blue-white) ──
      drawRoundedRect(ctx, x, y, w, h, r)
      ctx.strokeStyle = "rgba(140, 200, 255, 0.55)"
      ctx.lineWidth = 7
      ctx.setLineDash([segLen, perim - segLen])
      ctx.lineDashOffset = offset
      ctx.shadowBlur = 18
      ctx.shadowColor = "rgba(100, 180, 255, 0.9)"
      ctx.stroke()

      // ── 3. Mid glow (white-blue) ──
      drawRoundedRect(ctx, x, y, w, h, r)
      ctx.strokeStyle = "rgba(220, 240, 255, 0.85)"
      ctx.lineWidth = 3
      ctx.setLineDash([segLen * 0.8, perim - segLen * 0.8])
      ctx.lineDashOffset = offset
      ctx.shadowBlur = 10
      ctx.shadowColor = "rgba(200, 230, 255, 1)"
      ctx.stroke()

      // ── 4. Crisp white core line ──
      drawRoundedRect(ctx, x, y, w, h, r)
      ctx.strokeStyle = "rgba(255, 255, 255, 1)"
      ctx.lineWidth = 2
      ctx.setLineDash([segLen * 0.55, perim - segLen * 0.55])
      ctx.lineDashOffset = offset
      ctx.shadowBlur = 6
      ctx.shadowColor = "rgba(255, 255, 255, 1)"
      ctx.stroke()

      ctx.restore()
      rafRef.current = requestAnimationFrame(frame)
    }

    rafRef.current = requestAnimationFrame(frame)
    return () => cancelAnimationFrame(rafRef.current)
  }, [radius, speed])

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0"
      style={{ zIndex: 1 }}
    />
  )
}
