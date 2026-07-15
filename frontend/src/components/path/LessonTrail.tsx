import type { PathLesson } from "@/types"
import { PathNode } from "./PathNode"

/*
 * The winding lesson road for a unit page (Phase 23.4b). Nodes are placed along
 * a sine curve and the road itself is that same curve sampled finely — so the
 * trail genuinely curls rather than stepping left/right, and every node sits
 * exactly on the road.
 */
const SPACING = 124 // vertical gap between nodes
const AMP = 62 // how far the road swings sideways
const WIDTH = 260
const TOP = 52

/** Node centre for index `i` (fractional `i` samples the road between nodes). */
function pointAt(i: number) {
  return { x: WIDTH / 2 + AMP * Math.sin(i * (Math.PI / 2)), y: TOP + i * SPACING }
}

function roadPath(count: number): string {
  if (count < 2) return ""
  const steps: string[] = []
  for (let t = 0; t <= count - 1; t += 0.04) {
    const { x, y } = pointAt(t)
    steps.push(`${x.toFixed(1)},${y.toFixed(1)}`)
  }
  return `M${steps.join(" L")}`
}

export function LessonTrail({ lessons, accent }: { lessons: PathLesson[]; accent: string }) {
  const height = TOP + Math.max(0, lessons.length - 1) * SPACING + 96
  const d = roadPath(lessons.length)

  return (
    <div className="relative mx-auto" style={{ width: WIDTH, height }}>
      <svg width={WIDTH} height={height} className="absolute inset-0" aria-hidden="true">
        {d && (
          <>
            {/* the road */}
            <path
              d={d}
              fill="none"
              stroke="hsl(var(--surface-2))"
              strokeWidth={18}
              strokeLinecap="round"
            />
            {/* centre markings, tinted to the unit accent */}
            <path
              d={d}
              fill="none"
              stroke={accent}
              strokeWidth={2}
              strokeDasharray="2 14"
              strokeLinecap="round"
              opacity={0.55}
            />
          </>
        )}
      </svg>

      {lessons.map((lesson, i) => {
        const { x, y } = pointAt(i)
        return (
          <div
            key={lesson.id}
            className="absolute"
            style={{ left: x, top: y, transform: "translate(-50%, -50%)" }}
          >
            <PathNode
              state={lesson.state}
              label={lesson.title}
              accent={accent}
              crownLevel={lesson.crown}
            />
          </div>
        )
      })}
    </div>
  )
}
