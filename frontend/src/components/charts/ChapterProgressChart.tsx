import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

import type { Word } from "@/types"

interface ChapterProgressChartProps {
  words: Word[]
}

const BUCKETS = [
  { label: "New", color: "hsl(var(--muted-foreground))" },
  { label: "Learning", color: "hsl(var(--article-das))" },
  { label: "Review", color: "hsl(var(--accent))" },
  { label: "Learned", color: "hsl(var(--success))" },
]

function bucketIndex(word: Word): number {
  const p = word.progress
  if (!p || p.repetitions === 0) return 0
  if (p.interval <= 6) return 1
  if (p.interval <= 21) return 2
  return 3
}

export function ChapterProgressChart({ words }: ChapterProgressChartProps) {
  const counts = [0, 0, 0, 0]
  for (const w of words) counts[bucketIndex(w)] += 1
  const data = BUCKETS.map((b, i) => ({ ...b, count: counts[i] }))

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <h3 className="mb-4 text-sm font-medium text-foreground">
        Words by progress
      </h3>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
          <XAxis
            dataKey="label"
            tick={{ fontSize: 12, fill: "hsl(var(--muted-foreground))" }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            allowDecimals={false}
            tick={{ fontSize: 12, fill: "hsl(var(--muted-foreground))" }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            cursor={{ fill: "hsl(var(--muted))" }}
            contentStyle={{
              background: "hsl(var(--background))",
              border: "1px solid hsl(var(--border))",
              borderRadius: 8,
              fontSize: 12,
            }}
            labelStyle={{ color: "hsl(var(--foreground))" }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((b, i) => (
              <Cell key={i} fill={b.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
