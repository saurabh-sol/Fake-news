import { ShieldCheck, Gauge, Clock3, Users } from "lucide-react"

const features = [
  {
    icon: <ShieldCheck className="h-5 w-5" />,
    title: "Safe & Compliant",
    description: "Stays within Twitter API rate limits, no bans.",
  },
  {
    icon: <Gauge className="h-5 w-5" />,
    title: "Real-time Analytics",
    description: "Watch engagement metrics climb live.",
  },
  {
    icon: <Clock3 className="h-5 w-5" />,
    title: "Scheduled Delivery",
    description: "Spread engagement naturally over your chosen window.",
  },
  {
    icon: <Users className="h-5 w-5" />,
    title: "Targeted Audience",
    description: "Filter by verified status for authentic reach.",
  },
]

export function FeaturesStrip() {
  return (
    <section className="relative border-t border-border bg-card/40 px-6 py-16">
      <div className="mx-auto max-w-5xl">
        <h2 className="mb-10 text-center text-2xl font-bold text-foreground tracking-tight">
          Everything you need to grow on{" "}
          <span className="text-primary">X / Twitter</span>
        </h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((f) => (
            <div
              key={f.title}
              className="group rounded-xl border border-border bg-card/60 p-5 transition-all hover:border-primary/40 hover:bg-card"
              style={{ boxShadow: "0 0 0 0 var(--glow)" }}
            >
              <div
                className="mb-3 flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors"
              >
                {f.icon}
              </div>
              <h3 className="mb-1 text-sm font-semibold text-foreground">
                {f.title}
              </h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {f.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
