import { Twitter } from "lucide-react"

export function Navbar() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex h-14 items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-md">
      <div className="flex items-center gap-2.5">
        <div
          className="flex h-7 w-7 items-center justify-center rounded-md bg-primary"
          style={{ boxShadow: "0 0 12px var(--glow)" }}
        >
          <Twitter className="h-4 w-4 text-primary-foreground" fill="currentColor" />
        </div>
        <span className="text-sm font-semibold text-foreground tracking-tight">
          XBoost
        </span>
        <span className="hidden sm:inline-block rounded-full border border-primary/40 bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
          Beta
        </span>
      </div>

      <nav className="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
        <a href="#" className="hover:text-foreground transition-colors">
          How it Works
        </a>
        <a href="#" className="hover:text-foreground transition-colors">
          Pricing
        </a>
        <a href="#" className="hover:text-foreground transition-colors">
          Docs
        </a>
      </nav>

      <div className="flex items-center gap-3">
        <button className="hidden sm:inline-flex rounded-md border border-border bg-secondary px-4 py-1.5 text-xs font-medium text-foreground hover:bg-muted transition-colors">
          Log in
        </button>
        <button
          className="inline-flex rounded-md px-4 py-1.5 text-xs font-medium text-primary-foreground transition-all hover:opacity-90"
          style={{ background: "oklch(0.60 0.20 230)" }}
        >
          Get Started
        </button>
      </div>
    </header>
  )
}
