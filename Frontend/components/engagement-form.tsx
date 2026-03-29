"use client"

import { useState } from "react"
import { Heart, MessageCircle, Repeat2, Link2, Zap, ChevronDown, CheckCircle2 } from "lucide-react"
import { RunningBorder } from "@/components/running-border"

const TIMESTAMP_OPTIONS = [
  { value: "1d", label: "1 Day" },
  { value: "1w", label: "1 Week" },
  { value: "1m", label: "1 Month" },
  { value: "1y", label: "1 Year" },
]

const VERIFIED_OPTIONS = [
  { value: "all", label: "All Users" },
  { value: "verified", label: "Verified Only" },
  { value: "unverified", label: "Unverified Only" },
]

export function EngagementForm() {
  const [tweetUrl, setTweetUrl] = useState("")
  const [likes, setLikes] = useState("")
  const [comments, setComments] = useState("")
  const [retweets, setRetweets] = useState("")
  const [verified, setVerified] = useState("all")
  const [timestamp, setTimestamp] = useState("1d")
  const [executed, setExecuted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleExecute = async () => {
    if (!tweetUrl) return
    setLoading(true)
    setError(null)
    setResult(null)
    setExecuted(false)

    try {
      const response = await fetch("https://fake-news-orq6.onrender.com/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tweet: tweetUrl,
          likes: parseInt(likes) || 0,
          retweets: parseInt(retweets) || 0,
          comments: parseInt(comments) || 0,
          verified: verified === "verified",
          time_range: timestamp,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to fetch analysis result")
      }

      const data = await response.json()
      setResult(data)
      setExecuted(true)
    } catch (err: any) {
      setError(err.message || "An error occurred")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="relative z-10 w-full max-w-2xl flex flex-col gap-6">
      <div className="relative w-full">
        {/* Running border effect */}
        <RunningBorder radius={20} speed={8} />
        {/* Card */}
        <div
          className="relative rounded-2xl bg-card/90 backdrop-blur-md p-6 sm:p-8 shadow-2xl"
          style={{ boxShadow: "0 0 60px var(--glow)" }}
        >
          {/* Tweet URL */}
          <div className="mb-5">
            <label className="mb-1.5 block text-xs font-medium text-muted-foreground uppercase tracking-widest">
              Tweets
            </label>
            <div className="relative flex items-center">
              <Link2 className="absolute left-3 h-5 w-5 text-muted-foreground" />
              <input
                type="text"
                value={tweetUrl}
                onChange={(e) => setTweetUrl(e.target.value)}
                placeholder="Enter tweet text or URL"
                className="w-full rounded-lg border border-border bg-input pl-10 pr-4 py-4 text-base text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              />
            </div>
          </div>

          {/* Stat Inputs */}
          <div className="mb-5 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <StatInput
              icon={<Heart className="h-4 w-4" />}
              label="Likes"
              value={likes}
              onChange={setLikes}
              placeholder="e.g. 500"
              color="oklch(0.70 0.22 15)"
            />
            <StatInput
              icon={<MessageCircle className="h-4 w-4" />}
              label="Comments"
              value={comments}
              onChange={setComments}
              placeholder="e.g. 100"
              color="oklch(0.60 0.20 230)"
            />
            <StatInput
              icon={<Repeat2 className="h-4 w-4" />}
              label="Retweets"
              value={retweets}
              onChange={setRetweets}
              placeholder="e.g. 200"
              color="oklch(0.65 0.18 165)"
            />
          </div>

          {/* Dropdowns */}
          <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <SelectField
              label="Account Type"
              value={verified}
              onChange={setVerified}
              options={VERIFIED_OPTIONS}
            />
            <SelectField
              label="Timestamp"
              value={timestamp}
              onChange={setTimestamp}
              options={TIMESTAMP_OPTIONS}
            />
          </div>

          {/* Execute Button */}
          <button
            onClick={handleExecute}
            disabled={loading || !tweetUrl}
            className="group relative w-full overflow-hidden rounded-lg py-3 px-6 text-sm font-semibold text-primary-foreground transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            style={{
              background: executed
                ? "oklch(0.60 0.20 230)" // Keeps the original blue/purple color when executed
                : "oklch(0.60 0.20 230)",
              boxShadow: loading || executed ? "none" : "0 0 24px var(--glow)",
            }}
          >
            {/* shimmer */}
            <span className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-white/10 to-transparent pointer-events-none" />

            <span className="relative flex items-center justify-center gap-2">
              {loading ? (
                <>
                  <span className="inline-block h-4 w-4 rounded-full border-2 border-primary-foreground/30 border-t-primary-foreground animate-spin" />
                  Analyzing…
                </>
              ) : executed ? (
                <>
                  <CheckCircle2 className="h-4 w-4" />
                  Analyzed!
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4" />
                  Get Result
                </>
              )}
            </span>
          </button>

          {error && (
            <p className="mt-4 text-center text-sm text-red-500 font-medium">
              {error}
            </p>
          )}
        </div>
      </div>

      {/* Result Section */}
      {result && (
        <div className="relative w-full animate-in fade-in slide-in-from-bottom-4 duration-500 mt-6">
          <RunningBorder radius={20} speed={8} />
          <div 
            className="relative rounded-2xl bg-card/90 backdrop-blur-md p-6 sm:p-8 shadow-2xl"
            style={{ boxShadow: "0 0 60px var(--glow)" }}
          >
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Zap className="h-5 w-5 text-yellow-500" />
              Analysis Result
            </h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <ResultItem 
                label="Final Verdict" 
                value={result.verdict} 
                subValue={`${(result.final_score * 100).toFixed(1)}% Confidence`}
                highlight={true}
                color={result.verdict === "Likely TRUE" ? "text-green-500" : result.verdict === "Likely FALSE" ? "text-red-500" : "text-yellow-500"}
              />
              <ResultItem 
                label="Sentiment" 
                value={result.sentiment.label} 
                subValue={`${(result.sentiment.confidence * 100).toFixed(1)}% Confidence`}
                color="text-foreground"
                subColor="text-muted-foreground"
              />
              <ResultItem 
                label="Truth Score" 
                value={(result.truth * 100).toFixed(1) + "%"} 
              />
              <ResultItem 
                label="Similarity Score" 
                value={(result.similarity * 100).toFixed(1) + "%"} 
              />
              <ResultItem 
                label="User Credibility" 
                value={(result.credibility * 100).toFixed(1) + "%"} 
              />
            </div>

            {result.keywords && result.keywords.length > 0 && (
              <div className="mt-8">
                <label className="mb-2 block text-xs font-medium text-muted-foreground uppercase tracking-widest">
                  Extracted Keywords
                </label>
                <div className="flex flex-wrap gap-2">
                  {result.keywords.map((kw: string, i: number) => (
                    <span key={i} className="px-3 py-1 rounded-full bg-secondary text-secondary-foreground text-xs font-medium">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

function ResultItem({ label, value, subValue, highlight, color, subColor }: { label: string, value: string, subValue?: string, highlight?: boolean, color?: string, subColor?: string }) {
  return (
    <div className={`p-4 rounded-xl bg-input/50 border border-border/50 ${highlight ? 'sm:col-span-2 ring-2 ring-primary/20' : ''}`}>
      <label className="mb-1 block text-[10px] font-medium text-muted-foreground uppercase tracking-tighter">
        {label}
      </label>
      <div className={`text-xl font-bold ${color || 'text-foreground'}`}>
        {value}
      </div>
      {subValue && (
        <div className={`text-xs mt-1 font-medium ${subColor || 'text-muted-foreground'}`}>
          {subValue}
        </div>
      )}
    </div>
  )
}

/* ─── Sub-components ─── */

function StatInput({
  icon,
  label,
  value,
  onChange,
  placeholder,
  color,
}: {
  icon: React.ReactNode
  label: string
  value: string
  onChange: (v: string) => void
  placeholder: string
  color: string
}) {
  return (
    <div>
      <label className="mb-1.5 flex items-center gap-1.5 text-xs font-medium text-muted-foreground uppercase tracking-widest">
        <span style={{ color }}>{icon}</span>
        {label}
      </label>
      <input
        type="number"
        min={0}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-lg border border-border bg-input px-3 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
      />
    </div>
  )
}

function SelectField({
  label,
  value,
  onChange,
  options,
}: {
  label: string
  value: string
  onChange: (v: string) => void
  options: { value: string; label: string }[]
}) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium text-muted-foreground uppercase tracking-widest">
        {label}
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full appearance-none rounded-lg border border-border bg-input px-3 py-2.5 pr-9 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all cursor-pointer"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-popover">
              {opt.label}
            </option>
          ))}
        </select>
        <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      </div>
    </div>
  )
}
