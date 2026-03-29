import { Twitter } from "lucide-react"

export function Footer() {
  return (
    <footer className="border-t border-border bg-background px-6 py-8">
      <div className="mx-auto flex max-w-5xl flex-col items-center justify-between gap-4 sm:flex-row">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Twitter className="h-4 w-4 text-primary" fill="currentColor" />
          <span className="font-semibold text-foreground">XBoost</span>
          <span>— Twitter Engagement Tool</span>
        </div>
        <p className="text-xs text-muted-foreground">
          &copy; {new Date().getFullYear()} XBoost. All rights reserved.
        </p>
      </div>
    </footer>
  )
}
