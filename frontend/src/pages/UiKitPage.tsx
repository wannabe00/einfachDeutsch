import { SectionCard } from "@/components/ui/SectionCard"
import { LockOverlay } from "@/components/path/LockOverlay"
import { PathNode, type NodeState } from "@/components/path/PathNode"
import { NextUp } from "@/components/path/NextUp"
import { EnergyMeter } from "@/components/path/EnergyMeter"
import { resolveAccent, sectionColor } from "@/lib/sections"

/*
 * Design v3 "dark + depth" living style guide (Phase 23.2). A reference page for
 * the shared learning-path components, so the visual language can be reviewed
 * before real pages are built on it. Route: /ui-kit.
 */
export default function UiKitPage() {
  const nodeStates: NodeState[] = ["completed", "current", "available", "locked"]

  return (
    <div className="flex flex-col gap-10">
      <header>
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">Design v3 — UI kit</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Dark + depth components for the learning path (Phase 23.2).
        </p>
      </header>

      <Group title="Section cards + accents">
        <div className="grid gap-4 sm:grid-cols-3">
          {[0, 1, 2].map((i) => (
            <SectionCard key={i} accent={sectionColor(i)} glow>
              <div className="p-5">
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Unit {i + 1}
                </p>
                <p className="mt-1 font-bold">Kennenlernen</p>
                <p className="mt-1 text-sm text-muted-foreground">5 lessons · 3 done</p>
              </div>
            </SectionCard>
          ))}
        </div>
      </Group>

      <Group title="Path nodes">
        <div className="flex flex-wrap items-start gap-6">
          {nodeStates.map((state) => (
            <PathNode
              key={state}
              state={state}
              label={state}
              accent={sectionColor(1)}
              crownLevel={state === "completed" ? 1 : 0}
              onClick={() => {}}
            />
          ))}
        </div>
      </Group>

      <Group title="Next up">
        <NextUp
          title="Lektion 4 · Im Café"
          subtitle="Unit 2 — bestellen & bezahlen"
          href="#"
          accent={resolveAccent(undefined, 1)}
        />
      </Group>

      <Group title="Energy meter">
        <div className="flex flex-col gap-3">
          <EnergyMeter energy={3} max={3} />
          <EnergyMeter energy={1} max={3} secondsUntilNext={8340} />
          <EnergyMeter energy={0} max={3} secondsUntilNext={140} />
          <EnergyMeter energy={0} max={3} premium />
        </div>
      </Group>

      <Group title="Lock / blur overlay">
        <div className="grid gap-4 sm:grid-cols-2">
          <LockOverlay locked={false}>
            <SectionCard accent={sectionColor(3)}>
              <div className="p-5">
                <p className="font-bold">Unlocked lesson</p>
                <p className="mt-1 text-sm text-muted-foreground">You can open this.</p>
              </div>
            </SectionCard>
          </LockOverlay>
          <LockOverlay locked hint="Finish the previous lesson to unlock">
            <SectionCard accent={sectionColor(4)}>
              <div className="p-5">
                <p className="font-bold">Locked lesson</p>
                <p className="mt-1 text-sm text-muted-foreground">Hidden until you reach it.</p>
              </div>
            </SectionCard>
          </LockOverlay>
        </div>
      </Group>
    </div>
  )
}

function Group({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">{title}</h2>
      {children}
    </section>
  )
}
